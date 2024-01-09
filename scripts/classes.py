# myclasses.py

class Link:
    cap = 100

    def __init__(self, capacity, endpoints):
      self.capacity = capacity
      self.endpoints = endpoints

    def __str__(self):
      return f"Link with endpoint:{self.endpoints}, capacity:{self.capacity}"
    
    def setCap(self, newCap):
      self.capacity = newCap
    
    def checkEndpoints(self, firstEndpoint, secondEndpoint):
      return firstEndpoint in self.endpoints and secondEndpoint in self.endpoints

class Switch:
  def __init__(self, name, address, connectedTo):
    self.name = name
    self.address = address
    self.connectedTo = connectedTo

  def __str__(self):
    return f"Switch name:{self.name}, address:{self.address}, connectedTo:{self.connectedTo}"
