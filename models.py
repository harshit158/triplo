from dataclasses import dataclass
from typing import List, enum
from datetime import date
import uuid

class ItineraryType(enum.Enum):
    Flight = 'Flight'
    Hotel = 'Hotel'
    Car = 'Car'
    Activity = 'Activity'

@dataclass
class FlightLeg:
    origin: str
    departure_time: str
    destination: str
    arrival_time: str
    
@dataclass
class ItineraryFlight:
    origin: str
    airline: str
    destination: str
    confirmation: str
    legs: list[FlightLeg]
    cost: float

@dataclass
class ItineraryHotel:
    name: str
    address: str
    maps_url: str
    check_in_date: str
    check_in_time: str
    check_out_date: str
    check_out_time: str
    cost: float

@dataclass
class ItineraryCar:
    pick_up_location: str
    pick_up_date: str
    pick_up_time: str
    drop_off_location: str
    drop_off_date: str
    drop_off_time: str
    cost: float
    
@dataclass
class ItineraryItem:
    type: ItineraryType
    details: ItineraryFlight | ItineraryHotel | ItineraryCar

@dataclass
class Trip:
    id: uuid
    name: str
    start_date: date
    end_date: date
    itinerary: List[ItineraryItem]