import requests

API_KEY = "d95597e0-5fa3-49a7-b591-b2191eba2df4"

def get_air_quality(city, state, country):
    url = 'http://api.airvisual.com/v2/city'
    params = {
        "city": city,
        "state": state,
        "country": country,
        "key": "d95597e0-5fa3-49a7-b591-b2191eba2df4"
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code != 200 or "data" not in data:
            return {"error": data.get("message", "Unable to fetch air quality.")}

        pollution = data["data"]["current"]["pollution"]
        return {
            "city": city,
            "state": state,
            "country": country,
            "aqi_us": pollution["aqius"],
            "main_pollutant": pollution["mainus"]
            
        }

    except Exception as e:
        return {"error": str(e)}
