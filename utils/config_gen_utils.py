""" Utils module for config_gen.py script """

import random
import math
from datetime import timedelta
from utils import utils, exceptions
from utils import CONSTANTS as CONST
import sys


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
                    links[link_id] = link_format(i, p, link_cap)
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
                data_links[link_id] = link_format(switches[r][c-1], switches[r][c], link_cap)
                link_id += 1
            if r > 0:
                data_links[link_id] = link_format(switches[r-1][c], switches[r][c], link_cap)
                link_id += 1
        if(switch_cont > switch_number):
            break
    return data_links, switches

def link_format(switch_a, switch_b, link_cap):
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

    if "links" in user_data:
        return create_user_graph_links(user_data)

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
                    data_links[link_id] = link_format(mesh[r][c-1], mesh[r][c], link_cap)
                    link_id += 1
            if r > 0:
                if mesh[r][c] != 0 and mesh[r-1][c] != 0:
                    data_links[link_id] = link_format(mesh[r-1][c], mesh[r][c], link_cap)
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

def extract_custom_links(data_links):
    links = {}

    for l in data_links:
        ep_key = sorted([l["endpoints"][CONST.EP_A], l["endpoints"][CONST.EP_B]])
        links[(ep_key[CONST.EP_A], ep_key[CONST.EP_B])] = l["linkCap"]

    return links

def create_user_toro_links(user_data):

    if "links" in user_data:
        return create_user_graph_links(user_data)

    try:
        toro = user_data["coordinates"]
        link_cap = user_data["linkCap"]
    except KeyError as e:
        print(exceptions.CUSTOM_FILE_ERROR_MSG)
        print(f"{e} missing or badly formatted")

    links = create_user_mesh_links(user_data)
    rows = len(toro)
    cols = len(toro[0])
    links_id = len(links) + 1

    for i in range(cols):
        if toro[0][i] != 0 and toro[rows-1][i] != 0:
            links[links_id] = link_format(toro[0][i], toro[rows-1][i], link_cap)
            links_id += 1

    for i in range(rows):
        if toro[i][0] != 0 and toro[i][cols-1] != 0:
            links[links_id] = link_format(toro[i][0], toro[i][cols-1], link_cap)
            links_id += 1

    return links

def create_user_graph_links(user_data):
    links = {}
    link_id = 1

    try:
        if "linkCap" not in user_data and "links" in user_data:
            for link in user_data["links"]:
                links[link_id] = link_format(link["endpoints"][CONST.EP_A], link["endpoints"][CONST.EP_B], link["linkCap"])
                link_id += 1
        elif "linkCap" in user_data and "links" in user_data:
            link_cap = user_data["linkCap"]
            for link in user_data["links"]:
                links[link_id] = link_format(link[CONST.EP_A], link[CONST.EP_B], link_cap)
                link_id += 1
    except KeyError as e:
        print("WARNING, the custom file seems to be not formatted properly, please read the README for infos")
        print(f"{e} key missing in custom file or not properly formatted")
        sys.exit()

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
            links[links_id] = link_format(switches[0][i], switches[rows-1][i], link_cap)
            links_id += 1

    for i in range(rows):
        if switches[i][0] != 0 and switches[i][cols-1] != 0 and [switches[i][0], switches[i][cols-1]] not in linkList:
            links[links_id] = link_format(switches[i][0], switches[i][cols-1], link_cap)
            links_id += 1

    return links, switches

def check_custom_file(user_data):
    rows = len(user_data["coordinates"])
    cols = len(user_data["coordinates"][0])

    try:
        for row in range(rows):
            for col in range(cols):
                if user_data["coordinates"][row][col] != 0 and user_data["coordinates"][row][col] not in user_data["switches"]:
                    raise exceptions.CustomFileError
    except exceptions.CustomFileError as e:
        print(e)
        print("Switch IDs conflict in custom_graph.yaml file: keys coordinates/switches")
        print("Exiting program now")
        sys.exit()