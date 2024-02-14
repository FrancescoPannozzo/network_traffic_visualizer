""" Graphic visualizer TEST"""

from manim import *

class graphicVisualizer(Scene):
    """  Crea grafo con etichette numeriche e una testuale """
    def construct(self):
      
        # load analyzed data file
        

        vertices = ["s", 2, 3, 4]
        edges = [("s", 2), (2, 3), (3, 4), ("s", 3), ("s", 4)]
        g = Graph(vertices, edges, labels=True, layout="circular")
        #self.add(g)
        self.play(Create(g))
        self.wait(1)