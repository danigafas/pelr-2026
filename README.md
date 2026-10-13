# PELR 2026

**Plataforma para la Experimentación sobre Lenguajes Regulares**  
*A Python revival of a Java university project from 2007.*

PELR is an experimental platform for studying **regular languages, finite automata, and grammatical inference**. Its original implementation was developed in Java in 2007 as a university final project and included an automaton model, a Swing interface, and inference algorithms such as **KC** and **IM1**.

**PELR 2026** is a controlled migration of that project to Python. The goal is to recover and understand the historical implementation, preserve its sources, build automated regression tests, and introduce improvements **without silently changing the original algorithms**.

> **Status — 13 October 2026:** The state and automaton models, prefix-tree generation, classical KC, KC with negative samples, IM1 (k-suffixes, Levine, and Miclet), and nondeterministic string recognition have working Python implementations. The latest locally reported suite result is **176 passed, 2 expected failures**. KC incremental is not yet implemented. The migration remains a work in progress, not a claim of complete equivalence with the 2007 application.

## What does PELR do?

PELR starts with a **positive sample**: strings known to belong to a language. It builds a **prefix-tree acceptor (PTA)** and applies an inference algorithm to merge states, obtaining a smaller automaton that may recognize additional strings.

For example:

```python
positive_sample = ["ab", "ac", "aab"]
```

The prefix tree contains six states, named `%`, `a`, `ab`, `ac`, `aa`, and `aab`. In the historical PELR convention, **`%` denotes the empty string** (ε).

Applying classical **KC with `k = 1`** merges states according to their suffixes. In this example, the resulting groups are:

| Group | State type |
| --- | --- |
| `{%}` | Initial |
| `{a, aa}` | Intermediate |
| `{ab, aab}` | Final |
| `{ac}` | Final |

The inferred transitions are:

```text
{%}        --a--> {a, aa}
{a, aa}    --a--> {a, aa}
{a, aa}    --b--> {ab, aab}
{a, aa}    --c--> {ac}
```

The self-loop on `a` means this example recognizes strings of the form `a⁺(b|c)`, including strings not present in the original sample. **Generalization is the aim of grammatical inference**, but accepting the training data does not establish that the inferred language matches an unknown target language.

The overall workflow is:

```text
Positive sample
      |
      v
Prefix-tree acceptor
      |
      v
Inference algorithm (KC / IM1)
      |
      v
State merging + transition reconstruction
      |
      v
Inferred finite automaton
      |
      v
String recognition and regression checks
```

## Implementation status

| Component | Status |
| --- | --- |
| `State` — names, types, and state operations | Implemented and tested |
| `Automaton` — states, symbols, and transitions | Implemented and tested |
| Transition storage with multiple destinations | Implemented and tested |
| Automaton export (normal and compact formats) | Implemented and tested |
| Prefix-tree construction from positive samples | Implemented and tested |
| Classical KC — suffix comparison, merging, and transition reconstruction | Working first version; tested |
| KC with negative samples — search over values of `k` | Working first version; tested |
| IM1 with k-suffixes | Working first version; tested |
| IM1 with Levine's similarity threshold | Working first version; tested |
| IM1 with Miclet's automatically calculated threshold | Working first version; tested |
| Nondeterministic string recognition (`acepta_cadena`) | Implemented and tested |
| KC incremental | **Not implemented**; two tests marked `xfail` |
| Differential regression suite against Java | Exploratory comparison performed; integration pending |
| CLI / Python GUI | Not implemented |

“Implemented and tested” refers to the current test coverage; it does **not** mean full compatibility with every input of the original Java project.

## Repository layout

```text
pelr-2026/
├── legacy/
│   └── pelr-2007/            # Original Java sources, preserved as reference
├── src/
│   └── pelr/
│       ├── core/
│       │   ├── state.py       # State representation
│       │   ├── automaton.py   # Automaton representation and transitions
│       │   └── recognition.py # Nondeterministic string recognition
│       └── algorithms/
│           ├── prefix_tree.py     # Prefix-tree construction
│           ├── kc.py              # Classical KC
│           ├── kc_negative.py     # KC with negative samples
│           ├── kc_incremental.py  # Pending implementation
│           └── im1.py             # IM1, Levine, and Miclet
├── tests/
│   ├── test_state.py
│   ├── test_automaton.py
│   ├── test_prefix_tree.py
│   ├── test_kc.py
│   ├── test_kc_negative.py
│   ├── test_kc_incremental.py
│   ├── test_im1.py
│   └── test_recognition.py
└── README.md
```

The Java sources under `legacy/pelr-2007/` are kept separate from the Python implementation. In particular, the original `Estado`, `Automata`, `AlgoritmoKC`, `AlgoritmoIM1`, and Swing interface are primary references for the migration.

## Getting started

Use a modern Python installation and a virtual environment. From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install pytest
PYTHONPATH=src python -m pytest -q
```

If the `pelr` package is already installed in your development environment, `PYTHONPATH=src` is unnecessary. Packaging and support across Python versions are still being formalized.

### Example: prefix tree, KC, and recognition

```python
from pelr.algorithms.prefix_tree import generar_arbol_prefijos
from pelr.algorithms.kc import ejecutar_kc
from pelr.core.recognition import acepta_cadena

sample = ["ab", "ac", "aab"]
prefix_tree = generar_arbol_prefijos(sample)
learned = ejecutar_kc(prefix_tree, orden=1)

for state in learned.get_vector_estados():
    print(state.get_nombre_estado(), state.get_tipo_estado())

assert all(acepta_cadena(learned, word) for word in sample)
assert acepta_cadena(learned, "aaab")
```

The current API retains many Spanish method names (`obtener_estado`, `buscar_estado`, `une_estados`, etc.) to make comparisons with the historical Java source easier. A more idiomatic Python API is a later modernization task.

## Tests

PELR 2026 is developed incrementally with **pytest**:

```bash
python -m pytest -q
python -m pytest -v tests/test_kc.py
python -m pytest -v tests/test_im1.py
python -m pytest -v tests/test_kc_negative.py
python -m pytest -v tests/test_recognition.py
```

The latest locally reported result (13 October 2026) is:

```text
176 passed, 2 xfailed
```

The two expected failures belong to KC incremental: its function currently raises `NotImplementedError`. An expected failure (`xfail`) is **not a passing test**; the marks must be removed once that feature is implemented.

Tests include regression cases for previously problematic state merges, positive-sample preservation on selected examples, and recognition over multiple transition destinations. A high test count or coverage percentage **does not prove algorithmic correctness**. Broader property-based and differential tests remain important work.

## Compatibility with PELR 2007

The migration distinguishes **historical behavior**, **known defects**, and **intentional corrections**:

- **Prefix-tree construction:** The Java `addEstadoTransicion()` behavior does not always build missing intermediate prefixes. The Python PTA follows the separate `generaAP()` procedure rather than relying on that method.
- **Output alphabet:** The original Java setter contained an invalid cast from an array to `Vector`; the Python version implements the intended copying behavior.
- **Transition reconstruction in KC and IM1:** A persistent `pertenece` flag in the Java code could suppress later transitions. Python checks duplicate destinations per transition instead, preserving transitions that should exist. The inferred result can therefore be **nondeterministic**.
- **Repeated state merges:** The historical implementation could attempt to merge a state group with itself and fail to terminate. KC and IM1 now skip an already-completed merge, while `Automaton.une_estados()` retains its explicit protection against self-merging.
- **IM1 `Tspos`:** The Python recursion deliberately avoids an observed historical case where a reachable but non-accepting prefix was reported as a positive continuation. Full equivalence in other cases remains to be assessed.
- **Negative samples:** The original recognition path followed only the first transition destination. Python uses `acepta_cadena()` to explore **all reachable destinations**, ensuring that an accepted negative example is not overlooked in a nondeterministic automaton.
- **Negative KC search range:** The Python implementation tests `k` from zero through the **maximum positive sample length**. This differs from the original GUI's order-dependent range based on the last inserted sample. The change is intentional, not an exact reproduction of the GUI.

An exploratory differential study has compared Java and Python on generated samples. The cases where Java completes offer useful reference outputs; cases with Java nontermination and intentional bug fixes require separate treatment. These results have **not yet been incorporated as permanent golden tests** in this repository.

## Current limitations

- KC incremental, the command-line interface, and a new graphical interface are pending.
- Not all Java behavior has been validated against the Python implementation; the tests do not cover every sample, ordering, or edge case.
- Some functions retain Java-inspired naming and broad exception handling that should be refined after the behavior is stable.
- The licensing and provenance of historical assets require review before stating reuse terms. Do not assume that the absence of a `LICENSE` file grants permission for unrestricted reuse.

## Roadmap

1. **Stabilize inference:** expand regression tests for repeated merges and ensure training samples remain accepted over larger and randomized inputs.
2. **Automate differential checks:** adapt the Java/Python comparison harness and record known-good outputs as fixtures, documenting intentional deviations.
3. **Finish KC incremental:** port the state insertion and re-inference behavior from the original Swing handler; replace the `xfail` markers with passing tests.
4. **Improve test quality:** add property-based checks, negative-sample invariants, and edge-case coverage for nondeterministic automata.
5. **Maintainability:** reduce duplicated fusion logic and broad `except Exception` blocks; consider a more idiomatic Python API and automated CI.
6. **Experimentation tools:** CLI, automaton visualization (for example, Graphviz), benchmarks, and potentially a modern GUI.

## About this project

PELR 2026 is a **software preservation, learning, and academic experimentation** project. It connects the original 2007 implementation with modern Python testing and development practices, while treating the original source code as a historical record rather than modifying it in place.
