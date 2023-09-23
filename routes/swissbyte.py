import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)

def evaluate_code(challenge):
    code = challenge['code']
    cases = challenge['cases']

    def execute_code(code, variables):
        i = 0
        while i < len(code):
            line = code[i].split()

            if line[0] == 'fail':
                return "false", variables

            elif line[0] == 'if':
                var = variables[line[1]] if line[1] in variables else int(line[1])
                condition = line[2]
                comparison = variables[line[3]] if line[3] in variables else int(line[3])

                if (condition == '==' and var != comparison) or \
                (condition == '!=' and var == comparison) or \
                (condition == '>' and var <= comparison) or \
                (condition == '<' and var >= comparison):
                    while code[i] != 'endif':
                        i += 1

            elif line[1] == '=':
                if len(line) == 3:
                    variables[line[0]] = variables[line[2]] if line[2] in variables else int(line[2])
                else:
                    var1 = variables[line[2]] if line[2] in variables else int(line[2])
                    var2 = variables[line[4]] if line[4] in variables else int(line[4])

                    if line[3] == '+':
                        variables[line[0]] = var1 + var2
                    elif line[3] == '-':
                        variables[line[0]] = var1 - var2
                    elif line[3] == '*':
                        variables[line[0]] = var1 * var2
                    elif line[3] == '/':
                        variables[line[0]] = var1 // var2

            i += 1

        return "true", variables

    outcomes = []
    for case in cases:
        is_solvable, final_variables = execute_code(code, case)
        outcomes.append({
            'is_solvable': is_solvable,
            'variables': final_variables
        })

    return {'outcomes': outcomes}


@app.route('/swissbyte', methods=['POST'])
def swissbyte():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = evaluate_code(data)
    logging.info("My result :{}".format(result))
    return json.dumps(result)
