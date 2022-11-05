import json
import sys
import datetime
import uuid

time = datetime.datetime.now().astimezone().strftime('%Y-%m-%dT%H:%M:%S%z')

if __name__ == "__main__":
    with open(sys.argv[2], 'r') as config_file:
        config  = json.load(config_file)
        message = sys.argv[1]
        print(json.dumps({
            'time'    : time,
            'message' : message,
            'id'      : str(uuid.uuid4()),
            'config'  : config
        }))
