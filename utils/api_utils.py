import json
from utils import utils
import streamlit as st
from uuid import uuid4
from typing import Optional
from database import supabase

def insert(model) -> str:
    id = str(uuid4())
    model.id = id
    table_name = model.__class__.__name__.lower()
    supabase.table(table_name).insert([json.loads(model.model_dump_json())]).execute()
    return id

def fetch_trip(trip_id: int) -> dict:
    return supabase.table("trip").select("*").eq("id", trip_id).single().execute().data

@st.cache_data(ttl=1800)
def fetch_all(table: str, model, filter_field: Optional[str] = None, filter_value: Optional[str] = None) -> list:
    query = supabase.table(table).select("*")
    
    if filter_field and filter_value:
        query = query.eq(filter_field, filter_value)

    items = query.execute().data

    return [model(**item) for item in items]

def delete_itinerary(table: str, id: str):
    supabase.table(table).delete().eq("id", id).execute()
    st.toast(f"Item deleted", icon="✅")
    utils.clear_cache()