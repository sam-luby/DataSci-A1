import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy


format = json

# 10 cities, including Dublin as reference
locations = ["Dublin", "New York", "Los Angeles", "Las Vegas", "San Francisco", "Denver", "Chicago",  "Vancouver", "Toronto", "Montreal"]

# 5 parameters I deemed important to look at hourly
hourly_headings = ["time", "tempC", "FeelsLikeC", "precipMM", "humidity"]


# 5 parameters I deemed important to look at daily
daily_headings = ["date", "maxtempC", "mintempC", "sunHour", "totalSnow_cm"]

# parameters I deemed important to look at monthly
monthly_headings = ["warmestDay", "coldestDay", "daysWithRain", "daysWithSnow"]

