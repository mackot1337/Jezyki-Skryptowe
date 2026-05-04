def makeGenerator(f):
    def generator():
        n = 1
        while True:
            yield f(n)
            n += 1
    return generator()

if __name__ == "__main__":

    def fibonacci(n):
        if n <= 2:
            return 1
        return fibonacci(n-1) + fibonacci(n-2)

    # Fibonacci
    fibSeq = makeGenerator(fibonacci)
    print("Fibonacci:", [next(fibSeq) for _ in range(5)])

    # Arytmetyczny
    aritmSeq = makeGenerator(lambda n: 2 + (n - 1) * 3)
    print("Arytmetyczny:", [next(aritmSeq) for _ in range(5)])

    # Geometryczny
    geomSeq = makeGenerator(lambda n: 2 * (3 ** (n - 1)))
    print("Geometryczny:", [next(geomSeq) for _ in range(5)])

    # Potęgowy
    expySeq = makeGenerator(lambda n: n ** 2)
    print("Potęgowy:", [next(expySeq) for _ in range(5)])