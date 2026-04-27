import os
import csv
import datetime
from TimeSeries import TimeSeries
import shutil

from outlier_detector import OutlierDetector
from simple_reporter import SimpleReporter
from threshold_detector import ThresholdDetector
from zero_spike_detector import ZeroSpikeDetector


class Measurements:
    def __init__(self, directoryPath):
        self.directoryPath = directoryPath
        self.metadata = []
        self.loadedSeries = {}

        if not os.path.exists(directoryPath):
            raise FileNotFoundError(f"Katalog {directoryPath} nie istnieje.")
        # dodac sprawdzanie czy jest pusty i czy uzytkownik ma dostep
        
        for filename in os.listdir(directoryPath):
            if filename.endswith(".csv"):
                filepath = os.path.join(directoryPath, filename)

                parts = filename.replace(".csv", "").split("_")
                parameter = parts[1] if len(parts) > 1 else None
                frequency = parts[2] if len(parts) > 2 else None

                try:
                    #dodac sprawdzanie czy jest pusty wszedzie tam gdzie zczytujemy dane
                    with open(filepath, "r", encoding="utf-8") as f:
                        reader = csv.reader(f, delimiter=";")

                        rowNumbers = next(reader)      
                        rowStations = next(reader)     
                        rowParameters = next(reader)   
                        rowFrequency = next(reader)    
                        rowUnits = next(reader)        
                        rowPositions = next(reader)

                        stations = []
                        if len(rowStations) > 1:
                            for station in rowStations[1:]:
                                if station.strip():
                                    stations.append(station.strip())

                            self.metadata.append({
                                "path": filepath,
                                "parameter": rowParameters[1].strip() if len(rowParameters) > 1 else parameter,
                                "frequency": rowFrequency[1].strip() if len(rowFrequency) > 1 else frequency,
                                "stations": stations
                            })
                except Exception: 
                    pass

    def __len__(self):
        counter = 0
        for meta in self.metadata:
            counter += len(meta["stations"])
        return counter
    
    def __contains__(self, parameterName):
        for meta in self.metadata:
            if meta["parameter"] == parameterName:
                return True
        return False
    
    def loadDataForStations(self, meta, targetStations):
        stationsToLoad = targetStations if targetStations else meta["stations"]

        with open(meta["path"], "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=";")
            next(reader)

            headers = next(reader)

            for i in range(4):
                next(reader)

            stationIndices = {}
            for station in stationsToLoad:
                if station in headers:
                    stationIndex = headers.index(station)
                    stationIndices[station] = stationIndex

            dates = []
            valuesMap = {station: [] for station in stationIndices.keys()}

            for row in reader:
                if not row or not row[0].strip():
                    continue

                try:
                    dt = datetime.datetime.strptime(row[0].strip(), "%m/%d/%y %H:%M")
                except ValueError:
                    dt = row[0].strip()

                dates.append(dt)

                for station, index in stationIndices.items():
                    if index < len(row) and row[index].strip():
                        try:
                            value = float(row[index].replace(",", "."))
                        except ValueError:
                            value = None
                    else:
                        value = None
                    valuesMap[station].append(value)

        for station, values in valuesMap.items():
            ts = TimeSeries(
                name=meta["parameter"],
                stationCode=station,
                averageTime=meta["frequency"],
                dates=dates,
                values=values,
                unit="ng/m3"
            )
            self.loadedSeries[(meta["path"], station)] = ts

    
    def getByParameter(self, parameterName):
        results = []
        for meta in self.metadata:
            if meta["parameter"] == parameterName:
                for station in meta["stations"]:
                    if (meta['path'], station) not in self.loadedSeries:
                        self.loadDataForStations(meta, [station])

                    results.append(self.loadedSeries[(meta['path'], station)])
        return results
    
    def getByStation(self, stationCode):
        results = []
        for meta in self.metadata:
            if stationCode in meta["stations"]:
                if (meta['path'], stationCode) not in self.loadedSeries:
                    self.loadDataForStations(meta, [stationCode])

                results.append(self.loadedSeries[(meta['path'], stationCode)])
        return results
    
    def detectAllAnomalies(self, validators, preload=False):
        if preload:
            for meta in self.metadata:
                for station in meta["stations"]:
                    if (meta['path'], station) not in self.loadedSeries:
                        self.loadDataForStations(meta, [station])

        results = {}
        for ts in self.loadedSeries.values():
            results[ts] = []
            for validator in validators:
                anomalies = validator.analyze(ts)
                if anomalies:
                    results[ts].extend(anomalies)

        return results
#-----------nowe-----------------
    def runStrategiesOnAllSeries(self, validators):
        for meta in self.metadata:
            for station in meta["stations"]:
                if (meta['path'], station) not in self.loadedSeries:
                    self.loadDataForStations(meta, [station])

        aggregatedResults = {}
        for ts in self.loadedSeries.values():
            seriesKey = f"{ts.name}@{ts.stationCode}"
            aggregatedResults[seriesKey] = {}

            for validator in validators:
                strategyName = validator.__class__.__name__
                aggregatedResults[seriesKey][strategyName] = validator.analyze(ts)

        return aggregatedResults
    #-----------nowe-----------------
if __name__ == "__main__":
    print("ROZPOCZYNAM TESTY KLASY MEASUREMENTS")

    testDir = "testDir"
    os.makedirs(testDir, exist_ok=True)

    csvContent1 = """Nr;1;2
Kod stacji;DsBialka;DsBielGrot
Wskaźnik;PM10;PM10
Czas uśredniania;1g;1g
Jednostka;ug/m3;ug/m3
Kod stanowiska;Bialka-kod;BielGrot-kod
10/01/23 00:00;10.5;15.0
10/01/23 01:00;12.0;"""

    csvContent2 = """Nr;1;2
Kod stacji;DsBialka;MzKrakow
Wskaźnik;toluen;toluen
Czas uśredniania;24g;24g
Jednostka;ug/m3;ug/m3
Kod stanowiska;Bialka-kod;Krakow-kod
10/01/23 00:00;1.2;3.4
10/01/23 01:00;;5.5"""

    with open(os.path.join(testDir, "2023_PM10_1g.csv"), "w", encoding="utf-8") as f:
        f.write(csvContent1)
    with open(os.path.join(testDir, "2023_toluen_24g.csv"), "w", encoding="utf-8") as f:
        f.write(csvContent2)

    try:
        measurements = Measurements(testDir)
        print("\nTestowanie metod specjalnych:")
        assert len(measurements) == 4, "Błędna liczba stacji"
        assert "PM10" in measurements, "Nie znaleziono parametru PM10"
        assert "toluen" in measurements, "Nie znaleziono parametru toluen"
        assert "KOSMITA" not in measurements, "Nie powinno być parametru KOSMITA"
        print("Metody specjalne działają poprawnie.")

        print("\nTestowanie getByParameter:")
        pm10Series = measurements.getByParameter("PM10")
        assert len(pm10Series) == 2, "Niepoprawna liczba serii dla PM10"
        emptySeries = measurements.getByParameter("KOSMITA")
        assert len(emptySeries) == 0, "Nie powinno być serii dla KOSMITA"
        print("getByParameter działa poprawnie.")

        print("\nTestowanie getByStation:")
        bialkaSeries = measurements.getByStation("DsBialka")
        assert len(bialkaSeries) == 2, "Niepoprawna liczba serii dla stacji DsBialka"
        bielGrotSeries = measurements.getByStation("DsBielGrot")
        assert len(bielGrotSeries) == 1, "Niepoprawna liczba serii dla stacji DsBielGrot"
        emptySeries = measurements.getByStation("NieistniejacaStacja")
        assert len(emptySeries) == 0, "Nie powinno być serii dla nieistniejącej stacji"
        print("getByStation działa poprawnie.")

        print("\nTestowanie detectAllAnomalies:")
        class MockValidator:
            def analyze(self, series):
                if series.missingCount > 0:
                    return [f"Znaleziono {series.missingCount} brakujących pomiarów w {series.name}"]
                return []
            
        validators = [MockValidator()]
        resultsNoPreload = measurements.detectAllAnomalies(validators, preload=False)
        assert len(resultsNoPreload) == 3, "Niepoprawna liczba serii w wynikach bez preload"
        resultsPreload = measurements.detectAllAnomalies(validators, preload=True)
        assert len(resultsPreload) == 4, "Niepoprawna liczba serii w wynikach z preload"
        print("detectAllAnomalies działa poprawnie.")

#-----------nowe-----------------
        print("\nDemonstracja kaczego typowania:")
        demoSeries = TimeSeries(
            name="PM10",
            stationCode="DsDemo01",
            averageTime="1g",
            dates=[
                datetime.datetime(2023, 10, 1, 0, 0),
                datetime.datetime(2023, 10, 1, 1, 0),
                datetime.datetime(2023, 10, 1, 2, 0),
                datetime.datetime(2023, 10, 1, 3, 0),
                datetime.datetime(2023, 10, 1, 4, 0),
                datetime.datetime(2023, 10, 1, 5, 0),
                datetime.datetime(2023, 10, 1, 6, 0),
            ],
            values=[12.0, 0.0, None, 0.0, 0.0, 0.0, 95.0],
            unit="ug/m3",
        )

        analyzers = [
            OutlierDetector(k=1.4),
            ZeroSpikeDetector(),
            ThresholdDetector(threshold=80.0),
            SimpleReporter(),
        ]

        for analyzer in analyzers:
            print(f"\n{analyzer.__class__.__name__}:")
            for info in analyzer.analyze(demoSeries):
                print(f" - {info}")

        print("\nWniosek: wywołujemy analyze(series) na obiektach różnych klas bez sprawdzania typu.")
        print("To pokazuje polimorfizm strukturalny (kacze typowanie) w Pythonie.")

        print("\nUruchamianie każdej strategii (SeriesValidator) na każdym szeregu czasowym:")
        strategies = [
            OutlierDetector(k=1.4),
            ZeroSpikeDetector(),
            ThresholdDetector(threshold=11.0),
        ]
        aggregated = measurements.runStrategiesOnAllSeries(strategies)
        for seriesKey, strategyResults in aggregated.items():
            print(f"\nSeria: {seriesKey}")
            for strategyName, anomalies in strategyResults.items():
                print(f" - {strategyName}: {anomalies}")
#-----------nowe-----------------
    finally:
        shutil.rmtree(testDir)
        print("Testy zakończone.")