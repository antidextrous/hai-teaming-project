import os
import json
import time
import sys

def log_altitude(altitude):
    log_entry = {
        'timestamp': time.time(),
        'altitude': altitude
    }
    log_file_path = os.path.join(os.path.dirname(__file__), 'testdata', 'altitude_log.json')
    with open(log_file_path, 'a') as log_file:
        json.dump(log_entry, log_file)
        log_file.write('\n')
    

if __name__ == "__main__":
    altitude = float(sys.argv[1])
    log_altitude(altitude)

