import io
import os
from pathlib import Path
import glob
import tarfile
from itertools import chain
from functools import reduce
import operator
import xmltodict

from proj_stat import config
from proj_stat.database import mongo_db
from bson import json_util


datasets_col = mongo_db.get_datasets_col()
annotations_col = mongo_db.get_annotations_col()


def get_all_datasets_count() -> int:
    # len(datasets_col.find({}))
    return datasets_col.count_documents({})

def get_all_datasets() -> list[str]:
    cursor = datasets_col.find({}, {"_id": False})
    return [c["dataset_id"] for c in cursor]
    # for c in cursor:
        # ids.append(c.get("dataset_id"))
    # return {"dataset_ids": ids}

def get_image_list_from_tar(dataset_id) -> list[str]:
    return datasets_col.find_one({"dataset_id": dataset_id}).get("annotations")

def get_image_from_tar(dataset_id, image_id) -> io.BytesIO:
    dataset = datasets_col.find_one({"dataset_id": dataset_id})
    annot = annotations_col.find_one({"image_id": {"$in": dataset.get("annotations")}})
    with tarfile.open(os.path.join(config.TAR_SOURCE, dataset.get("dataset_path")), 'r') as tar:
        return io.BytesIO(tar.extractfile(annot.get("image_path")).read())


def get_images_from_tar():
    pass

def get_image_stat(dataset_id: str, image_id: str, queries: set[str]):
    """
    maybe have to change mongodb annotations schema as:
        annotation: [{"image_id": "..", "image_path" ...}, {"iamge_id": "..", }]
        -----> to dict
        annotation: {"test_image_id_1234": {"image_path": ...}, "test_image_id_4321": {"iamge_id": "..", }}
    """
    stat = dict()

    result = datasets_col.find_one({"dataset_id": dataset_id}).get("annotations")
    return stat

def get_stats(dataset_id: str, queries: set[str]) -> dict:
    stat = dict()
    result = [o for o in annotations_col.find({"dataset_id": dataset_id}, {"_id": False})]

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

def get_stat(dataset_id: str, image_id: str, queries: set[str]) -> dict:
    stat = dict()
    result = annotations_col.find_one({"dataset_id": dataset_id, "image_id": image_id}, {"_id": False})
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


########################################################################################
def _get_object_size(bnd_box: map):
    bnd_box = {k: float(v) for k, v in bnd_box.items()}
    return (bnd_box.get("xmax") - bnd_box.get("xmin")) * (bnd_box.get("ymax") - bnd_box.get("ymin"))

