""" Auswertungen für die Apps """
import os
import importlib.util

def auswertung(app, data, config):
    """ Definiert die Auswertung für die angegebene App """
    # Pfad zum Ordner mit den Auswertungsmodulen
    module_dir = 'Auswertungen'

    # Liste aller Python-Dateien im Ordner
    module_files = [f for f in os.listdir(module_dir) if f.endswith('.py')]

    for module_file in module_files:
        # Modulnamen sind Dateinamen ohne die .py Endung
        module_name = module_file[:-3]

        # Wenn der Modulname mit der App übereinstimmt, importiere das Modul
        if module_name == app:
            module_path = os.path.join(module_dir, module_file)

            # Modul importieren
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Wenn das Modul eine Funktion namens 'auswertung' hat, rufe sie auf
            if hasattr(module, 'auswertung'):
                module.auswertung(app, data, config)

            # Nachdem das Modul gefunden und ausgeführt wurde, breche die Schleife ab
            break
    else:
        print(f"Nope: Keine Auswertung für App \"{app}\" gefunden!")
