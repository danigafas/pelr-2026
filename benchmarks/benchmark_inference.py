import gc
import tracemalloc
import csv
from pathlib import Path
from random import Random
from time import perf_counter
from statistics import median
from pelr.algorithms.prefix_tree import generar_arbol_prefijos
from pelr.algorithms.kc import ejecutar_kc
from pelr.algorithms.im1 import ejecutar_im1, ejecutar_miclet
from pelr.core.recognition import acepta_cadena

def generar_muestra(
    cantidad: int,
    longitud: int,
    semilla: int = 2026
) -> list[str]:
    """Genera cadenas positivas distintas y reproducibles."""
    alfabeto = "abc"
    if cantidad > len(alfabeto) ** longitud:
        raise ValueError("No hay suficientes cadenas distintas")
    generador = Random(semilla)
    muestra = set()
    while len(muestra) < cantidad:
        cadena = "".join(
            generador.choices(alfabeto, k=longitud)
        )
        muestra.add(cadena)
    return sorted(muestra)

def medir(algoritmo: str, muestra: list[str], orden: int = 2, umbral: float = 0.5):
    """Mide una ejecución y verifica sus resultados."""
    # Construcción del árbol de prefijos.
    inicio = perf_counter()
    arbol = generar_arbol_prefijos(muestra)
    tiempo_arbol = perf_counter() - inicio
    estados_iniciales = arbol.obtener_numero_estados()
    # Medición de la inferencia.
    gc.collect()
    def inferir():
        if algoritmo == "KC":
            return ejecutar_kc(arbol, orden)
        elif algoritmo == "IM1":
            return ejecutar_im1(arbol, 0, orden, 0.0)
        elif algoritmo == "IM1-LEVINE":
            return ejecutar_im1(arbol, 1, 0, umbral)
        elif algoritmo == "IM1-MICLET":
            return ejecutar_miclet(arbol)
        else:
            raise ValueError(f"Algoritmo desconocido: {algoritmo}")
    # Medición del tiempo: cinco ejecuciones independientes.
    tiempos = []
    for _ in range(5):
        inicio = perf_counter()
        resultado = inferir()
        tiempos.append(perf_counter() - inicio)
    tiempo_inferencia = median(tiempos)
    # Medición de memoria por separado.
    del resultado
    gc.collect()
    tracemalloc.start()
    try:
        resultado = inferir()
        _, memoria_maxima = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    # Verificar que no se han perdido cadenas positivas.
    reconocidas = sum(
        acepta_cadena(resultado, cadena)
        for cadena in muestra
    )
    return (
        tiempo_arbol,
        tiempo_inferencia,
        estados_iniciales,
        resultado.obtener_numero_estados(),
        memoria_maxima / (1024 ** 2),
        reconocidas
    )

def main():
    cantidad = 80
    k = 2
    filas = []

    longitudes = [6, 8, 10, 12]

    print(
        f"{'Alg.':<6} {'Long.':>6} {'Estados AP':>11} "
        f"{'Resultado':>10} {'Tiempo(s)':>11} "
        f"{'Mem.(MiB)':>11} {'OK':>8}"
    )

    for longitud in longitudes:
        muestra = generar_muestra(cantidad, longitud)

        for algoritmo in ("KC", "IM1"):
            (
                tiempo_arbol,
                tiempo_inferencia,
                estados_iniciales,
                estados_finales,
                memoria,
                reconocidas
            ) = medir(algoritmo, muestra, orden=k)

            print(
                f"{algoritmo:<6} "
                f"{longitud:>6} "
                f"{estados_iniciales:>11} "
                f"{estados_finales:>10} "
                f"{tiempo_inferencia:>11.4f} "
                f"{memoria:>11.2f} "
                f"{reconocidas:>5}/{cantidad}"
            )
            filas.append({
                "algoritmo": algoritmo,
                "cadenas": cantidad,
                "longitud": longitud,
                "k": k,
                "estados_iniciales": estados_iniciales,
                "estados_resultantes": estados_finales,
                "tiempo_arbol_s": tiempo_arbol,
                "tiempo_inferencia_s": tiempo_inferencia,
                "memoria_pico_mib": memoria,
                "reconocidas": reconocidas,
            })
    directorio = Path("benchmarks/results")
    directorio.mkdir(parents=True, exist_ok=True)

    ruta = directorio / "longitud_k2.csv"

    with ruta.open("w", newline="", encoding="utf-8") as fichero:
        escritor = csv.DictWriter(
            fichero,
            fieldnames=filas[0].keys()
        )
        escritor.writeheader()
        escritor.writerows(filas)

    print(f"\nResultados guardados en: {ruta}")

if __name__ == "__main__":
    main()