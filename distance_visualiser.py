import csv
import datetime

import matplotlib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

# Sample telemetry data
times = []
data = []

day = datetime.date(2024, 5, 15)

# Visualize Position Data
fig = plt.figure()

def exponential_moving_average(s, n):
    """
    returns an n period exponential moving average for
    the time series s

    s is a list ordered from oldest (index 0) to most
    recent (index -1)
    n is an integer

    returns a numeric array of the exponential
    moving average
    """
    ema = []
    j = 1

    #get n sma first and calculate the next n period ema
    sma = sum(s[:n]) / n
    multiplier = 2 / float(1 + n)
    ema.append(sma)

    #EMA(current) = ( (Price(current) - EMA(prev) ) x Multiplier) + EMA(prev)
    ema.append(( (s[n] - sma) * multiplier) + sma)

    #now calculate the rest of the values
    for i in s[n+1:]:
        tmp = ( (i - ema[j]) * multiplier) + ema[j]
        j = j + 1
        ema.append(tmp)

    for i in range(n - 1):
        ema.append(ema[-1])

    return ema

def moving_average(arr):
    window_size = 3

    i = 0
    # Initialize an empty list to store moving averages
    moving_averages = []

    # Loop through the array to consider
    # every window of size 3
    while i < len(arr) - window_size + 1:
        # Store elements from i to i+window_size
        # in list to get the current window
        window = arr[i: i + window_size]

        # Calculate the average of current window
        window_average = round(sum(window) / window_size, 2)

        # Store the average of current
        # window in moving average list
        moving_averages.append(window_average)

        # Shift window to right by one position
        i += 1
    for i in range(window_size - 1):
        moving_averages.append(moving_averages[-1])
    return moving_averages

with open('./LOGS/distance_sensor/2024-09-12--16-01-55.log','r') as f_input:
    csv_input = csv.reader(f_input, delimiter=' ', skipinitialspace=True)
    x = []
    y = []
    for cols in csv_input:
        x.append(matplotlib.dates.datestr2num(cols[0]))
        y.append(float(cols[1]))

# naming the x axis
plt.xlabel('Time')
# naming the y axis
plt.ylabel('Distance, cm')
# giving a title to my graph
plt.title('Sound distance')
# plotting the points
plt.plot(x, y)
plt.plot(x, moving_average(y), '-g')
plt.plot(x, exponential_moving_average(y, 5))
plt.legend(['Distance', 'Moving average', 'Exponential moving average'])
# beautify the x-labels
plt.gcf().autofmt_xdate(rotation=90)
# function to show the plot
plt.show()
