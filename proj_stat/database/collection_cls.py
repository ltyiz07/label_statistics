import os
import json
import datetime
import tarfile
from unicodedata import name
import xmltodict
from proj_stat import config

from typing import TypedDict



"""
추후에 필요한 통계데이터들을 클래스 내부에 정의 하고 사용 -> 성능, 기능, 편의성 등에서 효율적
"""

##### Annotation #####################################################################
class Annotation(dict):
    """
    annotation info about a single image with multiples objects
    """
    def __init__(self, *vargs, **kwargs):
        if len(vargs) > 0:
            mapper = vargs[0]
        else:
            mapper = kwargs
        self["tar_path"]: str = mapper.get("tar_path")
        self["tar_name"]: str = mapper.get("tar_name")
        self["image_path"]: str = mapper.get("image_path")
        self["image_name"]: str = mapper.get("image_name")
        self["size"]: tuple[int] = mapper.get("size")       # width, height
        self["objects"]: list[TypedDict("Object", {"name": str, "bndbox": dict})] = mapper.get("objects")     # keys: {"name", "bndbox"}
        self["edited_date"]: datetime.datetime = mapper.get("edited_date")

    @property
    def tar_path(self): return self.get("tar_path")
    @property
    def image_path(self): return self.get("image_path")
    @property
    def image_id(self): return self.get("image_id")
    @property
    def size(self): return self.get("size")
    @property
    def objects(self): return self.get("objects")
    @property
    def edited_date(self): return self.get("edited_date")

##### Dataset #####################################################################
class Dataset(dict):
    def __init__(self, *vargs, **kwargs):
        if len(vargs) > 0:
            mapper = vargs[0]
        else:
            mapper = kwargs
        self["tar_path"]: str = mapper.get("tar_path")
        self["tar_name"]: str = mapper.get("tar_name")
        self["dataset_path"]: str = mapper.get("dataset_path")
        self["dataset_name"]: str = mapper.get("dataset_name")
        self["dataset_hash"]: str = mapper.get("dataset_hash")
        self["image_names"]: list[str] = mapper.get("image_names")
        self["edited_date"]: datetime.datetime = mapper.get("edited_date")

    @property
    def tar_path(self): return self.get("tar_path")
    @property
    def dataset_path(self): return self.get("dataset_path")
    @property
    def dataset_hash(self): return self.get("dataset_hash")
    @property
    def image_ids(self): return self.get("image_ids")
    @property
    def edited_date(self): return self.get("edited_date")


##### functions #####################################################################

def parse_annotations_from_tar(tar_path: str):
    """
    extract Annotations/*.xml files and parse content
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


def get_hash_from_tar(tar_path: str, annotations: list[str]):
    """
    generate hash from tar files content, using filenames, file-sizes, file-mtime
    """
    hash_str: str = None
    with tarfile.open(tar_path, 'r') as tar:
        # return hash(tuple( chain.from_iterable((t.name, t.size, t.mtime) for t in tar) ))
        for t in tar:
            if os.path.basename(t.name) == "Annotations":
                annotation_dir = t.name
                break
        return str(hash(tuple( tar.getmember("/".join((annotation_dir, annot_id + ".xml"))).chksum for annot_id in annotations if annot_id )))
