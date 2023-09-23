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
    food = [(w, v, val, min(val/w if w != 0 else float('inf'), val/v if v != 0 else float('inf'))) for w, v, val in food]

    # Sort by minimum value density
    food.sort(key=lambda item: item[3], reverse=True)

    total_value = 0
    for i in range(len(food)):
        w, v, val, _ = food[i]
        if w <= max_weight and v <= max_vol:
            # Take the whole item
            max_weight -= w
            max_vol -= v
            total_value += val
        else:
            # Consider taking a fraction of this item and the rest of the next item
            for j in range(i+1, len(food)):
                next_w, next_v, next_val, _ = food[j]
                if next_w < max_weight and next_v < max_vol:
                    fraction = min(max_weight/w, max_vol/v)
                    total_value += val * fraction
                    max_weight -= w * fraction
                    max_vol -= v * fraction
                    break

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