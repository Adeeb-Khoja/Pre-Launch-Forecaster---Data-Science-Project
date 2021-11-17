import os 
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pyrebase

class Modeler_Diffusion:
    def __init__(self):
    #    self.model = 'Diffusion Model'
        self.A = []         
        self.R = []         
        self.F = []          
        self.N = []

    def get_bass_model(self,p, q, M, period):   
        self.A = [0] * period          
        self.R = [0] * period         
        self.F = [0] * period          
        self.N = [0] * period         

        self.A[0] = 0
        self.R[0] = M
        self.F[0] = p
        self.N[0] = M*p
        t = 1

        def get_bass_model_helper(A, R, F, N, t):
            if t == period:
                return N, F, R, A
            else:            
                A[t] = N[t-1] + A[t-1]
                R[t] = M - A[t]
                F[t] = p + q * A[t]/M
                N[t] = F[t] * R[t]

            return get_bass_model_helper(A, R, F, N, t+1)

        self.N, self.F, self.R, self.A = get_bass_model_helper(self.A,
         self.R, self.F, self.N, t)
        return np.array(self.N), np.array(self.A)

    def Upload_NewAdopters_Graphs(self,p,q,period,dataset_name):
        
        t = list(range(0, period))

        fig1 = plt.figure()
        ax1=plt.gca()
        # New Adopters Graph
        ax1.plot(t, self.N, markersize = 4)
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.set_title('Adoption Count over Time Period')
        ax1.set_ylabel("New Adopters")
        ax1.set_xlabel("Years (t)")
        ax1.set_xticks(t)
        fig1.tight_layout()
        fig1.savefig('new adopters graph', dpi = 500)

        fig2 = plt.figure()
        ax2=plt.gca()
        #Cumulative adopters Graph
        ax2.plot(t, self.A, markersize = 4)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.set_title('Adoption Count over Time Period')
        ax2.set_ylabel("Cumulative Adopters")
        ax2.set_xlabel("Years (t)") 
        ax2.set_xticks(t)
        fig2.tight_layout()
        fig2.savefig('cumulative adopters graph', dpi = 500)

        serviceAccountConfig ={
            "type": "service_account",
            "project_id": "pre-launch-forecaster",
            "private_key_id": "1a4c412048f5d5d25c286f67b27859a8e9aae9b1",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCmI9ms/xhEpovA\nJ1faUxVC3aglX2SElWQggQ1ZyteXnSAq8w8PBd81jacm2KgGog6BU1iwWx0jPC14\nP7sh2D1rzVcYzE1UGoboCnM7pbs185cnHPqvS+FIP8WQTA0s4M+SLj1OAjX3OtCp\nokkObbTmCgIik5D9zELeQhaqYrNFEpwb972y/0hE0vs+GljkigMvBzO3iK3vlRUb\nDsqc5qp5WqZtgIzV+VyXXuF/TGCJxdutlqxUhU40BIFjboNKrMqh2o3ZS8zcbmTc\nSV5GpxUZdTJjKe/TXITZK+ICHIZj0r/BtLSlbsuesoC5x/vcVMla0eqHkNL+e2C8\nPVB2r9M/AgMBAAECggEAGkOX7sGTnDlZOwg9MCtq31uGcFoIhu54RKyCEswpPDOV\nA+p8BUZKsf7xtLISu0cKf1FQt5hqc8kt8FDgNrUmMzuOkEID23l8vYP2vDAyoeXJ\n4woGwIgrVgOW1NKLpqjnciwoeYOJ9R/Gys+ijaBe35rSGZXgbu7H3LZFOlbzZhtj\nfUse7pFV8FI2c2/2ertRQh1pPUbBfotq8GtV5SCujuD/SZGe1YL6wOwexrkOg1a1\nncFtB4GdLU2BoiZSn+fpjRpYc1GPFWTW83cIzaAqTzojeudZfYPQyNo8supqueT+\nHA3m9YDMrnbfdZZE2X0UVwsrjp/2yJsp5tdZFoixeQKBgQDQxlNQsCptXF/QNfHu\nPXPvhsuGfqwJZdRofjLnFDX/Hr5z9Q67UXMjfeBoN8iZpKqvjwCpTgNWiC84n/1B\nbxWYlzAzBdRqbr09Z5OdzK+kYcT0KZGXaRoJs3z/o9Wih2iymyslic9LCfcVzZkA\nK6sNp5VBuPP0vbHPQxTSVunIFQKBgQDLuKWdU3oiL/KTmnpjhOa/9pQ8Rh1WlHyt\nigxR9UQ1x6gP2Lcxb+vMOzvp2AVS3X+RlQr7+gNv8Xse0KNwmk2ABEKNbFYbbj7p\nuUV02UGDXRVpWbjJoTTTYIQn6fMI0aO7VfaLbKTG/zVrUrPHRT5oNAkf/rOIhXLR\nEUfs0WRPAwKBgEbPPWrclUdKUWT5Jvk69puDCHyxcgAt/YEDbJhbjoTdFJOXxkta\nMMcU5ovyf6M86ndo9Tx3LUKoJfv6p5cN6jE69ioYDBedP6oX+0VGKzyBvJ9jifHk\nv+QScI70Ln1Vl/kcD+JHf3tgAeHvPbmFFhsnf8Quyu9zd19ozSMaP2iRAoGBAK9l\njamTmp7em0K8CM2wOh9ihCQU1eOaOnILXioeOhj3iloCY088Jk8TXLUr2QGMVO4Z\n3XguvFDgHvnb9ivXngwvHsG2WbiKRb5jVkqRVtdsCChJKFDo65tmCMJ4qVeZbxe2\nnmtSIdh3GB4L+V8C3gVHb+fNGfPbuYwJDdz2Nx/TAoGAVif2QWoYsN3M8irfN6Ms\nTJV3mdlJq3uaQ29xP9lnBJcsYniSyGGyi8zySoDvML04ioHdmS3/bSDpInPMMp1o\ndN88wKdumfw1tDQvpJenRMrAORlXQ3e+nr4ZOxLs2utcy42WkC23tzQuOz0cFfGe\nt/hrIPIKJZRlGbtu8ycsx/A=\n-----END PRIVATE KEY-----\n",
            "client_email": "firebase-adminsdk-vjgn9@pre-launch-forecaster.iam.gserviceaccount.com",
            "client_id": "105039964167097231468",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-vjgn9%40pre-launch-forecaster.iam.gserviceaccount.com"
                }
        config = {
            "apiKey": "AIzaSyDxz1w7sZw4PUZAJ-bWbRASpfcBoKwsr84",
            "authDomain": "pre-launch-forecaster.firebaseapp.com",
            "databaseURL": "https://pre-launch-forecaster-default-rtdb.firebaseio.com",
            "projectId": "pre-launch-forecaster",
            "storageBucket": "pre-launch-forecaster.appspot.com",
            "messagingSenderId": "386991533112",
            "appId": "1:386991533112:web:0956fbe12d755d12ea8acd",
            "measurementId": "G-Y2VTVQPWG3",
            "serviceAccount": serviceAccountConfig
                }
        firebase = pyrebase.initialize_app(config)
        storage = firebase.storage()

        path_local1 = 'D:\\MY DATA\\Desktop\\DB\\Proposal\\new Senior\\Models Deployment\\All Models\\cumulative adopters graph.png'
        path_on_cloud1 = "Graphs/" + str(dataset_name) +" - cumulative graph.png"
        storage.child(path_on_cloud1).put(path_local1)

        path_local2 = 'D:\\MY DATA\\Desktop\\DB\\Proposal\\new Senior\\Models Deployment\\All Models\\new adopters graph.png'
        path_on_cloud2 = "Graphs/" + str(dataset_name) +" - new adopters graph.png"
        storage.child(path_on_cloud2).put(path_local2)