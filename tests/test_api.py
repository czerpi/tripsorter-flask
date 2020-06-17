from test_app import url, client
import json


def test_nonexits_page_get(client):
    # Assumses that it hasn't got a path of "/"
    test_url = url+'/'
    rv = client.get(
        test_url,
        content_type='application/json',
    )
    # Assumes that it will return a 404 response
    assert rv.status_code == 404
    # Assumes that response is in json format
    assert rv.content_type == 'application/json'
    # Assumes that it will return error not found
    assert rv.json == {'error': 'not found'}


def test_trips_page_get(client):
    # Assumses that it has a path of "/api/v1.0/trips/"
    test_url = url+'/api/v1.0/trips/'
    rv = client.get(
        test_url,
        content_type='application/json',
    )
    # Assumes that it will return a 404 response
    assert rv.status_code == 405
    # Assumes that it will return error method not allowed
    assert rv.json == {"error": "method not allowed"}


def test_trips_page_empty_post(client):
    # Assumses that it has a path of "/api/v1.0/trips/"
    test_url = url+'/api/v1.0/trips/'
    rv = client.post(
        test_url,
        content_type='application/json',
    )
    # Assumes that it will return a 500 response
    assert rv.status_code == 500
    # Assumes that it will return server error
    assert rv.json == {"error": "server error"}


def test_trips_page_wrong_body_post(client):
    # Assumses that it has a path of "/api/v1.0/trips/"
    test_url = url+'/api/v1.0/trips/'
    rv = client.post(
        test_url,
        content_type='application/json',
        json={"body": "12"}
    )
    # Assumes that it will return a 400 response
    assert rv.status_code == 400
    # Assumes that it will return error invalid input
    assert rv.json == {"error": "invalid input",
                       "message": "Wrong parameters in JSON body."}


def test_trips_page_empty_trip_post(client):
    # Assumses that it has a path of "/api/v1.0/trips/"
    test_url = url+'/api/v1.0/trips/'
    rv = client.post(
        test_url,
        content_type='application/json',
        json={"body": ""}
    )
    # Assumes that it will return a 200 response
    assert rv.status_code == 200
    # Assumes that it will return 0 stages
    assert rv.json['stages'] == 0
    # Assumes that it will return no trips planned
    assert rv.json['body'] == {'0': 'No trips planned yet.'}


def test_trips_page_duplicated_origin_post(client):
    body_duplicated_origin = {"body":
                              [
                                  {"transport_type": "airportbus",
                                   "origin": "Barcelona",
                                   "destination": "Girona Airport"},
                                  {"transport_type": "airportbus",
                                   "origin": "Barcelona",
                                   "destination": "Warsaw"},
                              ]
                              }
    # Assumses that it has a path of "/api/v1.0/trips/"
    test_url = url+'/api/v1.0/trips/'
    rv = client.post(
        test_url,
        content_type='application/json',
        json=body_duplicated_origin
    )
    # Assumes that it will return a 400 response
    assert rv.status_code == 400
    # Assumes that it will return error invalid input
    assert rv.json == {"error": "invalid input",
                       "message": "Broken chain between all the legs of the trip."}


def test_trips_page_circular_trip_post(client):
    body_duplicated_origin = {"body":
                              [
                                  {"transport_type": "airportbus",
                                   "origin": "Barcelona",
                                   "destination": "Girona Airport"},
                                  {"transport_type": "airportbus",
                                   "origin": "Girona Airport",
                                   "destination": "Barcelona"},
                              ]
                              }
    # Assumses that it has a path of "/api/v1.0/trips/"
    test_url = url+'/api/v1.0/trips/'
    rv = client.post(
        test_url,
        content_type='application/json',
        json=body_duplicated_origin
    )
    # Assumes that it will return a 400 response
    assert rv.status_code == 400
    # Assumes that it will return error invalid input
    assert rv.json == {"error": "invalid input",
                       "message": "Broken chain between all the legs of the trip."}


def test_trips_page_wrong_tranport_type_post(client):
    # uses wrong tranport_type 'nonexist'
    body_wrong_transport_type = {"body":
                                 [
                                     {"transport_type": "nonexist",
                                      "origin": "Barcelona",
                                      "destination": "Girona Airport"},
                                     {"transport_type": "airportbus",
                                         "origin": "Barcelona",
                                         "destination": "Warsaw"},
                                 ]
                                 }
    # Assumses that it has a path of "/api/v1.0/trips/"
    test_url = url+'/api/v1.0/trips/'
    rv = client.post(
        test_url,
        content_type='application/json',
        json=body_wrong_transport_type
    )
    # Assumes that it will return a 400 response
    assert rv.status_code == 400
    # Assumes that it will return error invalid input
    assert rv.json == {"error": "invalid input",
                       "message": "Bad transport type 'nonexist'"}


def test_trips_page_post_ok(client):
    body_ok = {"body":
               [
                   {"transport_type": "airportbus",
                    "origin": "Barcelona",
                    "destination": "Girona Airport"},
                   {"transport_type": "plane",
                       "origin": "Girona Airport",
                       "destination": "Stockholm",
                       "transport_no": "SK455",
                       "seat": "3A",
                       "gate": "45B",
                       "baggage_drop": 344},
                   {"transport_type": "train",
                       "origin": "Madrid",
                       "destination": "Barcelona",
                       "seat": "45B",
                       "transport_no": "78A"},
                   {"transport_type": "plane",
                       "origin": "Stockholm",
                       "transport_no": "SK22",
                       "destination": "New York",
                       "seat": "7B",
                       "gate": "22"}
               ]
               }
    response_ok = {
        "body": {
            "0": "Take train 78A from Madrid to Barcelona. Sit in seat 45B.",
            "1": "Take the airport bus from Barcelona to Girona Airport. No seat assignment.",
            "2": "From Girona Airport, take flight SK455 to Stockholm. Gate 45B, seat 3A. Baggage drop at ticket counter 344.",
            "3": "From Stockholm, take flight SK22 to New York. Gate 22, seat 7B. ",
            "4": "You have arrived at your final destination."
        },
        "stages": 4,
        "url": "http://127.0.0.1:5000/api/v1.0/trips/"
    }
    # Assumses that it has a path of "/api/v1.0/trips/"
    test_url = url+'/api/v1.0/trips/'
    rv = client.post(
        test_url,
        content_type='application/json',
        json=body_ok
    )
    # Assumes that it will return a 200 response
    assert rv.status_code == 200
    # # Assumes that it will return valid response
    assert rv.json == response_ok
