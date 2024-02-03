from datetime import datetime, timedelta, time


linkCap = 100
packetSize = 1518

pps = int(((linkCap * 1e6) / 8) / packetSize)

print(pps)

# Defining the simulation start time point
startTime = datetime(2024, 1, 1, 0, 0, 0)

# Defining the simulation time in seconds
simTime = 60
# Defining the pps creation rate delta time (milliseconds)
ppsDelta = 100
ppsInterval = timedelta(milliseconds=ppsDelta)
# Defining the traffic percentage variation, delta time (seconds)
trafficPercDelta = 1
trafficPercInterval = timedelta(seconds=trafficPercDelta)

creationRate = int(timedelta(seconds=trafficPercDelta)/timedelta(milliseconds=ppsDelta))

print(int(pps/creationRate))
print("-----")

links = [{"capacity":10, "endpoints":["switch1", "switch2"]},{"capacity":10, "endpoints":["switch1", "switch3"]}]
linksTemp = {}

print(links[0]["endpoints"][0])
cont = 0
for l in links:
  fs = frozenset({l["endpoints"][0], l["endpoints"][1]})
  linksTemp[fs] = {"key1":cont, "key2":cont}
  cont+=1


print(linksTemp)

print(linksTemp[frozenset({"switch3", "switch1"})]["key1"])

linksTemp[frozenset({"switch3", "switch1"})]["key1"] = 100

print(linksTemp[frozenset({"switch3", "switch1"})]["key1"])

print("-----")
seasons = ["Spring", "Summer", "Fall", "Winter"]

for i, season in enumerate(seasons):
    print(i, season)

print("-----")

ORCHESTRA = {
    "violin": {"feature":"strings", 
               "sound":"fiiiii"},
    "gong": {"feature":"strings",
                "sound":"GONG"}
}


for instrument, features in ORCHESTRA.items():
    fii = features["sound"]
    print(f"{instrument}: {fii}")