import json
import logging
import heapq
import math

from flask import request

from routes import app

logger = logging.getLogger(__name__)


def heuristic(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def min_distance(case):
    k = case['k']
    p = [[0, 0]] + case['p']  # add the starting point to the list of teleportation hubs
    q = case['q']
    n = len(q)
    m = len(p)

    # Define the distance matrix
    dist = [[heuristic(a, b) for b in p] for a in q]

    # Initialize the priority queue with the starting state
    queue = [(0, 0, k)]
    visited = {(0,k): 0}

    while queue:
        d, node, orbs = heapq.heappop(queue)
        if node == n-1:
            return round(d, 2)
        for j in range(m):
            new_dist = d + dist[node][j]
            if orbs > 0:
                new_node = node + 1
                new_orbs = orbs - 1
            else:
                new_node = node
                new_orbs = orbs
            if (new_node, new_orbs) not in visited or new_dist < visited[(new_node, new_orbs)]:
                visited[(new_node, new_orbs)] = new_dist
                heapq.heappush(queue, (new_dist + heuristic(q[new_node], p[j]), new_node, new_orbs))

    return -1  # it's impossible to reach all delivery locations


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