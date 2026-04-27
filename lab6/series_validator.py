from abc import ABC, abstractmethod
import numpy as np

from TimeSeries import TimeSeries


class SeriesValidator(ABC):
    
    @abstractmethod
    def analyze(self, series: TimeSeries) -> list[str]:
        pass
