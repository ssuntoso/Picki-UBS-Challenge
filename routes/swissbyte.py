import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)

# def evaluate_code(challenge):
#     code = challenge['code']
#     cases = challenge['cases']

#     def execute_code(code, variables):
#         i = 0
#         while i < len(code):
#             line = code[i].split()

#             if line[0] == 'fail':
#                 return "false", variables

#             elif line[0] == 'if':
#                 var = variables[line[1]] if line[1] in variables else int(line[1])
#                 condition = line[2]
#                 comparison = variables[line[3]] if line[3] in variables else int(line[3])

#                 if (condition == '==' and var != comparison) or \
#                 (condition == '!=' and var == comparison) or \
#                 (condition == '>' and var <= comparison) or \
#                 (condition == '<' and var >= comparison):
#                     while code[i] != 'endif':
#                         i += 1

#             elif line[1] == '=':
#                 if len(line) == 3:
#                     variables[line[0]] = variables[line[2]] if line[2] in variables else int(line[2])
#                 else:
#                     var1 = variables[line[2]] if line[2] in variables else int(line[2])
#                     var2 = variables[line[4]] if line[4] in variables else int(line[4])

#                     if line[3] == '+':
#                         variables[line[0]] = var1 + var2
#                     elif line[3] == '-':
#                         variables[line[0]] = var1 - var2
#                     elif line[3] == '*':
#                         variables[line[0]] = var1 * var2
#                     elif line[3] == '/':
#                         variables[line[0]] = var1 // var2

#             i += 1

#         return "true", variables

#     outcomes = []
#     for case in cases:
#         is_solvable, final_variables = execute_code(code, case)
#         outcomes.append({
#             'is_solvable': is_solvable,
#             'variables': final_variables
#         })

#     return {'outcomes': outcomes}


def evaluate_code(challenge):
    code = challenge['code']
    cases = challenge['cases']

    def execute_code(code, variables):
        i = 0
        if_depth = 0
        skip = False
        while i < len(code):
            line = code[i].split()

            if line[0] == 'if':
                if_depth += 1
                if len(line) >= 4:
                    var = variables.get(line[1], int(line[1]))
                    condition = line[2]
                    comparison = variables.get(line[3], int(line[3]))

                    condition_not_met = ((condition == '==' and var != comparison) or 
                                         (condition == '!=' and var == comparison) or 
                                         (condition == '>' and var <= comparison) or 
                                         (condition == '<' and var >= comparison))
                    if condition_not_met:
                        skip = True
                else:
                    raise ValueError("Invalid 'if' statement")

            if skip:
                if line[0] == 'endif':
                    if_depth -= 1
                    if if_depth == 0:
                        skip = False
                i += 1
                continue

            if line[0] == 'fail':
                return "false", variables

            elif line[1] == '=':
                if len(line) >= 3:
                    if len(line) == 3:
                        variables[line[0]] = variables.get(line[2], int(line[2]))
                    else:
                        var1 = variables.get(line[2], int(line[2]))
                        var2 = variables.get(line[4], int(line[4]))

                        if line[3] == '+':
                            variables[line[0]] = var1 + var2
                        elif line[3] == '-':
                            variables[line[0]] = var1 - var2
                        elif line[3] == '*':
                            variables[line[0]] = var1 * var2
                        elif line[3] == '/':
                            variables[line[0]] = var1 // var2
                else:
                    raise ValueError("Invalid assignment")

            elif line[0] == 'endif':
                if_depth -= 1

            i += 1

        return "true", variables

    outcomes = []
    for case in cases:
        is_solvable, final_variables = execute_code(code, case.copy())
        outcomes.append({
            'is_solvable': is_solvable == "true",
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
