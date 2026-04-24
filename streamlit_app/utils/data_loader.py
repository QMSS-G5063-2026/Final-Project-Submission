@st.cache_data
def load_bubble_data():
    path = os.path.join(BASE_DIR, "streamlit_app", "topic_bubble_data.parquet")
    return pd.read_parquet(path)

@st.cache_data
def load_heatmap_matrix():
    path = os.path.join(BASE_DIR, "streamlit_app", "topic_heatmap_matrix.parquet")
    return pd.read_parquet(path)
