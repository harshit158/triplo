import streamlit as st

def clear_cache():
    st.cache_data.clear()
    st.cache_resource.clear()