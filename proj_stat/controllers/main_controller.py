import os
import json
from datetime import datetime

from flask import Blueprint, request
from flask.json import jsonify

datasets = Blueprint("datasets", __name__, url_prefix="/datasets")
datasets.route("/")


@datasets.route("/", methods=["GET"])
def get_datasets():
    """get all datasets as list from api server.

    Returns:
        datasets
    """
    return jsonify(["hello", "world"])


@datasets.route("/<string:challenge_id>", methods=["GET"])
def get_challenge(challenge_id):
    """get challenge info with challenge ID

    Args:
        challenge_id (str): id of challenge from files meta-data
    Returns:
        Challenge
    """

    return "test"


@datasets.route("/<string:challenge_id>/submissions", methods=["POST"])
def submit_model(challenge_id):
    """request evaluation of model to server

    Args:
        challenge_id (string): id of challenge from file meta-data
    Returns:
        SubmissionInfo
    """
    return "test"


@datasets.route("/<string:challenge_id>/submissions/<string:submission_id>", methods=["GET"])
def get_status_or_result(challenge_id, submission_id):
    """if evaluated returns result else returns progress

    Args:
        challenge_id (string): id of challenge from file meta-data
        submission_id (string): id of submission on progress or done process
    Returns:
        SubmissionResult
    """
    return "test"


@datasets.route("/<string:challenge_id>/submissions", methods=["GET"])
def get_status_and_results(challenge_id):
    """get all status on progress and results

    Args:
        challenge_id (string): id of challenge from file meta-data
    Returns:
        response (dict): submission status and results
    """
    return "test"
