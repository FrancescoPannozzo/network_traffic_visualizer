# Network traffic visualizer and simulator

## Progetto di tesi per il corso di Laurea triennale in Informatica, Università La Sapienza, anno accademico 2023/2024

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

Lo script permette di creare simulazioni di traffico di rete automatiche mettendo a disposizione due modalità **auto** e **user**.
Entrambe le modalità produrranno due files, **network.yaml** conterà le caratteristiche della rete e **packets.yaml** conterrà il traffico vero e proprio
di tutti i pacchetti generati dalla simulazione.
La modalità _auto_ chiede all'utente il numero di switch, la capacità dei link e la tipologia del grafo (completo, mesh, torus) e imposterà in modo del tutto automatico la disposizione degli switch
in base alla scelta del grafo effettuata.
Per poter operare, in entrambe le modalità, lo script ha bisogno di leggere il file setup.yaml posto nella directory "./data", il quale contiene le informazioni necessarie per la configurazione.
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

La simulazione prevede una generazione di pacchetti calcolata sulla base della capacità dei link fornita e su un valore casuale di percentuale di traffico che varia ogni secondo, per esempio avendo 6 links su 3 secondi di simulazione potremmo avere delle assegnazioni di percentuali di traffico come le seguenti:

```
Link: 1, endpoints: [1, 2], sim second: 0, trafficPerc: 65
Link: 2, endpoints: [1, 3], sim second: 0, trafficPerc: 9
Link: 3, endpoints: [2, 4], sim second: 0, trafficPerc: 23
Link: 4, endpoints: [2, 5], sim second: 0, trafficPerc: 67
Link: 5, endpoints: [3, 6], sim second: 0, trafficPerc: 7
Link: 6, endpoints: [3, 7], sim second: 0, trafficPerc: 87
Link: 1, endpoints: [1, 2], sim second: 1, trafficPerc: 86
Link: 2, endpoints: [1, 3], sim second: 1, trafficPerc: 26
Link: 3, endpoints: [2, 4], sim second: 1, trafficPerc: 13
Link: 4, endpoints: [2, 5], sim second: 1, trafficPerc: 13
Link: 5, endpoints: [3, 6], sim second: 1, trafficPerc: 39
Link: 6, endpoints: [3, 7], sim second: 1, trafficPerc: 65
Link: 1, endpoints: [1, 2], sim second: 2, trafficPerc: 31
Link: 2, endpoints: [1, 3], sim second: 2, trafficPerc: 54
Link: 3, endpoints: [2, 4], sim second: 2, trafficPerc: 11
Link: 4, endpoints: [2, 5], sim second: 2, trafficPerc: 20
Link: 5, endpoints: [3, 6], sim second: 2, trafficPerc: 17
Link: 6, endpoints: [3, 7], sim second: 2, trafficPerc: 46
```

Una volta lanciato config_gen avremo le seguenti possibilità di scelte:

- **auto**
  - scelta del numero di switch
  - scelta della capacità dei link
  - scelta della tipologia della rete (grafo completo, mesh, torus)
- **user**

La modalità user necessita di un file **custom_graph.yaml** con i parametri necessari a descrivere
la rete del quale si vuole analizzare il traffico. Con questa modalità l'utente ha completa libertà nel personalizzare la rete
ed è tenuto quindi a descriverne ogni suo aspetto.
Il custom_graph.yaml prevede la struttura seguente, con possibili varianti:

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

La cui rappresentazione grafica ottenuta dal graphic visualizer è la seguente:

![only_links](./media/images/readme_pics/only_links.JPG)

- **graphType** identifica la tipologia del grafo da rappresentare, sono disponibili tre opzioni:
  - **mesh**: l'algoritmo individua in modo automatico gli archi (i link) che collegano i nodi (gli switch) adiacenti tra loro presenti nella matrice **coordinates**
  - **torus**: esegue lo stessa procedura usate per mesh e in addizione collega tra loro i nodi che si trovano alle estremità della matrice
  - **graph**: è la modalità più libera, collega gli switch tramite
    i link forniti dall'utente, indipendentemente da dove vengono collocati
- **coordinates** rappresenta le coordinate dei vari switch, i quali vanno rappresentati con un id numerico che va da 1 a 1000. C'è una precisa motivazione di design per questa scelta ed è legata a una rappresentazione grafica ottimale del visualizzatore grafico. Gli zeri invece rappresentano uno spazio vuoto in cui non è presente uno switch.
- **links** rappresenta i link della rete i quali possono essere specificati con i campi
  - **linkCap** esprime la capacità del link in Mbps
  - **endpoints** esprime gli endpoints collegati al link
- **phases** rappresenta le fasi temporali che accompagnano la durata dell'attività di rete, sono identificate tramite timestamp che ha come valore la descrizione della fase che parte dal timestamp stesso

Qualora la capacità dei link sia uguale per tutti è possibile insererire il campo **linkCap** e usare la seguente struttura:

```yaml
---
# linkCap, links
data:
  graphType: torus
  coordinates:
    - [1, 0, 2, 0]
    - [3, 0, 4, 5]
    - [6, 7, 8, 9]
  linkCap: 10
  switches:
    1:
      ip: "123.123.123.0"
      switchName: A
    2:
      ip: "123.123.123.1"
      switchName: B
    3:
      ip: "123.123.123.2"
      switchName: C
    4:
      ip: "123.123.123.3"
      switchName: D
    5:
      ip: "123.123.123.4"
      switchName: E
    6:
      ip: "123.123.123.5"
      switchName: F
    7:
      ip: "123.123.123.6"
      switchName: G
    8:
      ip: "123.123.123.7"
      switchName: H
    9:
      ip: "123.123.123.8"
      switchName: I
  links:
    - [1, 3]
    - [1, 6]
    - [3, 6]
    - [4, 8]
    - [5, 9]
    - [3, 5]
    - [6, 9]
    - [4, 5]
    - [6, 7]
    - [7, 8]
    - [8, 9]
    - [2, 4]
    - [2, 8]
  phases:
    2024-01-01 00:00:01: "phase1"
    2024-01-01 00:00:02: "phase2"
```

Un'altra possibilità è quella di lasciare che il programma ricavi in automatico i link, in questo caso basterà specificare solo **linkCap** che sarà uguale per tutti i link:

```yaml
---
data:
  graphType: mesh
  coordinates:
    - [1, 2, 3]
    - [4, 5, 6]
    - [7, 8, 9]
  linkCap: 10
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
  phases:
    2024-01-01 00:00:01: "phase1"
    2024-01-01 00:00:02: "phase2"
```

![auto_link](./media/images/readme_pics/auto.JPG)

Infine mostriamo un esempio di **graphType** posto con valore **graph**:

```yaml
---
data:
  graphType: graph
  coordinates:
    - [0, 0, 0, 0, 1, 0, 0, 0, 0]
    - [0, 0, 2, 0, 0, 0, 3, 0, 0]
    - [0, 4, 0, 5, 0, 6, 0, 7, 0]
  linkCap: 10
  switches:
    1:
      ip: "123.123.123.0"
      switchName: A
    2:
      ip: "123.123.123.1"
      switchName: B
    3:
      ip: "123.123.123.2"
      switchName: C
    4:
      ip: "123.123.123.3"
      switchName: D
    5:
      ip: "123.123.123.4"
      switchName: E
    6:
      ip: "123.123.123.5"
      switchName: F
    7:
      ip: "123.123.123.6"
      switchName: G
  links:
    - [1, 2]
    - [1, 3]
    - [2, 4]
    - [2, 5]
    - [3, 6]
    - [3, 7]
  phases:
    2024-01-01 00:00:01: "phase1"
    2024-01-01 00:00:02: "phase2"
```

![free_graph](./media/images/readme_pics/free_graph.JPG)

## Analisi dati di rete: traffic_analyzer

Lo script traffic_analyzer carica i due files prodotti da config_gen e analizza il traffico producendo un file, analyzed_data.yaml nella seguente forma:

```yaml
- averageDelta: 1000
  simStartTime: 2024-03-22 12:30:00
  simTime: 3
  updateDelta: 100
- - endpoints:
      - 1
      - 2
    traffic:
      - 35.0
      - 39.0
      - 43.0
      - 47.0
      - 51.0
      - 55.0
      - 59.0
      - 63.0
      - 67.0
      - 71.0
      - 75.0
      - 74.7
      - 74.4
      - 74.1
      - 73.8
      - 73.5
      - 73.2
      - 72.9
      - 72.6
      - 72.3
      - 72.0
  - endpoints:
      - 1
      - 3
    traffic:
      - 72.0
      - 70.0
      - 68.0
      - 66.0
      - 64.0
      - 62.0
      - 60.0
      - 58.0
      - 56.0
      - 54.0
      - 52.0
      - 50.2
      - 48.4
      - 46.6
      - 44.8
      - 43.0
      - 41.2
      - 39.4
      - 37.6
      - 35.8
      - 34.0
```

Il campo **traffic** rappresenta le percentuali di traffico registrate delle medie del peso dei pacchetti per un dato intervallo di tempo **averageDelta** (espresso in millisecondi), aggiornato ogni **updateDelta** millisecondi. Quindi, in questo specifico esempio in cui si descrive una rete di 3 switch, avremo la prima media percentuale di ciascun link esattamente a un secondo dall'inizio della trasmissione dei pacchetti e avremo valori aggiornati ogni 100 ms.
Una qualsiasi rete può essere analizzata se si forniscono i files network.yaml e packets.yaml, i quali devono essere correttamente formattati. Traffic analyzer funziona avendo l'assunzione che il file packets.yaml contenga i pacchetti in ordine temporale di invio, il file presenta la seguente struttura:

```yaml
- A: 2
  B: 1
  d: 4000
  t: &id001 2024-03-22 12:30:00
- A: 1
  B: 2
  d: 4000
  t: *id001
- A: 1
  B: 2
  d: 4000
  t: *id001
- A: 1
  B: 2
  d: 4000
  t: *id001
# and so on
```

La struttura prevede una lista di dizionari le quali chiavi sono:

- **A** - un endpoint del link sul quale il pacchetto ha viaggiato
- **B** - l'altro endpoint
- **d** - la dimensione del pacchetto in bytes
- **t** - il timestamp di quando il pacchetto è stato trasmesso

**NOTA:** la scelta di avere singoli caratteri come chiavi è dettata da esigenze di risparmio di data storage

Per quanto riguarda invece il file network.yaml si presenta con la seguente struttura:

```yaml
- - capacity: 10
    endpoints:
      - 1
      - 2
  - capacity: 10
    endpoints:
      - 1
      - 3
- - address: 10.0.0.1
    switchID: 1
    switchName: switch1
  - address: 10.0.0.2
    switchID: 2
    switchName: switch2
  - address: 10.0.0.3
    switchID: 3
    switchName: switch3
- averageDelta: 1000
  colorblind: "no"
  graphType: mesh
  linkCap: 10
  simTime: 3
  startSimTime: 2024-03-22 12:30:00
  updateDelta: 100
- coordinates:
    - - 1
      - 2
    - - 3
      - 0
- 2024-03-22 12:30:01: phase1
  2024-03-22 12:30:02: phase2
```

**NOTA:** Per una rappresentazione più leggibile delle coordinate è possibile usare anche la seguente forma:

```yaml
- coordinates:
    - [1, 2]
    - [3, 0]
```

Il file rappresenta una lista in cui ogni elemento rappresenta, in ordine, dal primo i seguenti valori:

- La lista dei links
- La lista di switches
- Una lista dei parametri necessari
- Le coordinate (una lista di liste) del posizionamento degli switch da rappresentare
- Le fasi che interessano l'andamento del traffico di rete

## Visualizzazione grafica: graphic_visualizer.py

Una volta ottenuto il file analyzed_data.yaml, esso verrà caricato dal graphic_visualizer al momento del lancio oltre che al file network.yaml, così da poter posizionare gli switch come indicato dalle coordinate, collegarli tra loro tramite la descrizione dei link per poi creare l'ambiente grafico che animerà nel tempo per mostrare la variazione del traffico. Il tutto viene eseguito tramite libreria Manim che provvede e fornire il risultato sottoforma di video

![graphic_visualizer_example](./media/images/readme_pics/GraphicVisualizer_example.gif)

È possibile visualizzare separatamente informazioni relatvie agli switch e ai link. Relativamente all'esempio precedente avremmo:

![network_data_example](./media/images/readme_pics/NetworkData_example.gif)

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
