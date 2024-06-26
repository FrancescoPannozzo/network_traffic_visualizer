""" Manim playground: personal study script"""


import logging
from manim import *
import numpy as np


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
        dot = Dot(UP * 2 + LEFT)
        self.add(dot)
        #tex = Tex(
        #    "FadeIn with ", "shift ", " or target\_position", " and scale"
        #).scale(1)
        tex = Tex("3 seconds simulation time, ", "starting at 00:00:00").scale(1)
        tex2 = Tex("20 switches, ", "mesh graph, ", "100 Mbps").scale(1)
        tex3 = Tex("1000ms average delta, ", "100ms update delta").scale(1)
        tex2.next_to(tex, DOWN)
        tex3.next_to(tex2, DOWN)
        animations = [
            FadeIn(tex[0]),
            FadeIn(tex[1], shift=DOWN),
            FadeIn(tex2[0]),
            FadeIn(tex2[1], target_position=dot),
            FadeIn(tex2[2], shift=UP),
            FadeIn(tex3[0]),
            FadeIn(tex3[1], scale=1.5)
        ]
        
        self.play(AnimationGroup(*animations, lag_ratio=0.5))
        self.wait(3)
        animations = [
            FadeOut(tex[0]),
            FadeOut(tex[1], shift=DOWN),
            FadeOut(tex2[0]),
            FadeOut(tex2[1], target_position=dot),
            FadeOut(tex2[2], shift=UP),
            FadeOut(tex3[0]),
            FadeOut(tex3[1], scale=1.5)
        ]
        self.play(AnimationGroup(*animations, lag_ratio=0.5))

        #self.wait(2)

class Dots(MovingCameraScene):
    def construct(self):

        t1 = Tex("0", color=RED)
        linkcap = Tex("100", font_size = 20, color=BLUE, stroke_width=1, stroke_color=PINK)
        linkcap2 = Tex("1000", font_size = 20, color=BLUE, stroke_width=1, stroke_color=PINK)
        
        dot0 = LabeledDot(t1)
        
        dot1 = LabeledDot("1")
        dot1.next_to(dot0, RIGHT)

        dot2 = LabeledDot("2")
        dot2.next_to(dot0, DOWN)

        line = Line(dot0.get_center(), dot1.get_center())
        line2 = Line(dot0.get_center(), dot2.get_center())
        
        self.add(line)
        self.add(line2)
        self.add(dot0)
        self.add(dot1)
        self.add(dot2)

        self.add(linkcap)
        linkcap.next_to(line, IN)

        self.add(linkcap2)
        linkcap2.next_to(line2, IN)


        
        #curve = ArcBetweenPoints(dot0.get_center(), dot.get_center(), angle=0.5)
        #self.add(curve)
        spacing = 0.5
        dot0_coord = dot0.get_center()
        dot0_coord[0] -= 0.5
        dot0_coord[1] -= 0.2
        dot2_coord = dot2.get_center()
        dot2_coord[0] -= 0.5
        dot2_coord[1] += 0.2
        b = [2, 0, 0]
        c = [0, 2, 0]
        d = []
        #ap1 = ArcPolygon(dot0.get_center(), arr, dot1_coord, dot.get_center(), radius=2)
        #self.add(ap1)

        #punti = [LEFT, LEFT + UP, RIGHT + UP, RIGHT]

        punti = [dot0.get_center(), dot0_coord, dot2_coord, dot2.get_center()]


        dot0_coord = dot0.get_center()
        dot0_coord[0] += 0.2
        dot0_coord[1] -= 0.2
        dot1_coord = dot1.get_center()
        dot1_coord[0] -= 0.2
        dot1_coord[1] -= 0.2
        punti2 = [dot0.get_center(), dot0_coord, dot1_coord, dot1.get_center()]

        linea_angolosa = VMobject(fill_color=RED, stroke_width=2).set_points_as_corners(punti)
        linea_angolosa.set_color(YELLOW)
        self.add(linea_angolosa)

        linea_angolosa2 = VMobject(fill_color=RED, stroke_width=2).set_points_as_corners(punti2)
        linea_angolosa2.set_color(RED)
        self.add(linea_angolosa2)

        self.play(self.camera.auto_zoom([dot0, dot1, dot2, line, line2, linkcap, linkcap2, linea_angolosa, linea_angolosa2], margin=1))
        self.wait(3)

        print("dot0_coord is:", dot0_coord)
        print("First arr element:", dot0_coord[0])
        # Printing type of arr object
        print("Array is of type: ", type(dot0_coord))
        
        # Printing array dimensions (axes)
        print("No. of dimensions: ", dot0_coord.ndim)
        
        # Printing shape of array
        print("Shape of array: ", dot0_coord.shape)
        
        # Printing size (total number of elements) of array
        print("Size of array: ", dot0_coord.size)
        
        # Printing type of elements in array
        print("Array stores elements of type: ", dot0_coord.dtype)
        



        

class CustomGraph(MovingCameraScene):
    def construct(self):

        SWITCH_NUMBER = 10
        layout_scale = 3
        font_size = 30
        
        t1 = Tex("sim time 00:00:01:000", color=RED, font_size=font_size, stroke_width=1, stroke_color=YELLOW )
        #t1.shift(RIGHT * (SWITCH_NUMBER/2))
        
        

        switches = []
        
        for i in range(1, SWITCH_NUMBER+1):
            switches.append(f"s{i}")

        links = []
        for i in range(1, len(switches)+1):
            for p in range(i, len(switches)+1):
                if i != p:
                    links.append(((f"s{i}"), (f"s{p}")))
        
        grafo = Graph(switches, links, labels=True, layout="circular", layout_scale=layout_scale, vertex_config={"color":BLUE})
        
        self.add(grafo)
        t1.next_to(grafo, UP)
        self.add(t1)
        
        #self.play(self.camera.frame.animate.scale(1.2))
        
        #self.play(self.camera.auto_zoom([grafo, t1], margin=1), run_time=0.5)
       
        
        self.wait(5)


from manim import *

from manim import *

class GridOfDots(MovingCameraScene):
    def construct(self):
        # Dimensioni della griglia
        rows = 24
        cols = 42
        
        # Distanza tra i nodi
        spacing = 1
        
        switch_cont = 0
        # Creazione della griglia di nodi
        grid = VGroup()  # Gruppo per contenere tutti i nodi
        for row in range(rows):
            for col in range(cols):
                switch_cont += 1
                dot = LabeledDot(f"{switch_cont}", point=np.array([col * spacing, row * spacing, 0]), radius=0.25)
                grid.add(dot)
        
        # Centrare la griglia nella scena
        grid.move_to(ORIGIN)

        t1 = Tex("sim time 00:00:01:000", color=RED, font_size=100, stroke_width=1, stroke_color=YELLOW )
        t1.next_to(grid, UP)
        self.add(t1)
        # Visualizzazione della griglia
        self.add(grid)
        self.play(self.camera.auto_zoom([grid , t1], margin=1), run_time=0.5)
        self.wait(5)

class Blackboard(Scene):
    def construct(self):
        t1 = Tex("sim time\n00:00:01:000", color=RED, font_size=24, stroke_width=1, stroke_color=YELLOW )
        t1.to_edge(RIGHT)
        self.add(t1)
        Blackboard.test(self, "ciao")
        rad = 0.25
        spacing = 1

        index = -6.5
        dot = Dot(point=np.array([index, 3.5, 0]), radius=rad, color=ORANGE)
        self.add(dot)
        prevDot = dot
        for _ in range(0, 20):
            index += spacing
            newdot = Dot(point=np.array([index, 3.5, 0]), radius=rad)
            #newdot.next_to(prevDot)
            self.add(newdot)
            prevDot = newdot

        #lineY = Line(start=[0,-4,0], end=[0,4,0])
        #lineX = Line(start=[-8,0,0], end=[8,0,0])
        #self.add(lineX, lineY)

        number_plane = NumberPlane(
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 4,
                "stroke_opacity": 0.6
            }
        )
        self.add(number_plane)

        centerDot = Dot(point=np.array([0, 0, 0]), color=YELLOW, radius=0.5)
        self.add(centerDot)
      

    def test(self, saluto):
        t1 = Tex(f"{saluto}", color=RED, font_size=24, stroke_width=1, stroke_color=YELLOW )
        t1.to_edge(LEFT)
        self.add(t1)

class MultiPointLine(Scene):
    def construct(self):
        # Definisci i punti
        punti = [LEFT, LEFT + UP, RIGHT + UP, RIGHT]
        
        # Crea una linea con angoli definiti
        linea_angolosa = VMobject().set_points_as_corners(punti)
        linea_angolosa.set_color(RED)
        
        # Crea una linea liscia
        linea_liscia = VMobject().set_points_smoothly(punti)
        linea_liscia.set_color(BLUE).next_to(linea_angolosa, DOWN, buff=1)
        
        # Mostra le linee
        self.add(linea_angolosa)
        self.add(linea_liscia)