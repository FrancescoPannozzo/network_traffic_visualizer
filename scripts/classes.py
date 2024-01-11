# myclasses.py

class Link:
    cap = 100

    def __init__(self, capacity, endpoints):
      self.capacity = capacity
      self.endpoints = endpoints
      self.trafficPerc = 0

    def getEndpoints(self):
      return self.endpoints

    def __str__(self):
      return f"Link with endpoint:{self.endpoints}, capacity:{self.capacity}, trafficPercentage:{self.getTrafficPerc()}"
    
    def setCap(self, newCap):
      self.capacity = newCap
    
    def checkEndpoints(self, firstEndpoint, secondEndpoint):
      return firstEndpoint in self.endpoints and secondEndpoint in self.endpoints
    
    def setTrafficPerc(self, trafficPerc):
      self.trafficPerc = trafficPerc

    def getTrafficPerc(self):
      return self.trafficPerc

class Switch:
  def __init__(self, name, address, connectedTo):
    self.name = name
    self.address = address
    self.connectedTo = connectedTo

  def __str__(self):
    return f"Switch name:{self.name}, address:{self.address}, connectedTo:{self.connectedTo}"
