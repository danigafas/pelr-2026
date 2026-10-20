from copy import deepcopy

from pelr.core.automaton import Automaton
from pelr.core.state import State
from pelr.algorithms.kc import ejecutar_kc


def ejecutar_kc_incremental(
    automata: Automaton,
    cadena: str,
    k: int
) -> Automaton:
    """Incorpora una cadena y vuelve a ejecutar KC."""
    if k < 0:
        raise ValueError("K no puede ser negativo")
    if automata.obtener_numero_estados() == 0:
        raise ValueError("El autómata no contiene estados")
    # Trabajar sobre una copia independiente.
    trabajo = deepcopy(automata)
    if cadena in ("", "%"):
        inicial = trabajo.obtener_estado(0)
        inicial.put_tipo_estado("INICIAL/FINAL")
    else:
        actual = 0
        prefijo = ""
        for posicion, simbolo in enumerate(cadena):
            prefijo += simbolo
            # Incorporar símbolos nuevos.
            simbolos = trabajo.get_simbolos()
            if simbolo not in simbolos:
                trabajo.put_simbolos(simbolos + [simbolo])
            indice_simbolo = trabajo.get_simbolos().index(simbolo)
            # Buscar una transición existente.
            try:
                destinos = trabajo.get_transicion(
                    actual, indice_simbolo
                )
            except IndexError:
                destinos = []
            if destinos:
                siguiente = trabajo.buscar_estado(destinos[0])
                if siguiente == -1:
                    raise ValueError(
                        "La transición apunta a un estado inexistente"
                    )
            else:
                # Crear el estado ausente.
                es_ultimo = posicion == len(cadena) - 1
                tipo = "FINAL" if es_ultimo else "INTERMEDIO"
                nuevo = State(prefijo, tipo)
                trabajo.add_estado(nuevo)
                siguiente = trabajo.buscar_estado(nuevo)
                if siguiente == -1:
                    raise ValueError(
                        "No se pudo localizar el nuevo estado"
                    )
                trabajo.add_transicion(
                    actual,
                    indice_simbolo,
                    trabajo.obtener_estado(siguiente)
                )
            actual = siguiente
        # Marcar como final el estado alcanzado.
        estado_final = trabajo.obtener_estado(actual)
        tipo_actual = estado_final.get_tipo_estado()
        if tipo_actual not in ("FINAL", "INICIAL/FINAL"):
            nuevo_tipo = (
                "INICIAL/FINAL"
                if tipo_actual == "INICIAL"
                else "FINAL"
            )
            estado_final.put_tipo_estado(nuevo_tipo)
    # Registrar la cadena incorporada.
    muestra = list(trabajo.get_alf_entrada())
    if cadena not in muestra:
        muestra.append(cadena)
        trabajo.put_alf_entrada(muestra)
    # Volver a aplicar KC sobre el autómata aprendido.
    return ejecutar_kc(trabajo, k)