from proj_stat.services.init_service import get_tarfiles
from proj_stat.database.collection_cls import parse_annotations_from_tar

import logging
log = logging.getLogger('test')


def test_tar_extraction():
    sample_tarfile_path = get_tarfiles()[0]
    parsed_data = parse_annotations_from_tar(sample_tarfile_path)
    log.debug(parsed_data)
