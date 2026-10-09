from __future__ import annotations

class State:
    def __init__(
        self,
        nombres: State | list[str] | str | None = None,
        tipo: str | None = None
    ):
        if nombres is None:
            self.nombres = []
            self.tipo = "INTERMEDIO"
        elif isinstance(nombres, State):
            self.nombres = nombres.nombres.copy()
            self.tipo = nombres.tipo
        elif isinstance(nombres, str):
            self.nombres = [nombres]
            self.tipo = tipo
        else:
            self.nombres = nombres.copy()
            self.tipo = tipo

        self.alfabeto_salida: list[str] | None = None

    def get_tipo_estado(self) -> str | None:
        return self.tipo

    def get_nombre_estado(self) -> list[str]:
        return self.nombres

    def put_tipo_estado(self, tipo: str | None) -> None:
        self.tipo = tipo

    def put_nombre_estado(self, nombres: list[str]) -> None:
        self.nombres = nombres.copy()

    def add_estado(self, nombre: str, tipo: str | None) -> None:
        self.nombres.append(nombre)
        self.tipo = tipo

    def del_estado(self, nombre: str) -> None:
        if nombre in self.nombres:
            self.nombres.remove(nombre)

    def get_num_estados(self) -> int:
        return len(self.nombres)

    def get_indice_estado(self, nombre: str) -> int:
        if nombre in self.nombres:
            return self.nombres.index(nombre)
        else:
            return -1