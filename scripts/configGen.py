# A yaml file config generator script. It creates two network config files

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
        logging.FileHandler('log_file.txt'),  # Aggiungi un gestore per registrare i messaggi su file
        logging.StreamHandler()  # Aggiungi un gestore per visualizzare i messaggi sulla console
    ]
)

# STARTING POINT

# Getting the switch number and the link capacity by prompt
inputParameters = utils.getInputParameters()

print(f"The choosen switch number is {inputParameters.switchNumber} and link capacity is {inputParameters.linkCap}MB")

switchNumber = inputParameters.switchNumber
linkCap = inputParameters.linkCap

# Defining the start time point
startTime = datetime(2024, 1, 1, 0, 0, 0)


# Defining the amount of simulation time in seconds
simTime = 60
# Defining the pps creation rate delta time (50ms)
ppsDelta = 50
ppsInterval = timedelta(milliseconds=ppsDelta)
# Defining the traffic percentage change delta time
trafficPercDelta = 1
trafficPercInterval = timedelta(seconds=trafficPercDelta)

# test
print(startTime)
print(startTime + timedelta(milliseconds=50))

# Gli archi rappresentanti i link che collegano gli switch(i nodi)
links = []

print("------")

# Creo i link
for i in range(1, switchNumber + 1):
  for p in range(1, switchNumber + 1):
    if i == p: 
      continue
    # Controllo che il link non sia stato già creato
    print(f"controllo che il link tra switch{i} e switch{p} non sia stato già creato:")
    if utils.inLinks(links, f"switch{i}", f"switch{p}"):
      continue
    print(f"creo link con endpoint: switch{i}, switch{p}...")
    links.append(Link(linkCap, [f"switch{i}", f"switch{p}"]))
    print("...link creato!!")

print("------")
for l in links:
  print(l)
print("------")

test =(10 * 1e6)/8
print(test)

#setta il nuovo valore di percentuale di traffico del link a partire dal precedente valore
for i in range(0, len(links)):
  links[i].setTrafficPerc(utils.changeTrafficPerc(links[i].getTrafficPerc()))

print("------")
for l in links:
  print(l)
print("------")


# Creo il traffico
# Ogni frazione di secondo (ppsDelta) di simulazione crea un numero di pacchetti proporzionato alla percentuale di traffico
# dei singoli link

packetSize = 1518
pps = int(((linkCap * 1e6) / 8) / packetSize)
timeWalker = startTime
creationRate = int(timedelta(seconds=trafficPercDelta)/timedelta(milliseconds=ppsDelta))

unitsPerSec = trafficPercInterval / ppsInterval

""" print(open('names.yaml').read()) """


packets = []
# Per ogni creationRate fino a fine simTime della simulazione
for sec in range(0, simTime * creationRate):
  # Crea pacchetti ogni 50 ms
  if sec % creationRate == 0:
    print("-----")
    for i in range(0, len(links)):
      links[i].setTrafficPerc(utils.changeTrafficPerc(links[i].getTrafficPerc()))
      print(links[i])

  timeWalker += timedelta(milliseconds=ppsDelta)

  for l in links:
    trafficPerc = l.getTrafficPerc()
    for p in range(0, int(int((pps*trafficPerc)/100)/creationRate)):
      sourceIndex = random.randint(0, 1)
      destIndex = 1 - sourceIndex
      packet = {"source": l.getEndpoints()[sourceIndex],
                "destination": l.getEndpoints()[destIndex],
                "timestamp": str(timeWalker),
                "dimension": packetSize}
      packets.append(packet)




print("----------")

with open('packets.yaml', 'w') as file:
    yaml.dump(packets, file)


switches = []
ipAddress = "123.123.123."
ipLastSect = 1
# Creo il network.yaml file
for i in range(1, switchNumber + 1):
  connectedTo = []
  for j in range(1, switchNumber + 1):
    if i == j:
      continue
    connectedTo.append(f"switch{j}")
  
  connectedToStr = "["
  for index in range(0, len(connectedTo)):
    if index == len(connectedTo) - 1:
      connectedToStr += f"\"{connectedTo[index]}\"]"
    else:
      connectedToStr += f"\"{connectedTo[index]}\","
  switches.append({
    "switchName": f"switch{i}",
    "address": f"{ipAddress}{ipLastSect}",
    "connectedTo": connectedToStr
  })
  ipLastSect += 1

for s in switches:
  print(s)

with open('network.yaml', 'w') as file:
  yaml.dump(switches, file)