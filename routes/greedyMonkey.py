import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)



def MonkeBrain(inputDict):
    max_weight = inputDict["w"]
    max_vol = inputDict["v"]
    food = inputDict["f"]
    
    # Create a 3D table for dynamic programming
    dp = [[[0 for item in range(max_vol+1)] for item in range(max_weight+1)] for item in range(len(food)+1)]
    
    for i in range(1, len(food)+1):
        weight, vol, value = food[i-1]
        for w in range(max_weight+1):
            for v in range(max_vol+1):
                if weight > max_weight or vol > max_vol:
                    continue
                elif weight <= w and vol <= v:
                    dp[i][w][v] = max(dp[i-1][w][v], dp[i-1][w-weight][v-vol] + value)
                else:
                    dp[i][w][v] = dp[i-1][w][v]
                    
    return dp[-1][-1][-1]



@app.route('/greedymonkey', methods=['POST'])
def greedyMonkey():

# Debugging Purpose
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    input_value = data
    result = input_value * input_value
    logging.info("My result :{}".format(result))

    return json.dumps(result)