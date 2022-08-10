import io
import os
from pathlib import Path
import glob
import tarfile
from itertools import chain
from functools import reduce
import operator
from flask_sqlalchemy import Pagination
import xmltodict

from proj_stat import config
from proj_stat.database import mongo_db
from bson import json_util


datasets_col = mongo_db.get_datasets_col()
annotations_col = mongo_db.get_annotations_col()


class DatasetPagination:
    index_gap = 10
    index_list = [ obj.get("_id") for e, obj in enumerate(datasets_col.find({}, {"_id": 1}).sort("_id", 1)) if e % 10 == 0 ]
    page_count = len(index_list)

    def __init__(self, page:int=0):
        self.page = int(page)

    @property
    def begin_index(self):
        return self.index_list[int(self.page)]

    @classmethod
    def update(cls):
        cls.index_list = [ obj.get("_id") for e, obj in enumerate(datasets_col.find({}, {"_id": 1}).sort("_id", 1)) if e % 10 == 0 ]
        cls.page_count = len(cls.index_list)

class ImageListPagination:
    index_gap = 20

    def __init__(self, tar_name: str, dataset_name: str, page: int):
        self.page = page
        name_list = datasets_col.find_one({"tar_name": tar_name, "dataset_name": dataset_name}).get("image_names")
        self.page_count = len(name_list) // self.index_gap


def get_all_datasets_count() -> int:
    return datasets_col.count_documents({})

def get_all_datasets() -> list[str]:
    cursor = datasets_col.find({}, {"_id": False})
    return [{"tar_name": c["tar_name"], "dataset_name": c["dataset_name"]} for c in cursor]

def get_datasets(pagination: DatasetPagination):
    cursor = datasets_col\
        .find({"_id": {"$gte": pagination.begin_index}})\
            .sort("_id", 1)\
                .limit(pagination.index_gap)
    return [{"tar_name": c["tar_name"], "dataset_name": c["dataset_name"]} for c in cursor]

def get_image_list(tar_name, dataset_name) -> list[str]:
    return datasets_col.find_one({"tar_name": tar_name, "dataset_name": dataset_name}).get("image_names")

def get_image_from_tar(tar_name, image_name) -> io.BytesIO:
    annot = annotations_col.find_one({"tar_name": tar_name, "image_name": image_name})
    with tarfile.open(os.path.join(config.TAR_SOURCE, annot.get("tar_path")), 'r') as tar:
        return io.BytesIO(tar.extractfile(annot.get("image_path")).read())

def get_stats(tar_name: str, dataset_name: str, queries: set[str]) -> dict:
    stat = dict()
    image_names = datasets_col.find_one({"tar_name": tar_name, "dataset_name": dataset_name}, {"_id": False}).get("image_names")
    result = [o for o in annotations_col.find({"tar_name": tar_name, "image_name": {"$in": image_names}}, {"_id": False})]

    if "images_sizes" in queries:
        stat["images_size"] = list({(annot.get("size").get("width"), annot.get("size").get("height")) for annot in result})
    if "images_count" in queries:
        # number of images in datasets
        stat["images_count"] = len(result)
    if "images" in queries:
        stat["images"] = list(annot.get("image_id") for annot in result)
    if "objects_count" in queries:
        # number of objects in datasets
        class_count = 0
        stat["objects_count"] = sum(len(annot.get("objects")) for annot in result)
    if "objects_unique_count" in queries:
        stat["objects_unique_count"] = len(set(obj.get("name") for annot in result for obj in annot.get("objects")))
    if "objects_unique" in queries:
        stat["objects_unique"] = list(set(obj.get("name") for annot in result for obj in annot.get("objects")))
        # pass
    if "objects" in queries:
        objects_dict = dict()
        for annot in result:
            for obj in annot.get("objects"):
                obj_name = obj.get("name")
                objects_dict[obj_name] = objects_dict.setdefault(obj_name, 0) + 1
        stat["objects"] = objects_dict
    if "objects_sizes_avg" in queries:
        stat["objects_sizes_avg"] = \
            sum(_get_object_size(obj.get("bndbox")) for annot in result for obj in annot.get("objects")) \
                / sum(len(annot.get("objects")) for annot in result)

    return stat

def get_stat(tar_name: str, image_name: str, queries: set[str]) -> dict:
    stat = dict()
    result = annotations_col.find_one({"tar_name": tar_name, "image_name": image_name}, {"_id": False})
    for k, v in result.items():
        stat[k] = v

    if "images_sizes" in queries:
        stat["images_size"] = list((result.get("size").get("width"), result.get("size").get("height")))
    if "images_count" in queries:
        # number of images in datasets
        stat["images_count"] = 1
    if "images" in queries:
        stat["images"] = [result.get("image_id")]
    if "objects_count" in queries:
        # number of objects in datasets
        class_count = 0
        stat["objects_count"] = len(result.get("objects"))
    if "objects_unique_count" in queries:
        stat["objects_unique_count"] = len(set(obj.get("name") for obj in result.get("objects")))
    if "objects_unique" in queries:
        stat["objects_unique"] = list(set(obj.get("name") for obj in result.get("objects")))
        # pass
    if "objects" in queries:
        objects_dict = dict()
        for obj in result.get("objects"):
            obj_name = obj.get("name")
            objects_dict[obj_name] = objects_dict.setdefault(obj_name, 0) + 1
        stat["objects"] = objects_dict
    if "objects_sizes_avg" in queries:
        stat["objects_sizes_avg"] = \
            sum(_get_object_size(obj.get("bndbox")) for obj in result.get("objects")) \
                / len(result.get("objects"))

    return stat


def get_object_count_all():
    """Returns min - max object counts at single image
    """
    cursor = annotations_col.find({}, {"_id": False})
    objects_counter = dict()
    for annot in cursor:
        for k, v in annot.get("object_count").items():
            objects_counter[k] = v if objects_counter.get(k, 0) < v else objects_counter[k]
    return objects_counter

def get_images_with_objects(objects_list):
    search_target = "object_count."
    search_query = {search_target + obj : {"$exists": True} for obj in objects_list}
    sort_query = [(search_target + obj, -1) for obj in objects_list]
    cursor = annotations_col.find(search_query, {"tar_name": 1, "image_name": 1}).sort(sort_query)
    return [ {"tar_name": c.get("tar_name"), "image_name": c.get("image_name")} for c in cursor]


########################################################################################
def _get_object_size(bnd_box: map):
    bnd_box = {k: float(v) for k, v in bnd_box.items()}
    return (bnd_box.get("xmax") - bnd_box.get("xmin")) * (bnd_box.get("ymax") - bnd_box.get("ymin"))

