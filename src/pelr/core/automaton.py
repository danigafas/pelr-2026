from __future__ import annotations

from pelr.core.state import State


class Automaton:
    """
    Representa un autómata de PELR.

    Adaptación de Automata.java (2007).
    """

    def __init__(
        self,
        v_estados: Automaton | list[State] | None = None,
        alfabeto_entrada: list[str] | None = None,
        delta: list | None = None,
        simbolos: list[str] | None = None
    ) -> None:
        if isinstance(v_estados, Automaton):
            origen = v_estados
            self.v_estados = origen.v_estados.copy()
            self.alfabeto_entrada = origen.alfabeto_entrada.copy()
            self.alfabeto_salida = origen.alfabeto_salida.copy()
            self.delta = origen.delta.copy()
            self.f_salida = origen.f_salida.copy()
            self.simbolos = origen.simbolos.copy()
            self.tipo = None
        elif (
            v_estados is not None
            and alfabeto_entrada is not None
            and delta is not None
            and simbolos is not None
        ):
            self.v_estados = v_estados.copy()
            self.alfabeto_entrada = alfabeto_entrada.copy()
            self.alfabeto_salida = None
            self.delta = delta.copy()
            self.tipo = None
            self.f_salida = None
            self.simbolos = simbolos.copy()
        else:
            if any(
                argumento is not None
                for argumento in (v_estados, alfabeto_entrada, delta, simbolos)
            ):
                raise TypeError("Debes proporcionar los cuatro argumentos")
            self.v_estados: list[State] = []
            self.alfabeto_entrada = []
            self.alfabeto_salida = []
            self.delta = []
            self.tipo = ""
            self.f_salida = []
            self.simbolos: list[str] = []

    def get_vector_estados(self) -> list[State]:
        return self.v_estados

    def put_vector_estados(self, estados: list[State]) -> list[State]:
        self.v_estados = estados.copy()

    def buscar_estado(self, estado: State) -> int:
        nombre = estado.get_estado(0)
        for i, grupo in enumerate(self.v_estados):
            if nombre in grupo.nombres:
                return i
        return -1

    def add_estado(self, estado: State) -> bool:
        if self.buscar_estado(estado) == -1:
            self.v_estados.append(estado)
            return True
        return False

    def obtener_indice_estado(self, estado: State) -> int:
        for i, grupo in enumerate(self.v_estados):
            if grupo.compara_estado(estado):
                return i
        return -1

    def del_estado(self, estado: State) -> None:
        indice = self.obtener_indice_estado(estado)
        if indice != -1:
            del self.v_estados[indice]

    def obtener_estado(self, indice: int) -> State:
        if indice < 0:
            raise IndexError("El índice no puede ser negativo")
        return self.v_estados[indice]

    def obtener_numero_estados(self) -> int:
        return len(self.v_estados)

    def get_simbolos(self) -> list[str]:
        return self.simbolos

    def put_simbolos(self, simbolos: list[str]) -> None:
        self.simbolos = simbolos.copy()

    def add_simbolo(self, simbolo: str) -> None:
        if simbolo not in self.simbolos:
            self.simbolos.append(simbolo)

    def del_simbolo(self, simbolo: str) -> None:
        if simbolo in self.simbolos:
            self.simbolos.remove(simbolo)

    def get_delta(self) -> list:
        return self.delta

    def put_delta(self, delta: list) -> None:
        self.delta = delta.copy()

    def limpia_transiciones(self) -> None:
        self.delta.clear()

    def add_transicion(
        self,
        estado: int,
        simbolo: int,
        destino: State
    ) -> None:

        while len(self.delta) <= estado:
            self.delta.append(None)

        if self.delta[estado] is None:
            self.delta[estado] = []

        while len(self.delta[estado]) <= simbolo:
            self.delta[estado].append(None)

        if self.delta[estado][simbolo] is None:
            self.delta[estado][simbolo] = []

        if destino not in self.delta[estado][simbolo]:
            self.delta[estado][simbolo].append(State(destino))
