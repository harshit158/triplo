import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Triplo",
    page_icon="✈️",
    layout="wide"
)

pg = st.navigation(["pages/Dashboard.py",
                   "pages/Trips.py"])

pg.run()