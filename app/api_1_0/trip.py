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
        if self:
            destinations = [v.destination for v in self.data.values()]
            destinations_set = set(destinations)

            if len(destinations) != len(destinations_set):
                # checks if there are not duplicated destinations
                raise ValidationError(
                    'Broken chain between all the legs of the trip. Duplicated destinations.')

            possible_origin = set(self.data.keys()) - set(destinations)
            if len(possible_origin) != 1:
                # check if only one origin exists in not empty dictionary
                raise ValidationError(
                    'Broken chain between all the legs of the trip. Lack of one origin.')
            origin = possible_origin.pop()
            while True:
                if origin not in self:
                    break
                yield origin
                origin = self.data[origin].destination
        return

    def __setitem__(self, key, item):
        """Blocks inserting the same origin"""
        if key not in self.data.keys():
            self.data[key] = item
        else:
            raise ValidationError(
                'Broken chain between all the legs of the trip. Duplicated origins.')

    def to_json(self):
        """Creates dictionary for JSON response with list of trip stages."""
        cards_list = [self[trip].description() for trip in self]
        if cards_list:
            cards_list.append('You have arrived at your final destination.')
        else:
            cards_list = ['No trips planned yet.']
        return {'cards': cards_list}

    @staticmethod
    def from_json(json_response):
        """Creates stages of Trip from JSON request"""
        trip = Trip()
        try:
            cards = json_response['cards']
        except KeyError:
            raise ValidationError('Wrong parameters in JSON.')
        for card in cards:
            try:
                origin = card['origin']
            except KeyError:
                raise ValidationError('Wrong parameters in JSON.')
            trip[origin] = BoardingCard.create(**card)
        return trip
