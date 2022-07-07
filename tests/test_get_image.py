import tarfile
from proj_stat.database import mongo_db
from proj_stat.services import service

import logging

log = logging.getLogger('test')


def test_get_image():
    sample_tar = service.get_tarfiles()[0]
    with tarfile.open(sample_tar, 'r') as tar:
        for t in tar:
            if t.name.endswith(".jpg"):
                file = tar.extractfile(t)
                log.debug(file.read())
