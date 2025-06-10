from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Union
from enum import Enum
from datetime import date, time
import streamlit as st
import urllib.parse
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
    category: ItineraryType = ItineraryType.Hotel
    trip_id: str
    name: str
    address: str
    maps_url: HttpUrl
    notes: Optional[str] = None
    cost: float
    
    def display_start(self):
        st.markdown(f"#### {self.name}")
        st.markdown(f":red[Check-In Time]: {self.start_time}")
        st.markdown(f"Maps URL: {self.maps_url}")
    
    def display_end(self):
        st.markdown(f"#### {self.name}")
        st.markdown(f":red[Check-Out Time]: {self.end_time}")
        st.markdown(f"Maps URL: {self.maps_url}")
    
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

class Car(BaseItineraryItem):
    category: ItineraryType = ItineraryType.Car
    trip_id: str
    pickup_location: str
    dropoff_location: str
    cost: float
    notes: Optional[str] = None
    
    def display_start(self):
        st.markdown(f"#### {self.pickup_location}")
        st.markdown(f":red[Pickup Time]: {self.start_time}")
    
    def display_end(self):
        dropoff_location = self.dropoff_location if self.dropoff_location else self.pickup_location
        gmaps_url = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote_plus(dropoff_location)}"
        st.markdown(f"##### [{dropoff_location}]({gmaps_url})")
        st.markdown(f":red[Dropoff Time]: {self.end_time}")

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