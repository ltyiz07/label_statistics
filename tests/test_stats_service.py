from proj_stat.services.init_service import get_stats

import logging

log = logging.getLogger('test')


def test_get_stats():
    log.debug(get_stats("GODTrain211111_test", ["images_sizes", "objects_sizes_avg"]))