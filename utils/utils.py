""" Traffic analyzer utils """

from datetime import timedelta, datetime
from utils import exceptions
import logging
import os
import sys
import math
import yaml
import json

def file_loader(file_name, extension):
    """ Load the configuration files 

    Keyword arguments:
    file_name: string
        file name generated by config_gen.py script

    Returns
    list -- the loaded data list 
    """
    
    #Getting absolute path from the running software directory
    current_folder = os.getcwd()
    #Abs path plus filename
    network_file_path = current_folder + "\\" + file_name + "." + extension

    # Open and parse the YAML file
    try:
        if extension == "json":
            with open(network_file_path, "r", encoding="utf-8") as data_file:
                data = json.load(data_file)
        else:
            with open(network_file_path, "r", encoding="utf-8") as data_file:
                data = yaml.safe_load(data_file)
    except FileNotFoundError as e:
        print(f"Warning, error with the provided file name, error: {e}")
        sys.exit(1)

    return data

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

    logging.debug("Traffic percetages:")
    for link, content in links.items():
        logging.debug("link: %s", link)
        for i in content["traffic"]:
            # Max traffic per fractional unit
            max_traffic_pu = max_traffic_per_unit(content['capacity'], update_delta)
            logging.debug(
                "updateTime: %s, delta traffic: %d, percentage: %f %%",
                i['updateTime'],
                i['traffic'],
                get_average(i['traffic'], average_fractions, max_traffic_pu)
            )

def max_traffic_per_unit(capacity, update_delta):
    """ Calculate the max traffic per fractional unit time
    
    Keyword arguments:
    capacity: int, link capacity
    update_delta: int, number of fractional units

    Returns:
    float -- the max traffic per fractional unit time
    """
    time_units_per_sec = timedelta(seconds=1)/update_delta
    return ((capacity * 1e6) / 8) / time_units_per_sec

    
def switches_aspect_ratio(switch_number):
    side = math.sqrt(switch_number)
    
    cols = math.ceil(side * 3/4)
    rows = int(side * 4/3)

    print("cols:%d, rows:%d", cols, rows)

def get_test_duration(start_time):
    end_time = datetime.now()
    duration = end_time - start_time
    
    return f"Test duration:{duration}"

def check_sim_setup(setup):
    """ Check if the sim_setup.yaml file is properly written """
    logger = logging.getLogger()

    try:
        datetime.strptime(str(setup["startSimTime"]), "%Y-%m-%d %H:%M:%S")

        if setup["packetSize"] not in range(1, 4001):
            raise exceptions.CustomFileError("WARNING, packetSize must be in range 1 - 4000")
        if setup["colorblind"] not in ["yes", "no"]:
            raise exceptions.CustomFileError("WARNING, \"colorBlind\" key mus be \"yes\" or \"no\"")
        if setup["dotsSize"] not in ["adaptive", "fixed"]:
            raise exceptions.CustomFileError("WARNING, \"dotSize\" mus be \"adaptive\" or \"fixed\"")
        if setup["packetsFile"] == "yaml" and setup["readeblePackets"] not in ["yes", "no"]:
            raise exceptions.CustomFileError("WARNING, \"readeblePackets\" must be in \"yes\" or \"not\"")
        if setup["trafficVariation"] not in [5, 10, 20, 25, 50, "random"]:
            raise exceptions.CustomFileError("WARNING \"trafficVariation\" must be one of [5, 10, 20 ,25, 50] values")
    except ValueError as ve:
        logger.error("%s: value not properly written, pleas check the README", ve)
        sys.exit()
    except KeyError as ke:
        logger.error("%s key not valid, please check the README", ke)
        sys.exit()
    except exceptions.CustomFileError as ce:
        logger.error(ce)
        sys.exit()

def check_network_sim_setup(setup):
    logger = logging.getLogger()

    try:
        datetime.strptime(str(setup["startSimTime"]), "%Y-%m-%d %H:%M:%S")

        if setup["graphType"] not in ["mesh", "torus", "graph", "complete"]:
            raise exceptions.CustomFileError("WARNING, \"graphType\" not valid, please check the README")
        if setup["colorblind"] not in ["yes", "no"]:
            raise exceptions.CustomFileError("WARNING, \"colorBlind\" key mus be \"yes\" or \"no\"")
        if setup["dotsSize"] not in ["adaptive", "fixed"]:
            raise exceptions.CustomFileError("WARNING, \"dotSize\" mus be \"adaptive\" or \"fixed\"")
        if setup["linkCap"] not in [10, 100, 1000, 10000, 100000]:
            raise exceptions.CustomFileError("WARNING, \"linkCap\" mus be one of [10, 100, 1000, 10000, 100000]")
    
    except exceptions.CustomFileError as ce:
        logger.error(ce)
        sys.exit()


def str_to_datetime(str_date):
    packet_timestamp = None
    if len(str_date) == 19:
        packet_timestamp = datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S")
    else:
        packet_timestamp = datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S.%f")
    
    return packet_timestamp