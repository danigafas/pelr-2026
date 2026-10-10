from pelr.core.state import State
import pytest

def test_state_default_constructor():
    estado = State()
    assert estado.nombres == []
    assert estado.tipo == "INTERMEDIO"
    assert estado.alfabeto_salida is None

def test_states_have_independent_name_lists():
    q0 = State()
    q1 = State()
    q0.nombres.append("q0")
    assert q0.nombres == ["q0"]
    assert q1.nombres == []

def test_state_constructor_copies_names():
    nombres = ["q0", "q1"]
    estado = State(nombres, "FINAL")
    assert estado.nombres is not nombres
    nombres.append("q2")
    assert estado.nombres == ["q0", "q1"]
    assert estado.tipo == "FINAL"

def test_state_constructor_with_single_name():
    estado = State("q0")
    assert estado.nombres == ["q0"]
    assert estado.tipo is None

def test_state_constructor_with_name_and_type():
    estado = State("q0", "FINAL")
    assert estado.nombres == ["q0"]
    assert estado.tipo == "FINAL"

def test_state_preserves_complete_name():
    estado = State("estado inicial", "INICIAL")
    assert estado.nombres == ["estado inicial"]

def test_state_with_empty_name():
    estado = State("")
    assert estado.nombres == [""]
    assert estado.tipo is None

def test_state_copy_constructor():
    original = State(["q0", "q1"], "FINAL")
    copia = State(original)
    assert copia.nombres == ["q0", "q1"]
    assert copia.tipo == "FINAL"
    assert copia is not original
    assert copia.nombres is not original.nombres

def test_state_copy_independent_names():
    original = State(["q0"], "INICIAL")
    copia = State(original)
    copia.nombres.append("q1")
    assert copia.nombres == ["q0", "q1"]
    assert original.nombres == ["q0"]

def test_get_tipo_estado():
    estado = State("q0", "INICIAL")
    assert estado.get_tipo_estado() == "INICIAL"

def test_get_tipo_estado_sin_definir():
    estado = State("q0")
    assert estado.get_tipo_estado() is None

def test_get_nombre_estado_return_reference():
    estado = State(["q0"], "INICIAL")
    nombres = estado.get_nombre_estado()
    nombres.append("q1")
    assert estado.nombres == ["q0", "q1"]

def test_put_tipo_estado():
    estado = State("q0", "INTERMEDIO")
    estado.put_tipo_estado("FINAL")
    assert estado.tipo == "FINAL"
    assert estado.get_tipo_estado() == "FINAL"

def test_put_nombre_estado():
    estado = State(["q0"], "INICIAL")
    estado.put_nombre_estado(["q1", "q2"])
    assert estado.nombres == ["q1", "q2"]
    assert estado.tipo == "INICIAL"

def test_put_nombre_estado_copies_list():
    estado = State(["q0", "INICIAL"])
    nuevos_nombres = ["q1", "q2"]
    estado.put_nombre_estado(nuevos_nombres)
    assert estado.nombres is not nuevos_nombres
    nuevos_nombres.append("q3")
    assert estado.nombres == ["q1", "q2"]

def test_add_estado():
    estado = State("q0", "INICIAL")
    estado.add_estado("q1", "FINAL")
    assert estado.nombres == ["q0", "q1"]
    assert estado.tipo == "FINAL"

def test_del_estado():
    estado = State(["q0", "q1", "q2"], "FINAL")
    estado.del_estado("q1")
    assert estado.nombres == ["q0", "q2"]
    assert estado.tipo == "FINAL"

def test_del_estado_inexistente():
    estado = State(["q0", "q1"], "INICIAL")
    estado.del_estado("q5")
    assert estado.nombres == ["q0", "q1"]

def test_del_estado_duplicado():
    estado = State(["q0", "q1", "q0"], "FINAL")
    estado.del_estado("q0")
    assert estado.nombres == ["q1", "q0"]

def test_get_num_estados():
    estado = State(["q0", "q1", "q2"], "FINAL")
    assert estado.get_num_estados() == 3

def test_get_num_estados_vacio():
    estado = State()
    assert estado.get_num_estados() == 0

def test_get_indice_estado():
    estado = State(["q0", "q1", "q2"], "INTERMEDIO")
    assert estado.get_indice_estado("q1") == 1

def test_get_indice_estado_inexistente():
    estado = State(["q0", "q1"], "INTERMEDIO")
    assert estado.get_indice_estado("q5") == -1

def test_get_indice_estado_duplicado():
    estado = State(["q0", "q1", "q0"], "INTERMEDIO")
    assert estado.get_indice_estado("q0") == 0

def test_get_estado():
    estado = State(["q0", "q1", "q2"], "FINAL")
    assert estado.get_estado(0) == "q0"
    assert estado.get_estado(1) == "q1"
    assert estado.get_estado(2) == "q2"

def test_get_estado_indice_negativo():
    estado = State(["q0", "q1"], "FINAL")
    with pytest.raises(IndexError):
        estado.get_estado(-1)

def test_get_estado_fuera_de_rango():
    estado = State(["q0", "q1"], "FINAL")
    with pytest.raises(IndexError):
        estado.get_estado(5)

def test_get_estado_vacio():
    estado = State()
    with pytest.raises(IndexError):
        estado.get_estado(0)

def test_compara_estado_iguales():
    q0 = State(["q0", "q1"], "FINAL")
    q1 = State(["q0", "q1"], "INICIAL")
    assert q0.compara_estado(q1) is True

def test_compara_estado_orden_distinto():
    q0 = State(["q0", "q1"], "FINAL")
    q1 = State(["q1", "q0"], "FINAL")
    assert q0.compara_estado(q1) is False

def test_compara_estado_longitud_distinta():
    q0 = State(["q0", "q1"], "FINAL")
    q1 = State(["q0"], "FINAL")
    assert q0.compara_estado(q1) is False

def test_compara_estado_nombres_distintos():
    q0 = State(["q0", "q1"], "FINAL")
    q1 = State(["q0", "q2"], "FINAL")
    assert q0.compara_estado(q1) is False

def test_get_alfabeto_s_default():
    estado = State("q0", "INICIAL")
    assert estado.get_alfabeto_s() is None

def test_put_alfabeto_s():
    estado = State("q0", "INICIAL")
    alfabeto = ["a", "b", "c"]
    estado.put_alfabeto_s(alfabeto)
    assert estado.get_alfabeto_s() == ["a", "b", "c"]
    alfabeto.append("d")
    assert estado.get_alfabeto_s() == ["a", "b", "c"]

def test_get_alfabeto_s_returns_reference():
    estado = State("q0", "INICIAL")
    estado.put_alfabeto_s(["a", "b"])
    alfabeto = estado.get_alfabeto_s()
    alfabeto.append("c")
    assert estado.alfabeto_salida == ["a", "b", "c"]

def test_obtener_numero_estados():
    estado = State(["q0", "q1", "q2"], "FINAL")
    assert estado.obtener_numero_estados() == 3


def test_obtener_numero_estados_vacio():
    estado = State()
    assert estado.obtener_numero_estados() == 0

def test_state_constructor_three_arguments():
    estado = State(["q0", "q1"], "FINAL", ["a", "b"])
    assert estado.nombres == ["q0", "q1"]
    assert estado.tipo == "FINAL"
    assert estado.alfabeto_salida is None

def test_state_constructor_three_arguments_copies_names():
    nombres = ["q0", "q1"]
    estado = State(nombres, "FINAL", ["a", "b"])
    nombres.append("q2")
    assert estado.nombres == ["q0", "q1"]

def test_copy_constructor_does_not_copy_output_alphabet():
    original = State("q0", "FINAL")
    original.put_alfabeto_s(["a", "b"])
    copia = State(original)
    assert copia.get_alfabeto_s() is None
    assert original.get_alfabeto_s() == ["a", "b"]