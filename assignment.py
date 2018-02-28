import os
import csv
import urllib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy
import json
import urllib.parse
import urllib.request
import json
import yweather
import time
import csv



baseurl = "https://query.yahooapis.com/v1/public/yql?"
client = yweather.Client()

locations = ["Dublin, Ireland", "London, England", "Paris, France", "Berlin, Germany", "Stockholm, Sweden", "Moscow, Russia", "Tokyo, Japan", "Sydney, Australia", "New York City, United States", "Los Angeles, United States"]
locations_woeid = []
weather_headings = ["country", "city", "data", "highTemp", "lowTemp"]


data_file = "weather_data.csv"

def create_file(file_location, date_headings):
    with open(file_location, 'w') as write_file:
        f = csv.writer(write_file)
        f.writerow(date_headings)
    write_file.close()


def write_to_file(file_location, data):
    with open(file_location, 'a') as write_file:
        f = csv.writer(write_file, delimiter=",", dialect='excel')
        f.writerow(data)
    write_file.close()


# get woeid (where on earth ID) from location names
for location in locations:
    locations_woeid.append(client.fetch_woeid(location))

    # need a slight delay to not overload client call
    time.sleep(0.5)
print(locations_woeid)


for i in range(len(locations)):
    data = []
    print(i)
    x = locations_woeid[i]
    yql_query = "select location, item.forecast from weather.forecast where woeid=" + x + " and u = 'C'"
    yql_url = baseurl + urllib.parse.urlencode({'q':yql_query}) + "&format=json"
    result = urllib.request.urlopen(yql_url).read()
    parsed_data = json.loads(result)

    city = parsed_data['query']['results']['channel'][0]['location']['city']
    data.append(str(city))

    country = parsed_data['query']['results']['channel'][0]['location']['country']
    data.append(str(country))

    date = parsed_data['query']['results']['channel'][0]['item']['forecast']['date']
    data.append(str(date))

    high_temp = (parsed_data['query']['results']['channel'][0]['item']['forecast']['high'])
    data.append(str(high_temp))

    low_temp = (parsed_data['query']['results']['channel'][0]['item']['forecast']['low'])
    data.append(str(low_temp))

    # diff_temp = abs(high_temp - low_temp)
    # data.append(diff_temp)

    print(data)

    write_to_file(data_file, data)


    print(parsed_data['query']['results']['channel'][0]['location']['city'], parsed_data['query']['results']['channel'][0]['location']['country'], parsed_data['query']['results']['channel'][0]['item']['forecast']['date'], parsed_data['query']['results']['channel'][0]['item']['forecast']['high'], parsed_data['query']['results']['channel'][0]['item']['forecast']['low'])
