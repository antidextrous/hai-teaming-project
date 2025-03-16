from SimConnect import SimConnect, AircraftRequests, AircraftEvents
from SimConnect.Attributes import SimConnectDll, SIMCONNECT_DATA_INITPOSITION
import time
import sys
import ctypes
import os
sm = SimConnect()
aq = AircraftRequests(sm, _time=2000)
smdll = SimConnectDll(r"C:\MSFS SDK\SimConnect SDK\lib\SimConnect.dll")
# Define the aircraft type and flight plan
def spawn_aircraft(sm):
    aircraft_type = "DA62 Asobo"
    altitude = 5000  # in feet
    departure="KATL"
    destination="KPDK"
    tail_number="N12345"
    flight_plan_path=os.path.join(os.path.dirname(__file__), 'fltplans', 'airmail')
    flight_plan_path2=os.path.join(os.path.dirname(__file__), 'fltplans', 'KPDK-JKAX')
    aircraft_type_c = ctypes.c_char_p(aircraft_type.encode('utf-8'))
    tail_number_c = ctypes.c_char_p(tail_number.encode('utf-8'))
    departure_c = ctypes.c_char_p(departure.encode('utf-8'))
    destination_c = ctypes.c_char_p(destination.encode('utf-8'))
    flight_plan_c = ctypes.c_char_p(flight_plan_path.encode('utf-8'))
    flight_plan_c2 = ctypes.c_char_p(flight_plan_path2.encode('utf-8'))
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
    sm_handle=sm.hSimConnect.value
    # Create a new AI aircraft
    request_id = 1  
    # Create a new AI aircraft
    ai_aircraft = smdll.AICreateNonATCAircraft(sm_handle, aircraft_type_c, tail_number_c, init_pos, request_id)

    # Wait for the aircraft to be created
    time.sleep(5)

    # Set the flight plan for the AI aircraft
    smdll.AISetAircraftFlightPlan(sm_handle, 1, flight_plan_c, request_id)
def change_heading(aq):
    
    while True:
        try:
            current_heading = aq.get("PLANE_HEADING_DEGREES_TRUE")
            new_heading = (current_heading + 1) % 360  # Increment heading by 1 degree and wrap around at 360
            aq.set("PLANE_HEADING_DEGREES_TRUE", new_heading,2)
            time.sleep(1)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    # Create a new instance of SimConnect
    

    # Spawn the aircraft
    spawn_aircraft(sm)

    # Start changing the heading
    change_heading(aq)

    # Monitor the aircraft
    while True:
        try:
            position = aq.get("PLANE_LATITUDE", "PLANE_LONGITUDE", "PLANE_ALTITUDE")
            print(f"Aircraft Position: {position}")
            time.sleep(10)
        except KeyboardInterrupt:
            break

    # Disconnect from the simulator
    sm.exit()