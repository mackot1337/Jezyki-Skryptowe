def liczba(numbers):
    return (numbers[0] if numbers[0] % 2 != 0 else 0) + liczba(numbers[1:]) if numbers else 0


def median(numbers):
    sorted_n = sorted(numbers)
    n = len(sorted_n)
    mid = n // 2
    return (sorted_n[mid] if n % 2 != 0 else (sorted_n[mid - 1] + sorted_n[mid]) / 2) if numbers else None


def pierwiastek(x, epsilon, y=1.0):
    return None if not (x > 0 or epsilon > 0) else y if abs(y**2 - x) < epsilon else pierwiastek(x, epsilon, 0.5 * (y + x / y))


def make_alpha_dict(text):
    words = text.split()
    chars = [c for c in dict.fromkeys(text) if c.isalpha()]
    return {c: sorted([w for w in words if c in w]) for c in chars}

def flatten(lst):
    return [
        item for sublist in lst 
        for item in (flatten(sublist) if isinstance(sublist, (list, tuple)) else [sublist])
    ]

def group_anagrams(words):
    return {
        "".join(sorted(w)): [word for word in words if "".join(sorted(word)) == "".join(sorted(w))] 
        for w in words
    }


if __name__ == "__main__":
    print("--- Testy Zadania 1 ---")

    # a. liczba (suma nieparzystych)
    assert liczba([1, 0, 5]) == 6
    print(f"\n1a. liczba([1, 0, 5]): {liczba([1, 0, 5])}")  # Wynik: 6
    assert liczba([]) == 0
    print(f"1a. Skrajny (pusta lista): {liczba([])}")    # Wynik: 0
    print("test zadania 1a zakończony.")

    # b. median (mediana)
    assert median([1, 1, 19, 2, 3, 4, 4, 5, 1]) == 3
    print(f"\n1b. median([1,1,19,2,3,4,4,5,1]): {median([1,1,19,2,3,4,4,5,1])}") # Wynik: 3
    assert median([-5, -10, -1]) == -5
    print(f"1b. Skrajny (ujemne): {median([-5, -10, -1])}") # Wynik: -5
    print("test zadania 1b zakończony.")

    # c. pierwiastek (metoda Newtona)
    assert pierwiastek(3, 0.1) == 1.75
    print(f"\n1c. pierwiastek(3, 0.1): {pierwiastek(3, 0.1)}") # Wynik: 1.75
    assert pierwiastek(0, 0.001) == 0.03125
    print(f"1c. Skrajny (zero): {pierwiastek(0, 0.001)}")   # Wynik: bliski 0
    print("test zadania 1c zakończony.")

    # d. make_alpha_dict (słownik znaków)
    # Wynik: {'o': ['on', 'ona'], 'n': ['on', 'ona'], 'i': ['i'], 'a': ['ona']}
    assert make_alpha_dict('on i ona') == {'o': ['on', 'ona'], 'n': ['on', 'ona'], 'i': ['i'], 'a': ['ona']}
    print(f"\n1d. make_alpha_dict('on i ona'): {make_alpha_dict('on i ona')}")
    assert make_alpha_dict('') == {}
    print(f"1d. Skrajny (pusty ciąg): {make_alpha_dict('')}") # Wynik: {}
    print("test zadania 1d zakończony.")

    # e. flatten (spłaszczanie list)
    # Wynik: [1, 2, 3, 4, 5, 6]
    assert flatten([1, [2, 3], [[4, 5], 6]]) == [1, 2, 3, 4, 5, 6]
    print(f"\n1e. flatten([1, [2, 3], [[4, 5], 6]]): {flatten([1, [2, 3], [[4, 5], 6]])}")
    assert flatten([]) == []
    print(f"1e. Skrajny (pusta lista): {flatten([])}") # Wynik: []
    print("test zadania 1e zakończony.")

    # f. group_anagrams (grupowanie anagramów)
    # Wynik: {'kot': ['kot', 'tok'], 'eips': ['pies'], 'ekp': ['kep', 'pek']}
    test_words = ["kot", "tok", "pies", "kep", "pek"]
    assert group_anagrams(test_words) == {'kot': ['kot', 'tok'], 'eips': ['pies'], 'ekp': ['kep', 'pek']}
    print(f"\n1f. group_anagrams: {group_anagrams(test_words)}")
    assert group_anagrams([]) == {}
    print(f"1f. Skrajny (pusta lista): {group_anagrams([])}") # Wynik: {}
    print("test zadania 1f zakończony.")