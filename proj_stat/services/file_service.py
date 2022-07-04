import os
import glob
import tarfile
from itertools import chain

from proj_stat import config


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

def load_tarfile(tar_path):
    """
    load
    Args:
    Returns:
    """
    pass

def get_hash_from_tar(tar_path: str):
    """
    generate hash from tar files content, using filenames, file-sizes, file-mtime
    """
    hash_str: str = None
    with tarfile.open(tar_path, 'r') as tar:
        return hash(tuple( chain.from_iterable((t.name, t.size, t.mtime) for t in tar) ))