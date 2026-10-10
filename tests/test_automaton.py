from pelr.core.automaton import Automaton
from pelr.core.state import State
import pytest


def test_automaton_default_constructor():
    automata = Automaton()
    assert automata.v_estados == []
    assert automata.alfabeto_entrada == []
    assert automata.alfabeto_salida == []
    assert automata.delta == []
    assert automata.tipo == ""
    assert automata.f_salida == []
    assert automata.simbolos == []

def test_automaton_independent_instances():
    a1 = Automaton()
    a2 = Automaton()
    a1.v_estados.append(State("q0"))
    assert len(a1.v_estados) == 1
    assert len(a2.v_estados) == 0

def test_automaton_four_arguments():
    estados = [State("q0")]
    alfabeto = ["a", "b"]
    delta = []
    simbolos = ["a", "b"]
    automata = Automaton(estados, alfabeto, delta, simbolos)
    assert len(automata.v_estados) == 1
    assert automata.alfabeto_entrada == ["a", "b"]
    assert automata.delta == []
    assert automata.simbolos == ["a", "b"]

def test_automaton_copy_constructor():
    original = Automaton()
    original.v_estados.append(State("q0"))
    original.tipo = "AFD"
    copia = Automaton(original)
    assert len(copia.v_estados) == 1
    assert copia.v_estados is not original.v_estados
    assert copia.v_estados[0] is original.v_estados[0]
    assert copia.tipo is None

def test_automaton_four_arguments_uninitialized_attributes():
    automata = Automaton([], [], [], [])
    assert automata.alfabeto_salida is None
    assert automata.f_salida is None
    assert automata.tipo is None

def test_get_vector_estados_returns_reference():
    automata = Automaton()
    estados = automata.get_vector_estados()
    estados.append(State("q0"))
    assert len(automata.v_estados) == 1
    assert estados is automata.v_estados

def test_put_vector_estados_copies_list():
    automata = Automaton()
    estados = [State("q0")]
    automata.put_vector_estados(estados)
    estados.append(State("q1"))
    assert len(automata.v_estados) == 1

def test_put_vector_estados_shallow_copy():
    automata = Automaton()
    estado = State("q0")
    automata.put_vector_estados([estado])
    assert automata.v_estados[0] is estado

def test_buscar_estado_en_grupo():
    automata = Automaton()
    automata.v_estados = [
        State(["q0", "q1"], "FINAL"),
        State(["q2", "q3"], "INTERMEDIO")
    ]
    assert automata.buscar_estado(State("q3")) == 1

def test_buscar_estado_inexistente():
    automata = Automaton()
    automata.v_estados = [
        State(["q0", "q1"], "FINAL"),
        State(["q2"], "INTERMEDIO")
    ]
    assert automata.buscar_estado(State("q9")) == -1

def test_buscar_estado_primera_coincidencia():
    automata = Automaton()
    automata.v_estados = [
        State(["q0", "q1"]),
        State(["q1", "q2"])
    ]
    assert automata.buscar_estado(State("q1")) == 0

def test_add_estado():
    automata = Automaton()
    estado = State("q0", "INICIAL")
    resultado = automata.add_estado(estado)
    assert resultado is True
    assert len(automata.v_estados) == 1
    assert automata.v_estados[0] is estado

def test_add_estado_duplicado():
    automata = Automaton()
    automata.add_estado(State("q0"))
    resultado = automata.add_estado(State("q0"))
    assert resultado is False
    assert len(automata.v_estados) == 1

def test_add_estado_ya_agrupado():
    automata = Automaton()
    automata.add_estado(State(["q0", "q1"]))
    resultado = automata.add_estado(State("q1"))
    assert resultado is False
    assert len(automata.v_estados) == 1

def test_obtener_indice_estado():
    automata = Automaton()
    automata.add_estado(State(["q0", "q1"], "FINAL"))
    automata.add_estado(State(["q2", "q3"], "INTERMEDIO"))
    indice = automata.obtener_indice_estado(
        State(["q2", "q3"], "FINAL")
    )
    assert indice == 1

def test_obtener_indice_estado_parcial():
    automata = Automaton()
    automata.add_estado(State(["q0", "q1"]))
    assert automata.obtener_indice_estado(State("q1")) == -1

def test_obtener_indice_estado_orden():
    automata = Automaton()
    automata.add_estado(State(["q0", "q1"]))
    assert automata.obtener_indice_estado(
        State(["q1", "q0"])
    ) == -1

def test_del_estado():
    automata = Automaton()
    automata.add_estado(State("q0"))
    automata.add_estado(State("q1"))
    automata.add_estado(State("q2"))
    automata.del_estado(State("q1"))
    assert len(automata.v_estados) == 2
    assert automata.v_estados[0].nombres == ["q0"]
    assert automata.v_estados[1].nombres == ["q2"]

def test_del_estado_parcial():
    automata = Automaton()
    automata.add_estado(State(["q0", "q1"]))
    automata.del_estado(State("q1"))
    assert len(automata.v_estados) == 1
    assert automata.v_estados[0].nombres == ["q0", "q1"]

def test_del_estado_inexistente():
    automata = Automaton()
    automata.add_estado(State("q0"))
    resultado = automata.del_estado(State("q9"))
    assert resultado is None
    assert len(automata.v_estados) == 1

def test_obtener_estado():
    automata = Automaton()
    estado = State("q0", "INICIAL")
    automata.add_estado(estado)
    assert automata.obtener_estado(0) is estado

def test_obtener_estado_indice_negativo():
    automata = Automaton()
    automata.add_estado(State("q0"))
    with pytest.raises(IndexError):
        automata.obtener_estado(-1)

def test_obtener_estado_fuera_de_rango():
    automata = Automaton()
    automata.add_estado(State("q0"))
    with pytest.raises(IndexError):
        automata.obtener_estado(5)

def test_obtener_numero_estados():
    automata = Automaton()
    assert automata.obtener_numero_estados() == 0
    automata.add_estado(State(["q0", "q1"]))
    automata.add_estado(State(["q2", "q3"]))
    assert automata.obtener_numero_estados() == 2

def test_get_simbolos():
    automata = Automaton()
    automata.simbolos = ["a", "b"]
    assert automata.get_simbolos() == ["a", "b"]

def test_get_simbolos_referencia():
    automata = Automaton()
    automata.simbolos = ["a"]
    simbolos = automata.get_simbolos()
    simbolos.append("b")
    assert automata.simbolos == ["a", "b"]

def test_put_simbolos_copia():
    automata = Automaton()
    simbolos = ["a", "b"]
    automata.put_simbolos(simbolos)
    simbolos.append("c")
    assert automata.get_simbolos() == ["a", "b"]

def test_add_simbolo():
    automata = Automaton()
    automata.add_simbolo("a")
    automata.add_simbolo("b")
    assert automata.simbolos == ["a", "b"]

def test_add_simbolo_duplicado():
    automata = Automaton()
    automata.add_simbolo("a")
    automata.add_simbolo("a")
    assert automata.simbolos == ["a"]

def test_del_simbolo():
    automata = Automaton()
    automata.put_simbolos(["a", "b", "c"])
    automata.del_simbolo("b")
    assert automata.simbolos == ["a", "c"]

def test_del_simbolo_inexistente():
    automata = Automaton()
    automata.put_simbolos(["a", "b"])
    resultado = automata.del_simbolo("z")
    assert resultado is None
    assert automata.simbolos == ["a", "b"]

def test_del_simbolo_no_elimina_coincidencias_parciales():
    automata = Automaton()
    automata.put_simbolos(["ab", "a"])
    automata.del_simbolo("a")
    assert automata.simbolos == ["ab"]

def test_del_simbolo_solo_primera_aparicion():
    automata = Automaton()
    automata.put_simbolos(["a", "x", "a"])
    automata.del_simbolo("a")
    assert automata.simbolos == ["x", "a"]

def test_get_delta_referencia():
    automata = Automaton()
    resultado = automata.get_delta()
    assert resultado is automata.delta

def test_put_delta_copia_exterior():
    automata = Automaton()
    transiciones = [[[State("q1")]]]
    automata.put_delta(transiciones)
    assert automata.delta is not transiciones
    transiciones.append([])
    assert len(automata.delta) == 1

def test_put_delta_copia_superficial():
    automata = Automaton()
    transiciones = [[[State("q1")]]]
    automata.put_delta(transiciones)
    transiciones[0].append([State("q2")])
    assert len(automata.delta[0]) == 2

def test_limpia_transiciones():
    automata = Automaton()
    automata.put_delta([[[State("q1")]]])
    automata.limpia_transiciones()
    assert automata.delta == []

def test_limpia_transiciones_mantiene_referencia():
    automata = Automaton()
    automata.put_delta([[[State("q1")]]])
    referencia = automata.get_delta()
    automata.limpia_transiciones()
    assert referencia is automata.delta
    assert referencia == []

def test_add_transicion_basica():
    automata = Automaton()
    destino = State("q1", "FINAL")
    automata.add_transicion(0, 0, destino)
    assert len(automata.delta) == 1
    assert len(automata.delta[0]) == 1
    assert len(automata.delta[0][0]) == 1
    copia = automata.delta[0][0][0]
    assert copia.nombres == ["q1"]
    assert copia is not destino

def test_add_transicion_indices_altos():
    automata = Automaton()
    automata.add_transicion(2, 1, State("q3"))
    assert len(automata.delta) == 3
    assert automata.delta[0] is None
    assert automata.delta[1] is None
    assert automata.delta[2][0] is None
    assert automata.delta[2][1][0].nombres == ["q3"]

def test_add_transicion_varios_destinos():
    automata = Automaton()
    automata.add_transicion(0, 0, State("q1"))
    automata.add_transicion(0, 0, State("q2"))
    destinos = automata.delta[0][0]
    assert len(destinos) == 2
    assert destinos[0].nombres == ["q1"]
    assert destinos[1].nombres == ["q2"]

def test_add_transicion_destinos_equivalentes():
    automata = Automaton()
    destino = State("q1")
    automata.add_transicion(0, 0, destino)
    automata.add_transicion(0, 0, destino)
    destinos = automata.delta[0][0]
    assert len(destinos) == 2
    assert destinos[0].compara_estado(destinos[1])
    assert destinos[0] is not destinos[1]

def test_add_transicion_misma_instancia_almacenada():
    automata = Automaton()
    automata.add_transicion(0, 0, State("q1"))
    destino = automata.delta[0][0][0]
    automata.add_transicion(0, 0, destino)
    assert len(automata.delta[0][0]) == 1