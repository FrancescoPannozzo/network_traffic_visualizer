from manim import *

class Test(Scene):
    def construct(self):
      vertices = ["s", 2, 3, 4]
      edges = [("s", 2), (2, 3), (3, 4), ("s", 3), ("s", 4)]
      g = Graph(vertices, edges, labels=True, layout="circular")
      self.add(g)
