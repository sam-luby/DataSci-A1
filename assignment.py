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
matplotlib.rcParams.update({'font.size': 6})
data_file = "weather_data.csv"
baseurl = "https://query.yahooapis.com/v1/public/yql?"
client = yweather.Client()
google_maps_api = "AIzaSyADj82WQ-2GlwwyGLO5z5KHoE0OID3HKiQ"
google_maps_api_url = 'https://maps.googleapis.com/maps/api/geocode/json'

locations = ["Dublin, Ireland", "London, England", "Paris, France", "Berlin, Germany", "Stockholm, Sweden", "Moscow, Russia", "Tokyo, Japan", "Honolulu, United States", "New York, United States", "San Diego, United States", "Nairobi, Kenya", "Masovian, Poland", "Helsinki, Poland"]
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



##################
#     Main       #
##################

# get_data(locations)
data = read_from_csv(data_file)
print(data)
formatted_headings = weather_headings
sort_parameter = 'HIGH-TEMP'

# format and print table
df = panda_table_formatter(data, formatted_headings, sort_parameter)
# print(df)

print('Max temperature across selected cities is %2.0f°C' % df['HIGH-TEMP'].max())
print('Min temperature across selected cities is %2.0f°C' % df['LOW-TEMP'].min())

# Print the weather forecast for the next few days in Ireland
ireland = df[df['COUNTRY'] == 'Ireland']
ireland = panda_table_formatter(ireland, formatted_headings, 'DATE')
# print(ireland)
dates = format_dates(ireland)
plt.bar(dates, ireland['HIGH-TEMP'], color='g')
plt.title("Predicted High Temperatures in Ireland")
plt.ylabel("High Temperature")
plt.xlabel("Date")
plt.show()


# TODO Fix bug that occurs when the lowest date is different due to time zones
#######################################
# Tomorrow's forecast for all cities #
#######################################
tomorrow_weather = df[df['DATE'] == df['DATE'].min()]
# print(tomorrow_weather)
plt.bar(tomorrow_weather['CITY'], tomorrow_weather['HIGH-TEMP'], width=0.5)
plt.title("Tomorrows weather in selected cities")
plt.ylabel("High Temperature")
plt.xlabel("City")
plt.show()


#################################
#  Temperature Range per city   #
#################################
temperature_ranges = []
cities = []
for i in range(len(locations)):
    cities.append(locations[i].split(',')[0])
    df_city = df[df['CITY'] == cities[i]]
    max_temp = df_city['HIGH-TEMP'].max()
    min_temp = df_city['LOW-TEMP'].min()
    temperature_ranges.append(max_temp-min_temp)

plt.bar(cities, temperature_ranges, width = 0.5)
plt.title("Temperature Ranges for selected cities")
plt.ylabel("Temperature Range")
plt.xlabel("City")
plt.show()


#######################################################
# Which days are hottest on average for all countries #
#######################################################
hottest_days = []
for i in range(len(locations)):
    # df_city = df[df['CITY'] == cities[i]]
    max_temp_days = get_days_max_temp(df, cities[i])

    # select the earliest date that the high temperatures occur, since we can assume predictions are more accurate
        # the closer to the date
    hottest_days.append(max_temp_days.iloc[0])
hottest_days = pd.DataFrame(hottest_days)

# Add an occurrences column to the dataframe to count which days are hottest on average in all countries
hottest_days = (pd.DataFrame(hottest_days['DATE'])).reset_index(drop=True)
hottest_days['OCCURRENCES'] = hottest_days.groupby('DATE')['DATE'].transform('count')
hottest_days.drop_duplicates(inplace=True)

# sort dates properly
hottest_days.sort_values(by='DATE', inplace=True, ascending=True)
hottest_days.reset_index(drop=True, inplace=True)

# format dates in dataframe
dates = hottest_days[['DATE']]
dates_fmt = format_dates(dates, len(dates))
hottest_days[['DATE']] = dates_fmt

matplotlib.rcParams.update({'font.size': 10})
plt.bar(hottest_days['DATE'], hottest_days['OCCURRENCES'], width=0.5)
plt.title("Hottest Days on Average")
plt.ylabel("Date")
plt.xlabel("Occurrences")
plt.show()


######################################################
# Mean Temperature per City vs Distance from Equator #
######################################################
mean_high_temps = []
for i in range(len(locations)):
    mean_high_temps.append(get_mean_high_temp(df, cities[i]))
    distances = data[['DISTANCE']]
    distances = distances.drop_duplicates()
    distances = distances['DISTANCE'].tolist()

# distances = [ '%.2f' % x for x in distances]
print(mean_high_temps)
print(distances)

# plt.plot(distances)
# plt.plot(mean_high_temps)
plt.scatter(distances, mean_high_temps)
plt.plot(np.unique(distances), np.poly1d(np.polyfit(distances, mean_high_temps, 1))(np.unique(distances)), color='r')
plt.title("Mean High Temperature vs Distance from Equator")
plt.ylabel("Mean High Temperature for the forecasted days (°C)")
plt.xlabel("Distance from equator (km)")
plt.show()

#delete_file(data_file)