""" Auswertung Automation für 1 Relais 1 Kontakt mit aktuellen 
Tasmota Daten Momentanleistung und Summe Tagesverbrauch """

from funktionen import awtrix3_send_app


def auswertung(app, data, config):
    text = []
    if bool(data[f"auto1r1k_automation_Relais1aktiv"]):
        relais_name = data.get(f"auto1r1k_automation_Relais1Name", "")
        text.append({"t": f" Relais 1 {relais_name} ", "c": "#c3ff00"})
        color = "#00ff00" if int(data[f"auto1r1k_automation_Relais1Kontakt1"]) else "#ff0000"
        text.append({"t": str(int(data[f"auto1r1k_automation_Relais1Kontakt1"])), "c": color})
        tasmota_power = data.get("auto1r1k_tasmota_Power", "")
        text.append({"t": f" akt. Energie {tasmota_power} W", "c": "#002fff"})
        tasmota_tag_power = data.get("auto1r1k_tasmota_Today", "")
        text.append({"t": f" gesamt Tag {tasmota_tag_power} kWh", "c": "#9a8f16"})

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
