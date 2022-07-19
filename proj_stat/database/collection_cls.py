import os
import json
import tarfile
import xmltodict


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
        self.annotations: list[Annotation]

    @classmethod
    def from_parsed_annotations(cls, tar_path, annotations):
        return cls({
            "dataset_id": os.path.splitext(os.path.basename(tar_path))[0],
            "dataset_path": os.path.realpath(tar_path),
            "dataset_hash": get_hash_from_tar(tar_path),
            "annotations": [k.rpartition(r"/")[2].partition(".")[0] for k in annotations.keys()]
        })

    @staticmethod
    def get_stats(annotations: list[Annotation]):
        pass


class Annotation(dict):
    def __init__(self, *vargs, **kwargs):
        if len(vargs) > 0:
            mapper = vargs[0]
        else:
            mapper = kwargs
        self["image_id"]: str = mapper.get("image_id")
        self["dataset_id"]: str = mapper.get("dataset_id")
        self["image_path"]: str = mapper.get("image_path")
        self["size"]: tuple[int] = mapper.get("size")
        self["objects"]: list[AnnotationObject] = mapper.get("objects")     # keys: {"name", "bndbox"}

    @classmethod
    def from_parsed_annotations(cls, tar_path, annotations):
        annotation_list = []
        for name, objs in annotations.items():
            annotation_list.append(cls({
                "image_id": name.rpartition(r"/")[2].partition(".")[0],
                "dataset_id": os.path.splitext(os.path.basename(tar_path))[0],
                "image_path": name.replace("Annotations", "JPEGImages").replace("xml", "jpg"),
                "size": {k: int(v) for k, v in objs["annotation"]["size"].items()},
                "objects": objs["annotation"]["object"]
            }))
        return annotation_list

class AnnotationObject(dict):
    def __init__(self, *vargs, **kwargs):
        if len(vargs) > 0:
            mapper = vargs[0]
        else:
            mapper = kwargs
        self["name"]: str = mapper.get("name")
        self["bndbox"]: dict[str, str] = mapper.get("bndbox")

def parse_annotations_from_tar(tar_path: str):
    """
    extract annotations/*.xml files and parse content
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


def get_hash_from_tar(tar_path: str):
    """
    generate hash from tar files content, using filenames, file-sizes, file-mtime
    """
    hash_str: str = None
    with tarfile.open(tar_path, 'r') as tar:
        # return hash(tuple( chain.from_iterable((t.name, t.size, t.mtime) for t in tar) ))
        return str(hash(tuple( t.chksum for t in tar) ))