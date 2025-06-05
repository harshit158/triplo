import streamlit as st
from models import ItineraryType, ItineraryItem, ItineraryFlight, ItineraryHotel, ItineraryCar, ItineraryActivity, FlightLeg, Airport, Airline

def add_itinerary():
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
            
            num_legs = st.selectbox("Number of Flight Legs", options=[1, 2, 3])
            legs = []
            for i in range(num_legs):
                st.subheader(f"Leg {i+1}")
                leg_origin = st.selectbox(f"Leg {i+1} Origin", options=[a.value for a in Airport], key=f'leg_origin_{i}')
                leg_departure_time = st.time_input(f"Leg {i+1} Departure Time", key=f'leg_dep_{i}', step=300)
                leg_destination = st.selectbox(f"Leg {i+1} Destination", options=[a.value for a in Airport], key=f'leg_dest_{i}')
                leg_arrival_time = st.time_input(f"Leg {i+1} Arrival Time", key=f'leg_arrival_{i}', step=300)
                legs.append(FlightLeg(leg_origin, leg_departure_time, leg_destination, leg_arrival_time))

            if st.button("Add Flight", use_container_width=True):
                itinerary_item = ItineraryItem(
                    type=ItineraryType.Flight,
                    item=ItineraryFlight(
                        origin=origin,
                        airline=airline,
                        destination=destination,
                        confirmation=confirmation,
                        legs=legs,
                        cost=cost
                    )
                )

        elif itinerary_type == ItineraryType.Hotel.value:
            name = st.text_input("Hotel Name")
            address = st.text_input("Address")
            maps_url = st.text_input("Google Maps URL")
            check_in_date = st.date_input("Check-in Date")
            check_in_time = st.time_input("Check-in Time", step=300)
            check_out_date = st.date_input("Check-out Date")
            check_out_time = st.time_input("Check-out Time", step=300)
            notes = st.text_area("Notes")
            cost = st.number_input("Cost", min_value=0.0)

            if st.button("Add Hotel", use_container_width=True):
                itinerary_item = ItineraryItem(
                    type=ItineraryType.Hotel,
                    item=ItineraryHotel(
                        name=name,
                        address=address,
                        maps_url=maps_url,
                        check_in_date=str(check_in_date),
                        check_in_time=check_in_time,
                        check_out_date=str(check_out_date),
                        check_out_time=check_out_time,
                        notes=notes,
                        cost=cost
                    )
                )

        elif itinerary_type == ItineraryType.Car.value:
            pick_up_location = st.text_input("Pick-up Location")
            pick_up_date = st.date_input("Pick-up Date")
            pick_up_time = st.time_input("Pick-up Time", step=300)
            drop_off_location = st.text_input("Drop-off Location")
            drop_off_date = st.date_input("Drop-off Date")
            drop_off_time = st.time_input("Drop-off Time", step=300)
            cost = st.number_input("Cost", min_value=0.0)

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
                        cost=cost
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
            st.success(f"{itinerary_item.type.value} added to trip!")