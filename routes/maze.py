import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)

def show_map(map):
    for m in map:
        print(m)

def transform_map(map):
    trans_map = []
    for m in map:
        trans_m = []
        for e in m:
            if e == 0:
                trans_e = 0
            elif e == 1:
                trans_e = "A"
            elif e == 2:
                trans_e = "B"
            elif e == 3:
                trans_e = "C"
            trans_m.append(trans_e)
        trans_map.append(trans_m)
    return trans_map

def locate_start(map):
    list_num = 0
    for m in map:
        if "B" in m or 2 in m:
            start = [list_num, m.index("B")]
        list_num += 1
        print(m)
    print(f"start: {start}")
    return start

def locate_end(map):
    list_num = 0
    for m in map:
        if "C" in m or 3 in m:
            end = [list_num, m.index("C")]
        list_num += 1
        print(m)
    print(f"start: {end}")
    return end

def transform_map_to_minesweeper(map):
    minesweeper_map = []
    list_num = 0
    for m in map:
        minesweeper_m = []
        c = 0
        for e in m:
            bomb = 0
            print(f"ELEMENT: {e}")
            if e == 0:
                up_index = list_num - 1
                down_index = list_num + 1
                
            else:
                
                # look right-left
                right_index = c + 1
                left_index = c - 1
                
                print("----------")
                print(m[right_index])
                if m[right_index] == 0:
                    print("right")
                    bomb += 1
                
                print("----------")
                print(m[left_index])
                if m[left_index] == 0:
                    print("left")
                    bomb += 1
                
                # look up down
                up_index = list_num - 1
                down_index = list_num + 1
                
                print("----------")
                print(map[up_index][c])
                if map[up_index][c] == 0:
                    print("up")
                    bomb += 1
                    
                print("----------")
                print(map[down_index][c])
                if map[down_index][c] == 0:
                    print("down")
                    bomb += 1
            
            
                    
            # update location marker
            minesweeper_m.append(bomb)
            
            print("==========================================")
            print("index_current_location: " + str(c))
            
            c += 1
            
        minesweeper_map.append(minesweeper_m)
        
        show_map(minesweeper_map)
        print("list_num: " + str(list_num))
        print("up index: " + str(up_index))
        print("down index: " + str(down_index))
        
        
        list_num += 1
    
    return minesweeper_map

def minesweeper_map_cleanup(map, start, end):
    row = 0
    for m in map:
        col = 0
        for e in m:
            coord = [row,col]
            print(e)
            print(coord)

            if (e == 3) and (coord != start) and (coord != end):
                print("redefine")
                row_to_change = map[row]
                row_to_change[col] = 0
                map[row] = row_to_change
                print(map[row])
            print("======================")
            col += 1
        row += 1
    
    return map

def walk(location_index, end, map, steps):
    if len(steps) >= 0:
        row = location_index[0]
        c = location_index[1]

        move = False
        print("Element: " + str(map[row][c]))
        
        # look right-left
        right_index = c + 1
        left_index = c - 1

        new_row = row
        new_col = c

        print("right: " + str(map[row][right_index]))
        if map[row][right_index] != 0 and [row, c+1] not in steps:
            print("right")
            control = ("right")
            move = True
            new_col = c + 1

        print("left: " + str(map[row][left_index]))
        if map[row][left_index] != 0 and [row, c-1] not in steps:
            print("left")
            control = ("left")
            move = True
            new_col = c - 1
        
        # look up down
        up_index = row - 1
        down_index = row + 1

        print("up: " + str(map[up_index][c]))
        if map[up_index][c] != 0 and [row-1, c] not in steps:
            print("up")
            control = ("up")
            move = True
            new_row = row - 1

        print("down: " + str(map[down_index][c]))
        if map[down_index][c] != 0  and [row+1, c] not in steps:
            print("down")
            control = ("down")
            move = True 
            new_row = row + 1
            
        # get new coord
        if move == True:
            location_index = [new_row, new_col]
            # steps.append(location_index)
            
        return location_index, control
                
    elif location_index == end:
        print("done")

def input_to_output(request_payload):
    map = request_payload['nearby']
    map = (transform_map(map))  
    start = locate_start(map) 
    try:
        end = locate_end(map)
    except:
        end = [0,0]
    
    for i in range(len(map) * len(map[0])):
        map = (transform_map_to_minesweeper(map))
        map = minesweeper_map_cleanup(map,start,end)
    
    steps = [start]
    controls = []
    location_index = start
    while True:
        if location_index != end:
            location_index, control = walk(location_index, end, map, steps)
            steps.append(location_index)
            controls.append(control)
            print(location_index)
        elif location_index == end:
            print("end")
            break
        print("-----------------------")
        # time.sleep(5)
    print(len(steps))
    print(steps)
    print(controls)

    return controls


# @app.route('/maze', methods=['POST'])
# def maze():
#     data = request.get_json()
#     logging.info("data sent for evaluation {}".format(data))
#     result = input_to_output(data)
#     logging.info("My result :{}".format(result))
#     return json.dumps(result)

action_index = 0

@app.route('/maze', methods=['POST'])
def maze():
    global action_index
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = input_to_output(data)
    logging.info("My result :{}".format(result))
    
    if action_index >= len(result):
        action_index = 0 # reset for next /maze request

    action = result[action_index]
    action_index += 1

    return json.dumps({"playerAction": action})
