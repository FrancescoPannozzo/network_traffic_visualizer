""" Manim playground """

import logging
from manim import *

class Graphic_visualizer(Scene):


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
        # Dati per il grafo
        

        circle = Circle(color=PINK)
        square = Square()
        nodi = [circle, square]
        archi = [(circle, square)]

        vertex_config = {
            square: {"fill_color": YELLOW},
            circle: {"fill_color": PINK}}

        # Crea un grafo
        grafo = Graph(nodi, archi, layout="circular", labels=True, layout_scale=3,
                      vertex_config=vertex_config)
        logging.debug("graph is type of:%s",grafo[circle])

        grafo.edges[(circle, square)].set_stroke(color=GREEN, width=20)
       
        logging.debug("grafo.edges[(circle, square)] is: %s", grafo.edges[(circle, square)])

        #FFF633
        self.play(Create(grafo))
        self.play(grafo.edges[(circle, square)].animate.set_color('#ffe100'), run_time=2)
        self.play(grafo.edges[(circle, square)].animate.set_color(RED), run_time=2)
        self.wait(2)

       
class DifferentRotations(Scene):
    def construct(self):
        left_square = Square(color=BLUE, fill_opacity=0.7).shift(2 * LEFT)
        right_square = Square(color=GREEN, fill_opacity=0.7).shift(2 * RIGHT)
        self.play(
            left_square.animate.rotate(PI), Rotate(right_square, angle=PI), run_time=2
        )
        self.wait()

class Switch(Circle):
    """ Switch represents the switch object """
    def __init__(self, name, address):
        """ 
        Keyword arguments:
        name: string -- the switch name
        address: string -- the switch ip address

        Returns:
        string -- a switch data string representation
         """
        self.name = name
        self.address = address

    def __str__(self):
        return f"Switch name:{self.name}, address:{self.address}"


class Test(Scene):
    def construct(self):
        """ circle = Circle(color=YELLOW)
        self.add(circle)
        self.wait() """

        switch1 = Switch("switch1", "123.123.123.1")
        switch2 = Switch("switch2", "123.123.123.2")
        nodi = [switch1.name, switch2.name]
        archi = [(switch1.name, switch2.name)]

        # Crea un grafo
        grafo = Graph(nodi, archi, layout="circular", labels=True, layout_scale=3,
                      vertex_config={switch1.name: {"fill_color": RED}, switch2.name: {"fill_color": YELLOW}})
        logging.debug("graph is type of:%s",grafo[switch1.name])

        grafo.edges[(switch1.name, switch2.name)].set_stroke(color=GREEN, width=20)
       
        logging.debug("grafo.edges[(switch1, switch2)] is: %s", grafo.edges[(switch1.name, switch2.name)])

        self.play(Create(grafo))
        self.play(grafo.edges[(switch1.name, switch2.name)].animate.set_color('#FFF633'), run_time=2)
        self.play(grafo.edges[(switch1.name, switch2.name)].animate.set_color(RED), run_time=2)
        self.wait(2)



