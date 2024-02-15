""" Graphic visualizer TEST
    uso: manim -pql graphic_visualizer.py Graphic_visualizer

"""

from manim import *
from network_traffic_visualizer import utils

class Graphic_visualizer(Scene):
    """  Crea grafo con etichette """
    def construct(self):
      
        # load analyzed data file
        networkData, packetsData = utils.file_loader("network", "analyzed_data")

        """
        vertices = ["s", 2, 3, 4]
        edges = [("s", 2), (2, 3), (3, 4), ("s", 3), ("s", 4)]
        g = Graph(vertices, edges, labels=True, layout="circular")
        #self.add(g)
        self.play(Create(g))
        self.wait(1) 
        """

        LINK_INDEX = 0
        SWITCH_INDEX = 1
        switches = []
        for s in networkData[SWITCH_INDEX]:
            switches.append(s["switchName"])
        links = []

        for link, content in networkData[LINK_INDEX].items():
            links.append((content["endpoints"][0], content["endpoints"][1]))
        g = Graph(switches, links, labels=True, layout="circular")
        #self.add(g)
        self.play(Create(g))
        self.wait(1) 
        