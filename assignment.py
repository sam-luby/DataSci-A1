# -*- coding: utf-8 -*-
import os
import csv
import urllib
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import scipy
import urllib.request
from datetime import datetime
import json
import yweather
import time
import csv
import requests
import math

##############
# parameters #
##############
matplotlib.rcParams.update({'font.size': 8})
data_file = "weather_data.csv"
baseurl = "https://query.yahooapis.com/v1/public/yql?"
client = yweather.Client()
google_maps_api = "AIzaSyADj82WQ-2GlwwyGLO5z5KHoE0OID3HKiQ"
google_maps_api_url = 'https://maps.googleapis.com/maps/api/geocode/json'

locations = ["Dublin, Ireland", "London, England", "Paris, France", "Berlin, Germany", "Stockholm, Sweden", "Moscow, Russia", "Tokyo, Japan", "Sydney, Australia", "New York City, United States", "LA, United States"]
weather_headings = ["CITY", "COUNTRY", "DATE", "HIGH-TEMP", "LOW-TEMP", "LATITUDE", "DISTANCE"]
month_lookup = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07',
                'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}

forecast_days = 10
DEGREE_IN_KM = 111

# create csv file to write data to
def create_file(file_location, date_headings):
    with open(file_location, 'w') as write_file:
        f = csv.writer(write_file)
        f.writerow(date_headings)
    write_file.close()


# delete csv file
def delete_file(file_location):
    os.remove(file_location)


# write data to file
def write_to_file(file_location, data):
    with open(file_location, 'a') as write_file:
        f = csv.writer(write_file, delimiter=",", dialect='excel', lineterminator = '\n')
        f.writerow(data)
    write_file.close()


# get woeid (where on earth ID) from location names
def translate_woeids(locations):
    locations_woeid = []
    for location in locations:
        locations_woeid.append(client.fetch_woeid(location))

        # need a slight delay to not overload client call
        time.sleep(0.5)
    return locations_woeid


# returns latitude coordinate for given location using google's geocode API
def get_latitude(location):
    params = {
        'address': location,
        'sensor': 'false',
        'key': google_maps_api
    }
    req = requests.get(google_maps_api_url, params=params)
    res = req.json()
    result = res['results'][0]
    latitude = (round(result['geometry']['location']['lat'], 4))
    return latitude


# converts the degrees minutes second latitude value to a decimal degree value
def DMS_to_DD(latitude):
    latitude = abs(latitude)
    split_lat = str(latitude).split('.')
    degree = int(split_lat[0])
    minute = int(split_lat[1])
    decimal_latitude = degree + (round((minute/60), 2)/100)
    return decimal_latitude


# calculate approximate distance from the equator
def distance_from_equator(decimal_latitude):
    distance = decimal_latitude*DEGREE_IN_KM
    return distance


# retrieves data using API GET calls, writes data to csv file
def get_data(locations):
    write_to_file(data_file, weather_headings)
    woeids = translate_woeids(locations)
    for i in range(len(locations)):
        woeid = woeids[i]
        yql_query = "select location, item.forecast from weather.forecast where woeid=" + woeid + " and u = 'C'"
        yql_url = baseurl + urllib.parse.urlencode({'q': yql_query}) + "&format=json"
        result = urllib.request.urlopen(yql_url).read()
        parsed_data = json.loads(result)

        latitude = get_latitude(locations[i])
        distance = distance_from_equator(DMS_to_DD(get_latitude(locations[i])))
        for x in range(forecast_days):
            data = []
            data.append(str(parsed_data['query']['results']['channel'][x]['location']['city']))
            data.append(str(parsed_data['query']['results']['channel'][x]['location']['country']))
            data.append(str(parsed_data['query']['results']['channel'][x]['item']['forecast']['date']))
            data.append(str(parsed_data['query']['results']['channel'][x]['item']['forecast']['high']))
            data.append(str(parsed_data['query']['results']['channel'][x]['item']['forecast']['low']))
            data.append(latitude)
            data.append(distance)
            write_to_file(data_file, data)


def read_from_csv(file_location):
    data = pd.read_csv(file_location)
    return data


# format the csv data into a sorted panda table with headings
def panda_table_formatter(data, data_headings, param):
    formatted_data = data[data_headings]
    formatted_data = formatted_data.sort_values(by=[param])
    return formatted_data


# returns the day(s) when the temperature in highest for a given country
def get_day_max_temp(df, country):
    df = df[df['COUNTRY'] == country]
    df = (df.loc[df['HIGH-TEMP'] == df['HIGH-TEMP'].max()])
    return df


# returns the day(s) when the temperature in lowest for a given country
def get_day_min_temp(df, country):
    df = df[df['COUNTRY'] == country]
    df = (df.loc[df['LOW-TEMP'] == df['LOW-TEMP'].min()])
    return df


# returns the mean max daily temperature for a particular country
def get_mean_high_temp(df, country):
    df = df[df['COUNTRY'] == country]
    mean = df['HIGH-TEMP'].mean()
    return mean


def format_dates(df):
    dates = []
    for i in range(forecast_days):
        s = "-"
        day = df['DATE'][i].split(' ')[0]
        month = month_lookup[df['DATE'][i].split(' ')[1]]
        seq = (day, month)
        date = s.join(seq)
        dates.append(date)
    return dates



# get_data(locations)
data = read_from_csv(data_file)
# print(data)
formatted_headings = weather_headings
sort_parameter = 'HIGH-TEMP'

# format and print table
df = panda_table_formatter(data, formatted_headings, sort_parameter)


# Print the weather forecast for the next few days in Ireland
ireland = df[df['COUNTRY'] == 'Ireland']
ireland = panda_table_formatter(ireland, formatted_headings, 'DATE')
# print(ireland)
dates = format_dates(ireland)
plt.bar(dates, ireland['HIGH-TEMP'])
plt.title("Predicted High Temperatures in Ireland")
plt.ylabel("High Temperature")
plt.xlabel("Date")
plt.show()

# TODO Fix bug that occurs when the lowest date is different due to time zones
# Print the weather forecast for tomorrow for all countries
tomorrow_weather = df[df['DATE'] == df['DATE'].min()]
# print(tomorrow_weather)
plt.bar(tomorrow_weather['CITY'], tomorrow_weather['HIGH-TEMP'], width=0.5)
plt.title("Tomorrows weather in selected cities")
plt.ylabel("High Temperature")
plt.xlabel("City")
plt.show()


print('Max temperature across selected cities is %2.0f°C' % df['HIGH-TEMP'].max())
print('Min temperature across selected cities is %2.0f°C' % df['LOW-TEMP'].min())
df = (df.loc[df['LOW-TEMP'] == df['LOW-TEMP'].min()])
# print(df)


### select rows based on value in certain column
# print(df.loc[df['COUNTRY'] == 'Ireland'])
### select rows based on high-temp > 0
# print(df.loc[df['HIGH-TEMP'] > 0])
### isolate Ireland's data
# newdf = df[df['COUNTRY'] == 'Ireland']
# newdf = panda_table_formatter(newdf, formatted_headings, 'DATE')
# print(newdf)
# print(newdf['HIGH-TEMP'].mean())

#delete_file(data_file)