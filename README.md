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
I componenti principali del progetto sono gli scripts:

- config_gen: crea il traffico simulato
- traffic_analyzer: analizza i files del traffico di rete per estrarne le percentuali di traffico
- graphic_visualizer: legge i dati prodotti da traffic_analyzer e li mostra graficamente con un video

## Simulazione: config_gen.py

Lo script _config_gen_ permette di creare simulazioni di traffico di rete automatiche mettendo a disposizione due modalità **auto** e **user**.
Entrambe le modalità produrranno due files, **network.yaml** conterà le caratteristiche della rete e **packets.yaml** conterrà il traffico vero e proprio
di tutti i pacchetti generati dalla simulazione.
La modalità _auto_ chiede all'utente il numero di switch, la capacità dei link e la tipologia del grafo (completo, mesh, torus) e imposterà in modo del tutto automatico la disposizione degli switch
in base alla scelta del grafo effettuata.
Per poter operare, in entrambe le modalità, lo script ha bisogno di leggere il file setup.yaml posto nella directory _"./data"_, il quale contiene le informazioni necessarie per la configurazione.
Il file setup.yaml è impostato come segue:

```yaml
averageDelta: 1000
updateDelta: 100
startSimTime: 2024-03-22 12:30:00
simTime: 3
packetSize: 4000
colorblind: "no"
```

- **averageDelta** rappresenta l'intervallo temporale in millisecondi delle medie di traffico da calcolare
- **updateDelta** rappresenta ogni quanti millisecondi si deve aggiornare la media averageDelta
- **startSimTime** è il datetime dell'inizio della simulazione nel formato YY:MM:DD HH:MM:SS
- **simTime** è la durata della simulazione in secondi
- **packetSize** è la dimensione in bytes di un pacchetto, i pacchetti nella simulazione avranno questa dimensione
- **colorblind** è una stringa "yes" o "no" che abilita se posta su "yes" una visualizazione compatibile per persone daltoniche

Una volta lanciato _config_gen_ avremo le seguenti possibilità di scelte:

- **auto**
  - scelta del numero di switch
  - scelta della capacità dei link
  - scelta della tipologia della rete (grafo completo, mesh, torus)
- **user**

La modalità _user_ necessita di un file **custom_graph.yaml** con i parametri necessari a descrivere
la rete del quale si vuole analizzare il traffico. Con questa modalità l'utente ha completa libertà nel personalizzare la rete
ed è tenuto quindi a descriverne ogni suo aspetto.
Il _custom_graph.yaml_ prevede la struttura seguente:

```yaml
---
data:
  graphType: mesh
  coordinates:
    - [1, 0, 2, 0]
    - [3, 0, 4, 5]
    - [6, 7, 8, 9]
  switches:
    1:
      ip: "123.123.123.0"
      switchName: Anthem
    2:
      ip: "123.123.123.1"
      switchName: Beta
    3:
      ip: "123.123.123.2"
      switchName: Cyber
    4:
      ip: "123.123.123.3"
      switchName: Dafne
    5:
      ip: "123.123.123.4"
      switchName: Eclipse
    6:
      ip: "123.123.123.5"
      switchName: Fox
    7:
      ip: "123.123.123.6"
      switchName: Gea
    8:
      ip: "123.123.123.7"
      switchName: H20
    9:
      ip: "123.123.123.8"
      switchName: Italy
  links:
    - { linkCap: 10, endpoints: [1, 3] }
    - { linkCap: 100, endpoints: [1, 6] }
    - { linkCap: 10, endpoints: [3, 6] }
    - { linkCap: 10, endpoints: [4, 8] }
    - { linkCap: 10, endpoints: [5, 9] }
    - { linkCap: 100, endpoints: [3, 5] }
    - { linkCap: 10, endpoints: [6, 9] }
    - { linkCap: 100, endpoints: [4, 5] }
    - { linkCap: 10, endpoints: [6, 7] }
    - { linkCap: 10, endpoints: [7, 8] }
    - { linkCap: 100, endpoints: [8, 9] }
    - { linkCap: 10, endpoints: [2, 4] }
    - { linkCap: 10, endpoints: [2, 8] }
  phases:
    2024-01-01 00:00:01: "phase1"
    2024-01-01 00:00:02: "phase2"
```

- **graphType** identifica la tipologia del grafo da rappresentare

## Analisi dati di rete: traffic_analyzer

...

## Visualizzazione grafica: graphic_visualizer.py

...

### Prerequisiti

- Python 3.6 o superiore
- PyYAML 5.3 o superiore
- Manim Community v0.18.0 o superiore

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
