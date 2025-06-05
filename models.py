from dataclasses import dataclass
from typing import List
from enum import Enum, auto
from datetime import date, time
import uuid

class Airport(Enum):
    BOS = "BOS (Boston Logan)"
    SJC = "SJC (San Jose)"
    SFO = "SFO (San Francisco)"
    LAX = "LAX (Los Angeles)"
    JFK = "JFK (John F. Kennedy)"
    DCA = "DCA (Washington Dulles)"

class Airline(Enum):
    JetBlue = 'JetBlue'
    Delta = 'Delta'
    United = 'United'
    American = 'American'
    Etihad = 'Etihad'
    Emirates = 'Emirates'
    Southwest = 'Southwest'
    
class ItineraryType(Enum):
    Flight = 'Flight'
    Hotel = 'Hotel'
    Car = 'Car'
    Activity = 'Activity'

@dataclass
class FlightLeg:
    origin: Airport
    departure_time: str
    destination: Airport
    arrival_time: str
    
@dataclass
class ItineraryFlight:
    origin: Airport
    airline: str
    destination: Airport
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
    notes: str
    cost: float

@dataclass
class ItineraryCar:
    pick_up_location: str
    pick_up_date: date
    pick_up_time: time
    drop_off_location: str
    drop_off_date: date
    drop_off_time: time
    cost: float

@dataclass
class ItineraryActivity:
    name: str
    location: str
    description: str
    cost: float
    
@dataclass
class ItineraryItem:
    type: ItineraryType
    item: ItineraryFlight | ItineraryHotel | ItineraryCar | ItineraryActivity

@dataclass
class Trip:
    id: uuid
    name: str
    start_date: date
    end_date: date
    itinerary: List[ItineraryItem]