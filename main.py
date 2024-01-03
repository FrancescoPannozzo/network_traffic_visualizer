import argparse
import os
import json
from network_traffic_visualizer import classes as obj
from network_traffic_visualizer import utils

#STARTING POINT

#Setting the command line option to load the network config file and the packets file
parser = argparse.ArgumentParser()
parser.add_argument("networkFile", help="The networkFile you want to load")
parser.add_argument("packetsFile", help="The packetsFile you want to load")
args = parser.parse_args()

#Loading files
networkFile, packetsFile = utils.fileLoader(args.networkFile, args.packetsFile)

print(networkFile[0])
print("-----")
print(packetsFile[0])

print(type(networkFile))
print(type(networkFile[0]))

