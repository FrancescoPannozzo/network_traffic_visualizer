""" Utils functions """

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
