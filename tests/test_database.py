import os
import sys
from pydoc import cli
from pymongo import MongoClient
from proj_stat.database import mongo_db

import logging
log = logging.getLogger('test')

client = MongoClient(host="localhost", port=27017) # set username, password

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
    mongo_db.create_col_datasets()
    col_datasets = mongo_db.get_col_datasets()
    try:
        col_datasets.insert_one({"x":1})
        log.debug("NOT good; the insert above should have failed.")
    except:
        log.debug(f"OK. Expected exception.")
    
    try:
        okdoc = {
                    "dataset_id": "god_filename",
                    "dataset_hash": "21324114",
                    "annotations": 
                        {
                            "image_id": "21231234",
                            "size": {"width": 21, "height": 31},
                            "objects":[
                                {"name": "bmw_car", "bndbox": {"xmin": 44.21, "ymin": 21.00, "xmax": 24.00, "ymax": 21.00}},
                                {"name": "random_car", "bndbox": {"xmin": 44.21, "ymin": 21.00, "xmax": 24.00, "ymax": 21.00}}
                                ]
                        },
        }
        col_datasets.insert_one(okdoc)
        log.debug("All good.")
    except:
        log.debug("Not good...")

    for c in col_datasets.find({}):
        log.debug("output: ")
        log.debug(c)