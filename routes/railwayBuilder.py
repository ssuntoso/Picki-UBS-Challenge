import json
import logging
import operator
from functools import reduce
from typing import Dict, List

from flask import request

from routes import app


logger = logging.getLogger(__name__)


def total_combination(total, component_count, nums, memo=None, i=0):
    if memo is None:
        memo = {}
    if (total, component_count, i) in memo:
        return memo[(total, component_count, i)]
    if total == 0 and component_count == 0:
        return 1
    elif total < 0 or component_count < 0 or i == len(nums):
        return 0
    else:
        memo[(total, component_count, i)] = total_combination(total - nums[i], component_count - 1, nums, memo, i + 1) \
                                             + total_combination(total, component_count, nums, memo, i + 1)
        return memo[(total, component_count, i)]

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
        railway_components = sorted(i[2])  # sort nums in ascending order
        result.append(total_combination(max_railway_Length, number_of_railway_component, railway_components))
        
    return result

@app.route('/railway-builder', methods=['POST'])
def railwayBuilder():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = Work(data)
    logging.info("My result :{}".format(result))
    return json.dumps(result)



