from __future__ import annotations

import csv
from pathlib import Path
from typing import Callable, Iterable

from Measurements import Measurements

def run_demo():
    base_dir = Path(__file__).resolve().parent
    measurements_dir = base_dir / "measurements"
    stations_csv = base_dir / "stacje.csv"

    print("=== LAB6: test klasy Measurements na realnych danych ===")
    print(f"Katalog pomiarow: {measurements_dir}")
    print(f"Plik stacji: {stations_csv}")

    measurements = Measurements(str(measurements_dir))

    metadata_count = len(measurements.metadata)
    expected_series_count = sum(len(meta["stations"]) for meta in measurements.metadata)

    print("\n--- 1) __len__ ---")
    print(f"Liczba plikow rozpoznanych w metadata: {metadata_count}")
    print(f"oczekiwano={expected_series_count}")
    print(f"otrzymano={len(measurements)}")

    print(f"get_by_parameter: {measurements.getByParameter("SO2")}")
    print(f"get_by_station: {measurements.getByStation("WmPuszczaBor")}")

    # sample_parameter = measurements.metadata[1]["parameter"] if measurements.metadata else None
    # bogus_parameter = "__NIEISTNIEJACY_WSKAZNIK__"

    # print("\n--- 2) __contains__(parameter_name) ---")
    # print(f"Testowany istniejacy parametr: {sample_parameter}")
    # print("oczekiwano=True")
    # print(f"otrzymano={sample_parameter in measurements}")

    # print(f"Testowany brakujacy parametr: {bogus_parameter}")
    # print("oczekiwano=False")
    # print(f"otrzymano={bogus_parameter in measurements}")

    # print("\n--- 3) get_by_parameter(param_name) / getByParameter(param_name) ---")
    # loaded_before = len(measurements.loadedSeries)
    # series_for_parameter = get_by_parameter(sample_parameter)
    # loaded_after = len(measurements.loadedSeries)

    # print("oczekiwano=lista serii dla istniejacego parametru")
    # print(f"otrzymano=typ {type(series_for_parameter).__name__}, liczba_serii {len(series_for_parameter)}")
    # print("oczekiwano=wzrost loadedSeries po pierwszym dostepie (leniwe ladowanie)")
    # print(f"otrzymano=loadedSeries przed={loaded_before}, po={loaded_after}")

    # empty_parameter_series = get_by_parameter(bogus_parameter)
    # print("oczekiwano=pusta lista dla nieistniejacego parametru")
    # print(f"otrzymano=liczba_serii {len(empty_parameter_series)}")

    # print("\n--- 4) get_by_station(station_code) / getByStation(station_code) ---")
    # station_rows = _load_station_rows(stations_csv)
    # stations_from_catalog = {row["Kod stacji"] for row in station_rows if row.get("Kod stacji")}

    # stations_from_measurements = []
    # for meta in measurements.metadata:
    #     for station_code in meta["stations"]:
    #         stations_from_measurements.append(station_code)

    # shared_station_codes = [code for code in stations_from_measurements if code in stations_from_catalog]
    # sample_station_code = _first_or_none(shared_station_codes) or _first_or_none(stations_from_measurements)

    # if sample_station_code is None:
    #     print("oczekiwano=co najmniej jedna stacja do testu")
    #     print("otrzymano=brak stacji - pomijam dalszy test get_by_station")
    #     return

    # station_series = get_by_station(sample_station_code)

    # print(f"Testowana stacja: {sample_station_code}")
    # print("oczekiwano=lista serii dla danej stacji")
    # print(f"otrzymano=typ {type(station_series).__name__}, liczba_serii {len(station_series)}")

    # empty_station_code = "__NIEISTNIEJACA_STACJA__"
    # empty_station_series = get_by_station(empty_station_code)
    # print("oczekiwano=pusta lista dla nieistniejacej stacji")
    # print(f"otrzymano=liczba_serii {len(empty_station_series)}")

    # print("\n--- 5) Krotkie podsumowanie zaladowanych serii ---")
    # if station_series:
    #     first_series = station_series[0]
    #     print(
    #         "Przyklad TimeSeries: "
    #         f"name={first_series.name}, station={first_series.stationCode}, "
    #         f"freq={first_series.averageTime}, probek={len(first_series.values)}"
    #     )

    # print("\nWYNIK: dane zostaly wczytane i wypisane zgodnie z punktami zadania (oczekiwano/otrzymano).")


if __name__ == "__main__":
    run_demo()
