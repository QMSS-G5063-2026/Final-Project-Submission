import streamlit as st
import pandas as pd
import pickle
import os

# Resolve path relative to repo root, works both locally and on Streamlit Cloud
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@st.cache_data
def load_master():
    path = os.path.join(BASE_DIR, "master_cleaned.parquet")
    return pd.read_parquet(path)

@st.cache_data
def load_bubble_data():
    path = os.path.join(BASE_DIR, "topic_bubble_data.parquet")
    return pd.read_parquet(path)

@st.cache_data
def load_heatmap_matrix():
    path = os.path.join(BASE_DIR, "topic_heatmap_matrix.parquet")
    return pd.read_parquet(path)

@st.cache_resource
def load_precinct_graph():
    path = os.path.join(BASE_DIR, "precinct_graph.pkl")
    with open(path, "rb") as f:
        return pickle.load(f)

@st.cache_resource
def load_offense_graph():
    path = os.path.join(BASE_DIR, "offense_cooc_graph.pkl")
    with open(path, "rb") as f:
        return pickle.load(f)
