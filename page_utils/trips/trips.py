import streamlit as st
import os
from collections import defaultdict
from utils import utils, maps_utils, api_utils
from models import ItineraryType, Flight, FlightLeg, FlightwithLegs, Hotel, Car, Activity, Airport, Airline, Trip, CarRentalCompany

def display_trip(trip: Trip):    
    hotels = api_utils.fetch_all("hotel", Hotel, filter_field="trip_id", filter_value=trip.id)
    cars = api_utils.fetch_all("car", Car, filter_field="trip_id", filter_value=trip.id)
    activity = api_utils.fetch_all("activity", Activity, filter_field="trip_id", filter_value=trip.id)
    
    flights = api_utils.fetch_all("flight", Flight, filter_field="trip_id", filter_value=trip.id)
    legs = []
    for flight in flights:
        flight_legs = api_utils.fetch_all("flightleg", FlightLeg, filter_field="flight_id", filter_value=flight.id)
        legs.extend(flight_legs)
    
    all_itineraries = hotels + cars + activity + legs
    dates = defaultdict(list)
    
    for itinerary in all_itineraries:
        dates[itinerary.start_date].append([itinerary.display_start, itinerary, itinerary.start_time])
        if itinerary.end_date:
            dates[itinerary.end_date].append([itinerary.display_end, itinerary, itinerary.end_time])
    
    dates_and_itineraries = utils.sort_itineraries(dates)
    
    icons = {
        ItineraryType.FlightLeg: "✈️",
        ItineraryType.Hotel: "🏨",
        ItineraryType.Car: "🚗",
        ItineraryType.Activity: "🎉"
    }
    
    with st.columns(1, border=False)[0]:
        st.title(trip.name)
        st.write(f"{trip.start_date} -> {trip.end_date}")
        
        with st.expander("", expanded=True):
            cols = st.columns(2)
            
            with cols[0]:
                add_itinerary(trip.id)
                
                with st.container(height=500):
                    for date, display_funcs_and_itineraries in dates_and_itineraries.items():
                        st.markdown(f"<h4 style='text-align: left; padding: 0px; color: green;'>{date}</h4><br>", unsafe_allow_html=True)
                        for i, (func, itinerary, time) in enumerate(display_funcs_and_itineraries):
                            st.markdown(f"<h5 style='text-align: left; background-color: #E8E8E8; padding: 0px;'>{icons[itinerary.category]} {itinerary.category.value}</h5><br>", unsafe_allow_html=True)
                            func()
                            with st.popover(f"Details"):
                                st.button("Delete", key=f"delete_{date}_{i}_{itinerary.id}", on_click=api_utils.delete_itinerary, args=(itinerary.__class__.__name__.lower(), itinerary.id), use_container_width=True)
                            st.divider()
            
            with cols[1]:
                maps_utils.display_map(dates_and_itineraries)
                
    
def display_trips():
    trips = api_utils.fetch_all("trip", Trip)
    for trip in trips:
        display_trip(trip)
    
def add_itinerary(trip_id: str):
    with st.popover("Add Itinerary", use_container_width=True):
        st.header("Add New Itinerary Item")

        itinerary_type = st.selectbox(
            "Select Itinerary Type",
            options=[t.value for t in ItineraryType if t != ItineraryType.FlightLeg],
            key=f"itinerary_type_{trip_id}"
        )

        if itinerary_type == ItineraryType.Flight.value:
            origin = st.selectbox("Origin", options=[a.value for a in Airport], key=f"flight_origin_{trip_id}")
            destination = st.selectbox("Destination", options=[a.value for a in Airport], key=f"flight_destination_{trip_id}")
            notes = st.text_area("Notes", key=f"flight_notes_{trip_id}")
            
            num_legs = st.selectbox("Number of Flight Legs", options=[1, 2, 3], key=f"flight_num_legs_{trip_id}")
            legs = []
            for i in range(num_legs):
                st.subheader(f"Leg {i+1}")
                leg_airline = st.selectbox(f"Airline", options=[a.value for a in Airline], key=f'leg_airline_{i}_{trip_id}')
                leg_confirmation = st.text_input(f"Confirmation Number", key=f'leg_conf_{i}_{trip_id}')
                leg_cost = st.number_input(f"Cost", min_value=0.0, key=f'leg_cost_{i}_{trip_id}')
                leg_origin = st.selectbox(f"Origin", options=[a.value for a in Airport], key=f'leg_origin_{i}_{trip_id}')
                leg_origin_terminal = st.text_input(f"Origin Terminal", key=f'leg_origin_terminal_{i}_{trip_id}')
                leg_departure_date = st.date_input(f"Departure Date", key=f'leg_dep_date_{i}_{trip_id}')
                leg_departure_time = st.time_input(f"Departure Time", key=f'leg_dep_{i}_{trip_id}', step=300)
                leg_destination = st.selectbox(f"Destination", options=[a.value for a in Airport], key=f'leg_dest_{i}_{trip_id}')
                leg_destination_terminal = st.text_input(f"Destination Terminal", key=f'leg_dest_terminal_{i}_{trip_id}')
                leg_arrival_date = st.date_input(f"Arrival Date", key=f'leg_arr_date_{i}_{trip_id}')
                leg_arrival_time = st.time_input(f"Arrival Time", key=f'leg_arrival_{i}_{trip_id}', step=300)
                legs.append(FlightLeg(origin=leg_origin, 
                                      origin_terminal=leg_origin_terminal,
                                      airline=leg_airline,
                                      confirmation=leg_confirmation,
                                      cost=leg_cost,
                                      start_date=leg_departure_date, 
                                      start_time=leg_departure_time, 
                                      destination=leg_destination,
                                      destination_terminal=leg_destination_terminal,
                                      end_date=leg_arrival_date, 
                                      end_time=leg_arrival_time))

            if st.button("Add Flight", use_container_width=True, key=f"add_flight_{trip_id}"):
                    flight = Flight(
                        trip_id=trip_id,
                        origin=origin,
                        destination=destination,
                        notes=notes
                    )
                    
                    st.toast(f"Flight added", icon="✅")
                    flight_id = api_utils.insert(flight)
                    
                    for leg in legs:
                        leg.flight_id = flight_id
                        api_utils.insert(leg)
                    
                    utils.clear_cache()
                    st.rerun()
                    

        elif itinerary_type == ItineraryType.Hotel.value:
            name = st.text_input("Hotel Name", value="dummy")
            address = st.text_input("Address", value="dummy")
            check_in_date = st.date_input("Check-in Date")
            check_in_time = st.time_input("Check-in Time", step=300)
            check_out_date = st.date_input("Check-out Date")
            check_out_time = st.time_input("Check-out Time", step=300)
            notes = st.text_area("Notes", key="hotel_notes")
            cost = st.number_input("Cost", min_value=0.0)

            if st.button("Add Hotel", use_container_width=True):
                hotel=Hotel(
                    trip_id=trip_id,
                    name=name,
                    address=address,
                    start_date=str(check_in_date),
                    start_time=check_in_time,
                    end_date=str(check_out_date),
                    end_time=check_out_time,
                    notes=notes,
                    cost=cost
                )
                
                st.toast(f"Hotel added: {hotel.name}", icon="✅")
                api_utils.insert(hotel)
                utils.clear_cache()
                st.rerun()

        elif itinerary_type == ItineraryType.Car.value:
            rental_company = st.selectbox("Rental Company", options=[c.value for c in CarRentalCompany])
            pickup_location = st.text_input("Pick-up Location")
            pickup_date = st.date_input("Pick-up Date")
            pickup_time = st.time_input("Pick-up Time", step=300)
            dropoff_location = st.text_input("Drop-off Location")
            dropoff_date = st.date_input("Drop-off Date")
            dropoff_time = st.time_input("Drop-off Time", step=300)
            cost = st.number_input("Cost", min_value=0.0)
            notes = st.text_area("Notes", key="car_notes")

            if st.button("Add Car", use_container_width=True):
                car=Car(
                    trip_id=trip_id,
                    rental_company=rental_company,
                    pickup_location=pickup_location,
                    start_date=str(pickup_date),
                    start_time=pickup_time,
                    dropoff_location=dropoff_location,
                    end_date=str(dropoff_date),
                    end_time=dropoff_time,
                    cost=cost,
                    notes=notes
                )
            
                st.toast(f"Car added: {car.pickup_location} to {car.dropoff_location}", icon="✅")
                api_utils.insert(car)
                utils.clear_cache()
                st.rerun()

        elif itinerary_type == ItineraryType.Activity.value:
            name = st.text_input("Activity Name")
            location = st.text_input("Location")
            date = st.date_input("Date")
            time = st.time_input("Time", step=300)
            description = st.text_area("Description")
            cost = st.number_input("Cost", min_value=0.0)

            if st.button("Add Activity", use_container_width=True):
                activity=Activity(
                        trip_id=trip_id,
                        name=name,
                        start_date=str(date),
                        start_time=time,
                        location=location,
                        description=description,
                        cost=cost
                )
                    
                st.toast(f"Activity added: {activity.start_date} @ {activity.location}", icon="✅")
                api_utils.insert(activity)
                utils.clear_cache()
                st.rerun()

def add_trip():
    with st.popover("Add a Trip", use_container_width=True):
        name = st.text_input("Trip Name")
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        notes = st.text_area("Notes")

        if st.button("Add Trip", use_container_width=True):
            trip = Trip(name=name, start_date=start_date, end_date=end_date, notes=notes)
            st.toast(f"Trip added: {trip.name}", icon="✅")
            
            api_utils.insert(trip)
            utils.clear_cache()
            st.rerun()