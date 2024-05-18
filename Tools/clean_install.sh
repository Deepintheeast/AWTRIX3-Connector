#!/bin/bash
# Script zum entfernen der angelegten Daten und Dienste
# Achtung "Alles Daten der Installation des AWTRIX3 Connectors werden unwiederbringlich gelöscht!"
# 

# Benutzername des Benutzers
username=$(whoami)

# Entfernen der erstellten Verzeichnisse und Dateien
rm -rf /home/$username/scripts/AWTRIX3-*
rm -rf /home/$username/.env

# Entfernen der systemd-Dienste
sudo rm /etc/systemd/system/awtrix3-connector.service
sudo rm /etc/systemd/system/awtrix3-connector-*.service

# Entfernen der Aliase aus der .bashrc-Datei
sed -i '/alias showdb=/d' /home/$username/.bashrc
sed -i '/alias awtrixconnect3=/d' /home/$username/.bashrc
sed -i '/alias awtrixconnect3-/d' /home/$username/.bashrc

# Neuladen der systemd-Daemon-Konfiguration
sudo systemctl daemon-reload

echo 'Deinstallation abgeschlossen!'
