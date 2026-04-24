import streamlit as st

st.set_page_config(
    page_title="Street-Level Stories: NYC Arrest Patterns",
    page_icon="🗽",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🗽 Street-Level Stories")
st.subheader("An Interactive Visual Analysis of NYC Arrest Patterns")

st.markdown("""
**Group:** Haoxuan Lu · Joey Zhu · Yijia Liu · Siyi Zhou  
**Course:** QMSS G5063 — Data Visualization, Spring 2026
""")

st.markdown("""
This dashboard explores NYPD arrest data across NYC's five boroughs,
combining geospatial maps, demographic breakdowns, NLP topic modeling,
and network analysis.

👈 **Use the sidebar to navigate between sections.**
""")

st.info("Data source: NYC Open Data — NYPD Arrest Data (Year to Date)")
