""" Graphic visualizer
    use: 
    rendering 854x480 15FPS: manim -pql graphic_visualizer.py GraphicVisualizer
    rendering 1280x720 60FPS: manim -pqm --fps 60 graphic_visualizer.py GraphicVisualizer

"""

import logging
from datetime import timedelta
from manim import *
from utils import utils

class GraphicVisualizer(MovingCameraScene):
    """  Graph creator """
    def construct(self):
        
        # Logger config
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                # Adding one handler to manage the messages on a file
                logging.FileHandler('./log_files/graphic_visualizer_log_matrix.txt', mode='w'),
                # Adding one handler to see messages on console
                logging.StreamHandler()
            ]
        )
      
        # load analyzed data file
        network_data, traffic_data = utils.file_loader("./data/network", "./data/analyzed_data_matrix")
        # assign traffic colors
        traffic_perc_colors = utils.traffic_colors_gen()
        # network_data link index
        LINK_INDEX = 0
        # network_data switch index
        SWITCH_INDEX = 1
        # extracting switches data
        switches = []
        for s in network_data[SWITCH_INDEX]:
            switches.append(s["switchID"])

        logging.debug("switches: %s", switches)
        
        # extracting links data
        links = []
        EP_A  = 0
        EP_B = 1
        LINK_DATA = 1
        for _, content in traffic_data[LINK_DATA].items():
            links.append((content["endpoints"][EP_A], content["endpoints"][EP_B]))

        logging.debug("links: %s", links)

        # graph creation
        ZERO_TRAFFIC = '#05ff00'
        grafo = Graph(switches, links, labels=True, layout="circular", vertex_config={"color":BLUE},
                      edge_config={"stroke_width": 10, "color":ZERO_TRAFFIC}
                      )
        


        # traffic_data simulation parameters index
        SIM_PAR = 0
        # traffic_data traffic data index
        TRAFFIC_DATA = 1
        sim_time = traffic_data[SIM_PAR]["simTime"]
        average_delta = traffic_data[SIM_PAR]["averageDelta"]
        start_time = traffic_data[SIM_PAR]["simStartTime"]
        end_time = start_time + timedelta(seconds=sim_time)
        update_delta = traffic_data[SIM_PAR]["updateDelta"]
        # show_delta is the time range we want to update the visualization
        show_delta = traffic_data[SIM_PAR]["updateDelta"]
        # time index to analyze
        time_walker = start_time + timedelta(milliseconds=average_delta)
        # the sim time to visualize
        sim_time_txt = Text(f"SIM TIME: {time_walker.strftime('%H:%M:%S.%f')[:-3]}", font_size=24).set_color(YELLOW)
        
        self.play(Create(grafo))
        sim_time_txt.next_to(grafo, UP)
        self.add(sim_time_txt)
        self.play(self.camera.auto_zoom([grafo, sim_time_txt], margin=1), run_time=0.5)
       
        perc_traffic_index = 0

        # creating traffic animations
        while time_walker <= end_time:
            # temp LabeledDot structure
            animations = []
            # definig all the traffic color links at timeWalker time
            for _, content in traffic_data[TRAFFIC_DATA].items():
                color_perc = int(content["traffic"][perc_traffic_index])
                animations.append(grafo.edges[(content["endpoints"][EP_A], content["endpoints"][EP_B])].animate.set_color(traffic_perc_colors[color_perc]["hexValue"]))
            perc_traffic_index += 1
            # playing animations
            self.play(*animations, Transform(sim_time_txt,
                                                Text(f"SIM TIME: {time_walker.strftime('%H:%M:%S.%f')[:-3]}",
                                                font_size=24).next_to(grafo, UP).set_color(YELLOW)),
                                                run_time=1
                                            )
            # pushing forward sim time to check
            time_walker += timedelta(milliseconds=show_delta)

        
        self.wait(2)
