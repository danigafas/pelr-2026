from pelr.core.automaton import Automaton
from pelr.core.state import State
from sys import float_info

CacheTs = dict[tuple[int, int], tuple[str, ...]]

def ts_pos(
    automata: Automaton,
    estado: State,
    orden: int,
    cache: CacheTs | None = None
) -> list[str]:

    if cache is None:
        cache = {}
    clave = (id(estado), orden)
    if clave in cache:
        return list(cache[clave])
    resultado = []
    if orden == 0:
        if estado.get_tipo_estado() in ("FINAL", "INICIAL/FINAL"):
            resultado.append("%")
    else:
        i_estado = automata.obtener_indice_estado(estado)
        if orden == 1:
            for indice, simbolo in enumerate(automata.get_simbolos()):
                try:
                    destinos = automata.get_transicion(i_estado, indice)
                    primero = destinos[0]
                except Exception:
                    continue
                if primero.get_tipo_estado() == "FINAL":
                    resultado.append(simbolo)
            if estado.get_tipo_estado() in ("FINAL", "INICIAL/FINAL"):
                resultado.append("%")
        elif orden > 1:
            for indice, simbolo in enumerate(automata.get_simbolos()):
                try:
                    destinos = automata.get_transicion(i_estado, indice)
                    primero = destinos[0]
                except Exception:
                    continue
                continuaciones = ts_pos(
                    automata, primero, orden - 1, cache
                )
                for continuacion in continuaciones:
                    if continuacion != "%":
                        nueva = simbolo + continuacion
                        resultado.append(nueva)
            anteriores = ts_pos(
                automata, estado, orden - 1, cache
            )
            for continuacion in anteriores:
                if continuacion not in resultado:
                    resultado.append(continuacion)
    cache[clave] = tuple(resultado)
    return resultado

def calcular_ts(automata: Automaton, orden: int) -> list[list[str]]:
    resultado = []
    for indice_estado in range(automata.obtener_numero_estados()):
        estado = automata.obtener_estado(indice_estado)
        vtemp = ts_pos(automata, estado, orden)
        resultado.append(vtemp)
    return resultado

def con_k_sufijos(
    vec_tes: list[list[str]],
    estado1: int,
    estado2: int
) -> bool:
    """Compara las T de dos estados según IM1 de PELR 2007."""
    return vec_tes[estado1] == vec_tes[estado2]

def interseccion(v1: list[str], v2: list[str]) -> list[str]:
    resultado = []
    # Recorrer v1 y añadir los elementos presentes en v2.
    for indice in range(len(v1)):
        if v1[indice] in v2:
            resultado.append(v1[indice])
    return resultado

def con_levine(
    automata: Automaton,
    u: int,
    v: int,
    s: float,
    cache: CacheTs | None = None,
    longitud_maxima: int | None = None
) -> bool:
    """Compara dos estados mediante el criterio Levine de PELR 2007."""
    if cache is None:
        cache = {}
    similitud_maxima = -1.0
    """longitud_maxima = 0
    for estado in automata.get_vector_estados():
        longitud = len(estado.get_estado(0))
        if longitud > longitud_maxima:
            longitud_maxima = longitud"""
    if longitud_maxima is None:
        longitud_maxima = max(
            (
                len(estado.get_estado(0))
                for estado in automata.get_vector_estados()
            ),
            default=0
        )
    estado_u = automata.obtener_estado(u)
    estado_v = automata.obtener_estado(v)
    for orden in range(longitud_maxima + 1):
        aux1 = ts_pos(automata, estado_u, orden, cache)
        aux2 = ts_pos(automata, estado_v, orden, cache)
        comunes = interseccion(aux1, aux2)
        denominador = len(aux1)+len(aux2)
        if denominador!= 0:
            stren = (2 * len(comunes)) / denominador
        else:
            stren = 0
        if stren > similitud_maxima:
            similitud_maxima = stren
    return similitud_maxima >= s

def ejecutar_im1(
    automata: Automaton,
    algoritmo: int,
    orden: int,
    umbral: float
) -> Automaton:
    """Ejecuta IM1 siguiendo la implementación de PELR 2007."""
    vec_tes = calcular_ts(automata, orden)
    b = Automaton()
    b.put_alf_entrada(automata.get_alf_entrada())
    b.put_simbolos(automata.get_simbolos())
    cantidad = automata.obtener_numero_estados()
    cond = [False] * cantidad
    anad = [False] * cantidad
    b.add_estado(State(automata.obtener_estado(0)))
    cache_ts = {} if algoritmo in (1, 2) else None
    longitud_maxima = None
    if algoritmo in (1, 2):
        longitud_maxima = max(
            (
                len(estado.get_estado(0))
                for estado in automata.get_vector_estados()
            ),
        default=0
    )
    for i in range(cantidad):
        primero = b.buscar_estado(automata.obtener_estado(i))
        for j in range(i, cantidad):
            if i == j:
                continue
            if not anad[j]:
                temporal = automata.obtener_estado(j)
                if b.add_estado(State(temporal)):
                    anad[j] = True
            if algoritmo == 0:
                fusionar = con_k_sufijos(vec_tes, i, j)
            elif algoritmo in (1, 2):
                fusionar = con_levine(
                    automata,
                    i,
                    j,
                    umbral,
                    cache_ts,
                    longitud_maxima
                )
            else:
                raise ValueError("Algoritmo IM1 desconocido")
            if fusionar and not cond[j]:
                segundo = b.buscar_estado(automata.obtener_estado(j))
                if primero != segundo:
                    b.une_estados(primero, segundo)
                cond[j] = True

    # Reconstrucción de transiciones
    for i in range(automata.obtener_numero_estados()):
        origen_original = automata.obtener_estado(i)
        indice_origen = b.buscar_estado(origen_original)
        for j in range(len(automata.get_simbolos())):
            try:
                destinos = automata.get_transicion(i, j)
                destino_original = destinos[0]
            except Exception:
                continue
            # Localizar en b el grupo del destino original.
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

def calcular_umbral_miclet(automata: Automaton) -> float:
    """Calcula el umbral automático de Miclet según generaS() de PELR 2007."""
    cache: CacheTs = {}
    estados = automata.get_vector_estados()

    umbral = float_info.max
    longitud_maxima = 0
    for estado in estados:
        longitud = len(estado.get_estado(0))
        if longitud > longitud_maxima:
            longitud_maxima = longitud
    for i in range(len(estados)):
        for j in range(i + 1, len(estados)):
            similitud_maxima = -1.0
            for orden in range(longitud_maxima + 1):
                t1 = ts_pos(automata, estados[i], orden, cache)
                t2 = ts_pos(automata, estados[j], orden, cache)
                comunes = interseccion(t1, t2)
                denominador = len(t1) + len(t2)
                if denominador != 0:
                    similitud = (2 * len(comunes)) / denominador
                else:
                    similitud = 0.0
                if similitud > similitud_maxima:
                    similitud_maxima = similitud
            # Miclet elige el menor valor positivo.
            if 0 < similitud_maxima < umbral:
                umbral = similitud_maxima
    return umbral

def ejecutar_miclet(automata: Automaton) -> Automaton:
    """Ejecuta IM1 con el umbral automático de Miclet."""
    umbral = calcular_umbral_miclet(automata)
    return ejecutar_im1(
        automata,
        algoritmo=2,
        orden=0,
        umbral=umbral
    )