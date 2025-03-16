from SimConnect import *
from ctypes import POINTER, cast

def handle_assigned_object_id(received_data, sky_connect):
    object_data = cast(received_data, POINTER(SIMCONNECT_RECV_ASSIGNED_OBJECT_ID)).contents
    request_id = object_data.dwRequestID
    it = sky_connect.pending_ai_aircraft_creation_requests.pop(request_id, None)
    
    if it is not None:
        aircraft = it
        aircraft.set_simulation_object_id(object_data.dwObjectID)
        # Continue with the rest of your logic