import os 
import joblib
from flask import Flask , jsonify, request
from flask_restful import Api, Resource
from modeler.Modeler import Modeler
import json


app = Flask(__name__)
api = Api(app)

class Predict(Resource):
    @staticmethod
    def post():
        data = request.get_json()
        p = 0.01
        q = 0.2
        M = data['market volume']
        period = data['period']
        
        m = Modeler()
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
        return jsonify({
            'Input': {
                'market volume': M,
                'period': period
            },
            'number of new adopters in each year': json.dumps(new_adopters_dict),
            'number of cumulative adopters over years': json.dumps(cum_adopters_dict)
        })

api.add_resource(Predict, '/predict_diffusion')

if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1',port=8000)