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


def get_all_datasets_count():
    # len(datasets_col.find({}))
    return datasets_col.count_documents({})

def get_all_datasets():
    cursor = datasets_col.find({}, {"_id": False})
    return dict(dataset_ids = [c["dataset_id"] for c in cursor])
    # for c in cursor:
        # ids.append(c.get("dataset_id"))
    # return {"dataset_ids": ids}

def get_iamge_list_from_tar(dataset_id):
    result = datasets_col.find_one({"dataset_id": dataset_id})
    return [annot.get("image_id") for annot in result.get("annotations")]

def get_image_from_tar(dataset_id, image_id):
    result = datasets_col.find_one({"dataset_id": dataset_id})
    for image_info in result.get("annotations"):
        if image_info.get("image_id") == image_id:
            print(image_info.get("image_id") )
            image_path = image_info.get("image_path")
            with tarfile.open(result.get("dataset_path"), 'r') as tar:
                # print(tar.extractfile(image_path).read())
                return io.BytesIO(tar.extractfile(image_path).read())
    
    return None

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

def get_stats(dataset_id: str, queries: set[str]):
    stat = dict()

    result = datasets_col.find_one({"dataset_id": dataset_id}).get("annotations")

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

########################################################################################
def _get_object_size(bnd_box: map):
    bnd_box = {k: float(v) for k, v in bnd_box.items()}
    return (bnd_box.get("xmax") - bnd_box.get("xmin")) * (bnd_box.get("ymax") - bnd_box.get("ymin"))


def update_database():
    datasets_col = mongo_db.create_datasets_col()
    datasets_col.insert_many( tuple(get_parsed_dict_from_tar(tar) for tar in get_tarfiles()) )

def init_datasets_col():
    return mongo_db.create_datasets_col()

def get_datasets_col():
    return mongo_db.get_datasets_col()

def get_tarfiles(source_dir=config.TAR_SOURCE):
    """
    get tar file list from tar data source(env)

    Args:
        source_dir (str): tar file source directory with absolute path
    Returns
         ([str]): list of tar files (*.tar)
    """
    source_dir = os.path.join(source_dir, "*.tar")
    return glob.glob(source_dir)


def get_hash_from_tar(tar_path: str):
    """
    generate hash from tar files content, using filenames, file-sizes, file-mtime
    """
    hash_str: str = None
    with tarfile.open(tar_path, 'r') as tar:
        # return hash(tuple( chain.from_iterable((t.name, t.size, t.mtime) for t in tar) ))
        return str(hash(tuple( t.chksum for t in tar) ))

def get_parsed_dict_from_tar(tar_path: str):
    """
    use this api for insert into mongodb
    """
    return _matching_datasets_validator(tar_path)

def _matching_datasets_validator(tar_path: str):
    """
    convert parsed annotation dict to 
    image_id : filename.rpartision(r"/")[2].partision(".")[0]
    Args:
        tar_path (str): absolute path of .tar file
    Returns:
    """
    dict_out = dict()
    dict_out["dataset_path"] = os.path.realpath(tar_path)
    dict_out["dataset_id"] = os.path.splitext(os.path.basename(tar_path))[0]
    dict_out["dataset_hash"] = get_hash_from_tar(tar_path)
    dict_out["annotations"] = _matching_annotations(tar_path)
    return dict_out

def _matching_annotations(tar_path: str):
    """
    sub method for method _matching_datasets_validator
    set value of annotations at dict
    """
    annots = []
    for name, content in _parse_annotations_from_tar(tar_path).items():
        annots.append({
            "image_path": name.replace("Annotations", "JPEGImages").replace("xml", "jpg"),
            "image_id": name.rpartition(r"/")[2].partition(".")[0],
            "size": {k: int(v) for k, v in content["annotation"]["size"].items()},
            "objects": content["annotation"]["object"]
        })
    return annots

def _parse_annotations_from_tar(tar_path: str):
    """
    extrace annotations/*.xml files and parse content
    to (dict) type

    Args:
        tar_path (str): absolute path of tar file
    Returns:
            (dict): {image_id (str), annotations (dict)}
    """
    with tarfile.open(tar_path, "r") as tar:
        return {
            t.name: xmltodict.parse(tar.extractfile(t.name).read())
            for t in tar
            if t.name.endswith(".xml") and os.path.basename(os.path.dirname(t.name)) == "Annotations"
        }