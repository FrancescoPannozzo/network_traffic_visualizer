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
    """ A check function for parser method add_argument(). Check user input switch number parameter 
    
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
    """A check function for parser method add_argument(). Check user input links capacity parameter 
    
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
    """ Change the traffic% by +10% or -10% if CONTROLLED is True
        Random value (0, 100) otherwise
    
    Keyword Arguments:
    traffic_perc -- a traffic perc value

    Returns:
    int -- a new traffic perc value
    """
    CONTROLLED = False

    if CONTROLLED:
        new_traffic_perc = traffic_perc
        if random.randint(0, 1) == 1:
            if new_traffic_perc < 100:
                new_traffic_perc += 10
        else:
            if new_traffic_perc > 0:
                new_traffic_perc -= 10
    else:
        new_traffic_perc = random.randint(0, 100)
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

def create_complete_links(link_cap, switch_number):
    """ Create links for a complete graph 
    
    Key arguments:
    link_cap: int -- link capacity
    switch_number: int -- switch number

    Returns
    dict -- links representation
    """
    # The arcs representing the links connecting the switches (nodes)
    links = {}
    # The link ID counter
    link_id = 1

    for i in range(1, switch_number + 1):
        for p in range(i, switch_number + 1):
            if i != p:
                if link_id not in links:
                    links[link_id] = {
                        "endpoints": [i, p],
                        "capacity": link_cap,
                        "trafficPerc": 0
                        }
                    link_id += 1
    return links

def create_not_complete_links(link_cap, switch_number):
    """ Create links for a complete graph 
    
    Key arguments:
    link_cap: int -- link capacity
    switch_number: int -- switch number
    creation_perc: in -- percentage links creation

    Returns
    dict -- links representation
    """
    data_links = {}
    # The arcs representing the links connecting the switches (nodes)
    links = []
    # The link ID counter
    link_id = 1

    for i in range(1, switch_number + 1):
        adiacenti_possibili = [s for s in range(1, switch_number+1) if s != i]
        #print(f"----- adiacenti possibili per nodo {i}:", adiacenti_possibili)
        n_adiacenti = random.randint(1, len(adiacenti_possibili))
        #print(f"----- nodo {i} avrà {n_adiacenti} adiacenti")
        for _ in range(1, n_adiacenti+1):
            scelto = random.choice(adiacenti_possibili)
            if sorted([i, scelto]) not in links:
                links.append(sorted([i, scelto]))
            adiacenti_possibili.remove(scelto)

    links = sorted(links)

    for l in links:
        data_links[link_id] = {
            "endpoints": l,
            "capacity": link_cap,
            "trafficPerc": 0
            }
        link_id += 1

    return data_links
