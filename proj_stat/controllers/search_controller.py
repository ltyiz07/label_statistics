import os
import json
from datetime import datetime
from time import monotonic
import json

from flask import Blueprint
from flask import request
from flask import send_file
from flask.json import jsonify

from proj_stat.services import main_service


search = Blueprint("search", __name__, url_prefix="/search")
search.route("/")


@search.route("/objects", methods=["GET", "POST"])
def get_object_with_max_count():
    if request.method == "GET":
        """Response unique objects with its min-max count
        """
        return jsonify({"result": main_service.get_object_count_all()})

    elif request.method == "POST":
        # https://stackoverflow.com/questions/20001229/how-to-get-posted-json-in-flask
        # get JSON type data with object_name and min, max count
        """Response image list with its best fits orders
        """
        pass
