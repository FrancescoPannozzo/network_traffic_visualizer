# network_traffic_visualizer

# Progetto di tesi per corso di Laurea in Informatica, Università La Sapienza

Cosa si propone di fare il progetto:
Il progetto è un visualizzatore e simulatore grafico di traffico di rete.
La simulazione è affidata allo script config_gen.py
. . .
Tramite due file di input, uno con dettagli sulla configurazione di rete
e un altro con dettagli sui pacchetti trasmessi, si vuole mostrare
il traffico simulato nel tempo. La visualizzazione grafica è rappresentata da un grafo completo
i quali nodi sono gli switch e gli archi sono i link. Gli archi vengono colorati nel tempo a seconda
della percentuale di traffico calcolata partendo da un colore verde chiaro che rappresenta un traffico nullo/basso
fino ad arrivare a un rosso acceso che rappresenta un alto traffico per la capacità dei link.

Uso:
Creare traffico e dati di rete: python config_gen.py

Analizzare il traffico: python traffic_analyzer.py

Visualizzare il traffico: manim -pql graphic_visualizer.py GraphicVisualizer
Visualizzare i dati d switch e links: manim -pql graphic_visualizer.py NetworkData
