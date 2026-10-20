import pytest

from benchmarks.benchmark_inference import generar_muestra
from pelr.algorithms.prefix_tree import generar_arbol_prefijos
from pelr.algorithms.im1 import ts_pos


@pytest.mark.parametrize(
    "cantidad,longitud,semilla",
    [
        (5, 4, 7),
        (8, 6, 2026),
        (8, 6, 42),
    ]
)
def test_cache_ts_pos(cantidad, longitud, semilla):
    muestra = generar_muestra(cantidad, longitud, semilla)
    automata = generar_arbol_prefijos(muestra)

    cache = {}

    for estado in automata.get_vector_estados():
        for orden in range(longitud + 1):
            sin_cache_compartida = ts_pos(
                automata, estado, orden
            )

            con_cache_compartida = ts_pos(
                automata, estado, orden, cache
            )

            assert sin_cache_compartida == con_cache_compartida