import sys
import tarfile

from proj_stat.services.init_service import get_tarfiles

import logging
log = logging.getLogger('test')

def test_tarfile_module():
    sample_tarfile_path = get_tarfiles()[0]
    with tarfile.open(sample_tarfile_path, 'r') as tar:
        log.debug(sys.getsizeof(tar.getnames()))
        log.debug(sys.getsizeof(tar.getmembers()))