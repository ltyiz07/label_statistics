from proj_stat.services.init_service import TarFormat
from proj_stat.services.init_service import get_tarfiles

import logging
log = logging.getLogger('test')

def test_tar_format_cls():
    sample_tarfile_path = get_tarfiles()[0]
    tar_format = TarFormat.from_file(sample_tarfile_path)
    log.debug(tar_format)

