import os
import json
from datetime import datetime
from time import monotonic
import json

from flask import Blueprint
from flask import request
from flask import send_file
from flask.json import jsonify

from proj_stat.services import service

datasets = Blueprint("datasets", __name__, url_prefix="/datasets")
datasets.route("/")


@datasets.route("/", methods=["GET"])
def get_datasets():
    """get all datasets as list from api server.

    Returns:
        datasets
    """
    count_param = request.args.get("count", default="", type=str)
    if count_param == "all":
        return jsonify({"result": service.get_all_datasets_count()})
    
    return jsonify({"result": service.get_all_datasets()})


@datasets.route("/<string:dataset_id>/images", methods=["GET"])
def get_image_list(dataset_id):
    """get images with imageId using ImageSets filename list

    Args:
        dataset_id (str): will be the name of .tar file
    Returns:
        Challenge
    """
    return jsonify({"result": service.get_iamge_list_from_tar(dataset_id)})


@datasets.route("/<string:dataset_id>/images/<string:image_id>", methods=["GET"])
def get_image(dataset_id: str, image_id: str):
    """request evaluation of model to server

    Args:
        challenge_id (string): id of challenge from file meta-data
    Returns:
        SubmissionInfo
    """
    return send_file(service.get_image_from_tar(dataset_id, image_id), mimetype="image/jpeg")
    # return f"call get_image with, dataset_id: {dataset_id}, image_id: {image_id}"


@datasets.route("/<string:dataset_id>/stats", methods=["GET"])
def get_stats(dataset_id):
    """if evaluated returns result else returns progress

    Args:
        challenge_id (string): id of challenge from file meta-data
        submission_id (string): id of submission on progress or done process
    Returns:
        SubmissionResult
    """
    queries_set = set(request.args.get("queries", "").split(","))
    queries_set = list(map(lambda x: x.lower().strip(), queries_set))
    return jsonify({"result": service.get_stats(dataset_id, queries_set)})


@datasets.route("/<string:dataset_id>/stats/<string:image_id>", methods=["GET"])
def get_stat(dataset_id, image_id):
    """get all status on progress and results

    Args:
        challenge_id (string): id of challenge from file meta-data
    Returns:
        response (dict): submission status and results
    """
    # return f"call get_stat with, dataset_id: {dataset_id}, image_id: {image_id}"
    queries_set = set(request.args.get("queries", "").split(","))
    queries_set = list(map(lambda x: x.lower().strip(), queries_set))
    return jsonify({"result": service.get_stat(dataset_id, image_id, queries_set)})

@datasets.route("/updateAll", methods=["GET"])
def update_datasets():
    ################ CAUTION: Have to update this method #######################
    start = datetime.now()
    service.init_datasets_col()
    service.update_database()
    return jsonify({"status": "success", "duration(microsec)": (datetime.now() - start).microseconds})
