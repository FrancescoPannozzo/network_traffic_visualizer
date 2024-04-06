""" Traffic analyzer utils """

from datetime import timedelta, datetime
import logging
import os
import sys
import math
import yaml

def file_loader(file_name):
    """ Load the .yaml configuration files 

    Keyword arguments:
    file_name: string
        file name generated by config_gen.py script

    Returns
    list -- the loaded data list 
    """
    
    #Getting absolute path from the running software directory
    current_folder = os.getcwd()
    #Abs path plus filename
    network_file_path = current_folder + "\\" + file_name + ".yaml"

    # Open and parse the YAML file
    try:
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
