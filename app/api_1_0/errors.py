
from flask import jsonify

from . import api


class ValidationError(ValueError):
    pass


@api.app_errorhandler(400)
def json_server_error(e):
    response = jsonify({'error': 'invalid input',
                        'message': e.args[0]})
    response.status_code = 400
    return response


@api.app_errorhandler(404)
def page_not_found(e):
    response = jsonify({'error': 'not found'})
    response.status_code = 404
    return response


@api.app_errorhandler(405)
def page_not_found(e):
    response = jsonify({'error': 'method not allowed'})
    response.status_code = 405
    return response


@api.app_errorhandler(500)
def internal_server_error(e):
    response = jsonify({'error': 'server error'})
    response.status_code = 500
    return response


@api.errorhandler(ValidationError)
def validation_error(e):
    return json_server_error(e)
