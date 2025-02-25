import numpy as np
import pickle
import pandas as pd
import category_encoders as ce

class Crop_yield_result:

    def __init__(self,data):
        self.data = data

    def crop_yield_result(self):
        model_file = 'D://Phd Research//crop usecases//smart_farming_tool//models//crop_yield_prediction_model.pkl'
        target_encoder = 'target_encoder.pkl'
        model = pickle.load(open(model_file, 'rb'))
        encoder_load = pickle.load(open(target_encoder, 'rb'))
        df_yield= pd.DataFrame()
        #print(self.data)
        #print(self.data[0])
        State_Name_list = [self.data[0]]
        District_Name_list = [self.data[1]]
        Season_list = [self.data[2]]
        Crop_list = [self.data[1]]
        Area_list = [self.data[4]]
        df_yield['State_Name']= State_Name_list
        df_yield['District_Name'] = District_Name_list
        df_yield['Season'] = Season_list
        df_yield['Crop'] = Crop_list
        df_yield_target=encoder_load.transform(df_yield)
        df_yield_target['Area']=Area_list
        prediction = model.predict(df_yield_target)
        print("Final Yield prediction ", prediction[0])
        return prediction[0]

