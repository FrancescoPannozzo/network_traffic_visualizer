# myclasses.py

class Link:
    cap = 100
    linkIDcounter = 0

    def __init__(self, capacity, endpoints):
      self.capacity = capacity
      self.endpoints = endpoints
      self.trafficPerc = 0
      Link.linkIDcounter += 1
      self.linkId = Link.linkIDcounter

    def __str__(self):
      return f"Link ID:{self.linkId}, endpoints:{self.endpoints}, capacity:{self.capacity}, trafficPercentage:{self.trafficPerc}"
    
    def checkEndpoints(self, firstEndpoint, secondEndpoint):
      return firstEndpoint in self.endpoints and secondEndpoint in self.endpoints

class Switch:
  def __init__(self, name, address):
    self.name = name
    self.address = address

  def __str__(self):
    return f"Switch name:{self.name}, address:{self.address}"
