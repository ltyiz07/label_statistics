from proj_stat import config
from proj_stat.services import file_service
import tarfile
import xmltodict

import logging
log = logging.getLogger('test')

def test_get_tarfiles():
    log.debug(file_service.get_tarfiles())
    assert file_service.get_tarfiles() is not None

def test_get_hash_from_tar():
    tarfiles = file_service.get_tarfiles()
    hash_code = file_service.get_hash_from_tar(tarfiles[0])
    log.debug(hash_code)
    assert file_service.get_hash_from_tar(tarfiles[0]) != file_service.get_hash_from_tar(tarfiles[1])
    assert file_service.get_hash_from_tar(tarfiles[1]) == file_service.get_hash_from_tar(tarfiles[1])

def test_load_data():
    tarfile_path = file_service.get_tarfiles()[0]
    log.debug(tarfile_path)
    with tarfile.open(tarfile_path, 'r') as tar:
        ff = {t.name: xmltodict.parse(tar.extractfile(t.name).read()) for t in tar if t.name.endswith(".xml")}
        log.debug(ff.popitem())
        # for t in tar:
            # log.debug(t.name)

def test_parse_annotation_from_tar():
    tarfile_path = file_service.get_tarfiles()[0]
    json_content = file_service.parse_annotations_from_tar(tarfile_path)
    log.debug(json_content)

def test_matching_schema():
    tarfile_path = file_service.get_tarfiles()[0]
    dict_content = file_service.parse_annotations_from_tar(tarfile_path)
    for filename, annot in dict_content.items():
        log.debug(filename)
        log.debug(annot)