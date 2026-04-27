class SimpleReporter:
    def analyze(self, series):
        validValues = [v for v in series.values if v is not None]
        meanValue = sum(validValues) / len(validValues) if validValues else 0.0
        return [f"Info: {series.name} at {series.stationCode} has mean = {meanValue:.2f}"]
