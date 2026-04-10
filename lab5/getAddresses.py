import re
from pathlib import Path
from parseCsvFile import parseCsvFile

def getAddresses(path, city):
    path = Path(path)
    
    stationsData = parseCsvFile(path)
    
    pattern = re.compile(r"^(.*?)(?:\s+(\d[^\s]*))?$")
    result = []
    
    for station in stationsData:
        if station.get('Miejscowość', '').strip().lower() == city.lower():
            
            county = station.get('Województwo', '').strip()
            cityData = station.get('Miejscowość', '').strip()
            fullAddress = station.get('Adres', '').strip()
            
            if not fullAddress:
                result.append((county, cityData, "", ""))
                continue
                
            match = pattern.match(fullAddress)
            
            if match:
                street = match.group(1) if match.group(1) else fullAddress
                number = match.group(2) if match.group(2) else ""
            else:
                street = fullAddress
                number = ""
                
            result.append((county, cityData, street, number))
            
    return result