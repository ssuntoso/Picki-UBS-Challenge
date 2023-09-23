import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)


def MonkeBrain(inputDict):
    max_weight = inputDict["w"]
    max_vol = inputDict["v"]
    food = inputDict["f"]

    n = len(food)
    left_half = food[:n//2]
    right_half = food[n//2:]
    
    def compute_combinations(half):
        n = len(half)
        combinations = []
        for mask in range(1 << n):
            weight, vol, value = 0, 0, 0
            for i in range(n):
                if mask & (1 << i):
                    w, v, val = half[i]
                    weight += w
                    vol += v
                    value += val
            combinations.append((weight, vol, value))
        return combinations
    
    left_combinations = compute_combinations(left_half)
    right_combinations = compute_combinations(right_half)
    
    right_combinations.sort()
    
    def compute_max_values(combinations):
        max_values = [0 for _ in range(max_vol+1)]
        max_val = 0
        for w, v, val in combinations:
            if w <= max_weight and v <= max_vol:
                max_val = max(max_val, val)
                max_values[v] = max(max_values[v], max_val)
        for i in range(1, max_vol+1):
            max_values[i] = max(max_values[i], max_values[i-1])
        return max_values
    
    right_max_values = compute_max_values(right_combinations)
    
    max_value = 0
    for w1, v1, val1 in left_combinations:
        if w1 <= max_weight and v1 <= max_vol:
            w2 = max_weight - w1
            v2 = max_vol - v1
            val2 = right_max_values[v2] if v2 < len(right_max_values) else 0
            max_value = max(max_value, val1 + val2)
    
    return max_value


@app.route('/greedymonkey', methods=['POST'])
def greedyMonkey():

# Debugging Purpose
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    input_value = data
    result = MonkeBrain(input_value)
    logging.info("My result :{}".format(result))

    return json.dumps(result)