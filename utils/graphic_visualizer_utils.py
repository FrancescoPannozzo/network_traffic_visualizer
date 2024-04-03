" Graphic visualizer utils"

from manim import *
from datetime import datetime

def get_test_duration(start_time):
    end_time = datetime.now()
    duration = end_time - start_time
    
    return f"Test duration:{duration}"

def set_sim_infos(infos, font_size):
    start_time = f"start sim time: {infos['simStartTime']}\n"
    sim_time = f"sim time: {infos['simTime']} secs\n"
    average_delta = f"average delta: {infos['averageDelta']} ms\n"
    update_delta = f"update delta: {infos['updateDelta']} ms"
    infos = Text(f"{start_time}{sim_time}{average_delta}{update_delta}", font="Courier New", font_size=(font_size/2)+2).set_color(YELLOW)

    return infos

def traffic_colors_gen(r, g, b):
    """ A traffic colors generator, green to yellow to red 

    Returns:
    dict -- a dictionary with keys as percentage number and values as hex color
    """
    MID_TRAFFIC = 50
    MAX_TRAFFIC = 100
    hexColors = {}

    for i in range(0, MAX_TRAFFIC+1):
        if i <= MID_TRAFFIC:
            r += 5
        else:
            g -= 5
        hexColors[i] = {"hexValue": hex_converter(r, g, b)}
    
    return hexColors

def traffic_colors_gen_colorblind():
    MID_TRAFFIC = 50
    MAX_TRAFFIC = 100
    hexColors = {}
    r = 255
    g = 255
    b = 255

    for i in range(0, MAX_TRAFFIC+1):
        if i <= MID_TRAFFIC:
            r -= 5
            b -= 5
        else:
            r += 5
            g -= 5
            b += 5
        hexColors[i] = {"hexValue": hex_converter(r, g, b)}
    
    return hexColors


def hex_converter(r, g, b):
    """ Translate r, g, b code in hex format
    
    Returns:
    string -- hex color string representation
    """
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)