import argparse
import random

# Check if a link is already present in links list
def inLinks(links, firstEndopoint, secondEndpoint):
    for l in links:
      if l.checkEndpoints(firstEndopoint, secondEndpoint):
        return True
    return False

# Argparse function to insert file config parameters
def getInputParameters():
   # Setting the command line option to set thw switch number and the switch-links capacity
    parser = argparse.ArgumentParser()
    parser.add_argument("switchNumber", type=int, help="The switch number you want to create")
    parser.add_argument("linkCap", type=int, help="The switch-link capacity (MB) you want to load")
    args = parser.parse_args()
    return args

# Update traffic percentage
def changeTrafficPerc(trafficPerc): 
  newTrafficPerc = trafficPerc
  if random.randint(0, 1) == 1:
    if newTrafficPerc < 100:
      newTrafficPerc += 10
  else:
    if newTrafficPerc > 0:
      newTrafficPerc -= 10
  return newTrafficPerc
