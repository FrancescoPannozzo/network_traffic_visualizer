""" The class module for the project """

# Link class for manim use, actually only concept
class Link:
    """ Link represents the link object between switch-endpoints """
    linkIDcounter = 0

    def __init__(self, capacity, endpoints):
        """ 
        Keyword arguments:
        capacity: int, the link capacity
        endpoints: List[string], the linked endpoints list  
        """
        self.capacity = capacity
        self.endpoints = endpoints
        Link.linkIDcounter += 1
        self.link_id = Link.linkIDcounter
        self.time_averages = []

    def __str__(self):
        return f"Link ID:{self.link_id}, capacity:{self.capacity}, endpoints:{self.endpoints}"

    def check_endpoints(self, first_endpoint, second_endpoint):
        """ Check if two endpoints are connected to the link object
         
        Keyword arguments:
        first_endpoint: string -- one of the two endpoints to check
        second_endpoint: string -- the other endpoint to check
        
        Returns:
        bool -- True if the two endpoints are linked to the link, False otherwise
        """
        return first_endpoint in self.endpoints and second_endpoint in self.endpoints


class Switch:
    """ Switch represents the switch object """
    switch_id = 0
    def __init__(self, name, address):
        """ 
        Keyword arguments:
        name: string -- the switch name
        address: string -- the switch ip address

        Returns:
        string -- a switch data string representation
         """
        self.name = name
        self.address = address
        Switch.switch_id += 1

    def __str__(self):
        return f"Switch ID:{self.switch_id}, switch name:{self.name}, address:{self.address}"
    
class CustomLabeledDot():

    def __init__(self, labeled_dot, name):
        self.labeled_dot = labeled_dot
        self.name = name
    
    def __str__(self):
        return f"Switch name:{self.name}"
    
    def get_switch_name(self):
         return self.name
    
    def get_labeled_dot(self):
        return self.labeled_dot