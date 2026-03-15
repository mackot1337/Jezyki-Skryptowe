import sys
import io

def findFirstComplexSentence():
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    current = ""

    while True:
        char = sys.stdin.read(1)
        if not char:
            # Sprawdzamy ostatnie zdanie, jeżeli plik nie kończy się kropką
            if current.strip() != "" and current.count(",") > 1:
                return current.strip()
            break

        current += char

        # Jeżeli trafimy na koniec zdania
        if char in ".?!":
            if current.count(",") > 1:
                return current.strip()
            current = ""

    return ""

if __name__ == "__main__":
    try:
        # Przekazujemy strumień wejściowy do funkcji
        result = findFirstComplexSentence()

        if result:
            # Wypisujemy wynik na standardowe wyjście
            sys.stdout.write(result + "\n")
        else:
            sys.stdout.write("No complex sentence found.\n")
    except Exception as e:
        sys.stderr.write(f"Wystąpił błąd: {e}\n")