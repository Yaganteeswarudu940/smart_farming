import numpy as np
import pickle
import pandas as pd
import category_encoders as ce

class Soil_fertility_result:

    def __init__(self,data):
        self.data = data

    def soil_fertility_result(self):
        model_file = 'D://Phd Research//crop usecases//smart_farming_tool//models//soil_fertility_model.pkl'
        model = pickle.load(open(model_file, 'rb'))
        prediction = model.predict(self.data)
        final_prediction = "Fertile"
        if prediction[0]==0:
            final_prediction='Non Fertile'
        elif prediction[0]==1:
            final_prediction="Fertile"
        else:
            final_prediction="Fertile"
        print("Final prediction ", final_prediction)
        return final_prediction
