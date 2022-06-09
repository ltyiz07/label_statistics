from flask.json import jsonify
from flask import Flask, config, redirect, render_template
import os

from insert_data import load_challenges_to_db, load_results_to_db
from evaluate_api.controller import challenges
from flasgger import Swagger
from evaluate_api.swagger.swagger import swagger_config
from evaluate_api.database import engine, db_session, Base

"""
for convert structure to api style
check this page: https://flask.palletsprojects.com/en/2.1.x/views/#method-views-for-apis
"""


def create_app(test_config=None):
    """
    entry for flask application
    if reset_database == True => drop tables and regenerate from files

    Args:
        test_config (dict): config for test if none set as default
    Returns
        app (Flask): generated flask application
    """
    reset_database = False

    app = Flask(__name__, instance_relative_config=True, template_folder=r"./templates")

    if test_config is None:
        app.config.from_mapping(
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            SWAGGER={
                'title': "Bookmarks API",
            }
        )
    else:
        app.config.from_mapping(test_config)

    if reset_database:
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        load_challenges_to_db(db_session)
        load_results_to_db(db_session)

    app.register_blueprint(challenges)
    swagger = Swagger(app, config=swagger_config, template_file="./swagger/swagger.yaml")

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.errorhandler(404)
    def handle_404(e):
        print(e)
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def handle_500(e):
        print(e)
        return jsonify({'error': 'Something went wrong, we are working on it'}), 500

    @app.teardown_request
    def shutdown_session(exception=None):
        db_session.remove()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()