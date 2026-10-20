import argparse
import json

from benchmarks.benchmark_inference import generar_muestra, medir


def main():
    parser = argparse.ArgumentParser(
        description="Ejecuta un experimento de PELR"
    )

    parser.add_argument(
        "--algoritmo",
        choices=["KC", "IM1", "IM1-LEVINE", "IM1-MICLET"],
        required=True
    )
    parser.add_argument("--cadenas", type=int, required=True)
    parser.add_argument("--longitud", type=int, required=True)
    parser.add_argument("--k", type=int, default=2)
    parser.add_argument("--semilla", type=int, default=2026)
    parser.add_argument("--umbral", type=float, default=0.5)

    args = parser.parse_args()

    if args.cadenas < 1 or args.longitud < 1 or args.k < 0:
        parser.error("Los parámetros deben ser positivos y K >= 0")

    muestra = generar_muestra(
        args.cadenas,
        args.longitud,
        args.semilla
    )

    (
        tiempo_arbol,
        tiempo_inferencia,
        estados_iniciales,
        estados_resultantes,
        memoria,
        reconocidas
    ) = medir(args.algoritmo, muestra, args.k, args.umbral)

    resultado = {
        "algoritmo": args.algoritmo,
        "cadenas": args.cadenas,
        "longitud": args.longitud,
        "k": args.k,
        "semilla": args.semilla,
        "estados_iniciales": estados_iniciales,
        "estados_resultantes": estados_resultantes,
        "tiempo_arbol_s": tiempo_arbol,
        "tiempo_inferencia_s": tiempo_inferencia,
        "memoria_pico_mib": memoria,
        "reconocidas": reconocidas,
        "consistente": reconocidas == args.cadenas,
        "umbral": args.umbral if args.algoritmo == "IM1-LEVINE" else None,
    }

    print(json.dumps(resultado))


if __name__ == "__main__":
    main()