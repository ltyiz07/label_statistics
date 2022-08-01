from proj_stat import config
from proj_stat.services import init_service, main_service
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

def test_pagination_class():
    pagination = main_service.DatasetPagination(0)
    pagination.update()

    datasets_col = mongo_db.get_datasets_col()
    cursor = datasets_col\
        .find({"_id": {"$gte": pagination.begin_index}})\
            .sort([("_id", 1)])\
                .limit(pagination.index_gap)

    log.debug([{"tar_name": c["tar_name"], "dataset_name": c["dataset_name"]} for c in cursor])
    log.debug("index_gap: " + str(pagination.index_gap) + "\n")
    log.debug("begin_index: " + str(pagination.begin_index) + "\n")
    log.debug("index_list: " + str(pagination.index_list) + "\n")
    log.debug("page_count: " + str(pagination.page_count) + "\n")
