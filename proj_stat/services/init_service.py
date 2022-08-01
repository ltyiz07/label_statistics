import os
import glob
import datetime
import tarfile

import xmltodict

from proj_stat.database import mongo_db
from proj_stat import config
from proj_stat.database.collection_cls import Annotation, Dataset

def upload_database():
    # Drop all database and recreate collections
    mongo_db.create_collections_with_schemas()

    annotation_col = mongo_db.get_annotations_col()
    dataset_col = mongo_db.get_datasets_col()

    get_id = lambda path: os.path.basename(path).split(".")[0]
    get_dirname = lambda path: os.path.basename(os.path.dirname(path))
    for tar_abs_path in get_tarfiles():
        dataset_paths = list()
        xml_names = dict()
        img_names = dict()      # { image_name : image_path }
        with tarfile.open(tar_abs_path, 'r') as tar:
            tar_path = os.path.basename(tar_abs_path)
            tar_name = get_id(tar_path)
            for member in tar.getmembers():
                if member.isfile():
                    if get_dirname(member.name) == "ImageSets":
                        dataset_paths.append(member.name)
                    if get_dirname(member.name) == "Annotations":
                        xml_names[get_id(member.name)] = member.name
                    if get_dirname(member.name) == "JPEGImages":
                        img_names[get_id(member.name)] = member.name

            # Add annotation #####
            for image_name in img_names.keys():
                parsed = xmltodict.parse(tar.extractfile(xml_names.get(image_name)).read())
                annot = Annotation({
                    "tar_path": tar_path,
                    "tar_name": tar_name,
                    "image_path": img_names.get(image_name),
                    "image_name": image_name,
                    "size": (parsed["annotation"]["size"]["width"], parsed["annotation"]["size"]["height"]),
                    "objects": parsed["annotation"]["object"],
                    "object_count": _get_object_count(parsed["annotation"]["object"]),
                    "edited_date": datetime.datetime.now(),
                })
                # Insert to database
                annotation_col.insert_one(annot.__dict__)
            # Add dataset #####
            for dataset_path in dataset_paths:
                image_name_list = [ l.decode().strip() for l in tar.extractfile(dataset_path).readlines() if len(l.strip()) > 3 ]
                dataset_hash = str(hash(tar.gettarinfo(xml_names.get(file_id)).chksum for file_id in image_name_list))
                dataset = Dataset({
                    "tar_path": tar_path,
                    "tar_name": tar_name,
                    "dataset_path": dataset_path,
                    "dataset_name": get_id(dataset_path),
                    "dataset_hash": dataset_hash,
                    "image_names": image_name_list,
                    "edited_date": datetime.datetime.now(),
                })
                dataset_col.insert_one(dataset.__dict__)

def update_database():
    pass

def get_dataset_hash():
    pass

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


def _get_object_count(objects):
    obj_count = dict()
    for obj in objects:
        obj_name = obj["name"]
        obj_count[obj_name] = obj_count.get(obj_name, 0) + 1
    return obj_count