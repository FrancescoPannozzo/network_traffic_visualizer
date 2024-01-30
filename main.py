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

# Data loaded are "list of list of dictionaries" for both files

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

logging.info("Network data:")
for i in networkData:
  logging.info(i)

# Range times parameters (must be equal to parameters used in configGen.py script)
# Update average time in milliseconds
updateDelta = timedelta(milliseconds=100)
# The considered average time in seconds
averageDelta = timedelta(seconds=1)


# Setting the starting time point, (must be equal to parameters used in configGen.py script)
startTime = datetime(2024, 1, 1, 0, 0, 0)
# The analyzed time
timeWalker = startTime
# Number of fractional units per averageDelta
averageFractions = int(averageDelta / updateDelta)
# The number of fractional units needed to get the first fractional unit of the last averageDelta
# starting from the last element of the list updateDeltaTraffic in the in the linksTemp auxiliary structure
lastFirstUDindex = averageFractions
logging.info(f"lastFirstUDindex: {lastFirstUDindex}")

iterator = iter(packetsData)

# Defining the amount of simulation time in seconds (must be equal to the simulation time value used in configGen.py script)
simTime = timedelta(seconds=60)

# Initializing temporary variable about links averages sums
linksTemp = []

# updateDeltaTraffic list represents all fractional units of seconds given by updatedelta, for example 60 seconds divided by 100 ms is 600 fractional units
# traffic list represents the sum of bytes in an averageDelta time
# Each list element is a dictionary in the form {"updateTime":value, "traffic":value} with
# "updateTime" meaning the recorded timestamp and "traffic" the packets bytes sum
for link in links:
  linksTemp.append({"linkId": link.linkId, "trafficDT":0, "trafficUDT":0, "updateDeltaTraffic": [], "traffic": []})

logging.info("LinksTemp structure:")
for i in linksTemp:
  logging.info(i)
# Taking fist packet to analyze
packet = next(iterator, None)

# Calculating averages
# Every loop is an analyzed fractional unit
while timeWalker <= startTime + (simTime - updateDelta):
  # For each updateDelta reset values
  for linkTemp in linksTemp:
    linkTemp["trafficUDT"] = 0
  # Identify the link belonging to the analyzed packet
  if packet is not None:
    link = utils.getLink(links, packet["source"], packet["destination"])
    linkTemp = utils.getLinkTempById(linksTemp, link.linkId)
  else:
    break
  # Analyzing every packet in the analyzed range
  while packet["timestamp"] >= timeWalker and packet["timestamp"] < timeWalker + updateDelta:
    linkTemp["trafficUDT"] += packet["dimension"]
    linkTemp["trafficDT"] += packet["dimension"]
    packet = next(iterator, None)
    if packet is not None:
      link = utils.getLink(links, packet["source"], packet["destination"])
      linkTemp = utils.getLinkTempById(linksTemp, link.linkId)
    else:
      break
  # Pushing forward the analyzing time
  timeWalker += updateDelta
  # Storing the fractional time units values
  for linkTemp in linksTemp:
    linkTemp["updateDeltaTraffic"].append({"updateTime": timeWalker, "traffic": linkTemp["trafficUDT"]})

  # Storing the averageDelta units value
  if timeWalker >= startTime + averageDelta:
    for linkTemp in linksTemp:
      linkTemp["trafficDT"] = linkTemp["trafficDT"] - linkTemp["updateDeltaTraffic"][ (len(linkTemp["updateDeltaTraffic"]) - 1) - lastFirstUDindex ]["traffic"]
      linkTemp["traffic"].append({"updateTime": timeWalker, "traffic": linkTemp["trafficDT"]})


for linkTemp in linksTemp:
  logging.debug(f"linkID: {linkTemp["linkId"]}")
  logging.debug("updateDeltaTraffic[]:")
  for i in linkTemp["updateDeltaTraffic"]:
     logging.debug(i)
  logging.debug("traffic[]:")
  for i in linkTemp["traffic"]:
     logging.debug(i)

    