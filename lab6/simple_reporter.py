import numpy as np


class SimpleReporter:
    def analyze(self, series):
        mean = np.mean([v for v in series.values if v is not None])
        return [f"Info: {series.name} at {series.stationCode} has mean = {mean:.2f}"]
