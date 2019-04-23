# 1. import Flask
from flask import Flask, jsonify
import numpy as np
import pandas as pd

import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)
inspector = inspect(engine)



# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
            f"Welcome to my 'Surf's Up' page!<br/>"
            f"The following API's are available:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/<start><br/>"
            f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query all precipitation
    precipitation_query = session.query(Measurement.date, Measurement.prcp).\
                order_by(Measurement.date).all()

    #Convert to jsonify
    precipitation = []
    for precip in precipitation_query:
        precip_dict = {}
        precip_dict["date"] = precip.date
        precip_dict["prcp"] = precip.prcp
        precipitation.append(precip_dict)

    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():
    #Query stations info
    stations_query = session.query(Measurement.station, func.count(Measurement.station)).\
                    group_by(Measurement.station).\
                    order_by(func.count(Measurement.station).desc()).all()

    #Convert to jsonify
    stations = []
    for station in stations_query:
        station_dict = {}
        station_dict["station"] = station[0]
        station_dict["count"] = station[1]
        stations.append(station_dict)

    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():

    # Calculate the date 1 year ago from the last data point in the database
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    year_ago_tobs_data = session.query(Measurement.date, Measurement.tobs).\
                        filter(Measurement.date >= year_ago).\
                        order_by(Measurement.date).all()


    # Convert to jsonify
    year_ago__tobs = []
    for tob in year_ago_tobs_data:
        tobs_dict = {}
        tobs_dict["date"] = tob.date
        tobs_dict["station"] = tob.tobs
        year_ago__tobs.append(tobs_dict)

    return jsonify(year_ago__tobs)



@app.route("/api/v1.0/<start>")
def start_date(start_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
        Args:
            start_date (string): A date string in the format %Y-%m-%d
            end_date (string): A date string in the format %Y-%m-%d
        
        Returns:
            TMIN, TAVE, and TMAX"""
    start_date_results = session.query(func.min(Measurement.tobs), 
                        func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                        filter(Measurement.date >= start_date).all()

    calc_start_date = []
    for row in start_date_results:
        calc_tobs_dict = {}
        calc_tobs_dict["TMIN"] = row[0]
        calc_tobs_dict["TAVG"] = row[1]
        calc_tobs_dict["TMAX"] = row[2]
        calc_start_date.append(calc_tobs_dict)

    return jsonify(calc_start_date)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
        Args:
            start_date (string): A date string in the format %Y-%m-%d
            end_date (string): A date string in the format %Y-%m-%d
        
        Returns:
            TMIN, TAVE, and TMAX"""
    
    start_end_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), 
                        func.max(Measurement.tobs)).\
                        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    calc_start_end_date = []
    for row in start_end_results:
        calc_tobs_dict = {}
        calc_tobs_dict["TMIN"] = row[0]
        calc_tobs_dict["TAVG"] = row[1]
        calc_tobs_dict["TMAX"] = row[2]
        calc_start_end_date.append(calc_tobs_dict)

    return jsonify(calc_start_end_date)                   

if __name__ == "__main__":
    app.run(debug=True)


