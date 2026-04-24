import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import plotly.express as px
import requests
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.data_loader import load_master

st.set_page_config(page_title="Spatial Analysis", layout="wide")
st.header("Spatial Analysis")

with st.spinner("Loading data..."):
    df = load_master()

with st.sidebar:
    st.header("Filters")
    borough_options = sorted(df["ARREST_BORO"].dropna().unique().tolist())
    boroughs = st.multiselect("Borough", borough_options, default=borough_options)

filtered = df[df["ARREST_BORO"].isin(boroughs)]

GEOJSON_URLS = [
    "https://data.cityofnewyork.us/resource/kmep-waad.geojson?$limit=200",
    "https://raw.githubusercontent.com/ResidentMario/geoplot-data/master/nyc-police-precincts.geojson",
]

@st.cache_data(ttl=86400, show_spinner=False)
def fetch_geojson():
    for url in GEOJSON_URLS:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                data = r.json()
                if "features" in data and len(data["features"]) > 0:
                    return data
        except Exception:
            continue
    return None

tab1, tab2, tab3 = st.tabs(["Precinct Choropleth", "Arrest Heatmap", "Precinct Bar Chart"])

with tab1:
    geo = fetch_geojson()

    precinct_counts = (
        filtered.groupby("ARREST_PRECINCT").size()
        .reset_index(name="arrests")
    )
    precinct_counts["ARREST_PRECINCT"] = precinct_counts["ARREST_PRECINCT"].astype(int)

    if geo is None:
        st.warning("Could not load GeoJSON. Showing bar chart instead.")
        fig = px.bar(
            precinct_counts.sort_values("arrests", ascending=False),
            x="ARREST_PRECINCT", y="arrests",
            title="Arrests by Precinct",
            color="arrests", color_continuous_scale="YlOrRd"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        # ── Inspect what keys and value types the GeoJSON actually has ──
        sample_props = geo["features"][0]["properties"]
        st.caption("GeoJSON properties found: " + str(list(sample_props.keys())))

        # Find the precinct key
        precinct_key = None
        for key in ["Precinct", "precinct", "PRECINCT", "pct", "PCT", "police_precinct"]:
            if key in sample_props:
                precinct_key = key
                break

        if precinct_key is None:
            st.error("No precinct key found in GeoJSON. Falling back to bar chart.")
            fig = px.bar(
                precinct_counts.sort_values("arrests", ascending=False),
                x="ARREST_PRECINCT", y="arrests",
                title="Arrests by Precinct",
                color="arrests", color_continuous_scale="YlOrRd"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            # Normalize GeoJSON precinct values to int to match our data
            for feature in geo["features"]:
                try:
                    feature["properties"][precinct_key] = int(feature["properties"][precinct_key])
                except (ValueError, TypeError):
                    pass

            # Use Plotly choropleth_mapbox — handles key matching much more reliably than folium
            fig = px.choropleth_mapbox(
                precinct_counts,
                geojson=geo,
                locations="ARREST_PRECINCT",
                featureidkey="properties." + precinct_key,
                color="arrests",
                color_continuous_scale="YlOrRd",
                mapbox_style="carto-darkmatter",
                zoom=10,
                center={"lat": 40.73, "lon": -73.94},
                opacity=0.7,
                labels={"arrests": "Arrest Count", "ARREST_PRECINCT": "Precinct"},
                title="Arrests by Precinct"
            )
            fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0}, height=600)
            st.plotly_chart(fig, use_container_width=True)

with tab2:
    df_geo = filtered.dropna(subset=["Latitude", "Longitude"])
    df_geo = df_geo[
        df_geo["Latitude"].between(40.45, 40.95) &
        df_geo["Longitude"].between(-74.30, -73.65)
    ]
    sample = df_geo[["Latitude", "Longitude"]].sample(
        min(10000, len(df_geo)), random_state=42
    )
    m2 = folium.Map(location=[40.73, -73.94], zoom_start=11, tiles="CartoDB dark_matter")
    HeatMap(sample.values.tolist(), radius=8, blur=10).add_to(m2)
    st_folium(m2, width=None, height=600, use_container_width=True)

with tab3:
    precinct_counts2 = (
        filtered.groupby(["ARREST_PRECINCT", "ARREST_BORO"]).size()
        .reset_index(name="arrests")
        .sort_values("arrests", ascending=False)
    )
    fig3 = px.bar(
        precinct_counts2,
        x="ARREST_PRECINCT",
        y="arrests",
        color="ARREST_BORO",
        title="Arrests by Precinct colored by Borough",
        labels={
            "ARREST_PRECINCT": "Precinct",
            "arrests": "Arrest Count",
            "ARREST_BORO": "Borough"
        }
    )
    fig3.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig3, use_container_width=True)
