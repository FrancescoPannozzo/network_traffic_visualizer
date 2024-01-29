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

print("-------------")

diz = { "cd":1, "cd2":2, "cd3":[{"campo1": 1, "campo2":2}, {"campo1": 3, "campo2": 4}, {"campo1": 5, "campo2":6}]}


print(diz["cd3"][1]["campo2"])

lista = [1,2,3,4,5]
print(lista[len(lista)-1])