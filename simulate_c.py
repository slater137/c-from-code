#!/usr/bin/env python3
"""simulate_c.py  — v1.1
-------------------------------------------------
Numerically evaluates the emergent signalling speed

    v_* = √(χ / κ) / ℓ_P

and (optionally) performs a lightweight bootstrap to
estimate statistical uncertainty, as described in
Shrieve (2025).

Key improvements (v1.1)
----------------------
* **Graceful defaults** – running the script *without* CLI
  arguments now falls back to sensible example values
  instead of exiting with `SystemExit: 2`.
* **Self‑tests** – `--test` flag runs a tiny unit‑test suite
  to guard against regressions.
* **Benchmarks** – `--bench` prints JSON describing the
  host machine and wall‑clock setup time, allowing readers
  to quote their own timings.

Quick start
-----------
```bash
# Example run with defaults
python simulate_c.py

# Explicit arguments
python simulate_c.py --n 65536 --kappa 0.125 --chi 0.051 \
                     --eps 1e-6 --trials 12 --seed 42

# One‑liner benchmark
python simulate_c.py --bench

# Run internal tests
python simulate_c.py --test
```
"""
from __future__ import annotations

import argparse
import json
import math
import multiprocessing as mp
import os
import platform
import random
import statistics
import sys
import time
from dataclasses import dataclass
from typing import Optional

# ---------------------------------------------------------------------------
# Physical constant (CODATA 2018)
ELL_P = 1.616_255e-35  # Planck length [m]

# ---------------------------------------------------------------------------
# Defaults used when no CLI overrides are supplied
DEFAULT_N = 65_536       # lattice sites
DEFAULT_KAPPA = 0.125    # code rate k/n
DEFAULT_CHI = 0.051      # entropy density
DEFAULT_EPS = 1e-6       # LR tail cut‑off
DEFAULT_TRIALS = 1
DEFAULT_SEED = 0


@dataclass
class SimParams:
    """Container for all simulation parameters."""

    n: int = DEFAULT_N
    kappa: float = DEFAULT_KAPPA
    chi: float = DEFAULT_CHI
    eps: float = DEFAULT_EPS
    trials: int = DEFAULT_TRIALS
    seed: int = DEFAULT_SEED


# ---------------------------------------------------------------------------
# Core numerical routine

def compute_vstar(chi: float, kappa: float) -> float:
    """Return v_* [m/s] for positive χ, κ."""
    if chi <= 0 or kappa <= 0:
        raise ValueError("chi and kappa must be positive and non‑zero")
    return math.sqrt(chi / kappa) / ELL_P


def bootstrap_vstar(params: SimParams) -> tuple[float, float]:
    """Mean ± σ of v_* over a toy bootstrap on χ."""
    random.seed(params.seed)
    samples = [
        compute_vstar(max(1e-12, random.gauss(params.chi, params.eps * params.chi)), params.kappa)
        for _ in range(params.trials)
    ]
    mean = statistics.mean(samples)
    std = statistics.stdev(samples) if params.trials > 1 else 0.0
    return mean, std


# ---------------------------------------------------------------------------
# CLI & helpers

def parse_cli(argv: Optional[list[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Compute emergent signalling speed v_*")
    p.add_argument('--n', type=int, help='lattice sites')
    p.add_argument('--kappa', type=float, help='code rate k/n')
    p.add_argument('--chi', type=float, help='entropy density')
    p.add_argument('--eps', type=float, help='LR tail cut‑off (default 1e‑6)')
    p.add_argument('--trials', type=int, help='bootstrap samples')
    p.add_argument('--seed', type=int, help='RNG seed')
    p.add_argument('--bench', action='store_true', help='print hardware/time JSON then exit')
    p.add_argument('--test', action='store_true', help='run internal unit tests then exit')

    ns = p.parse_args(argv)
    return ns


def ns_to_params(ns: argparse.Namespace) -> SimParams:
    """Fill in missing namespace attributes with defaults."""
    return SimParams(
        n=ns.n if ns.n is not None else DEFAULT_N,
        kappa=ns.kappa if ns.kappa is not None else DEFAULT_KAPPA,
        chi=ns.chi if ns.chi is not None else DEFAULT_CHI,
        eps=ns.eps if ns.eps is not None else DEFAULT_EPS,
        trials=ns.trials if ns.trials is not None else DEFAULT_TRIALS,
        seed=ns.seed if ns.seed is not None else DEFAULT_SEED,
    )


# ---------------------------------------------------------------------------
# Self‑tests

def _test_compute_vstar() -> None:
    assert math.isclose(
        compute_vstar(chi=0.051, kappa=0.125),
        math.sqrt(0.051 / 0.125) / ELL_P,
    )
    try:
        compute_vstar(-1.0, 0.1)
    except ValueError:
        pass
    else:
        raise AssertionError("Negative χ did not raise ValueError")


def _run_tests() -> None:
    """Run minimal internal tests."""
    _test_compute_vstar()
    print("All self‑tests passed.")


# ---------------------------------------------------------------------------
# Entry‑point

def main(argv: Optional[list[str]] = None) -> None:
    ns = parse_cli(argv)

    if ns.test:
        _run_tests()
        return

    if ns.bench:
        t0 = time.time()
        compute_vstar(chi=0.05, kappa=0.1)
        elapsed = round(time.time() - t0, 4)
        bench_out = {
            "python": platform.python_version(),
            "machine": platform.platform(),
            "cpus": mp.cpu_count(),
            "elapsed_s": elapsed,
        }
        print(json.dumps(bench_out))
        return

    params = ns_to_params(ns)
    mean_v, std_v = bootstrap_vstar(params)

    result = {
        "params": params.__dict__,
        "ell_p_m": ELL_P,
        "v_star_mean_m_per_s": mean_v,
        "v_star_std_m_per_s": std_v,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
