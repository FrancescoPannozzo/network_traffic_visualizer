import argparse
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

startTime = packetsData[0]["timestamp"]

