import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.data_loader import load_bubble_data, load_heatmap_matrix

st.set_page_config(page_title="NLP Topics", layout="wide")
st.header("🧠 NLP — Offense Topic Analysis")

tab1, tab2 = st.tabs(["Topic Bubble Chart", "Topic × Borough Heatmap"])

with tab1:
    try:
        bubble_df = load_bubble_data()
        fig = px.scatter(
            bubble_df, x="umap_x", y="umap_y",
            size="arrest_count", color="dominant_boro",
            hover_name="topic_name",
            hover_data={"top_keywords": True, "arrest_count": True,
                        "umap_x": False, "umap_y": False},
            size_max=60,
            title="Offense Topic Clusters — Size = Arrest Volume, Color = Dominant Borough",
            template="plotly_white"
        )
        fig.update_layout(
            xaxis=dict(showticklabels=False, title=""),
            yaxis=dict(showticklabels=False, title=""),
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)
    except FileNotFoundError:
        st.warning("topic_bubble_data.parquet not found. Run the notebook first and commit the file.")

with tab2:
    try:
        heatmap_pct = load_heatmap_matrix()
        top_topics = heatmap_pct.sum(axis=0).nlargest(15).index
        heatmap_top = heatmap_pct[top_topics]

        fig2, ax = plt.subplots(figsize=(16, 5))
        sns.heatmap(heatmap_top, annot=True, fmt=".1f",
                    cmap="YlOrRd", linewidths=0.4,
                    linecolor="white",
                    cbar_kws={"label": "% of Borough Arrests"}, ax=ax)
        ax.set_title("Topic Mix Across NYC Boroughs (Top 15 Topics)", fontsize=13)
        ax.tick_params(axis="x", rotation=40, labelsize=8)
        plt.tight_layout()
        st.pyplot(fig2)
    except FileNotFoundError:
        st.warning("topic_heatmap_matrix.parquet not found. Run the notebook first and commit the file.")
