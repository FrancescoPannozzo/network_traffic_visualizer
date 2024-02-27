""" 
Network and packets traffic generator

Description: 
    A yaml file config generator script. It creates two network config files,
    a network.yaml file with the networtk features and a packets.yaml file with 
    all the generated traffic packets. By inserting a switch number and a links capacity it create
    a complete graph structure and a packets traffic for evrey link. 
    Traffic varies by +/-10% for each second of simulation
Usage: 
    launch the script: python config_gen.py switches_number link_capacity_number
    help: python config_gen.py -h 
Author: Francesco Pannozzo
"""

from datetime import datetime, timedelta
import logging
import math
import yaml
from utils import config_gen_utils

# Logger config
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        # Adding one handler to manage the messages on a file
        logging.FileHandler('./log_files/config_gen_log.txt', mode='w'),
        # Adding one handler to see messages on console
        logging.StreamHandler()
    ]
)

# Getting the switch number and the link capacity (Mbps) from the user by prompt
inputParameters = config_gen_utils.get_input_parameters()

logging.info("The choosen switches number is %d and the network link capacity is %d Mbps",
             inputParameters.switchNumber, inputParameters.linkCapacity)

SWITCH_NUMBER = inputParameters.switchNumber
LINK_CAP = inputParameters.linkCapacity
# Defining the simulation start time point
START_TIME = datetime(2024, 1, 1, 0, 0, 0)
# Defining the simulation time in seconds
SIM_TIME = 3
# Defining the packets per second creation rate delta time (milliseconds)
PPS_DELTA = 100
# Defining packets size (MB) (example 1518 Bytes ipv4 max payload, 4000 datacenters)
PACKET_SIZE = 4000
# Packets Per Second
PPS = ((LINK_CAP * 1e6) / 8) / PACKET_SIZE

logging.info("LinkCap in Bytes: %dB", (LINK_CAP * 1e6) / 8)
logging.debug("PPS: %f", PPS)

# The arcs representing the links connecting the switches (nodes)
links = {}
# The link ID counter
link_id = 1
# Creating links: complete graph
logging.info("Creating links..")
links = config_gen_utils.create_complete_links(LINK_CAP, SWITCH_NUMBER)

logging.info("..links creation done!Links created are:")
for link, content in links.items():
    logging.info("%s: %s", link, content)

# Creating traffic packets
# Each fraction of a second (PPS_DELTA) of simulation creates a number of packets
# proportionate to the percentage of traffic for each link

# The packets creation index time
timeWalker = START_TIME

# creationRate is the fractional time units value in one second
# example: in one second we have 10 fractional units of 100 milliseconds
# usage: choose PPS_DELTA to avoid remainder != 0
# PPS_DELTA values examples: 50, 100, 200, 250, 500
creationRate = int(timedelta(milliseconds=1000)/timedelta(milliseconds=PPS_DELTA))

# Defining the list containing all the packets generated
packets = []

# Creating packets
logging.info("Creating packets.yaml file structure..")
# Each fractional_unit represents the unit of time space in which a number of packets
# proportionate to the chosen traffic are created
for fractional_unit in range(0, SIM_TIME * creationRate):
    # Changing trafficPercentage every second
    if fractional_unit % creationRate == 0:
        for link, content in links.items():
            content["trafficPerc"] = config_gen_utils.change_traffic_perc(content["trafficPerc"])
            logging.info("Link: %s, endpoints: %s, sim second: %d, trafficPerc: %d",
                         link, content["endpoints"],
                         (fractional_unit / creationRate),
                         content["trafficPerc"])

    ENDP_A = 0
    ENDP_B = 1
    for link, content in links.items():
        trafficPerc = content["trafficPerc"]

        for i in range(0, int((PPS*(trafficPerc/100))/creationRate) ):
            packet = config_gen_utils.create_packet(content["endpoints"][ENDP_A],
                                         content["endpoints"][ENDP_B],
                                         timeWalker,
                                         PACKET_SIZE)
            packets.append(packet)

        remaining_packets, _ = math.modf((PPS*(trafficPerc/100))/creationRate)
        if remaining_packets != 0:
            remaining_packet_size = int(round(remaining_packets, 3) * PACKET_SIZE)
            packet = config_gen_utils.create_packet(content["endpoints"][ENDP_A],
                                         content["endpoints"][ENDP_B],
                                         timeWalker,
                                         remaining_packet_size)
            packets.append(packet)

    timeWalker += timedelta(milliseconds=PPS_DELTA)

logging.info("..packets.yaml file structure done!")
logging.info("Writing packets.yaml file..")
with open('./data/packets.yaml', 'w', encoding="utf-8") as file:
    yaml.dump(packets, file)
logging.info("..packets file creation done!")

# Defining the network.yaml fields defined in each switch object
switches = []
# Defining the switches ip address structure
ip_address = {
    "groupA": 10,
    "groupB": 0,
    "groupC": 0,
    "groupD": 0
}

# Creating network.yaml file
# File structure composed by a links list and a switches list
# networkData = [[links list],[switches list]]
logging.info("Creating network.yaml file structure..")
networkData = [{},[],{}]
LINK_INDEX = 0
SWITCH_INDEX = 1
SIM_PARAMETERS = 2
MAX_GROUP_IP_ADDRESS = 255

for link, content in links.items():
    networkData[LINK_INDEX][link] = {
        "endpoints": content["endpoints"],
        "capacity": content["capacity"]
    }

switch_ID_counter = 0
for i in range(1, SWITCH_NUMBER + 1):
    if i % (MAX_GROUP_IP_ADDRESS + 1) == 0:
        ip_address["groupC"] += 1
    ip_address["groupD"] = i % 256

    switch_ID_counter += 1
    networkData[SWITCH_INDEX].append({
        "switchID": switch_ID_counter,
        "switchName": f"switch{i}",
        "address": config_gen_utils.ip_to_string(ip_address)
    })

logging.info("Switches created:")
for i in networkData[SWITCH_INDEX]:
    logging.info(i)

networkData[SIM_PARAMETERS] = {
    "simTime": SIM_TIME,
    "startSimTime": START_TIME
}
logging.info("..network.yaml file structure done!")
logging.info("Writing network.yaml file..")
try:
    with open('./data/network.yaml', 'w', encoding="utf-8") as file:
        yaml.dump(networkData, file)
except OSError as e:
    print(f"I/O error: {e}")
except yaml.YAMLError as e:
    print(f"YAML error: {e}")

logging.info("..network.yaml file creation done!")