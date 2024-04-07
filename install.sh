#!/bin/sh
# Installationsscript für 'AWTRIX3-Connector' ab Version 0.1

# Abfrage der Debian-Version
version=$(lsb_release -rs)

sudo apt install git

if [ ! -d '/home/pi/temp_awtrix3' ]; then
  echo $1
  echo $#
  #sudo apt update
  #sudo apt dist-upgrade -y

  if [ "$version" = "11" ]; then
    echo "Debian 11 erkannt. Führe Installationen für Debian 11 aus..."
    sudo apt install pip

  elif [ "$version" = "12" ]; then
    echo "Debian 12 erkannt. Führe Installationen für Debian 12 aus..."
    sudo apt install python3-pip
    
  else
    echo "Unbekannte Debian-Version. Beende Skript."
    exit 1
  fi

# lokales Environment für User pi anlegen und aktivieren
  python -m venv ~/.env  
  source ~/.env/bin/activate
  
  pip3 install requests
  pip3 install ephem
  pip3 install schedule
  pip3 install influxdb
  #pip3 install mysql-binary
  pip3 install mysql-connector-python
  pip3 install psycopg2-binary
  

  mkdir -p /home/pi/temp_awtrix3
  mkdir -p /home/pi/scripts
  
fi

cd /home/pi/temp_awtrix3

git clone https://github.com/Deepintheeast/AWTRIX3-Connector.git

if [  $# -eq 0 ]; then
    echo 'Instanz 0 erstellen!'
    mv AWTRIX3-Connector /home/pi/scripts/AWTRIX3-Connector
    chmod 755 /home/pi/scripts/AWTRIX3-Connector/awtrix3connect.py
    sudo cp /home/pi/scripts/AWTRIX3-Connector/awtrix3-connector.service /etc/systemd/system/awtrix3-connector.service
    sudo chmod 644 /etc/systemd/system/awtrix3-connector.service
    sudo systemctl daemon-reload
    sudo systemctl enable awtrix3-connector.service
    echo 'Nach erfolgreicher Konfiguration und Test, den Dienst starten nicht vergessen!'

else
     echo 'Instanz '$1' erstellen!'
     mv AWTRIX3-Connector /home/pi/scripts/AWTRIX3-Connector-$1
     cd /home/pi/scripts/AWTRIX3-Connector-$1
     chmod 755 /home/pi/scripts/AWTRIX3-Connector-$1/awtrix3connect.py
     sed -i 's/AWTRIX3-Connector/AWTRIX3-Connector-'$1'/g' awtrix3-connector.service
     mv awtrix3-connector.service awtrix3-connector-$1.service

     sudo cp /home/pi/scripts/AWTRIX3-Connector-$1/awtrix3-connector-$1.service /etc/systemd/system/awtrix3-connector-$1.service
     sudo chmod 644 /etc/systemd/system/awtrix3-connector-$1.service
     sudo systemctl daemon-reload
     sudo systemctl enable awtrix3-connector-$1.service
     echo 'Nach erfolgreicher Konfiguration und Test, den Dienst starten nicht vergessen!'

fi

echo 'Installation beendet ! Have Fun !'
