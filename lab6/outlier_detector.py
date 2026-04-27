import numpy as np

from TimeSeries import TimeSeries
from series_validator import SeriesValidator


class OutlierDetector(SeriesValidator):
    def __init__(self, k: float):
        self.k = k

    def analyze(self, series: TimeSeries) -> list[str]:
        mean = np.nanmean([v for v in series.values if v is not None])
        std = np.nanstd([v for v in series.values if v is not None])
        
        anomalies = []
        for i, val in enumerate(series.values):
            if val is not None and abs(val - mean) > self.k * std:
                anomalies.append(f"Outlier: {val} at index {i} (date: {series.dates[i]})")
        return anomalies