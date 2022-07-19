import os
import json
import tarfile
from unicodedata import name
import xmltodict
from proj_stat import config

from typing import TypedDict


"""
추후에 필요한 통계데이터들을 클래스 내부에 정의 하고 사용 -> 성능, 기능, 편의성 등에서 효율적
"""

class Dataset(dict):
    def __init__(self, *vargs, **kwargs):
        if len(vargs) > 0:
            mapper = vargs[0]
        else:
            mapper = kwargs
        self["dataset_id"]: str = mapper.get("dataset_id")
        self["dataset_path"]: str = mapper.get("dataset_path")
        self["dataset_hash"]: str = mapper.get("dataset_hash")
        self["annotations"]: list[str] = mapper.get("annotations")

    @classmethod
    def from_parsed_annotations(cls, tar_path):

        """
        Values:
            "dataset_id": tar_filename + ":" + imagesets_filename      ## using only filename without format
            "dataset_path": filename with files format
            "dataset_hash": get_hash_from_tar(tar_path),        # check method below
            "annotations": list of image_filenames      # content of the imagesets_file ex. all.txt
        """
        cls_list = []
        with tarfile.open(tar_path, 'r') as tar:
            sub_sets = [
                t.name
                for t in tar
                if t.name.endswith(".txt") and os.path.basename(os.path.dirname(t.name)) == "ImageSets"
            ]
            for sub_set in sub_sets:
                tar.extractfile(sub_set)
                annotations = [l.decode().strip() for l in tar.extractfile(sub_set)]
                cls_list.append(cls({
                    "dataset_id": get_id_from_path(tar_path) + ":" + get_id_from_path(sub_set),
                    "dataset_path": os.path.basename(os.path.realpath(tar_path)),
                    "dataset_hash": get_hash_from_tar(os.path.join(config.TAR_SOURCE, tar_path), annotations),
                    "annotations": annotations        # content of the imagesets_file ex. all.txt
                }))
        return cls_list

    # @staticmethod
    # def get_stats(annotations: list[Annotation]):
    #     pass


class Annotation(dict):
    """
    annotation info about a single image with multiples objects
    """
    def __init__(self, *vargs, **kwargs):
        if len(vargs) > 0:
            mapper = vargs[0]
        else:
            mapper = kwargs
        self["image_id"]: str = mapper.get("image_id")
        self["image_path"]: str = mapper.get("image_path")
        self["dataset_path"]: str = mapper.get("dataset_path")
        self["size"]: tuple[int] = mapper.get("size")
        self["objects"]: list[TypedDict("Object", {"name": str, "bndbox": dict})] = mapper.get("objects")     # keys: {"name", "bndbox"}

    @classmethod
    def from_parsed_annotations(cls, tar_path, annotations):
        annotation_list = []
        for name, objs in annotations.items():
            annotation_list.append(cls({
                "image_id": name.rpartition(r"/")[2].partition(".")[0],
                "dataset_path": os.path.basename(os.path.realpath(tar_path)),
                "image_path": name.replace("Annotations", "JPEGImages").replace("xml", "jpg"),
                "size": {k: int(v) for k, v in objs["annotation"]["size"].items()},
                "objects": objs["annotation"]["object"]
            }))
        return annotation_list


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

def parse_subsets_from_tar(tar_path: str):
    """
    extract ImageSets/*.txt files and parse content
    to (dict) type

    Args:
        tar_path (str): absolute path of tar file
    Returns:
            (dict): {subset_id (str), image_id}
                - subset_id is filename of .txt file without format
                - image_id is filename from .txt file without format
    """
    with tarfile.open(tar_path, "r") as tar:
        return {
            t.name: xmltodict.parse(tar.extractfile(t.name).read())
            for t in tar
            if t.name.endswith(".txt") and os.path.basename(os.path.dirname(t.name)) == "ImageSets"
        }


def get_subsets_from_tar(tar_path: str):
    with tarfile.open(tar_path, 'r') as tar:
        subset_names = [
            t.name
            for t in tar
            if t.name.endswith(".txt") and os.path.basename(os.path.dirname(t.name)) == "ImageSets"
        ]
        return subset_names



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

def get_id_from_path(file_path: str):
    return os.path.basename(file_path).split(".")[0]