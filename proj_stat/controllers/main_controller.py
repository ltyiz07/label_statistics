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
    return "call get_datasets"


@datasets.route("/<string:dataset_id>/images", methods=["GET"])
def get_image_list(dataset_id):
    """get images with imageId using ImageSets filename list

    Args:
        dataset_id (str): will be the name of .tar file
    Returns:
        Challenge
    """
    return f"call get_image_list with, dataset_id: {dataset_id}"


@datasets.route("/<string:dataset_id>/images/<string:image_id>", methods=["GET"])
def get_image(dataset_id: str, image_id: str):
    """request evaluation of model to server

    Args:
        challenge_id (string): id of challenge from file meta-data
    Returns:
        SubmissionInfo
    """
    return f"call get_image with, dataset_id: {dataset_id}, image_id: {image_id}"


@datasets.route("/<string:dataset_id>/stats", methods=["GET"])
def get_stats(dataset_id):
    """if evaluated returns result else returns progress

    Args:
        challenge_id (string): id of challenge from file meta-data
        submission_id (string): id of submission on progress or done process
    Returns:
        SubmissionResult
    """
    return f"call get_stats with, dataset_id: {dataset_id}"


@datasets.route("/<string:dataset_id>/stats/<string:image_id>", methods=["GET"])
def get_stat(dataset_id, image_id):
    """get all status on progress and results

    Args:
        challenge_id (string): id of challenge from file meta-data
    Returns:
        response (dict): submission status and results
    """
    return f"call get_stat with, dataset_id: {dataset_id}, image_id: {image_id}"
