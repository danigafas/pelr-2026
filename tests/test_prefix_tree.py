from pelr.algorithms.prefix_tree import generar_arbol_prefijos

def test_generar_ap_cadena_simple():
    ap = generar_arbol_prefijos(["ab"])
    estados = [
        (e.get_estado(0), e.get_tipo_estado())
        for e in ap.get_vector_estados()
    ]
    assert estados == [
        ("%", "INICIAL"),
        ("a", "INTERMEDIO"),
        ("ab", "FINAL"),
    ]
    assert ap.get_simbolos() == ["a", "b"]
    assert ap.get_transicion(0, 0)[0].get_estado(0) == "a"
    assert ap.get_transicion(1, 1)[0].get_estado(0) == "ab"

def test_generar_ap_dos_cadenas():
    ap = generar_arbol_prefijos(["ab", "ac"])
    nombres = [
        e.get_estado(0) for e in ap.get_vector_estados()
    ]
    assert nombres == ["%", "a", "ab", "ac"]
    assert ap.get_simbolos() == ["a", "b", "c"]
    assert ap.get_transicion(1, 1)[0].get_estado(0) == "ab"
    assert ap.get_transicion(1, 2)[0].get_estado(0) == "ac"

def test_generar_ap_prefijo_final():
    ap = generar_arbol_prefijos(["a", "ab"])
    assert ap.obtener_estado(1).get_tipo_estado() == "FINAL"
    assert ap.obtener_estado(2).get_tipo_estado() == "FINAL"

def test_generar_ap_cadena_vacia():
    ap = generar_arbol_prefijos(["%", "a"])
    assert ap.obtener_estado(0).get_tipo_estado() == "INICIAL/FINAL"
    assert ap.get_simbolos() == ["a"]

def test_generar_ap_simbolos_repetidos():
    ap = generar_arbol_prefijos(["ab", "ac", "aab"])
    nombres = [
        estado.get_estado(0)
        for estado in ap.get_vector_estados()
    ]
    assert nombres == ["%", "a", "ab", "ac", "aa", "aab"]
    assert ap.get_simbolos() == ["a", "b", "c"]
    # Transición de 'a' hacia 'aa' leyendo 'a'.
    indice_a = ap.obtener_indice_estado(State("a"))
    indice_aa = ap.obtener_indice_estado(State("aa"))
    simbolo_a = ap.get_simbolos().index("a")
    assert indice_a != indice_aa
    destino = ap.get_transicion(indice_a, simbolo_a)[0]
    assert destino.get_estado(0) == "aa"
    # Y desde 'aa' llegamos a 'aab' leyendo 'b'.
    simbolo_b = ap.get_simbolos().index("b")
    destino = ap.get_transicion(indice_aa, simbolo_b)[0]
    assert destino.get_estado(0) == "aab"

from pelr.core.state import State
from pelr.algorithms.prefix_tree import generar_arbol_prefijos


def test_arbol_prefijos_aab():
    muestra = ["ab", "ac", "aab"]
    ap = generar_arbol_prefijos(muestra)
    nombres = [
        estado.get_estado(0)
        for estado in ap.get_vector_estados()
    ]
    assert nombres == ["%", "a", "ab", "ac", "aa", "aab"]
    assert ap.get_simbolos() == ["a", "b", "c"]
    assert ap.get_alf_entrada() == ["%", "ab", "ac", "aab"]
    # La función no modifica la muestra recibida.
    assert muestra == ["ab", "ac", "aab"]
    # Comprobamos las transiciones del árbol.
    transiciones = {
        ("%", "a"): "a",
        ("a", "a"): "aa",
        ("a", "b"): "ab",
        ("a", "c"): "ac",
        ("aa", "b"): "aab",
    }
    for (origen, simbolo), destino_esperado in transiciones.items():
        indice_estado = ap.obtener_indice_estado(State(origen))
        indice_simbolo = ap.get_simbolos().index(simbolo)
        destinos = ap.get_transicion(indice_estado, indice_simbolo)
        assert len(destinos) == 1
        assert destinos[0].get_estado(0) == destino_esperado