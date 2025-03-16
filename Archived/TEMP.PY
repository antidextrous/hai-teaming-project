import os
import subprocess
import time
import keyboard
from SimConnect import SimConnect, AircraftRequests, AircraftEvents

def spawn_player():
    # Spawn the player at 5000 feet above Atlanta Hartsfield-Jackson
    # Connect to the simulator
    sm = SimConnect()
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

if __name__ == "__main__":
    aq, ae = spawn_player()
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