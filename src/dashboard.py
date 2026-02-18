import streamlit as st
import pandas as pd
import requests


# Islands data
coords = {
    "Biscoe": {"lat": -65.4333, "lon": -65.5000},
    "Dream": {"lat": -64.7333, "lon": -64.2333},
    "Torgersen": {"lat": -64.7667, "lon": -64.0833},
}


# Cached method to fetch historical weather data (for demonstration, the free API has limited range and info)
@st.cache_data
def fetch_historical():
    url = "https://archive-api.open-meteo.com/v1/archive?latitude=-64.77&longitude=-64.05&start_date=2023-01-01&end_date=2023-01-31&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m,surface_pressure"
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    return None


# Map
st.title("Infographic Dashboard")
st.markdown("""
This page shows the usage of various more _obscure_ Streamlit components, such as maps. Also, it demonstrates how
to fetch live data using https requests and display it in the app. In this case, live data from meteo station 
at Palmer Station, Antarctica is fetched and displayed.
""")
island = st.selectbox("Select an island:", list(coords.keys()))
map_data = pd.DataFrame(
    [
        {
            "lat": coords[island]["lat"],
            "lon": coords[island]["lon"],
            "color": "#0000FF",
        },
        {"lat": -64.7742, "lon": -64.0531, "color": "#FF0000"},
    ]
)
st.map(map_data, zoom=7, color="color")
st.markdown("""
🔵 **Selected Island** &nbsp;&nbsp;&nbsp; 🔴 **Palmer Station**
""")

# Usings requests to fetch live weather data (some displayed values are hardcoded, as this is free API with limited
# data and info)
url = "https://api.open-meteo.com/v1/forecast?latitude=-64.7667&longitude=-64.0833&current_weather=true"
st.subheader("Current Weather at Palmer Station")
try:
    response = requests.get(url).json()
    temp = response["current_weather"]["temperature"]
    wind = response["current_weather"]["windspeed"]
    wind_dir = response["current_weather"]["winddirection"]
    day = response["current_weather"]["is_day"]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Current Temperature", f"{temp} °C", delta="-2 °C")
        st.metric("Humidity", "80%", delta="+3%")
    with c2:
        st.metric("Wind Speed", f"{wind} km/h", delta="+5 km/h")
        st.metric("Wind Direction", f"{wind_dir}°", delta="No change")
    with c3:
        st.metric("Day/Night", "Day" if day == 1 else "Night")
        st.metric("Visibility", "10 km", delta="-2 km")
    with c4:
        st.metric("Pressure", "1015 hPa", delta="+5 hPa")
        st.metric("Weather Condition", "Cloudy")
except Exception as e:
    st.error("Failed to fetch weather data. Please try again later.")

# Using requests to fetch historical weather data
st.subheader("Historical Weather at Palmer Station")
data = fetch_historical()
if data:
    df_hist = pd.DataFrame(
        {
            "Time": pd.to_datetime(data["hourly"]["time"]),
            "Temperature (°C)": data["hourly"]["temperature_2m"],
            "Humidity (%)": data["hourly"]["relative_humidity_2m"],
            "Wind Speed (km/h)": data["hourly"]["wind_speed_10m"],
            "Pressure (hPa)": data["hourly"]["surface_pressure"],
        }
    ).set_index("Time")

    c1, c2 = st.columns(2)
    with c1:
        st.line_chart(
            df_hist["Temperature (°C)"], x_label="Time", y_label="Temperature (°C)"
        )
        st.bar_chart(
            df_hist["Wind Speed (km/h)"], x_label="Time", y_label="Wind Speed (km/h)"
        )
    with c2:
        st.area_chart(df_hist["Humidity (%)"], x_label="Time", y_label="Humidity (%)")
        st.line_chart(
            df_hist["Pressure (hPa)"], x_label="Time", y_label="Pressure (hPa)"
        )
else:
    st.error("Error fetching historical data.")
