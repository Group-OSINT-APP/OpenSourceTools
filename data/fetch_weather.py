import requests

API_KEY = "10fee22e6167a302338f108e07d44951" 

def get_weather(city_name):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city_name,
        'appid': "10fee22e6167a302338f108e07d44951",
        'units': 'metric'
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        weather_info = {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed']
        }
        return weather_info
    else:
        return {'error': f"City '{city_name}' not found or API limit reached."}
