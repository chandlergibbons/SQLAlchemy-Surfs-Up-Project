from flask import Flask, jsonify
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import desc

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///hawaii.sqlite")
conn = engine.connect()

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#precipitation query
sel=[Measurement.date, Measurement.prcp]
date_precip_scores = session.query(*sel).group_by(Measurement.date).all()

date_precip_scores_pd = pd.DataFrame(date_precip_scores,columns=['Date', 'Precip_score'])

date_precip_scores_dict = date_precip_scores_pd.to_dict()

#station query
sel2=[Station.station]
stations = session.query(*sel2).all()

#tobs query sequence

#grabs most recent date
newest_date = session.query(Measurement).order_by(desc('date')).first()
old_date = newest_date.date


#subtracts a year from old_-date
from datetime import datetime
from dateutil.relativedelta import relativedelta

your_date_string = old_date
format_string = "%Y-%m-%d"

datetime_object = datetime.strptime(old_date, format_string).date()
new_date = datetime_object - relativedelta(years=1)
new_date_string = datetime.strftime(new_date, format_string).replace(' 0', ' ')



sel3=[Measurement.date, Measurement.tobs]
tobs = session.query(*sel3).filter(Measurement.date >= new_date_string).group_by(Measurement.date).all()





app = Flask(__name__)

@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Welcome to my 'Home' page!<br/>" 
        f"Here are all the routes<br/>" 
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
        )


@app.route("/api/v1.0/precipitation")
def jsonified():
    return jsonify(date_precip_scores_dict)


@app.route("/api/v1.0/stations")
def jsonified2():
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def jsonified3():
    return jsonify(tobs) 


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def stats(start=None, end=None):
    if start == None:
        return f"please return a valid date"

    elif end == None:

        sel4=[func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
        temp_mess = session.query(*sel4).filter(Measurement.date >= start).all()
        return jsonify(temp_mess)

    else:

        sel5=[func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
        temp_mess2 = session.query(*sel5).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
        return jsonify(temp_mess2)


    





    return jsonify(stations)


if __name__ == "__main__":
    app.run(debug=True)