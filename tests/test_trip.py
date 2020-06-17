import pytest
from app.api_1_0.boardingcard import BoardingCard
from app.api_1_0.trip import Trip
from app.api_1_0.errors import ValidationError
from test_app import url, client


def test_trip_class():
    trip = Trip()
    # Assumes that trip is a dictionary
    assert trip == {}
    # Assumes that trip is empty
    assert len(trip) == 0

    # Assumes that wrong json will raise ValidationError
    with pytest.raises(ValidationError):
        trip.from_json({})


def test_trip_sorting():
    # creates test trip
    trip = Trip()
    trip['Barcelona'] = BoardingCard.create(
        **{"transport_type": "airportbus",
           "origin": "Barcelona",
           "destination": "Girona Airport"})
    trip['Girona Airport'] = BoardingCard.create(
        **{"transport_type": "plane",
           "origin": "Girona Airport",
           "destination": "Stockholm",
           "transport_no": "SK455",
           "seat": "3A",
           "gate": "45B",
           "baggage_drop": 344})
    trip['Madrid'] = BoardingCard.create(
        ** {"transport_type": "train",
            "origin": "Madrid",
            "destination": "Barcelona",
            "seat": "45B",
            "transport_no": "78A"})
    trip['Stockholm'] = BoardingCard.create(
        **{"transport_type": "plane",
           "origin": "Stockholm",
           "transport_no": "SK22",
           "destination": "New York",
           "seat": "7B",
           "gate": "22"})

    # Assumes that trip has 4 stages
    assert len(trip) == 4

    it = iter(trip)
    # Assumes that trip starts in Madrid
    assert next(it) == 'Madrid'

    # Assumes that trip stages are in the
    # following order Madrid => Barcelona => Girona Airport => Stockholm
    assert [origin for origin in trip] == [
        'Madrid', 'Barcelona', 'Girona Airport', 'Stockholm']

    # Checks Girona Airport stage printout
    ans = 'From Girona Airport, take flight SK455 to Stockholm. Gate 45B, seat 3A. Baggage drop at ticket counter 344.'
    assert trip['Girona Airport'].description() == ans


def test_trip_duplicate_origin():
    # creates test trip
    trip = Trip()
    trip['Barcelona'] = BoardingCard.create(
        **{"transport_type": "airportbus",
           "origin": "Barcelona",
           "destination": "Girona Airport"})

    # Assumses that one cannot add the same origin
    with pytest.raises(ValidationError):
        trip['Barcelona'] = BoardingCard.create(
            **{"transport_type": "plane",
               "origin": "Barcelona",
               "destination": "Stockholm",
               "transport_no": "SK455",
               "seat": "3A",
               "gate": "45B",
               "baggage_drop": 344})


def test_trip_duplicate_destination():
    # creates test trip
    trip = Trip()
    trip['Barcelona'] = BoardingCard.create(
        **{"transport_type": "airportbus",
           "origin": "Barcelona",
           "destination": "Girona Airport"})

    # add duplicated destination
    trip['Stockholm'] = BoardingCard.create(
        **{"transport_type": "plane",
           "origin": "Stockholm",
           "destination": "Girona Airport",
           "transport_no": "SK455",
           "seat": "3A",
           "gate": "45B",
           "baggage_drop": 344})

    it = iter(trip)
    with pytest.raises(ValidationError):
        assert next(it)


def test_trip_unlinked_stages():
    # creates test trip
    trip = Trip()
    trip['Barcelona'] = BoardingCard.create(
        **{"transport_type": "airportbus",
           "origin": "Barcelona",
           "destination": "Girona Airport"})

    # add unlinked stages
    trip['Stockholm'] = BoardingCard.create(
        **{"transport_type": "plane",
           "origin": "Stockholm",
           "destination": "Warszawa",
           "transport_no": "SK455",
           "seat": "3A",
           "gate": "45B",
           "baggage_drop": 344})

    it = iter(trip)
    with pytest.raises(ValidationError):
        assert next(it)


def test_trip_circular():
    # creates test trip
    trip = Trip()
    trip['Barcelona'] = BoardingCard.create(
        **{"transport_type": "airportbus",
           "origin": "Barcelona",
           "destination": "Girona Airport"})
    trip['Girona Airport'] = BoardingCard.create(
        **{"transport_type": "plane",
           "origin": "Girona Airport",
           "destination": "Madrid",
           "transport_no": "SK455",
           "seat": "3A",
           "gate": "45B",
           "baggage_drop": 344})
    trip['Madrid'] = BoardingCard.create(
        ** {"transport_type": "train",
            "origin": "Madrid",
            "destination": "Barcelona",
            "seat": "45B",
            "transport_no": "78A"})

    it = iter(trip)
    with pytest.raises(ValidationError):
        assert next(it)


def test_trip_circular_duplicate_destination():
    # creates test trip
    trip = Trip()
    trip['Barcelona'] = BoardingCard.create(
        **{"transport_type": "airportbus",
           "origin": "Barcelona",
           "destination": "Girona Airport"})
    trip['Girona Airport'] = BoardingCard.create(
        **{"transport_type": "plane",
           "origin": "Girona Airport",
           "destination": "Barcelona",
           "transport_no": "SK455",
           "seat": "3A",
           "gate": "45B",
           "baggage_drop": 344})
    trip['Madrid'] = BoardingCard.create(
        ** {"transport_type": "train",
            "origin": "Madrid",
            "destination": "Barcelona",
            "seat": "45B",
            "transport_no": "78A"})

    it = iter(trip)
    with pytest.raises(ValidationError):
        assert next(it)
