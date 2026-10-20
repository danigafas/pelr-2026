import pytest
from pathlib import Path
from pelr.algorithms.prefix_tree import generar_arbol_prefijos
from pelr.algorithms.kc import ejecutar_kc
from pelr.algorithms.im1 import ejecutar_im1, ejecutar_miclet
from pelr.core.recognition import acepta_cadena

RUTA_MUESTRAS = Path(__file__).parent / "data" / "muestras_pelr_150.txt"

MUESTRAS = [
    linea.split()
    for linea in RUTA_MUESTRAS.read_text(encoding="utf-8").splitlines()
    if linea.strip()
]

@pytest.mark.parametrize(
    "muestra",
    MUESTRAS,
    ids=[f"caso_{i:03d}" for i in range(len(MUESTRAS))]
)
@pytest.mark.parametrize("algoritmo", ["KC", "IM1"])
def test_inferencia_conserva_muestra_positiva(muestra, algoritmo):
    longitud_maxima = max(len(cadena) for cadena in muestra)

    for k in range(longitud_maxima + 1):
        arbol = generar_arbol_prefijos(muestra)

        if algoritmo == "KC":
            resultado = ejecutar_kc(arbol, k)
        else:
            resultado = ejecutar_im1(arbol, 0, k, 0.0)

        for cadena in muestra:
            assert acepta_cadena(resultado, cadena), (
                f"{algoritmo}, K={k}, "
                f"muestra={muestra}: "
                f"no reconoce {cadena!r}"
            )

@pytest.mark.parametrize(
    "muestra",
    MUESTRAS,
    ids=[f"caso_{i:03d}" for i in range(len(MUESTRAS))]
)
@pytest.mark.parametrize("modo,umbral", [
    ("Levine", 0.3),
    ("Levine", 0.5),
    ("Levine", 0.8),
    ("Miclet", None),
])
def test_im1_levine_miclet_conserva_positivos(muestra, modo, umbral):

    arbol = generar_arbol_prefijos(muestra)

    if modo == "Miclet":
        resultado = ejecutar_miclet(arbol)
    else:
        resultado = ejecutar_im1(
            arbol,
            algoritmo=1,
            orden=0,
            umbral=umbral
        )

    for cadena in muestra:
        assert acepta_cadena(resultado, cadena), (
            f"{modo}, umbral={umbral}, "
            f"muestra={muestra}: "
            f"no reconoce {cadena!r}"
        )
