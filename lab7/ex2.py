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
    print(f"2a. forall(is_positive, [1, 2, 3]): {forall(is_positive, [1, 2, 3])}")  # Wynik: True
    print(f"2a. Skrajny (pusta lista): {forall(is_positive, [])}")                # Wynik: True (pusta spełnia próżniowo)

    # b. exists
    print(f"2b. exists(is_even, [1, 3, 4]): {exists(is_even, [1, 3, 4])}")         # Wynik: True
    print(f"2b. Skrajny (pusta lista): {exists(is_even, [])}")                  # Wynik: False

    # c. atleast
    # Przynajmniej 2 liczby parzyste w liście
    print(f"2c. atleast(2, is_even, [1, 2, 4, 5]): {atleast(2, is_even, [1, 2, 4, 5])}") # Wynik: True
    print(f"2c. Skrajny (n=0, pusta lista): {atleast(0, is_even, [])}")                # Wynik: True (0 >= 0)

    # d. atmost
    # Najwyżej 1 liczba parzysta w liście[cite: 3]
    print(f"2d. atmost(1, is_even, [1, 2, 4, 5]): {atmost(1, is_even, [1, 2, 4, 5])}")   # Wynik: False
    print(f"2d. Skrajny (n=5, pusta lista): {atmost(5, is_even, [])}")                  # Wynik: True (0 <= 5)