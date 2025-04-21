import requests

API_KEY = "0nliiIgGihIG1OE3iOR6XoA0YbsKmt8X"

# Example: Chicago bounding box (lat1,lon1,lat2,lon2)
CITIES = {
    "Chicago": "41.6445,-87.9401,42.0230,-87.5237",
    "New York": "40.4774,-74.2591,40.9176,-73.7002",
    "Los Angeles": "33.7037,-118.6682,34.3373,-118.1553"
}

def get_traffic(city_name):
    if city_name not in CITIES:
        return {'error': "City not supported for traffic data."}
    
    bbox = CITIES[city_name]
    url = f"https://api.tomtom.com/traffic/services/5/incidentDetails"
    params = {
        'key': '0nliiIgGihIG1OE3iOR6XoA0YbsKmt8X',
        'bbox': bbox,
        'fields': 'id,geometry,properties',
        'language': 'en',
        'categoryFilter': 'Accident,Jam,Construction,Other'
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        incidents = data.get('incidents', [])
        parsed_incidents = []

        for inc in incidents[:5]:  
            props = inc['properties']
            parsed_incidents.append(f"{props['eventCode']}: {props.get('description', 'No description')}")

        return {
            'city': city_name,
            'count': len(incidents),
            'incidents': parsed_incidents
        }
    else:
        return {'error': 'Failed to fetch traffic data.'}
