import datetime

class TimeSeries:
    def __init__(self, name, stationCode, averageTime, dates, values, unit):
        self.name = name
        self.stationCode = stationCode
        self.averageTime = averageTime
        self.dates = dates
        self.values = values
        self.unit = unit

    def __str__(self):
        return f"Wskaźnik {self.name} - Kod stacji: {self.stationCode}: (Czas uśredniania: {self.averageTime}, Daty: {self.dates}, Wartości: {self.values}, Jednostka: {self.unit})"
    
    def __getitem__(self, key):
        if isinstance(key, int):
            return (self.dates[key], self.values[key])
        elif isinstance(key, slice):
            return list(zip(self.dates[key], self.values[key]))
        elif isinstance(key, (datetime.date, datetime.datetime)):
            results = []
            for d, v in zip(self.dates, self.values):
                if d == key:
                    results.append(v)
            if not results:
                raise KeyError(f"Brak danych dla znacznika czasu {key}")
            return results 
        else:
            raise TypeError("Nieobsługiwany typ klucza")
    
    @property
    def missingCount(self):
        counter = 0
        for v in self.values:
            if v is None:
                counter += 1
        return counter
    
    @property
    def completeness(self):
        total = len(self.values)
        if total == 0:
            return 0.0
        
        count = total - self.missingCount
        return (count / total) * 100.0
    
if __name__ == "__main__":
    d1 = datetime.datetime(2023, 10, 1, 0, 0, 0)
    d2 = datetime.datetime(2023, 10, 1, 12, 0, 0)
    d3 = datetime.datetime(2023, 10, 2, 0, 0, 0)
    d4 = datetime.datetime(2023, 10, 2, 12, 0, 0)

    ts = TimeSeries("As(PM10)", "DsGlogWiStwo", "24g", [d1, d2, d3, d4], [1.57, 5.93, 45.5, None], "ng/m3")

    print(f"Indeks 0: {ts[0]}")
    print(f"Indeksy od 1 do 3: {ts[1:4]}")
    print(f"Konkretna wartosc datetime: {ts[d3]}")

    print(f"Brakujace pomiary: {ts.missingCount}")
    print(f"Kompletnosc: {ts.completeness}")

    badDate = datetime.datetime(1990, 1, 1)
    try:
        print(ts[badDate])
    except KeyError as e:
        print(e)

    try:
        print(ts["Not a date"])
    except TypeError as e:
        print(e)