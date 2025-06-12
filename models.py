from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, Union
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
    FlightLeg = 'FlightLeg'
    Hotel = 'Hotel'
    Car = 'Car'
    Activity = 'Activity'

class CarRentalCompany(str, Enum):
    Avis = 'Avis'
    Hertz = 'Hertz'
    Fox = 'Fox'
    Sixt = 'Sixt'
    Budget = 'Budget'
    Thrifty = 'Thrifty'
    Alamo = 'Alamo'
    Enterprise = 'Enterprise'
    National = 'National'
    Other = 'Other'

class BaseItineraryItem(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    
    def generate_gmaps_url(self, address: str):
        gmaps_url = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote_plus(address)}"
        return gmaps_url

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
        st.markdown(f"Address: [{self.address}]({self.generate_gmaps_url(self.address)})")
    
    def display_end(self):
        st.markdown(f"#### {self.name}")
        st.markdown(f":red[Check-Out Time]: {self.end_time}")
        
    
class FlightLeg(BaseItineraryItem):
    category: ItineraryType = ItineraryType.FlightLeg
    flight_id: Optional[str] = None
    origin: Airport
    origin_terminal: Optional[str] = None
    destination: Airport
    destination_terminal: Optional[str] = None
    confirmation: Optional[str] = None
    airline: Airline
    cost: Optional[float] = None
    
    def display_start(self):
        st.markdown(f"#### {self.airline.value}")
        st.markdown(f":red[Origin]: [{self.origin.value}]({self.generate_gmaps_url(self.origin)})")
        if self.origin_terminal:
            st.markdown(f":red[Origin Terminal]: {self.origin_terminal}")
        if self.start_time:
            st.markdown(f":red[Departure Time]: {self.start_time}")
    
    def display_end(self):
        st.markdown(f"#### {self.airline.value}")
        st.markdown(f":red[Destination]: [{self.destination.value}]({self.generate_gmaps_url(self.destination)})")
        if self.end_time:
            st.markdown(f":red[Arrival Time]: {self.end_time}")
        if self.destination_terminal:
            st.markdown(f":red[Destination Terminal]: {self.destination_terminal}")

class Flight(BaseItineraryItem):
    category: ItineraryType = ItineraryType.Flight
    trip_id: str
    origin: Airport
    destination: Airport
    notes: Optional[str] = None

class FlightwithLegs(Flight):
    legs: list[FlightLeg]

class Car(BaseItineraryItem):
    category: ItineraryType = ItineraryType.Car
    trip_id: str
    rental_company: Optional[str]
    pickup_location: str
    dropoff_location: str
    cost: float
    notes: Optional[str] = None
    
    def display_start(self):
        st.markdown(f"#### {self.rental_company}")
        st.markdown(f":red[Pickup Location]: [{self.pickup_location}]({self.generate_gmaps_url(self.pickup_location)})")
        st.markdown(f":red[Pickup Time]: {self.start_time}")
    
    def display_end(self):
        st.markdown(f"#### {self.rental_company}")
        dropoff_location = self.dropoff_location if self.dropoff_location else self.pickup_location
        st.markdown(f":red[Dropoff Location]: [{dropoff_location}]({self.generate_gmaps_url(dropoff_location)})")
        st.markdown(f":red[Dropoff Time]: {self.end_time}")

class Activity(BaseItineraryItem):
    category: ItineraryType = ItineraryType.Activity
    trip_id: str
    name: str
    location: str
    description: str
    cost: float
    
    def display_start(self):
        st.markdown(f"#### {self.name}")
        st.markdown(f":red[Location]: [{self.location}]({self.generate_gmaps_url(self.location)})")
        if self.start_time:
            st.markdown(f":red[Start Time]: {self.start_time}")

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