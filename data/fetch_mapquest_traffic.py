import requests
import json

MAPQUEST_API_KEY = "j3qC3EMgJxcXjapO1jqczfeQYuHVdPAm"

def get_city_coordinates(city):
   
    base_url = "http://www.mapquestapi.com/geocoding/v1/address"
    params = {
        "key": MAPQUEST_API_KEY,
        "location": city,
        "outFormat": "json"
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        if data and data.get('results') and data['results'][0].get('locations'):
            location = data['results'][0]['locations'][0]['latLng']
            return location.get('lat'), location.get('lng')
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching coordinates: {e}")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON response for coordinates.")
        return None

def get_mapquest_traffic_incidents(bounding_box, incident_types=None):
     
    base_url = "https://www.mapquestapi.com/traffic/v2/incidents"
    params = {
        "key": MAPQUEST_API_KEY,
        "boundingBox": bounding_box,
        "outFormat": "json"
    }
    if incident_types:
        params["filters"] = ",".join(incident_types)

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching MapQuest traffic data: {e}"}
    except json.JSONDecodeError:
        return {"error": "Error decoding JSON response."}


