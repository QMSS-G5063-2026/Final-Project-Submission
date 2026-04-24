import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import plotly.express as px
import requests
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.data_loader import load_master

st.set_page_config(page_title="Spatial Analysis", layout="wide")
st.header("🗺️ Spatial Analysis")

with st.spinner("Loading data..."):
    df = load_master()

# ── Sidebar filters ───────────────────────────────────────────────────
with st.sidebar:
    st.header("Filters")
    boroughs = st.multiselect(
        "Borough", sorted(df["ARREST_BORO"].dropna().unique()),
        default=sorted(df["ARREST_BORO"].dropna().unique())
    )
filtered = df[df["ARREST_BORO"].isin(boroughs)]

# ── GeoJSON fetch (best-effort, no crash if it fails) ─────────────────
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
                # Validate it has features
                if "features" in data and len(data["features"]) > 0:
                    return data
        except Exception:
            continue
    return None

tab1, tab2, tab3 = st.tabs(["Precinct Choropleth", "Arrest Heatmap", "Precinct Bar Chart"])

# ── Tab 1: Choropleth ─────────────────────────────────────────────────
with tab1:
    geo = fetch_geojson()

    precinct_counts = (
        filtered.groupby("ARREST_PRECINCT").size()
        .reset_index(name="arrests")
    )
    precinct_counts["ARREST_PRECINCT"] = precinct_counts["ARREST_PRECINCT"].astype(str)

    if geo is None:
        st.warning("Could not load precinct GeoJSON boundaries. Showing Plotly choropleth instead.")
        fig = px.bar(
            precinct_counts.sort_values("arrests", ascending=False),
            x="ARREST_PRECINCT", y="arrests",
            title="Arrests by Precinct",
            labels={"ARREST_PRECINCT": "Precinct", "arrests": "Arrest Count"},
            color="arrests", color_continuous_scale="YlOrRd"
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    else:
        # Find the correct property key for precinct number
        sample_props = geo["features"][0]["properties"]
        st.caption(f"GeoJSON feature properties: {list(sample_props.keys())}")

        # Try common key names
        precinct_key = None
        for key in ["Precinct", "precinct", "PRECINCT", "pct", "PCT"]:
            if key in sample_props:
                precinct_key = key
                break

        if precinct_key is None:
            st.warning(f"Could not find precinct key in GeoJSON. Properties found: {list(sample_props.keys())}")
            fig = px.bar(
                precinct_counts.sort_values("arrests", ascending=False),
                x="ARREST_PRECINCT", y="arrests",
                title="Arrests by Precinct",
                color="arrests", color_continuous_scale="YlOrRd"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            m = folium.Map(location=[40.73, -73.94], zoom_start=11,
                           tiles="CartoDB dark_matter")
            folium.Choropleth(
                geo_data=geo,
                data=precinct_counts,
                columns=["ARREST_PRECINCT", "arrests"],
                key_on=f"feature.properties.{precinct_key}",
                fill_color="YlOrRd",
                fill_opacity=0.7,
                line_opacity=0.3,
                legend_name="Arrest Count by Precinct",
                nan_fill_color="transparent",
                nan_fill_opacity=0.1
            ).add_to(m)
            st_folium(m, width=None, height=600, use_container_width=True)

# ── Tab 2: Heatmap ────────────────────────────────────────────────────
with tab2:
    df_geo = filtered.dropna(subset=["Latitude", "Longitude"])
    df_geo = df_geo[
        df_geo["Latitude"].between(40.45, 40.95) &
        df_geo["Longitude"].between(-74.30, -73.65)
    ]

    sample = df_geo[["Latitude", "Longitude"]].sample(
        min(10000, len(df_geo)), random_state=42
    )

    m2 = folium.Map(location=[40.73, -73.94], zoom_start=11,
                    tiles="CartoDB dark_matter")
    HeatMap(sample.values.tolist(), radius=8, blur=10).add_to(m2)
    st_folium(m2, width=None, height=600, use_container_width=True)

# ── Tab 3: Precinct Bar Chart (always works, no GeoJSON needed) ───────
with tab3:
    precinct_counts2 = (
        filtered.groupb
