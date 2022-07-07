from proj_stat import config
from proj_stat.services import service
import tarfile
import xmltodict
import os
from proj_stat.database import mongo_db

import logging
log = logging.getLogger('test')

def test_get_tarfiles():
    log.debug(service.get_tarfiles())
    assert service.get_tarfiles() is not None

def test_get_hash_from_tar():
    tarfiles = service.get_tarfiles()
    hash_code = service.get_hash_from_tar(tarfiles[0])
    log.debug(hash_code)
    assert service.get_hash_from_tar(tarfiles[0]) != service.get_hash_from_tar(tarfiles[1])
    assert service.get_hash_from_tar(tarfiles[1]) == service.get_hash_from_tar(tarfiles[1])

def test_load_data():
    tarfile_path = service.get_tarfiles()[0]
    log.debug(tarfile_path)
    with tarfile.open(tarfile_path, 'r') as tar:
        ff = {t.name: xmltodict.parse(tar.extractfile(t.name).read()) for t in tar if t.name.endswith(".xml")}
        assert ff.popitem() != None
        # for t in tar:
            # log.debug(t.name)

def test_parse_annotation_from_tar():
    tarfile_path = service.get_tarfiles()[0]
    json_content = service._parse_annotations_from_tar(tarfile_path)
    assert len(json_content) > 0

def test_parse_others():
    tarfile_path = service.get_tarfiles()[1]
    with tarfile.open(tarfile_path, "r") as tar:
        for t in tar:
            log.debug(t.name)
            log.debug(t.isfile())
            log.debug(os.path.basename(os.path.dirname(t.name)))

def test_matching_schema():
    tarfile_path = service.get_tarfiles()[0]
    dict_content = service._parse_annotations_from_tar(tarfile_path)
    assert dict_content.popitem() != None
    # for filename, annot in dict_content.items():
        # log.debug(filename)
        # log.debug(annot)
    log.debug(os.path.realpath(tarfile_path))

def test_get_dict_from_tar():
    mongo_db.create_datasets_col()
    col_datasets = mongo_db.get_datasets_col()
    sample_tar = service.get_tarfiles()[1]
    output = service.get_parsed_dict_from_tar(sample_tar)
    # log.debug(output)
    col_datasets.insert_one(output)