import os 
import joblib
import pandas as pd
import numpy as np

class Modeler:
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
