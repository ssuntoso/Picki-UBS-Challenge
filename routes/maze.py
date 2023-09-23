import json
import logging

from flask import request

from routes import app

from random import shuffle

logger = logging.getLogger(__name__)

# def show_map(map):
#     for m in map:
#         print("We're always in the middle")
#         print(m)

def move(request_payload):
    map = request_payload["nearby"]
    
    # check surrounding
    up = map[0][1]
    down = map[2][1]
    right = map[1][2]
    left = map[1][0]
    
    path = []
    if up != 0:
        path.append("up")
    elif down != 0:
        path.append("down")
    elif right != 0:
        path.append("right")
    elif left != 0:
        path.append("left")
        
    # if len(path) > 1:
    #     shuffle(path)
        
    return [path[0]]
    
        
action_index = 0

@app.route('/maze', methods=['POST'])
def maze():
    global action_index
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    
    # answer
    global move_storage
    global map
    move_storage = []
    if action_index == 0:
        map = data["nearby"]
    else:
        if move_storage[-1] == "up":
            additional_map = data["nearby"][0]
            map[0].append(additional_map)
        elif move_storage[-1] == "down":
            additional_map = data["nearby"][-1]
            map.append(additional_map)
        elif move_storage[-1] == "right":
            map.append(data["nearby"][0][-1])
            map.append(data["nearby"][1][-1])
            map.append(data["nearby"][2][-1])
        elif move_storage[-1] == "left":
            map.append(data["nearby"][0][0])
            map.append(data["nearby"][1][0])
            map.append(data["nearby"][2][0])
        
    # check surrounding
    up = map[0][1]
    down = map[2][1]
    right = map[1][2]
    left = map[1][0]
    
    move_storage = []
    if up != 0:
        move_storage.append("up")
    elif down != 0:
        move_storage.append("down")
    elif right != 0:
        move_storage.append("right")
    elif left != 0:
        move_storage.append("left")
        
    result = [move_storage[0]]
    
    print("\n"+"moves: "+str(move_storage))
    print("\n"+"map: "+str(map))
    
    
    
    
    logging.info("My result :{}".format(result))
    
    if action_index >= len(result):
        action_index = 0 # reset for next /maze request

    action = result[action_index]
    action_index += 1

    return json.dumps({"playerAction": action})
