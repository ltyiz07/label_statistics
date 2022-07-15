import os
import glob

from proj_stat.database import mongo_db
from proj_stat import config
from proj_stat.database.collection_cls import Annotation, Dataset, parse_annotations_from_tar

def update_database():
    mongo_db.create_collections_with_schemas()
    datasets_col = mongo_db.get_datasets_col()
    annotations_col = mongo_db.get_annotations_col()

    # parsed_data =  tuple(get_parsed_dict_from_tar(tar) for tar in get_tarfiles()) 
    for tar in get_tarfiles():
        parsed_data = parse_annotations_from_tar(tar)

        # Dataset => dataset_id: str, dataset_path: str, dataset_hash: str, annotations: list[str]
        dataset = Dataset.from_parsed_annotations(tar, parsed_data)
        # [Annotation] => image_id: str, dataset_id: str, image_path: str, size: tuple[int], objects: list[AnnotationObject]
        annotations = Annotation.from_parsed_annotations(tar, parsed_data)

        datasets_col.insert_one(dataset)
        annotations_col.insert_many(annotations)

def get_tarfiles(source_dir=config.TAR_SOURCE):
    """
    get tar file list from tar data source(env)

    Args:
        source_dir (str): tar file source directory with absolute path
    Returns
         ([str]): list of tar files (*.tar)
    """
    source_dir = os.path.join(source_dir, "*.tar")
    return glob.glob(source_dir)
