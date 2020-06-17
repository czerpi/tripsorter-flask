# TripSorter API v.1.0

**TripSorter is a FLASK REST API for sorting trip stages.**

API JSON with a stack of boarding cards for various transportations that will take you from point A to point B via several stops on the way.

All of the boarding cards are out of order and you don't know where your journey starts, nor where it ends. Each boarding card contains information about seat assignment, and means of transportation (such as flight number, bus number, etc).Sorting algorithm should work with any set of boarding passes, as long as there is always an unbroken chain between all the legs of the trip.

API takes an unordered set of boarding cards in **one single  JSON** request body and responds sorted list.


## Installation

```bash
git clone https://github.com/czerpi/tripsorter-flask.git
cd tripsorter-flask
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Run

```bash
export FLASK_APP=app
flask run
```

## Test

```bash
pip install '.[test]'
pytest
```

Run with coverage report:
```bash
coverage run -m pytest
coverage report
coverage html  # open htmlcov/index.html in a browser
```

## API overview
The API is RESTFUL and returns results only in JSON. 

**[OPENAPI documentation is available via link.](https://app.swaggerhub.com/apis-docs/czerpi/tripsorter-flask/1.0.0-oas3)**

You can test the trip sorter by sending POST with *body* list of stages to the following route:

http://127.0.0.1:5000/api/v1.0/trips/

Testing the following trip with 3 different transport modes (train, airport bus, plane):

```json
{"body":[{"transport_type": "airportbus",          
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
  "gate": "22"}]}
```

Using the [curl](https://curl.haxx.se/) for testing:
```bash
curl -X POST -H "Content-Type: application/json" -d 'PUT BODYHERE' http://127.0.0.1:5000/api/v1.0/trips/
```


Will return the following result:
```json
{
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
```

## Create new types of transportation

**Simple class for transport mode**
```python
class NewTranportBoardingCard(BoardingCard):
    """New Transport Boarding Card class.
    Takes only two parameters (origin, destination)"""
    _BOARDINGCARTTYPE = 'newtransport'

    def __str__(self):
        return f'Take new transport mode from {self.origin} to {self.destination}'

```

**Enhanced class for transport mode**
```python
class OtherTranportBoardingCard(BoardingCard):
    """Other Transport Boarding Card class.
    Takes more parameters"""
    _BOARDINGCARTTYPE = 'othertransport'

    def __init__(self,
                 origin,
                 destination,
                 transport_no,
                 seat,
                 departure_time):
        super().__init__(origin, destination)
        self.transport_no = transport_no
        self.seat = seat
        self.departure_time = departure_time

    def __str__(self):
        sentence1 = f'Take transport {self.transport_no} at {self.departure_time} '
        sentence1 += f'from {self.origin} to {self.destination}.'
        sentence2 = f'Sit in seat {self.seat}.'
        return ' '.join([sentence1, sentence2])

```
