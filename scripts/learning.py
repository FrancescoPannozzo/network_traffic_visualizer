""" Manim playground """

import logging
from manim import *
import random

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

class Graphic_visualizer(Scene):
    def construct(self):

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

        grafo.edges[(circle, square)].set_stroke(color=GREEN, width=30)
       
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

class Switch():
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
                      vertex_config={switch1.name: {"fill_color": RED, "radius": 0.5}, switch2.name: {"fill_color": YELLOW}})
        logging.debug("graph elements is type of:%s",grafo[switch1.name])

        #grafo[switch1.name].label = Tex("test", "font_size"=10)
      
        grafo.edges[(switch1.name, switch2.name)].set_stroke(color=GREEN, width=30)
       
        logging.debug("grafo.edges[(switch1, switch2)] is: %s", grafo.edges[(switch1.name, switch2.name)])

        self.play(Create(grafo))
        #self.play(grafo.edges[(switch1.name, switch2.name)].animate.set_color('#FFF633'), run_time=2)
        #self.play(grafo.edges[(switch1.name, switch2.name)].animate.set_color(RED), run_time=2)

        #self.wait(2)

class Dots(Scene):
    def construct(self):

        t1 = Tex("test", color=RED)
        t1.font_size = 60
        self.add(t1)
        l1 = LabeledDot(t1)
        l1.next_to(t1, UL)
        self.add(l1)

class CustomGraph(Scene):
    def construct(self):
        
        t1 = Tex("n1", color=RED)
        t1.font_size = 20
        n1 = LabeledDot(t1)
        n2 = LabeledDot(Tex("n2", color=BLUE))

        n3 = LabeledDot(Tex("wow"), color=GREEN)
        nodi = [n1, n2]
        archi = [(n1, n2)]
        n1.move_to(UP * 2)
        n2.next_to(n1)
        self.add(n1, n2)

        switches = []
        SWITCH_NUMBER = 10
        for i in range(1, SWITCH_NUMBER+1):
            switches.append(f"S{i}")

        links = []
        for i in range(1, len(switches)+1):
            for p in range(i, len(switches)+1):
                if i != p:
                    links.append(((f"S{i}"), (f"S{p}")))

        print(switches)
        print(links)
        
        grafo = Graph(switches, links, labels=True, layout="spring", layout_scale=3)
        

        """         # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # Graph aggiusta da solo il radius dei nodi in base alla lunghezza della label associata
        grafo = Graph(nodi, archi, layout="circular", labels={ n1: "s1", n2: "s2" }, layout_scale=3,
                      vertex_config={n1: {"fill_color": RED}, n2: {"fill_color": YELLOW}}
                     ) """
        

        self.add(grafo)



class Graph3DScene(ThreeDScene):
    def construct(self):

        switches = []
        SWITCH_NUMBER = 10
        for i in range(1, SWITCH_NUMBER+1):
            switches.append(f"S{i}")

        links = []
        for i in range(1, len(switches)+1):
            for p in range(i, len(switches)+1):
                if i != p:
                    links.append(((f"S{i}"), (f"S{p}")))

        # Definizione dei vertici nel 3D (x, y, z)
        vertices_positions = {
            1: np.array([1, 1, 1]),
            2: np.array([-1, 1, -1]),
            3: np.array([-1, -1, 1]),
            4: np.array([1, -1, -1]),
        }

        # Creazione dei nodi come sfere
        vertices = {k: Sphere(radius=0.1, resolution=(8, 8)).move_to(v) for k, v in vertices_positions.items()}
        for vertex in vertices.values():
            self.add(vertex)

        # Definizione degli archi come linee
        edges = [
            (1, 2),
            (2, 3),
            (3, 1),
            (1, 4),
            (2, 4),
            (3, 4),
        ]

        # Creazione e aggiunta degli archi alla scena
        for start, end in edges:
            start_pos = vertices_positions[start]
            end_pos = vertices_positions[end]
            edge = Line(start_pos, end_pos, color=WHITE)
            self.add(edge)

        # Animazione della scena
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.2)  # Rotazione lenta della camera
        self.wait(5)


class Custom3D(ThreeDScene):
    def construct(self):
        # Definizione dei vertici nel 3D (x, y, z)
        vertices_positions = {
            1: np.array([1, 1, 1]),
            2: np.array([-1, 1, -2]),
            3: np.array([-1, -1, 2]),
            4: np.array([1, -1, -2]),
        }

        # Creazione dei nodi come sfere
        vertices = {k: Sphere(radius=0.1, resolution=(8, 8)).move_to(v) for k, v in vertices_positions.items()}
        for vertex in vertices.values():
            self.add(vertex)

        # Definizione degli archi come linee
        edges = [
            (1, 2),
            (2, 3),
            (3, 1),
            (1, 4),
            (2, 4),
            (3, 4),
        ]

        # Creazione e aggiunta degli archi alla scena
        for start, end in edges:
            start_pos = vertices_positions[start]
            end_pos = vertices_positions[end]
            edge = Line(start_pos, end_pos, color=WHITE)
            self.add(edge)

        # Animazione della scena
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.2)  # Rotazione lenta della camera
        self.wait(5)

class Dot3DExample(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75*DEGREES, theta=-45*DEGREES)

        axes = ThreeDAxes()
        dot_1 = Dot3D(point=axes.coords_to_point(0, 0, 1), color=RED)
        dot_2 = Dot3D(point=axes.coords_to_point(2, 0, 0), radius=0.1, color=BLUE)
        dot_3 = Dot3D(point=[0, 2.5, 0], radius=0.1, color=ORANGE)
        testo = Text("ciao")
        testo.move_to([0, 2.5, 0.5])
        #self.add_fixed_in_frame_mobjects(testo)
        self.add(axes, dot_1, dot_2,dot_3, testo)