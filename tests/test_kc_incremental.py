from pelr.algorithms.prefix_tree import generar_arbol_prefijos
from pelr.algorithms.kc import ejecutar_kc
from pelr.algorithms.kc_incremental import ejecutar_kc_incremental
from pelr.core.recognition import acepta_cadena
import pytest

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

def test_incremental_convierte_prefijo_en_final():
    arbol = generar_arbol_prefijos(["ab"])
    automata = ejecutar_kc(arbol, 2)
    resultado = ejecutar_kc_incremental(automata, "a", 2)
    destino = resultado.get_transicion_estrella(0, "a")
    assert destino.get_tipo_estado() == "FINAL"
    assert resultado.obtener_numero_estados() == 3

def test_incremental_anade_rama_larga():
    arbol = generar_arbol_prefijos(["ab"])
    automata = ejecutar_kc(arbol, 2)
    resultado = ejecutar_kc_incremental(
        automata, "acde", 2
    )
    assert acepta_cadena(resultado, "ab")
    assert acepta_cadena(resultado, "acde")
    assert "d" in resultado.get_simbolos()
    assert "e" in resultado.get_simbolos()

def test_incremental_no_modifica_original():
    arbol = generar_arbol_prefijos(["ab"])
    automata = ejecutar_kc(arbol, 2)
    resultado = ejecutar_kc_incremental(
        automata, "ac", 2
    )
    assert acepta_cadena(resultado, "ac")
    assert not acepta_cadena(automata, "ac")
    assert "c" not in automata.get_simbolos()

def test_incremental_acepta_cadena_vacia():
    arbol = generar_arbol_prefijos(["ab"])
    automata = ejecutar_kc(arbol, 2)
    resultado = ejecutar_kc_incremental(
        automata, "%", 2
    )
    assert acepta_cadena(resultado, "%")
    assert acepta_cadena(resultado, "ab")

def test_incremental_dos_incorporaciones_consecutivas():
    arbol = generar_arbol_prefijos(["ab"])
    inicial = ejecutar_kc(arbol, 2)
    # Primera incorporación.
    primero = ejecutar_kc_incremental(inicial, "ac", 2)
    # Segunda incorporación sobre el resultado anterior.
    segundo = ejecutar_kc_incremental(primero, "acd", 2)
    # Debe conservar las tres cadenas positivas.
    for cadena in ["ab", "ac", "acd"]:
        assert acepta_cadena(segundo, cadena)
    # El primer resultado no debe modificarse.
    assert acepta_cadena(primero, "ac")
    assert not acepta_cadena(primero, "acd")
    # Tampoco el autómata inicial.
    assert acepta_cadena(inicial, "ab")
    assert not acepta_cadena(inicial, "ac")