class Switch:
  def __init__(self, switchName, ipAddress, connectedTo):
    self.switchName = switchName
    self.ipAddress = ipAddress
    self.connectedTo = connectedTo.copy()