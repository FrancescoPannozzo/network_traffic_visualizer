""" Graphic visualizer TEST
    uso: manim -pql graphic_visualizer.py Graphic_visualizer

"""

from manim import *
from network_traffic_visualizer import utils
from network_traffic_visualizer import classes
import logging
from datetime import timedelta

class Graphic_visualizer(Scene):
    """  Crea grafo con etichette """
    def construct(self):
        # Logger config
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                # Adding one handler to manage the messages on a file
                logging.FileHandler('log_manim.txt', mode='w'),
                # Adding one handler to see messages on console
                logging.StreamHandler()
            ]
        )
      
        # load analyzed data file
        networkData, trafficData = utils.file_loader("network", "analyzed_data")

        trafficPercColors = utils.traffic_colors_gen()

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
        simTime = trafficData[SIM_PAR]["simTime"]
        averageDelta = trafficData[SIM_PAR]["averageDelta"]
        startTime = trafficData[SIM_PAR]["simStartTime"]
        endTime = startTime + timedelta(seconds=simTime)
        timeWalker = startTime + timedelta(milliseconds=averageDelta)
        time = Text(f"sim time = {timeWalker}", font_size=24).to_edge(UR).set_color(YELLOW)
        self.add(time)
        
        while timeWalker <= endTime:
            animations = []
            for _, content in trafficData[TRAFFIC_DATA].items():
                colorPerc = int(content["traffic"][timeWalker])
                animations.append(grafo.edges[(content["endpoints"][EP_A], content["endpoints"][EP_B])].animate.set_color(trafficPercColors[colorPerc]["hexValue"]))
                
            self.play(*animations, Transform(time, Text(f"sim time = {timeWalker.strftime('%H:%M:%S')}", font_size=24).to_edge(UR).set_color(YELLOW)), run_time=1)
            timeWalker += timedelta(milliseconds=averageDelta)

        self.wait(2) 
