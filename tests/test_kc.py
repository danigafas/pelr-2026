from pelr.algorithms.kc import se_une
from pelr.core.state import State
from pelr.algorithms.prefix_tree import generar_arbol_prefijos
from pelr.algorithms.kc import ejecutar_kc

def test_kc_sufijos_iguales_k1():
    assert se_une("a", "aa", 1) is True
    assert se_une("ab", "aab", 1) is True

def test_kc_sufijos_distintos_k1():
    assert se_une("ab", "ac", 1) is False

def test_kc_sufijos_k2():
    assert se_une("ab", "aab", 2) is True
    assert se_une("a", "aa", 2) is False

def test_kc_estado_raiz():
    assert se_une("%", "a", 1) is False

def test_kc_orden_cero():
    assert se_une("ab", "ac", 0) is True

def test_kc_agrupacion_k1():
    arbol = generar_arbol_prefijos(["ab", "ac", "aab"])
    resultado = ejecutar_kc(arbol, 1)
    grupos = {
        frozenset(estado.get_nombre_estado())
        for estado in resultado.get_vector_estados()
    }
    assert grupos == {
        frozenset(["%"]),
        frozenset(["a", "aa"]),
        frozenset(["ab", "aab"]),
        frozenset(["ac"]),
    }
    # El árbol original debe conservar sus seis estados.
    assert arbol.obtener_numero_estados() == 6

def test_kc_agrupacion_k2():
    arbol = generar_arbol_prefijos(["ab", "ac", "aab"])
    resultado = ejecutar_kc(arbol, 2)
    grupos = {
        frozenset(estado.get_nombre_estado())
        for estado in resultado.get_vector_estados()
    }
    assert grupos == {
        frozenset(["%"]),
        frozenset(["a"]),
        frozenset(["ab", "aab"]),
        frozenset(["ac"]),
        frozenset(["aa"]),
    }

def test_kc_genera_bucle():
    arbol = generar_arbol_prefijos(["aa"])
    resultado = ejecutar_kc(arbol, 1)
    indice_raiz = resultado.buscar_estado(State("%"))
    indice_fusionado = resultado.buscar_estado(State("a"))
    indice_aa = resultado.buscar_estado(State("aa"))
    # Los dos estados originales ahora pertenecen al mismo grupo.
    assert indice_fusionado == indice_aa
    simbolo_a = resultado.get_simbolos().index("a")
    # La raíz conduce al estado fusionado.
    destinos_raiz = resultado.get_transicion(indice_raiz, simbolo_a)
    assert destinos_raiz[0].compara_estado(
        resultado.obtener_estado(indice_fusionado)
    )
    # El estado fusionado tiene un bucle con 'a'.
    destinos_bucle = resultado.get_transicion(indice_fusionado, simbolo_a)
    assert destinos_bucle[0].compara_estado(
        resultado.obtener_estado(indice_fusionado)
    )

def test_kc_no_duplica_transiciones():
    arbol = generar_arbol_prefijos(["aa", "aaa"])
    resultado = ejecutar_kc(arbol, 1)
    indice = resultado.buscar_estado(State("a"))
    indice_aa = resultado.buscar_estado(State("aa"))
    indice_aaa = resultado.buscar_estado(State("aaa"))
    # Los tres nombres pertenecen al mismo grupo.
    assert indice == indice_aa == indice_aaa
    simbolo = resultado.get_simbolos().index("a")
    destinos = resultado.get_transicion(indice, simbolo)
    # Aunque había dos transiciones originales,
    # solamente debe existir un bucle.
    assert len(destinos) == 1
    assert destinos[0].compara_estado(
        resultado.obtener_estado(indice)
    )

def test_kc_completo_k1():
    arbol = generar_arbol_prefijos(["ab", "ac", "aab"])
    resultado = ejecutar_kc(arbol, 1)
    assert resultado.obtener_numero_estados() == 4
    raiz = resultado.buscar_estado(State("%"))
    grupo_a = resultado.buscar_estado(State("a"))
    grupo_ab = resultado.buscar_estado(State("ab"))
    grupo_ac = resultado.buscar_estado(State("ac"))
    # Comprobamos las fusiones.
    assert grupo_a == resultado.buscar_estado(State("aa"))
    assert grupo_ab == resultado.buscar_estado(State("aab"))
    # Los cuatro grupos son diferentes.
    assert len({raiz, grupo_a, grupo_ab, grupo_ac}) == 4
    # Función auxiliar para comprobar destinos.
    def destinos(origen, simbolo):
        indice_simbolo = resultado.get_simbolos().index(simbolo)
        transiciones = resultado.get_transicion(
            origen, indice_simbolo
        )
        return [
            frozenset(estado.get_nombre_estado())
            for estado in transiciones
        ]
    assert destinos(raiz, "a") == [frozenset(["a", "aa"])]
    # El bucle.
    assert destinos(grupo_a, "a") == [frozenset(["a", "aa"])]
    # Las otras ramas.
    assert destinos(grupo_a, "b") == [frozenset(["ab", "aab"])]
    assert destinos(grupo_a, "c") == [frozenset(["ac"])]
    # KC no modifica el árbol original.
    assert arbol.obtener_numero_estados() == 6

def test_kc_evitar_autofusion():
    arbol = generar_arbol_prefijos(["aaa", "aa", "a"])
    resultado = ejecutar_kc(arbol, 2)
    assert resultado.obtener_numero_estados() > 0