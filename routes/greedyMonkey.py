import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)



# def MonkeBrain(inputDict):
#     max_weight = inputDict["w"]
#     max_vol = inputDict["v"]
#     food = inputDict["f"]

#     # Compute the value densities for each item
#     food_weight_based = [(w, v, val, val/w if w != 0 else float('inf')) for w, v, val in food]
#     food_vol_based = [(w, v, val, val/v if v != 0 else float('inf')) for w, v, val in food]

#     # Sort by value density
#     food_weight_based.sort(key=lambda item: item[3], reverse=True)
#     food_vol_based.sort(key=lambda item: item[3], reverse=True)

#     total_value_weight_based = 0
#     for w, v, val, _ in food_weight_based:  
#         if w <= max_weight and v <= max_vol:
#             max_weight -= w
#             max_vol -= v
#             total_value_weight_based += val

#     max_weight = inputDict["w"]  # reset max_weight
#     max_vol = inputDict["v"]  # reset max_vol

#     total_value_vol_based = 0
#     for w, v, val, _ in food_vol_based:
#         if w <= max_weight and v <= max_vol:
#             max_weight -= w
#             max_vol -= v
#             total_value_vol_based += val

#     return max(total_value_weight_based, total_value_vol_based)


def MonkeBrain(inputDict):
    max_weight = inputDict["w"]
    max_vol = inputDict["v"]
    food = inputDict["f"]
    
    # Create a 3D table for dynamic programming
    dp = [[[-1 for _ in range(max_vol+1)] for _ in range(max_weight+1)] for _ in range(len(food)+1)]
    
    # Recursive function for knapsack
    def knapsack(i, w, v):
        # Base case: no items or no weight/volume left
        if i == 0 or w == 0 or v == 0:
            return 0
        # If the result is already computed, return it
        if dp[i][w][v] != -1:
            return dp[i][w][v]
        
        weight, vol, value = food[i-1]
        # If the item is too heavy or too voluminous, skip it
        if weight > w or vol > v:
            dp[i][w][v] = knapsack(i-1, w, v)
        else:
            # Either include the item or skip it, and choose the better option
            dp[i][w][v] = max(knapsack(i-1, w, v),
                               value + knapsack(i-1, w-weight, v-vol))
            
        return dp[i][w][v]
    
    # Call the recursive function starting with all items and the maximum weight and volume
    return knapsack(len(food), max_weight, max_vol)


@app.route('/greedymonkey', methods=['POST'])
def greedyMonkey():

# Debugging Purpose
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    input_value = data
    result = MonkeBrain(input_value)
    logging.info("My result :{}".format(result))

    return json.dumps(result)