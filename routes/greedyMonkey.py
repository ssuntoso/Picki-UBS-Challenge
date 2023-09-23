import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)



def MonkeBrain(inputDict):
    max_weight = inputDict["w"]
    max_vol = inputDict["v"]
    food = inputDict["f"]
    
    dp = [[[-1 for _ in range(max_vol+1)] for _ in range(max_weight+1)] for _ in range(len(food)+1)]
    
    def knapsack(i, w, v):
        if i == 0 or w == 0 or v == 0:
            return 0
        if dp[i][w][v] != -1:
            return dp[i][w][v]
        
        weight, vol, value = food[i-1]
        # If the item is too heavy or too voluminous, skip it
        if weight > w or vol > v:
            dp[i][w][v] = knapsack(i-1, w, v)
        else:
            dp[i][w][v] = max(knapsack(i-1, w, v),
                               value + knapsack(i-1, w-weight, v-vol))
            
        return dp[i][w][v]
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