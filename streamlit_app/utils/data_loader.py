import streamlit as st
import pandas as pd
import pickle
import os

# Repo root = two levels up from this file (utils/ → streamlit_app/ → repo root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@st.cache_data
def load_master():
    path = os.path.join(BASE_DIR, "streamlit_app", "master_cleaned.parquet")
    return pd.read_parquet(path)

@st.cache_data
def load_bubble_data():
    path = os.path.join(BASE_DIR, "streamlit_app", "topic_bubble_data.parquet")
    return pd.read_parquet(path)

@st.cache_data
def load_heatmap_matrix():
    path = os.path.join(BASE_DIR, "streamlit_app", "topic_heatmap_matrix.parquet")
    return pd.read_parquet(path)

@st.cache_resource
def load_precinct_graph():
    path = os.path.join(BASE_DIR, "streamlit_app", "precinct_graph.pkl")
    with open(path, "rb") as f:
        return pickle.load(f)

@st.cache_resource
def load_offense_graph():
    path = os.path.join(BASE_DIR, "streamlit_app", "offense_cooc_graph.pkl")
    with open(path, "rb") as f:
        return pickle.load(f)
