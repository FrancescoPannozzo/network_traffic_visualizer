# network_traffic_visualizer

#Progetto di tesi per corso di Laurea in Informatica, Università La Sapienza

Cosa si propone di fare il progetto:
Il progetto è un visualizzatore grafico interattivo di traffico di rete.
Tramite due file di input, uno con dettagli sulla configurazione di rete
e un altro con dettagli sui pacchetti che viaggiano nella medesima, si vuole mostrare
il traffico simulato nel tempo. L'interattività viene dalla possibilità di interagire
nell'interfaccia grafica, rappresentate la rete, nello specifico sui nodi che rappresentano
i vari switch, così da poter ottenere informazioni relative agli stessi come ad esempio
a quali altri switch sono connessi, indirizzo ip e così via, inoltre la capacirà dei link è regolabile
tramite personalizzazione, quindi ogni link è configurarbile
La simulazione viene calcolata con una proporione temporale, ad esempio una trasmissione di
pacchetti di un'ora viene mostrata in una simulazione della durata di un minuto in cui viene mostrata
la media calcolata del traffico. La media nel tempo è calcolata tramite un intervallo x di tempo considerato che viene ricalcolato
ogni intervallo di y tempo più piccolo di x.

Uso:
Creare traffico di rete con config_gen.py presente nella directory "scripts"
Caricare i file prodotti da config_gen tramite main.py per analizzare il traffico
