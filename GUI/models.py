import pyrebase
import pandas as pd
import requests
import json


class Models:
    def __init__(self):
        self.predicted_price = ""
        self.cluster = ""
        self.satisfaction = ""

    def callPriceModel(self, DatasetName):
        df = pd.read_csv(DatasetName)
        horsepower = df.horsepower.iloc[0]
        carwidth = df.carwidth.iloc[0]
        carbody = self.carbody(df.carbody.iloc[0])
        carbody_hatchback = 0
        carbody_wagon = 0
        carbody_sedan = 0
        if carbody == 2:
            carbody_hatchback = 1
        if carbody == 3:
            carbody_sedan = 1
        if carbody == 4:
            carbody_wagon = 1
        enginetype_dohcv = 0
        enginetype = self.engineType(df.enginetype.iloc[0])
        if enginetype == 1:
            enginetype_dohcv = 1
        list = [horsepower, carwidth, carbody_hatchback, carbody_wagon, carbody_sedan, enginetype_dohcv]
        response_price = requests.post(url='http://127.0.0.1:8000/predict_price',
                                       json={
                                           'horsepower': int(horsepower),
                                           'carwidth': int(carwidth),
                                           'carbody_hatchback': int(carbody_hatchback),
                                           'carbody_wagon': int(carbody_wagon),
                                           'carbody_sedan': int(carbody_sedan),
                                           'enginetype_dohcv': int(enginetype_dohcv)
                                       })
        response_price
        json_object = json.loads(response_price.content)
        print(json_object)
        n = json_object['Price']
        self.predicted_price = "%.2f" % round(n, 1)
        return str(self.predicted_price)

    def callClasificationModel(self, DatasetName):
        df = pd.read_csv(DatasetName)
        price = 15898.861708922908
        enginetype = self.engineType(df.enginetype.iloc[0])
        fueltype = self.fueltype(df.fueltype.iloc[0])
        aspiration = self.aspiration(df.aspiration.iloc[0])
        carbody = self.carbody(df.carbody.iloc[0])
        cylindernumber = self.cylindernumber(df.cylindernumber.iloc[0])
        drivewheel = self.drivewheel(df.drivewheel.iloc[0])
        wheelbase = df.wheelbase.iloc[0]
        curbweight = df.curbweight.iloc[0]
        enginesize = df.enginesize.iloc[0]
        boreratio = df.boreratio.iloc[0]
        horsepower = df.horsepower.iloc[0]
        citympg = df.city_mpg.iloc[0]
        highwaympg = df.highwaympg.iloc[0]
        carlength = df.carlength.iloc[0]
        carwidth = df.carwidth.iloc[0]

        response_cluster = requests.post(url='http://127.0.0.1:8000/predict_cluster',
                                         json={
                                             'price': int(price),
                                             'enginetype': int(enginetype),
                                             'fueltype': int(fueltype),
                                             'aspiration': int(aspiration),
                                             'carbody': int(carbody),
                                             'cylindernumber': int(cylindernumber),
                                             'drivewheel': int(drivewheel),
                                             'wheelbase': int(wheelbase),
                                             'curbweight': int(curbweight),
                                             'enginesize': int(enginesize),
                                             'boreratio': int(boreratio),
                                             'horsepower': int(horsepower),
                                             'citympg': int(citympg),
                                             'highwaympg': int(highwaympg),
                                             'carlength': int(carlength),
                                             'carwidth': int(carwidth)
                                         })
        response_cluster
        json_object = json.loads(response_cluster.content)
        print(json_object['Cluster'])
        if json_object['Cluster'] == 0:
            self.cluster = 'Cheap Cars'
        if json_object['Cluster'] == 1:
            self.cluster = 'Top Notch Cars'
        if json_object['Cluster'] == 2:
            self.cluster = 'Standard Cars'

        return self.cluster

    def callStatisfactionModel(self, DatasetName):
        df = pd.read_csv(DatasetName)
        model = self.car_Model(df.Model.iloc[0])
        year = df.Year.iloc[0]
        Engine_HP = df.Engine_HP.iloc[0]
        Engine_Cylinders = df.Engine_Cylinders.iloc[0]
        Driven_Wheels = self.DrivenWheels(df.Driven_Wheels.iloc[0])
        nbr_of_doors = df.Number_of_Doors.iloc[0]
        Market_Category = self.MarketCategory(df.Market_Category.iloc[0])
        Vehicle_Size = self.Size(df.Vehicle_Size.iloc[0])
        highway_MPG = df.highway_MPG.iloc[0]
        city_mpg = df.city_mpg.iloc[0]
        Vehicle_Style = self.VehicleStyle(df.Vehicle_Style.iloc[0])
        response_satis = requests.post(url='http://127.0.0.1:8000/predict_stisfaction',
                                       json={
                                           'Model': int(model),
                                           'Year': int(year),
                                           'Engine HP': int(Engine_HP),
                                           'Engine Cylinders': int(Engine_Cylinders),
                                           'Driven_Wheels': int(Driven_Wheels),
                                           'Number of Doors': int(nbr_of_doors),
                                           'Market Category': int(Market_Category),
                                           'Vehicle Size': int(Vehicle_Size),
                                           'highway MPG': int(highway_MPG),
                                           'city mpg': int(city_mpg),
                                           'Vehicle Style\r': int(Vehicle_Style)
                                       })
        response_satis
        response_satis.content
        json_object = json.loads(response_satis.content)
        s = json_object['Predicted Satisfaction Score'] * 10
        self.satisfaction = "%.1f" % round(s, 1)
        return self.satisfaction

    def callSalesModel(self, volume, period, datasetName):
        response_sales = requests.post(url='http://127.0.0.1:8000/predict_sales',
                                       json={
                                           'market volume': int(volume),
                                           'period': int(period),
                                           'dataset name': str(datasetName)

                                       })
        response_sales
        print("Uploaded")

    def engineType(self, i):
        switcher = {
            'dohc': 0,
            'dohcv': 1,
            'l': 2,
            'ohc': 3,
            'ohcf': 4,
            'ohcv': 5,
            'rotor': 6
        }
        return switcher.get(i, "Invalid engine")

    def carbody(self, i):
        switcher = {
            'convertible': 0,
            'hardtop': 1,
            'hatchback': 2,
            'sedan': 3,
            'wagon': 4
        }
        return switcher.get(i, "Invalid carbody")

    def fueltype(self, i):
        switcher = {
            'diesel': 0,
            'gas': 1
        }
        return switcher.get(i, "Invalid fuel")

    def aspiration(self, i):
        switcher = {
            'std': 0,
            'turbo': 1
        }
        return switcher.get(i, "Invalid aspitation")

    def carbody(self, i):
        switcher = {
            'convertible': 0,
            'hardtop': 1,
            'hatchback': 2,
            'sedan': 3,
            'wagon': 4
        }
        return switcher.get(i, "Invalid carbody")

    def cylindernumber(self, i):
        switcher = {
            'eight': 0,
            'five': 1,
            'four': 2,
            'six': 3,
            'three': 4,
            'twelve': 5,
            'two': 6
        }
        return switcher.get(i, "Invalid cylindernumber")

    def drivewheel(self, i):
        switcher = {
            '4wd': 0,
            'fwd': 1,
            'rwd': 2
        }
        return switcher.get(i, "Invalid drivewheel")

    def car_Model(self, i):
        switcher = {
            'X1': 16,
            'X6': 19,
            '3 Series': 2,
            '2 Series': 1,
            'M2': 11,
            'ActiveHybrid 7': 9,
            '6 Series': 5,
            'X5': 18,
            'nan': 24,
            'Z4': 21,
            'M': 10,
            '1 Series': 0,
            '5 Series': 4,
            '7 Series': 6,
            'Z8': 22,
            'M4': 13,
            'M6': 15,
            '4 Series': 3,
            '8 Series': 7,
            'X3': 17,
            'Z3': 20,
            'ALPINA B6 Gran Coupe': 8,
            'i3': 23,
            'M3': 12,
            'M5': 14
        }
        return switcher.get(i, "Invalid Model")

    def DrivenWheels(self, i):
        switcher = {
            'rear wheel drive': 2,
            'all wheel drive': 0,
            'nan': 1
        }
        return switcher.get(i, "Invalid Driven Wheels")

    def MarketCategory(self, i):
        switcher = {
            'Crossover,Luxury,Performance': 2,
            'Crossover,Luxury': 0,
            'Luxury': 6,
            'Luxury,Performance': 8,
            'Factory Tuner,Luxury,High-Performance': 4,
            'Luxury,Performance,Hybrid': 9,
            'Luxury,High-Performance': 7,
            'Crossover,Luxury,Diesel': 1,
            'nan': 10,
            'Exotic,Luxury,High-Performance': 3,
            'Hatchback,Luxury': 5
        }
        return switcher.get(i, "Invalid MarketCategory")

    def Size(self, i):
        switcher = {
            'Midsize': 2,
            'Compact': 0,
            'Large': 1,
            'nan': 3
        }
        return switcher.get(i, "invalid Size")

    def VehicleStyle(self, i):
        switcher = {
            '4dr SUV': 2,
            'Wagon': 6,
            'Coupe': 4,
            'Sedan': 5,
            'Convertible': 3,
            'nan': 0,
            '4dr Hatchback': 1
        }
        return switcher.get(i, "invalid Vehicle Style")
