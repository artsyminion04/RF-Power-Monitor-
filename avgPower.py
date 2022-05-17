import csv
import pandas as pd
import matplotlib.pyplot as plt

# freq range for calculating averages
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

lowerBound = 739000000
upperBound = 749000000

file_name = 'tenMinute.csv'
# get csv files
file = open(file_name, 'r')
# remove header to iterate to data
data = csv.reader(file)
header = next(data)

# of points per inquiry
pts = 108

# looping variables
totalPower = 0
avgPower = []
time = []
counter = 0
prev = 0

# iterate through each row of data
for row in data:
    # check if we are still on the same time
    if counter < pts:
        # increment total dBM
        totalPower += float(row[2])
        prev = float(row[0])
        counter += 1
    else:
        # add avg Power and time to respective lists
        avgPower.append(totalPower/pts)
        time.append(prev)
        # the else statement is triggered because we've already moved on to the next row. we need to account for this by incrementing these variables
        # refreshes total power then sets it to our current rows dbm
        totalPower = float(row[2])
        counter = 1

#  last iteration does not get saved inside the for loop
avgPower.append(totalPower/pts)
time.append(prev)

# calculate average of average
average = sum(avgPower) / len(avgPower)
print(average)

# plot everything
plt.plot(time,avgPower, color='#cc4400', marker="o", mfc='w',mec='#cc4400') #old marker color #3399ffv
plt.axhline(y=average, color='r', linestyle='-')
plt.title(file_name + ": " + str(lowerBound) + " - " + str(upperBound))
plt.xlabel("time (s)")
plt.ylabel("Average Channel Power (dBm)")
plt.show()

