# Import styling for plots
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

# Import data handling and array manipulation libraries
import numpy as np
import pandas as pd

# Import date handling library
import datetime as dt

# Regular expression library (if needed)
import re

# Import SQLAlchemy for database management
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import Flask for building the web app
from flask import Flask, jsonify

# Debugging output: check current working directory
import os
print("Current Working Directory:", os.getcwd())

# Database Setup
# Update this path to the actual location of your hawaii.sqlite file
engine = create_engine("sqlite:///C:/Users/antho/Downloads/SurfsUp/Resources/hawaii.sqlite")

# Reflect the tables
Base = automap_base()
Base.prepare(autoload_with=engine)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def welcome():
    return (
        f"Welcome to Hawaii Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start (enter as YYYY-MM-DD)<br/>"
        f"/api/v1.0/start/end (enter as YYYY-MM-DD/YYYY-MM-DD)"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    twelve_months = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    last_date = dt.date(twelve_months.year, twelve_months.month, twelve_months.day)
    pre_score = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_date).order_by(Measurement.date.desc()).all()
    session.close()
    
    # Create dictionary
    p_dict = dict(pre_score)
    return jsonify(p_dict)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    sel = [Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation]
    queryresult = session.query(*sel).all()
    session.close()
    
    # Format results into list of dictionaries
    stations = []
    for station, name, lat, lon, el in queryresult:
        station_dict = {
            "Station": station,
            "Name": name,
            "Lat": lat,
            "Lon": lon,
            "Elevation": el
        }
        stations.append(station_dict)
    
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    queryresult = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= '2016-08-23').all()
    session.close()
    
    # Format results into list of dictionaries
    tob_obs = [{"Date": date, "Tobs": tobs} for date, tobs in queryresult]
    return jsonify(tob_obs)

@app.route("/api/v1.0/<start>")
def temps_start(start):
    session = Session(engine)
    temp_result = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()
    
    # Format results into dictionary
    temps = []
    for min_temp, max_temp, avg_temp in temp_result:
        temps_dict = {
            "Minimum Temperature": min_temp,
            "Average Temperature": avg_temp,
            "Maximum Temperature": max_temp
        }
        temps.append(temps_dict)
    
    return jsonify(temps)

@app.route("/api/v1.0/<start>/<end>")
def temps_start_end(start, end):
    session = Session(engine)
    start_end_result = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    
    # Format results into dictionary
    temps = []
    for min_temp, avg_temp, max_temp in start_end_result:
        temps_dict = {
            "Minimum Temperature": min_temp,
            "Average Temperature": avg_temp,
            "Maximum Temperature": max_temp
        }
        temps.append(temps_dict)
    
    return jsonify(temps)

if __name__ == '__main__':
    app.run(debug=True)
