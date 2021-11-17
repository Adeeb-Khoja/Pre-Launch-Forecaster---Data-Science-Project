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
        Model = data['Model']
        Year = data['Year']
        Engine_HP = data['Engine HP']
        Engine_Cylinders = data['Engine Cylinders']
        Driven_Wheels = data['Driven_Wheels']
        Number_of_Doors = data['Number of Doors']
        Market_Category = data['Market Category']
        Vehicle_Size = data['Vehicle Size']
        highway_MPG = data['highway MPG']
        city_mpg = data['city mpg']
        Vehicle_Style = data['Vehicle Style\r']


        m = Modeler()
        if not os.path.exists('models/satisfaction.model'):
            m.fit()
        X = sm.add_constant([[Model,Year,
        Engine_HP,Engine_Cylinders,Driven_Wheels,
       Number_of_Doors,Market_Category, Vehicle_Size,
      highway_MPG, city_mpg,Vehicle_Style]],has_constant='add')
        prediction = m.predict(X)
        return jsonify({
            
                'Model':Model,
                'Year':Year,
                'Engine HP':Engine_HP,
                'Engine Cylinders': Engine_Cylinders,
                'Driven_Wheels':Driven_Wheels,
                'Number of Doors':Number_of_Doors,
                'Market Category':Market_Category,
                'Vehicle Size':Vehicle_Size,
                'highway MPG':highway_MPG,
                'city mpg':city_mpg,
                'Vehicle Style\r':Vehicle_Style,
            
            'Predicted Satisfaction Sscore': prediction
        })

api.add_resource(Predict, '/predict')

if __name__ == '__main__':
    app.run(debug=True)