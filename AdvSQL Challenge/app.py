# Import dependencies
import numpy as np
import datetime as dt
from dateutil.relativedelta import relativedelta

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import Flask and jsonify
from flask import Flask, jsonify

######################
# Setup for database #
######################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

###############
# Flask Setup #
###############
app = Flask(__name__)

################
# Flask Routes #
################
@app.route("/")
def welcome():
    """List all api routes"""
    return (
        f"Please follow below routes for more information<br/><br/>"
        f"/api/v1.0/precipitation<br/>Dictionary of date and precipitation<br/><br/>"
        f"/api/v1.0/stations<br/>List of the weather stations<br/><br/>"
        f"/api/v1.0/tobs<br/>Dictionary of date and tobs of the most active station for the last year of the data<br/><br/>"
        f"/api/v1.0/<start><br/>Min, Max, Avg tobs for all dates greater than and equal to the start date.<br/><br/>"
        f"/api/v1.0/<start>/<end><br/>Min, Max, Avg tobs for dates between the start and end date inclusive.<br/><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
     # Create session from Python
    session = Session(engine)

    # Query date and prcp for the last 12 months
    result = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>='2016-08-23').group_by(Measurement.date).order_by(Measurement.date).all()

    session.close()

   
    precipitation_list = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict['date'] = date
        precipitation_dict['prcp'] = prcp
        precipitation_list.append(precipitation_dict)

    return jsonify(precipitation_list)

# Show All weather stations
@app.route("/api/v1.0/stations")
def stations (): 
    session = Session(engine)

    result_1 = session.query(Station.station).all()

    session.close()

    all_stations = list(np.ravel(result_1))

    return jsonify(all_stations)
    

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
 
    # Query dates and temperature observations 
    result_2 =  session.query(Measurement.date,Measurement.tobs).filter(Measurement.date>='2016-08-23').filter(Station.station == Measurement.station).filter(Station.name == 'WAIHEE 837.5, HI US').all()

    session.close()

    # Temperature observations
    tobs_list = []
    for date, tobs in result_2:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs 
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)


@app.route("/api/v1.0/<start>")
def StartDate(start):
    session = Session(engine)
    result_3 = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).all()
    session.close()

    #list of max, min, avg tobs
    start_list = []
    for date,tmin,tmax,tavg in result_3:
        start_dict = {}
        start_dict["Date"] = date
        start_dict["TMIN"] = tmin
        start_dict["TMAX"] = tmax
        start_dict["TAVG"] = tavg
        start_list.append(start_dict)

    return jsonify(start_list)

@app.route("/api/v1.0/<start>/<end>")
def StartDateEndDate(start,end):
    session = Session(engine)
    result_4 = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date<=end).group_by(Measurement.date).all()
    session.close()
    startend_list = []
    for date,Tmin,Tmax,Tavg in result_4:
        startend_dict = {}
        startend_dict['Date'] = date
        startend_dict['TMIN'] = Tmin
        startend_dict['TMAX'] = Tmax
        startend_dict['TAVG'] = Tavg
        startend_list.append(startend_dict)

    return jsonify(startend_list)

if __name__ == '__main__':
    app.run(debug=True)