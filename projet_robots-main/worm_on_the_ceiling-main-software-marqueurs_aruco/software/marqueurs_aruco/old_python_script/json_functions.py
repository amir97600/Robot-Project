
import json
import os
import numpy as np 
name = "config_calib"
file = os.path.abspath(name)

def write_json(data):
    """ 
    Writes matrice into JSON file
    """
    with open(file, "w") as outfile:
        mtx = data[0].tolist()
        dist = data[1].tolist()
        save = {"mtx" :mtx,"dist" : dist }
        json.dump(save,outfile)

def load_json():
    """
    Open a JSON file containing Matrix.
    """
    f = open(file)
    data = json.load(f)
    return data

