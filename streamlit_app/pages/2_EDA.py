import streamlit as st
import plotly.express as px
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.data_loader import load_master

st.set_page_config(page_title="EDA", layout="wide")
st.header("Exploratory Analysis")

with st.spinner("Loading data..."):
    df = load_master()

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
st.caption("Showing " + str(len(filtered)) + " arrests")

# Row 1
col1, col2 = st.columns(2)

with col1:
    fig1 = px.bar(
        filtered["ARREST_BORO"].value_counts().reset_index(),
        x="ARREST_BORO", y="count",
        title="Arrests by Borough", color="ARREST_BORO"
    )
    st.plotly_chart(fig1, use_container_width=True, key="boro_bar")

with col2:
    fig2 = px.pie(
        filtered["LAW_CAT_CD"].value_counts().reset_index(),
        names="LAW_CAT_CD", values="count",
        title="Offense Severity Breakdown"
    )
    st.plotly_chart(fig2, use_container_width=True, key="severity_pie")

# Row 2 — Monthly trend
if "YEAR" in filtered.columns and "MONTH" in filtered.columns:
    monthly = filtered.groupby(["YEAR", "MONTH"]).size().reset_index(name="count")
    fig3 = px.line(
        monthly, x="MONTH", y="count", color="YEAR",
        title="Monthly Arrest Trend", markers=True,
        labels={"MONTH": "Month", "count": "Arrests", "YEAR": "Year"}
    )
    st.plotly_chart(fig3, use_container_width=True, key="monthly_trend")

# Row 3
col3, col4 = st.columns(2)

with col3:
    top10 = filtered["OFNS_DESC"].value_counts().head(10).reset_index()
    fig4 = px.bar(
        top10, x="count", y="OFNS_DESC", orientation="h",
        title="Top 10 Offense Categories"
    )
    fig4.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig4, use_container_width=True, key="top10_offenses")

with col4:
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    if "WEEKDAY" in filtered.columns:
        wd = (
            filtered["WEEKDAY"].value_counts()
            .reindex(weekday_order)
            .reset_index()
        )
        wd.columns = ["WEEKDAY", "count"]
        fig5 = px.bar(wd, x="WEEKDAY", y="count", title="Arrests by Day of Week")
        st.plotly_chart(fig5, use_container_width=True, key="weekday_bar")

# Row 4 — Demographics
col5, col6 = st.columns(2)

with col5:
    fig6 = px.bar(
        filtered["PERP_RACE"].value_counts().reset_index(),
        x="count", y="PERP_RACE", orientation="h",
        title="Arrests by Race"
    )
    st.plotly_chart(fig6, use_container_width=True, key="race_bar")

with col6:
    if "AGE_GROUP" in filtered.columns:
        fig7 = px.bar(
            filtered["AGE_GROUP"].value_counts().reset_index(),
            x="AGE_GROUP", y="count",
            title="Arrests by Age Group"
        )
        st.plotly_chart(fig7, use_container_width=True, key="age_bar")
