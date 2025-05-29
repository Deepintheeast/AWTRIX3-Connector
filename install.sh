#!/bin/bash
# Installationsscript für 'AWTRIX3-Connector' ab Version 0.1.2

timestamp=$(date +"%Y-%m-%d_%H-%M-%S")

# Username des Benutzers
username=$(whoami)
# Abfrage der Debian-Version
version=$(lsb_release -rs)

cd /home/$username

sudo apt install git

if [ ! -d '/home/$username/temp_awtrix3' ]; then
  echo $1
  echo $#
  #sudo apt update
  #sudo apt dist-upgrade -y

  if [ "$version" = "11" ]; then
    echo "Debian 11 erkannt. Führe Installationen für Debian 11 aus..."
    sudo apt install pip
    sudo apt-get install python3-venv

  elif [ "$version" = "12" ]; then
    echo "Debian 12 erkannt. Führe Installationen für Debian 12 aus..."
    sudo apt install python3-pip
    
  else
    echo "Unbekannte Debian-Version. Beende Skript."
    exit 1
  fi

# lokales Environment für User anlegen und aktivieren
  python3 -m venv ~/.env  
  source ~/.env/bin/activate

  pip3 install requests
  pip3 install ephem
  pip3 install schedule
  pip3 install influxdb
  pip3 install influxdb-client
  pip3 install mysql-connector-python
  pip3 install psycopg2-binary
  
  mkdir -p /home/$username/temp_awtrix3
  mkdir -p /home/$username/scripts
  
fi

cd /home/$username/temp_awtrix3

git clone https://github.com/Deepintheeast/AWTRIX3-Connector.git

if [  $# -eq 0 ]; then
    echo 'Instanz 0 erstellen!'

    if [ -d "/home/$username/scripts/AWTRIX3-Connector" ]; then
     mv -f /home/$username/scripts/AWTRIX3-Connector /home/$username/scripts/AWTRIX3-Connector-$timestamp.old
    fi

    mv AWTRIX3-Connector /home/$username/scripts/AWTRIX3-Connector
    chmod 755 /home/$username/scripts/AWTRIX3-Connector/awtrix3connect.py
    sudo cp /home/$username/scripts/AWTRIX3-Connector/awtrix3-connector.service /etc/systemd/system/awtrix3-connector.service
    sudo chmod 644 /etc/systemd/system/awtrix3-connector.service
    sudo sed -i "s|USERNAME|$username|g" /etc/systemd/system/awtrix3-connector.service
    sudo systemctl daemon-reload
    sudo systemctl enable awtrix3-connector.service

    if ! grep -q "alias showdb=" /home/$username/.bashrc; then
      echo "alias showdb='cd /home/$username/scripts/AWTRIX3-Connector/Tools && /home/$username/.env/bin/python3 ./showdb.py'" >> /home/$username/.bashrc
    fi

    if ! grep -q "alias awtrixconnect3=" /home/$username/.bashrc; then
      echo "alias awtrixconnect3='cd /home/$username/scripts/AWTRIX3-Connector && /home/$username/.env/bin/python3 ./awtrix3connect.py'" >> /home/$username/.bashrc
    fi

else
     echo 'Instanz '$1' erstellen!'

      if [ -d "/home/$username/scripts/AWTRIX3-Connector-$1" ]; then
       mv -f /home/$username/scripts/AWTRIX3-Connector-$1 /home/$username/scripts/AWTRIX3-Connector-$1-$timestamp.old
      fi

     mv AWTRIX3-Connector /home/$username/scripts/AWTRIX3-Connector-$1
     cd /home/$username/scripts/AWTRIX3-Connector-$1
     chmod 755 /home/$username/scripts/AWTRIX3-Connector-$1/awtrix3connect.py
     sed -i 's/AWTRIX3-Connector/AWTRIX3-Connector-'$1'/g' awtrix3-connector.service
     mv awtrix3-connector.service awtrix3-connector-$1.service

     sudo cp /home/$username/scripts/AWTRIX3-Connector-$1/awtrix3-connector-$1.service /etc/systemd/system/awtrix3-connector-$1.service
     sudo chmod 644 /etc/systemd/system/awtrix3-connector-$1.service
     sudo sed -i "s|USERNAME|$username|g" /etc/systemd/system/awtrix3-connector-$1.service
     sudo systemctl daemon-reload
     sudo systemctl enable awtrix3-connector-$1.service

     if ! grep -q "alias awtrixconnect3-$1=" /home/$username/.bashrc; then
      echo "alias awtrixconnect3-$1='cd /home/$username/scripts/AWTRIX3-Connector-$1 && /home/$username/.env/bin/python3 ./awtrix3connect.py'" >> /home/$username/.bashrc
     fi

fi

echo ''
echo 'Nach erfolgreicher Konfiguration und Test, den Dienst starten nicht vergessen!'
echo ''
echo 'Durch den angelegten alias genügt zum starten des Scriptes ein awtrixconnect3 auf der Konsole!'
echo 'Installation beendet! Viel Spaß!'
echo ''

source ~/.bashrc
rm -rf /home/$username/temp_awtrix3/
rm -f /home/$username/install.sh
