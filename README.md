# SQLAlchemy Surfs Up Project

![](Surf.gif)

For this project I took a SQLite dataset about Honolulu, Hawaii and with SQLAlchemy in Python ran a climate analysis on it. 

1. First I utilized SQLAlchemy create_engine to connect to the sqlite database.


2. I then used SQLAlchemy automap_base() to reflect my tables into classes and save a reference to those classes called Station and Measurement.


3. I then linked Python to the database by creating an SQLAlchemy session.

**Precipitation Analysis**

1. First I started by finding the most recent date in the data set.


2. Using this date, I then retrieved the last 12 months of precipitation data by querying the 12 preceding months of data. Note you do not pass in the date as a variable to your query.


3. I then narrowed the query results down to just the date and prcp values.


4. I then loaded the query results into a Pandas DataFrame and set the index to the date column and sorted the values by date.


5. I then utilized MatPlotLib to plot the results using the DataFrame plot method.









