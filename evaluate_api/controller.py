from flask import Blueprint, request
from flask.json import jsonify
from sqlalchemy import select
from sqlalchemy.orm import Bundle

from evaluate_api.database import db_session
from evaluate_api.model import Challenge, Metric, Result
from evaluate_api.service.base import get_metric, get_hash_from

challenges = Blueprint("challenges", __name__, url_prefix="/challenges")
challenges.route("/")


@challenges.route("/", methods=["GET"])
def get_challenges():
    """get all challenges as list from api server.

    Returns:
        Challenges
    """
    result = db_session.execute(
        select(Challenge)
        .from_statement(
            select(Bundle("Challenge", Challenge.create_time, Challenge.title, Challenge.challenge_id))
        )
    )
    # print([e for e in result.scalars().all()])
    return jsonify([e.get_dict() for e in result.scalars().all()])
    # return jsonify({"method": "get_challenges"})


@challenges.route("/<string:challenge_id>", methods=["GET"])
def get_challenge(challenge_id):
    """get challenge info with challenge ID

    Args:
        challenge_id (str): id of challenge from files meta-data
    Returns:
        Challenge
    """
    result = db_session.execute(
        select(Challenge).where(Challenge.challenge_id == challenge_id)
    ).fetchone()
    if result:
        result = result[0]
    return result.get_dict()


@challenges.route("/<string:challenge_id>/submissions", methods=["POST"])
def submit_model(challenge_id):
    """request evaluation of model to server

    Args:
        challenge_id (string): id of challenge from file meta-data
        request (dict | bytes): requestBody from client
    Returns:
        SubmissionInfo
    """
    user_name = request.form.get("user_name", "unknown")
    file = request.files.get("submission_file")
    if not file:
        return jsonify({"error": "file not found"}), 400

    # metrics = db_session.execute(select(Metric).where(Metric))

    # TODO: convert this work to multi threaded
    file_content = file.stream.readlines()


    # result_metric = get_metric(get_hash_from(challenge_id, file_content), )
    return jsonify({"result": "file submitted, processing..."})


@challenges.route("/<string:challenge_id>/submissions/<string:submission_id>", methods=["GET"])
def get_status_or_result(challenge_id, submission_id):
    """if evaluated returns result else returns progress

    Args:
        challenge_id (string): id of challenge from file meta-data
        submission_id (string): id of submission on progress or done process
    Returns:
        SubmissionResult
    """
    return jsonify({"method": "get_status_or_result"})


@challenges.route("/<string:challenge_id>/submissions", methods=["GET"])
def get_status_and_results(challenge_id):
    """get all status on progress and results

    Args:
        challenge_id (string): id of challenge from file meta-data
    Returns:
        InlineResponse200
    """
    return jsonify({"method": "get_status_and_results"})
