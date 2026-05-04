import functools
from ex4 import makeGenerator

def makeGeneratorMem(f):
    memoized = functools.cache(f)
    return makeGenerator(memoized)

if __name__ == "__main__":
    def heavyComputation(n):
        print(f"Obliczam dla n={n}")
        return n * 10

    memGen = makeGeneratorMem(heavyComputation)
    print("Pierwsze wywołanie:", next(memGen))
    print("Drugie wywołanie:", next(memGen))
    print("Trzecie wywołanie:", next(memGen))