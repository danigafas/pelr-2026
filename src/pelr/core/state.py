class State:
	def __init__(
		self,
		nombres: list[str] | None = None,
		tipo: str | None = "INTERMEDIO"
	):
		if nombres is None:
			self.nombres = []
		else:
			self.nombres = list.copy(nombres)

		self.tipo = tipo
		self.alfabeto_salida: list[str] | None = None