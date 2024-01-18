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

# Check if a link is already present in links list
def inLinks(links, firstEndopoint, secondEndpoint):
    for l in links:
      if l.checkEndpoints(firstEndopoint, secondEndpoint):
        return True
    return False

# Check and return a link, None if the link is not in links
def getLink(links, firstEndopoint, secondEndpoint):
    for l in links:
      if l.checkEndpoints(firstEndopoint, secondEndpoint):
         return l
    return None
      
def getLinkById(links, linkId):
   for link in links:
    if link.linkId == linkId:
       return link

def getAverage(capacity, tempSum):
   return (tempSum * 100) / ((capacity * 1e6) / 8)