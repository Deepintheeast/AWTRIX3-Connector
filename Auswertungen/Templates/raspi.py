""" Anzeige Zustand (Temperatur und freier Speicher) Raspi """
# Um auf die benötigten Daten zugreifen zu können bitte
# Seite 7 von https://solaranzeige.de/phpBB3/download/EigeneErweiterungen.pdf beachten

# Importieren der benötigten Funktionen aus der Funktionen-Bibliothek
from funktionen import (
    awtrix3_send_app,
)

def auswertung(app, data, config):
    """ Auswertung Temperatur und freier Speicher des Raspi"""

# Zugriff auf den Wert und Entfernen von 'G\n'
    data['raspi_RaspiFreierSpeicher'] = data['raspi_RaspiFreierSpeicher'].replace('G\n', '')

    temp = data["raspi_RaspiTemp"]
    # Schriftfarbe für Wert in Abhängigkeit der Temperatur festlegen
    if temp <= 30:
        hex_color_temp = '#00FF00'
    elif temp <= 40:
        hex_color_temp = '#e2e21d'
    elif temp <= 50:
        hex_color_temp= '#ff0000'
    else:
        hex_color_temp = '#ff0000'

    frei = int(data["raspi_RaspiFreierSpeicher"])
    # Schriftfarbe für Wert in Abhängigkeit des freien Speichers festlegen
    if frei <= 5:
        hex_color_frei = '#ff0000'
    elif frei > 5:
        hex_color_frei = '#00ff00'

    data_app = {
        "text": [
            {"t": " Temperatur: ", "c": "#fcff33"},
            {"t": str(int(data["raspi_RaspiTemp"])) + " °C " , "c": hex_color_temp},
            {"t": "  Freier Speicher: ", "c": "#fcff33"},
            {"t": (data['raspi_RaspiFreierSpeicher'] + " GB"), "c": hex_color_frei},
        ],
        "icon": 9718,
        "pushIcon": 2,
    }
    awtrix3_send_app(
        config["awtrix3"]["url"],
        app,
        data_app,
        config["settings"]["app_scroll_duration"],
        config["settings"]["app_show_time"],
    )
