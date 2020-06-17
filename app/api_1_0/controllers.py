from flask import jsonify, request

from . import api
from .trip import Trip


@api.route('/trips/', methods=['POST'])
def get_trips():
    """Returns sorted trip stages"""
    trip = Trip.from_json(request.json)
    return jsonify(trip.to_json())
