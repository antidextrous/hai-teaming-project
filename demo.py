import os
import subprocess
import time
import keyboard
from SimConnect import SimConnect, AircraftRequests, AircraftEvents
from SimConnect.Attributes import SimConnectDll, SIMCONNECT_DATA_INITPOSITION
import ctypes
import math

sm = SimConnect()
smdll = SimConnectDll(r"C:\MSFS SDK\SimConnect SDK\lib\SimConnect.dll")
aq = AircraftRequests(sm, _time=1000)
ae = AircraftEvents(sm)

def spawn_player():
    # Set the altitude and location, and pause the sim
    aq.set("PLANE_ALTITUDE", 5000)
    aq.set("PLANE_PITCH_DEGREES", 0)
    aq.set("PLANE_HEADING_DEGREES_TRUE", 0)
    aq.set("AIRSPEED_INDICATED", 100)
    aq.set("PLANE_BANK_DEGREES", 0)
    aq.set("PLANE_LATITUDE", 33.5367)  # Latitude for KATL
    aq.set("PLANE_LONGITUDE", -84.4281)  # Longitude for KATL
    half_throttle_event = ae.find("THROTTLE_50")
    half_throttle_event()
    center_airler_rudder_event=ae.find("CENTER_AILER_RUDDER")
    center_airler_rudder_event()
    pause_event = ae.find("PAUSE_ON")
    pause_event()
    print("Player spawned at 5000 feet above Atlanta Hartsfield-Jackson")
    return

def call_logger(altitude):
    # Call the logger.py script
    logger_script = os.path.join(os.path.dirname(__file__), 'logger.py')
    subprocess.run(['python', logger_script, str(altitude)])

def unpause_game(ae):
    unpause_event = ae.find("PAUSE_OFF")
    unpause_event()
    print("Game unpaused")

def spawn_landmarks():
    # Create a point of interest 2 miles south of KATL
    poi_latitude = 33.5367 - (2 / 69)  # Approximate conversion from miles to degrees latitude
    poi_longitude = -84.4281

    # Create a landmark at the point of interest
    landmark_name = "POI_South_of_KATL"
    landmark_type = "Windsock"  # Example landmark type, you can change it to any valid type
    

    # Use SimConnect to create the landmark
    smdll.AICreateSimulatedObject(sm.hSimConnect, landmark_type.encode('utf-8'), poi_latitude, poi_longitude, 0, 0, 0, 0, 0, 0, 0)
    print(f"Landmark '{landmark_name}' placed 2 miles south of KATL")

def spawn_agent():
    global aircraft_id
    aircraft_type = "DA62 Asobo"
    altitude = 5000
    tail_number="N12345"
    flight_plan_path=os.path.join(os.path.dirname(__file__), 'fltplans', 'KATL-KPDK')
    flight_plan_path2=os.path.join(os.path.dirname(__file__), 'fltplans', 'KPDK-KJAX')
    aircraft_type_c = ctypes.c_char_p(aircraft_type.encode('utf-8'))
    tail_number_c = ctypes.c_char_p(tail_number.encode('utf-8'))
    flight_plan_c = ctypes.c_char_p(flight_plan_path.encode('utf-8'))
    flight_plan_c2 = ctypes.c_char_p(flight_plan_path.encode('utf-8'))
    
    # Create an instance of SIMCONNECT_DATA_INITPOSITION
    init_pos = SIMCONNECT_DATA_INITPOSITION()
    init_pos.Latitude = 33.5363
    init_pos.Longitude = -84.4281
    init_pos.Altitude = altitude
    init_pos.Pitch = 0.0
    init_pos.Bank = 0.0
    init_pos.Heading = 0.0
    init_pos.OnGround = 0
    init_pos.Airspeed = 140
    sm_handle=sm.hSimConnect
    request_id = 1
    ai_aircraft = smdll.AICreateNonATCAircraft(sm_handle, aircraft_type_c, tail_number_c, init_pos, request_id)
    print("AI aircraft created")
    # Wait for the aircraft to be created
    time.sleep(1)
    
    # Set the flight plan for the AI aircraft
    smdll.AISetAircraftFlightPlan(sm_handle, 1, flight_plan_c,2)
    time.sleep(10)
    smdll.AISetAircraftFlightPlan(sm_handle, 1, flight_plan_c2,2)
    
def atFlag(lat, lon):
    # Coordinates for KATL
    katl_lat = 33.6367
    katl_lon = -84.4281

    # Calculate the distance using the Haversine formula
    radius = 3959  # Radius of the Earth in miles

    dlat = math.radians(lat - katl_lat)
    dlon = math.radians(lon - katl_lon)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(katl_lat)) * math.cos(math.radians(lat)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = radius * c

    return distance <= 2
if __name__ == "__main__":
    spawn_player()
    spawn_agent()
    
    time_counter=0
    while True:
        #checks if it has been 5 seconds, if so logs altitude
        if time_counter==50:
            altitude = aq.get('PLANE_ALTITUDE')
            call_logger(altitude)
            time_counter=0
        player_lat = aq.get('PLANE_LATITUDE')
        player_lon = aq.get('PLANE_LONGITUDE')
        if atFlag(player_lat, player_lon):
            print("Player wins")
            break
        if keyboard.is_pressed('/'):
            unpause_game(ae)
        if keyboard.is_pressed('['):
            print("Ending script")
            quit()
        time.sleep(.1)
        time_counter+=1
        
#setup visual for flags, look into ai aircraft controlling with waypoints, see whether you can dynamically change the flight plan of ai aircraft, and documentation
#do same thing in xplane and compile rl projects from github, with a focus on exploring different ways of controlling an ai aircraft (like spawning as an npc with waypoints, or heading speed altitude, are there open source full controllers)