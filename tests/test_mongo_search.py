from proj_stat.database.collection_cls import Annotation
from proj_stat.database import mongo_db

import logging

log = logging.getLogger('test')

annots_col = mongo_db.get_annotations_col()
datasets_col = mongo_db.get_datasets_col()


def test_searh_with_object_name():
    """
    cite Jimin
    """
    search_result = annots_col.find({}).sort( [("object_count.pickup_truck", -1), ("object_count.sedan", -1)] )
    for obj in search_result:
        annot = Annotation(obj)
        log.debug("tar_name: " + annot.tar_name)
        log.debug("image_name: " + annot.image_name)
        log.debug("image_name: " + str(annot.object_count))