import requests

API_KEY = "d95597e0-5fa3-49a7-b591-b2191eba2df4"

def get_air_quality(city, state, country):
    url = "https://api.airvisual.com/v2/city"
    params = {
        'city': city,
        'state': state,
        'country': country,
        'key': 'd95597e0-5fa3-49a7-b591-b2191eba2df4'
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()['data']
        aqi_us = data['current']['pollution']['aqius']
        main_pollutant = data['current']['pollution']['mainus']
        return {
            'city': city,
            'state': state,
            'country': country,
            'aqi_us': aqi_us,
            'main_pollutant': main_pollutant
        }
    else:
        return {'error': 'Could not retrieve AQI data. Check location or API key.'}
