from pelr.core.automaton import Automaton
from pelr.algorithms.kc import ejecutar_kc

def comprueba_muestra_negativa(automata: Automaton, muestra_negativa: list[str]) -> bool:
    """Indica si el autómata acepta alguna cadena negativa."""
    for cadena in muestra_negativa:
        try:
            temp = automata.get_transicion_estrella(0, cadena)
            if (temp.get_tipo_estado() == "INICIAL/FINAL") or (temp.get_tipo_estado() == "FINAL"):
                return True
        except Exception:
            continue
    return False

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
