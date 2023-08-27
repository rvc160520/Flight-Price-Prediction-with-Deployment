from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd
import numpy as np

application = Flask(__name__)
app = application
model = pickle.load(open(r'flight.pkl', "rb"))

print(model)

@app.route("/")
@cross_origin()
def home():
    return render_template("h2.html")




@app.route("/predict", methods = ["GET", "POST"])
@cross_origin()
#function for converting time of format 00:00 to minutes
def predict():
    def convert_to_minutes(h,m):

        t_min = int(h * 60 ) + int(m)
        return t_min
    
    print("In predict")
    print(request.method)
    print(request.form)
    if request.method == "POST":
        #Date of booking

        date_book = request.form["Arr_time"]
        date_books = pd.to_datetime(date_book, format="%Y-%m-%dT%H:%M")
        print(date_book)


        # Date_of_Journey2
        date_dep = request.form["Dep_Time"]
        date_dep=pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M")
        day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
        month = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").month)
        print("Journey Date : ",day, month)
        
        
        #daysource_left1
        day_left=(date_dep - date_books).days
        print("daysource_left",day_left)

        
        # Departure1
        Dep_hour = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").hour)
        Dep_min = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").minute)
        dept_time	= convert_to_minutes(Dep_hour,Dep_min)
        print("Departure : ",Dep_hour, Dep_min,dept_time)

        
        # Arrival1
        date_arr = request.form["Arrival_Time"]
        print(date_arr)
        Arrival_hour = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").hour)
        Arrival_min = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").minute)
        arr_time=convert_to_minutes(Arrival_hour,Arrival_min)
        print("Arrival : ", Arrival_hour, Arrival_min,arr_time)

        
        # Duration1
        Duration_min = abs(arr_time - dept_time)
        print(Duration_min)

        
        # Total Stops1
        Total_stops = int(request.form["stops"])
        print(Total_stops)

        #3
        clas = request.form['class']
        print(clas)
        if (clas=="Economy"):
          class_ECONOMY=1
          class_FIRST=0
          class_PREMIUMECONOMY=0
        elif (clas=="First"):
          class_ECONOMY=0
          class_FIRST=1
          class_PREMIUMECONOMY=0
        else:
          class_ECONOMY=0
          class_FIRST=0
          class_PREMIUMECONOMY=1
        

        
        #8airline_AirAsia=1airline_AkasaAir=0
        airline=request.form['airline']
        print(airline)
        if(airline=='AirAsia'):
            airline_AirAsia=1
            airline_AkasaAir=0
            airline_AllianceAir=0
            airline_GOFIRST=0
            airline_Indigo=0
            airline_SpiceJet=0
            airline_StarAir=0
            airline_Vistara=0
                    
        elif (airline=='Vistara'):
            airline_AirAsia=0
            airline_AkasaAir=0
            airline_AllianceAir=0
            airline_GOFIRST=0
            airline_Indigo=0
            airline_SpiceJet=0
            airline_StarAir=0
            airline_Vistara=1
        elif (airline=='AllianceAir'):
            airline_AirAsia=0
            airline_AkasaAir=0
            airline_AllianceAir=1
            airline_GOFIRST=0
            airline_Indigo=0
            airline_SpiceJet=0
            airline_StarAir=0
            airline_Vistara=0
        elif (airline=='GO FIRST'):
            airline_AirAsia=0
            airline_AkasaAir=0
            airline_AllianceAir=0
            airline_GOFIRST=1
            airline_Indigo=0
            airline_SpiceJet=0
            airline_StarAir=0
            airline_Vistara=0

        elif (airline=='Indigo'):
            airline_AirAsia=0
            airline_AkasaAir=0
            airline_AllianceAir=0
            airline_GOFIRST=0
            airline_Indigo=1
            airline_SpiceJet=0
            airline_StarAir=0
            airline_Vistara=0

        elif (airline=='Spicejet'):
            airline_AirAsia=0
            airline_AkasaAir=0
            airline_AllianceAir=0
            airline_GOFIRST=0
            airline_Indigo=0
            airline_SpiceJet=1
            airline_StarAir=0
            airline_Vistara=0
            
        elif (airline=='AkasaAir'):
            airline_AirAsia=0
            airline_AkasaAir=1
            airline_AllianceAir=0
            airline_GOFIRST=0
            airline_Indigo=0
            airline_SpiceJet=0
            airline_StarAir=0
            airline_Vistara=0

        else:
            airline_AirAsia=0
            airline_AkasaAir=0
            airline_AllianceAir=0
            airline_GOFIRST=0
            airline_Indigo=0
            airline_SpiceJet=0
            airline_StarAir=1
            airline_Vistara=0
    
        Source = request.form["Source"]
        print(Source)
        if (Source == 'Delhi'):
            source_Delhi = 1
            source_Kolkata = 0
            source_Mumbai = 0
            source_Chennai = 0
            source_Banglore=0
            source_Ahmedabad=0

        elif (Source == 'Kolkata'):
            source_Delhi = 0
            source_Kolkata = 1
            source_Mumbai = 0
            source_Chennai = 0
            source_Banglore=0
            source_Ahmedabad=0

        elif (Source == 'Mumbai'):
            source_Delhi = 0
            source_Kolkata = 0
            source_Mumbai = 1
            source_Chennai = 0
            source_Banglore=0
            source_Ahmedabad=0

        elif (Source == 'Chennai'):
            source_Delhi = 0
            source_Kolkata = 0
            source_Mumbai = 0
            source_Chennai = 1
            source_Banglore=0
            source_Ahmedabad=0
        
        elif (Source == 'Banglore'):
            source_Banglore=1
            source_Delhi = 0
            source_Kolkata = 0
            source_Mumbai = 0
            source_Chennai = 0
            source_Ahmedabad=0

        else:
            source_Ahmedabad=1
            source_Banglore=0
            source_Delhi = 0
            source_Kolkata = 0
            source_Mumbai = 0
            source_Chennai = 0

        # print(source_Delhi,
        #     source_Kolkata,
        #     source_Mumbai,
        #     source_Chennai)

        # Destination
        # Banglore = 0 (not in column)6
        Destination = request.form["Destination"]
        print(Destination)
        if (Destination == 'Ahmedabad'):
            Destination_Mumbai = 0
            Destination_Ahmedabad = 1
            Destination_Delhi = 0
            Destination_Banglore = 0
            Destination_Hyderabad = 0
            Destination_Kolkata = 0
        
        elif (Destination == 'Delhi'):
            Destination_Mumbai = 0
            Destination_Ahmedabad = 0
            Destination_Delhi = 1
            Destination_Banglore = 0
            Destination_Hyderabad = 0
            Destination_Kolkata = 0

        elif (Destination == 'Banglore'):
            Destination_Mumbai = 0
            Destination_Ahmedabad = 0
            Destination_Delhi = 0
            Destination_Banglore = 1
            Destination_Hyderabad = 0
            Destination_Kolkata = 0

        elif (Destination == 'Hyderabad'):
            Destination_Mumbai = 0
            Destination_Ahmedabad = 0
            Destination_Delhi = 0
            Destination_Banglore = 0
            Destination_Hyderabad = 1
            Destination_Kolkata = 0

        elif (Destination == 'Kolkata'):
            Destination_Mumbai = 0
            Destination_Ahmedabad = 0
            Destination_Delhi = 0
            Destination_Banglore = 0
            Destination_Hyderabad = 0
            Destination_Kolkata = 1

        else:
            Destination_Mumbai = 1
            Destination_Ahmedabad = 0
            Destination_Delhi = 0
            Destination_Banglore = 0
            Destination_Hyderabad = 0
            Destination_Kolkata = 0

               
        # prediction=model.predict([[
        #     airline,clas,source,Destination,Duration_min,dept_time,arr_time,Total_stops,daysource_left,month,day
            

        # ]])

        

        feature_vector = [[
            Duration_min,
            dept_time,
            arr_time,
            Total_stops,
            day_left,
            month,
            day,
            airline_AirAsia,
            airline_AkasaAir,
            airline_AllianceAir,
            airline_GOFIRST,
            airline_Indigo,
            airline_SpiceJet,
            airline_StarAir,
            airline_Vistara,
            class_ECONOMY,
            class_FIRST,
            class_PREMIUMECONOMY,
            source_Delhi,
            source_Kolkata,
            source_Mumbai,
            source_Chennai,
            source_Banglore,
            source_Ahmedabad,
            Destination_Mumbai,
            Destination_Ahmedabad,
            Destination_Delhi,
            Destination_Banglore,
            Destination_Hyderabad,
            Destination_Kolkata,
            
        ]]
        print(feature_vector)

        prediction = model.predict(np.array(feature_vector).reshape(1, -1))

        output=round(prediction[0],2)
        print(output)
        return render_template('h2.html',prediction_text="Your Flight price is Rs. {}".format(output))
    

        
    return render_template("h2.html")




if __name__ == "__main__":
    app.run(host="0.0.0.0" , port =5000)
    app.config['DEBUG'] = True
