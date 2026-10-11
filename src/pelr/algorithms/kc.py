from pelr.core.automaton import Automaton
from pelr.core.state import State

def se_une(primero: str, segundo: str, orden: int) -> bool:
    """Comprueba la coincidencia de sufijos según KC de PELR 2007."""
    if len(primero) > orden:
        p = primero[len(primero)-orden:]
    else:
        p = primero

    if len(segundo) > orden:
        s = segundo[len(segundo)-orden:]
    else:
        s = segundo

    return p == s

def ejecutar_kc(arbol: Automaton, orden: int) -> Automaton:
    """Aplica KC sobre un árbol de prefijos."""
    b = Automaton()
    b.put_alf_entrada(arbol.get_alf_entrada())
    b.put_simbolos(arbol.get_simbolos())
    cantidad = arbol.obtener_numero_estados()
    cond = [False] * cantidad
    anad = [False] * cantidad
    b.add_estado(State(arbol.obtener_estado(0)))

    for i in range(cantidad):
        primero = b.buscar_estado(arbol.obtener_estado(i))
        for j in range(i, cantidad):
            if i == j:
                continue
            if not anad[j]:
                temporal = arbol.obtener_estado(j)
                if b.add_estado(State(temporal)):
                    anad[j] = True
            if se_une(arbol.obtener_estado(i).get_estado(0), arbol.obtener_estado(j).get_estado(0), orden) and not cond[j]:
                segundo = b.buscar_estado(arbol.obtener_estado(j))
                b.une_estados(primero, segundo)
                cond[j] = True

    for i in range(arbol.obtener_numero_estados()):
        origen_original = arbol.obtener_estado(i)
        indice_origen = b.buscar_estado(origen_original)
        for j in range(len(arbol.get_simbolos())):
            try:
                destinos = arbol.get_transicion(i, j)
            except Exception:
                continue
            destino_original = destinos[0]
            primero = b.buscar_estado(destino_original)
            tmp = b.obtener_estado(primero)
            try:
                destinos_existentes = b.get_transicion(indice_origen, j)
            except Exception:
                destinos_existentes = []
            existe = any (
                destino.compara_estado(tmp)
                for destino in destinos_existentes
            )
            if not existe:
                b.add_transicion(indice_origen, j, tmp)
    return b