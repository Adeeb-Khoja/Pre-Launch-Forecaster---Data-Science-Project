import os 
import joblib
from flask import Flask , jsonify, request
from flask_restful import Api, Resource
from modeler.Modeler_Classification import Modeler_Classification
from modeler.Modeler_Diffusion import Modeler_Diffusion
from modeler.Modeler_Price import Modeler_Price
import json
import statsmodels.api as sm

app = Flask(__name__)
api = Api(app)

class Predict_Sales(Resource):
    @staticmethod
    def post():
        data = request.get_json()
        p = 0.01
        q = 0.2
        M = data['market volume']
        period = data['period']
        datasetName = data['dataset name']
        
        m = Modeler_Diffusion()
        N, A = m.get_bass_model(p, q, M = M, period=period)

        new_adopters_dict = {}
        counter1 = 1
        for value in N:
            new_adopters_dict['year '+ str(counter1)] = value
            counter1 += 1
        
        counter2 = 1
        cum_adopters_dict ={}
        for value in A:
            cum_adopters_dict['year '+ str(counter2)] = value
            counter2 += 1

        m.Upload_NewAdopters_Graphs(p, q, period,datasetName)
        return jsonify({
            'Input': {
                'market volume': M,
                'period': period
            },
            'number of new adopters in each year': json.dumps(new_adopters_dict),
            'number of cumulative adopters over years': json.dumps(cum_adopters_dict)
        })



class Predict_Price(Resource):
    @staticmethod
    def post():
        data = request.get_json()
        horsepower = data['horsepower']
        carwidth = data['carwidth']
        carbody_hatchback = data['carbody_hatchback']
        carbody_wagon = data['carbody_wagon']
        carbody_sedan = data['carbody_sedan']
        enginetype_dohcv = data['enginetype_dohcv']

        m = Modeler_Price()
        if not os.path.exists('models/price.model'):
            m.fit()
        X = sm.add_constant([[horsepower,carwidth,carbody_hatchback,
        carbody_wagon,carbody_sedan,enginetype_dohcv]],has_constant='add')
        prediction = m.predict(X)
        return jsonify({
            'Input': {
                'horsepower':horsepower,
                'carwidth':carwidth,
                'carbody_hatchback':carbody_hatchback,
                'carbody_wagon':carbody_wagon,
                'carbody_sedan': carbody_sedan,
                'enginetype_dohcv':enginetype_dohcv
            },
            'Price': prediction
        })

class Predict_Cluster(Resource):
    @staticmethod
    def post():
        data = request.get_json()
        price = data['price']
        enginetype = data['enginetype']
        fueltype = data['fueltype']
        aspiration = data['aspiration']
        carbody = data['carbody']
        cylindernumber = data['cylindernumber']
        drivewheel = data['drivewheel']
        wheelbase = data['wheelbase']
        curbweight = data['curbweight']
        enginesize = data['enginesize']
        boreratio = data['boreratio']
        horsepower = data['horsepower']
        citympg = data['citympg']
        highwaympg = data['highwaympg']
        carlength = data['carlength']
        carwidth = data['carwidth']
        
        m = Modeler_Classification()
        if not os.path.exists('models/classifier.model'):
            m.fit()
        X = [[price,enginetype,fueltype,aspiration,carbody,cylindernumber,
        drivewheel,wheelbase,curbweight,enginesize,boreratio,horsepower,citympg,highwaympg,carlength,carwidth]]
        prediction = m.predict(X)
        return jsonify({
            'Input': {
                'price' : int(price),
                'enginetype' : int(enginetype),
                'fueltype' : int(fueltype),
                'aspiration' : int(aspiration),
                'carbody' : int(carbody),
                'cylindernumber' : int(cylindernumber),
                'drivewheel' : int(drivewheel),
                'wheelbase' : int(wheelbase),
                'curbweight' : int(curbweight),
                'enginesize' : int(enginesize),
                'boreratio' : int(boreratio),
                'horsepower': int(horsepower),
                'citympg' : int(citympg),
                'highwaympg' : int(highwaympg),
                'carlength' : int(carlength),
                'carwidth' : int(carwidth) 
            },
            'Cluster': int(prediction)
        })



api.add_resource(Predict_Sales, '/predict_sales')
api.add_resource(Predict_Price, '/predict_price')
api.add_resource(Predict_Cluster, '/predict_cluster')

if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1',port=8000)