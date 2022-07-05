import os
from celery import Celery
from proj_stat.database import mongo_db


BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
celler_app = Celery(__name__, broker=BROKER_URL, backend=CELERY_RESULT_BACKEND)
celler_app.autodiscover_tasks()
# cache = redis.Redis(host=os.environ.get("REDIS_HOST", "localhost"))
# AsyncResult1 = celler_app.AsyncResult


@celler_app.task(name="evaluate_submission")
def load_db(challenge_id: str, submission_id: str, metrics: list):
    return None

def load_db():
    col_datasets = mongo_db.create_col_datasets()
    
