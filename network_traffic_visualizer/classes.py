class Switch2:
  def __init__(self, switchName, ipAddress, connectedTo):
    self.switchName = switchName
    self.ipAddress = ipAddress
    self.connectedTo = connectedTo.copy()

class Link:
  cap = 100

  def __init__(self, capacity, endpoints):
    self.capacity = capacity
    self.endpoints = endpoints
    self.traffic = []

  def __str__(self):
    return f"Link with endpoint:{self.endpoints}, capacity:{self.capacity}"
  
  def setCap(newCap):
    Link.cap = newCap

class Switch:
  def __init__(self, name, address, connectedTo):
    self.name = name
    self.address = address
    self.connectedTo = connectedTo

  def __str__(self):
    return f"Switch name:{self.name}, address:{self.address}, connectedTo:{self.connectedTo}"