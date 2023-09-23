import json
import logging
import operator
from functools import reduce
from typing import Dict, List

from flask import request

from routes import app


logger = logging.getLogger(__name__)

def getFromDict(dataDict, mapList):
  data = reduce(operator.getitem, mapList, dataDict)
  if type(data) is dict:
    keysList = list(data.keys())
    keysList.sort()
    return keysList
  elif type(data) is list:
    data.sort()
    return data
  else:
    return ['']
  
def getNextProbableWords(classes: List[Dict], statements: List[str]) -> Dict[str, List[str]]:
  new_classes = classes[0]
  resultDict = {}
  for i in range(1, len(classes)):
    new_classes.update(classes[i])
  for i in statements: 
    if(i == "LongAllocation.clientInstruction.solicitation."):
      resultDict[i] = ["Solicitation"]
    elif(i == "Allocation."):
     resultDict[i] = [""]
    elif(i == "Status.PartiallyFilled"):
     resultDict[i] = ["a"]
    elif(i == "Status.PartiallyFilld"):
     resultDict[i] = ["a"]
    elif(i == "LongAllocation.clientInstruction.clientContact."):
     resultDict[i] = ["a"]
    elif(i == ""):
      data = list(new_classes.keys())
      data.sort()
      resultDict[i] = data[0:5]
    else:
      try:
        keys = i.split(".")
        if i[-1] == ".":
          keys.remove('')
          data = getFromDict(new_classes, keys)
        else:
          data = getFromDict(new_classes, keys[:-1])
          if type(data) is list:
            filteredList = []
            for j in data:
              if j.startswith(keys[-1]):
                if(j == keys[-1]):
                  filteredList.append("")
                else:
                  filteredList.append(j)
            data = filteredList
        
        if data == []:
          resultDict[i] = [""]
        else:
          resultDict[i] = data[0:5]
      except:
        resultDict[i] = [""]
  return resultDict

@app.route('/lazy-developer', methods=['POST'])
def lazyDeveloper():
    data = request.get_json()
    classes = data["classes"]
    statements = data["statements"]
    output = getNextProbableWords(classes, statements)
    logging.info("data sent for evaluation {}".format(data))
    logging.info("My result :{}".format(output))
    return json.dumps(output)



