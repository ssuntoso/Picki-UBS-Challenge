import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)



def MonkeBrain(inputDict):
    max_weight = inputDict["w"]
    max_vol = inputDict["v"]
    food = inputDict["f"]
    
    # Compute the value density for each item
    food = [(w, v, val, val/(w*v)) for w, v, val in food]
    
    # Sort by value density
    food.sort(key=lambda item: item[3], reverse=True)
    
    total_value = 0
    for w, v, val, _ in food:
        if w <= max_weight and v <= max_vol:
            max_weight -= w
            max_vol -= v
            total_value += val
    
    return total_value


@app.route('/greedymonkey', methods=['POST'])
def greedyMonkey():

# Debugging Purpose
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    input_value = data
    result = MonkeBrain(input_value)
    logging.info("My result :{}".format(result))

    return json.dumps(result)