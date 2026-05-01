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
    # canonical_keys = [dict.fromkeys(["".join(sorted(w)) for w in words])]
    return {
        "".join(sorted(w)): [word for word in words if "".join(sorted(word)) == "".join(sorted(w))] 
        for w in words
    }


if __name__ == "__main__":
    print("--- Testy Zadania 1 ---")

    # a. liczba (suma nieparzystych)
    print(f"1a. liczba([1, 0, 5]): {liczba([1, 0, 5])}")  # Wynik: 6
    print(f"1a. Skrajny (pusta lista): {liczba([])}")    # Wynik: 0

    # b. median (mediana)
    print(f"1b. median([1,1,19,2,3,4,4,5,1]): {median([1,1,19,2,3,4,4,5,1])}") # Wynik: 3
    print(f"1b. Skrajny (ujemne): {median([-5, -10, -1])}") # Wynik: -5

    # c. pierwiastek (metoda Newtona)
    print(f"1c. pierwiastek(3, 0.1): {pierwiastek(3, 0.1)}") # Wynik: 1.75[cite: 3]
    print(f"1c. Skrajny (zero): {pierwiastek(0, 0.001)}")   # Wynik: bliski 0

    # d. make_alpha_dict (słownik znaków)
    # Wynik: {'o': ['on', 'ona'], 'n': ['on', 'ona'], 'i': ['i'], 'a': ['ona']}[cite: 3]
    print(f"1d. make_alpha_dict('on i ona'): {make_alpha_dict('on i ona')}")
    print(f"1d. Skrajny (pusty ciąg): {make_alpha_dict('')}") # Wynik: {}

    # e. flatten (spłaszczanie list)
    # Wynik: [1, 2, 3, 4, 5, 6][cite: 3]
    print(f"1e. flatten([1, [2, 3], [[4, 5], 6]]): {flatten([1, [2, 3], [[4, 5], 6]])}")
    print(f"1e. Skrajny (pusta lista): {flatten([])}") # Wynik: []

    # f. group_anagrams (grupowanie anagramów)
    # Wynik: {'kot': ['kot', 'tok'], 'eips': ['pies'], 'ekp': ['kep', 'pek']}[cite: 3]
    test_words = ["kot", "tok", "pies", "kep", "pek"]
    print(f"1f. group_anagrams: {group_anagrams(test_words)}")
    print(f"1f. Skrajny (pusta lista): {group_anagrams([])}") # Wynik: {}