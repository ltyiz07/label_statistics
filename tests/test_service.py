from proj_stat import config
from proj_stat.services import init_service
import tarfile
import xmltodict
import os
from proj_stat.database import mongo_db
from proj_stat.database.collection_cls import parse_annotations_from_tar, get_hash_from_tar

import logging
log = logging.getLogger('test')

def test_get_tarfiles():
    log.debug(init_service.get_tarfiles())
    assert init_service.get_tarfiles() is not None

def test_load_data():
    tarfile_path = init_service.get_tarfiles()[0]
    log.debug(tarfile_path)
    with tarfile.open(tarfile_path, 'r') as tar:
        ff = {t.name: xmltodict.parse(tar.extractfile(t.name).read()) for t in tar if t.name.endswith(".xml")}
        assert ff.popitem() != None
        # for t in tar:
            # log.debug(t.name)

def test_parse_annotation_from_tar():
    tarfile_path = init_service.get_tarfiles()[0]
    json_content = parse_annotations_from_tar(tarfile_path)
    assert len(json_content) > 0

def test_parse_others():
    tarfile_path = init_service.get_tarfiles()[1]
    with tarfile.open(tarfile_path, "r") as tar:
        for t in tar:
            log.debug(t.name)
            log.debug(t.isfile())
            log.debug(os.path.basename(os.path.dirname(t.name)))

def test_database_update():
    init_service.upload_database()
