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

logging.info("Network data:")
for i in networkData:
  logging.info(i)

# Update average time in milliseconds
updateDelta = timedelta(milliseconds=100)
# The considered average time in seconds
averageDelta = timedelta(seconds=1)


# Setting the starting time point
startTime = datetime(2024, 1, 1, 0, 0, 0)

timeWalker = startTime

averageFractions = int(averageDelta / updateDelta)
lastFirstUDindex = averageFractions
logging.info(f"lastFirstUDindex: {lastFirstUDindex}")

iterator = iter(packetsData)

# Defining the amount of simulation time in seconds
simTime = timedelta(seconds=60)

# Initializing temporary variable about links averages sums
linksTemp = []

# updateDeltaTraffic rappresenta tutte le unità frazionarie di secondo date da updatedelta, esempio 60 secondi divisi per 100 ms sono 600 unità frazionarie
# traffic rappresenta la somma dei bytes in un tempo averageDelta, quindi il primo valore parte dopo le prime averageFractions unità temporali e finisce prima delle ultime averageFraction unità temporali
for link in links:
  linksTemp.append({"linkId": link.linkId, "trafficDT":0, "trafficUDT":0, "updateDeltaTraffic": [], "traffic": []})

logging.info("LinksTemp structure:")
for i in linksTemp:
  logging.info(i)

packet = next(iterator, None)
# Calculating averages

#Ogni loop è un'unità frazionaria analizzata
while timeWalker <= startTime + (simTime - updateDelta):
  # Per ogni updateDelta azzeriamo pesi
  for linkTemp in linksTemp:
    linkTemp["trafficUDT"] = 0
  # Individuo link di appartenenza al packet analizzato
  if packet is not None:
    link = utils.getLink(links, packet["source"], packet["destination"])
    linkTemp = utils.getLinkTempById(linksTemp, link.linkId)
  else:
    break

  while packet["timestamp"] >= timeWalker and packet["timestamp"] < timeWalker + updateDelta:
    linkTemp["trafficUDT"] += packet["dimension"]
    linkTemp["trafficDT"] += packet["dimension"]
    packet = next(iterator, None)
    if packet is not None:
      link = utils.getLink(links, packet["source"], packet["destination"])
      linkTemp = utils.getLinkTempById(linksTemp, link.linkId)
    else:
      break
  


  timeWalker += updateDelta

  for linkTemp in linksTemp:
    linkTemp["updateDeltaTraffic"].append({"updateTime": timeWalker, "traffic": linkTemp["trafficUDT"]})

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

    