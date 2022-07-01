import os
from pydoc import cli
from pymongo import MongoClient

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