""" 
Network and packets traffic generator

Description: 
    A yaml file config generator script. It creates two network config files,
    a network.yaml file with the networtk features and a packets.yaml file with 
    all the generated traffic packets.

Author: Francesco Pannozzo
"""

from datetime import timedelta, datetime
import logging
import math
import os
import json
import yaml
from utils import config_gen_utils
from utils import utils
from utils import CONSTANTS as CONST


if not os.path.exists("./log_files"):
    os.makedirs("./log_files")

# Logger config
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        # Adding one handler to manage the messages on a file
        logging.FileHandler('./log_files/config_gen_jsonTest_log.txt', mode='w'),
        # Adding one handler to see messages on console
        logging.StreamHandler()
    ]
)

link_capacity = None
switch_number = None
graph_type = None
user_mode = None
user_data = None

# LOADING PARAMETERS
setup = utils.file_loader("./data/sim_setup", "yaml")
utils.check_sim_setup(setup)

# CHOSING USER MODE OR AUTO MODE
CORRECT_CHOOSE = False
while not CORRECT_CHOOSE:
    choice = input("Choose the graph visualization mode:\n"
                "1 - User mode\n"
                "2 - Auto mode\n")
    try:
        user_mode = int(choice)
        if user_mode in [CONST.USER_MODE, CONST.AUTO_MODE]:
            CORRECT_CHOOSE = True
        else:
            logging.warning("WARNING, values must be 1 or 2.\n")
    except ValueError:
        logging.warning("WARNING, value is not an int, please retry, choose 1 or 2.\n")

CORRECT_CHOOSE = False

if user_mode == CONST.USER_MODE:
    logging.info("You choosed the user mode!")
    logging.info("Loading user file..")
    user_data = utils.file_loader("./data/custom_graph", "yaml")
    config_gen_utils.check_custom_file(user_data["data"])
    user_data = user_data["data"]
    switch_number = len(user_data["switches"])
    graph_type = user_data["graphType"]
else:
    logging.info("You choosed the auto mode!")
    while not CORRECT_CHOOSE:
        switch_number = input("Please insert the switch number min 2 - max 1000:\n")
        graph_type = input("Please enter c if you want a complete graph\n"
                            "enter m for a mesh graph, t for a torus graph\n")
        try:
            switch_number = int(switch_number)
            if switch_number in range(2, 1001) and graph_type in ["c", "m", "t"]:
                CORRECT_CHOOSE = True
                graph_types = {
                    "c": "complete",
                    "m": "mesh",
                    "t": "torus"
                }
                graph_type = graph_types[graph_type]
            else:
                logging.warning("WARNING, values must be in range [2-1000] and c/m/t.\n")
        except ValueError:
            logging.warning("WARNING, switch number is not an int, please retry.\n")

CORRECT_CHOOSE = False
if user_mode == CONST.AUTO_MODE:
    while not CORRECT_CHOOSE:
        link_capacity = input("please insert the links capacity [10, 100, 1000]:\n")
        try:
            link_capacity = int(link_capacity)
            if link_capacity in [10, 100, 1000]:
                CORRECT_CHOOSE = True
            else:
                logging.warning("WARNING, values must be one of these [10, 100, 1000].\n")
        except ValueError:
            logging.warning("WARNING, value is not an int, please retry, choose 1 or 2.\n")
elif user_mode == CONST.USER_MODE:
    if "linkCap" in user_data:
        link_capacity = user_data["linkCap"]
    else:
        link_capacity = "mixed"

# Testing che network and packets structure creation time
start_test_time = datetime.now()

# Defining the simulation start time point
# START_TIME = datetime(2024, 1, 1, 0, 0, 0)
START_TIME = setup["startSimTime"]
# Defining the simulation time in seconds
SIM_TIME = setup["simTime"]
# Defining the packets creation delta time rate(milliseconds)
PC_DELTA = setup["creationDelta"]
# Defining packets size (MB) (example 1518 Bytes ipv4 max payload, 4000 datacenters)
PACKET_SIZE = setup["packetSize"]

# The arcs representing the links connecting the switches (nodes)
links = {}
# Switches
switches = []

# CREATING LINKS
logging.info("Creating links..")
if user_mode == CONST.USER_MODE:
    if user_data["graphType"] == CONST.MESH_GRAPH:
        links = config_gen_utils.create_user_mesh_links(user_data)
    elif user_data["graphType"] == CONST.TORUS_GRAPH:
        links = config_gen_utils.create_user_toro_links(user_data)
    elif user_data["graphType"] == CONST.FREE_GRAPH:
        links = config_gen_utils.create_user_graph_links(user_data)
else:
    if graph_type == CONST.COMPLETE_GRAPH:
        links = config_gen_utils.create_auto_complete_links(link_capacity, switch_number)
    elif graph_type == CONST.MESH_GRAPH:
        links, switches = config_gen_utils.create_auto_mesh_links(link_capacity, switch_number)
    elif graph_type == CONST.TORUS_GRAPH:
        links, switches = config_gen_utils.create_auto_toro_links(link_capacity, switch_number)

logging.info("..links creation done!")

logging.info("Links created are:")
for link, content in links.items():
    logging.info("%s: %s", link, content)

# Creating traffic packets
# Each fraction of a second (PC_DELTA) of simulation creates a number of packets
# proportionate to the percentage of traffic for each link

# The packets creation index time
timeWalker = START_TIME

# creationRate is the fractional time units value in one second
# example: in one second we have 10 fractional units of 100 milliseconds
# usage: choose PC_DELTA to avoid remainder != 0
# PC_DELTA values examples: 50, 100, 200, 250, 500
creationRate = int(timedelta(milliseconds=1000)/timedelta(milliseconds=PC_DELTA))

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
            content["trafficPerc"] = config_gen_utils.change_traffic_perc(content["trafficPerc"], setup["trafficVariation"])
            # debug
            #logging.info("Link: %s, endpoints: %s, sim second: %d, trafficPerc: %d",
            #             link, content["endpoints"],
            #            (fractional_unit / creationRate),
            #           content["trafficPerc"])
            # debug
            #numero = str(content["trafficPerc"]).replace('.', ',')
            #print(numero)
    ENDP_A = 0
    ENDP_B = 1
    for link, content in links.items():
        trafficPerc = content["trafficPerc"]
        # Packets Per Second
        PPS = ((content["capacity"] * 1e6) / 8) / PACKET_SIZE
        timeWalker_toStore = None
        if setup["packetsFile"] == "json":
            timeWalker_toStore = str(timeWalker) # json non parsa i datetime!
        else:
            timeWalker_toStore = timeWalker
        for i in range(0, int((PPS*(trafficPerc/100))/creationRate) ):
            packet = config_gen_utils.create_packet(content["endpoints"][ENDP_A],
                                         content["endpoints"][ENDP_B],
                                         timeWalker_toStore,
                                         PACKET_SIZE)
            packets.append(packet)

        remaining_packets, _ = math.modf((PPS*(trafficPerc/100))/creationRate)
        if remaining_packets != 0:
            remaining_packet_size = int(round(remaining_packets, 3) * PACKET_SIZE)
            packet = config_gen_utils.create_packet(content["endpoints"][ENDP_A],
                                         content["endpoints"][ENDP_B],
                                         timeWalker_toStore,
                                         remaining_packet_size)
            packets.append(packet)
    timeWalker += timedelta(milliseconds=PC_DELTA)

logging.info("..packets file structure done!")

# Defining the network.yaml fields defined in each switch object

# Creating network.yaml file
# File structure composed by a links list and a switches list
# networkData = [[links list],[switches list],{},{},{}]
logging.info("Creating network.yaml file structure..")
networkData = [[],[],{},{},{}]
LINK_INDEX = CONST.NETWORK["LINKS"]
SWITCH_INDEX = CONST.NETWORK["SWITCHES"]
SIM_PARAMETERS_INDEX = CONST.NETWORK["SIM_PARAMS"]
COORDINATES_INDEX = CONST.NETWORK["COORDINATES"]
PHASES_INDEX = CONST.NETWORK["PHASES"]

for link, content in links.items():
    networkData[LINK_INDEX].append({
        "endpoints": content["endpoints"],
        "capacity": content["capacity"]
    })

if user_mode == CONST.USER_MODE:
    for switch_key, content in user_data["switches"].items():
        networkData[SWITCH_INDEX].append({
            "switchID": switch_key,
            "switchName": content["switchName"],
            "address": content["ip"]
        })

    networkData[PHASES_INDEX] = user_data["phases"]
else:
    # Defining the switches ip address structure for the auto mode
    MAX_GROUP_IP_ADDRESS = 255
    ip_address = config_gen_utils.ip_address(10, 0, 0, 0)
    switch_ID_counter = 0
    for i in range(1, switch_number + 1):
        if i % (MAX_GROUP_IP_ADDRESS + 1) == 0:
            ip_address["groupC"] += 1
        ip_address["groupD"] = i % 256

        switch_ID_counter += 1
        networkData[SWITCH_INDEX].append({
            "switchID": switch_ID_counter,
            "switchName": f"switch{i}",
            "address": config_gen_utils.ip_to_string(ip_address)
        })

    networkData[PHASES_INDEX] = config_gen_utils.create_auto_phases(START_TIME, SIM_TIME, setup)

logging.info("Switches created:")
for i in networkData[SWITCH_INDEX]:
    logging.info(i)

# SIM PARAM FOR COMPLETE/MESH/TORO GRAPHS
networkData[SIM_PARAMETERS_INDEX] = {
    "simTime": SIM_TIME,
    "startSimTime": START_TIME,
    "graphType": graph_type,
    "linkCap": link_capacity,
    "colorblind": setup["colorblind"],
    "updateDelta": setup["updateDelta"],
    "averageDelta": setup["averageDelta"],
    "dotsSize": setup["dotsSize"],
    "packetsFile": setup["packetsFile"]
}

if user_mode == CONST.USER_MODE:
    networkData[COORDINATES_INDEX]["coordinates"] = user_data["coordinates"]
else:
    networkData[COORDINATES_INDEX]["coordinates"] = switches

logging.info("..network.yaml file structure done!")

logging.debug("NETWORK and PACKETS structure creation time:%s", utils.get_test_duration(start_test_time))

if not os.path.exists("./data"):
    os.makedirs("./data")

try:
    logging.info("Writing network.yaml file..")
    with open('./data/network.yaml', 'w', encoding="utf-8") as file:
        yaml.dump(networkData, file)
        #json.dump(networkData, file, ensure_ascii=False, indent=4)
    logging.info("..network.yaml file creation done!")

    start_test_time = datetime.now()

    logging.info("Writing packets file..")
    # readeblePackets key in sim_setup.yaml file allow to choose if you want a 
    # readeble packets.yaml file having a bigger file and bigger computational time, or
    # a not readeble packets.yaml file having a smaller file and a better
    # computational time

    if setup["packetsFile"] == "json":
        with open('./data/packets.json', 'w', encoding="utf-8") as file:
            json.dump(packets, file, ensure_ascii=False, indent=4)
    else:
        with open('./data/packets.yaml', 'w', encoding="utf-8") as file:
            yaml.dump(packets, file)
    
    logging.info("..packets file creation done!")
    
    logging.debug("NETWORK and PACKETS structure writing time:%s", utils.get_test_duration(start_test_time))

except OSError as e:
    print(f"I/O error: {e}")
except yaml.YAMLError as e:
    print(f"YAML error: {e}")


#any_key = input("Press any key to exit")
#sys.exit()