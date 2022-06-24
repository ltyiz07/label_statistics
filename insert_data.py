import json
import os
from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import select
from annotation_statistics.model import Challenge, Result


def load_json(path: str):
    with open(path, 'r') as file:
        return json.load(file)


def load_text(path: str):
    with open(path, 'r') as file:
        return file.read()


def load_challenges_to_db(session, sample_dir: str = r"./sample_data"):
    pass


def load_results_to_db(session, sample_dir: str = r"./sample_data"):
    pass
