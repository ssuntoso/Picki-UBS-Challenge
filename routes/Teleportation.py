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
    
    # Initialize the priority queue and visited set
    visited = [[False]*(k+1) for _ in range(n)]
    queue = [(dist[0][j], 0, k - int(j != 0)) for j in range(m)]  # (distance, node, orbs remaining)
    heapq.heapify(queue)

    while queue:
        d, node, orbs = heapq.heappop(queue)
        if visited[node][orbs]:
            continue
        visited[node][orbs] = True
        if node == n-1:
            return round(d, 2)
        for j in range(m):
            if orbs > 0 and not visited[node+1][orbs-1]:
                heapq.heappush(queue, (d + dist[node+1][j], node+1, orbs-1))
            elif j == 0 and not visited[node+1][orbs]:
                heapq.heappush(queue, (d + dist[node+1][j], node+1, orbs))
                
    return -1  # it's impossible to reach all delivery locations


@app.route('/teleportation ', methods=['POST'])
def teleportation():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = min_distance(data)
    logging.info("My result :{}".format(result))
    return json.dumps(result)
