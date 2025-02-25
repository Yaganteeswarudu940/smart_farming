import numpy as np
import pickle


class Crop_recomm_result:

    def __init__(self,data):
        self.data = data

    def crop_recomm_result(self):
        model_file = 'D://Phd Research//crop usecases//smart_farming_tool//models//crop_recommendationmodel.pkl'
        model = pickle.load(open(model_file, 'rb'))
        prediction = model.predict(self.data)
        print(prediction)
        crop_list=['apple' 'banana' 'blackgram' 'chickpea' 'coconut' 'coffee' 'cotton'
                   'grapes' 'jute' 'kidneybeans' 'lentil' 'maize' 'mango' 'mothbeans'
                   'mungbean' 'muskmelon' 'orange' 'papaya' 'pigeonpeas' 'pomegranate'
                   'rice' 'watermelon']
        final_pred = prediction[0]
        print(type(final_pred))
        print("Final predictions ", final_pred)
        final_crop = "no"
        if final_pred[-21]==1:
            final_crop = 'apple'
        elif final_pred[-20]==1:
            final_crop = 'banana'
        elif final_pred[-19]==1:
            final_crop = 'blackgram'
        elif final_pred[-18]==1:
            final_crop = 'chickpea'
        elif final_pred[-17]==1:
            final_crop = 'coconut'
        elif final_pred[-16]==1:
            final_crop = 'coffee'
        elif final_pred[-15]==1:
            final_crop = 'cotton'
        elif final_pred[-14]==1:
            final_crop = 'grapes'
        elif final_pred[-13]==1:
            final_crop = 'jute'
        elif final_pred[-12]==1:
            final_crop = 'kidneybeans'
        elif final_pred[-11]==1:
            final_crop = 'lentil'
        elif final_pred[-10]==1:
            final_crop = 'mango'
        elif final_pred[-9]==1:
            final_crop = 'mothbeans'
        elif final_pred[-8]==1:
            final_crop = 'mungbean'
        elif final_pred[-7]==1:
            final_crop = 'muskmelon'
        elif final_pred[-6]==1:
            final_crop = 'orange'
        elif final_pred[-5]==1:
            final_crop = 'papaya'
        elif final_pred[-4]==1:
            final_crop = 'pigeonpeas'
        elif final_pred[-3]==1:
            final_crop = 'pomegranate'
        elif final_pred[-2]==1:
            final_crop = 'rice'
        elif final_pred[-1]==1:
            final_crop = 'watermelon'
        else :
            final_crop = "no"
        print("Final crop ",final_crop)
        return final_crop





