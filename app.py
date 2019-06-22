import numpy as np
import sqlalchemy
import pandas as pd
import datetime as dt
import json

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from dateutil import parser
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
latest_date = pd.read_sql(session.query(Measurement).order_by(Measurement.date.desc()).statement,session.bind)["date"][1]
latest_date_dt = parser.parse(latest_date)
year_ago_date = latest_date_dt - dt.timedelta(days=365)
recent_year = session.query(Measurement.date, Measurement.prcp, Measurement.tobs).filter(Measurement.date >= year_ago_date).all()



@app.route("/")
def home():
    """List all available api routes."""
    return (
        """
        <h1>Hawai'i Climate Data</h1>
        <h2>Available Routes:<h2>
        <h3><ul>
                <li><a href="http://127.0.0.1:5000/api/v1.0/precipitation">Precipitation with dates from recent year</a>
                <li><a href="http://127.0.0.1:5000/api/v1.0/stations">List of all climate measuring stations</a>
                <li><a href="http://127.0.0.1:5000/api/v1.0/tobs">Temperature Observations with dates from recent year</a>
                <li>Temperature Statistics between desired date and most reccent date (MM-DD-YYYY format)</a>
                <br>Enter http://127.0.0.1:5000/api/v1.0/<desired date></br>
                e.g. http://127.0.0.1:5000/api/v1.0/2014-12-11 will return temperature statistics between 
                <li>Temperature Statistics between two desired dates (MM-DD-YYYY format)</a>
                <br>Enter http://127.0.0.1:5000/api/v1.0/<start date>/<end date>
                <br>e.g. http://127.0.0.1:5000/api/v1.0/2014-12-11/2014-12-18
                <h3>""")


@app.route("/api/v1.0/precipitation")
def precipitation():
        recent_year_prcp = []
        for date, prcp, tobs in recent_year:
                row = {}
                ignore={}
                row["date"] = date
                row["prcp"] = prcp
                recent_year_prcp.append(row)
                ignore["tobs"]=tobs
        return jsonify(recent_year_prcp)


@app.route("/api/v1.0/stations")
def stations():
        stations_query = session.query(Station.name, Station.station)
        all_stations = []
        for name, station in stations_query:
                row = {}
                row["name"] = name
                row["station"] = station
                all_stations.append(row)
        return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
        recent_year_tobs = []
        ignore = {}
        for date, prcp, tobs in recent_year:
                row = {}
                row["date"] = date
                row["tobs"] = tobs
                recent_year_tobs.append(row)
                ignore["prcp"] = prcp
        return jsonify(recent_year_tobs)
        


@app.route("/api/v1.0/<start>")
def start(start):
        def calc_temps(start):
                return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).all()
        temps = calc_temps(start)
        temp_stats=[]
        for tmin, tavg, tmax in temps:
            row = {}
            row["Minimum Temperature"] = tmin
            row["Average"] = tavg
            row["Maxiumum Temperature"]=tmin
            temp_stats.append(row)
        return jsonify(temp_stats)

@app.route("/api/v1.0/<start>/<end>")
def calc_temps(start,end):
        temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).filter(Measurement.date <= end).all()
        calc_temps=[]
        for tmin, tavg, tmax in temps:
            row = {}
            row["Minimum Temperature"] = tmin
            row["Average"] = tavg
            row["Maxiumum Temperature"]=tmax
            calc_temps.append(row)
        return jsonify(calc_temps)

if __name__ == '__main__':
    app.run(debug=True)

