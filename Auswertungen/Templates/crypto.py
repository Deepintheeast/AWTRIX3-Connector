""" Auswertung für Kryptowährungen Anzeige des aktuellen Preises und der prozentualen 
    Änderungen in den letzten 24 Stunden und der letzten Stunde"""

# Importieren der benötigten Funktionen aus der Funktionen-Bibliothek
from funktionen import awtrix3_send_app

def auswertung(app, data, config):
    """
    Auswertung Anzeige Kryptowährungen
     1. Wert: aktueller Preis in Euro,
     2. Wert: 24h-Änderung in %,
     3. Wert: letzte Stunde-Änderung in %
    """
    data_app = {
        "icon": 48432,
        "pushIcon": 1,
        "text": [],  # Initialisieren "text" als leere Liste
    }

    # Crypto-Daten hinzufügen
    for key, value in data.items():
        if key.endswith('_0'):
            color = "#00ff00" if data[key[:-1] + '1'] >= 0 else "#ff0000"
            data_app["text"].extend([
                {"t": f" {key.split('_')[1]}: ", "c": "#ddff33"},
                {"t": f"{str(value)} € ", "c": color},
                {"t": " + ", "c": "#ed7d3b"},
                {"t": f" {str(data[key[:-1] + '1'])} % ", "c": color},
                {"t": " + ", "c": "#ed7d3b"},
                {"t": f" {str(data[key[:-1] + '2'])} % ", "c": color}
            ])
    awtrix3_send_app(
        config["awtrix3"]["url"],
        app,
        data_app,
        config["settings"]["app_scroll_duration"],
        config["settings"]["app_show_time"],
    )
