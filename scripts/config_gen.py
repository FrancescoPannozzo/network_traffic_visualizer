""" 
Network and packets traffic generator

Description: 
    A yaml file config generator script. It creates two network config files,
    a network.yaml file with the networtk features and a packets.yaml file with 
    all the generated traffic packets. By inserting a switch number and a links capacity it create
    a complete graph structure and a packets traffic for evrey link. 
    Traffic varies by 10% for each second of simulation
Usage: 
    launch the script: python config_gen.py switches_number link_capacity_number
    help: python config_gen.py -h 
Author: Francesco Pannozzo"""

from datetime import datetime, timedelta
import logging
import random
import utils
import yaml

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

# Getting the switch number and the link capacity (Mbps) from the user by prompt
inputParameters = utils.get_input_parameters()

logging.info("The choosen switches number is %d and the network link capacity is %d Mbps",
             inputParameters.switchNumber, inputParameters.linkCapacity)

SWITCH_NUMBER = inputParameters.switchNumber
LINK_CAP = inputParameters.linkCapacity
# Defining the simulation start time point
START_TIME = datetime(2024, 1, 1, 0, 0, 0)
# Defining the simulation time in seconds
SIM_TIME = 60
# Defining the packets per second creation rate delta time (milliseconds)
PPS_DELTA = 50
# Defining packets size (MB) 1518
PACKET_SIZE = 1518
# Packets Per Seconds
PPS = ((LINK_CAP * 1e6) / 8) / PACKET_SIZE

# The arcs representing the links connecting the switches (nodes)
links = {}
# The link ID counter
linkID = 1
# Creating links
logging.info("Creating links..")
for i in range(1, SWITCH_NUMBER + 1):
    for p in range(i, SWITCH_NUMBER + 1):
        if i != p:
            if linkID not in links:
                links[linkID] = {
                    "endpoints": [f"switch{i}", f"switch{p}"],
                    "capacity": LINK_CAP,
                    "trafficPerc": utils.change_traffic_perc(0)
                    }
                linkID += 1

logging.info("Links creation done!Links created are:")
for link, content in links.items():
    logging.info("%s: %s", link, content)

# Creating traffic packets
# Each fraction of a second (PPS_DELTA) of simulation creates a number of packets
# proportionate to the percentage of traffic for each link

logging.info("Packets per second: %f ", PPS)
# The packets creation index time
timeWalker = START_TIME
# creationRate is the fractional time units value in one second
# example: 10 fractional time units for 100ms in 1 second
creationRate = int(timedelta(seconds=1)/timedelta(milliseconds=PPS_DELTA))
# Defining the list containing all the packets generated
packets = []

# Creating packets
logging.info("Creating packets.yaml file structure..")
for sec in range(0, SIM_TIME * creationRate):
  # Changing trafficPercentage every (sec / creationRate) time units
    if sec % creationRate == 0:
        for link, content in links.items():
            content["trafficPerc"] = utils.change_traffic_perc(content["trafficPerc"])
            logging.info("Link: %s, endpoints: %s, sim second: %d, trafficPerc: %d",
                         link, content["endpoints"], (sec / creationRate), content["trafficPerc"])

    for link, content in links.items():
        trafficPerc = content["trafficPerc"]
        for i in range(0, int((PPS*(trafficPerc/100))/creationRate) ):
            sourceIndex = random.randint(0, 1)
            destIndex = 1 - sourceIndex
            packet = {"source": content["endpoints"][sourceIndex],
                      "destination": content["endpoints"][destIndex],
                      "timestamp": timeWalker,
                      "dimension": PACKET_SIZE}
            packets.append(packet)

    timeWalker += timedelta(milliseconds=PPS_DELTA)

logging.info("..packets.yaml file structure done!")
logging.info("Writing packets.yaml file..")
with open('../packets.yaml', 'w', encoding="utf-8") as file:
    yaml.dump(packets, file)
logging.info("..packets file creation done!")

# Defining the network.yaml fields defined in each switch object
switches = []
# First 3 address groups
IP_ADDRESS = "123.123.123."
# Last address group
ipLastGroup = 1

# Creating network.yaml file
# File structure composed by a links list and a switches list
# networkData = [[links list],[switches list]]
logging.info("Creating network.yaml file structure..")
networkData = [{},[],{}]
LINK_INDEX = 0
SWITCH_INDEX = 1
SIM_PARAMETERS = 2

for link, content in links.items():
    networkData[LINK_INDEX][link] = {
        "endpoints": content["endpoints"],
        "capacity": content["capacity"]
    }

for i in range(1, SWITCH_NUMBER + 1):
    networkData[SWITCH_INDEX].append({
      "switchName": f"switch{i}",
      "address": f"{IP_ADDRESS}{ipLastGroup}"
    })
    ipLastGroup += 1

networkData[SIM_PARAMETERS] = {
    "simTime": SIM_TIME,
    "startSimTime": START_TIME
}
logging.info("..network.yaml file structure done!")
logging.info("Writing network.yaml file..")
try:
    with open('../network.yaml', 'w', encoding="utf-8") as file:
        yaml.dump(networkData, file)
except OSError as e:
    print(f"I/O error: {e}")
except yaml.YAMLError as e:
    print(f"YAML error: {e}")

logging.info("..network.yaml file creation done!")
