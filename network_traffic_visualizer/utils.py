""" Utils functions """

from datetime import timedelta
import logging
import os
import yaml

def file_loader(network_file_name, packets_file_name):
    """ Load the .yaml configuration files """
     #Getting absolute path from the running software directory
    current_folder = os.getcwd()
    #Abs path plus filename
    network_file_path = current_folder + "\\" + network_file_name + ".yaml"
    packets_file_path = current_folder + "\\" + packets_file_name + ".yaml"

    # Open and parse the YAML file
    with open(network_file_path, "r", encoding="utf-8") as network_file:
        network_data = yaml.safe_load(network_file)

    with open(packets_file_path, "r", encoding="utf-8") as packets_file:
        packets_data = yaml.safe_load(packets_file)

    return network_data, packets_data

def get_average(temp_sum, average_fractions, max_traffic_unit):
    """ Calculate the percentage average """
    return (temp_sum/average_fractions)  *  ( 100 / max_traffic_unit)

def show_updates_data(links):
    """ Show the updates delta time packets sums """
    logging.debug("UpdateDeltaTraffic sums:")
    for link, content in links.items():
        logging.debug("link: %s", link)
        for i in content["updateDeltaTraffic"]:
            logging.debug("updateTime: %s, packets sum: %d", i['updateTime'], i['traffic'])
            
def show_averages_data(links, update_delta, average_fractions):
    """ Show the averages delta time packets sums """
    time_units_per_sec = timedelta(seconds=1)/update_delta
    logging.debug("Traffic percetages:")
    for link, content in links.items():
        logging.debug("link: %s", link)
        for i in content["traffic"]:
            # Max traffic per fractional unit
            max_traffic_per_unit = ((content['capacity'] * 1e6) / 8) / time_units_per_sec
            logging.debug(
                "updateTime: %s, delta traffic: %d, percentage: %f %%",
                i['updateTime'],
                i['traffic'],
                get_average(i['traffic'], average_fractions, max_traffic_per_unit)
            )