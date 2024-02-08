""" Core script """
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
# networkData:composed by a link list, a switch list and network parameters
# packetsData:composed by a packets list
networkData, packetsData = utils.file_loader(args.networkFile, args.packetsFile)

# links is an auxiliary structure, needed to perform the simulation calculations
links = {}
switches = []
LINK_INDEX = 0
SWITCH_INDEX = 1
SIM_PARAMETERS = 2

logging.info("Analyzing files..")


logging.debug("networkData[LINK_INDEX] is type of: %s", type(networkData[LINK_INDEX]))
logging.debug("links: %s", networkData[LINK_INDEX])

# Extracting links data

# updateDeltaTraffic list represents all fractional units of seconds given by updatedelta,
# for example 60 seconds divided by 100 ms is 600 fractional units
# traffic list represents the sum of bytes in an averageDelta time
# Each list element is a dictionary in the form {"updateTime":value, "traffic":value} with
# "updateTime" meaning the recorded timestamp and "traffic" the packets bytes sum
FIRST_ENDPOINT = 0
SECOND_ENDPOINT = 1
for link, content in networkData[LINK_INDEX].items():
    links[frozenset({content["endpoints"][FIRST_ENDPOINT], content["endpoints"][SECOND_ENDPOINT]})] = {
        "linkID": content["linkID"],
        "capacity": content["capacity"], 
        "trafficDT":0, 
        "trafficUDT":0, 
        "updateDeltaTraffic": [], 
        "traffic": []
        }

# Showing links with own endpoints
for index, (link, content) in enumerate(links.items(), start=1):
    logging.info("Link ID %d:", link)
    for endpoint in link:
        logging.info(endpoint)

logging.info("Simulation parameters:")
logging.info(networkData[SIM_PARAMETERS])

# Extracting switches data
for s in networkData[SWITCH_INDEX]:
    switches.append(obj.Switch (s["switchName"], s["address"]))

logging.info("Switches:")
for i in switches:
    logging.info(i)

# Range times parameters
# Update average time in milliseconds
updateDelta = timedelta(milliseconds=100)
# The considered average time in seconds
AVG_DELTA_TIME = 1000
averageDelta = timedelta(milliseconds=AVG_DELTA_TIME)

# Setting the starting time point, (must be equal to parameters used in configGen.py script)
startTime = networkData[SIM_PARAMETERS]["startSimTime"]
# The analyzed time
timeWalker = startTime
# Number of fractional units per averageDelta
averageFractions = int(averageDelta / updateDelta)

# The number of fractional units needed to get the first fractional unit of the last averageDelta
# starting from the last element of the list updateDeltaTraffic in the in the linksTemp
# auxiliary structure
lastFirstUDindex = averageFractions

packetsDataIterator = iter(packetsData)

# Defining the amount of simulation time in seconds (must be equal to the
# simulation time value used in configGen.py script)
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
        link = links[frozenset({packet["source"], packet["destination"]})]
        # Analyzing every packet in the analyzed range
        while packet["timestamp"] >= timeWalker and packet["timestamp"] < timeWalker + updateDelta:
            link["trafficUDT"] += packet["dimension"]
            link["trafficDT"] += packet["dimension"]
            prevPacket = packet
            packet = next(packetsDataIterator, None)
            if packet is not None:
                link = links[frozenset({packet["source"], packet["destination"]})]
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

logging.debug("UpdateDeltaTraffic sums:")
for link, content in links.items():
    logging.debug("link: %s", link)
    for i in content["updateDeltaTraffic"]:
        logging.debug("updateTime: %s, packets sum: %d", i['updateTime'], i['traffic'])

timeUnitsPerSec = timedelta(seconds=1)/updateDelta
logging.debug("Traffic percetages:")
for link, content in links.items():
    logging.debug("link: %s", link)
    for i in content["traffic"]:
        # Max traffic per fractional unit
        maxTrafficPerUnit = ((content['capacity'] * 1e6) / 8) / timeUnitsPerSec
        logging.debug(
            "updateTime: %s, delta traffic: %d, percentage: %f %%",
            i['updateTime'],
            i['traffic'],
            utils.get_average(i['traffic'], averageFractions, maxTrafficPerUnit)
        )

logging.info("Done!")
