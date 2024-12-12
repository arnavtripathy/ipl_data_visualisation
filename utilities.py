
import pandas as pd
def extract_id_and_city(data):
    if 'id' in data.columns and 'city' in data.columns:
        new_df = data[['id', 'city']].copy()  # Extract and create a new DataFrame
    else:
        raise ValueError("Columns 'id' and/or 'city' not found in the dataset.")
    
    id_city_df = new_df

    id_city_df = data[['id', 'city']].groupby('city').count().reset_index()
    id_city_df.rename(columns={'id': 'match_count'}, inplace=True)

    # Add coordinates for cities
    city_coords = {
        "Bangalore": {"lat": 12.9716, "lon": 77.5946},
        "Chandigarh": {"lat": 30.7333, "lon": 76.7794},
        "Delhi": {"lat": 28.6139, "lon": 77.2090},
        "Mumbai": {"lat": 19.0760, "lon": 72.8777},
        "Kolkata": {"lat": 22.5726, "lon": 88.3639},
        "Jaipur": {"lat": 26.9124, "lon": 75.7873},
        "Hyderabad": {"lat": 17.3850, "lon": 78.4867},
        "Chennai": {"lat": 13.0827, "lon": 80.2707},
        "Cape Town": {"lat": -33.9249, "lon": 18.4241},
        "Port Elizabeth": {"lat": -33.9608, "lon": 25.6022},
        "Durban": {"lat": -29.8587, "lon": 31.0218},
        "Centurion": {"lat": -25.8519, "lon": 28.1850},
        "East London": {"lat": -33.0153, "lon": 27.9116},
        "Johannesburg": {"lat": -26.2041, "lon": 28.0473},
        "Kimberley": {"lat": -28.7280, "lon": 24.7497},
        "Bloemfontein": {"lat": -29.0852, "lon": 26.1596},
        "Ahmedabad": {"lat": 23.0225, "lon": 72.5714},
        "Cuttack": {"lat": 20.4625, "lon": 85.8828},
        "Nagpur": {"lat": 21.1458, "lon": 79.0882},
        "Dharamsala": {"lat": 32.2190, "lon": 76.3234},
        "Kochi": {"lat": 9.9312, "lon": 76.2673},
        "Indore": {"lat": 22.7196, "lon": 75.8577},
        "Visakhapatnam": {"lat": 17.6868, "lon": 83.2185},
        "Pune": {"lat": 18.5204, "lon": 73.8567},
        "Raipur": {"lat": 21.2514, "lon": 81.6296},
        "Ranchi": {"lat": 23.3441, "lon": 85.3096},
        "Abu Dhabi": {"lat": 24.4539, "lon": 54.3773},
        "Rajkot": {"lat": 22.3039, "lon": 70.8022},
        "Kanpur": {"lat": 26.4499, "lon": 80.3319},
        "Bengaluru": {"lat": 12.9716, "lon": 77.5946},
        "Dubai": {"lat": 25.2760, "lon": 55.2962},
        "Sharjah": {"lat": 25.3463, "lon": 55.4209},
        "Navi Mumbai": {"lat": 19.0330, "lon": 73.0297},
        "Lucknow": {"lat": 26.8467, "lon": 80.9462},
        "Guwahati": {"lat": 26.1445, "lon": 91.7362},
        "Mohali": {"lat": 30.7046, "lon": 76.7179},
    }

    # Add latitude and longitude to the DataFrame
    id_city_df['lat'] = id_city_df['city'].map(lambda city: city_coords.get(city, {}).get('lat', None))
    id_city_df['lon'] = id_city_df['city'].map(lambda city: city_coords.get(city, {}).get('lon', None))
    return id_city_df.dropna(subset=['lat', 'lon'])    
