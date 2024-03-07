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