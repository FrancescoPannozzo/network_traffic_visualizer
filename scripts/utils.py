""" Utils module for config_gen.py script """

import argparse
import random


# Argparse function to insert file config parameters
def get_input_parameters():
    """ Setting the command line option to set the switch number and the switch-links capacity """
    parser = argparse.ArgumentParser()
    parser.add_argument("switchNumber", type=int, help="The switch number you want to create")
    parser.add_argument("linkCapacity", type=int,
                        help="The switch-link capacity (MB) you want to load")
    args = parser.parse_args()
    return args

# Update traffic percentage
def change_traffic_perc(traffic_perc):
    """ Change the traffic% by +10% or -10% """
    new_traffic_perc = traffic_perc
    if random.randint(0, 1) == 1:
        if new_traffic_perc < 100:
            new_traffic_perc += 10
    else:
        if new_traffic_perc > 0:
            new_traffic_perc -= 10
    return new_traffic_perc
