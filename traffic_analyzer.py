""" 
Traffic analyzer

Description:
    The script load data from network.yaml and packets.yaml and 
    calculates the payloads sums (bytes) for every updateDeltaTime in the
    time simulation and the averages in delta time, updated every updateDeltaTime
"""

from datetime import timedelta
import logging
import yaml
from utils import utils
from utils import CONSTANTS as CONST
import sys

# Logger config
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        # Adding one handler to manage the messages on a file
        logging.FileHandler('./log_files/traffic_analyzer_log.txt', mode='w'),
        # Adding one handler to see messages on console
        logging.StreamHandler()
    ]
)

logging.info("Loading files..")
# networkData:list composed by a link dict, a switch list and network parameters dict
# packetsData:composed by a packets dict

logging.info("Loading network file..")
#networkData = utils.file_loader(args.networkFile)
networkData = utils.file_loader("./data/network")
logging.info("..done!")
logging.info("Loading packets file..")
#packetsData = utils.file_loader(args.packetsFile)
packetsData = utils.file_loader("./data/packets")
logging.info("..done!")

SIM_PARAMETERS = CONST.NETWORK["SIM_PARAMS"]

logging.info("Analyzing files..")

# links is an auxiliary structure, needed to perform the simulation calculations
# the links keys are frozensets with the two endpoints linked names
# keys: frozenset("enpoint_a", "endpoint_b")
# key values are dictionaries in the form:
# "capacity": int, capacity of the link
# "trafficDT": int, the sum of the bytes for an average delta time
# "trafficUDT":int, the sum of the bytes for an update delta time
# "updateDeltaTraffic": List[dict], represents the list of sums of each time fractional unit.
#   The list is composed by dictionaries: {"updateTime":value, "traffic":value}
#       "updateTime": datetime, the timestamp of the sum
#       "traffic": the traffic bytes sum
# "traffic": List[dict], represents the list of sums of each average in delta time.
#   The list is composed by dictionaries: {"updateTime":value, "traffic":value}
#       "updateTime": datetime, the timestamp of the sum
#       "traffic": the traffic bytes sum
links = {}
# Extracting links data
for content in networkData[CONST.NETWORK["LINKS"]]:
    links[frozenset({content["endpoints"][CONST.EP_A], content["endpoints"][CONST.EP_B]})] = {
        #"linkID": link,
        "capacity": content["capacity"], 
        "trafficDT":0, 
        "trafficUDT":0, 
        "updateDeltaTraffic": [], 
        "traffic": []
        }

#logging.debug("SHOWING LINKS STRUCTURE:")
#logging.debug(links)

# Logging links with own endpoints
#for link, content in links.items():
#    logging.info("Link ID %s:", link)
#    for endpoint in link:
#        logging.info("endpoint: %s", endpoint)

# Logging simulation parameters
logging.info("Simulation parameters:")
logging.info(networkData[SIM_PARAMETERS])

# Range times parameters
# LOADING PARAMETERS
# Update average delta time (milliseconds)
UPDATE_DELTA_TIME = networkData[CONST.NETWORK["SIM_PARAMS"]]["updateDelta"]
updateDelta = timedelta(milliseconds=UPDATE_DELTA_TIME)
# The considered average time (milliseconds)
AVG_DELTA_TIME = networkData[CONST.NETWORK["SIM_PARAMS"]]["averageDelta"]
averageDelta = timedelta(milliseconds=AVG_DELTA_TIME)

# Setting the starting time point
startTime = networkData[CONST.NETWORK["SIM_PARAMS"]]["startSimTime"]
# The analyzed time
timeWalker = startTime
# Number of fractional units per averageDelta
#(averageDelta / updateDelta) must be int
averageFractions = int(averageDelta / updateDelta)

# The number of fractional units needed to get the first fractional unit of the last averageDelta
# starting from the last element of the updateDeltaTraffic list in the links
# auxiliary structure
lastFirstUDindex = averageFractions

packetsDataIterator = iter(packetsData)

# Defining the amount of simulation time in seconds
simTime = timedelta(seconds=networkData[CONST.NETWORK["SIM_PARAMS"]]["simTime"])

# Taking first packet to analyze
packet = next(packetsDataIterator, None)

# Calculating averages
# Every loop is an analyzed fractional unit
while timeWalker <= startTime + (simTime - updateDelta):
    # For each updateDelta reset values
    for link, content in links.items():
        # reset traffic
        content["trafficUDT"] = 0
    # Identify the link belonging to the analyzed packet
    if packet is not None:
        link = links[frozenset({packet["A"], packet["B"]})]
        # Analyzing every packet in the analyzed range
        while packet["t"] >= timeWalker and packet["t"] < timeWalker + updateDelta:
            link["trafficUDT"] += packet["d"]
            link["trafficDT"] += packet["d"]
            packet = next(packetsDataIterator, None)
            if packet is not None:
                link = links[frozenset({packet["A"], packet["B"]})]
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
    # In this case we don't need to subtract an updateDeltaTraffic
    elif timeWalker == startTime + averageDelta:
        for link, content in links.items():
            content["traffic"].append({"updateTime": timeWalker, "traffic": content["trafficDT"]})

# DEBUG
#utils.show_updates_data(links)
#utils.show_averages_data(links, updateDelta, averageFractions)

logging.info("..done!")

# file structure
sim_parameters = {
    "simTime": networkData[CONST.NETWORK["SIM_PARAMS"]]["simTime"],
    "updateDelta": UPDATE_DELTA_TIME,
    "averageDelta": AVG_DELTA_TIME,
    "simStartTime": startTime
}

analyzed_data = []
for link, content in links.items():
    endpoints = []
    traffic = []
    for ep in link:
        endpoints.append(ep)

    for c in content["traffic"]:
        average = utils.get_average(c['traffic'], averageFractions, utils.max_traffic_per_unit(content['capacity'], updateDelta))
        traffic.append(round(average, 2))

    analyzed_data.append({
        "endpoints": sorted(endpoints),
        "traffic": traffic
    })

fileStructure = []
fileStructure.append(sim_parameters)
fileStructure.append(analyzed_data)

# frontend file input
logging.info("Writing analyzed_data_test.yaml file..")
try:
    with open('./data/analyzed_data.yaml', 'w', encoding="utf-8") as file:
        yaml.dump(fileStructure, file)
    logging.info("analyzed_data_test.yaml file creation done!")
except OSError as e:
    print(f"I/O error: {e}")
except yaml.YAMLError as e:
    print(f"YAML error: {e}")

any_key = input("Press any key to exit")
sys.exit()
