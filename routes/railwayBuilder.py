import json
import logging
import operator
from functools import reduce
from typing import Dict, List

from flask import request

from routes import app


logger = logging.getLogger(__name__)


def total_combination(total, nums, i=0):
    if total==0:
        return 1
    elif total <0 or i == len(nums):
        return 0
    else:
        return total_combination(total - nums[i], nums, i) +  total_combination(total, nums, i + 1)

def Work(InputList):
    ListedInputList = []
    result = []

    #We split the first 2 character into number, and the rest as a list of integer
    for item in InputList:
        num_list = list(map(int, item.split(", ")))
        ListedInputList.append([num_list[0], num_list[1], num_list[2:]])

    for i in ListedInputList:
        max_railway_Length = i[0]
        number_of_railway_component = i[1]
        railway_components = i[2]
        
        result.append(total_combination(max_railway_Length, railway_components))

    return result

@app.route('/railway-builder', methods=['POST'])
def railwayBuilder():
    data = request.get_json()
    result = Work(data)
    logging.info("data sent for evaluation {}".format(data))
    logging.info("My result :{}".format(result))
    return json.dumps(data)



