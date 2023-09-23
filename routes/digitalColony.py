import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)

def getNextColony(colony, weight):
  nextColony = colony.copy()
  insertIndex = 0
  for i in range(len(colony)-1):
    j = i+1
    num1 = colony[i]
    num2 = colony[j]
    if (num1 >= num2):
      sign = num1-num2
    else:
      sign = 10-(num2-num1)
    newDigit = (weight + sign)%10
    nextColony.insert(j+insertIndex, newDigit)
    insertIndex += 1
  return nextColony

@app.route('/digital-colony', methods=['POST'])
def digitalColony():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = []
    for inputdata in data:
        generations = inputdata["generations"]
        colony = list(map(int, list(inputdata["colony"])))
        if(generations <= 10):
            for i in range(generations):
                colony = getNextColony(colony, sum(colony))
            result.append(str(sum(colony)))
        else:
           result.append("0")
           
    logging.info("My result :{}".format(result))
    return json.dumps(result)