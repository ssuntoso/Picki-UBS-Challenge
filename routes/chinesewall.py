import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)


@app.route('/chinese-wall', methods=['GET'])
def chinesewall():
    result = {
        "1": "Fluffy",
        "2": "Galactic",
        "3": "Mangoes",
        "4": "Subatomic",
        "5": "Throne"
        }
    logging.info("My result :{}".format(result))
    return json.dumps(result)
