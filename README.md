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

Lo script config_gen permette di creare simulazioni di traffico di rete producendo due files, network.yaml e packets.yaml,
i quali rappresentano rispettivamente i dati relativi alla rete e i pacchetti generati. Per poter operare, lo script
ha bisogno di leggere il file setup.yaml posto nella directory "./data", il quale contiene le informazioni necessarie per la configurazione.
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
- **packetSize** è la dimensione in bytes di un pacchetto
- **colorblind** è una stringa "yes" o "no" che abilita se posta su "yes" una visualizazione compatibile per persone daltoniche

Questi campi devono essere **tutti** presenti qualora si decidesse di procedere con la modalità _auto_, mentre
se si decidesse di utilizzare direttamente il **traffic_analyzer** per far analizzare propri files, allora il campo
_packetSize_ può essere omesso.

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
