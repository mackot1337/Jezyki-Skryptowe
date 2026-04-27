import datetime

from TimeSeries import TimeSeries
from series_validator import SeriesValidator


class ThresholdDetector(SeriesValidator):
    def __init__(self, threshold: float):
        self.threshold = threshold

    def analyze(self, series: TimeSeries) -> list[str]:
        anomalies = []
        for i, val in enumerate(series.values):
            if val is not None and val > self.threshold:
                anomalies.append(f"Threshold exceeded: {val} > {self.threshold}, date: {series.dates[i]}")
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

    detector = ThresholdDetector(100.0)

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