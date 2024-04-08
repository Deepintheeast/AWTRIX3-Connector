""" Auswertung der Indikatoren und Ansteuerung der Anzeige"""

# Importieren der benötigten Funktionen aus der Funktionen-Bibliothek
from funktionen import (
    awtrix3_send_indikator,
    awtrix3_send_notifikation
)

fehler_aufgetreten = False

def auswertung(app, data, config):
    global fehler_aufgetreten

    # Indikator 1: Lade(strom) (grün) oder Entlade(strom) (rot)
    if data["indikator_Strom"] > 0:
        indi1_data = {"color": "#00ff00"}
    elif data["indikator_Entladestrom"] > 0:
        indi1_data = {"color": "#ff0000"}
    else:
        indi1_data = {"color": "#000000"}
    awtrix3_send_indikator(config["awtrix3"]["url"], 1, indi1_data)

    # Indikator 2: Temperatur Raspi (grün < 35°C, orange 36°C-50°C, rot >= 50°C)
    raspi_temp = int(data["indikator_RaspiTemp"])
    if raspi_temp <= 35:
        indi2_data = {"color": "#00ff00", "fade": 5000}
    elif 36 <= raspi_temp <= 50:
        indi2_data = {"color": "#f1b953", "fade": 3000}
    else:
        indi2_data = {"color": "#ff0000", "blink": 200}
    awtrix3_send_indikator(config["awtrix3"]["url"], 2, indi2_data)

    # Indikator 3: Betriebsmodus (Batterie (grün), Netz (blau), Fehler(rot))
    # und Notifikation bei Fehler
    int_modus = int(data["indikator_IntModus"])
    if int_modus == 3:  # Batteriemodus
        indi3_data = {"color": "#00ff00"}
    elif int_modus == 4:  # Line(Netz)modus
        indi3_data = {"color": "#0000ff"}
    else:  # Error(Fehler)modus
        indi3_data = {"color": "#ff0000", "blink": 100}
        if not fehler_aufgetreten:
            notifi_data = {
                "text": "Achtung! Wechselrichter befindet sich im Fehlermodus! Bitte überprüfen! ",
                "color": "#ff0000",
                "hold": True,
            }
            awtrix3_send_notifikation(config["awtrix3"]["url"], notifi_data)
            fehler_aufgetreten = True
    awtrix3_send_indikator(config["awtrix3"]["url"], 3, indi3_data)
