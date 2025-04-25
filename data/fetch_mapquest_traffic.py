
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

def get_mapquest_traffic_incidents(bounding_box):
 
    base_url = "https://www.mapquestapi.com/traffic/v2/incidents"
    params = {
        "key": MAPQUEST_API_KEY,
        "boundingBox": bounding_box,
        "outFormat": "json"
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching MapQuest traffic data: {e}"}
    except json.JSONDecodeError:
        return {"error": "Error decoding JSON response."}

if __name__ == '__main__':
    # Example usage for testing
    test_city = "Lombard, IL"
    coordinates = get_city_coordinates(test_city)
    if coordinates:
        lat, lng = coordinates
        # Define a bounding box (adjust the radius as needed)
        radius = 0.05  # Approximately 5-7 miles in latitude/longitude
        bbox = f"{lat - radius},{lng - radius},{lat + radius},{lng + radius}"
        traffic_data = get_mapquest_traffic_incidents(bbox)
        print(json.dumps(traffic_data, indent=4))
    else:
        print(f"Could not get coordinates for {test_city}")
