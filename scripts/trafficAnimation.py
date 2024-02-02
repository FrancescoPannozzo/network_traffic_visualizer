from manim import *

class NodoArcoAnimazione(Scene):
    def construct(self):
        # Creare i nodi
        nodo1 = Dot(point=LEFT, color=BLUE)
        nodo2 = Dot(point=RIGHT, color=BLUE)

        # Creare l'arco che collega i nodi
        arco = Line(nodo1.get_center(), nodo2.get_center(), buff=0).set_color(WHITE)

        # Aggiungere i nodi e l'arco alla scena
        self.play(FadeIn(nodo1), FadeIn(nodo2), Create(arco))

        # Cambiare il colore dell'arco nel tempo
        self.play(arco.animate.set_color(RED), run_time=2)
        self.play(arco.animate.set_color(GREEN), run_time=2)
        self.play(arco.animate.set_color(BLUE), run_time=2)

        # Mantenere l'ultima immagine per alcuni secondi prima di concludere
        self.wait(2)
