import streamlit as st
import plotly.express as px
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.data_loader import load_master

st.set_page_config(page_title="EDA", layout="wide")
st.header("📊 Exploratory Analysis")

with st.spinner("Loading data..."):
    df = load_master()

# Sidebar filters
with st.sidebar:
    st.header("Filters")
    boroughs = st.multiselect(
        "Borough", sorted(df["ARREST_BORO"].dropna().unique()),
        default=sorted(df["ARREST_BORO"].dropna().unique())
    )
    severity = st.multiselect(
        "Severity", sorted(df["LAW_CAT_CD"].dropna().unique()),
        default=sorted(df["LAW_CAT_CD"].dropna().unique())
    )

filtered = df[df["ARREST_BORO"].isin(boroughs) & df["LAW_CAT_CD"].isin(severity)]
st.caption(f"Showing {len(filtered):,} arrests")

# Row 1
col1, col2 = st.columns(2)

with col1:
    fig = px.bar(
        filtered["ARREST_BORO"].value_counts().reset_index(),
        x="ARREST_BORO", y="count",
        title="Arrests by Borough", color="ARREST_BORO"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig2 = px.pie(
        filtered["LAW_CAT_CD"].value_counts().reset_index(),
        names="LAW_CAT_CD", values="count",
        title="Offense Severity Breakdown"
    )
    st.plotly_chart(fig2, use_container_width=True)

# Row 2 — Monthly trend
monthly = filtered.groupby(["year","month"]).size().reset_index(name="count")
fig3 = px.line(monthly, x="month", y="count", color="year",
               title="Monthly Arrest Trend", markers=True)
st.plotly_chart(fig3, use_container_width=True)

# Row 3
col3, col4 = st.columns(2)

with col3:
    top10 = filtered["OFNS_DESC"].value_counts().head(10).reset_index()
    fig4 = px.bar(top10, x="count", y="OFNS_DESC", orientation="h",
                  title="Top 10 Offense Categories")
    fig4.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig4, use_container_width=True)

with col4:
    weekday_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    wd = filtered["weekday"].value_counts().reindex(weekday_order).reset_index()
    fig5 = px.bar(wd, x="weekday", y="count", title="Arrests by Day of Week")
    st.plotly_chart(fig5, use_container_width=True)

# Row 4 — Demographics
col5, col6 = st.columns(2)

with col5:
    fig6 = px.bar(
        filtered["PERP_RACE"].value_counts().reset_index(),
        x="count", y="PERP_RACE", orientation="h", title="Arrests by Race"
    )
    st.plotly_chart(fig6, use_container_width=True)

with col6:
    fig7 = px.bar(
        filtered["AGE_GROUP"].value_counts().reset_index(),
        x="AGE_GROUP", y="count", title="Arrests by Age Group"
    )
    st.plotly_chart(fig7, use_container_width=True)
