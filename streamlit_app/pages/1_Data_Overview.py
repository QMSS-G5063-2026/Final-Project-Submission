import streamlit as st
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.data_loader import load_master

st.set_page_config(page_title="Data Overview", layout="wide")
st.header("📋 Dataset Overview")

with st.spinner("Loading data..."):
    df = load_master()

col1, col2, col3 = st.columns(3)
col1.metric("Total Arrests", f"{len(df):,}")
col2.metric("Columns", df.shape[1])
col3.metric("Boroughs", df["ARREST_BORO"].nunique())

st.subheader("Sample Records")
st.dataframe(df.head(100), use_container_width=True)

st.subheader("Missing Values")
missing = df.isna().sum().sort_values(ascending=False)
missing = missing[missing > 0].reset_index()
missing.columns = ["Column", "Missing Count"]
st.dataframe(missing, use_container_width=True)

st.subheader("Summary Statistics")
st.dataframe(df.describe().T, use_container_width=True)
