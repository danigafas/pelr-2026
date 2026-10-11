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

        if estado <0 or simbolo <0:
            raise IndexError("No se permiten índices negativos")
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

    def get_transicion(self, estado: int, simbolo: int) -> list[State]:
        if estado < 0 or simbolo < 0:
            raise IndexError("No se permiten índices negativos")
        if self.delta[estado] is None:
            raise IndexError("Ese estado no tiene transiciones")
        if self.delta[estado][simbolo] is None:
            raise IndexError("No hay transiciones para ese símbolo")
        return self.delta[estado][simbolo]

    def get_vector_transicion(self, estado: int) -> list | None:
        if estado < 0:
            raise IndexError("No se permiten índices negativos")
        return self.delta[estado]

    def get_transicion_estrella(
        self,
        estado: int,
        cadena: str
    ) -> State:
        estado_actual = State(self.obtener_estado(estado))
        for simbolo_actual in cadena:
            try:
                indice_simbolo = self.simbolos.index(simbolo_actual)
                indice_estado = self.buscar_estado(estado_actual)
                destinos = self.get_transicion(indice_estado,indice_simbolo)
                # Aquí estamos limitando la funcionalidad de los automatas no determinísticos.
                # Sólo seleccionamos el primero de los posibles destinos
                estado_actual = destinos[0]
            except Exception as error:
                raise Exception(
                    "No llega a ningún estado válido"
                ) from error
        return estado_actual

    def put_tipo_automata(self, tipo: str) -> None:
        self.tipo = tipo

    def get_tipo_automata(self) -> str | None:
        return self.tipo

    def une_estados(self, primero: int, segundo: int) -> None:
        if primero == segundo:
            raise ValueError("No se puede unir un estado consigo mismo")
        primer_estado = self.obtener_estado(primero)
        segundo_estado = self.obtener_estado(segundo)
        for nombre in segundo_estado.nombres:
            if primer_estado.tipo == "INTERMEDIO":
                tipo_resultante = segundo_estado.tipo
            elif segundo_estado.tipo == "INTERMEDIO":
                tipo_resultante = primer_estado.tipo
            elif ((primer_estado.tipo == "INICIAL" and segundo_estado.tipo == "FINAL")
                or (primer_estado.tipo == "FINAL" and segundo_estado.tipo == "INICIAL")):
                tipo_resultante = "INICIAL/FINAL"
            else:
                tipo_resultante = primer_estado.tipo
            primer_estado.add_estado(nombre,tipo_resultante)
        self.del_estado(segundo_estado)

    def get_alf_entrada(self) -> list[str]:
        return self.alfabeto_entrada

    def put_alf_entrada(self, entrada: list[str]) -> None:
        self.alfabeto_entrada = entrada.copy()

    def get_alf_salida(self) -> list[str] | None:
        return self.alfabeto_salida

    def get_f_salida(self) -> list | None:
        return self.f_salida

    def put_f_salida(self, funcion: list) -> None:
        self.f_salida = funcion.copy()

    # Corrección respecto a PELR 2007:
    # putAlfSalida() contenía una conversión inválida de String[] a Vector.
    def put_alf_salida(self, alfabeto: list[str]) -> None:
        self.alfabeto_salida = alfabeto.copy()

    def add_estado_transicion(self, estado: State) -> bool:
        if self.add_estado(estado):
            cadena = estado.get_estado(0)
            estado_actual = State("%")
            for simbolo_actual in cadena:
                self.add_simbolo(simbolo_actual)
                indice_estado = self.obtener_indice_estado(estado_actual)
                indice_simbolo = self.simbolos.index(simbolo_actual)
                try:
                    destinos = self.get_transicion(indice_estado, indice_simbolo)
                    estado_actual = destinos[0]
                except Exception:
                    self.add_transicion(
                        self.buscar_estado(estado_actual),
                        indice_simbolo,
                        estado
                    )
            return True
        return False

    def guardar_automata(self, compacto: bool, nombre_fichero: str) -> None:
        with open(nombre_fichero, "w", encoding="utf-8") as salida:
            salida.write("Estados: \n\n")
            for indice, estado in enumerate(self.v_estados):
                tipo = estado.get_tipo_estado()
                nombres = estado.get_nombre_estado()
                nombre = ",".join(nombres)
                if compacto:
                    salida.write(f"{indice}. ")
                salida.write(f"[{tipo}] {nombre}\n")
            salida.write("\nAlfabeto: \n\n")
            for simb in self.get_simbolos():
                salida.write(f"{simb}\n")
            salida.write("\nMatriz de transiciones: \n\nEstado ")
            for simb in self.get_simbolos():
                salida.write(f"{simb} ")
            salida.write("\n")
            for indice_estado, estado in enumerate(self.v_estados):
                nombre = ",".join(estado.get_nombre_estado())
                if compacto:
                    salida.write(f"q{self.buscar_estado(estado)} ")
                else:
                    salida.write(f"{{{nombre}}} ")
                for indice_simbolo in range(len(self.simbolos)):
                    try:
                        destinos = self.get_transicion(indice_estado, indice_simbolo)
                        for i, destino in enumerate(destinos):
                            if compacto:
                                salida.write(f"q{self.buscar_estado(destino)}")
                            else:
                                n = ",".join(destino.get_nombre_estado())
                                salida.write(f"{{{n}}}")
                            if i < len(destinos) -1 :
                                salida.write(",")
                        salida.write(" ")
                    except Exception:
                        salida.write("- ")
                salida.write("\n")
