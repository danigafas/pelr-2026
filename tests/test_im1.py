from pelr.algorithms.im1 import ts_pos, calcular_ts, con_k_sufijos, interseccion, con_levine, ejecutar_im1, calcular_umbral_miclet, ejecutar_miclet
from pelr.algorithms.prefix_tree import generar_arbol_prefijos
from pelr.core.state import State
import pytest
from sys import float_info

def test_ts_pos_k1():
    ap = generar_arbol_prefijos(["ab", "ac", "aab"])
    estado_a = ap.obtener_estado(1)
    assert ts_pos(ap, estado_a, 1) == ["b", "c"]

def test_ts_pos_estado_final():
    ap = generar_arbol_prefijos(["ab", "ac", "aab"])
    estado_ab = ap.obtener_estado(2)
    assert ts_pos(ap, estado_ab, 1) == ["%"]

def test_ts_pos_k2():
    arbol = generar_arbol_prefijos(["ab", "ac", "aab"])
    estado_a = arbol.obtener_estado(1)
    resultado = ts_pos(arbol, estado_a, 2)
    assert set(resultado) == {"ab", "b", "c"}

def test_ts_pos_k0():
    arbol = generar_arbol_prefijos(["ab", "ac", "aab"])
    estado_a = arbol.obtener_estado(1)
    estado_ab = arbol.obtener_estado(2)
    assert ts_pos(arbol, estado_a, 0) == []
    assert ts_pos(arbol, estado_ab, 0) == ["%"]

def test_ts_pos_k3():
    arbol = generar_arbol_prefijos(["ab", "ac", "aab"])
    raiz = arbol.obtener_estado(0)
    resultado = ts_pos(arbol, raiz, 3)
    assert set(resultado) == {"ab", "ac", "aab"}

def test_calcular_ts_k1():
    arbol = generar_arbol_prefijos(["ab", "ac", "aab"])
    resultado = calcular_ts(arbol, 1)
    assert resultado == [
        [],
        ["b", "c"],
        ["%"],
        ["%"],
        ["b"],
        ["%"],
    ]

def test_con_k_sufijos_iguales():
    arbol = generar_arbol_prefijos(["ab", "ac", "aab"])
    valores_t = calcular_ts(arbol, 1)
    # ab (índice 2) y ac (índice 3)
    assert con_k_sufijos(valores_t, 2, 3) is True

def test_con_k_sufijos_distintos():
    arbol = generar_arbol_prefijos(["ab", "ac", "aab"])
    valores_t = calcular_ts(arbol, 1)
    # a (índice 1) y aa (índice 4)
    assert con_k_sufijos(valores_t, 1, 4) is False

def test_interseccion():
    assert interseccion(["a", "b", "c"], ["b", "c", "d"]) == ["b", "c"]

def test_interseccion_duplicados():
    assert interseccion(["a", "b", "b"], ["b"]) == ["b", "b"]

def test_con_levine_umbral_superado():
    arbol = generar_arbol_prefijos(["ab", "ac", "aab"])
    # Estados a (1) y aa (4).
    assert con_levine(arbol, 1, 4, 0.6) is True

def test_con_levine_umbral_no_superado():
    arbol = generar_arbol_prefijos(["ab", "ac", "aab"])
    assert con_levine(arbol, 1, 4, 0.8) is False

def test_im1_agrupacion_k_sufijos():
    arbol = generar_arbol_prefijos(["ab", "ac", "aab"])
    resultado = ejecutar_im1(
        arbol,
        algoritmo=0,
        orden=1,
        umbral=0.0
    )
    grupos = {
        frozenset(estado.get_nombre_estado())
        for estado in resultado.get_vector_estados()
    }
    assert grupos == {
        frozenset(["%"]),
        frozenset(["a"]),
        frozenset(["ab", "ac", "aab"]),
        frozenset(["aa"]),
    }
    assert arbol.obtener_numero_estados() == 6

def test_im1_reconstruye_transiciones_sin_duplicados():
    arbol = generar_arbol_prefijos(["ab", "cb"])
    resultado = ejecutar_im1(
        arbol,
        algoritmo=0,
        orden=1,
        umbral=0.0
    )
    assert resultado.obtener_numero_estados() == 3
    origen = resultado.buscar_estado(State("a"))
    assert origen == resultado.buscar_estado(State("c"))
    indice_b = resultado.get_simbolos().index("b")
    destinos = resultado.get_transicion(origen, indice_b)
    assert len(destinos) == 1
    assert set(destinos[0].get_nombre_estado()) == {"ab", "cb"}

def test_im1_completo_k_sufijos():
    arbol = generar_arbol_prefijos(["ab", "ac", "aab"])
    resultado = ejecutar_im1(arbol, 0, 1, 0.0)
    assert resultado.obtener_numero_estados() == 4
    raiz = resultado.buscar_estado(State("%"))
    a = resultado.buscar_estado(State("a"))
    aa = resultado.buscar_estado(State("aa"))
    finales = resultado.buscar_estado(State("ab"))
    assert a != aa
    assert finales == resultado.buscar_estado(State("ac"))
    assert finales == resultado.buscar_estado(State("aab"))
    def comprobar_transicion(origen, simbolo, destino):
        indice_simbolo = resultado.get_simbolos().index(simbolo)
        destinos = resultado.get_transicion(origen, indice_simbolo)
        assert len(destinos) == 1
        assert destinos[0].compara_estado(
            resultado.obtener_estado(destino)
        )
    comprobar_transicion(raiz, "a", a)
    comprobar_transicion(a, "a", aa)
    comprobar_transicion(a, "b", finales)
    comprobar_transicion(a, "c", finales)
    comprobar_transicion(aa, "b", finales)
    assert arbol.obtener_numero_estados() == 6

def test_im1_levine_miclet_mismo_umbral():
    arbol = generar_arbol_prefijos(["ab", "ac", "aab"])
    levine = ejecutar_im1(arbol, 1, 1, 0.8)
    miclet = ejecutar_im1(arbol, 2, 1, 0.8)
    grupos_levine = [
        estado.get_nombre_estado()
        for estado in levine.get_vector_estados()
    ]
    grupos_miclet = [
        estado.get_nombre_estado()
        for estado in miclet.get_vector_estados()
    ]
    assert grupos_levine == grupos_miclet

def test_ts_pos_no_incluye_prefijos_no_finales():
    arbol = generar_arbol_prefijos(["aa", "baaa"])
    raiz = arbol.obtener_estado(0)
    assert set(ts_pos(arbol, raiz, 3)) == {"aa"}

def test_ts_pos_incluye_cadena_larga_con_k4():
    arbol = generar_arbol_prefijos(["aa", "baaa"])
    raiz = arbol.obtener_estado(0)
    assert set(ts_pos(arbol, raiz, 4)) == {"aa", "baaa"}

def test_miclet_calcula_umbral():
    arbol = generar_arbol_prefijos(["ab", "ac", "aab"])
    umbral = calcular_umbral_miclet(arbol)
    assert umbral == pytest.approx(0.4)

def test_miclet_sin_similitudes_positivas():
    arbol = generar_arbol_prefijos(["a"])
    umbral = calcular_umbral_miclet(arbol)
    assert umbral == float_info.max

def test_miclet_ejecucion_completa():
    arbol = generar_arbol_prefijos(["ab", "ac", "aab"])
    resultado = ejecutar_miclet(arbol)
    grupos = {
        frozenset(estado.get_nombre_estado())
        for estado in resultado.get_vector_estados()
    }
    assert grupos == {
        frozenset(["%", "a", "aa"]),
        frozenset(["ab", "ac", "aab"]),
    }

def test_im1_evitar_autofusion():
    arbol = generar_arbol_prefijos(["aaa", "aa", "a"])
    resultado = ejecutar_im1(
        arbol,
        algoritmo=0,
        orden=2,
        umbral=0.0
    )
    assert resultado.obtener_numero_estados() > 0