from pelr.core.state import State
from pelr.core.automaton import Automaton


def generar_arbol_prefijos(muestra_positiva: list[str]) -> Automaton:
    """Genera el árbol de prefijos a partir de una muestra positiva."""
    muestra = muestra_positiva.copy()
    prefijos = []
    simbolos = []
    lamda_original = "%" in muestra

    if "%" not in muestra:
        muestra.insert(0, "%")
    for cadena in muestra:
        if len(cadena) == 1:
            prefijos.append(cadena)
            if cadena != "%":
                simbolos.append(cadena)
        else:
            for longitud in range(1, len(cadena) + 1):
                prefijo = cadena[:longitud]
                if prefijo not in prefijos:
                    prefijos.append(prefijo)
            for simbolo in cadena:
                if simbolo not in simbolos:
                    simbolos.append(simbolo)

    for i in range(len(prefijos)):
        for j in range(i, len(prefijos)):
            if len(prefijos[i]) > len(prefijos[j]):
                prefijos[i], prefijos[j] = prefijos[j], prefijos[i]

    estados = []
    for prefijo in prefijos:
        if prefijo == "%":
            if lamda_original:
                estados.append(State([prefijo], "INICIAL/FINAL"))
            else:
                estados.append(State([prefijo], "INICIAL"))
        elif prefijo in muestra:
            estados.append(State([prefijo], "FINAL"))
        else:
            estados.append(State([prefijo], "INTERMEDIO"))

    ap = Automaton()
    ap.put_vector_estados(estados)
    ap.put_alf_entrada(muestra)
    ap.put_simbolos(simbolos)
    ap.limpia_transiciones()

    for i in range(1, ap.obtener_numero_estados()):
        actual = ap.obtener_estado(i).get_estado(0)
        simbolo = actual[-1]
        indice_simbolo = simbolos.index(simbolo)
        if len(actual) == 1:
            ap.add_transicion(0, indice_simbolo, State(actual))

        else:
            origen = actual[:-1]
            indice_origen = ap.obtener_indice_estado(State(origen))
            ap.add_transicion(indice_origen, indice_simbolo, ap.obtener_estado(i))

    return ap