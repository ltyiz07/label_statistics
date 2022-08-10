from proj_stat.database.collection_cls import Annotation
from proj_stat.database import mongo_db
from bson.son import SON

import logging


log = logging.getLogger('test')

annots_col = mongo_db.get_annotations_col()
datasets_col = mongo_db.get_datasets_col()


def test_searh_with_object_name():
    """
    cite Jimin
    """
    search_result = annots_col.find({}).sort( [("object_count.pickup_truck", -1), ("object_count.sedan", -1)] )
    for obj in search_result[:10]:
        annot = Annotation(obj)
        log.debug("tar_name: " + annot.tar_name)
        log.debug("image_name: " + annot.image_name)
        log.debug("image_name: " + str(annot.object_count))

        
def test_search_with_objects():
    # cur = annots_col.find({"object_count": {"$exists": "sedan", "$exists": "pickup_truck"}}, {"image_name": 1})
    # cur = annots_col.find({"object_count": {"$exists": "sedan"}}, {"image_name": 1})
    # cur = annots_col.find({"object_count": SON([("sedan", 5)])}, {"image_name": 1})
    # cur = annots_col.find({"object_count.sedan": 4}, {"image_name": 1})
    # cur = annots_col.find({"object_count.sedan": 5 , "object_count.pickup_truck": 1 }, {"image_name": 1})
    cur = annots_col.find(
            {"object_count.sedan": {"$exists": True} , "object_count.pickup_truck": {"$exists": True} },
            {"image_name": 1, "object_count": 1}
        ).sort( [("object_count.sedan", -1), ("object_count.pickup_truck", -1)] )
    count = 0
    for c in cur:
        log.debug(c)
        count += 1
    log.debug(count)