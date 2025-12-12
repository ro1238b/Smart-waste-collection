import streamlit as st
import pandas as pd
from db import fetch_data
from logic import detect_overflow_bins, sort_bins, prepare_route_points
from routeoptimize import get_optimized_route

from streamlit_folium import st_folium
import folium

st.set_page_config(page_title="Smart Waste Route Dashboard", layout="wide")

st.title("🚛 Smart Waste Collection – Driver View")
st.write("Live optimized route with bin details, waste type & fill percentage.")

# ---------------------------
# Load live data from MongoDB
# ---------------------------
df = pd.DataFrame(fetch_data())
if df.empty:
    st.error("No bin data available!")
    st.stop()

# ---------------------------
# Urgent bins
# ---------------------------
urgent = detect_overflow_bins(df.to_dict("records"), threshold=60)
urgent = sort_bins(urgent)[:50]

urgent_df = pd.DataFrame(urgent)

st.subheader("🔥 Urgent Bins (Sorted)")
st.dataframe(urgent_df[["bin_id", "fill_level_percent", "waste_type", "timestamp"]])

# ---------------------------
# Route optimization
# ---------------------------
points = prepare_route_points(urgent)
route, total_distance = get_optimized_route(points)

route_df = pd.DataFrame(route, columns=["bin_id", "lat", "lon"])

st.success(f"Optimized Route Distance: **{round(total_distance, 2)} km**")

# ---------------------------
#  REALISTIC MAP WITH FOLIUM
# ---------------------------

st.subheader("🗺 Realistic Route Map for Driver")

# Center map on first bin
start_lat, start_lon = route[0][1], route[0][2]
m = folium.Map(location=[start_lat, start_lon], zoom_start=13)

# Draw route polyline
polyline_points = [(r[1], r[2]) for r in route]
folium.PolyLine(polyline_points, weight=6, color="blue").add_to(m)

# Add markers
for idx, row in route_df.iterrows():
    bin_id = row["bin_id"]
    lat = row["lat"]
    lon = row["lon"]

    bin_info = urgent_df[urgent_df["bin_id"] == bin_id].iloc[0]

    fill_level = bin_info["fill_level_percent"]
    waste_type = bin_info["waste_type"]

    # Popup HTML card
    popup_html = f"""
    <div style="width:200px">
        <h4>🗑 {bin_id}</h4>
        <b>Fill Level:</b> {fill_level}%<br>
        <b>Waste Type:</b> {waste_type}<br><br>
        <img src="https://cdn-icons-png.flaticon.com/512/679/679922.png"
             width="60">
    </div>
    """

    folium.Marker(
        location=(lat, lon),
        tooltip=f"{idx+1}. {bin_id}",
        popup=popup_html,
        icon=folium.Icon(color="green", icon="info-sign")
    ).add_to(m)

# Display map
st_folium(m, width=1200, height=650)



