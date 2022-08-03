import os

from flask.json import jsonify
from flask import Flask
from flask import redirect
from flasgger import Swagger

from proj_stat.controllers.main_controller import datasets
from proj_stat.controllers.search_controller import search
from proj_stat.controllers.page_controller import pages
from proj_stat.swagger.swagger import swagger_config

"""
for convert structure to api style
check this page: https://flask.palletsprojects.com/en/2.1.x/views/#method-views-for-apis
"""


def create_app():
    """
    entry for flask application

    Args:
        test_config (dict): config for test if none set as default
    Returns
        app (Flask): generated flask application
    """

    app = Flask(__name__, instance_relative_config=True, template_folder=r"./templates")
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SWAGGER={
            'title': "Database Statistics API",
        }
    )

    app.register_blueprint(datasets)
    app.register_blueprint(search)
    app.register_blueprint(pages)

    Swagger(app, config=swagger_config, template_file="./swagger/swagger.yaml")

    @app.get("/")
    def index():
        return redirect("/pages/subsets", code=302)

    @app.errorhandler(404)
    def handle_404(e):
        print(e)
        return jsonify({'error': 'Not Found'}), 404

    @app.errorhandler(500)
    def handle_500(e):
        print(e)
        return jsonify({'error': 'Something went wrong, we are working on it'}), 500

    @app.teardown_request
    def shutdown_session(exception=None):
        """
        cleanup request scope objects (ex: database session/transaction)
        """
    return app


if __name__ == "__main__":
    app = create_app()
    app.run()