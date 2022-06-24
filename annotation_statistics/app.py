import os

from flask.json import jsonify
from flask import Flask, render_template
from flasgger import Swagger

from annotation_statistics.controllers.main_controller import challenges
from annotation_statistics.swagger.swagger import swagger_config
from annotation_statistics.database import db_session

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

    #### this code should moved to module under service
    # reset_database = True
    # if reset_database:
    #     Base.metadata.drop_all(bind=engine)
    #     Base.metadata.create_all(bind=engine)
    #     load_challenges_to_db(db_session)
    #     load_results_to_db(db_session)

    app.register_blueprint(challenges)
    Swagger(app, config=swagger_config, template_file="./swagger/swagger.yaml")

    @app.get("/")
    def index():
        return render_template("index.html")

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
        db_session.remove()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()