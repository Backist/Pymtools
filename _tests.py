from __future__ import print_function
from timeit import Timer
import time as t 

import misctools.misc as mtm
import misctools.netfuncs as ntm
import misctools.sysfuncs as sfm
import misctools.colorfuncs as ctm
import misctools.exports as exm
import misctools.ext as extm



def benchmark(stmt, n=1000, r=3, setup: str = 'from colorama import Style, Fore, Back;'):
    setup = (
        'from colorama import Style, Fore, Back;'
    )
    timer = Timer(stmt, setup=setup)
    best = min(timer.repeat(r, n))

    usec = best * 1e6 / n
    #* Retorna el mejor tiempo en indice 0 y los 5 primeros e indice 1
    return usec

def run_tests(title, tests):
    print(title)
    results = sorted((benchmark(v), k) for k, v in tests.items())
    print(results)
    for usec, name in results:
        print(f'\t{name:<12} {usec:01.4f} μs')
        print("\tConvertion: 1 μs = 0.001 ms = 0.00001 s = 0.000001 s = 0.000000001 s")
        print()





#TODO /////////////////////// BENCHMARKS ///////////////////////

b = t.time()
testr = """Esto es una pequeña prueba.

    Cabezera 1:
        - Ejemplo 1 -> Esto es una breve explicacion de lo que puede llegar a contener este ejemplo.
        - Ejemplo 2 -> Esto es una breve explicacion de lo que puede llegar a contener este ejemplo.
        - Ejemplo 3 -> Esto es una breve explicacion de lo que puede llegar a contener este ejemplo.
        - Ejemplo 4 -> Esto es una breve explicacion de lo que puede llegar a contener este ejemplo.
        Sub-cabecera 1:
            - Ejemplo 1.1 -> Estos son algunos ejemplos de la Sub-cabezera 1.
            - Ejemplo 2.1 -> Estos son algunos ejemplos de la Sub-cabezera 1.
            - Ejemplo 3.1 -> Estos son algunos ejemplos de la Sub-cabezera 1.
            - Ejemplo 4.1 -> Estos son algunos ejemplos de la Sub-cabezera 1.
            Sub-sub-cabezera 1 -> Sin embargo, en la sub-sub-cabecera 1 tenemos algunos ejemplos de demostracion con aproxiamadamente 3 tabulaciones
                - Ejemplo 1.1.1 -> Esto es una breve explicacion de lo que puede llegar a contener este ejemplo.
                - Ejemplo 2.1.1 -> Esto es una breve explicacion de lo que puede llegar a contener este ejemplo.
                - Ejemplo 3.1.1 -> Esto es una breve explicacion de lo que puede llegar a contener este ejemplo.
                - Ejemplo 4.1.1 -> Esto es una breve explicacion de lo que puede llegar a contener este ejemplo.
    Cabezera 2:
        - Ejemplo 1 -> Esto serian algunos ejemplos mas importantes puesto que estan en la segunda cabezera, y, por tanto, segundo elemento principal de esta string.
        - Ejemplo 2 -> Esto serian algunos ejemplos mas importantes puesto que estan en la segunda cabezera, y, por tanto, segundo elemento principal de esta string.
        - Ejemplo 3 -> Esto serian algunos ejemplos mas importantes puesto que estan en la segunda cabezera, y, por tanto, segundo elemento principal de esta string.
        - Ejemplo 4 -> Esto serian algunos ejemplos mas importantes puesto que estan en la segunda cabezera, y, por tanto, segundo elemento principal de esta string.
    -------------------------------------------------------------
    Despedida y finalizacion del texto/docstring:

    Como modo de prueba y finalizacion del texto/docstring,
    Backest.
    """ 

w = {
    "a": "asd",
    "b": {
        "c": "asd",
        "d": {
            "e": "asd",
            "f": "asd",
            "g": "asd",
        },
        "h": {
            ("i", "j", "k"): "asd",
            "l": "asd",
            "m": "asd",
        },
        "n": ({
            "o": "asd",
            "p": "asd",
            "q": "asd",

        }, "asd", "asd", "asd"
        ),
        "r": "asd",
    },
    "c": "asd",
    "d": "asd",
    "e": "asd",
    "f": "asd",
    "g": "asd",
    "h": "asd",
    "i": ({})
}

e = mtm.cFormatter(
    testr,
    color="LIGHTBLUE_EX", 
    iter_colors= ["GREEN", "BLUE", "YELLOW", "CYAN"],
    forline=True
)

h = ctm.randomHex(True)
r = ctm.randomRgb(True)
l = ctm.randomHsl(True)
v = ctm.randomHsv(True)
a = ctm.rgb2hex(r)
print(a)
print(h)
print(r)
print(l)
print(v)
print(mtm.sortByType([23, ("asd", "Asd"), 1, 435, "Asd"], [str, int]))