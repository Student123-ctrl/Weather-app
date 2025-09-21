from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

# ✅ Your OpenWeatherMap API key
API_KEY = "0ba3bd48af491574a377b9bafe76aec0"

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>🌦️ Weather App</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(to right, #00c6ff, #0072ff);
            text-align: center;
            padding: 50px;
            color: white;
        }
        h1 { font-size: 40px; }
        form { margin: 20px; }
        input[type=text] {
            padding: 10px;
            width: 250px;
            border-radius: 5px;
            border: none;
            font-size: 16px;
        }
        input[type=submit] {
            padding: 10px 20px;
            border-radius: 5px;
            border: none;
            font-size: 16px;
            background: #ff9800;
            color: white;
            cursor: pointer;
        }
        .weather-box {
            margin-top: 30px;
            padding: 20px;
            background: rgba(0,0,0,0.3);
            border-radius: 10px;
            display: inline-block;
        }
        .error {
            margin-top: 20px;
            color: yellow;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h1>🌤️ Weather App</h1>
    <form method="POST" onsubmit="return validateCity()">
        <input type="text" name="city" placeholder="Enter city name" required pattern="[A-Za-z\\s]+" title="Please enter letters only">
        <input type="submit" value="Get Weather">
    </form>

    <script>
    function validateCity() {
        const cityInput = document.querySelector('input[name="city"]').value;
        const regex = /^[A-Za-z\\s]+$/;
        if (!regex.test(cityInput)) {
            alert("City name should contain letters only, no numbers or symbols!");
            return false; // prevent form submission
        }
        return true; // allow form submission
    }
    </script>
    
    {% if weather %}
    <div class="weather-box">
        <h2>{{ weather.city }}</h2>
        <p><b>Temperature:</b> {{ weather.temp }}°C</p>
        <p><b>Humidity:</b> {{ weather.humidity }}%</p>
        <p><b>Condition:</b> {{ weather.description }}</p>
    </div>
    {% elif error %}
    <div class="error">{{ error }}</div>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error = None
    if request.method == "POST":
        city = request.form["city"]
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if response.status_code == 200:
                weather = {
                    "city": data["name"],
                    "temp": data["main"]["temp"],
                    "humidity": data["main"]["humidity"],
                    "description": data["weather"][0]["description"].title()
                }
            elif response.status_code == 401:
                error = "Invalid API key. Please check your key."
            else:
                error = data.get("message", "City not found. Please try again.")
        
        except requests.exceptions.RequestException:
            error = "Unable to connect to the weather service. Check your internet."

    return render_template_string(HTML, weather=weather, error=error)

if __name__ == "__main__":
    app.run(debug=True)