import json
import os

def get_parameter_value(parameter_name):
    # Opening JSON file
    f = open(f"{os.path.dirname(os.path.realpath(__file__))}/PARAMETERSTORE.json")

    # returns JSON object as a dictionary
    data = json.load(f)
    
    # Closing file
    f.close()
    return data[parameter_name]
