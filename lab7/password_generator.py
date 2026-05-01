import random
import string

class PasswordGenerator:
    def __init__(self, length, charset=string.ascii_letters + string.digits, count=0):
        """
        Inicjalizacja iteratora:
        - length: długość pojedynczego hasła
        - charset: zestaw znaków (domyślnie litery i cyfry)
        - count: maksymalna liczba haseł do wygenerowania
        """
        self.length = length
        self.charset = charset
        self.count = count
        self.current_index = 0  # Licznik wygenerowanych haseł

    def __iter__(self):
        """Metoda zwracająca iterator (zgodnie z protokołem)"""
        return self

    def __next__(self):
        """Metoda zwracająca kolejne hasło lub StopIteration"""
        # Sprawdzenie, czy nie przekroczono limitu haseł
        if self.current_index >= self.count:
            raise StopIteration
        
        # Generowanie losowego hasła o zadanej długości
        password = "".join(random.choices(self.charset, k=self.length))
        
        # Zwiększenie licznika i zwrot hasła
        self.current_index += 1
        return password

# --- Testowanie iteratora (if main) ---

if __name__ == "__main__":
    print("--- Testy Zadania 3 ---")
    
    # 1. Test z jawnym wywołaniem funkcji next()
    print("Test next():")
    pg1 = PasswordGenerator(length=8, count=2)
    print(f"Hasło 1: {next(pg1)}")
    print(f"Hasło 2: {next(pg1)}")
    # Kolejne wywołanie next(pg1) rzuciłoby StopIteration
    
    print("\nTest pętli for (3 hasła po 5 znaków):")
    # 2. Test w pętli for
    pg2 = PasswordGenerator(length=5, count=3)
    for pwd in pg2:
        print(f"Wygenerowane: {pwd}")
        
    print("\nTest skrajny (count=0):")
    pg3 = PasswordGenerator(length=10, count=0)
    # Pętla nie powinna wykonać się ani razu
    for pwd in pg3:
        print("To się nie wyświetli")
    print("Koniec testu skrajnego.")