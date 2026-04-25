from datetime import date

class Station:
    def __init__(self, stationCode, name, startDate, closeDate):
        self.stationCode = stationCode
        self.name = name
        self.startDate = startDate
        self.closeDate = closeDate

    def __str__(self):
        return f"Stacja: {self.name} - Kod stacji: {self.stationCode}"
    
    def __repr__(self):
        return f"Station: {self.name} (Station number: {self.stationCode}, Start date: {self.startDate}, Close date: {self.closeDate})"
    
    def __eq__(self, other):
        if not isinstance(other, Station):
            return False
        return self.stationCode == other.stationCode
    
if __name__ == "__main__":
    station1 = Station("DsBialka", "Bialka", date(1990, 1, 3), date(2005, 12, 31))
    station2 = Station("DsBielGrot", "Bielawa", date(1994, 1, 2), date(2003, 12, 31))
    station3 = Station("DsBialka", "Bialka", date(1990, 1, 3), date(2005, 12, 31))

    print(station1)
    print(station2)

    print(repr(station3))

    print(station1 == station2)
    print(station1 == station3)