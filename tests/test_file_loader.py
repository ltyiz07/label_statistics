import os
import tarfile
import json
import xmltodict
from proj_stat.database import collection_cls

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


def test_get_subset_from_tar():
    sample_tar_path = ["/".join(config.TAR_SOURCE, p) for p in os.listdir(config.TAR_SOURCE) if p.endswith(".tar")][0]
    # sample_tar_path = os.path.join(config.TAR_SOURCE, "test_7.tar")
    result = collection_cls.get_subsets_from_tar(sample_tar_path)
    logger.debug(result)
    with tarfile.open(sample_tar_path, "r") as tar:
        # content = tar.extractfile(result[0])
        # logger.debug([l.decode().strip() for l in content])
        for t in tar:
            if t.name.endswith(".xml"):
                logger.debug(tar.getmember(t.name).chksum)

