import os
import json
from datetime import datetime
from time import monotonic
import json

from flask import Blueprint
from flask import request
from flask import send_file
from flask.json import jsonify

from proj_stat.services import init_service, main_service


datasets = Blueprint("datasets", __name__, url_prefix="/datasets")
datasets.route("/")


@datasets.route("/", methods=["GET"])
def get_datasets():
    """get all datasets as list from api server.

    Returns:
        datasets
    """
    if request.args.get("count", "", type=str) == "all":
        return jsonify({"result": main_service.get_all_datasets_count()})

    page = request.args.get("page", 0)
    page = 0 if page == "" else page
    pagination = main_service.DatasetPagination(page)
    pagination_obj = {
        "page": pagination.page,
        "index_gap": pagination.index_gap,
        "page_count": pagination.page_count
        }
    return jsonify({"result": main_service.get_datasets(pagination), "pagination": pagination_obj})


@datasets.route("/<string:dataset_id>/images", methods=["GET"])
def get_image_list(dataset_id):
    """get images with imageId using ImageSets filename list

    Args:
        dataset_id (str): will be the name of .tar file
    Returns:
        Challenge
    """
    tar_name, dataset_name = dataset_id.split(":")
    return jsonify({"result": main_service.get_image_list(tar_name, dataset_name)})


@datasets.route("/<string:dataset_id>/images/<string:image_name>", methods=["GET"])
def get_image(dataset_id: str, image_name: str):
    """request evaluation of model to server

    Args:
        challenge_id (string): id of challenge from file meta-data
    Returns:
        SubmissionInfo
    """
    tar_name, dataset_name = dataset_id.split(":")
    return send_file(main_service.get_image_from_tar(tar_name, image_name), mimetype="image/jpeg")
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
    tar_name, dataset_name = dataset_id.split(":")
    queries_set = set(request.args.get("queries", "").split(","))
    queries_set = set(map(lambda x: x.lower().strip(), queries_set))
    return jsonify({"result": main_service.get_stats(tar_name, dataset_name, queries_set)})


@datasets.route("/<string:dataset_id>/stats/<string:image_name>", methods=["GET"])
def get_stat(dataset_id, image_name):
    """get all status on progress and results

    Args:
        challenge_id (string): id of challenge from file meta-data
    Returns:
        response (dict): submission status and results
    """
    # return f"call get_stat with, dataset_id: {dataset_id}, image_id: {image_id}"
    tar_name, dataset_name = dataset_id.split(":")
    queries_set = set(request.args.get("queries", "").split(","))
    queries_set = list(map(lambda x: x.lower().strip(), queries_set))
    return jsonify({"result": main_service.get_stat(tar_name, image_name, queries_set)})


@datasets.route("/search/images", methods=["POST"])
def get_object_min_max_count():
    pass


@datasets.route("/search/images", methods=["POST"])
def get_image_list_with_order():
    # https://stackoverflow.com/questions/20001229/how-to-get-posted-json-in-flask
    object_list = list(request.args.get("objects", "").split(","))
    

@datasets.route("/updateAll", methods=["GET"])
def update_datasets():
    ################ CAUTION: Have to update this method #######################
    start = datetime.now()
    init_service.upload_database()
    main_service.DatasetPagination.update()
    return jsonify({"status": "success", "duration(microsec)": (datetime.now() - start).microseconds})
