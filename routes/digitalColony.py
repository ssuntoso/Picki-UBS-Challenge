import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)

from collections import deque

def calculate_new_digit(num1, num2, weight):
    signature = (num1 - num2) % 10
    new_digit = (weight + signature) % 10
    return new_digit

def get_final_weight(data):
    result = []
    for inputdata in data:
        generations = inputdata["generations"]
        colony = list(map(int, inputdata["colony"]))
        colony_len = len(colony)
        for _ in range(generations):
            new_colony = []
            weight = sum(colony)
            for i in range(colony_len - 1):
                new_digit = calculate_new_digit(colony[i], colony[i+1], weight)
                new_colony.append(colony[i])
                new_colony.append(new_digit)
            new_colony.append(colony[-1])
            colony = new_colony
            colony_len = len(colony)
        result.append(str(sum(colony)))
    return result

@app.route('/digital-colony', methods=['POST'])
def digitalColony():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = get_final_weight(data)
    logging.info("My result :{}".format(result))
    return json.dumps(result)