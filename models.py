from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Union
from enum import Enum
from datetime import date, time
import streamlit as st
import uuid

# Enums
class Airport(str, Enum):
    BOS = "BOS (Boston Logan)"
    SJC = "SJC (San Jose)"
    SFO = "SFO (San Francisco)"
    LAX = "LAX (Los Angeles)"
    JFK = "JFK (John F. Kennedy)"
    DCA = "DCA (Washington Dulles)"

class Airline(str, Enum):
    JetBlue = 'JetBlue'
    Delta = 'Delta'
    United = 'United'
    American = 'American'
    Etihad = 'Etihad'
    Emirates = 'Emirates'
    Southwest = 'Southwest'

class ItineraryType(str, Enum):
    Flight = 'Flight'
    Hotel = 'Hotel'
    Car = 'Car'
    Activity = 'Activity'

class BaseItineraryItem(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    start_date: date
    end_date: Optional[date]
    start_time: Optional[time]
    end_time: Optional[time]

class Hotel(BaseItineraryItem):
    trip_id: str
    name: str
    address: str
    maps_url: HttpUrl
    notes: Optional[str] = None
    cost: float
    
    def display_start(self):
        return st.markdown(f"{self.start_date} {self.start_time}")
    
    def display_end(self):
        return st.markdown(f"{self.end_date} {self.end_time}")
    
class FlightLeg(BaseModel):
    origin: Airport
    departure_time: time
    destination: Airport
    arrival_time: time

class Flight(BaseModel):
    origin: Airport
    airline: Airline
    destination: Airport
    confirmation: str
    legs: List[FlightLeg]
    cost: float
    notes: Optional[str] = None

class Car(BaseModel):
    pick_up_location: str
    pick_up_date: date
    pick_up_time: time
    drop_off_location: str
    drop_off_date: date
    drop_off_time: time
    cost: float
    notes: Optional[str] = None

class Activity(BaseModel):
    name: str
    location: str
    description: str
    cost: float

# Polymorphic itinerary item
class ItineraryItem(BaseModel):
    type: ItineraryType
    item: Union[Flight, Hotel, Car, Activity]

# Trip model
class Trip(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    start_date: date
    end_date: date
    notes: Optional[str] = None