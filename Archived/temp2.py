import os
import subprocess
import time
import keyboard
from SimConnect import SimConnect, AircraftRequests, AircraftEvents
from SimConnect.Attributes import SimConnectDll, SIMCONNECT_DATA_INITPOSITION
import ctypes


sm = SimConnect()
smdll = SimConnectDll(r"C:\MSFS SDK\SimConnect SDK\lib\SimConnect.dll")
def spawn_player():
    # Spawn the player at 5000 feet above Atlanta Hartsfield-Jackson
    # Connect to the simulator
    
    aq = AircraftRequests(sm, _time=1000)
    ae = AircraftEvents(sm)
    
    # Set the altitude and location
    aq.set("PLANE_ALTITUDE", 5000)
    aq.set("PLANE_PITCH_DEGREES", 0)
    aq.set("PLANE_HEADING_DEGREES_TRUE", 0)
    aq.set("AIRSPEED_INDICATED", 100)
    aq.set("PLANE_BANK_DEGREES", 0)
    aq.set("PLANE_LATITUDE", 33.6367)  # Latitude for KATL
    aq.set("PLANE_LONGITUDE", -84.4281)  # Longitude for KATL
    half_throttle_event = ae.find("THROTTLE_50")
    half_throttle_event()
    center_airler_rudder_event=ae.find("CENTER_AILER_RUDDER")
    center_airler_rudder_event()
    pause_event = ae.find("PAUSE_ON")
    pause_event()

    # Confirm the spawn command
    spawn_command = "Player spawned at 5000 feet above Atlanta Hartsfield-Jackson"

    # Spawn the player
    # This is a placeholder for the actual implementation
    print("Spawning player at 5000 feet above Atlanta Hartsfield-Jackson...")
    print(spawn_command)
    return aq, ae

def call_logger(altitude):
    # Call the logger.py script
    logger_script = os.path.join(os.path.dirname(__file__), 'logger.py')
    subprocess.run(['python', logger_script, str(altitude)])

def unpause_game(ae):
    unpause_event = ae.find("PAUSE_OFF")
    unpause_event()
    print("Game unpaused")

def spawn_landmarks():
    latitude = 33.6697  # 2 miles north of KATL
    longitude = -84.4277
    altitude = 50.0  # Altitude in feet
    # Define the landmark position (2 miles north of KATL)
    rqst=sm.create_request()
    # Create an AI SimObject (Replace with a valid object name)
    landmark_object = sm.createSimulatedObject("Mountain of JACK", latitude, longitude, rqst)

    print("Landmark placed 2 miles north of KATL")
def spawn_aircraft(sm,aq):
    aircraft_type = "DA62 Asobo"
    flight_plan = "KATL to KPDK"
    altitude = 6000  # in feet
    departure="KATL"
    destination="KPDK"
    tail_number="N12345"
    flight_plan_path=os.path.join(os.path.dirname(__file__), 'fltplans', 'KATL-KPDK')
    aircraft_type_c = ctypes.c_char_p(aircraft_type.encode('utf-8'))
    tail_number_c = ctypes.c_char_p(tail_number.encode('utf-8'))
    departure_c = ctypes.c_char_p(departure.encode('utf-8'))
    destination_c = ctypes.c_char_p(destination.encode('utf-8'))
    flight_plan_c = ctypes.c_char_p(flight_plan_path.encode('utf-8'))
    # Create an instance of SIMCONNECT_DATA_INITPOSITION
    init_pos = SIMCONNECT_DATA_INITPOSITION()
    init_pos.Latitude = 33.6367
    init_pos.Longitude = -84.4281
    init_pos.Altitude = altitude
    init_pos.Pitch = 0.0
    init_pos.Bank = 0.0
    init_pos.Heading = 0.0
    init_pos.OnGround = 0
    init_pos.Airspeed = 140
    sm_handle=sm.hSimConnect.value
    # Create a new AI aircraft
    request_id = 1
    # Create a new AI aircraft
    ai_aircraft = smdll.AICreateNonATCAircraft(sm_handle, aircraft_type_c, tail_number_c, init_pos, request_id)
    print("AI aircraft created")
    # Wait for the aircraft to be created
    time.sleep(1)

    # Set the flight plan for the AI aircraft
    smdll.AISetAircraftFlightPlan(sm_handle, ai_aircraft, flight_plan_c,2)

if __name__ == "__main__":
    aq, ae = spawn_player()
    spawn_aircraft(sm,aq)
    #spawn_landmarks()
    time_counter=0
    while True:
        #checks if it has been 5 seconds, if so logs altitude
        if time_counter==50:
            altitude = aq.get('PLANE_ALTITUDE')
            call_logger(altitude)
            time_counter=0
        if keyboard.is_pressed('/'):
            unpause_game(ae)
        if keyboard.is_pressed('['):
            print("Ending script")
            quit()
        time.sleep(.1)
        time_counter+=1
        
#setup visual for flags, look into ai aircraft controlling with waypoints, see whether you can dynamicall change the flight plan of ai aircraft, test out capture the flag demo, and documentation 