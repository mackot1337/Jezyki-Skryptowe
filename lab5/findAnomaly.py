def findAnomaly(measurements, alarmLimit=500.0, jumpLimit=100.0):

    anomalies = []
    errorsCounter = 0
    previousValue = None

    for measurement in measurements:
        time = measurement.get('Czas', measurement.get('Data', 'Nieznany czas'))
        value = measurement.get('Wartość', '').strip()

        if not value or value.lower() in ('none', 'null', 'brak'):
            errorsCounter += 1
            continue

        try:
            value = float(value.replace(',', '.'))
        except ValueError:
            errorsCounter += 1
            continue

        if value < 0:
            anomalies.append(f"[{time}] BŁĄD: Wartość ujemna ({value}). Awaria czujnika?")
            continue

        if value > alarmLimit:
            anomalies.append(f"[{time}] ALARM: Ekstremalnie wysoka wartość: {value}!")

        if previousValue is not None:
            jump = abs(value - previousValue)
            if jump > jumpLimit:
                anomalies.append(f"[{time}] SKOK: Nagła zmiana o {jump:.2f} (z {previousValue} na {value})")
        
        previousValue = value

    return {
        "bledy_czujnika_ilosc": errorsCounter,
        "wykryte_ostrzezenia": anomalies
    }