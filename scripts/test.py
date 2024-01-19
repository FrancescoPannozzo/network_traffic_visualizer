from datetime import timedelta


connectedTo = ["s1", "s2"]

switch = {
  "connectedTo": connectedTo
}

print(switch)
print(type(switch["connectedTo"]))

data = [[],[]]
data[0].append({"endpoints": ["link1", "link2"],
             "linkcap": 10})
data[0].append({"endpoints": ["link1", "link3"],
             "linkcap": 20}
             )

data[1].append({"name": "switch1",
                "address": "123.123.123.123"})

data[1].append({"name": "switch2",
                "address": "123.123.123.124"}
              )

for i in data:
  print(i)

packetSize = 1518
# Packets Per Seconds
ppsint = int(((10 * 1e6) / 8) / packetSize)
pps = ((10 * 1e6) / 8) / packetSize

print(ppsint)
print(pps)
print(1e6)

print("-------------")

updateDelta = timedelta(milliseconds=100)
# The considered average time in seconds
averageDelta = timedelta(seconds=1)

print(int(averageDelta / updateDelta))

print("--------")
rate = 10
source = []
result = []

for i in range(0, 30):
  source.append(i)

print(source)

print("--------")
for i in range(0, 30):
  if( i % rate == 0):
    if i > 1:
      result.append(source[i-rate+1])
  else:
    result.append(source[i])

print(result)