import random
import string

class PasswordGenerator:
    def __init__(self, length, charset=string.ascii_letters + string.digits, count=0):
        self.length = length
        self.charset = charset
        self.count = count
        self.current_index = 0

    def __iter__(self):
        """Metoda zwracająca iterator"""
        return self

    def __next__(self):
        """Metoda zwracająca kolejne hasło lub StopIteration"""

        if self.current_index >= self.count:
            raise StopIteration
        
        password = "".join(random.choices(self.charset, k=self.length))
        
        self.current_index += 1
        return password

if __name__ == "__main__":
    print("--- Testy Zadania 3 ---")
    
    # 1. Test z jawnym wywołaniem funkcji next()
    print("Test next():")
    pg1 = PasswordGenerator(length=8, count=2)
    pwd1 = next(pg1)
    assert len(pwd1) == 8
    print(f"Hasło 1: {pwd1}")
    pwd2 = next(pg1)
    assert len(pwd2) == 8
    print(f"Hasło 2: {pwd2}")
    
    try:
        next(pg1)
        assert False, "Powinno rzucić StopIteration"
    except StopIteration:
        pass
    print("Test 3a zakończony pomyślnie\n")
    
    print("Test pętli for (3 hasła po 10 znaków):")
    # 2. Test w pętli for
    pg2 = PasswordGenerator(length=10, count=3)
    generated_count = 0
    for pwd in pg2:
        assert len(pwd) == 10
        generated_count += 1
        print(f"Wygenerowane: {pwd}")
    assert generated_count == 3
    print("Test 3b zakończony pomyślnie\n")
        
    print("Test skrajny (count=0):")
    pg3 = PasswordGenerator(length=10, count=0)
    for pwd in pg3:
        assert False, "Nie powinno wygenerować żadnego hasła"
        print("To się nie wyświetli")
    print("Koniec testu skrajnego.")
    print("Test 3c zakończony pomyślnie\n")