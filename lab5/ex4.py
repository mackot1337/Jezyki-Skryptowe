import re

def pullDates(stationData):
    pattern = re.compile(r"\d{4}-\d{2}-\d{2}")
    foundDates = []
    
    for stacja in stationData:
        startDate = stacja.get('Data uruchomienia', '')
        endDate = stacja.get('Data zamknięcia', '')
        
        if pattern.match(startDate) and startDate not in foundDates:
            foundDates.append(startDate)
            
        if pattern.match(endDate) and endDate not in foundDates:
            foundDates.append(endDate)
            
    return foundDates

def pullCoordinates(stationData):
    pattern = re.compile(r"^\d+\.\d{6}$")
    coordinates = []
    
    for station in stationData:
        latitude = station.get('WGS84 φ N', '').strip()
        longitude = station.get('WGS84 λ E', '').strip()
        
        if pattern.match(latitude) and pattern.match(longitude):
            coordinates.append((latitude, longitude))
            
    return coordinates

def pullTwoPartNames(stationData):
    pattern = re.compile(r"^[^-]+-[^-]+$")
    result = []
    
    for station in stationData:
        name = station.get('Nazwa stacji', '')
        if pattern.match(name):
            result.append(name)
            
    return result

def pullThreePartNames(stationData):
    pattern = re.compile(r"^[^-]+-[^-]+-[^-]+$")
    result = []
    
    for station in stationData:
        name = station.get('Nazwa stacji', '')
        if pattern.match(name):
            result.append(name)
            
    return result

def cleanName(name):
    name = re.sub(r"\s+", "_", name)
    
    def substitute(match):
        dict = {'ą':'a', 'ć':'c', 'ę':'e', 'ł':'l', 'ń':'n', 'ó':'o', 'ś':'s', 'ź':'z', 'ż':'z',
                   'Ą':'A', 'Ć':'C', 'Ę':'E', 'Ł':'L', 'Ń':'N', 'Ó':'O', 'Ś':'S', 'Ź':'Z', 'Ż':'Z'}
        return dict[match.group()]
        
    name = re.sub(r"[ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]", substitute, name)
    
    return name

def verify_mob(stationData):
    pattern_mob = re.compile(r"MOB$")
    
    for station in stationData:
        code = station.get('Kod stacji', '')
        type = station.get('Rodzaj stacji', '').lower()
        
        if pattern_mob.search(code):
            if 'mobilna' not in type:
                return False 
                
    return True

def stationWithStreet(stationData):
    pattern = re.compile(r",\s*(ul\.|al\.)")
    result = []
    
    for station in stationData:
        name = station.get('Nazwa stacji', '')
        if pattern.search(name):
            result.append(name)
            
    return result