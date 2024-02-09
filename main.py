""" 
Data loader

Description:
    The script load data from network.yaml and packets.yaml and 
    calculates the payloads sums (bytes) for every updateDeltaTime in the
    time simulation and the average in delta time, updated every updateDeltaTime
Usage: 
    launch the script: python main.py switches_number link_capacity_number
    help: python main.py -h 
Author: Francesco Pannozzo
"""
import argparse
from datetime import timedelta
import logging
from network_traffic_visualizer import classes as obj
from network_traffic_visualizer import utils

# Logger config
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        # Adding one handler to manage the messages on a file
        logging.FileHandler('log_file.txt', mode='w'),
        # Adding one handler to see messages on console
        logging.StreamHandler()
    ]
)

# Setting the command line option to load the network config file and the packets file
parser = argparse.ArgumentParser()
parser.add_argument("networkFile", help="The networkFile you want to load")
parser.add_argument("packetsFile", help="The packetsFile you want to load")
args = parser.parse_args()

logging.info("Loading files..")
# networkData:list composed by a link dict, a switch list and network parameters dict
# packetsData:composed by a packets dict
networkData, packetsData = utils.file_loader(args.networkFile, args.packetsFile)


switches = []
LINK_INDEX = 0
SWITCH_INDEX = 1
SIM_PARAMETERS = 2

logging.info("Analyzing files..")

# links is an auxiliary structure, needed to perform the simulation calculations
links = {}
# updateDeltaTraffic list represents all traffic fractional units,
# for example 60 sim seconds divided by an update delta time 100 ms is 600 fractional units
# traffic list represents the sum of bytes in an averageDelta time
# "updateDeltaTraffic" and "traffic" list element is a dictionary in the form {"updateTime":value, "traffic":value} with
# "updateTime" meaning the recorded timestamp and "traffic" the packets bytes sum
FIRST_ENDPOINT = 0
SECOND_ENDPOINT = 1
# Extracting links data
for link, content in networkData[LINK_INDEX].items():
    links[frozenset({content["endpoints"][FIRST_ENDPOINT], content["endpoints"][SECOND_ENDPOINT]})] = {
        "linkID": link,
        "capacity": content["capacity"], 
        "trafficDT":0, 
        "trafficUDT":0, 
        "updateDeltaTraffic": [], 
        "traffic": []
        }

# Showing links with own endpoints
for link, content in links.items():
    logging.info("Link ID %s:", link)
    for endpoint in link:
        logging.info("endpoint: %s", endpoint)

logging.info("Simulation parameters:")
logging.info(networkData[SIM_PARAMETERS])

# Extracting switches data
for s in networkData[SWITCH_INDEX]:
    switches.append(obj.Switch (s["switchName"], s["address"]))

logging.info("Switches:")
for i in switches:
    logging.info(i)

# Range times parameters
# Update average delta time in milliseconds
UPDATE_DELTA_TIME = 100
updateDelta = timedelta(milliseconds=UPDATE_DELTA_TIME)
# The considered average time in seconds
AVG_DELTA_TIME = 1000
averageDelta = timedelta(milliseconds=AVG_DELTA_TIME)

# Setting the starting time point
startTime = networkData[SIM_PARAMETERS]["startSimTime"]
# The analyzed time
timeWalker = startTime
# Number of fractional units per averageDelta
averageFractions = int(averageDelta / updateDelta)

# The number of fractional units needed to get the first fractional unit of the last averageDelta
# starting from the last element of the updateDeltaTraffic list in the in the links
# auxiliary structure
lastFirstUDindex = averageFractions

packetsDataIterator = iter(packetsData)

# Defining the amount of simulation time in seconds
simTime = timedelta(seconds=networkData[SIM_PARAMETERS]["simTime"])

# Taking first packet to analyze
packet = next(packetsDataIterator, None)

# Calculating averages
# Every loop is an analyzed fractional unit
while timeWalker <= startTime + (simTime - updateDelta):
    # For each updateDelta reset values
    for link, content in links.items():
        content["trafficUDT"] = 0
    # Identify the link belonging to the analyzed packet
    if packet is not None:
        link = links[frozenset({packet["epA"], packet["epB"]})]
        # Analyzing every packet in the analyzed range
        while packet["timest"] >= timeWalker and packet["timest"] < timeWalker + updateDelta:
            link["trafficUDT"] += packet["dim"]
            link["trafficDT"] += packet["dim"]
            packet = next(packetsDataIterator, None)
            if packet is not None:
                link = links[frozenset({packet["epA"], packet["epB"]})]
            else:
                break
    # Pushing forward the analyzing time
    timeWalker += updateDelta
    # Storing the fractional time units values
    for link, content in links.items():
        content["updateDeltaTraffic"].append(
            {"updateTime": timeWalker, "traffic": content["trafficUDT"]}
        )

    # Storing the averageDelta units value
    # If the averageDelta average is not the first one
    if timeWalker > startTime + averageDelta:
        for link, content in links.items():
            # Calcolate the element index to subtract from `updateDeltaTraffic`
            index = (len(content["updateDeltaTraffic"]) - 1) - lastFirstUDindex
            # Traffic value to subtract from the averageTraffic
            traffic_to_subtract = content["updateDeltaTraffic"][index]["traffic"]
            content["trafficDT"] -= traffic_to_subtract
            content["traffic"].append({"updateTime": timeWalker, "traffic": content["trafficDT"]})
    # Else if the averageDelta average is the first one
    elif timeWalker == startTime + averageDelta:
        for link, content in links.items():
            content["traffic"].append({"updateTime": timeWalker, "traffic": content["trafficDT"]})


utils.show_updates_data(links)
utils.show_averages_data(links, updateDelta, averageFractions)

logging.info("Done!")
