# -*- coding: utf-8 -*-
import os
import csv
import urllib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy
import urllib.request
import json
import yweather
import time
import csv

##############
# parameters #
##############
baseurl = "https://query.yahooapis.com/v1/public/yql?"
client = yweather.Client()
locations = ["Dublin, Ireland", "London, England", "Paris, France", "Berlin, Germany", "Stockholm, Sweden", "Moscow, Russia", "Tokyo, Japan", "Sydney, Australia", "New York City, United States", "Los Angeles, United States"]
weather_headings = ["CITY", "COUNTRY", "DATE", "HIGH-TEMP", "LOW-TEMP"]
locations_woeid = []

data_file = "weather_data.csv"
forecast_days = 10


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
    for location in locations:
        locations_woeid.append(client.fetch_woeid(location))

        # need a slight delay to not overload client call
        time.sleep(0.5)
    return locations_woeid


# retrieves data using API GET calls, writes data to csv file
def get_data(locations):
    write_to_file(data_file, weather_headings)
    for i in range(len(locations)):
        x = locations_woeid[i]
        yql_query = "select location, item.forecast from weather.forecast where woeid=" + x + " and u = 'C'"
        yql_url = baseurl + urllib.parse.urlencode({'q': yql_query}) + "&format=json"
        result = urllib.request.urlopen(yql_url).read()
        parsed_data = json.loads(result)

        for x in range(forecast_days):
            data = []
            data.append(str(parsed_data['query']['results']['channel'][x]['location']['city']))
            data.append(str(parsed_data['query']['results']['channel'][x]['location']['country']))
            data.append(str(parsed_data['query']['results']['channel'][x]['item']['forecast']['date']))
            data.append(str(parsed_data['query']['results']['channel'][x]['item']['forecast']['high']))
            data.append(str(parsed_data['query']['results']['channel'][x]['item']['forecast']['low']))
            write_to_file(data_file, data)
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




translate_woeids(locations)
get_data(locations)
data = read_from_csv(data_file)
formatted_headings = ["COUNTRY", "CITY", "DATE", "HIGH-TEMP", "LOW-TEMP"]
sort_parameter = 'HIGH-TEMP'

# format and print table
df = panda_table_formatter(data, formatted_headings, sort_parameter)
print(df[0:len(df)])


countries = df


print('Max temperature anywhere today is %2.0f°C' % df['HIGH-TEMP'].max())
print('Min temperature anywhere today is %2.0f°C' % df['LOW-TEMP'].min())

# select rows based on value in certain column
print(df.loc[df['COUNTRY'] == 'Ireland'])

# select rows based on high-temp > 0
print(df.loc[df['HIGH-TEMP'] > 0])

# isolate Ireland data
newdf = df[df['COUNTRY'] == 'Ireland']
newdf = panda_table_formatter(newdf, formatted_headings, 'DATE')
print(newdf)
print(newdf['HIGH-TEMP'].mean())


newdf = get_day_max_temp(newdf, 'Ireland')
print(newdf)

delete_file(data_file)