from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)
model = pickle.load(open("flight_dtr.pkl", "rb"))



@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")




@app.route("/predict", methods = ["GET", "POST"])
@cross_origin()
#function for converting time of format 00:00 to minutes
def convert_to_minutes(h,m):

    total_minutes = int(h * 60 ) + int(m)
    return total_minutes

def predict():
    if request.method == "POST":

        # Date_of_Journey
        date_dep = request.form["Dep_Time"]
        day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
        month = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").month)
        # print("Journey Date : ",Journey_day, Journey_month)

        # Departure
        Dep_hour = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").hour)
        Dep_min = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").minute)
        dept_time	= (Dep_hour,Dep_min)
        # print("Departure : ",Dep_hour, Dep_min)

        # Arrival
        date_arr = request.form["Arrival_Time"]
        Arrival_hour = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").hour)
        Arrival_min = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").minute)
        arr_time=(Arrival_hour,Arrival_min)
        # print("Arrival : ", Arrival_hour, Arrival_min)

        # Duration
        Duration_min = abs(arr_time - dept_time)
        # print("Duration : ", dur_hour, dur_min)

        # Total Stops
        Total_stops = int(request.form["stops"])
        # print(Total_stops)

        # Airline
        # AIR ASIA = 0 (not in column)
        clas = request.form['class']
        if (clas=="Economy"):
          Economy=1
        else:
          Buisness=0

        airline=request.form['airline']
        if(airline=='SpiceJet'):
            SpiceJet = 6

        elif (airline=='IndiGo'):
            Indigo =5

        elif (airline=='Air India'):
            Air_India = 0
            
        elif (airline=='GO First'):
            GoAir = 4
                     
        elif (airline=='AirAsia'):
            AirAsia= 1
            
        elif (airline=='Vistara'):
            Vistara=8

        elif (airline=='AkasaAir'):
            AkasaAir=2

        elif (airline=='AllianceAir'):
            AllianceAir=3

        elif (airline=='StarAir'):
            StarAir=7


        source = request.form["source"]
        if (source == 'Mumbai'):
          Mumbai=6

                   
        elif (source == 'Banglore'):
            Banglore=1

        elif (source == 'Hyderabad'):
            Hydrabad=4
        
        elif (source == 'Delhi'):
            Delhi=3

        elif (source == 'Kolkata'):
            Kolkata=5

        elif (source == 'Chennai'):
            Chennai=2
        elif (source == 'Ahmedabad'):
            Ahmedabad=0

      
      #destinations
        Destination = request.form["Destination"]
        if (Destination == 'Mumbai'):
          Mumbai=6

                   
        elif (Destination == 'Banglore'):
            Banglore=1

        elif (Destination == 'Hyderabad'):
            Hydrabad=4
        
        elif (Destination == 'Delhi'):
            Delhi=3

        elif (Destination == 'Kolkata'):
            Kolkata=5

        elif (Destination == 'Chennai'):
            Chennai=2
        elif (Destination == 'New_Delhi'):
            Ahmedabad=0

               
        prediction=model.predict([[
            day,month,Total_stops,airline,source,Destination,Duration_min,dept_time,arr_time
            
        ]])

        output=round(prediction[0],2)

        return render_template('home.html',prediction_text="Your Flight price is Rs. {}".format(output))


    return render_template("home.html")




if __name__ == "__main__":
    app.run(host="0.0.0.0")