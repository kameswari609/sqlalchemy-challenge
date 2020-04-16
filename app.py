

import numpy as np
import pandas as pd
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func , inspect

from flask import Flask, jsonify
# 1. import Flask
from flask import Flask


engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement


# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


session = Session(engine)

# 3. Define what to do when a user hits the index route
@app.route("/")
def welcome():

    print("welcome to home page")
    return (
        f"Welcome to the climate and stations API analysis!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/end<br/>"
      
    )





@app.route("/api/v1.0/precipitation")
def precipitation():

    
#Convert the query results to a dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.
  
  results = session.query(Measurement.date, Measurement.prcp).all()
 #for row in results:
    #print(row._asdict())
 #return jsonify(results)
# Create a dictionary from the row data and append to a list 
  all_passengers = []
  for date,prcp in results:
     passenger_dict = {}
     passenger_dict["date"] = date
     passenger_dict["prcp"] = prcp
        
     all_passengers.append(passenger_dict)

  return jsonify(all_passengers)



@app.route("/api/v1.0/stations")
def stations():
    results2 = session.query(Station.station, Station.name).all()
    return jsonify(results2)

# /api/v1.0/tobs
# Return a JSON list of Temperature Observations (tobs) for the previous year
@app.route("/api/v1.0/tobs")
def tobs():

 prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
 t_results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= prev_year).all()
 return jsonify(t_results)

@app.route("/api/v1.0/<date>")
def startDateOnly(date):
    results4 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= date).all()
    return jsonify(results4)


@app.route("/api/v1.0/<start>/<end>")
def startDateEndDate(start,end):
    results6 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(results6)    

if __name__ == "__main__":
    app.run(debug=True)
