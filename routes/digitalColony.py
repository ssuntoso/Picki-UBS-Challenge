import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)

def getNextColony(colony, weight):
    colony_len = len(colony)
    result = []
    
    for i in range(colony_len - 1):
        num1, num2 = colony[i], colony[i + 1]
        sign = (num1 - num2) % 10
        newDigit = (weight + sign) % 10
        result.extend([num1, newDigit])
    
    result.append(colony[-1])  # Add the last element of the original colony
    
    return result

@app.route('/digital-colony', methods=['POST'])
def digitalColony():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = []
    for inputdata in data:
        generations = inputdata["generations"]
        colony = list(map(int, list(inputdata["colony"])))
        for i in range(generations):
            colony = getNextColony(colony, sum(colony))
        result.append(str(sum(colony)))
           
    logging.info("My result :{}".format(result))
    return json.dumps(result)