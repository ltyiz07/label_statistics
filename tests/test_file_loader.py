import os
import tarfile
import json
import xmltodict

from proj_stat import config

import logging
logger = logging.getLogger('test')


def test_dir_read():
    dir_list = os.listdir(config.TAR_SOURCE)
    logger.debug(dir_list)


def test_tar_read():
    with tarfile.open(r"./sample_data/tars/GODTrain211111_test.tar", 'r') as tar:
        for t in tar:
            # tar_info = tarfile.TarInfo.fromtarfile(tar)
            logger.debug(f"name: {t.name}")
            logger.debug(f"size: {t.size}")
            logger.debug(f"mtime: {t.mtime}")
            logger.debug(f"isdir: {t.isfile()}")
            if t.isfile():
                file = tar.extractfile(t)
                # logger.debug(content.read())
                if t.name.split(".")[-1] == "xml":
                    content = file.read()
                    xml_dict = xmltodict.parse(content)
                    logger.debug(xml_dict)