import argparse
import logging
import os
import yaml

#check if a link is already present in links list
def inLinks(links, firstEndopoint, secondEndpoint):
    for l in links:
      if l.checkEndpoints(firstEndopoint, secondEndpoint):
        print(f"link con endpoints {firstEndopoint}, {secondEndpoint} già creato")
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