import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
import warnings
import statsmodels.api as sm
import numpy as np
import csv
from sklearn.metrics import r2_score

from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import RFE
from statsmodels.stats.outliers_influence import variance_inflation_factor
import numpy as np
from sklearn import metrics
import seaborn as sns
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler

with open(r'C:\Users\user\PycharmProjects\SeniorV7.0\Datasets\listfet2.csv', newline='') as f:
    reader = csv.reader(f)
    features = list(reader)


class Feature:
    def __init__(self):
        self.predicted_score = ""
        self.predicted_accuracy = ""

    def pred(self, x):
        df_SC = pd.read_csv(r'C:\Users\user\PycharmProjects\SeniorV7.0\Datasets\FinalDataset_SC.csv')
        key_fet = x
        data_Fet = pd.DataFrame([])
        # search for the key and fetch the data into the Data df
        for i in range(len(df_SC)):
            if key_fet in str(features[i]):
                data_Fet = data_Fet.append(pd.DataFrame({'Vehicle_Title': df_SC['Vehicle_Title'][i],
                                                         'Ratings': str(df_SC['Ratings'][i]),
                                                         'Sentiment': df_SC['Sentiment'][i],
                                                         'Compound_Score': df_SC['Compound_Score'][i]},
                                                        index=[0]), ignore_index=True)
        for c in data_Fet.columns:
            if data_Fet[c].dtype == 'object':
                lbl = preprocessing.LabelEncoder()
                lbl.fit(list(data_Fet[c].values))
                data_Fet[c] = lbl.transform(list(data_Fet[c].values))
        np.random.seed(0)
        df_train, df_test = train_test_split(data_Fet,
                                             train_size=0.7, test_size=0.3, random_state=0)
        y_train = df_train.pop('Compound_Score')
        X_train = df_train
        lm = LinearRegression()
        lm.fit(X_train, y_train)

        rfe = RFE(lm, 15)
        rfe = rfe.fit(X_train, y_train)
        col_sup = X_train.columns[rfe.support_]
        X_train_rfe = X_train[col_sup]
        X_train_rfec = sm.add_constant(X_train_rfe)
        lm_rfe = sm.OLS(y_train, X_train_rfec).fit()
        y_train_sats = lm_rfe.predict(X_train_rfec)
        scaler = preprocessing.StandardScaler()

        warnings.filterwarnings("ignore")
        df_train = scaler.fit_transform(df_train)
        y_test = df_test.pop('Compound_Score')
        X_test = df_test
        X_test_1 = sm.add_constant(X_test)

        # Taking only the columns of the model
        X_test_new = X_test_1[X_train_rfec.columns]

        # The final predictions should be made by the testing data, all previous predictions were made by training data
        y_pred = lm_rfe.predict(X_test_new)
        predt2 = pd.DataFrame({'Real data': y_test.tolist(), 'Predicted data': y_pred.tolist()})

        leng = len(y_pred)
        acc = r2_score(y_test, y_pred) * 100
        score = predt2['Real data'].mean()
        print('accuracy: ', acc, '%\n\n', 'Score: ', score)
        self.predicted_score = str("%.1f" % round(score, 1))
        self.predicted_accuracy = str("%.1f" % round(acc, 1))

