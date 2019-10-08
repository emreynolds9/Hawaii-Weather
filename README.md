# Climate Analysis and Exploration

This project uses Python, MatPlotLib, and SQLAlchemy to do basic climate analysis and data exploration of a climate database. 

The data is queried from a sqlite file and an initial data exploration is done in a [Jupyter Notebook](https://github.com/emreynolds9/Hawaii-Weather/blob/master/SQL%20Alchemy%20Homework.ipynb).



![alt text](https://github.com/emreynolds9/Hawaii-Weather/blob/master/Images/precipitation.png)
![alt text](https://github.com/emreynolds9/Hawaii-Weather/blob/master/Images/station-histogram.png)
![alt text](https://github.com/emreynolds9/Hawaii-Weather/blob/master/Images/describe.png)
![alt text](https://github.com/emreynolds9/Hawaii-Weather/blob/master/Images/temperature.png)



# Climate App

The next part of the project is a Flask API based on the previous queries. Below are the API routes: 

Home page.
List all routes that are available.



/api/v1.0/precipitation - returns a JSON list of all precipitation observations from the dataset.
/api/v1.0/stations - return a JSON list of stations from the dataset.
/api/v1.0/tobs - returns a JSON list of Temperature Observations (tobs) for the previous year.
/api/v1.0/<start> and /api/v1.0/<start>/<end> - returns a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.






