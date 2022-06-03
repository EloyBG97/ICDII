from pymongo import MongoClient
import pandas as pd
from sklearn.impute import KNNImputer
from datetime import datetime
import json
import os
import certifi
import seaborn as sns

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
    result = client['ICDII']['AirQuality'].aggregate([
        {
            '$unwind': {
                'path': '$data'
            }
        }, {
            '$addFields': {
                'data.avg_level': {
                    '$avg': [
                        '$data.values'
                    ]
                }
            }
        }, {
            '$group': {
                '_id': {
                    'pollutant': '$data.pollutant', 
                    'unit': '$data.unit', 
                    'date': '$date', 
                    'location': {
                        'com_autonoma': '$location.com_autonoma', 
                        'provincia': '$location.provincia'
                    }
                }, 
                'avg_level': {
                    '$avg': '$data.avg_level'
                }
            }
        }, {
            '$project': {
                '_id': 0, 
                'pollutant': '$_id.pollutant', 
                'unit': '$_id.unit', 
                'year': '$_id.date.year', 
                'month': '$_id.date.month', 
                'provincia': '$_id.location.provincia', 
                'com_autonoma': '$_id.location.com_autonoma', 
                'avg_level': 1
            }
        }
    ])


    #Step 1: Load Data
    list_cur = list(result)
    df = pd.DataFrame(list_cur)

    # Solo avg_level tiene NaN values
    #for col in df:
    #   print(len(df[df[col].isna()]))

    #Step 1: Imputate 'avg_level' values using KNN method 
    df["pollutant"] = df["pollutant"].astype('category')
    df["com_autonoma"] = df["com_autonoma"].astype('category')
    df["provincia"] = df["provincia"].astype('category')

    df["pollutant_cat"] = df["pollutant"].cat.codes
    df["com_autonoma_cat"] = df["com_autonoma"].cat.codes
    df["provincia_cat"] = df["provincia"].cat.codes

    imputer = KNNImputer(n_neighbors = 4)
    df["avg_level"] = imputer.fit_transform(df[["avg_level", "pollutant_cat", "com_autonoma_cat", "provincia_cat", "year", "month"]])[:,0]

    del df["pollutant_cat"]
    del df["com_autonoma_cat"]
    del df["provincia_cat"]
    
    #Step 2: Normalize scales (unit)
    df["avg_level"] = df.apply(lambda row: scale(row["unit"], row["avg_level"]), axis = 1)
    del df["unit"]


    #Step 3: Datetime

    df['Date'] = df.apply(lambda row: datetime(row["year"], row["month"], 1), axis = 1)
    del df["year"]
    del df["month"]

    

    df_v = df[df["com_autonoma"] == "Andalucía"]

    print(df_v.head())

    #Visualize...

    g = sns.relplot(data = df_v, x = "Date", y = "avg_level", hue = "pollutant", col = "pollutant")

    for pollutant, ax in g.axes_dict.items():

        # Add the title as an annotation within the plot
        ax.text(.8, .85, pollutant, transform=ax.transAxes, fontweight="bold")

        # Plot every year's time series in the background
        sns.lineplot(
            data=df_v, x="Date", y="avg_level",
            estimator=None, color=".7", linewidth=1, ax=ax,
        )

    # Reduce the frequency of the x axis ticks
    ax.set_xticks(ax.get_xticks()[::2])

    # Tweak the supporting aspects of the plot
    g.set_titles("")
    g.set_axis_labels("", "Passengers")
    g.tight_layout()

if(__name__ == '__main__'):
    main()
