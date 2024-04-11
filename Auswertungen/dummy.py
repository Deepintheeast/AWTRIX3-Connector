""" Auswertung Dummy für die Apps """

# Importieren der benötigten Funktionen aus der Funktionen-Bibliothek
from funktionen import awtrix3_send_app


def auswertung(app, data, config):
    """Dummy Auswertung"""
    data_app = {
        "text": (
            "Soweit so gut! Jetzt bitte eure 'Apps' in der 'config.ini' definieren, eine "
            "Auswertung dazu erstellen (Datei muss 'AppName.py' heißen) und im Ordner 'Auswertungen' "
            "speichern. Templates speziell zum Einsatz mit 'Solaranzeige' findet ihr im Ordner "
            "Auswertungen/Templates  ....... "
            "Have Fun! ( um dieses Dummy zu deaktivieren, einfach 'dummy.py' aus dem "
            "Ordner Auswertungen entfernen/löschen und/oder in der 'config.ini' deaktivieren! ) "
        ),
        #"icon": "HILFE",
        #"pushIcon": 2,
        "rainbow": bool(1),
    }
    awtrix3_send_app(
        config["awtrix3"]["url"],
        app,
        data_app,
        config["settings"]["app_scroll_duration"],
        config["settings"]["app_show_time"],
    )
