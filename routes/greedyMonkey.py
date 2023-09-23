import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)



def MonkeBrain(inputDict):
    max_weight = inputDict["w"]
    max_vol = inputDict["v"]
    food = inputDict["f"]

    # Compute the value densities for each item
    food_weight_based = [(w, v, val, val/w if w != 0 else float('inf')) for w, v, val in food]
    food_vol_based = [(w, v, val, val/v if v != 0 else float('inf')) for w, v, val in food]

    # Sort by value density
    food_weight_based.sort(key=lambda item: item[3], reverse=True)
    food_vol_based.sort(key=lambda item: item[3], reverse=True)

    total_value_weight_based = 0
    for w, v, val, _ in food_weight_based:
        if w <= max_weight and v <= max_vol:
            max_weight -= w
            max_vol -= v
            total_value_weight_based += val

    max_weight = inputDict["w"]  # reset max_weight
    max_vol = inputDict["v"]  # reset max_vol

    total_value_vol_based = 0
    for w, v, val, _ in food_vol_based:
        if w <= max_weight and v <= max_vol:
            max_weight -= w
            max_vol -= v
            total_value_vol_based += val

    return max(total_value_weight_based, total_value_vol_based)


@app.route('/greedymonkey', methods=['POST'])
def greedyMonkey():

# Debugging Purpose
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    input_value = data
    result = MonkeBrain(input_value)
    logging.info("My result :{}".format(result))

    return json.dumps(result)