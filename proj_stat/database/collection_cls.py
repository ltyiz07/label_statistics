import json

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
        self["objects"]: list[AnnotationObject] = mapper.get("objects")

class AnnotationObject(dict):
    def __init__(self, *vargs, **kwargs):
        if len(vargs) > 0:
            mapper = vargs[0]
        else:
            mapper = kwargs
        self["name"]: str = mapper.get("name")
        self["bndbox"]: dict[str, str] = mapper.get("bndbox")