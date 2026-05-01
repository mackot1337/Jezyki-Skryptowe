def forall(pred, iterable):
    return all([pred(x) for x in iterable])


def exists(pred, iterable):
    return any([pred(x) for x in iterable])


def atleast(n, pred, iterable):
    return sum([1 for x in iterable if pred(x)]) >= n


def atmost(n, pred, iterable):
    return sum([1 for x in iterable if pred(x)]) <= n


if __name__ == "__main__":
    print("--- Testy Zadania 2 ---")

    # Przykładowy predykat: czy liczba jest dodatnia
    is_positive = lambda x: x > 0
    # Przykładowy predykat: czy liczba jest parzysta
    is_even = lambda x: x % 2 == 0

    # a. forall
    assert forall(is_positive, [1, 2, 3]) == True
    print(f"2a. forall(is_positive, [1, 2, 3]): {forall(is_positive, [1, 2, 3])}")# Wynik: True
    assert forall(is_positive, []) == True
    print(f"2a. Skrajny (pusta lista): {forall(is_positive, [])}") # Wynik: True
    print("Test 2a zakończony pomyślnie\n")

    # b. exists
    assert exists(is_even, [1, 3, 4]) == True
    print(f"2b. exists(is_even, [1, 3, 4]): {exists(is_even, [1, 3, 4])}") # Wynik: True
    assert exists(is_even, []) == False
    print(f"2b. Skrajny (pusta lista): {exists(is_even, [])}") # Wynik: False
    print("Test 2b zakończony pomyślnie\n")

    # c. atleast
    # Przynajmniej 2 liczby parzyste w liście
    assert atleast(2, is_even, [1, 2, 4, 5]) == True
    print(f"2c. atleast(2, is_even, [1, 2, 4, 5]): {atleast(2, is_even, [1, 2, 4, 5])}") # Wynik: True
    assert atleast(0, is_even, []) == True
    print(f"2c. Skrajny (n=0, pusta lista): {atleast(0, is_even, [])}")                # Wynik: True (0 >= 0)
    print("Test 2c zakończony pomyślnie\n")

    # d. atmost
    # Najwyżej 1 liczba parzysta w liście
    assert atmost(1, is_even, [1, 2, 4, 5]) == False
    print(f"2d. atmost(1, is_even, [1, 2, 4, 5]): {atmost(1, is_even, [1, 2, 4, 5])}")   # Wynik: False
    assert atmost(5, is_even, []) == True
    print(f"2d. Skrajny (n=5, pusta lista): {atmost(5, is_even, [])}")                  # Wynik: True (0 <= 5)
    print("Test 2d zakończony pomyślnie\n")