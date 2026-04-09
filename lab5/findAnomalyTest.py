from findAnomaly import findAnomaly

def runTest():
    print("Rozpoczynam testowanie wykrywania anomalii...")
    
    testData = [
        {'Czas': '12:00', 'Wartość': '20,5'},  
        {'Czas': '13:00', 'Wartość': '25,0'},  
        {'Czas': '14:00', 'Wartość': '150,0'}, 
        {'Czas': '15:00', 'Wartość': '600,0'},
        {'Czas': '16:00', 'Wartość': ''},      
        {'Czas': '17:00', 'Wartość': '-10,0'}, 
        {'Czas': '18:00', 'Wartość': 'Brak'}   
    ]
    
    report = findAnomaly(testData, alarmLimit=500.0, jumpLimit=100.0)
    
    assert report["bledy_czujnika_ilosc"] == 2, "Błąd testu: Zła liczba błędów czujnika!"
    
    attentions = report["wykryte_ostrzezenia"]
    assert len(attentions) == 4, f"Błąd testu: Oczekiwano 4 ostrzeżeń, znaleziono {len(attentions)}"
    assert any("SKOK" in o and "150.0" in o for o in attentions), "Brak komunikatu o skoku o 14:00"
    assert any("ALARM" in o and "600.0" in o for o in attentions), "Brak komunikatu o alarmie o 15:00"
    assert any("ujemna" in o for o in attentions), "Brak komunikatu o ujemnej wartości"
    
    print("Wszystkie testy anomalii ZALICZONE!")
    print("\nOto Twój raport z anomalii (podgląd):")
    print(f"Ilość braków danych: {report['bledy_czujnika_ilosc']}")
    for attention in attentions:
        print(f" -> {attention}")

if __name__ == "__main__":
    runTest()