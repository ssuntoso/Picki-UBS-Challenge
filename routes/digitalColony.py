import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)

def get_next_colony(colony, weight):
    if len(colony) == 1:
        return colony

    num1, num2 = colony[0], colony[1]
    sign = (num1 - num2) % 10
    new_digit = (weight + sign) % 10

    return [num1, new_digit] + get_next_colony(colony[1:], weight)

def get_final_weight(data):
    result = []
    for inputdata in data:
        generations = inputdata["generations"]
        colony = list(map(int, list(inputdata["colony"])))
        colony_sum = sum(colony)
        
        for _ in range(generations):
            colony = get_next_colony(colony, colony_sum)
            colony_sum = sum(colony)
        
        result.append(str(colony_sum))
    return result

@app.route('/digital-colony', methods=['POST'])
def digitalColony():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = getFinalWeight(data)
    logging.info("My result :{}".format(result))
    return json.dumps(result)