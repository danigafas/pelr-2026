from pelr.core.automaton import Automaton
from pelr.algorithms.kc import ejecutar_kc
from pelr.core.recognition import acepta_cadena

def comprueba_muestra_negativa(
    automata: Automaton,
    muestra_negativa: list[str]
) -> bool:
    """Indica si el autómata acepta alguna cadena negativa."""
    return any(
        acepta_cadena(automata, cadena)
        for cadena in muestra_negativa
    )

def ejecutar_kc_con_negativos(arbol: Automaton, muestra_negativa: list[str]) -> tuple[Automaton, int, bool]:
    longitud_maxima = max(
        len(cadena) for cadena in arbol.get_alf_entrada()
    )
    reconmneg = True
    for k in range(longitud_maxima + 1):
        resultado = ejecutar_kc(arbol, k)
        reconmneg = comprueba_muestra_negativa(resultado, muestra_negativa)
        if not reconmneg:
            return resultado, k, True
    return resultado, k, False
