import streamlit as st
import requests

# ----------------------------
# Your OpenWeatherMap API key
API_KEY = "0ba3bd48af491574a377b9bafe76aec0"
# ----------------------------

st.set_page_config(page_title="🌦️ Weather App", page_icon="🌤️", layout="centered")
st.markdown("<h1 style='text-align: center;'>🌤️ Weather App</h1>", unsafe_allow_html=True)
st.markdown("---")

# Input box
city = st.text_input("Enter City Name", "")

# Validate city name
def is_valid_city(name):
    return name.replace(" ", "").isalpha()

# Map OpenWeatherMap icon codes to emojis
ICON_MAP = {
    "01d": "☀️", "01n": "🌙",
    "02d": "⛅", "02n": "🌙☁️",
    "03d": "☁️", "03n": "☁️",
    "04d": "☁️", "04n": "☁️",
    "09d": "🌧️", "09n": "🌧️",
    "10d": "🌦️", "10n": "🌦️",
    "11d": "⛈️", "11n": "⛈️",
    "13d": "❄️", "13n": "❄️",
    "50d": "🌫️", "50n": "🌫️"
}

if st.button("Get Weather"):
    if not city:
        st.warning("Please enter a city name.")
    elif not is_valid_city(city):
        st.warning("City name should contain letters only, no numbers or symbols!")
    else:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        try:
            response = requests.get(url, timeout=10)
            data = response.json()

            if response.status_code == 200:
                weather = data["weather"][0]
                main = data["main"]
                icon = ICON_MAP.get(weather["icon"], "🌤️")
                
                st.markdown(f"<h2 style='text-align: center;'>{icon} Weather in {data['name']} {icon}</h2>", unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                col1.metric("🌡 Temperature", f"{main['temp']} °C")
                col2.metric("💧 Humidity", f"{main['humidity']} %")
                col3.metric("🌬 Condition", weather["description"].title())
                
                st.markdown("---")

            elif response.status_code == 401:
                st.error("Invalid API key. Please check your key.")
            else:
                st.error(data.get("message", "City not found. Please try again."))

        except requests.exceptions.RequestException:
            st.error("Unable to connect to the weather service. Check your internet.")
