import os 
import joblib
import pandas as pd
import statsmodels.api as sm

class Modeler:
    def __init__(self):
        self.df = pd.read_csv('C:/Users/abdul/Desktop/FYP/FinalDataset.csv')
        try: self.model = joblib.load('models/satisfaction.model')
        except: self.model = None

    def fit(self):
        X = self.df.drop('Compound_Score', axis=1)
        Y = self.df['Compound_Score']
        X = sm.add_constant(X)
        self.model = sm.OLS(Y, X).fit()
        joblib.dump(self.model, 'models/satisfaction.model')
        
    def predict(self, measurement):
        if not os.path.exists('models/satisfaction.model'):
            raise Exception('Model not trained yet. Fit the model first')
        #if len(measurement[0]) != 7:
            #raise Exception(f'Expected six parameter for predictions but got {measurement}')
        prediction = self.model.predict(measurement)
        return prediction[0]
        
        
        