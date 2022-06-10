import os
import json
from datetime import datetime

from flask import Blueprint, request
from flask.json import jsonify
from sqlalchemy import select
from sqlalchemy.orm import Bundle

import redis

from evaluate_api.database import db_session
from evaluate_api.model import Challenge, Result
from evaluate_api.service.base import get_hash_from
from evaluate_api.service.evaluator import evaluate_submission, AsyncResult1

challenges = Blueprint("challenges", __name__, url_prefix="/challenges")
challenges.route("/")
# cache = redis.Redis(host='redis', port=6379)
cache = redis.Redis(host=os.environ.get("REDIS_HOST", "localhost"), port=6379, db=0)


@challenges.route("/", methods=["GET"])
def get_challenges():
    """get all challenges as list from api server.
    and this is difficult to caching...

    Returns:
        Challenges
    """

    result = db_session.execute(
        select(Challenge)
        .from_statement(
            select(Bundle("Challenge", Challenge.create_time, Challenge.title, Challenge.challenge_id))
        )
    )
    return jsonify([e.get_dict() for e in result.scalars().all()])


@challenges.route("/<string:challenge_id>", methods=["GET"])
def get_challenge(challenge_id):
    """get challenge info with challenge ID

    Args:
        challenge_id (str): id of challenge from files meta-data
    Returns:
        Challenge
    """

    cached_value = cache.get(challenge_id)
    if cached_value:
        return cached_value
    else:
        result = db_session.execute(
            select(Challenge).where(Challenge.challenge_id == challenge_id)
        ).fetchone()
        if len(result) == 1:
            result = result[0]
    jsonized = json.dumps(result.get_dict())
    cache.set(challenge_id, jsonized)
    return jsonized


@challenges.route("/<string:challenge_id>/submissions", methods=["POST"])
def submit_model(challenge_id):
    """request evaluation of model to server

    Args:
        challenge_id (string): id of challenge from file meta-data
    Returns:
        SubmissionInfo
    """

    user_name = request.form.get("user_name")
    if user_name == "":
        user_name = "unknown"
    file = request.files.get("submission_file")
    if not file:
        return jsonify({"error": "file not found"}), 400

    # get data from database
    try:
        challenge = db_session.execute(
            select(Challenge).where(Challenge.challenge_id == challenge_id)
        ).fetchone()[0]
        metrics = json.loads(challenge.metrics)
    except IndexError as e:
        print(e)
        return jsonify({"error": "challenge not found"}), 400

    # generate submissino_id before submit
    submission_id = get_hash_from(challenge_id, file.stream.read())
    # to check already submitted
    request_key = f"{challenge_id}-{submission_id}"
    cached_result = cache.get(request_key)
    if cached_result:
        return cached_result
    else:
        async_id = evaluate_submission.delay(challenge_id, submission_id, metrics).id
        cache.set(submission_id, async_id)
        cache.sadd(f"{challenge_id}-", submission_id)
        res = json.dumps({
            "submission_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "challenge_id": challenge_id,
            "submission_id": submission_id,
            "user_name": user_name
        })
        cache.set(request_key, res)
        return res


@challenges.route("/<string:challenge_id>/submissions/<string:submission_id>", methods=["GET"])
def get_status_or_result(challenge_id, submission_id):
    """if evaluated returns result else returns progress

    Args:
        challenge_id (string): id of challenge from file meta-data
        submission_id (string): id of submission on progress or done process
    Returns:
        SubmissionResult
    """

    challenge_submission = json.loads(cache.get(f"{challenge_id}-{submission_id}"))
    submission_time = challenge_submission["submission_time"]
    user_name = challenge_submission["user_name"]
    async_id = cache.get(submission_id)
    async_result_1 = AsyncResult1(async_id)
    if async_result_1.status == "SUCCESS":
        result_form = {
            "result": json.loads(async_result_1.get()),
            "submission_time": submission_time, "user_name": user_name
        }
    else:
        result_form = {
            "status": "processing",
            "submission_time": submission_time, "user_name": user_name
        }
    return json.dumps(result_form)


@challenges.route("/<string:challenge_id>/submissions", methods=["GET"])
def get_status_and_results(challenge_id):
    """get all status on progress and results

    Args:
        challenge_id (string): id of challenge from file meta-data
    Returns:
        response (dict): submission status and results
    """

    results = {}
    for sub_id in cache.smembers(f"{challenge_id}-"):
        sub_id = sub_id.decode()
        challenge_submission = json.loads(cache.get(f"{challenge_id}-{sub_id}"))
        submission_time = challenge_submission["submission_time"]
        user_name = challenge_submission["user_name"]
        async_result_1 = AsyncResult1(cache.get(sub_id).decode())
        if async_result_1.status == "SUCCESS":
            results[sub_id] = {
                "result": json.loads(async_result_1.get()),
                "submission_time": submission_time, "user_name": user_name
            }
        else:
            results[sub_id] = {
                "status": "processing",
                "submission_time": submission_time, "user_name": user_name
            }
    return json.dumps(results)
