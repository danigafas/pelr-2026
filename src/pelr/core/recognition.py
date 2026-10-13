from pelr.core.automaton import Automaton


def acepta_cadena(automata: Automaton, cadena: str) -> bool:
    """Comprueba si un autómata acepta una cadena."""
    if automata.obtener_numero_estados() == 0:
        return False
    # En PELR 2007, % representa la cadena vacía.
    if cadena == "%":
        cadena = ""
    simbolos = automata.get_simbolos()
    actuales = {0}
    for simbolo in cadena:
        if simbolo not in simbolos:
            return False
        indice_simbolo = simbolos.index(simbolo)
        siguientes = set()
        for indice_estado in actuales:
            try:
                destinos = automata.get_transicion(
                    indice_estado, indice_simbolo
                )
            except IndexError:
                continue
            for destino in destinos:
                indice_destino = automata.buscar_estado(destino)
                if indice_destino < 0:
                    raise ValueError(
                        "La transición apunta a un estado inexistente"
                    )
                siguientes.add(indice_destino)
        actuales = siguientes
        if not actuales:
            return False
    return any(
        automata.obtener_estado(i).get_tipo_estado()
        in ("FINAL", "INICIAL/FINAL")
        for i in actuales
    )