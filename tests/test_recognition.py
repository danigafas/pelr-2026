from pelr.core.automaton import Automaton
from pelr.core.state import State
from pelr.core.recognition import acepta_cadena
from pelr.algorithms.prefix_tree import generar_arbol_prefijos
from pelr.algorithms.kc import ejecutar_kc
from pelr.algorithms.im1 import ejecutar_im1


def test_acepta_cadena_explora_todos_los_destinos():
    automata = Automaton()
    automata.put_simbolos(["a"])
    automata.add_estado(State("%", "INICIAL"))
    automata.add_estado(State("q1", "INTERMEDIO"))
    automata.add_estado(State("q2", "FINAL"))
    automata.add_transicion(0, 0, automata.obtener_estado(1))
    automata.add_transicion(0, 0, automata.obtener_estado(2))
    assert acepta_cadena(automata, "a") is True
    assert acepta_cadena(automata, "aa") is False

def test_inferencia_conserva_muestra_positiva():
    muestra = ["aaa", "aa", "a"]
    arbol = generar_arbol_prefijos(muestra)
    resultados = [
        ejecutar_kc(arbol, 2),
        ejecutar_im1(arbol, 0, 2, 0.0)
    ]
    for resultado in resultados:
        for cadena in muestra:
            assert acepta_cadena(resultado, cadena), (
                f"No se reconoce la cadena positiva {cadena!r}"
            )