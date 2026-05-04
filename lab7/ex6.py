import logging
import time
import functools
import inspect

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

def log(level):
    def decorator(obj):
        if inspect.isclass(obj):
            original_init = obj.__init__

            @functools.wraps(original_init)
            def newInit(self, *args, **kwargs):
                logging.log(level, f"Zainicjowano obiekt klasy {obj.__name__}")
                original_init(self, *args, **kwargs)

            obj.__init__ = newInit
            return obj
        
        else:
            @functools.wraps(obj)
            def wrapper(*args, **kwargs):
                startTime = time.time()
                callTimeStr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(startTime))

                result = obj(*args, **kwargs)

                endTime = time.time()
                duration = endTime - startTime

                logMessage = (
                    f"Czas wywołania: {callTimeStr} | "
                    f"Czas trwania: {duration:.6f}s | "
                    f"Funkcja: {obj.__name__} | "
                    f"Argumenty: args={args}, kwargs={kwargs} | "
                    f"Wartość zwracana: {result}"
                )
                logging.log(level, logMessage)
                return result
            return wrapper
         
    return decorator

if __name__ == "__main__":
    @log(logging.INFO)
    def addWithDelay(a, b):
        time.sleep(0.5)
        return a + b

    print("Wynik funkcji:", addWithDelay(5, 10))

    @log(logging.DEBUG)
    class BazaDanych:
        def __init__(self, dbName):
            self.dbName = dbName

    print("Tworzenie obiektu:")
    baza = BazaDanych("MojaBaza")