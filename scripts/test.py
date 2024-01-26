from datetime import timedelta
from datetime import datetime


startTimeRange = datetime(2024, 1, 1, 0, 0, 0)
simTime = timedelta(seconds=60)
updateDelta = timedelta(milliseconds=100)
print(startTimeRange + simTime)
print("-------------")
print(simTime // updateDelta)
print("-------------")

# Update average time in milliseconds
updateDelta = timedelta(milliseconds=100)
# The considered average time in seconds
averageDelta = timedelta(seconds=1)

averageFractions = int(averageDelta / updateDelta)

# Defining the amount of simulation time in seconds
simTime = timedelta(seconds=60)

print((simTime // updateDelta) - averageFractions * 2)