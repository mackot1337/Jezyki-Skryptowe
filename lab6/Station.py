from datetime import date

class Station:
    def __init__(self, stationCode, InternationalCode, name, oldCode, startDate, closeDate, type, areaType, stationType, province, city, address, latitude, longitude):
        self.stationCode = stationCode
        self.InternationalCode = InternationalCode
        self.name = name
        self.oldCode = oldCode
        self.startDate = startDate
        self.closeDate = closeDate
        self.type = type
        self.areaType = areaType
        self.stationType = stationType
        self.province = province
        self.city = city
        self.address = address
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return f"Stacja: {self.name} - Kod stacji: {self.stationCode}"
    
    def __repr__(self):
        return f"Station(stationCode='{self.stationCode}', InternationalCode='{self.InternationalCode}', name='{self.name}', oldCode='{self.oldCode}', startDate={self.startDate}, closeDate={self.closeDate}, type='{self.type}', areaType='{self.areaType}', stationType='{self.stationType}', province='{self.province}', city='{self.city}', address='{self.address}', latitude={self.latitude}, longitude={self.longitude})"
    
    def __eq__(self, other):
        if isinstance(other, Station):
            return self.stationCode == other.stationCode
        return False

if __name__ == "__main__":
    station1 = Station("DsBialka", "Bialka", "Białka", "", date(1990, 1, 3), date(2005, 12, 31), "przemysłowa", "podmiejski", "kontenerowa stacjonarna", "DOLNOŚLĄSKIE", "Białka", "", 51.197783, 16.117390)
    station2 = Station("DsBielGrot", "Bielawa", "Bielawa", "", date(1994, 1, 2), date(2003, 12, 31), "przemysłowa", "podmiejski", "kontenerowa stacjonarna", "DOLNOŚLĄSKIE", "Bielawa", "", 51.197783, 16.117390)
    station3 = Station("DsBialka", "Bialka", "Białka", "", date(1990, 1, 3), date(2005, 12, 31), "przemysłowa", "podmiejski", "kontenerowa stacjonarna", "DOLNOŚLĄSKIE", "Białka", "", 51.197783, 16.117390)

    print(station1)
    print(station2)

    print(repr(station3))

    print(station1 == station2)
    print(station1 == station3)
    print(station1 == "Not a station")
    print(station1 == None)
