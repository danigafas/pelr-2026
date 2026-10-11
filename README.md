# PELR 2026

**Plataforma para la Experimentación sobre Lenguajes Regulares**  
*A Python revival of a Java university project from 2007.*

PELR is an experimental platform for studying **regular languages, finite automata, and grammatical inference**. The original application was developed in Java in 2007 as a university final project. It included automaton data structures, a Swing graphical interface, and inference algorithms such as **KC** and **IM1**.

**PELR 2026** revisits that work in Python. The objective is not simply to rewrite the application with newer technology, but to **recover, understand, test, and document its original behavior** before making deliberate improvements.

> **Project status:** Work in progress. The core automaton model, prefix-tree generation, and an initial version of classical KC are implemented and covered by automated tests. IM1 and other historical features are still being migrated.

## What does PELR do?

The central experiment starts with a **positive sample**: a set of strings assumed to belong to a regular language. PELR can represent those examples as a **prefix-tree automaton** and then apply an inference algorithm to merge states and produce a more general automaton.

For example, given:

```python
positive_sample = ["ab", "ac", "aab"]
```

The prefix tree contains states corresponding to the distinct prefixes `%`, `a`, `ab`, `ac`, `aa`, and `aab`. In the original PELR convention, **`%` represents the empty string** (ε).

When applying **KC with `k = 1`**, states whose names share the same final character can be merged. In this example, `a` and `aa` merge; the former transition `a --a--> aa` can therefore become a **self-loop** in the inferred automaton.

```text
Positive sample
      |
      v
Prefix-tree automaton
      |
      v
Inference algorithm (KC / IM1)
      |
      v
State merging and transition reconstruction
      |
      v
Inferred finite automaton
```

The inferred automaton may recognize strings beyond the initial sample. That generalization is the purpose of the experiment; it does not, by itself, prove that the inferred language is identical to the unknown target language.

## Implementation status

| Component | Status |
| --- | --- |
| `State`: names, types, and state operations | Implemented and tested |
| `Automaton`: states, symbols, and transitions | Initial port implemented and tested |
| Deterministic and nondeterministic transition storage | Implemented and tested |
| Automaton export (normal and compact formats) | Implemented and tested |
| Prefix-tree construction from positive samples | Implemented and tested |
| Classical KC: suffix comparison, state merging, and transition reconstruction | Initial version implemented and tested |
| IM1: `Tspos` and inference criteria | Planned / in progress |
| Historical KC variants (incremental and negative-sample handling) | Pending investigation and porting |
| Python graphical interface | Not implemented |

These statuses refer to the **currently tested Python functionality**, not exhaustive compatibility with every behavior and input of PELR 2007.

## Repository layout

```text
pelr-2026/
├── legacy/
│   └── pelr-2007/           # Original Java project, kept as a reference
├── src/
│   └── pelr/
│       ├── core/
│       │   ├── state.py      # State representation and operations
│       │   └── automaton.py  # Automaton model and transitions
│       └── algorithms/
│           ├── prefix_tree.py  # Prefix-tree construction
│           └── kc.py           # Classical KC inference
├── tests/
│   ├── test_state.py
│   ├── test_automaton.py
│   ├── test_prefix_tree.py
│   └── test_kc.py
└── README.md
```

The historical sources are preserved separately from the Python implementation. In particular, the Java versions of `Estado`, `Automata`, `AlgoritmoKC`, `AlgoritmoIM1`, and the Swing interface provide a reference for understanding the original design.

## Example: prefix tree and KC

With the project's Python environment configured so that the `pelr` package can be imported:

```python
from pelr.algorithms.prefix_tree import generar_arbol_prefijos
from pelr.algorithms.kc import ejecutar_kc

sample = ["ab", "ac", "aab"]

prefix_tree = generar_arbol_prefijos(sample)
learned_automaton = ejecutar_kc(prefix_tree, orden=1)

for state in learned_automaton.get_vector_estados():
    print(state.get_nombre_estado(), state.get_tipo_estado())
```

The function and method names remain in Spanish where they closely reflect the historical code. Naming conventions may be revisited after functional compatibility has been established.

## Tests

The Python port is developed incrementally using **pytest**. From the repository root, in the configured environment, run:

```bash
python -m pytest -v
```

To run tests for individual components:

```bash
python -m pytest -v tests/test_automaton.py
python -m pytest -v tests/test_prefix_tree.py
python -m pytest -v tests/test_kc.py
```

Tests cover both expected functionality and selected edge cases encountered while analyzing the original Java implementation. Passing the suite is a useful regression check, **not** a claim of complete behavioral equivalence.

## Compatibility with PELR 2007

The migration follows a deliberate approach:

1. Examine the original Java implementation and recover the intent of its algorithms.
2. Reproduce the relevant behavior in small Python modules, independent of the old Swing interface.
3. Add automated tests and compare results with known examples.
4. Record intentional corrections separately from historical behavior.

Some legacy details require special attention:

- The historical `addEstadoTransicion()` method does not always create missing intermediate prefix states. Prefix-tree generation is therefore ported from the separate `generaAP()` routine.
- The Java output-alphabet setter contained an invalid array-to-`Vector` cast. The Python setter implements the intended list-copying behavior.
- The original KC transition-reconstruction logic used a duplicate-detection flag whose lifetime could suppress later transitions. The Python implementation checks existing destinations for each transition instead.

These distinctions matter: **faithful migration does not mean silently preserving every accidental bug**, and fixes should not obscure how the original program worked.

## Roadmap

The next priority is **IM1**, beginning with `Tspos` and then the state-comparison and inference procedures present in `AlgoritmoIM1.java`. Further work includes checking the historical KC variants, extending compatibility and edge-case tests, and evaluating whether a modern user interface would be useful.

## About this project

PELR 2026 is an ongoing **software preservation, learning, and academic experimentation** project. It connects the original 2007 implementation with current Python development practices while retaining the original sources as a historical reference.
