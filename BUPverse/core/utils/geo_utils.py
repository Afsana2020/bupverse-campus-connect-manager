import openrouteservice
from django.conf import settings
import requests

client = openrouteservice.Client(key=settings.ORS_API_KEY)

def geocode_with_ors(address):
    full_address = f"{address}, Dhaka, Bangladesh"
    print(f"[DEBUG] Geocoding: {full_address}")

    try:
        ors_result = client.pelias_search(text=full_address)
        print("[DEBUG] ORS Raw Response:", ors_result)
        if ors_result['features']:
            props = ors_result['features'][0]['properties']
            coords = ors_result['features'][0]['geometry']['coordinates']
            confidence = props.get('confidence', 0)
            accuracy = props.get('accuracy', '')

            if confidence >= 0.8 and accuracy in ['point', 'building']:
                return coords[1], coords[0]
    except Exception as e:
        print("ORS error:", e)

    try:
        nominatim_url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": full_address,
            "format": "json",
            "limit": 1,
        }
        headers = {
            "User-Agent": "BUPverse/1.0 (afsanahena24@gmail.com)"
        }
        response = requests.get(nominatim_url, params=params, headers=headers)
        data = response.json()
        print("[DEBUG] Nominatim Raw Response:", data)
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
    except Exception as e:
        print("Nominatim error:", e)

    return None, None



def get_real_distance_km(coord1, coord2):
    if coord1 == coord2:
        return 0.0
    try:
        print(f"[DEBUG] Requesting SHORTEST route from {coord1} to {coord2}")
        routes = client.directions(
            coordinates=[(coord1[1], coord1[0]), (coord2[1], coord2[0])],
            profile='driving-car',
            preference='shortest',  
            format='geojson'
        )

        meters = routes['features'][0]['properties']['summary']['distance']
        distance_km = meters / 1000
        print(f"[DEBUG] Shortest Distance: {distance_km:.2f} km")
        return round(distance_km, 2)
    except Exception as e:
        print(f"[ERROR] Error calculating shortest path: {e}")
        return float('inf')
    
    
