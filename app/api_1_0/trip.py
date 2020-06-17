import json
from collections import UserDict

from flask import jsonify, url_for

from .boardingcard import BoardingCard
from .errors import ValidationError


class Trip(UserDict):
    """Trip dictionary class to keep trip stages"""

    def __iter__(self):
        """Class iterator definition. 
        Finds the begining of the trip and iterates 
        from origin via destination to another origin 
        until there is no other origin"""
        if self.data.keys():
            origin = set(self.data.keys()) - \
                {v.destination for v in self.data.values()}
            if len(origin) != 1:
                # check if only one origin exists in not empty dictionary
                raise ValidationError(
                    'Broken chain between all the legs of the trip.')
            orig = origin.pop()
            while True:
                try:
                    yield self.data[orig]
                    orig = self.data[orig].destination
                except KeyError as exc:
                    break
        return

    def __setitem__(self, key, item):
        """Blocks inserting the same origin"""
        if key not in self.data.keys():
            self.data[key] = item
        else:
            raise ValidationError(
                'Broken chain between all the legs of the trip.')

    def to_json(self):
        """Creates dictionary for JSON response with list of trip stages."""
        body_list = [str(trip) for trip in self]
        if body_list:
            body_list.append('You have arrived at your final destination.')
        else:
            body_list = ['No trips planned yet.']
        body = {num: txt for num, txt in enumerate(body_list)}
        json_post = {
            'url': url_for('api.get_trips', _external=True),
            'stages': len(self.data),
            'body': body
        }
        return json_post

    @staticmethod
    def from_json(json_response):
        """Creates stages of Trip from JSON request"""
        trip = Trip()
        try:
            body = json_response['body']
        except:
            raise ValidationError('Wrong parameters in JSON body.')

        for stage in body:
            try:
                origin = stage.get('origin')
            except:
                raise ValidationError('Wrong parameters in JSON body.')

            trip[origin] = BoardingCard.create(**stage)

        return trip
