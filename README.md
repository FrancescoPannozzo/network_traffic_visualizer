# Network traffic visualizer and simulator

## Progetto di tesi per corso di Laurea in Informatica, Università La Sapienza

Cosa si propone di fare il progetto:
Il progetto è un visualizzatore grafico e simulatore di traffico di rete.
Tramite due file di input, uno con dettagli sulla configurazione di rete
e un altro con dettagli sui pacchetti trasmessi, si vuole mostrare
il traffico nel tempo. La visualizzazione grafica è rappresentata da un grafo
i quali nodi sono gli switch e gli archi sono i link. Gli archi vengono colorati nel tempo a seconda
della percentuale di traffico calcolata partendo da un colore verde chiaro che rappresenta un traffico nullo/basso
fino ad arrivare a un rosso acceso che rappresenta un alto traffico per la capacità dei link.
I componenti principali del progetto sono

- Lo script config_gen che si occupa della creazione di traffico simulato
- Lo script traffic_analyzer che si occupa di analizzare i files del traffico di rete per estrarne le percentuali di traffico
- Lo script graphic_visualizer che legge i dati prodotti da traffic_analyzer e li mostra graficamente con un video

config_gen:
Questo script permette di creare simulazioni di traffico di rete producendo due files, network.yaml e packets.yaml,
i quali rappresentano rispettivamente i dati relativi alla rete e i pacchetti generati. Per poter operare, lo script
ha bisogno di leggere il file setup.yaml, il quale contiene le informazioni necessarie per la configurazione.

## Uso:

Creare traffico e dati di rete:

```python
python config_gen.py
```

Analizzare il traffico:

```python
python traffic_analyzer.py
```

Visualizzare il traffico:

```python
 manim -pql graphic_visualizer.py GraphicVisualizer
```

Visualizzare i dati di switch e links:

```python
 manim -pql graphic_visualizer.py NetworkData
```
