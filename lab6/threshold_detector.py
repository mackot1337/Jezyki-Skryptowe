from lab6.TimeSeries import TimeSeries
from lab6.series_validator import SeriesValidator


class ThresholdDetector(SeriesValidator):
    def __init__(self, threshold: float):
        self.threshold = threshold

    def analyze(self, series: TimeSeries) -> list[str]:
        anomalies = []
        for i, val in enumerate(series.values):
            if val is not None and val > self.threshold:
                anomalies.append(f"Threshold exceeded: {val} > {self.threshold} at index {i}")
        return anomalies