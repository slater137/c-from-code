# *c* from Code

> Reference implementation for the numerical experiments in **Shrieve (2025), *“An Information-Theoretic Origin for Light Speed”***.
>
> Computes the emergent signalling speed
>
> and reproduces all figures and tables in the paper.

---

## 1. Features

* **Single‑file script** – `simulate_c.py` (≈200 LOC) with no external modules beyond NumPy & SciPy.
* **Reproducible** – deterministic output given the RNG seed; `--bench` prints host hardware/time.
* **Self‑tests** – `--test` flag runs a micro unit‑test suite to guard against regressions.
* **Zero‑config** – sensible defaults mean `python simulate_c.py` “just works.”

---

## 2. Installation

### Conda (recommended)

```bash
conda env create -f env.yml
conda activate c-from-code
```

### Pip

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Dependencies (≥ versions):

* Python 3.11
* NumPy 1.26
* SciPy 1.13

---

## 3. Usage

### Quick run (defaults)

```bash
python simulate_c.py           # JSON output with v_* value
```

### Custom parameters

```bash
python simulate_c.py \
  --n 65536            \
  --kappa 0.125        \
  --chi 0.051          \
  --eps 1e-6           \
  --trials 12          \
  --seed 42
```

### Benchmark host machine

```bash
python simulate_c.py --bench   # prints hardware + elapsed_s in JSON
```

### Run self‑tests

```bash
python simulate_c.py --test
```

---

## 4. Command‑line flags

| Flag       | Default | Description                                |
| ---------- | ------- | ------------------------------------------ |
| `--n`      | 65 536  | Lattice sites                              |
| `--kappa`  | 0.125   | Code rate *k*/n                            |
| `--chi`    | 0.051   | Entropy density                            |
| `--eps`    | 1e‑6    | LR tail cut‑off                            |
| `--trials` | 1       | Bootstrap samples                          |
| `--seed`   | 0       | RNG seed (PCG64)                           |
| `--bench`  | –       | Print hardware info & setup time then exit |
| `--test`   | –       | Run internal unit tests                    |

---

## 5. Reproducing the paper’s figures

The exact configuration used for Figures 2–3 is:

```bash
python simulate_c.py --n 65536 --kappa 0.125 --chi 0.051 \
                     --eps 1e-6 --trials 12 --seed 42 > results.json
```

Parse `results.json` for `v_star_mean_m_per_s` and `v_star_std_m_per_s` and feed those numbers into your plotting routine (e.g., matplotlib or pgfplots).

---

## 6. Citation

If you use this code, please cite:

```bibtex
@software{Shrieve2025simulatec,
  author  = {Slater Shrieve},
  title   = {c-from-code: An Information-Theoretic Origin for Light Speed},
  version = {v1.0},
  doi     = {10.5281/zenodo.xxxxx},
  year    = {2025}
}
```

---

## 7. License

This project is released under the [MIT License](LICENSE).

---

## 8. Author & Acknowledgements

**Slater Shrieve** – [slater.shrieve@icloud.com](mailto:slater.shrieve@icloud.com)

Numerical method inspired by discussions with D. Hoffman and the Quantum Error‑Correction reading group.

---

## 9. Contributing

Pull requests are welcome for bug fixes, performance tweaks, or expanded tests. Please open an issue first to discuss substantial changes.
