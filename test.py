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
import requests
import scipy
import math


# google_maps_api = "AIzaSyADj82WQ-2GlwwyGLO5z5KHoE0OID3HKiQ"
# google_maps_api_url = 'https://maps.googleapis.com/maps/api/geocode/json'
#
# locations = ["Dublin, Ireland", "London, England", "Paris, France", "Berlin, Germany", "Stockholm, Sweden", "Moscow, Russia", "Tokyo, Japan", "Sydney, Australia", "New York City, United States", "Los Angeles, United States"]
# lat = []
#
# #test_url = 'https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=AIzaSyADj82WQ-2GlwwyGLO5z5KHoE0OID3HKiQ'
#
# for location in locations:
#     params = {
#         'address': location,
#         'sensor' : 'false',
#         'key' : google_maps_api
#     }
#     req = requests.get(google_maps_api_url, params=params)
#     res = req.json()
#
#     result = res['results'][0]
#     print(result)
#     lat.append(round(result['geometry']['location']['lat'],2))
#
# print(lat)


dublin_lat =  37.26

split_lat = str(dublin_lat).split('.')
degree = int(split_lat[0])
minute = int(split_lat[1])

print(degree)
print(minute)

decimal_latitude = degree + round((minute/60), 2)
print(decimal_latitude)


#
# rads = decimal_latitude*(scipy.pi/180)
rads = math.cos(math.radians(decimal_latitude))
print(rads)



