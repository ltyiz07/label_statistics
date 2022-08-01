from flask import Blueprint
from flask import request
from flask import render_template


pages = Blueprint("pages", __name__, url_prefix="/pages")
pages.route("/")


@pages.route("/subsets", methods=["GET"])
def subsets():
    page = request.args.get("page", 0)
    return render_template("index.html", page=page)

@pages.route("/search", methods=["GET"])
def search():
    return render_template("search.html")