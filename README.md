# DataSciPy-1
Data Science in Python - Assignment 1 (A+ grade achieved)

project structure:
i) assignment1.ipynb - The Jupyter notebook for nice step-by-step procedure including graphs and discussion of results.
ii) assignment1.py - The source code used to create the notebook.


This assignment served as both an introduction to data science as well as to Python.
The assignment was very open-ended, providing little instructions beyond "find an interesting web API, gather a sufficient amount of data, process that data appropriately and analyse the data to make some conclusions/predictions etc".  

## APIs Used

The main API I used to gather data was the Yahoo Weather API which provides which provides weather information for any location (historical and forecasted).
The Yahoo Weather API is also used in seperate requests to get the WOEID (where on earth ID) for each location used. A WOEID is an integer used by many weather/map applications to avoid placename translation issues between different languages.
The Google Maps Geocoder API is used to get the latitude of each location.

## Procedure 

### Collecting Data
* I picked out 10 different cities from around the world at various latitudes for which I wanted to gather forecasted weather information. 
* The WOEID is translated from each location name, using the Yahoo Weather API (for which there is a Python module).
* For each location, the latitude is found using the Google Maps Geocoder API.
* The latitudes are given in 'degrees, minutes, seconds', so I convert to a decimal degree value.
* The distance from the equator for each location is calculated using the decimal degree value.
* For each location for the next 10 consecutive days, I gather the forecasted high and low temperatures.
  * This is achieved using the Yahoo Weather web API, using YQL (yahoo query language) which is an SQL-like query language
    with the syntax: "select location, item.forecast from weather.forecast where woeid="
  * The query response is in json format and I parse it to retrieve the data of interest.
* The data is saved into a csv (comma seperated values) file with the following headings:
  * ["CITY", "COUNTRY", "DATE", "HIGH-TEMP", "LOW-TEMP", "LATITUDE", "DISTANCE"]


### Pandas
Pandas is a python library which provides tools for making data structures and tools for data analysis.

* Using the pandas.read_csv() function, I load the data from the CSV file into a pandas table.
* I made a function to sort the table by some input argument (e.g. by highest temperature descending).
* I use pandas built in functions throughout to sort and gather information as needed from the table (e.g. find the    forecasted weather in each city for a particular date, find the location/date which has the highest temperature for the forecasted days) etc.

Below is an example of the pandas table, filtering by only looking at data related to Dublin.
<image>

  
  
 ### Matplotlib
 Matplotlib is a python library for creating MATLAB like plots and graphs. I use matplotlib throughout to give visual context to my data.
 
 
## Analysis 
I examine the highest and lowest temperatures for the list of cities over the next 10 forecasted days.
I use the _panda_table_formatter_ method I created to sort the pandas dataframe. The method returns a new dataframe, sorted in ascending or descending order of the input parameter (e.g. high temperature).
The hottest and coldest temperature can be found using the pandas _.max()_ and _.min()_ methods respectively. 

Below are the outputs when examining the 5 hottest and 5 coldest temperatures for the forecasted days.
<image>
<image>


I also examine the weather for a particular location by just creating a new pandas dataframe by filtering an existing one based on location. Using the same data as in the table above for Dublin, I can create a matplotlib histogram to show the temperatures for the forecasted days. I had to create a new method _format_dates_ to change date format from 'dd-mmm-yy' to 'dd-mm' to fit on the plot.
<image of histogram>
  
  

Additionally, I examine tomorrow's weather for all locations. This simply involved creating a new dataframe, using the pandas _.min()_ method to find the "lowest" date (i.e. earliest recorded date). I also needed to shorten the city names to allow them to all fit on the graph neatly, so I made a _truncate_names_ method.
<image of tomorrow's weather table>
<image of tomorrow's weather graph>



Analysis continues on in a similar fashion, where I analysed the following stats:
* Temperature range in each city (max forecasted temp - min forecasted temp)
* The hottest day on average across all cities (is there any particular day on earth when the temperature is higher, on average, everywhere?)



Finally, I wanted to measure if there was a correlation between the mean high temperature and the distance from the equator for each city. Pandas _.mean()_ method comes in handy here, and a new dataframe is created, consisting of each city along with its mean high temperature over the forecasted days. Initially I used the 10 original locations, but I changed this to 40 locations to get a more accurate line of best fit to examine the correlation. The graph to represent this information is shown below, with a line of best fit:
<image>
 
The graph shows the data points are closely clustered around the line of best fit, showing a strong correlation. Using the _.corr()_ function to calculate the correlation, I found there was a correlation coeffeicient of approximately -0.91 (i.e. the mean high temperatures decrease as you get farther from the equator).


## Notes

The python Jupyter notebook (.ipynb file) shows the step-by-step process of the project, the code used, as well as a full discussion of results.
