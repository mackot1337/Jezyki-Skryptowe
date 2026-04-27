from pathlib import Path

from Measurements import Measurements
from zero_spike_detector import ZeroSpikeDetector
from outlier_detector import OutlierDetector
from threshold_detector import ThresholdDetector

def run_demo():
    base_dir = Path(__file__).resolve().parent
    measurements_dir = base_dir / "measurements" 
    
    print("=== LAB 6: Test klasy Measurements na realnych danych ===")
    print(f"Katalog pomiarow: {measurements_dir}")

    measurements = Measurements(str(measurements_dir))
    
    # --- Test 1: __len__ ---
    metadata_count = len(measurements.metadata)
    expected_series_count = sum(len(meta["stations"]) for meta in measurements.metadata)

    print("\n--- 1) __len__ (Liczba możliwych serii) ---")
    print(f"Liczba plikow rozpoznanych w metadata: {metadata_count}")
    print(f"Oczekiwano stacji = {expected_series_count}")
    print(f"Otrzymano stacji = {len(measurements)}")
    print(f"Test __len__ zaliczony: {expected_series_count == len(measurements)}")

    # --- Test 2: __contains__ ---
    sample_parameter = "SO2"
    bad_parameter = "zly_parametr"

    print("\n--- 2) __contains__ (Sprawdzanie obecności wskaźnika) ---")
    print(f"Czy zbiór zawiera '{sample_parameter}'? {'Tak' if sample_parameter in measurements else 'Nie'} (oczekiwano: Tak)")
    print(f"Czy zbiór zawiera '{bad_parameter}'? {'Tak' if bad_parameter in measurements else 'Nie'} (oczekiwano: Nie)")

    # --- Test 3: getByParameter ---
    print(f"\n--- 3) getByParameter dla '{sample_parameter}' ---")
    param_series = measurements.getByParameter(sample_parameter)
    
    print(f"Liczba wczytanych serii dla {sample_parameter}: {len(param_series)}")
    if param_series:
        first_series = param_series[0]
        print(f"Sukces! Pierwsza wczytana seria to: Stacja {first_series.stationCode}, Pomiary: {len(first_series.values)}")
    else:
        print(f"UWAGA: Nie wczytano żadnych serii. Sprawdź, czy masz plik z {sample_parameter} w folderze.")

    # --- Test 4: getByStation ---
    print("\n--- 4) getByStation ---")
    if measurements.metadata and measurements.metadata[0]["stations"]:
        sample_station = measurements.metadata[0]["stations"][0]
        print(f"Test dla stacji: '{sample_station}'")
        
        station_series = measurements.getByStation(sample_station)
        print(f"Liczba wczytanych serii dla stacji {sample_station}: {len(station_series)}")
        
        if station_series:
            print("Wczytane wskaźniki dla tej stacji:")
            for s in station_series:
                print(f" - {s.unit} (Pomiarów: {len(s.values)})")
    else:
        print("Brak metadanych lub stacji do przetestowania.")

    #--- Test 5: detectAllAnomalies ---
    print("\n--- 5) detectAllAnomalies (Roznice leniwego wczytywania) ---")
    validators = [ZeroSpikeDetector(), ThresholdDetector(threshold=100.0)]
    
    # Tworzymy nowy obiekt Measurements, aby pokazac stan od zera
    measurements_lazy = Measurements(str(measurements_dir))
    print(f"Poczatkowa liczba wczytanych serii w nowym obiekcie: {len(measurements_lazy.loadedSeries)}")
    
    results_no_preload = measurements_lazy.detectAllAnomalies(validators, preload=False)
    print("Po wykonaniu detectAllAnomalies(preload=False):")
    print(f" - Liczba wczytanych serii: {len(measurements_lazy.loadedSeries)}")
    print(f" - Liczba serii przebadanych: {len(results_no_preload)}")
    
    results_preload = measurements_lazy.detectAllAnomalies(validators, preload=True)
    print("\nPo wykonaniu detectAllAnomalies(preload=True):")
    print(f" - Liczba wczytanych serii (loadedSeries): {len(measurements_lazy.loadedSeries)}")
    print(f" - Liczba serii przebadanych: {len(results_preload)}")

    print("\nWypisanie znalezionych anomalii:")
    anomalies_found = False
    for ts, anomalies in results_preload.items():
        if anomalies:
            anomalies_found = True
            print(f" -> [{ts.name} @ {ts.stationCode}] Znaleziono {len(anomalies)} anomalie:")
            for idx, anomaly in enumerate(anomalies, 1):
                print(f"    {idx}. {anomaly}")
    
    if not anomalies_found:
        print("  Brak anomalii dla zadanych kryteriów w wczytanych danych.")

if __name__ == "__main__":
    run_demo()