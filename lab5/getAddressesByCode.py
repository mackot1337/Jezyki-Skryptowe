import re
from pathlib import Path
from parseCsvFile import parseCsvFile

def getAddressesByCode(path, station_code):
    path = Path(path)
    
    stationsData = parseCsvFile(path)
    
    # Przetwarzamy adresy, aby oddzielić ulicę od numeru
    pattern = re.compile(r"^(.*?)(?:\s+(\d[^\s]*))?$")
    result = []
    
    for station in stationsData:
        if station.get('Kod stacji', '').strip().lower() == station_code.lower():
            
            county = station.get('Województwo', '').strip()
            cityData = station.get('Miejscowość', '').strip()
            fullAddress = station.get('Adres', '').strip()
            stationName = station.get('Nazwa stacji', '').strip()
            
            if not fullAddress:
                result.append((county, cityData, "", "", stationName))
                continue
                
            match = pattern.match(fullAddress)
            
            if match:
                street = match.group(1) if match.group(1) else fullAddress
                number = match.group(2) if match.group(2) else ""
            else:
                street = fullAddress
                number = ""
                
            result.append((county, cityData, street, number, stationName))
            
    return result