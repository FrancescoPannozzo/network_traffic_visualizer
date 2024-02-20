# network_traffic_visualizer

#Progetto di tesi per corso di Laurea in Informatica, Università La Sapienza

Cosa si propone di fare il progetto:
Il progetto è un visualizzatore grafico interattivo di traffico di rete.
Tramite due file di input, uno con dettagli sulla configurazione di rete
e un altro con dettagli sui pacchetti che viaggiano nella medesima, si vuole mostrare
il traffico simulato nel tempo. La visualizzazione grafica è rappresentata da un grafo completo
i quali nodi sono gli switch e gli archi sono i link. Gli archi vengono colorati nel tempo a seconda
della percentuale di traffico calcolata partendo da un colore verde chiaro che rappresenta un basso traffico
fino ad arrivare a un rosso acceso che rappresenta un alto traffico.

Uso:
Creare traffico di rete: python config_gen.py switches_number link_capacity_number
Analizzare il traffico: python traffic_analyzer.py ./data/network ./data/packets
Visualizzare il traffico: manim -pql graphic_visualizer.py GraphicVisualizer
