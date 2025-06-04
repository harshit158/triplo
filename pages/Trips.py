import streamlit as st

with st.popover("Add a Trip", use_container_width=True):
    st.text_input("Name")

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
    
with st.columns(1, border=False)[0]:
    st.title("Utah")
    # Add participants
    display_participants()
    
    with st.expander("Itinerary", expanded=True):
        cols = st.columns(2)
        
        with cols[0]:
            with st.container(height=500):
                st.markdown("<h5 style='text-align: left; padding: 0px; color: green;'>Tuesday, September 5</h5><br>", unsafe_allow_html=True)
                st.markdown("<h6 style='text-align: left; background-color: #E8E8E8; padding: 0px;'>✈️ Flight</h6><br>", unsafe_allow_html=True)
                
                st.markdown("[Open JetBlue App](jetblue://)", unsafe_allow_html=True)
                
                st.markdown("<h6 style='text-align: left; background-color: #E8E8E8; padding: 0px;'>🛌 Accommodation</h6><br>", unsafe_allow_html=True)
                st.markdown("<a href='https://www.google.com/maps/place/Wyndham+Visalia/data=!4m2!3m1!1s0x0:0xe23a39812213a431?sa=X&ved=1t:2428&ictx=111'>Wyndham Visalia</a>", unsafe_allow_html=True)

                
                st.divider()
                
                st.markdown("<h5 style='text-align: left; padding: 0px; color: green;'>Tuesday, September 5</h5><br>", unsafe_allow_html=True)
                st.markdown("<h6 style='text-align: left; background-color: #E8E8E8; padding: 0px;'>✈️ Flight</h6><br>", unsafe_allow_html=True)
                st.markdown(":red[BOS: (23:11)] -> :green[SFO (20:00)]", unsafe_allow_html=True)
                st.markdown("<h6 style='text-align: left; background-color: #E8E8E8; padding: 0px;'>🛌 Accommodation</h6><br>", unsafe_allow_html=True)
                st.markdown("<a href='https://www.google.com/maps/place/Wyndham+Visalia/data=!4m2!3m1!1s0x0:0xe23a39812213a431?sa=X&ved=1t:2428&ictx=111'>Wyndham Visalia</a>", unsafe_allow_html=True)
                
                st.divider()
                
                st.markdown("<h5 style='text-align: left; padding: 0px; color: green;'>Tuesday, September 5</h5><br>", unsafe_allow_html=True)
                st.markdown("<h6 style='text-align: left; background-color: #E8E8E8; padding: 0px;'>✈️ Flight</h6><br>", unsafe_allow_html=True)
                st.markdown(":red[BOS: (23:11)] -> :green[SFO (20:00)]", unsafe_allow_html=True)
                st.markdown("<h6 style='text-align: left; background-color: #E8E8E8; padding: 0px;'>🛌 Accommodation</h6><br>", unsafe_allow_html=True)
                st.markdown("<a href='https://www.google.com/maps/place/Wyndham+Visalia/data=!4m2!3m1!1s0x0:0xe23a39812213a431?sa=X&ved=1t:2428&ictx=111'>Wyndham Visalia</a>", unsafe_allow_html=True)
                st.image("https://lh3.googleusercontent.com/p/AF1QipNxQ8tKwCEpvbSgjN0bmU5H0mIkUB0uGpgOZlDe=w408-h272-k-no", width=100)
        
        with cols[1]:
            st.map()

st.divider()

with st.columns(1, border=False)[0]:
    st.title("Yellowstone")
    with st.expander("Details"):
        st.write("Trips")