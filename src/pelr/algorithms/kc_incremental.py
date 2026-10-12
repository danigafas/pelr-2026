from pelr.core.automaton import Automaton
from pelr.core.state import State
from pelr.algorithms.kc import ejecutar_kc

def ejecutar_kc_incremental(
    automata: Automaton,
    cadena: str,
    k: int
) -> Automaton:

    # 1. Comenzar en el estado inicial.

    # 2. Recorrer los símbolos de la nueva cadena.

    # 3. Seguir las transiciones existentes.

    # 4. Si falta una transición, crear el estado
    #    y conectar el autómata.

    # 5. Marcar como final el estado alcanzado.

    # 6. Volver a ejecutar KC sobre el autómata modificado.