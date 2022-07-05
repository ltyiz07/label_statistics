import os
import glob
import tarfile
from itertools import chain
import xmltodict

from proj_stat import config


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
        return hash(tuple( t.chksum for t in tar) )

def parse_annotations_from_tar(tar_path: str):
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
            if t.name.startswith("Annotations/") and t.name.endswith(".xml")
        }

def matching_datasets_validator(tar_path):
    """
    convert parsed annotation dict to 
    image_id : filename.rpartision(r"/")[2].partision(".")[0]
    Args:
        tar_path (str): absolute path of .tar file
    Returns:
    """
    dict_content = parse_annotations_from_tar(tar_path)
    dict_out = dict()
    dict_out["dataset_id"] = os.path.basename(tar_path)
    dict_out["dataset_hash"] = get_hash_from_tar(tar_path)
    dict_out["annotations"] = {
        fn.rpartition(r"/")[2].partition(".")[0]: _matching_annotation(an)
        for fn, an in dict_content.items()
    }
    # for filename, annot in dict_content.items():
        # dict_schema[filename.rpartition(r"/")[2].partition(".")[0]] = \


def _matching_annotation(dict_content: dict):
    dict_out = dict()
    dict_out[""]