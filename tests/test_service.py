from proj_stat import config
from proj_stat.services import file_service

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
