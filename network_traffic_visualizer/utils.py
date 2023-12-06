import json
import os
import argparse

#load the .json configuration files
def fileLoader(networkFileName, packetsFileName):
  #Getting absolute path from the running software directory
  current_folder = os.getcwd()
  #Abs path plus filename
  networkFilePath = current_folder + "\\" + networkFileName + ".json"
  packetsFilePath = current_folder + "\\" + packetsFileName + ".json"

  #testing
  print(networkFilePath)
  print(packetsFilePath)

  #loading files
  networkFile = open(networkFilePath)
  packetsFile = open(packetsFilePath)

  return json.load(networkFile), json.load(packetsFile)
