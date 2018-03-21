# -*- coding: utf-8 -*-
import os
import urllib
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import urllib.request
import json
import yweather
import time
import csv
import requests
import numpy as np

##############
# parameters #
##############
matplotlib.rcParams.update({'font.size': 6})  #Sets plot font size to small to accomodate a large amount of data
data_file = "weather_data.csv"                #File to write csv values to
baseurl = "https://query.yahooapis.com/v1/public/yql?"
client = yweather.Client()
google_maps_api = "AIzaSyADj82WQ-2GlwwyGLO5z5KHoE0OID3HKiQ"
google_maps_api_url = 'https://maps.googleapis.com/maps/api/geocode/json'

# locations = ["Dublin, Ireland", "London, England", "Paris, France", "Berlin, Germany", "Stockholm, Sweden", "Moscow, Russia", "Tokyo, Japan", "Honolulu, United States", "New York, United States", "San Diego, United States", "Nairobi, Kenya", "Masovian, Poland", "Helsinki, Poland"]"
locations = ["Dublin", "Paris", "Moscow", "Dubai", "Sydney", "Mumbai", "Accra", "Berlin", "Stockholm", "Tokyo", "New York", "San Diego", "Honolulu", "Singapore", "Lagos", "Phuket", "Pattaya", "Dakar" , "Mecca", "Hong Kong", "Riyadh", "Orlando", "New Orleans", "Dallas", "Seoul",
             "Athens", "Lisbon", "Pyongyang", "Beijing", "Istanbul", "Chicago", "Cannes", "Bucharest", "Montreal", "Budapest", "Prague",  "Narvik", "Eureka", "Hammerfest","Fairbanks"]

weather_headings = ["CITY", "COUNTRY", "DATE", "HIGH-TEMP", "LOW-TEMP", "LATITUDE", "DISTANCE"]
month_lookup = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07',
                'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
forecast_days = 10
DEGREE_IN_KM = 111.11


#########################
#       Functions       #
#########################

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
        print(parsed_data)

        latitude = get_latitude(locations[i])
        print(locations[i], latitude)
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


# format the csv data into a sorted panda table with headings
def panda_table_formatter(data, data_headings, param, asc=True):
    formatted_data = data[data_headings]
    formatted_data = formatted_data.sort_values(by=[param], ascending=asc)
    return formatted_data


# returns the day(s) when the temperature in highest for a given country
def get_days_max_temp(df, city):
    df = df[df['CITY'] == city]
    df = (df.loc[df['HIGH-TEMP'] == df['HIGH-TEMP'].max()])
    return df


# returns the day(s) when the temperature in lowest for a given country
def get_days_min_temp(df, city):
    df = df[df['CITY'] == city]
    df = (df.loc[df['LOW-TEMP'] == df['LOW-TEMP'].min()])
    return df


# returns the mean max daily temperature for a particular country
def get_mean_high_temp(df, city):
    df = df[df['CITY'] == city]
    mean = df['HIGH-TEMP'].mean()
    return mean

# function to format dates [01-Mar-18 to 01-03]
def format_dates(df, it=forecast_days):
    dates = []
    for i in range(it):
        s = "-"
        day = df['DATE'][i].split(' ')[0]
        month = month_lookup[df['DATE'][i].split(' ')[1]]
        seq = (day, month)
        date = s.join(seq)
        dates.append(date)
    return dates


# truncate the city names so the barchart isnt cluttered
def truncate_names(df):
    city_names = df['CITY'].tolist()
    print(city_names)
    for i, city in enumerate(city_names):
        city = city[0:3]
        city_names[i] = city
    return city_names


##################
#     Main       #
##################

# get_data(locations)
data = pd.read_csv(data_file)
# print(data)


# format and print table
df = panda_table_formatter(data, weather_headings, 'HIGH-TEMP', False)
# print(df)



######################################################
# Mean Temperature per City vs Distance from Equator #
######################################################
mean_high_temps = []
for i in range(len(locations)):
    mean_high_temps.append(get_mean_high_temp(df, locations[i]))
    distances = data[['DISTANCE']]
    distances = distances.drop_duplicates()
    distances = distances['DISTANCE'].tolist()
df_dist = pd.DataFrame({'DIST': distances, 'TEMP': mean_high_temps})

print(distances)
print(mean_high_temps)

test_df = pd.DataFrame({'COUNTRY': locations, 'DIST': distances, 'TEMP': mean_high_temps})
print(test_df)

plt.scatter(df_dist['DIST'], df_dist['TEMP'])
plt.plot(np.unique(distances), np.poly1d(np.polyfit(distances, mean_high_temps, 1))(np.unique(distances)), color='r')
plt.title("Mean High Temperature vs Distance from Equator")
plt.ylabel("Mean High Temperature for the forecasted days (°C)")
plt.xlabel("Distance from equator (km)")
plt.show()

#delete_file(data_file)