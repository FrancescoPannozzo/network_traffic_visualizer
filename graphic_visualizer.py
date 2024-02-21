""" Graphic visualizer
    use: 
    rendering 854x480 15FPS: manim -pql graphic_visualizer.py GraphicVisualizer
    rendering 1280x720 60FPS: manim -pqm --fps 60 graphic_visualizer.py GraphicVisualizer

"""

import logging
from datetime import timedelta
from manim import *
from utils import utils

class GraphicVisualizer(Scene):
    """  Graph creator """
    def construct(self):
        # Logger config
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                # Adding one handler to manage the messages on a file
                logging.FileHandler('./log_files/graphic_visualizer_log.txt', mode='w'),
                # Adding one handler to see messages on console
                logging.StreamHandler()
            ]
        )
      
        # load analyzed data file
        network_data, traffic_data = utils.file_loader("./data/network", "./data/analyzed_data")
        # assign traffic colors
        traffic_perc_colors = utils.traffic_colors_gen()
        # network_data link index
        LINK_INDEX = 0
        # network_data switch index
        SWITCH_INDEX = 1
        # extracting switches data
        switches = []
        for s in network_data[SWITCH_INDEX]:
            switches.append(s["switchName"])

        logging.debug("switches: %s", switches)
        
        # extracting links data
        links = []
        EP_A  = 0
        EP_B = 1
        for _, content in network_data[LINK_INDEX].items():
            links.append((content["endpoints"][EP_A], content["endpoints"][EP_B]))

        logging.debug("links: %s", links)

        # graph creation
        ZERO_TRAFFIC = '#05ff00'
        grafo = Graph(switches, links, labels=True, layout="circular", layout_scale=3,
                      edge_config={"stroke_width": 20, "color":ZERO_TRAFFIC}
                      )
        self.play(Create(grafo)) 

        # traffic_data simulation parameters index
        SIM_PAR = 0
        # traffic_data traffic data index
        TRAFFIC_DATA = 1
        sim_time = traffic_data[SIM_PAR]["simTime"]
        average_delta = traffic_data[SIM_PAR]["averageDelta"]
        start_time = traffic_data[SIM_PAR]["simStartTime"]
        end_time = start_time + timedelta(seconds=sim_time)
        # show_delta is the time range we want to update the visualization
        show_delta = traffic_data[SIM_PAR]["updateDelta"]
        # time index to analyze
        time_walker = start_time + timedelta(milliseconds=average_delta)
        # the sim time to visualize
        sim_time_txt = Text(f"sim time = {time_walker}", font_size=24).to_edge(UR).set_color(YELLOW)

        self.add(sim_time_txt)

        # creating traffic animations
        while time_walker <= end_time:
            # temp LabeledDot structure
            animations = []
            # definig all the traffic color links at timeWalker time
            for _, content in traffic_data[TRAFFIC_DATA].items():
                color_perc = int(content["traffic"][time_walker])
                animations.append(grafo.edges[(content["endpoints"][EP_A], content["endpoints"][EP_B])].animate.set_color(traffic_perc_colors[color_perc]["hexValue"]))
            # playing animations
            self.play(*animations, Transform(sim_time_txt,
                                                Text(f"sim time = {time_walker.strftime('%H:%M:%S.%f')[:-3]}",
                                                font_size=24).to_edge(UR).set_color(YELLOW)),
                                                run_time=1
                                            )
            # pushing forward sim time to check
            time_walker += timedelta(milliseconds=show_delta)
        self.wait(2)
