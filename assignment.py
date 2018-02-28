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

# client_ID = "dj0yJmk9NGIxN3VNS2plWXhLJmQ9WVdrOVRHaEVlVlJKTnpJbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD0zNA--"
# client_secret = "c3667c48ae6fc0700391e74993e9c37cfc296e21"

baseurl = "https://query.yahooapis.com/v1/public/yql?"
client = yweather.Client()

locations = ["Dublin, Ireland", "London, England", "Paris, France", "Berlin, Germany", "Stockholm, Sweden", "Moscow, Russia", "Tokyo, Japan", "Sydney, Australia", "New York City, United States", "Los Angeles, United States"]
locations_woeid = []


weather_data_file = open('WeatherData.csv', 'w')
csvwriter = csv.writer(weather_data_file)
count = 0

# get woeid (where on earth ID) from location names
for location in locations:
    locations_woeid.append(client.fetch_woeid(location))

    # need a slight delay to not overload client call
    time.sleep(0.5)
print(locations_woeid)


for i in range(len(locations)):
    x = locations_woeid[i]
    yql_query = "select location.city, item.forecast from weather.forecast where woeid=" + x + " and u = 'C'"
    yql_url = baseurl + urllib.parse.urlencode({'q':yql_query}) + "&format=json"
    result = urllib.request.urlopen(yql_url).read()
    data = json.loads(result)
    # print(data)
    
    print(data['query']['results']['channel'][0]['location']['city'], data['query']['results']['channel'][0]['item']['forecast']['date'], data['query']['results']['channel'][0]['item']['forecast']['high'],  data['query']['results']['channel'][0]['item']['forecast']['low'])

