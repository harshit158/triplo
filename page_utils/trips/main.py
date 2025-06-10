import streamlit as st
from page_utils.trips import trips as trips_utils

def display_participants():
    participants = st.session_state.get('participants', [])
    st.write(f"{' | '.join(participants)}")
        
    with st.popover("➕"):
        participants = st.session_state.get('participants', [])
        new_participant = st.text_input("Name", key=f'participants_{len(participants)}')
        if new_participant:
            participants.append(new_participant)
            st.session_state.participants = participants
            st.rerun()

def main():
    st.write("## Trips")
    trips_utils.add_trip()
    
    trips_utils.display_trips()

    st.divider()

    with st.columns(1, border=False)[0]:
        st.title("Yellowstone")
        with st.expander("Details"):
            st.write("Trips")