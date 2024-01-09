import os
import yaml

#load the .json configuration files
def fileLoader(networkFileName, packetsFileName):
  #Getting absolute path from the running software directory
  current_folder = os.getcwd()
  #Abs path plus filename
  networkFilePath = current_folder + "\\" + networkFileName + ".yaml"
  packetsFilePath = current_folder + "\\" + packetsFileName + ".yaml"

  #testing
  print(networkFilePath)
  print(packetsFilePath)

  # Open and parse the YAML file
  with open(networkFilePath, "r") as networkFile:
      networkData = yaml.safe_load(networkFile)

  with open(packetsFilePath, "r") as packetsFile:
      packetsData = yaml.safe_load(packetsFile)

  return networkData, packetsData
