import json

from flask import Flask, render_template, request,jsonify
from flask_bootstrap import Bootstrap

# Weather Prediction
from weather import Weather

# Market Stats
from market_stat import Market

# Crop Prediction
from crop_yield_prediction import Crop_yield_result
from Crop_recommendation import Crop_recomm_result
from soil_fertility_prediction import Soil_fertility_result
# Fertilizer Info
import pandas as pd


# Weather Forcast 15 Days
import requests
import bs4

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import pickle
import numpy as np

app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = 'e53b7406a43e2fd9ec89553019420927'


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/weather',methods=['POST','GET'])
def weather():
    weatherModel = Weather()
    if request.method == 'POST':
        city_name = request.form['city']
        if len(city_name) == 0:
            return render_template('weather_pred.html',error=1)
        f_value = request.form.get("daily")
        if(f_value=='Daily Weather Forcast'):
            f_value = request.form.get("daily")
            print(" form value ",f_value)
            daily = request.form['daily']
            print(daily)
            valid = weatherModel.update(city_name)
            if valid == 'noData':
                return render_template('weather_pred.html',error=1)

            weather_data = weatherModel.display()
            # print()
            invalidZip = False
            results = {"zipcode":city_name,"invalidZip":invalidZip, "weather":weather_data}

            return render_template('weather.html',results=results)
        if (f_value == '15 Days Weather Forcast'):
            day_15 = request.form['daily']
            print(day_15)
            city_name = city_name.lower()
            print(city_name)
            res = requests.get('https://www.timeanddate.com/weather/india/'+city_name+'/ext')
            data = bs4.BeautifulSoup(res.text,'lxml')
            # temp = data.find('table',{"id": "wt-ext"})
            temp = data.find_all('tr','c1')

            lt = []
            for i in range(len(temp)):
                dt = {}
                dt['day'] = temp[i].find('th').text
                x = temp[i].find_all('td')
                dt['temp'] = x[1].text
                dt['weather'] = x[2].text
                dt['temp_max'] = x[3].text
                dt['wind_speed'] = x[4].text
                dt['max_humidity'] = x[6].text
                dt['min_humidity'] = x[7].text
                dt['sun_rise'] = x[10].text
                dt['sun_set'] = x[11].text
                
                lt.append(dt)
            

            return render_template('weather_15_days.html',result=lt,result_len = len(lt))
      
    
    return render_template('weather_pred.html',error=0)



@app.route("/crop_recommendation", methods=['POST','GET'])
def crop_recommendation():
    if request.method == 'POST':
        nitrogen = request.form['nitrogen']
        phosphorus = request.form['phosphorus']
        potasium = request.form['potasium']
        temperature = request.form['temperature']
        humidity = request.form['humidity']
        ph = request.form['ph']
        rainfall = request.form['rainfall']
        data = [[nitrogen, phosphorus, potasium, temperature, humidity, ph, rainfall]]
        crop_data = Crop_recomm_result(data)
        final_crop=crop_data.crop_recomm_result()
        # model_file = 'crop_recommendationmodel.pkl'
        # model = pickle.load(open(model_file, 'rb'))
        # prediction = model.predict(data)
        # print(prediction)

        return render_template('crop_recommendation_result.html',result=final_crop, nitrogen_out=nitrogen, phosphorus_out=phosphorus, potasium_out=potasium,
                               temperature_out=temperature, humidity_out=humidity,ph_out=ph,rainfall_out=rainfall)


    return render_template('crop_recommendation_predict.html',error=0)


@app.route('/soil_fertility_prediction',methods=['POST','GET'])
def soil_fertility_prediction():
    if request.method == 'POST':
        nitrogen = request.form['nitrogen']
        phosphorus = request.form['phosphorus']
        potasium = request.form['potasium']
        ph = request.form['ph']
        EC = request.form['EC']
        OC = request.form['OC']
        OM = request.form['OM']
        Zn = request.form['Zn']
        Fe = request.form['Fe']
        Cu = request.form['Cu']
        Mn = request.form['Mn']
        Sand = request.form['Sand']
        Silt = request.form['Silt']
        Clay = request.form['Clay']
        CaCO3 = request.form['CaCO3']
        CEC = request.form['CEC']

        data = [[nitrogen, phosphorus, potasium, ph, EC, OC, OM,Zn,Fe,Cu,Mn, Sand,Silt,Clay,CaCO3,CEC ]]
        soil_obj = Soil_fertility_result(data)
        final_soil_type=soil_obj.soil_fertility_result()
        return render_template('soil_fertility_prediction_result.html',
                               result=final_soil_type,nitrogen_out =nitrogen,phosphorus_out=phosphorus,potasium_out=potasium,
                               ph_out=ph,EC_out=EC,OC_out=OC,OM_out=OM,Zn_out = Zn,Fe_out = Fe,Cu_out = Cu,
                               Mn_out = Mn ,Sand_out =Sand,Silt_out = Silt ,Clay_out = Clay,
                               CaCO3_out = CaCO3 , CEC_out = CEC)

    return render_template('soil_fertility_prediction_main.html')
    

@app.route('/crop_yield_prediction',methods=['GET','POST'])
def crop_yield_prediction():

    if request.method == 'POST':
        State_Name = request.form['State_Name']
        District_Name = request.form['District_Name']
        Season = request.form['Season']
        Crop = request.form['Crop_name']
        Area = request.form['Area']
        data = [State_Name, District_Name, Season, Crop, Area]
        crop_yield = Crop_yield_result(data)
        yield_value= crop_yield.crop_yield_result()

        return render_template('crop_yield_prediction_result.html',result=yield_value,State_Name_out = State_Name,
                               District_Name_out=District_Name,Season_out=Season,Crop_name_out = Crop,Area_out=Area)

    return render_template('crop_yield_prediction_main.html',error=0)



@app.route('/fertilizer_info',methods=['POST','GET'])
def fertilizer_info():
    data = pd.read_csv('final_fertilizer.csv')
    crops = data['Crop'].unique()

    if request.method == 'GET':
        crop_se = request.args.get('manager')
        query = data[data['Crop']==crop_se]
        query = query['query'].unique()
        queryArr = []
        if len(query):
            for query_name in query:
                queryObj = {}
                queryObj['name'] = query_name
                print(query_name)
                queryArr.append(queryObj)
            
            return jsonify({'data':render_template('fertilizer.html',crops=crops,crop_len=len(crops)),
                            'query':queryArr})
           
    
    if request.method == 'POST':
        crop_name = request.form['crop']
        query_type = request.form['query']
        query = data[data['Crop']==crop_name]
        answer = query[query['query']== query_type]
        answer = answer['KCCAns'].unique()
        protection = []
        for index in answer:
            protection.append(index)

        return render_template('fertilizer.html',protection=protection,protection_len=len(protection),display=True,crops=crops,crop_len=len(crops))


    return render_template('fertilizer.html',crops=crops,crop_len=len(crops),query_len=0)


@app.route('/shop',methods=['POST','GET'])
def shop():
    if request.method == 'POST':
        city = request.form['city']
        print(city)

        return render_template('fertilizer_shop.html',city=city,data=True)

    return render_template('fertilizer_shop.html')

@app.route("/crop_recommendation_result", methods=['POST','GET'])
def crop_recommendation_result():
    return render_template('crop_recommendation_predict.html',error=0)

@app.route("/soil_fertility_result", methods=['POST','GET'])
def soil_fertility_result():
    return render_template('soil_fertility_prediction_main.html',error=0)

@app.route("/crop_yield_result", methods=['POST','GET'])
def crop_yield_result():
    return render_template('crop_yield_prediction_main.html',error=0)


if __name__ == "__main__":
    
    app.run(debug=True)
    
