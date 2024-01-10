# A yaml file config generator script. It creates two network config files

from classes import Link
from datetime import datetime, timedelta
import utils
import logging
import random

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
startTime = datetime(2024, 1, 1, 0, 0, 0, 1)
# Defining the generation rate delta time in milliseconds
delta = 50
# Defining the amount of simulation time in seconds
simTime = 60

# test
print(startTime)
print(startTime + timedelta(milliseconds=delta))

# Gli archi rappresentanti i link che collegano gli switch(i nodi)
links = []

print("------")

# Creo i link
for i in range(1, switchNumber + 1):
  for p in range(1, switchNumber + 1):
    if i == p: 
      continue
    
    #Controllo che il link non sia stato già creato
    print(f"controllo che il link tra switch{i} e switch{p} non sia stato già creato:")
    if utils.inLinks(links, f"switch{i}", f"switch{p}"):
      continue

    print(f"creo link con endpoint: switch{i}, switch{p}...")
    links.append(Link(linkCap, [f"switch{i}", f"switch{p}"]))
    print("...link creato!!")

print("------")
for l in links:
  print(l)

test =(10 * 1e6)/8
print(test)

# traffico di ciascun link


test = 0
for i in range(0, 20):
  if random.randint(1, 10) > 5:
    if test < 10:
      test += 1
  else:
    if test > 0:
      test -= 1



for _ in range(0, 10):
  for i in range(0, len(links)):
    #setta il nuovo valore di percentuale di traffico del link a partire dal precedente valore
    links[i].setTrafficPerc(utils.changeTrafficPerc(links[i].getTrafficPerc()))
    print(links[i])
  print("--------")
















