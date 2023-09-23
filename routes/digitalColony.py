import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)

from collections import deque

def get_next_generation(colony, weight):
    next_gen = [0]*10
    for i in range(9, -1, -1):
        if i < 9:
            next_gen[i] += next_gen[i+1]
        if colony[i] > 0:
            next_gen[(i-weight)%10] += colony[i]
            if i > 0:
                next_gen[(i-1)%10] += colony[i]
    return next_gen, sum(i * count for i,count in enumerate(next_gen))

def get_final_weight(data):
    result = []
    for inputdata in data:
        generations = inputdata["generations"]
        colony = [0]*10
        for digit in map(int, list(inputdata["colony"])):
            colony[digit] += 1
        weight = sum(i * count for i,count in enumerate(colony))
        for _ in range(generations):
            colony, weight = get_next_generation(colony, weight)
        result.append(str(weight))
    return result
@app.route('/digital-colony', methods=['POST'])
def digitalColony():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = get_final_weight(data)
    logging.info("My result :{}".format(result))
    return json.dumps(result)