from pelr.algorithms.prefix_tree import generar_arbol_prefijos
from pelr.algorithms.kc import ejecutar_kc
from pelr.algorithms.kc_incremental import ejecutar_kc_incremental
import pytest

@pytest.mark.xfail(
    raises=NotImplementedError,
    reason="KC incremental pendiente",
    strict=True
)

def test_incremental_anade_cadena_nueva():
    arbol = generar_arbol_prefijos(["ab"])
    automata = ejecutar_kc(arbol, 2)
    resultado = ejecutar_kc_incremental(automata, "ac", 2)
    assert resultado.obtener_numero_estados() == 4
    assert "c" in resultado.get_simbolos()
    destino = resultado.get_transicion_estrella(0, "ac")
    assert destino.get_tipo_estado() == "FINAL"
    destino = resultado.get_transicion_estrella(0, "ab")
    assert destino.get_tipo_estado() == "FINAL"

@pytest.mark.xfail(
    raises=NotImplementedError,
    reason="KC incremental pendiente",
    strict=True
)

def test_incremental_convierte_prefijo_en_final():
    arbol = generar_arbol_prefijos(["ab"])
    automata = ejecutar_kc(arbol, 2)
    resultado = ejecutar_kc_incremental(automata, "a", 2)
    destino = resultado.get_transicion_estrella(0, "a")
    assert destino.get_tipo_estado() == "FINAL"
    assert resultado.obtener_numero_estados() == 3
