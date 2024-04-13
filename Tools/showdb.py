
#!/usr/bin/env python3

"""
Dieses Skript stellt eine Verbindung zu einer InfluxDB-Datenbank her, 
ruft alle Measurements ab und gibt jeden letzten Wert für jedes Measurement aus.
Benötigt "InfluxDBClient" aus dem Paket "influxdb".
Installation mit "pip3 install influxdb"

Aufruf: python3 showdb.py <database_name>
"""
from influxdb import InfluxDBClient

def show_measurements_and_last_values(database_name):
    """
    Stellt eine Verbindung zu einer InfluxDB-Datenbank her, 
    ruft alle Measurements ab und gibt jeden letzten Wert für jedes Measurement aus.
    """
    # Verbindung zum InfluxDB-Server herstellen
    client = InfluxDBClient(host='127.0.0.1', port=8086)

    # Datenbank auswählen
    client.switch_database(database_name)

    # Alle Measurements abrufen
    measurements = client.query('SHOW MEASUREMENTS')

    for measurement in measurements.get_points():
        measurement_name = measurement['name']
        print(f"\nMeasurement: {measurement_name}")

        # Letzten Wert und Zeitstempel für dieses Measurement abrufen
        last_value = client.query(f'SELECT * FROM "{measurement_name}"  ORDER BY time DESC LIMIT 1')
        for point in last_value.get_points():
            # 'last_' aus den Spaltennamen entfernen
            point = {k.replace('last_', ''): v for k, v in point.items()}
            print(f"Letzter Wert: {point}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <database_name>")
        sys.exit(1)

    database_name = sys.argv[1]
    show_measurements_and_last_values(database_name)
