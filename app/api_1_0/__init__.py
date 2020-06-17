from flask import Blueprint

api = Blueprint('api', __name__)
if api:
    from . import errors, controllers
