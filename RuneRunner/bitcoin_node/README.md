# Bitcoin Node Configuration

## Setup

1. Installiere Bitcoin Core und kopiere die `bitcoind.exe` Datei in `C:\Program Files\Bitcoin\daemon`.
2. Stelle sicher, dass die Blockchain-Daten im Verzeichnis `E:\Bitcoin` liegen.

## Konfiguration

Die Konfigurationsdatei `bitcoind.conf` enthält die notwendigen Einstellungen:
```ini
server=1
rpcuser=yourrpcuser
rpcpassword=yourrpcpassword
datadir=E:\Bitcoin
