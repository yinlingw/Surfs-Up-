import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the table
Measurement = Base.classes.measurements
Station=Base.classes.stations

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def homepage():
    return(
        f"Hawaii Weather Repository API<br/>"
        f"Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )

@app.route("/api/v1.0/precipitation")
def percipitation():

    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2017-04-01").all()
    for item in data:
        data = {}
        data["date"]=Measurement.date
        data["prcp"]=Measurement.prcp
    return jsonify(data)
    
@app.route("/api/v1.0/stations")
def stations():
   results = session.query(Station.station).all()
   all_names = list(np.ravel(results))
   return jsonify(all_names)
@app.route("/api/v1.0/tobs")
def tobs():
    results = session.query(Measurement.tobs).\
    filter(Measurement.date >= "2017-04-01").\
    filter(Measurement.station == "USC00519281").all()

    temps = list(np.ravel(results))
    return jsonify(temps)
@app.route("/api/v1.0/<start>")
def strtonly(start):
    canonicalized = start.replace(" ", "")
    results = session.query(func.avg(Measurement.tobs),func.min(Measurement.tobs),func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all()
    new_data = list(np.ravel(results))
    return jsonify(new_data)
@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    new_start = start.replace(" ", "")
    new_end = end.replace(" ", "")
    results = session.query(func.avg(Measurement.tobs),func.min(Measurement.tobs),func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).all()
    new_data = list(np.ravel(results))
    
    return jsonify(new_data)


if __name__ == "__main__":
    app.run(debug=True)