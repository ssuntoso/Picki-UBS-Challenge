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
        porto[i] = math.radians((porto[i]/total)*365)
    for i in reversed(porto):
        pie.append(i+pie[-1])
    return pie

@app.route('/pie-chart', methods=['POST'])
def piechart():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    part = data.get("part")
    if part == "FIRST":
        result = drawPieChart(data.get("data"))
    else:
        result = []
    logging.info("My result :{}".format(result))
    return json.dumps(result)
