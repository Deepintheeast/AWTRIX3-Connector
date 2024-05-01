""" Auswertung Template für einen einzelnen Wert
WERT und ICON müssen an die verwendeten, gewünschten Werte angepasst werden"""

# Importieren der benötigten Funktionen aus der Funktionen-Bibliothek
from funktionen import awtrix3_send_app

def auswertung(app, data, config):
    # Auswertung Template für einen einzelnen Wert
    data_app = {
        "text": str(int(data["WERT"])) + " Irgendwas oder löschen! ", # oder
        #"text": " Irgendwas oder löschen! " + str(int(data["WERT"])),
        "icon": ICON, # Hier verwendetes Icon festlegen
        "color": "#00ff00", # Hier Textfarbe festlegen
    }
    awtrix3_send_app(
        config["awtrix3"]["url"],
        app,
        data_app,
        config["settings"]["app_scroll_duration"],
        config["settings"]["app_show_time"],
    )