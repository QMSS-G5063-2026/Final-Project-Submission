import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.data_loader import load_master

st.set_page_config(page_title="Spatial Analysis", layout="wide")
st.header("🗺️ Spatial Analysis")

with st.spinner("Loading data..."):
    df = load_master()

# GeoJSON with your existing multi-fallback logic
GEOJSON_URLS = [
    "https://data.cityofnewyork.us/resource/kmep-waad.geojson?$limit=200",
    "https://raw.githubusercontent.com/ResidentMario/geoplot-data/master/nyc-police-precincts.geojson",
    "https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/arcgis/rest/services/NYC_Police_Precincts/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=geojson"
]

@st.cache_data(ttl=86400)
def fetch_geojson():
    for url in GEOJSON_URLS:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                return r.json()
        except Exception:
            continue
    return None

tab1, tab2 = st.tabs(["Precinct Choropleth", "Arrest Heatmap"])

with tab1:
    geo = fetch_geojson()
    precinct_counts = (
        df.groupby("ARREST_PRECINCT").size()
        .reset_index(name="arrests")
    )
    precinct_counts["ARREST_PRECINCT"] = precinct_counts["ARREST_PRECINCT"].astype(str)

    m = folium.Map(location=[40.73, -73.94], zoom_start=11,
                   tiles="CartoDB dark_matter")

    if geo:
        folium.Choropleth(
            geo_data=geo,
            data=precinct_counts,
            columns=["ARREST_PRECINCT", "arrests"],
            key_on="feature.properties.Precinct",
            fill_color="YlOrRd",
            fill_opacity=0.7,
            line_opacity=0.3,
            legend_name="Arrest Count by Precinct",
            nan_fill_color="transparent"
        ).add_to(m)
        st.success("GeoJSON loaded successfully")
    else:
        st.warning("Could not load precinct boundaries — showing point map only")

    st_folium(m, width=None, height=600, use_container_width=True)

with tab2:
    from folium.plugins import HeatMap

    df_geo = df.dropna(subset=["LATITUDE", "LONGITUDE"])
    df_geo = df_geo[
        df_geo["LATITUDE"].between(40.45, 40.95) &
        df_geo["LONGITUDE"].between(-74.30, -73.65)
    ]

    # Sample for performance (10k points is plenty for a heatmap)
    sample = df_geo[["LATITUDE","LONGITUDE"]].sample(
        min(10000, len(df_geo)), random_state=42
    )

    m2 = folium.Map(location=[40.73, -73.94], zoom_start=11,
                    tiles="CartoDB dark_matter")
    HeatMap(sample.values.tolist(), radius=8, blur=10).add_to(m2)
    st_folium(m2, width=None, height=600, use_container_width=True)
