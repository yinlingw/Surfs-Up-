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
##########################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurements
Station = Base.classes.stations

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
def welcome():
    """List all available api routes."""
    return (
        f"Surfs Up Info!!!!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    results_prec = session.query(Measurement.date, Measurement.tobs).\
    filter(func.strftime("%Y", Measurement.date) == "2017").all()

    temperature_dict = {}
    for temp in results_prec:
        temperature_dict["date"] = temp.tobs

    return jsonify(temperature_dict)


@app.route("/api/v1.0/stations")
def stations():

    results_stations = session.query(Station.station).all()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results_stations))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs_monthly():
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == "USC00519281").\
        filter(Measurement.date >= "2017-04-01").all()

    temperatures = list(np.ravel(results))
    return jsonify(temperatures)


@app.route("/api/v1.0/<start>")
def start_only(start):

    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).all()

    new_data = list(np.ravel(results))

    return jsonify(new_data)

@app.route("/api/v1.0/<start>/<end>")
def start_and_end(start, end):

    results_calc = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start, Measurement.date <= end).all()

    start_and_end_data = list(np.ravel(results))

    return jsonify(start_and_end_data)

if __name__ == '__main__':
    app.run(debug=True)