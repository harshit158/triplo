# Ref: https://developers.google.com/maps/documentation/embed/embedding-map

import streamlit as st
import urllib.parse
import streamlit.components.v1 as components
import os

def display_map(dates_and_itineraries: dict):
    places = []
    for date, display_funcs_and_itineraries in dates_and_itineraries.items():
        for display_func, itinerary, time in display_funcs_and_itineraries:
            if hasattr(itinerary, 'address'):
                places.append(itinerary.address)
            elif hasattr(itinerary, 'location'):
                places.append(itinerary.location)
    
    if places:
        origin, destination = urllib.parse.quote_plus(places[0]), urllib.parse.quote_plus(places[-1])
        print(origin, "=>", destination)
        waypoints = places[1:-1]
        google_maps_url = (
                    f"https://www.google.com/maps/embed/v1/directions"
                    f"?key={os.environ.get('GOOGLE_MAPS_API_KEY')}"
                    f"&origin={origin}"
                    f"&destination={destination}"
                    f"&waypoints={'|'.join(waypoints)}"
                )
                            
        components.iframe(google_maps_url, height=560, width=900)
    
    else:
        st.write("No places found")