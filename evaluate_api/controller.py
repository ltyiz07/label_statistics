from flask import Blueprint, request
from flask.json import jsonify
from flasgger import swag_from
from sqlalchemy import select

from evaluate_api.database import db_session, Base
# from evaluate_api.model import *
from evaluate_api.model import Metric

challenges = Blueprint("challenges", __name__, url_prefix="/challenges")
challenges.route("/")
"""
함수들의 순서는 제공 받은 문서에서 정의된 순서와 동일합니다.
"""


@challenges.route("/", methods=["GET"])
def get_challenges():
    """get all challenges as list from api server.

    Returns:
        Challenges
    """
    return jsonify({"method": "get_challenges"})


@challenges.route("/<string:challenge_id>", methods=["GET"])
def get_challenge(challenge_id):
    """get challenge info with challenge ID

    Args:
        challenge_id (str): id of challenge from files meta-data
    Returns:
        Challenge
    """
    print(db_session.execute(select(Metric)))
    return jsonify({"method": "get_challenge"})


@challenges.route("/<string:challenge_id>/submissions", methods=["POST"])
def submit_model(body, challenge_id):
    """request evaluation of model to server

    Args:
        body (dict | bytes): requestBody from client
        challenge_id (string): id of challenge from file meta-data
    Returns:
        SubmissionInfo
    """
    # if connexion.request.is_json:
    #     body = Object.from_dict(connexion.request.get_json())
    return jsonify({"method": "submit_model"})


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


