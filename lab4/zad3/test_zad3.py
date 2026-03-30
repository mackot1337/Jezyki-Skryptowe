from tail_util import tail_logic

def test_zad3():
    print("Rozpoczynam testy...")
    
    # 1. Testowanie wartości skrajnych (pusta lista, lista mniejsza niż n)
    assert tail_logic([], 10) == [], "Błąd: Pusta lista powinna zwrócić pustą listę."
    assert tail_logic(["a\n", "b\n"], 10) == ["a\n", "b\n"], "Błąd: Mniej linii niż żądano powinno zwrócić wszystko."
    
    # 2. Testowanie poprawnego zwracania ostatnich n linii
    data = ["1\n", "2\n", "3\n", "4\n", "5\n"]
    assert tail_logic(data, 2) == ["4\n", "5\n"], "Błąd: Zwrócono nieprawidłowe ostatnie linie."
    
    # 3. Testowanie wartości problematycznych (np. ujemne n lub zero)
    assert tail_logic(data, 0) == [], "Błąd: n=0 powinno zwrócić pustą listę."
    assert tail_logic(data, -5) == [], "Błąd: n ujemne powinno zwrócić pustą listę."

    print("Wszystkie testy zakończone pomyślnie!\n")