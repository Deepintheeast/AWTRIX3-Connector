""" Auswertung Automation universal für x Relais und x Kontakte,
    Anzeige der aktiven Relais und deren Kontakte 0 = aus, 1 = ein"""

# Importieren der benötigten Funktionen aus der Funktionen-Bibliothek
from funktionen import awtrix3_send_app

def auswertung(app, data, config):
    # Auswertung Automation universal für x Relais und x Kontakte
    # Es werden die aktiven Relais und deren Kontakte angezeigt
    # 0 = aus, 1 = ein
    text = []
    for j in range(1, 3):  # 3 = Anzahl der Relais + 1
        if bool(data[f"auto_automation_Relais{j}aktiv"]):
            # Fügen Sie den Text für das Relais und seinen Namen hinzu
            relais_name = data.get(f"auto_automation_Relais{j}Name", "")
            text.append({"t": f" Relais {j} {relais_name} ", "c": "#c3ff00"})
            # Fügen Sie die Werte der aktiven Kontakte hinzu
            num_contacts = int(data[f"auto_automation_Relais{j}AnzKontakte"])
            for i in range(1, num_contacts + 1):
                color = "#00ff00" if int(data[f"auto_automation_Relais{j}Kontakt{i}"]) else "#ff0000"
                text.append({"t": str(int(data[f"auto_automation_Relais{j}Kontakt{i}"])), "c": color})        
    # Erstellen Sie das Dictionary nur, wenn Text vorhanden ist
    if text:
        for item in text:
            item["t"] = " " + item["t"]

        data_app = {
            "text": text,
            "icon": "automation",
            "pushIcon": 2,
        }
    else:
        data_app = {}

    awtrix3_send_app(
        config["awtrix3"]["url"],
        app,
        data_app,
        config["settings"]["app_scroll_duration"],
        config["settings"]["app_show_time"],
    )
