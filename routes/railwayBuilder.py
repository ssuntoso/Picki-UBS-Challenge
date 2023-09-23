import json
import logging
import operator
from functools import reduce
from typing import Dict, List

from flask import request

from routes import app


logger = logging.getLogger(__name__)

@app.route('/railway-builder', methods=['POST'])
def railwayBuilder():
    data = request.get_json()
    #logging.info("data sent for evaluation {}".format(data))
    #logging.info("My result :{}".format(output))
    return json.dumps(data)



