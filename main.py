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


print(type(networkData))
print(type(networkData[0]))
print("-----------")
""" print(type(packetsData))
print(type(packetsData[0])) """

switches = []

for s in networkData:
  switches.append(obj.Switch (s["switchName"], s["address"], s["connectedTo"]))

for s in switches:
  print(s)


print(type(networkData[0]["connectedTo"]))
print(networkData[0]["connectedTo"])

