import datetime
import numpy as np

from TimeSeries import TimeSeries
from series_validator import SeriesValidator


class OutlierDetector(SeriesValidator):
    def __init__(self, k: float):
        self.k = k

    def analyze(self, series: TimeSeries) -> list[str]:
        valid_values = [v for v in series.values if v is not None]
        if not valid_values:
            return []
        
        mean = np.mean([v for v in series.values if v is not None])
        std = np.std([v for v in series.values if v is not None])
        
        anomalies = []
        for i, val in enumerate(series.values):
            if val is not None and abs(val - mean) > self.k * std:
                anomalies.append(f"Outlier: {val}, date: {series.dates[i]}")
        return anomalies


def test():
    base_dates = [
        datetime.datetime(2024, 1, 1, 0, 0),
        datetime.datetime(2024, 1, 1, 1, 0),
        datetime.datetime(2024, 1, 1, 2, 0),
        datetime.datetime(2024, 1, 1, 3, 0),
        datetime.datetime(2024, 1, 1, 4, 0),
        datetime.datetime(2024, 1, 1, 5, 0),
    ]

    empty_series = TimeSeries("test", "ST", "1h", [], [], "u")
    full_series = TimeSeries("test", "ST", "1h", base_dates, [1.0, 1.0, 1.0, 1000.0, 1.0, 1.0], "u")
    gapped_series = TimeSeries("test", "ST", "1h", base_dates, [1.0, 0.0, None, 0.0, 1000.0, 1.0], "u")

    detector = OutlierDetector(1.5)

    # test1: pusta seria
    assert detector.analyze(empty_series) == []
    print("Test 1 passed: Empty series")

    # test2: pelna seria
    assert len(detector.analyze(full_series)) == 1
    print("Test 2 passed: Full series")

    # test3: pelna seria z dziurami
    assert len(detector.analyze(gapped_series)) == 1
    print(detector.analyze(gapped_series))
    print("Test 3 passed: Full series with gaps")


if __name__ == "__main__":
    test()