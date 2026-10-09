from pelr.core.state import State

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