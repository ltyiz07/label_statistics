import os
import glob
import tarfile
import xmltodict

from proj_stat.database import mongo_db
from proj_stat import config
from proj_stat.database.collection_cls import Annotation, AnnotationObject, Dataset

def update_database():
    mongo_db.create_collections_with_schemas()
    datasets_col = mongo_db.get_datasets_col()
    annotations_col = mongo_db.get_annotations_col()

    # parsed_data =  tuple(get_parsed_dict_from_tar(tar) for tar in get_tarfiles()) 
    for tar in get_tarfiles():
        # parsed_data = get_parsed_dict_from_tar(tar)

        # Dataset => dataset_id: str, dataset_path: str, dataset_hash: str, annotations: list[str]
        dataset = Dataset()
        # Annotation => image_id: str, dataset_id: str, image_path: str, size: tuple[int], objects: list[AnnotationObject]
        annot = Annotation()
        # Annotationobject => name: str, bndbox: dict
        anno_obj = AnnotationObject()

        datasets_col.insert_one(extract_dataset(parsed_data))
        annotations_col.insert_many(extract_annotations(parsed_data))

def get_parsed_dict_from_tar(tar_path: str):
    """
    use this api for insert into mongodb
    """
    return _matching_datasets_validator(tar_path)

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

class TarFormat(dict):
    """
    tar file contains {images(.jpg), image_list(.txt), annotations(.xml)}
    this class itself uses only annotations
    """
    def __init__(self, annotations):
        # self.annotations = annotations
        # self.dataset_id: str = os.path.splitext(os.path.basename(tar_path))[0]
        # self.image_ids
        pass

    @classmethod
    def from_file(cls, tar_path):
        content = TarFormat._parse_annotations_from_tar(tar_path)
        cls.tar_path = tar_path
        cls(content)
        return cls


    @staticmethod
    def _parse_annotations_from_tar(tar_path: str):
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


