""" Utils module for config_gen.py script """

import argparse
import os
import random
import sys
import math
from datetime import datetime, timedelta
from utils import utils
import yaml


# Update traffic percentage
def change_traffic_perc(traffic_perc):
    """ Change the traffic% by +10% or -10% if CONTROLLED is True.
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
    source_index = random.randint(0, 1)
    dest_index = 1 - source_index
    return {
        "A": endpoints[source_index],
        "B": endpoints[dest_index],
        "t": timewalker,
        "d": packet_size
        }

def create_auto_complete_links(link_cap, switch_number):
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
                        "endpoints": sorted([i, p]),
                        "capacity": link_cap,
                        "trafficPerc": 0
                        }
                    link_id += 1
    return links


def create_auto_mesh_links(link_cap, switch_number):
    data_links = {}
    link_id = 1

    side = math.sqrt(switch_number)
    # 16/9 aspect ratio
    rows = math.ceil(side * (3/4))
    cols = int(side * (4/3))

    if (rows * cols) < switch_number:
        cols += 1

    switches = [[0 for _ in range(cols)] for _ in range(rows)]
    switch_cont = 1
    for r in range(0, rows):
        for c in range(0, cols):
            if(switch_cont > switch_number):
                break
            switches[r][c] = switch_cont
            switch_cont += 1

            if c > 0:
                print(f"link - ({switches[r][c-1]},{switches[r][c]}), linkID: {link_id}")
                data_links[link_id] = not_complete_links_format(switches[r][c-1], switches[r][c], link_cap)
                link_id += 1
            if r > 0:
                print(f"link - ({switches[r-1][c]},{switches[r][c]}), linkID: {link_id}")
                data_links[link_id] = not_complete_links_format(switches[r-1][c], switches[r][c], link_cap)
                link_id += 1
        if(switch_cont > switch_number):
            break
    return data_links, switches

def not_complete_links_format(switch_a, switch_b, link_cap):
    return {
            "endpoints": sorted((switch_a, switch_b)),
            "capacity": link_cap,
            "trafficPerc": 0
            }

def ip_address(groupA, groupB, groupC, groupD):
    return {
        "groupA": groupA,
        "groupB": groupB,
        "groupC": groupC,
        "groupD": groupD
        }

def create_user_mesh_links(user_data):
    mesh = user_data["coordinates"]
    rows = len(mesh)
    cols = len(mesh[0])
    link_id = 1
    data_links = {}
    link_cap = user_data["linkCap"]

    for r in range(0, rows):
        for c in range(0, cols):
            if c > 0:
                if mesh[r][c] != 0 and mesh[r][c-1] != 0:
                    data_links[link_id] = {
                        "endpoints": sorted((mesh[r][c-1], mesh[r][c])),
                        "capacity": link_cap,
                        "trafficPerc": 0
                        }
                    link_id += 1
            if r > 0:
                if mesh[r][c] != 0 and mesh[r-1][c] != 0:
                    data_links[link_id] = {
                        "endpoints": sorted((mesh[r-1][c], mesh[r][c])),
                        "capacity": link_cap,
                        "trafficPerc": 0
                        }
                    link_id += 1

    return data_links

def create_auto_phases(start_time, sim_time):
    setup = utils.file_loader("./data/setup")

    average_delta = setup["averageDelta"]
    phase_intervall = timedelta(milliseconds=1000)
    timewalker = start_time + timedelta(milliseconds=average_delta)
    phases = {}
    phase_count = 1

    while timewalker < start_time + timedelta(seconds=sim_time):
        phases[timewalker] = f"phase{phase_count}"
        phase_count += 1
        timewalker += phase_intervall

    return phases

def create_user_toro_links(user_data):
    links = create_user_mesh_links(user_data)
    toro = user_data["coordinates"]
    rows = len(toro)
    cols = len(toro[0])
    link_cap = user_data["linkCap"]
    links_id = len(links) + 1

    for i in range(cols):
        if toro[0][i] != 0 and toro[rows-1][i] != 0:
            links[links_id] = {
                "endpoints": sorted((toro[0][i], toro[rows-1][i])),
                "capacity": link_cap,
                "trafficPerc": 0
            }
            links_id += 1

    for i in range(rows):
        if toro[i][0] != 0 and toro[i][cols-1] != 0:
            links[links_id] = {
                "endpoints": sorted((toro[i][0], toro[i][cols-1])),
                "capacity": link_cap,
                "trafficPerc": 0
            }
            links_id += 1

    return links

def create_user_graph_links(user_data):
    links = {}
    link_id = 1

    for link in user_data["links"]:
        links[link_id] = {
            "endpoints": sorted(link["endpoints"]),
            "capacity": link["linkCap"],
            "trafficPerc": 0
        }
        link_id += 1
    
    return links



def create_auto_toro_links(link_cap, switch_number):
    links, switches = create_auto_mesh_links(link_cap, switch_number)
    rows = len(switches)
    cols = len(switches[0])
    links_id = len(links) + 1

    linkList = []

    for _, content in links.items():
        linkList.append(content["endpoints"])

    for i in range(cols):
        if switches[0][i] != 0 and switches[rows-1][i] != 0 and [switches[0][i],switches[rows-1][i]] not in linkList:
            links[links_id] = {
                "endpoints": sorted((switches[0][i], switches[rows-1][i])),
                "capacity": link_cap,
                "trafficPerc": 0
            }
            links_id += 1

    for i in range(rows):
        if switches[i][0] != 0 and switches[i][cols-1] != 0 and [switches[i][0], switches[i][cols-1]] not in linkList:
            links[links_id] = {
                "endpoints": sorted((switches[i][0], switches[i][cols-1])),
                "capacity": link_cap,
                "trafficPerc": 0
            }
            links_id += 1

    return links, switches

