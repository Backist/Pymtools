from __future__ import print_function
from timeit import Timer

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


# tests_simple_1 = {
#     "colorama":   'Fore.LIGHTBLUE_EX+"ghoASDASD"+Style.RESET_ALL',
# }
# run_tests("Benchmark 1", tests_simple_1)