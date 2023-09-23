import json
import logging
import heapq
import math

from flask import request

from routes import app

logger = logging.getLogger(__name__)


def min_distance(case):
    k = case['k']
    p = [[0, 0]] + case['p']  # add the starting point to the list of teleportation hubs
    q = case['q']
    n = len(q)
    m = len(p)

    # Define the distance matrix
    dist = [[math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2) for b in p] for a in q]

    # Start from the first delivery point
    current = 0
    total_distance = 0

    while current < n:
        # Find the nearest hub
        nearest_hub = min(range(m), key=lambda j: dist[current][j])

        # Add the distance to the total
        total_distance += dist[current][nearest_hub]

        # Move to the next delivery point
        current += 1

    return round(total_distance, 2)

@app.route('/teleportation', methods=['POST'])
def teleportation():
    data = request.data.decode("utf-8")  # Decode using utf-8 encoding
    logging.info("data sent for evaluation {}".format(data))
    
    # Assuming your data is a json string, you can convert it to a Python object
    import json
    data_object = json.loads(data)
    
    result = min_distance(data_object)
    logging.info("My result :{}".format(result))
    return str(result)