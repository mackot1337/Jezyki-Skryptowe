import os
import csv
import datetime
import numpy as np
from abc import ABC, abstractmethod
from typing import Any, Union, Optional

# ==========================
# Station
# ==========================

class Station:
    def __init__(self, stationCode: str, InternationalCode: str, name: str, 
                 oldCode: str, startDate: datetime.date, closeDate: datetime.date, 
                 type: str, areaType: str, stationType: str, province: str, city: str, 
                 address: str, latitude: float, longitude: float) -> None:
        
        self.stationCode: str = stationCode
        self.InternationalCode: str = InternationalCode
        self.name: str = name
        self.oldCode: str = oldCode
        self.startDate: datetime.date = startDate
        self.closeDate: datetime.date = closeDate
        self.type: str = type
        self.areaType: str = areaType
        self.stationType: str = stationType
        self.province: str = province
        self.city: str = city
        self.address: str = address
        self.latitude: float = latitude
        self.longitude: float = longitude

    def __str__(self) -> str:
        return f"Stacja: {self.name} - Kod stacji: {self.stationCode}"
    
    def __repr__(self) -> str:
        return f"Station(stationCode='{self.stationCode}', InternationalCode='{self.InternationalCode}', name='{self.name}', oldCode='{self.oldCode}', startDate={self.startDate}, closeDate={self.closeDate}, type='{self.type}', areaType='{self.areaType}', stationType='{self.stationType}', province='{self.province}', city='{self.city}', address='{self.address}', latitude={self.latitude}, longitude={self.longitude})"
    
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Station):
            return self.stationCode == other.stationCode
        return False
    
# ==========================
# TimeSeries
# ==========================

class TimeSeries:
    def __init__(self, name: str, stationCode: str, averageTime: str, 
                 dates: list[Union[datetime.date, datetime.datetime]], values: list[Optional[float]], unit: str):
        self.name: str = name
        self.stationCode: str = stationCode
        self.averageTime: str = averageTime
        self.dates: list[Union[datetime.date, datetime.datetime]] = dates
        self.values: list[Optional[float]] = values
        self.unit: str = unit

    def __str__(self) -> str:
        return f"Wskaźnik {self.name} - Kod stacji: {self.stationCode}: (Czas uśredniania: {self.averageTime}, Daty: {self.dates}, Wartości: {self.values}, Jednostka: {self.unit})"
    
    def __getitem__(self, key: Union[int, slice, datetime.date, datetime.datetime]) -> Any:
        if isinstance(key, int):
            return (self.dates[key], self.values[key])
        elif isinstance(key, slice):
            return list(zip(self.dates[key], self.values[key]))
        elif isinstance(key, (datetime.date, datetime.datetime)):
            results: list[Optional[float]] = []
            for d, v in zip(self.dates, self.values):
                if d == key:
                    results.append(v)
            if not results:
                raise KeyError(f"Brak danych dla znacznika czasu {key}")
            return results 
        else:
            raise TypeError("Nieobsługiwany typ klucza")
    
    @property
    def missingCount(self) -> int:
        counter: int = 0
        for v in self.values:
            if v is None:
                counter += 1
        return counter
    
    @property
    def completeness(self) -> float:
        total: int = len(self.values)
        if total == 0:
            return 0.0
        
        count: int = total - self.missingCount
        return (count / total) * 100.0
    
# ==========================
# Validators
# ==========================

class SeriesValidator(ABC):
    
    @abstractmethod
    def analyze(self, series: TimeSeries) -> list[str]:
        pass

class OutlierDetector(SeriesValidator):
    def __init__(self, k: float) -> None:
        self.k: float = k

    def analyze(self, series: TimeSeries) -> list[str]:
        valid_values = [v for v in series.values if v is not None]
        if not valid_values:
            return []
        
        mean: float = np.mean(valid_values)
        std: float = np.std(valid_values)
        
        anomalies: list[str] = []
        for i, val in enumerate(series.values):
            if val is not None and abs(val - mean) > self.k * std:
                anomalies.append(f"Outlier: {val}, date: {series.dates[i]}")
        return anomalies
    
class ThresholdDetector(SeriesValidator):
    def __init__(self, threshold: float) -> None:
        self.threshold: float = threshold

    def analyze(self, series: TimeSeries) -> list[str]:
        anomalies: list[str] = []
        for i, val in enumerate(series.values):
            if val is not None and val > self.threshold:
                anomalies.append(f"Threshold exceeded: {val} > {self.threshold}, date: {series.dates[i]}")
        return anomalies
    
class ZeroSpikeDetector(SeriesValidator):
    def analyze(self, series: TimeSeries) -> list[str]:
        anomalies: list[str] = []
        count: int = 0
        block_start: Optional[int] = None
        for i, val in enumerate(series.values):
            if val == 0 or val is None:
                if count == 0:
                    block_start = i
                count += 1
            else:
                if count >= 3:
                    anomalies.append(
                        f"ZeroSpike block: length {count}, dates: {series.dates[block_start]} to {series.dates[i - 1]}"
                    )
                count = 0

        if count >= 3:
            anomalies.append(
                f"ZeroSpike block: length {count}, dates: {series.dates[block_start]} to {series.dates[len(series.values) - 1]}"
            )

        return anomalies
    
class SimpleReporter:
    def analyze(self, series: TimeSeries) -> list[str]:
        valid_values = [v for v in series.values if v is not None]
        if not valid_values:
            return []
        mean: float = float(np.mean(valid_values))
        return [f"Info: {series.name} at {series.stationCode} has mean = {mean:.2f}"]
    
# ==========================
# Measurements
# ==========================

class Measurements:
    def __init__(self, directoryPath: str) -> None:
        self.directoryPath: str = directoryPath
        self.metadata: list[dict[str, Any]] = []
        self.loadedSeries: dict[tuple[str, str], TimeSeries] = {}

        if not os.path.exists(directoryPath):
            raise FileNotFoundError(f"Katalog {directoryPath} nie istnieje.")
        
        if not os.listdir(directoryPath):
            raise ValueError(f"Katalog {directoryPath} jest pusty.")
        
        for filename in os.listdir(directoryPath):
            if filename.endswith(".csv"):
                filepath: str = os.path.join(directoryPath, filename)

                parts: list[str] = filename.replace(".csv", "").split("_")
                parameter: Optional[str] = parts[1] if len(parts) > 1 else None
                frequency: Optional[str] = parts[2] if len(parts) > 2 else None

                try:
                    if os.path.getsize(filepath) == 0:
                        continue
                    
                    with open(filepath, "r", encoding="utf-8") as f:
                        reader = csv.reader(f, delimiter=",")

                        rowNumbers: list[str] = next(reader)      
                        rowStations: list[str] = next(reader)     
                        rowParameters: list[str] = next(reader)   
                        rowFrequency: list[str] = next(reader)    
                        rowUnits: list[str] = next(reader)        
                        rowPositions: list[str] = next(reader)

                        stations: list[str] = []
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

    def __len__(self) -> int:
        counter: int = 0
        for meta in self.metadata:
            counter += len(meta["stations"])
        return counter
    
    def __contains__(self, parameterName: str) -> bool:
        for meta in self.metadata:
            if meta["parameter"] == parameterName:
                return True
        return False
    
    def loadDataForStations(self, meta: dict[str, Any], targetStations: Optional[list[str]]) -> None:
        stationsToLoad: list[str] = targetStations if targetStations else meta["stations"]

        with open(meta["path"], "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=",")
            next(reader)

            headers: list[str] = next(reader)

            for _ in range(4):
                next(reader)

            stationIndices: dict[str, int] = {}
            for station in stationsToLoad:
                if station in headers:
                    stationIndex = headers.index(station)
                    stationIndices[station] = stationIndex

            dates: list[Union[datetime.datetime, datetime.date]] = []
            valuesMap: dict[str, list[Optional[float]]] = {station: [] for station in stationIndices.keys()}

            for row in reader:
                if not row or not row[0].strip():
                    continue

                try:
                    dt: Union[datetime.datetime, datetime.date] = datetime.datetime.strptime(row[0].strip(), "%m/%d/%y %H:%M")
                except ValueError:
                    dt: Union[datetime.datetime, datetime.date] = row[0].strip()

                dates.append(dt)

                for station, index in stationIndices.items():
                    if index < len(row) and row[index].strip():
                        try:
                            value: Optional[float] = float(row[index])
                        except ValueError:
                            value: Optional[float] = None
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

    
    def getByParameter(self, parameterName: str) -> list[TimeSeries]:
        results: list[TimeSeries] = []
        for meta in self.metadata:
            if meta["parameter"] == parameterName:
                for station in meta["stations"]:
                    if (meta['path'], station) not in self.loadedSeries:
                        self.loadDataForStations(meta, [station])

                    results.append(self.loadedSeries[(meta['path'], station)])
        return results
    
    def getByStation(self, stationCode: str) -> list[TimeSeries]:
        results: list[TimeSeries] = []
        for meta in self.metadata:
            if stationCode in meta["stations"]:
                if (meta['path'], stationCode) not in self.loadedSeries:
                    self.loadDataForStations(meta, [stationCode])

                results.append(self.loadedSeries[(meta['path'], stationCode)])
        return results
    
    def detectAllAnomalies(self, validators: list[Any], preload: bool=False) -> dict[TimeSeries, list[str]]:
        if preload:
            for meta in self.metadata:
                for station in meta["stations"]:
                    if (meta['path'], station) not in self.loadedSeries:
                        self.loadDataForStations(meta, [station])

        results: dict[TimeSeries, list[str]] = {}
        for ts in self.loadedSeries.values():
            results[ts] = []
            for validator in validators:
                anomalies = validator.analyze(ts)
                if anomalies:
                    results[ts].extend(anomalies)

        return results

    def runStrategiesOnAllSeries(self, validators: list[Any]) -> dict[str, dict[str, list[str]]]:
        for meta in self.metadata:
            for station in meta["stations"]:
                if (meta['path'], station) not in self.loadedSeries:
                    self.loadDataForStations(meta, [station])

        aggregatedResults: dict[str, dict[str, list[str]]] = {}
        for ts in self.loadedSeries.values():
            seriesKey = f"{ts.name}@{ts.stationCode}"
            aggregatedResults[seriesKey] = {}

            for validator in validators:
                strategyName = validator.__class__.__name__
                aggregatedResults[seriesKey][strategyName] = validator.analyze(ts)

        return aggregatedResults