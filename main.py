import argparse
from datetime import timedelta
import os
from network_traffic_visualizer import classes as obj
from network_traffic_visualizer import utils

# Setting the command line option to load the network config file and the packets file
parser = argparse.ArgumentParser()
parser.add_argument("networkFile", help="The networkFile you want to load")
parser.add_argument("packetsFile", help="The packetsFile you want to load")
args = parser.parse_args()

# Loading files
networkData, packetsData = utils.fileLoader(args.networkFile, args.packetsFile)

# Data loaded is a "list of list of dictionaries" form for both files

""" print(type(networkData))
print(type(networkData[0]))
print("-----------") """

links = []
switches = []
linkIndex = 0
switchIndex = 1

# Extracting links data
for link in networkData[linkIndex]:
  links.append(obj.Link(link["capacity"],link["endpoints"]))

# Extracting switches data
for s in networkData[switchIndex]:
  switches.append(obj.Switch (s["switchName"], s["address"], s["connectedTo"]))

""" print(type(networkData[0]["connectedTo"]))
print(networkData[0]["connectedTo"])

print(type(packetsData[0]["timestamp"]))
print(packetsData[1]["timestamp"]) """

for i in networkData:
  print(i)

# Setting the starting time point
startTimeRange = packetsData[0]["timestamp"]
# Update average time in milliseconds
updateDelta = timedelta(milliseconds=100)
# The considered average time in seconds
averageDelta = timedelta(seconds=1)

# Initializing temporary variable about links averages sums
linksTemp = []

for link in links:
  linksTemp.append({"linkId": link.linkId, "tempSum": 0})

timeWalker = startTimeRange 

# Calculating the first average
for packet in packetsData:
  if packet["timestamp"] > (startTimeRange + averageDelta):
    break
  link = utils.getLink(links, packet["source"], packet["destination"])
  utils.addLinkTempSum(links, link.linkId, packet["dimension"])


for linkTemp in linksTemp:
  link = utils.getLinkById(links, linkTemp["linkId"])
  average = (linkTemp["tempSum"] * 100) / ((link.linkCap * 1e6) / 8)
  link.timeAverages.append(average)


for l in linkTemp:
  print(l)
