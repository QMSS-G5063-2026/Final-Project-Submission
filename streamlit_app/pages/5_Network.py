import streamlit as st
import streamlit.components.v1 as components
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

st.set_page_config(page_title="Network Analysis", layout="wide")
st.header("🕸️ Network Analysis")

tab1, tab2 = st.tabs(["Precinct Similarity", "Offense Co-occurrence"])

with tab1:
    st.subheader("Precinct Similarity Network")
    st.caption("Nodes = precincts · Size = arrest volume · Color = Louvain community · Edge = cosine similarity ≥ 0.85")
    try:
        with open("streamlit_app/precinct_similarity_network.html", "r", encoding="utf-8") as f:
            html = f.read()
        components.html(html, height=750, scrolling=True)
    except FileNotFoundError:
        st.warning("precinct_similarity_network.html not found. Run the notebook and commit the file.")

with tab2:
    st.subheader("Offense Co-occurrence Network")
    st.caption("Nodes = offense types · Size = total arrests · Color = Louvain community · Edge = shared precincts ≥ 20")
    try:
        with open("streamlit_app/offense_cooccurrence_network.html", "r", encoding="utf-8") as f:
            html = f.read()
        components.html(html, height=750, scrolling=True)
    except FileNotFoundError:
        st.warning("offense_cooccurrence_network.html not found. Run the notebook and commit the file.")
