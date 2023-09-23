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

    # Initialize variables to keep track of the best solution
    best_value = 0
    best_weight = 0
    best_vol = 0

    for _ in range(2):  # Run the loop twice, once for each strategy
        curr_weight = max_weight
        curr_vol = max_vol
        curr_value = 0
        food = food_weight_based if _ == 0 else food_vol_based  # Choose the strategy based on the iteration
        
        for w, v, val, _ in food:
            if w <= curr_weight and v <= curr_vol:
                curr_weight -= w
                curr_vol -= v
                curr_value += val

        if curr_value > best_value:  # If the current solution is better, update the best solution
            best_value = curr_value
            best_weight = curr_weight
            best_vol = curr_vol

    return best_value

@app.route('/greedymonkey', methods=['POST'])
def greedyMonkey():

# Debugging Purpose
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    input_value = data
    result = MonkeBrain(input_value)
    logging.info("My result :{}".format(result))

    return json.dumps(result)