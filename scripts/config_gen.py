""" A yaml file config generator script. It creates two network config files:
a network.yaml file with the networtk features and a packets.yaml file with 
all the generated traffic packets """

from datetime import datetime, timedelta
import logging
import random
import utils
import yaml
from classes import Link


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
inputParameters = utils.getInputParameters()

logging.info("The choosen switches number is %d and the network link capacity is %d Mbps",
             inputParameters.switchNumber, inputParameters.linkCap)

switchNumber = inputParameters.switchNumber
linkCap = inputParameters.linkCap

# Defining the simulation start time point
startTime = datetime(2024, 1, 1, 0, 0, 0)

# Defining the simulation time in seconds
SIM_TIME = 60
# Defining the pps creation rate delta time (milliseconds)
PPS_DELTA = 100
ppsInterval = timedelta(milliseconds=PPS_DELTA)
# Defining the traffic percentage variation, delta time (seconds)
TRAFFIC_PERC_DELTA = 1
trafficPercInterval = timedelta(seconds=TRAFFIC_PERC_DELTA)

# The arcs representing the links connecting the switches (nodes)
links = []

# Creating links
logging.info("Creating links..")
for i in range(1, switchNumber + 1):
    for p in range(1, switchNumber + 1):
        if i == p:
            continue
        # Checking if the link is already created
        if utils.inLinks(links, f"switch{i}", f"switch{p}"):
            continue
        links.append(Link(linkCap, [f"switch{i}", f"switch{p}"]))
logging.info("Links creation done!Links created are:")
for l in links:
    logging.info(l)

# Creating the links initial traffic percentage
for link in links:
    link.trafficPerc = utils.changeTrafficPerc(link.trafficPerc)
    logging.info("Link with id: %d, trafficPerc choose: %d", link.linkId, link.trafficPerc)

# Creating traffic packets
# Each fraction of a second (PPS_DELTA) of simulation creates a number of packets
# proportionate to the percentage of traffic for each link
logging.info("Creating packets file..")
# Defining packets size (MB) 1518
PACKET_SIZE = 1518
# Packets Per Seconds
pps = int(((linkCap * 1e6) / 8) / PACKET_SIZE)
logging.info("Packets per second: %d ", pps)
# The packets creation index time
timeWalker = startTime
# The time interval unit for packets creation, we'll create packets
# "creationTime times" in "TRAFFIC_PERC_DELTA seconds"
creationRate = int(timedelta(seconds=TRAFFIC_PERC_DELTA)/timedelta(milliseconds=PPS_DELTA))
# Defining the list containing all the packets generated
packets = []

# Creating packets
for sec in range(0, SIM_TIME * creationRate):
  # Changing trafficPercentage every (sec / creationRate) time units
    if sec % creationRate == 0:
        for link in links:
            link.trafficPerc = utils.changeTrafficPerc(link.trafficPerc)
            logging.info("Sim second: %d, Link id: %d, trafficPerc: %d",
                         (sec / creationRate), link.linkId, link.trafficPerc)

    for l in links:
        trafficPerc = l.trafficPerc
        for p in range(0, int(int((pps*trafficPerc)/100)/creationRate)):
            sourceIndex = random.randint(0, 1)
            destIndex = 1 - sourceIndex
            packet = {"source": l.endpoints[sourceIndex],
                      "destination": l.endpoints[destIndex],
                      "timestamp": timeWalker,
                      "dimension": PACKET_SIZE}
            packets.append(packet)

    timeWalker += timedelta(milliseconds=PPS_DELTA)

logging.info("Creating packets.yaml file..")
with open('../packets.yaml', 'w', encoding="utf-8") as file:
    yaml.dump(packets, file)
logging.info("..packet file creation done!")

# Defining the network.yaml fields defined in each switch object
switches = []
# First 3 address groups
IP_ADDRESS = "123.123.123."
# Last address group
IP_LAST_SECT = 1

# Creating network.yaml file
# File structure composed by a links list and a switches list
# networkData = [[links list],[switches list]]
logging.info("Creating network.yaml file..")
networkData = [[],[]]
LINK_INDEX = 0
SWITCH_INDEX = 1

# filling the links list:
for link in links:
    networkData[LINK_INDEX].append({"endpoints": link.endpoints,
                                    "capacity": link.capacity})

    networkData[SWITCH_INDEX].append({
      "switchName": f"switch{i}",
      "address": f"{IP_ADDRESS}{IP_LAST_SECT}"
    })
    IP_LAST_SECT += 1

with open('../network.yaml', 'w', encoding="utf-8") as file:
    yaml.dump(networkData, file)
logging.info("..network.yaml file creation done!")