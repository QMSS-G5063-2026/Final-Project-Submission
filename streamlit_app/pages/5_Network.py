import streamlit as st
import streamlit.components.v1 as components
import os

st.set_page_config(page_title="Network Analysis", layout="wide")
st.header("🕸️ Network Analysis")

# Resolve path to repo root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

tab1, tab2 = st.tabs(["Precinct Similarity", "Offense Co-occurrence"])

with tab1:
    st.subheader("Precinct Similarity Network")
    st.caption("Nodes = precincts · Size = arrest volume · Color = Louvain community · Edge = cosine similarity ≥ 0.85")
    path1 = os.path.join(BASE_DIR, "streamlit_app", "precinct_similarity_network.html")
    if os.path.exists(path1):
        with open(path1, "r", encoding="utf-8") as f:
            components.html(f.read(), height=750, scrolling=True)
    else:
        st.warning(f"File not found at: {path1}")
        st.info("Upload precinct_similarity_network.html to the streamlit_app/ folder in your GitHub repo.")

with tab2:
    st.subheader("Offense Co-occurrence Network")
    st.caption("Nodes = offense types · Size = total arrests · Color = Louvain community · Edge = shared precincts ≥ 20")
    path2 = os.path.join(BASE_DIR, "streamlit_app", "offense_cooccurrence_network.html")
    if os.path.exists(path2):
        with open(path2, "r", encoding="utf-8") as f:
            components.html(f.read(), height=750, scrolling=True)
    else:
        st.warning(f"File not found at: {path2}")
        st.info("Upload offense_cooccurrence_network.html to the streamlit_app/ folder in your GitHub repo.")
