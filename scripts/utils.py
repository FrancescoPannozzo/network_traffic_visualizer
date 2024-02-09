""" Utils module for config_gen.py script """

import argparse
import random
import sys


# Argparse function to insert file config parameters
def get_input_parameters():
    """ Setting the command line option to set the switch number and the switch-links capacity """
    parser = argparse.ArgumentParser()
    parser.add_argument("switchNumber", type=check_switch, 
                        help="The switch number you want to create (2 - 1000)")
    parser.add_argument("linkCapacity", type=check_link,
                        help="The switch-link capacity (MB), allowed values: 10, 100, 1000")
    args = parser.parse_args()
    return args

def check_switch(value):
    """ Check user input switch number parameter """
    ivalue = int(value)
    if ivalue < 2 or ivalue > 1000:
        print(f"{value} in not valid. Value must be in range 2 - 1000.")
        sys.exit(1)
    return ivalue

def check_link(value):
    """ Check user input links capacity parameter """
    ivalue = int(value)
    valid_cap = {10, 100, 1000}
    if ivalue not in valid_cap:
        print(f"{value} in not valid. Value must be one of these value: [10, 100, 1000].")
        sys.exit(1)
    return ivalue



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

def ip_to_string(ip):
    """ Write an ip string rappresentation from passed ip dict """
    return f"{ip['groupA']}.{ip['groupB']}.{ip['groupC']}.{ip['groupD']}"
