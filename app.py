from flask import Flask,request, url_for, redirect, render_template, jsonify
# from pycaret.regression import *
import pandas as pd
import pickle
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from statistics import mean
from sklearn.preprocessing import RobustScaler 
from sklearn.model_selection import cross_val_predict, cross_validate, cross_val_score
from sklearn import ensemble
import os
import fiona
from shapely.geometry import shape,mapping, Point, Polygon, MultiPolygon
import geojson
import json

# Initalise the Flask app
app = Flask(__name__)

# app.use("/static", express.static('./static/'))

# Loads pre-trained model
print("Current working directory: {0}".format(os.getcwd()))
model = pickle.load(open('finalized_model.pkl', 'rb'))

cols = ['District_code', 'rooms', 'Mosques_1_km', 'Hotels_1_km', 'HealthCentres_1_km', 'cafes_1_km', 'BusStops_1_km', 'Pharmacy_1_km', 'Governement_department_1_km', 'Refreshment_fastFood_1_km', 'PetrolStation_1_km', 'Public_Parks_1_km', 'Cultural_Facility_1_km' ]

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/predict',methods=['POST'])
def predict():
    int_features = [int(x) for x in request.form.values()]
    final = np.array(int_features)
    print(final)
    data_unseen = pd.DataFrame([final], columns = cols)
    print (type(data_unseen.values))
    print(data_unseen.values)
    prediction = model.predict(data_unseen.values)
    print (prediction)
    prediction = int(prediction[0])
    return render_template('home.html',pred='Expected house price will be {}'.format(prediction))

@app.route('/predict_api',methods=['POST'])
def predict_api():
    data = request.get_json(force=True)
    data_unseen = pd.DataFrame([data])
    prediction = model.predict(data_unseen.values)
    output = prediction[0]
    return jsonify(output)

@app.route('/district', methods=['POST'])
def district():
    lat = float(request.form['lat'])
    lng = float(request.form['lng'])

    with fiona.open('Abudhabi_analytics_final_3.json') as layer:
        Alist = list(layer)
    point = {'coordinates': (lng, lat), 'type': 'Point'}
    pt = shape(point)
    for district_mpolygon in Alist:
        if pt.within(shape(district_mpolygon['geometry'])):
            district_name = district_mpolygon['properties']['DISTRICTNA']
            district_id = district_mpolygon['properties']['id']
    print(district_name)
    district_info = {"district_name": district_name, "district_id": district_id}

    return json.dumps(district_info)



if __name__ == '__main__':
     app.run(debug=True)