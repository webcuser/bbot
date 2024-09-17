# Sell DOGS Script

Questo progetto include uno script Python per vendere automaticamente i DOGS alla data e ora specificata. Questo README fornisce le istruzioni su come configurare e eseguire lo script su un server Linux Ubuntu.

## Configurazione

### 1. Clona il Repository
Se non hai già il codice, clona il repository con:

```sh
git clone https://github.com/tuo-utente/tuo-repo.git
cd tuo-repo
```

### 2. Installa le Dipendenze
Installa le librerie necessarie utilizzando pip. Assicurati di avere un ambiente Python configurato (potresti considerare di usare un ambiente virtuale per evitare conflitti con altre librerie):

```sh
pip install -r requirements.txt
```

### 3. Configura le Variabili
Modifica il file config.py con le tue credenziali e configurazioni. Apri config.py e aggiorna i seguenti valori:

```sh
API_KEY = 'la_tua_api_key'
API_SECRET = 'la_tua_api_secret'
ACCOUNT = 'UNIFIED'  # Tipo di account, ad esempio: UNIFIED, SPOT, CONTRACT
SYMBOL = 'DOGSUSDT'  # Simbolo da vendere
```
### 4. Pianifica l'Esecuzione dello Script
Opzione 1: Usare cron
Per eseguire lo script automaticamente il 26 settembre alle 12:00, puoi aggiungere un cron job. Esegui:

```sh
crontab -e
```
Aggiungi la seguente riga al file crontab per eseguire lo script alla data e ora specificata:

```sh
0 12 26 9 * /usr/bin/python3 /percorso/assoluto/al/sell_dogs.py
```
Sostituisci /percorso/assoluto/al/sell_dogs.py con il percorso corretto del tuo script Python.

Opzione 2: Usare systemd
Se preferisci usare systemd, segui questi passaggi:

### 1. Crea un file di servizio in /etc/systemd/system/sell_dogs.service con il seguente contenuto:
```sh
[Unit]
Description=Sell DOGS Script

[Service]
ExecStart=/usr/bin/python3 /percorso/assoluto/al/sell_dogs.py
WorkingDirectory=/percorso/assoluto/al/
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
### 2. Ricarica systemd per riconoscere il nuovo servizio:

```sh
sudo systemctl daemon-reload
```
### 3. Abilita il servizio per l'avvio automatico:
```sh
sudo systemctl enable sell_dogs.service
```
### 4. Avvia il servizio:
```sh
sudo systemctl start sell_dogs.service
```
