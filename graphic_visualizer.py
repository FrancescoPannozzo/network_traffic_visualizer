""" Graphic visualizer TEST
    use: manim -pql graphic_visualizer.py GraphicVisualizer

"""

import logging
from manim import *
from datetime import timedelta
from utils import traffic_analyzer_utils

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
        networkData, trafficData = traffic_analyzer_utils.file_loader("./data/network", "./data/analyzed_data")

        trafficPercColors = traffic_analyzer_utils.traffic_colors_gen()

        LINK_INDEX = 0
        SWITCH_INDEX = 1
      
        switches = []
        for s in networkData[SWITCH_INDEX]:
            switches.append(s["switchName"])

        logging.debug("switches: %s", switches)
        
        links = []
        EP_A  = 0
        EP_B = 1
        for _, content in networkData[LINK_INDEX].items():
            links.append((content["endpoints"][EP_A], content["endpoints"][EP_B]))

        logging.debug("links: %s", links)

        grafo = Graph(switches, links, labels=True, layout="circular", layout_scale=3,
                      edge_config={"stroke_width": 10, "color":'#05ff00'}
                      )
        
        self.play(Create(grafo)) 
      
        SIM_PAR = 0
        TRAFFIC_DATA = 1
        sim_time = trafficData[SIM_PAR]["simTime"]
        average_delta = trafficData[SIM_PAR]["averageDelta"]
        start_time = trafficData[SIM_PAR]["simStartTime"]
        end_time = start_time + timedelta(seconds=sim_time)
        time_walker = start_time + timedelta(milliseconds=average_delta)
        sim_time_txt = Text(f"sim time = {time_walker}", font_size=24).to_edge(UR).set_color(YELLOW)

        self.add(sim_time_txt)

        while time_walker <= end_time:
            animations = []
            for _, content in trafficData[TRAFFIC_DATA].items():
                color_perc = int(content["traffic"][time_walker])
                animations.append(grafo.edges[(content["endpoints"][EP_A], content["endpoints"][EP_B])].animate.set_color(trafficPercColors[color_perc]["hexValue"]))

            self.play(*animations, Transform(sim_time_txt, Text(f"sim time = {time_walker.strftime('%H:%M:%S')}", font_size=24).to_edge(UR).set_color(YELLOW)),
                      run_time=1)
            time_walker += timedelta(milliseconds=average_delta)

        self.wait(2) 
