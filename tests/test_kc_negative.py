from pelr.algorithms.prefix_tree import generar_arbol_prefijos
from pelr.algorithms.kc import ejecutar_kc
from pelr.algorithms.kc_negative import comprueba_muestra_negativa, ejecutar_kc_con_negativos

def test_kc_acepta_muestra_negativa():
    arbol = generar_arbol_prefijos(["ab", "aab"])
    resultado = ejecutar_kc(arbol, 1)
    assert comprueba_muestra_negativa(
        resultado, ["aaab"]
    ) is True

def test_kc_rechaza_muestra_negativa():
    arbol = generar_arbol_prefijos(["ab", "aab"])
    resultado = ejecutar_kc(arbol, 2)
    assert comprueba_muestra_negativa(
        resultado, ["aaab"]
    ) is False

def test_kc_muestra_negativa_vacia():
    arbol = generar_arbol_prefijos(["ab"])
    resultado = ejecutar_kc(arbol, 1)
    assert comprueba_muestra_negativa(
        resultado, []
    ) is False

def test_kc_negativos_encuentra_k():
    arbol = generar_arbol_prefijos(["ab", "aab"])
    resultado, k, valido = ejecutar_kc_con_negativos(
        arbol, ["aaab"]
    )
    assert valido is True
    assert k == 2
    assert comprueba_muestra_negativa(resultado, ["aaab"]) is False

def test_kc_negativos_sin_solucion():
    arbol = generar_arbol_prefijos(["a"])
    resultado, k, valido = ejecutar_kc_con_negativos(
        arbol, ["a"]
    )
    assert valido is False
    assert k == 1