import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)

def getNextColony(colony, weight):
    result = [colony[0]]

    for i in range(1, len(colony)):
        num1, num2 = colony[i-1], colony[i]
        sign = (num1 - num2) % 10
        newDigit = (weight + sign) % 10
        result.extend([newDigit, num2])

    return result

def getFinalWeight(data):
    result = []
    for inputdata in data:
        generations = inputdata["generations"]
        colony = list(map(int, list(inputdata["colony"])))
        colony_sum = sum(colony)
        for i in range(generations):
            colony = getNextColony(colony, colony_sum)
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