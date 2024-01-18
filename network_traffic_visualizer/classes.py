# myclasses.py

class Link:
    cap = 100
    linkIDcounter = 0

    def __init__(self, capacity, endpoints):
      self.capacity = capacity
      self.endpoints = endpoints
      Link.linkIDcounter += 1
      self.linkId = Link.linkIDcounter
      self.timeAverages = []

    def __str__(self):
      return f"Link ID:{self.linkId}, capacity:{self.capacity}, endpoints:{self.endpoints}"
    
    def checkEndpoints(self, firstEndpoint, secondEndpoint):
      return firstEndpoint in self.endpoints and secondEndpoint in self.endpoints
    
    def getTimeAverages(self):
      return f"{str(self)}, timeAverages:{self.timeAverages}"

class Switch:
  def __init__(self, name, address, connectedTo):
    self.name = name
    self.address = address
    self.connectedTo = connectedTo

  def __str__(self):
    return f"Switch name:{self.name}, address:{self.address}, connectedTo:{self.connectedTo}"
