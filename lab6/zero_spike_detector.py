from TimeSeries import TimeSeries
from series_validator import SeriesValidator


class ZeroSpikeDetector(SeriesValidator):
    def analyze(self, series: TimeSeries) -> list[str]:
        anomalies = []
        count = 0
        block_start = None
        for i, val in enumerate(series.values):
            if val == 0 or val is None:
                if count == 0:
                    block_start = i
                count += 1
            else:
                if count >= 3:
                    anomalies.append(
                        f"ZeroSpike block: length {count}, start index {block_start}, end index {i - 1}"
                    )
                count = 0

        if count >= 3:
            anomalies.append(
                f"ZeroSpike block: length {count}, start index {block_start}, end index {len(series.values) - 1}"
            )

        return anomalies