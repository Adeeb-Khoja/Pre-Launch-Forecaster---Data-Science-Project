import os 
import joblib
from flask import Flask , jsonify, request
from flask_restful import Api, Resource
from modeler.Modeler import Modeler
import statsmodels.api as sm

app = Flask(__name__)
api = Api(app)

class Predict(Resource):
    @staticmethod
    def post():
        data = request.get_json()
        horsepower = data['horsepower']
        carwidth = data['carwidth']
        carbody_hatchback = data['carbody_hatchback']
        carbody_wagon = data['carbody_wagon']
        carbody_sedan = data['carbody_sedan']
        enginetype_dohcv = data['enginetype_dohcv']

        m = Modeler()
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

api.add_resource(Predict, '/predict')

if __name__ == '__main__':
    app.run(debug=True)