from pelr.algorithms.prefix_tree import generar_arbol_prefijos
from pelr.algorithms.kc import ejecutar_kc
from pelr.algorithms.kc_negative import comprueba_muestra_negativa, ejecutar_kc_con_negativos
from pelr.core.automaton import Automaton
from pelr.core.state import State

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

def test_muestra_negativa_explora_todos_los_destinos():
    automata = Automaton()
    automata.put_simbolos(["a"])
    automata.add_estado(State("%", "INICIAL"))
    automata.add_estado(State("q1", "INTERMEDIO"))
    automata.add_estado(State("q2", "FINAL"))
    automata.add_transicion(0, 0, automata.obtener_estado(1))
    automata.add_transicion(0, 0, automata.obtener_estado(2))
    assert comprueba_muestra_negativa(automata, ["a"]) is True