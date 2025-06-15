import streamlit as st

def clear_cache():
    st.cache_data.clear()
    st.cache_resource.clear()
    
def sort_itineraries(dates: dict):
    # sort dates
    dates = dict(sorted(dates.items()))
    
    for date, display_funcs_and_itineraries in dates.items():
        display_funcs_and_itineraries.sort(key=lambda x: x[2])
    
    return dates