import streamlit as st
from collections import defaultdict
from database import supabase
from utils import api_utils
from models import ItineraryType, ItineraryItem, Flight, Hotel, Car, Activity, FlightLeg, Airport, Airline, Trip

def display_trip(trip: Trip):    
    hotels = api_utils.fetch_all("hotel", Hotel, filter_field="trip_id", filter_value=trip.id)
    dates = defaultdict(list)
    
    for hotel in hotels:
        dates[hotel.start_date].append(hotel.display_start)
        if hotel.end_date:
            dates[hotel.end_date].append(hotel.display_end)
    
    with st.columns(1, border=False)[0]:
        st.title(trip.name)
        st.write(f"{trip.start_date} -> {trip.end_date}")
        
        with st.expander("", expanded=True):
            cols = st.columns(2)
            
            with cols[0]:
                add_itinerary(trip.id)
                
                with st.container(height=500):
                    for date, display_funcs in dates.items():
                        st.markdown(f"<h5 style='text-align: left; padding: 0px; color: green;'>{date}</h5><br>", unsafe_allow_html=True)
                        for func in display_funcs:
                            st.markdown(f"<h6 style='text-align: left; background-color: #E8E8E8; padding: 0px;'>🛌 Accommodation</h6><br>", unsafe_allow_html=True)
                            func()
                            st.divider()
                        
                # with st.container(height=500):
                #     st.markdown("<h5 style='text-align: left; padding: 0px; color: green;'>Tuesday, September 5</h5><br>", unsafe_allow_html=True)
                #     st.markdown("<h6 style='text-align: left; background-color: #E8E8E8; padding: 0px;'>✈️ Flight</h6><br>", unsafe_allow_html=True)
                    
                #     st.markdown("[Open JetBlue App](jetblue://)", unsafe_allow_html=True)
                    
                #     st.markdown("<h6 style='text-align: left; background-color: #E8E8E8; padding: 0px;'>🛌 Accommodation</h6><br>", unsafe_allow_html=True)
                #     st.markdown("<a href='https://www.google.com/maps/place/Wyndham+Visalia/data=!4m2!3m1!1s0x0:0xe23a39812213a431?sa=X&ved=1t:2428&ictx=111'>Wyndham Visalia</a>", unsafe_allow_html=True)

                    
                #     st.divider()
                    
                #     st.markdown("<h5 style='text-align: left; padding: 0px; color: green;'>Tuesday, September 5</h5><br>", unsafe_allow_html=True)
                #     st.markdown("<h6 style='text-align: left; background-color: #E8E8E8; padding: 0px;'>✈️ Flight</h6><br>", unsafe_allow_html=True)
                #     st.markdown(":red[BOS: (23:11)] -> :green[SFO (20:00)]", unsafe_allow_html=True)
                #     st.markdown("<h6 style='text-align: left; background-color: #E8E8E8; padding: 0px;'>🛌 Accommodation</h6><br>", unsafe_allow_html=True)
                #     st.markdown("<a href='https://www.google.com/maps/place/Wyndham+Visalia/data=!4m2!3m1!1s0x0:0xe23a39812213a431?sa=X&ved=1t:2428&ictx=111'>Wyndham Visalia</a>", unsafe_allow_html=True)
                    
                #     st.divider()
                    
                #     st.markdown("<h5 style='text-align: left; padding: 0px; color: green;'>Tuesday, September 5</h5><br>", unsafe_allow_html=True)
                #     st.markdown("<h6 style='text-align: left; background-color: #E8E8E8; padding: 0px;'>✈️ Flight</h6><br>", unsafe_allow_html=True)
                #     st.markdown(":red[BOS: (23:11)] -> :green[SFO (20:00)]", unsafe_allow_html=True)
                #     st.markdown("<h6 style='text-align: left; background-color: #E8E8E8; padding: 0px;'>🛌 Accommodation</h6><br>", unsafe_allow_html=True)
                #     st.markdown("<a href='https://www.google.com/maps/place/Wyndham+Visalia/data=!4m2!3m1!1s0x0:0xe23a39812213a431?sa=X&ved=1t:2428&ictx=111'>Wyndham Visalia</a>", unsafe_allow_html=True)
                #     st.image("https://lh3.googleusercontent.com/p/AF1QipNxQ8tKwCEpvbSgjN0bmU5H0mIkUB0uGpgOZlDe=w408-h272-k-no", width=100)
            
            with cols[1]:
                st.map()
    
def display_trips():
    trips = api_utils.fetch_all("trip", Trip)
    for trip in trips:
        display_trip(trip)
    
def add_itinerary(trip_id: str):
    with st.popover("Add Itinerary", use_container_width=True):
        st.header("Add New Itinerary Item")

        itinerary_type = st.selectbox(
            "Select Itinerary Type",
            options=[t.value for t in ItineraryType]
        )

        # Initialize placeholders
        itinerary_item = None

        if itinerary_type == ItineraryType.Flight.value:
            origin = st.selectbox("Origin", options=[a.value for a in Airport])
            destination = st.selectbox("Destination", options=[a.value for a in Airport])
            airline = st.selectbox("Airline", options=["Select Airline"]+[a.value for a in Airline])
            confirmation = st.text_input("Confirmation Number")
            cost = st.number_input("Cost", min_value=0.0)
            notes = st.text_area("Notes", key="flight_notes")
            
            num_legs = st.selectbox("Number of Flight Legs", options=[1, 2, 3])
            legs = []
            for i in range(num_legs):
                st.subheader(f"Leg {i+1}")
                leg_origin = st.selectbox(f"Leg {i+1} Origin", options=[a.value for a in Airport], key=f'leg_origin_{i}')
                leg_departure_time = st.time_input(f"Leg {i+1} Departure Time", key=f'leg_dep_{i}', step=300)
                leg_destination = st.selectbox(f"Leg {i+1} Destination", options=[a.value for a in Airport], key=f'leg_dest_{i}')
                leg_arrival_time = st.time_input(f"Leg {i+1} Arrival Time", key=f'leg_arrival_{i}', step=300)
                legs.append(FlightLeg(origin=leg_origin, departure_time=leg_departure_time, destination=leg_destination, arrival_time=leg_arrival_time))

            if st.button("Add Flight", use_container_width=True):
                itinerary_item = ItineraryItem(
                    type=ItineraryType.Flight,
                    item=ItineraryFlight(
                        origin=origin,
                        airline=airline,
                        destination=destination,
                        confirmation=confirmation,
                        legs=legs,
                        cost=cost,
                        notes=notes
                    )
                )

        elif itinerary_type == ItineraryType.Hotel.value:
            name = st.text_input("Hotel Name", value="dummy")
            address = st.text_input("Address", value="dummy")
            maps_url = st.text_input("Google Maps URL", value="https://www.google.com/maps")
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
                    maps_url=maps_url,
                    start_date=str(check_in_date),
                    start_time=check_in_time,
                    end_date=str(check_out_date),
                    end_time=check_out_time,
                    notes=notes,
                    cost=cost
                )
                
                st.toast(f"Hotel added: {hotel.name}", icon="✅")
                api_utils.insert(hotel)

        elif itinerary_type == ItineraryType.Car.value:
            pick_up_location = st.text_input("Pick-up Location")
            pick_up_date = st.date_input("Pick-up Date")
            pick_up_time = st.time_input("Pick-up Time", step=300)
            drop_off_location = st.text_input("Drop-off Location")
            drop_off_date = st.date_input("Drop-off Date")
            drop_off_time = st.time_input("Drop-off Time", step=300)
            cost = st.number_input("Cost", min_value=0.0)
            notes = st.text_area("Notes", key="car_notes")

            if st.button("Add Car", use_container_width=True):
                itinerary_item = ItineraryItem(
                    type=ItineraryType.Car,
                    item=ItineraryCar(
                        pick_up_location=pick_up_location,
                        pick_up_date=str(pick_up_date),
                        pick_up_time=pick_up_time,
                        drop_off_location=drop_off_location,
                        drop_off_date=str(drop_off_date),
                        drop_off_time=drop_off_time,
                        cost=cost,
                        notes=notes
                    )
                )

        elif itinerary_type == ItineraryType.Activity.value:
            name = st.text_input("Activity Name")
            location = st.text_input("Location")
            description = st.text_area("Description")
            cost = st.number_input("Cost", min_value=0.0)

            if st.button("Add Activity", use_container_width=True):
                itinerary_item = ItineraryItem(
                    type=ItineraryType.Activity,
                    item=ItineraryActivity(
                        name=name,
                        location=location,
                        description=description,
                        cost=cost
                    )
                )

        # Save to session state if created
        if itinerary_item:
            if 'itinerary_list' not in st.session_state:
                st.session_state.itinerary_list = []
            st.session_state.itinerary_list.append(itinerary_item)
            st.toast(f"{itinerary_item.type.value} added to trip!")

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