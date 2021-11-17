import os 
import joblib
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier

class Modeler:
    def __init__(self):
        self.df = pd.read_csv('D:/MY DATA\Desktop/DB/Proposal/new Senior/Models Deployment/Classifier Model/modeler/Main Clustered Data.csv')
        try: self.model = joblib.load('models/classifier.model')
        except: self.model = None

    def fit(self):
        X , Y = self.df.loc[: , self.df.columns != 'cluster'] , self.df.loc[:, 'cluster']
        self.model =  KNeighborsClassifier(n_neighbors = 3)
        self.model.fit(X,Y)
        joblib.dump(self.model, 'models/classifier.model')
        
    def predict(self, measurement):
        if not os.path.exists('models/classifier.model'):
            raise Exception('Model not trained yet. Fit the model first')
        #if len(measurement[0]) != 7:
            #raise Exception(f'Expected six parameter for predictions but got {measurement}')
        prediction = self.model.predict(measurement)
        return prediction[0]