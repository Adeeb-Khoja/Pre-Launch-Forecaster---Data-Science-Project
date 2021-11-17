import os 
import joblib
from flask import Flask , jsonify, request
from flask_restful import Api, Resource
from modeler.Modeler import Modeler


app = Flask(__name__)
api = Api(app)

class Predict(Resource):
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
        
        m = Modeler()
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

api.add_resource(Predict, '/predict_classification')

if __name__ == '__main__':
    app.run(debug=True)