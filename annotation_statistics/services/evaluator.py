import json
import os

from celery import Celery

from annotation_statistics.services.base import get_metric

BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
celler_app = Celery(__name__, broker=BROKER_URL, backend=CELERY_RESULT_BACKEND)
celler_app.autodiscover_tasks()
# cache = redis.Redis(host=os.environ.get("REDIS_HOST", "localhost"))
AsyncResult1 = celler_app.AsyncResult


@celler_app.task(name="evaluate_submission")
def evaluate_submission(challenge_id: str, submission_id: str, metrics: list):
    # request_key = f"{challenge_id}-{submission_id}"
    # if not cache.get(request_key):
    result = json.dumps(get_metric(submission_id, metrics))
    return result