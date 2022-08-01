import os
from random import sample
import sys
from pydoc import cli
from pymongo import MongoClient
from proj_stat.database import mongo_db
from proj_stat.database.collection_cls import Dataset, Annotation
from proj_stat.services import init_service

import logging
log = logging.getLogger('test')

client = MongoClient(host="localhost", port=27017)  # set username, password


def test_connection():
    assert len(client.list_database_names()) > 2


def test_insert():
    collection = client["test_db"].inventory
    collection.drop()
    insert_output = collection.insert_many([
        {
            "item": "canvas",
            "qty": 100,
            "tags": ["cotton"],
            "size": {"h": 28, "w": 35.5, "uom": "cm"},
        },
        {
            "item": "paint",
            "qty": 20,
            "tags": ["liquid"],
            "size": {"h": 10, "w": 5.5, "uom": "cm"},
        }
    ])
    log.debug(insert_output)
    cursor = collection.find({})
    for c in cursor:
        log.debug(c)


def test_col_datasets_validation():
    mongo_db.create_collections_with_schemas()
    datasets_col = mongo_db.get_datasets_col()
    annotations_col = mongo_db.get_annotations_col()
    try:
        datasets_col.insert_one({"x": 1})
        log.debug("NOT good; the insert above should have failed.")
    except:
        log.debug(f"OK. Expected exception.")

    sample_dataset =  Dataset({"tar_path": "test_filename.tar"})
    sample_annotation_1 = Annotation({"tar_path": "test_filename.tar"})
    sample_annotation_2 = Annotation({"tar_path": "test_filename.tar"})
    datasets_col.insert_one(sample_dataset.__dict__)
    # annotations_col.insert_many([sample_annotation_1, sample_annotation_2])
    annotations_col.insert_one(sample_annotation_1.__dict__)
    annotations_col.insert_one(sample_annotation_2.__dict__)
    log.debug("All good.")

def test_get_as_py_class():
    init_service.upload_database()

    annotations_col = mongo_db.get_annotations_col()
    datasets_col = mongo_db.get_datasets_col()

    datasets_cursor = datasets_col.find_one()
    sample_tar_file = datasets_cursor.get("tar_path")

    dataset = Dataset(datasets_col.find_one({"tar_path": sample_tar_file}))
    log.debug(dataset)

    sample_annotations = annotations_col.find({"dataset_id": sample_tar_file})

    dataset.annotations = [Annotation(o) for o in sample_annotations]
    log.debug(dataset.annotations)


def test_db_update():
    init_service.upload_database()
    annotations_col = mongo_db.get_annotations_col()
    datasets_col = mongo_db.get_datasets_col()
    for i in annotations_col.find():
        log.debug(i)
