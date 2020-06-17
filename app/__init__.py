import os

from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint,
                           url_prefix='/api/v1.0')
    return app


# app = create_app()
