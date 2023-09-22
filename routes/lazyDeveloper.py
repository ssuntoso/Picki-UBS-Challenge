import json
import logging
from typing import Dict, List

from flask import request

from routes import app


logger = logging.getLogger(__name__)

from typing import Dict, List

def getNextProbableWords(classes: List[Dict],
                         statements: List[str]) -> Dict[str, List[str]]:

  no_dicts = len(classes)  
  ansbank = []                # storing lists of values to be returned
  answer = {}                 # to be returned
  items = []                  # storing lists of segmented statements
  for i in range(len(statements)):          # loop for each statement
    items.append(statements[i].split("."))    # initializations, divide statements
    ansbank.append([])
    targetdict = -1                         
    refsearch = True                        # whether the key is successfully located. Implemented based on assumption in line 4.   
    for j in range(len(items[i]) - 1):      # loop for each segment (except the last one)
      refsearch = False                   
      if targetdict == -1:                      # the search will always start with main json mapping keys
        for d in range(no_dicts):                         # searching json mapping keys
          if items[i][j] in classes[d]:
            reference = items[i][j]                      
            valuetype = type(classes[d][reference])           # check type of json key to determine method of entry
            targetdict = d
            d = no_dicts
            refsearch = True
      elif valuetype == dict or valuetype == list:            # continuing into lists or dictionaries
        if items[i][j] in classes[targetdict][reference]:
          if valuetype == dict:            
            reference = classes[targetdict][reference][items[i][j]]
          else:                            
            reference = items[i][j]
          for d in range(no_dicts):                           # searching json mapping keys
            if reference in classes[d]:
              valuetype = type(classes[d][reference])
              targetdict = d
              d = no_dicts
              refsearch = True
    if refsearch:
      for j in classes[targetdict][reference]:                # returning probable words
        if items[i][-1] == j[:len(items[i][-1])]:
          ansbank[i].append(j)
      ansbank[i].sort()                                       # ascending alphabetical order
      while len(ansbank[i]) > 5:                              # select top 5
        ansbank[i].pop()
    if len(ansbank[i]) == 0:                                  # add empty string for no results
      ansbank[i].append("")
    answer[statements[i]] = ansbank[i]
  # Fill in your solution here and return the correct output based on the given input
  return answer

@app.route('/lazy-developer', methods=['POST'])
def lazyDeveloper():
    data = request.get_json()
    classes = data["classes"]
    statements = data["statements"]
    output = getNextProbableWords(classes, statements)
    print(output)
    return json.dumps(output)



