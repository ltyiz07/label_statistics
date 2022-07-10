import sys
from ast import Mod
from pymongo import MongoClient
from proj_stat.config import MONGO_PORT, MONGO_HOST
from proj_stat.database.collection_schemas import datasets_validator


mongo_client = MongoClient(host=MONGO_HOST, port=MONGO_PORT) # set username, password
# from proj_stat.database.collection_schemas import annotations_schema
def create_datasets_col():
    db = mongo_client["annotation"]
    if "datasets" in db.list_collection_names():
        db.get_collection("datasets").drop()

    db.create_collection("datasets")
    db.command('collMod', 'datasets', validator=datasets_validator, validationLevel='moderate')
    # db.create_collection('collMod', {"validator": datasets_validator, "validationLevel": 'moderate'})
    # cursor = collection.find({})
    # for c in cursor:
        # print(c) # <= dict type
        # print(c["_id"])
    return db.get_collection("datasets")

def get_datasets_col():
    return mongo_client["annotation"]["datasets"]
