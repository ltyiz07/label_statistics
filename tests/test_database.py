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

    sample_dataset =  Dataset({
        "dataset_id": "test_filename",
        "dataset_path": "test_filename.tar",
        "dataset_hash": "21324114",
        "annotations": ["21231234", "21231236"],
    })
    sample_annotation_1 = Annotation({
        "image_id": "21231234",
        "dataset_id": "test_filename",
        "image_path": "Image/21231234.jpg",
        "size": {"width": 21, "height": 31},
        "objects": [
            {
                "name": "bmw_car",
                "bndbox": {
                    "xmin": "45.21", "ymin": "22.00",
                    "xmax": "24.00", "ymax": "21.00"
                }
            },
            {
                "name": "random_car",
                "bndbox": {
                "xmin": "45.21", "ymin": "22.00",
                "xmax": "24.00", "ymax": "21.00"
                }
            }
        ]
    })
    sample_annotation_2 = Annotation({
        "image_id": "21231236",
        "image_path": "Image/21231235.jpg",
        "dataset_id": "test_filename",
        "size": {"width": 22, "height": 32},
        "objects": [
            {
                "name": "bmw_car",
                "bndbox": {
                    "xmin": "45.21", "ymin": "22.00",
                    "xmax": "24.00", "ymax": "21.00"
                }
            },
            {
                "name": "random_car",
                "bndbox": {
                "xmin": "45.21", "ymin": "22.00",
                "xmax": "24.00", "ymax": "21.00"
                }
            }
        ]
    })
    datasets_col.insert_one(sample_dataset)
    # annotations_col.insert_many([sample_annotation_1, sample_annotation_2])
    annotations_col.insert_one(sample_annotation_1)
    annotations_col.insert_one(sample_annotation_2)
    log.debug("All good.")

def test_get_as_py_class():
    init_service.update_database()

    annotations_col = mongo_db.get_annotations_col()
    datasets_col = mongo_db.get_datasets_col()

    cursor = datasets_col.find({})
    sample_dataset_id = cursor[0].get("dataset_id")
    dataset = Dataset(datasets_col.find_one({"dataset_id": sample_dataset_id}))
