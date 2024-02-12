from manim import *

class GrafoCircolare(Scene):
    def construct(self):
      vertices = [1, 2, 3, 4, 5, 6, 7, 8]
      edges = [(1, 7), (1, 8), (2, 3), (2, 4), (2, 5),
                (2, 8), (3, 4), (6, 1), (6, 2),
                (6, 3), (7, 2), (7, 4)]
      g = Graph(vertices, edges, layout="circular")
      self.add(g)

