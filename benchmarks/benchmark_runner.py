import csv
import json
import os
import subprocess
import sys

from datetime import datetime
from pathlib import Path
from time import perf_counter


RAIZ = Path(__file__).resolve().parents[1]

CAMPOS = [
    "estado", "algoritmo", "cadenas", "longitud", "k", "umbral",
    "semilla", "estados_iniciales", "estados_resultantes",
    "tiempo_arbol_s", "tiempo_inferencia_s",
    "memoria_pico_mib", "reconocidas", "consistente",
    "duracion_total_s", "error"
]

def ejecutar_experimento(
    algoritmo: str,
    cantidad: int,
    longitud: int,
    k: int,
    limite: float = 15.0,
    umbral: float = 0.5
) -> dict:

    comando = [
        sys.executable,
        "-m", "benchmarks.benchmark_worker",
        "--algoritmo", algoritmo,
        "--cadenas", str(cantidad),
        "--longitud", str(longitud),
        "--k", str(k),
        "--umbral", str(umbral),
    ]

    entorno = os.environ.copy()
    entorno["PYTHONPATH"] = os.pathsep.join(filter(None, [
        str(RAIZ / "src"),
        entorno.get("PYTHONPATH", "")
    ]))

    fila = {
        "algoritmo": algoritmo,
        "cadenas": cantidad,
        "longitud": longitud,
        "k": k,
        "semilla": 2026,
        "estado": "error",
        "error": "",
        "umbral": umbral if algoritmo == "IM1-LEVINE" else None,
    }

    inicio = perf_counter()

    try:
        proceso = subprocess.run(
            comando,
            cwd=RAIZ,
            env=entorno,
            capture_output=True,
            text=True,
            timeout=limite
        )

        if proceso.returncode != 0:
            fila["error"] = (
                proceso.stderr or proceso.stdout
            ).strip()[-400:]

        else:
            try:
                datos = json.loads(proceso.stdout)
                fila.update(datos)

                if datos.get("consistente") is True:
                    fila["estado"] = "ok"
                elif datos.get("consistente") is False:
                    fila["estado"] = "inconsistente"
                else:
                    fila["error"] = "Resultado sin campo consistente"

            except (json.JSONDecodeError, AttributeError):
                fila["error"] = "El worker no devolvió JSON válido"

    except subprocess.TimeoutExpired:
        fila["estado"] = "timeout"
        fila["error"] = f"Superado el límite de {limite}s"

    fila["duracion_total_s"] = round(
        perf_counter() - inicio, 4
    )

    return fila


def main():
    perfiles = [
        (5, 6),
        (8, 6),
    ]

    k = 0
    limite = 15.0

    directorio = RAIZ / "benchmarks" / "results"
    directorio.mkdir(parents=True, exist_ok=True)

    marca = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta = directorio / f"stress_{marca}.csv"

    with ruta.open("w", newline="", encoding="utf-8") as fichero:
        escritor = csv.DictWriter(
            fichero,
            fieldnames=CAMPOS,
            extrasaction="ignore"
        )
        escritor.writeheader()
        fichero.flush()

        for cantidad, longitud in perfiles:
            for algoritmo in ("IM1-LEVINE", "IM1-MICLET"):
                print(
                    f"Ejecutando {algoritmo}: "
                    f"{cantidad} cadenas, longitud {longitud}, K={k}",
                    flush=True
                )

                fila = ejecutar_experimento(
                    algoritmo, cantidad, longitud, k, limite
                )

                escritor.writerow(fila)
                fichero.flush()

                print(
                    f"  {fila['estado']} | "
                    f"{fila['duracion_total_s']:.3f}s",
                    flush=True
                )

    print(f"\nResultados guardados en: {ruta}")

if __name__ == "__main__":
    main()