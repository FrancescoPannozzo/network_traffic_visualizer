import argparse
from datetime import timedelta
from datetime import datetime
import logging
import os
from network_traffic_visualizer import classes as obj
from network_traffic_visualizer import utils

# Logger config
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('log_file.txt', mode='w'),  # Adding one handler to manage the messages on a file
        logging.StreamHandler()  # Adding one handler to see messages on console
    ]
)

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
""" startTimeRange = packetsData[0]["timestamp"] """
startTimeRange = datetime(2024, 1, 1, 0, 0, 0)
# Update average time in milliseconds
updateDelta = timedelta(milliseconds=100)
# The considered average time in seconds
averageDelta = timedelta(seconds=1)

# Initializing temporary variable about links averages sums
linksTemp = []

for link in links:
  linksTemp.append({"linkId": link.linkId, "trafficDT":0, "trafficUDT":0, "updateDeltaTraffic": [], "traffic": []})

for i in linksTemp:
  print(i)

timeWalker = startTimeRange

lastFirstUDindex = (averageDelta / updateDelta) + 1

# Calculating averages
for packet in packetsData:
  """ logging.info(f"Analyzing packet: {packet}") """
  link = utils.getLink(links, packet["source"], packet["destination"])
  linkTemp = utils.getLinkTempById(linksTemp, link.linkId)

  if packet["timestamp"] >= timeWalker and packet["timestamp"] < (timeWalker + updateDelta):
    linksTemp["trafficDT"] += packet["dimension"]
    linksTemp["trafficUDT"] += packet["dimension"]
    timeWalker += updateDelta
  else:
    linkTemp["updateDeltaTraffic"].append(linkTemp["trafficUDT"])
    linksTemp["trafficUDT"] = 0
    if packet["timestamp"] >= (startTimeRange + averageDelta):
      startTimeRange = timeWalker
      lastFirstDelta = linkTemp["updateDeltaTraffic"][len(linkTemp["updateDeltaTraffic"] - lastFirstUDindex)]
      linkTemp["trafficDT"] = linkTemp["trafficDT"] - lastFirstDelta
      linkTemp["traffic"].append(linkTemp["trafficDT"])
    timeWalker += updateDelta