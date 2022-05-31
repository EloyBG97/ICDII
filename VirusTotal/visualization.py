from pymongo import MongoClient
import pandas as pd
from sklearn.impute import KNNImputer
from datetime import datetime
import json
import os
import certifi

# Requires the PyMongo package.
# https://api.mongodb.com/python/current

def dist(X, Y, metric, **kwds):
    total = 0

    if(X["provincia"] != Y["provincia"]):
        total += 1

    if(X["com_autonoma"] != Y["com_autonoma"]):
        total += 1

    total += abs(X["year"] - Y["year"])
    total += abs(X["month"] - Y["month"])

    return total

def scale(unit, level):

    if(unit == "µg/m3"):
        level *= 10e-6

    elif(unit == "mg/m3"):
        level *= 10e-3

    elif(unit == "ng/m3"):
        level *= 10e-9

    return level


def auth():
    
    if(os.path.exists('../auth.json')):
        with open("../auth.json", 'r') as f:
            auth_data = json.load(f)

    else:
        auth_data = {
            "user": "invitado",
            "pass": "invitado"
        }

    return (auth_data["user"], auth_data["pass"])

def main():
    auth_data = auth()
    print("Authenticating as {user}".format(user = auth_data[0]))
    client = MongoClient('mongodb+srv://{user}:{passw}@cluster0.itzr6.mongodb.net/test'.format(user = auth_data[0], passw = auth_data[1]), tlsCAFile=certifi.where())
    result = client['ICDII']['VirusTotal'].aggregate([
    {
        '$project': {
            '_id': 0,
            'scan_id': 1, 
            'scans': {
                '$objectToArray': '$scans'
            }
        }
    }, {
        '$unwind': {
            'path': '$scans'
        }
    }, {
        '$project': {
            'scan_id': 1, 
            'antivirus_name': '$scans.k', 
            'detected': '$scans.v.detected', 
            'version': '$scans.v.version', 
            'result': '$scans.v.result', 
            'update': '$scans.v.update'
        }
    }, {
        '$match': {
            'detected': True
        }
    }
    ])

    #Step 1: Load Data
    list_cur = list(result)
    df = pd.DataFrame(list_cur)

    print(df.head())


if(__name__ == '__main__'):
    main()
