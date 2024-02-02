# A yaml file config generator script. It creates two network config files:
# a network.yaml file with the networtk features and a packets.yaml file with all the generated traffic packets

from classes import Link
from datetime import datetime, timedelta, time
import utils
import logging
import random
import yaml

# Logger config
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('log_file.txt', mode='w'),  # Adding one handler to manage the messages on a file
        logging.StreamHandler()  # Adding one handler to see messages on console
    ]
)

# Getting the switch number and the link capacity (Mbps) from the user by prompt
inputParameters = utils.getInputParameters()

logging.info(f"The choosen switches number is {inputParameters.switchNumber} and the network link capacity is {inputParameters.linkCap}Mbps")

switchNumber = inputParameters.switchNumber
linkCap = inputParameters.linkCap

# Defining the simulation start time point
startTime = datetime(2024, 1, 1, 0, 0, 0)

# Defining the simulation time in seconds
simTime = 60
# Defining the pps creation rate delta time (milliseconds)
ppsDelta = 100
ppsInterval = timedelta(milliseconds=ppsDelta)
# Defining the traffic percentage variation, delta time (seconds)
trafficPercDelta = 1
trafficPercInterval = timedelta(seconds=trafficPercDelta)

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
for i in range(0, len(links)):
  links[i].trafficPerc = utils.changeTrafficPerc(links[i].trafficPerc)
  logging.info(f"Link with id: {links[i].linkId}, trafficPerc choose: {links[i].trafficPerc}")

# Creating traffic packets
# Each fraction of a second (ppsDelta) of simulation creates a number of packets proportionate to the percentage of traffic
# for each link
logging.info("Creating packets file..")
# Defining packets size (MB)
packetSize = 1518
# Packets Per Seconds
pps = int(((linkCap * 1e6) / 8) / packetSize)
# The packets creation index time
timeWalker = startTime
# The time interval unit for packets creation, we'll create packets "creationTime times" in "trafficPercDelta seconds"
creationRate = int(timedelta(seconds=trafficPercDelta)/timedelta(milliseconds=ppsDelta))
# Defining the list containing all the packets generated
packets = []

# Creating packets
for sec in range(0, simTime * creationRate):
  # Changing trafficPercentage every (sec / creationRate) time units
  if sec % creationRate == 0:
    for i in range(0, len(links)):
      links[i].trafficPerc = utils.changeTrafficPerc(links[i].trafficPerc)
      logging.info(f"Sim second: {sec / creationRate}, Link with id: {links[i].linkId}, trafficPerc choose: {links[i].trafficPerc}")

  for l in links:
    trafficPerc = l.trafficPerc
    for p in range(0, int(int((pps*trafficPerc)/100)/creationRate)):
      sourceIndex = random.randint(0, 1)
      destIndex = 1 - sourceIndex
      packet = {"source": l.endpoints[sourceIndex],
                "destination": l.endpoints[destIndex],
                "timestamp": timeWalker,
                "dimension": packetSize}
      packets.append(packet)

  timeWalker += timedelta(milliseconds=ppsDelta)

logging.info("Creating packets.yaml file..")
with open('../packets.yaml', 'w') as file:
    yaml.dump(packets, file)
logging.info("..packet file creation done!")

# Defining the network.yaml fields defined in each switch object
switches = []
# First 3 address groups
ipAddress = "123.123.123."
# Last address group
ipLastSect = 1

# Creating network.yaml file
# File structure composed by a links list and a switches list
# networkData = [[links list],[switches list]]
logging.info("Creating network.yaml file..")
networkData = [[],[]]
linkIndex = 0
switchIndex = 1

# filling the links list:
for link in links:
  networkData[linkIndex].append({"endpoints": link.endpoints,
                                 "capacity": link.capacity})

  networkData[switchIndex].append({
    "switchName": f"switch{i}",
    "address": f"{ipAddress}{ipLastSect}"
  })
  ipLastSect += 1

with open('../network.yaml', 'w') as file:
  yaml.dump(networkData, file)
logging.info("..network.yaml file creation done!")