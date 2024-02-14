""" Utils module for config_gen.py script """

import argparse
import random
import sys


# Argparse function to insert file config parameters
def get_input_parameters():
    """ Setting the command line option to set the switch number and the switch-links capacity
    Returns:
    args Namespace, Namespace object containing extracted data
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("switchNumber", type=check_switch,
                        help="The switch number you want to create (2 - 1000)")
    parser.add_argument("linkCapacity", type=check_link,
                        help="The switch-link capacity (MB), allowed link_numbers: 10, 100, 1000")
    args = parser.parse_args()
    return args

def check_switch(switch_number):
    """ A check function for method add_argument(). Check user input switch number parameter 
    
    Keyword arguments:
    switch_number: int, the switches number

    Returns:
    int -- a checked switches number
    """
    i_switch_number = int(switch_number)
    if i_switch_number < 2 or i_switch_number > 1000:
        print(f"{switch_number} in not valid. link_number must be in range 2 - 1000.")
        sys.exit(1)
    return i_switch_number

def check_link(link_number):
    """A check function for method add_argument(). Check user input links capacity parameter 
    
    Keyword arguments:
    link_number: int -- the links number

    Returns:
    int -- a checked links number
    """
    i_link_number = int(link_number)
    valid_cap = {10, 100, 1000}
    if i_link_number not in valid_cap:
        print(f"{link_number} not valid, must be one of these link_number: [10, 100, 1000].")
        sys.exit(1)
    return i_link_number



# Update traffic percentage
def change_traffic_perc(traffic_perc):
    """ Change the traffic% by +10% or -10% 
    
    Keyword Arguments:
    traffic_perc -- a traffic perc value

    Returns:
    int -- a new traffic perc value
    """
    new_traffic_perc = traffic_perc
    if random.randint(0, 1) == 1:
        if new_traffic_perc < 100:
            new_traffic_perc += 10
    else:
        if new_traffic_perc > 0:
            new_traffic_perc -= 10
    return new_traffic_perc

def ip_to_string(ip):
    """ Write an ip string rappresentation from passed ip dict 
    
    Keyword arguments:
    ip: dict -- dict representation about an ip address
    
    Returns:
    string -- the ip string representation
    """
    return f"{ip['groupA']}.{ip['groupB']}.{ip['groupC']}.{ip['groupD']}"

def create_packet(ep_a, ep_b, timewalker, packet_size):
    """ Create a packet with random endpoint positioning 
    
    Key arguments:
    ep_a: string -- a link endpoint
    ep_b: string -- the other link endpoint
    timewalker: datetime -- packet timestamp
    packet_size: int -- packet payload size (Bytes)

    Returns:
    dict -- packet representation
    """
    endpoints = [ep_a, ep_b]
    source_ndex = random.randint(0, 1)
    dest_index = 1 - source_ndex
    return {
        "epA": endpoints[source_ndex],
        "epB": endpoints[dest_index],
        "timest": timewalker,
        "dim": packet_size
        }
