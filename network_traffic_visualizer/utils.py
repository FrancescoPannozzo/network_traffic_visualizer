""" Utils functions """

from datetime import timedelta
import logging
import os
import sys
import yaml

def file_loader(network_file_name, packets_file_name):
    """ Load the .yaml configuration files 

    Keyword arguments:
    network_file_name: string
        the network file name generated by config_gen.py script
    packets_file_name: string
        the packets file name generated by config_gen.py script

    Returns
    list, list -- the loaded network and packets data list 
    """
    
    #Getting absolute path from the running software directory
    current_folder = os.getcwd()
    #Abs path plus filename
    network_file_path = current_folder + "\\" + network_file_name + ".yaml"
    packets_file_path = current_folder + "\\" + packets_file_name + ".yaml"

    # Open and parse the YAML file
    try:
        with open(network_file_path, "r", encoding="utf-8") as network_file:
            network_data = yaml.safe_load(network_file)

        with open(packets_file_path, "r", encoding="utf-8") as packets_file:
            packets_data = yaml.safe_load(packets_file)
    except FileNotFoundError as e:
        print(f"Warning, error with the provided file name, error: {e}")
        sys.exit(1)

    return network_data, packets_data

def get_average(temp_sum, average_fractions, max_traffic_unit):
    """ Calculate the percentage average 
    
    Keyword arguments:
    average_fractions: int, number of fractional units per averageDeltaTime
    max_traffic_unit: int, max traffic per fractional unit

    Returns:
    float -- percentage average
    """
    return (temp_sum/average_fractions)  *  ( 100 / max_traffic_unit)

def show_updates_data(links):
    """ Show the updates delta time packets sums 
    
    Keyword arguments:
    links: dict, a links dictionary representation
    """
    logging.debug("UpdateDeltaTraffic sums:")
    for link, content in links.items():
        logging.debug("link: %s", link)
        for i in content["updateDeltaTraffic"]:
            logging.debug("updateTime: %s, packets sum: %d", i['updateTime'], i['traffic'])

def show_averages_data(links, update_delta, average_fractions):
    """ Show the averages delta time packets sums 
    
    Keyword arguments:
    update_delta: int, update delta time (milliseconds)
    average_fractions: int, number of fractional units
    """
    #time_units_per_sec = timedelta(seconds=1)/update_delta
    logging.debug("Traffic percetages:")
    for link, content in links.items():
        logging.debug("link: %s", link)
        for i in content["traffic"]:
            # Max traffic per fractional unit
            # max_traffic_per_unit = ((content['capacity'] * 1e6) / 8) / time_units_per_sec
            max_traffic_pu = max_traffic_per_unit(content['capacity'], update_delta)
            logging.debug(
                "updateTime: %s, delta traffic: %d, percentage: %f %%",
                i['updateTime'],
                i['traffic'],
                get_average(i['traffic'], average_fractions, max_traffic_pu)
            )

def max_traffic_per_unit(capacity, update_delta):
    time_units_per_sec = timedelta(seconds=1)/update_delta
    return ((capacity * 1e6) / 8) / time_units_per_sec

def rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def traffic_colors_gen():
    MID_TRAFFIC = 50
    MAX_TRAFFIC = 100
    #percColors = {}
    hexColors = {}
    r = 0
    g = 255
    b = 0

    for i in range(0, MAX_TRAFFIC+1):
        if i <= MID_TRAFFIC:
            r += 5
        else:
            g -= 5
        #percColors[i] = {"r":r, "g":g, "b":b}
        hexColors[i] = {"hexValue": rgb_to_hex(r, g, b)}
    
    return hexColors