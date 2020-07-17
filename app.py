import numpy as np

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
Measurement = Base.classes.measurement
Station = Base.classes.station

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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/temperatures<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/date_range/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precip():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all dates within past 12 months
    precipYear = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > "2016-08-31").\
        group_by(Measurement.date).\
        order_by(Measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    precipTuple = list(np.ravel(precipYear))

    return jsonify(precipTuple)

@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all stations
    stations = session.query(Measurement.station).distinct().all()

    session.close()

    # Convert list of tuples into normal list
    stationList = list(np.ravel(stations))

    return jsonify(stationList)

@app.route("/api/v1.0/temperatures")
def temp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query 
    tempObservations = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == "USC00519523").\
        filter(Measurement.date > "2016-08-31").\
        order_by(Measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    tempList = list(np.ravel(tempObservations))

    return jsonify(tempList)

@app.route("/api/v1.0/<start>")
def calc_temps(start):


    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query 
    tempDate = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    session.close()

    # Convert list of tuples into normal list
    tempDateList = list(np.ravel(tempDate))

    return jsonify(tempDateList)

@app.route("/api/v1.0/date_range/<start>/<end>/")
def calc_temps2(start, end):


    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query 
    dateRange = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    session.close()

    # Convert list of tuples into normal list
    dateRangeResults = list(np.ravel(dateRange))

    return jsonify(dateRangeResults)

if __name__ == '__main__':
    app.run(debug=True)