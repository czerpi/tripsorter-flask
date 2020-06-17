from abc import ABC, ABCMeta, abstractmethod

from .errors import ValidationError


class BoardingCard(ABC):
    """Boarding Card abstract class"""
    subclasses = {}

    def __init__(self,
                 origin,
                 destination):
        self.origin = origin
        self.destination = destination

    @property
    @abstractmethod
    def _BOARDINGCARTTYPE(self):
        """Set Boarding cart type"""

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.subclasses[cls._BOARDINGCARTTYPE] = cls

    @classmethod
    def create(cls, transport_type, *args, **kwargs):
        """Creates BoardingCard subclass based on the given transport type."""
        if transport_type not in cls.subclasses:
            raise ValidationError(f"Bad transport type '{transport_type}'")
        return cls.subclasses[transport_type](*args, **kwargs)

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.origin} {self.destination}>'

    @abstractmethod
    def description(self):
        """Print way from <Origin> to <Destination>"""


class TrainBoardingCard(BoardingCard):
    """Boarding Card for train"""
    _BOARDINGCARTTYPE = 'train'

    def __init__(self,
                 origin,
                 destination,
                 transport_no,
                 seat):
        super().__init__(origin, destination)
        self.transport_no = transport_no
        self.seat = seat

    def description(self):
        sentence1 = f'Take train {self.transport_no} from '
        sentence1 += f'{self.origin} to {self.destination}.'
        sentence2 = f'Sit in seat {self.seat}.'
        return ' '.join([sentence1, sentence2])


class AirportBusBoardingCard(BoardingCard):
    """Boarding Card for airport bus"""
    _BOARDINGCARTTYPE = 'airportbus'

    def __init__(self,
                 origin,
                 destination,
                 ):
        super().__init__(origin, destination)

    def description(self):
        sentence1 = f'Take the airport bus from {self.origin} '
        sentence1 += f'to {self.destination}.'
        sentence2 = 'No seat assignment.'
        return ' '.join([sentence1, sentence2])


class PlaneBoardingCard(BoardingCard):
    """Boarding Card for plane"""
    _BOARDINGCARTTYPE = 'plane'

    def __init__(self,
                 origin,
                 destination,
                 transport_no,
                 gate,
                 seat,
                 baggage_drop=''):
        super().__init__(origin, destination)
        self.transport_no = transport_no
        self.gate = gate
        self.seat = seat
        self.baggage_drop = baggage_drop

    def description(self):
        sentence1 = f'From {self.origin}, take flight {self.transport_no} '
        sentence1 += f'to {self.destination}.'
        sentence2 = f'Gate {self.gate}, seat {self.seat}.'
        sentence3 = f'Baggage drop at ticket counter {self.baggage_drop}.' \
            if self.baggage_drop else ''

        return ' '.join([sentence1, sentence2, sentence3])
