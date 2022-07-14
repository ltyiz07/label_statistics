import sys
from ast import Mod
from pymongo import MongoClient
from proj_stat.config import MONGO_PORT, MONGO_HOST
from proj_stat.database.collection_schemas import datasets_schema, annotations_schema


mongo_client = MongoClient(host=MONGO_HOST, port=MONGO_PORT) # set username, password

def create_collections_with_schemas():
    db = mongo_client["annotation"]
    if "datasets" in db.list_collection_names():
        db.get_collection("datasets").drop()
    if "annotations" in db.list_collection_names():
        db.get_collection("annotations").drop()

    db.create_collection("datasets")
    db.create_collection("annotations")

    db.command('collMod', 'datasets', validator=datasets_schema, validationLevel='moderate')
    db.command('collMod', 'annotations', validator=annotations_schema, validationLevel='moderate')

    return db

def get_datasets_col():
    return mongo_client["annotation"]["datasets"]

def get_annotations_col():
    return mongo_client["annotation"]["annotations"]
