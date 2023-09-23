import json
import logging
import math

from flask import request

from routes import app

logger = logging.getLogger(__name__)

def drawPieChart(data):
    porto = []
    pie = [0]
    for row in data:
        porto.append(row["price"]*row["quantity"])
    total = sum(porto)
    for i in range(len(porto)):
        porto[i] = (porto[i]/total)*6.28318531
        
    # readjustment section
    diffs = []
    for p in porto:
        if p < 0.00314159:
            # calculate difference
            diff = 0.00314159 - p
            diffs.append([diff,porto.index(p)])
            # redefine
            porto[porto.index(p)] = 0.00314159
    
    for diff in diffs:
        diff_indices = [i[1] for i in diffs]
        total = sum([i for i in porto if porto.index(i) not in diff_indices])
        for p in porto:
            if porto.index(p) not in diff_indices:
                porto[porto.index(p)] = p - diff[0]*(p/total)
                
    # reverse and sum
    porto.sort()
    porto.reverse()
    porto.insert(0,0.0)
    
    print(porto)
    
    pie = []
    c = 0
    for p in porto:
        if c == 0:
            pie.append(p)
        else:
            pie.append(p+pie[c-1])
        c += 1
        
    return pie

@app.route('/pie-chart', methods=['POST'])
def piechart():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    part = data.get("part")
    if part == "FIRST":
        result = drawPieChart(data["data"])
    else:
        result = []
    logging.info("My result :{}".format(result))
    return json.dumps(result)
