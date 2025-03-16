from SimConnect import *
import time
import math

# Flag location (set to a real-world coordinate)
FLAG_LAT = 37.7749  # Example: San Francisco
FLAG_LON = -122.4194

# Base locations (set for each team)
TEAM1_BASE_LAT = 37.6213  # Example: SFO Airport
TEAM1_BASE_LON = -122.3790
TEAM2_BASE_LAT = 34.0522  # Example: LAX Airport
TEAM2_BASE_LON = -118.2437

# Flag status
flag_holder = None  # Holds player ID who has the flag

def haversine(lat1, lon1, lat2, lon2):
    """Calculate distance (km) between two lat/lon points."""
    R = 6371  # Radius of the Earth in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c * 1000  # Convert to meters

# Connect to SimConnect
sm = SimConnect()
aq = AircraftRequests(sm, _time=2000)  # 2-second interval

print("Capture the Flag script started!")

while True:
    try:
        player_id = aq.get("ATC ID")  # Get player identifier
        player_lat = aq.get("PLANE LATITUDE")
        player_lon = aq.get("PLANE LONGITUDE")

        # Check if player is near the flag and no one has it
        if flag_holder is None and haversine(player_lat, player_lon, FLAG_LAT, FLAG_LON) < 50:
            flag_holder = player_id
            print(f"Flag captured by {player_id}!")

        # Check if flag holder reaches their base
        if flag_holder == player_id:
            if haversine(player_lat, player_lon, TEAM1_BASE_LAT, TEAM1_BASE_LON) < 100:
                print(f"Team 1 scores! {player_id} returned the flag!")
                flag_holder = None  # Reset flag
            elif haversine(player_lat, player_lon, TEAM2_BASE_LAT, TEAM2_BASE_LON) < 100:
                print(f"Team 2 scores! {player_id} returned the flag!")
                flag_holder = None  # Reset flag

        time.sleep(1)  # Check every second
    except Exception as e:
        print("Error:", e)
        break