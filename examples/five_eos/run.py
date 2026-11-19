"""Compare five 1.4 Msun stars with the driver's default microphysics.

Run from repository root: python examples/five_eos/run.py
APR and BSk25 require the documented source handling in EOS_NOTES.md.
"""
import sys
from pathlib import Path
REPO = Path(__file__).resolve().parents[2]
CODE = REPO / "code"
sys.path.insert(0, str(CODE))
HERE = Path(__file__).resolve().parent

import argparse
import json
from dataclasses import asdict, replace
from pathlib import Path
from time import perf_counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from config import CoolingConfig
from cooling import run_cooling
from cooling_driver import save_run
from emissivity import NEUTRINO_PROCESSES, modified_urca_emissivity
from emissivity_updated import use_updated_rates
from energy_balance import energy_budget, energy_closure
from input_model import read_parameters
from stellar_structure import StructureOptions, build_stellar_model

ROOT = CODE


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=HERE / "results")
    parser.add_argument("--mesh", default="C", choices=("A", "B", "C", "D"))
    args = parser.parse_args()
    from mesh import mesh_spec
    args.out.mkdir(parents=True, exist_ok=True)
    cfg = read_parameters(ROOT / "input_bsk24")
    config = replace(CoolingConfig(), initial_temperature_8=cfg["Tinit8"])
    use_updated_rates()
    NEUTRINO_PROCESSES.register("modified_urca", replace=True)(modified_urca_emissivity)
    summaries = []
    fig, ax = plt.subplots(figsize=(8.5, 6))
    for name, color in zip(("BSk22", "BSk24", "BSk25", "BSk26", "APR"),
                           ("#4477AA", "#228833", "#EE7733", "#AA3377", "#222222")):
        start = perf_counter()
        model = build_stellar_model(StructureOptions(name, mass_solar=1.4,
                                    mesh=mesh_spec(args.mesh)), ROOT / "eos", cfg)
        background = model.background
        structure_seconds = perf_counter() - start
        start = perf_counter()
        run = run_cooling(background, config)
        cooling_seconds = perf_counter() - start
        out = args.out / name
        out.mkdir(exist_ok=True)
        save_run(out, background, run)
        closure = energy_closure(energy_budget(run, background), start_years=1, tolerance=.01)
        (out / "energy_closure.txt").write_text(closure.format() + "\n")
        mr = model.eos.mass_radius
        stable = mr[:np.argmax(mr[:, 1]) + 1]
        rref = float(np.interp(1.4, stable[:, 1], stable[:, 0]))
        core = background.cells.xh == 0
        cells = background.cells
        durca = core & ((cells.kf_n <= cells.kf_p + cells.kf_e) |
                        ((cells.ymu > 0) & (cells.kf_n <= cells.kf_p + cells.kf_mu)))
        row = dict(eos=name, mass_solar=model.star.mass_solar,
                   radius_km=model.star.radius_cm / 1e5, radius_compose_km=rref,
                   central_pressure=model.star.pressure_central,
                   central_nb_fm3=float(model.eos.at_pressure(model.star.pressure_central).nb_fm3),
                   direct_urca_cells=int(durca.sum()), cells=len(cells.rho),
                   accepted_steps=run.completed_steps, rejected_steps=run.rejected_steps,
                   final_years=float(run.step_times_years[-1]), stop_reason=run.stop_reason,
                   energy_max_error=closure.max_error,
                   structure_seconds=structure_seconds, cooling_seconds=cooling_seconds)
        summaries.append(row)
        (args.out / "summary.json").write_text(json.dumps(summaries, indent=2) + "\n")
        print(json.dumps(row), flush=True)
        label = "DDFGOS(APR)*" if name == "APR" else name + ("*" if name == "BSk25" else "")
        ax.loglog(run.times_years, run.luminosity_erg_s, color=color,
                  lw=2.2, ls="--" if name == "APR" else "-", label=label)
    ax.set(xlabel="Age [yr]", ylabel=r"$L_\gamma^\infty$ [erg s$^{-1}$]",
           xlim=(1, 1.2e6), ylim=(8e30, 1e35),
           title=r"Neutron-star cooling: $M=1.4\,M_\odot$, $B=0$")
    ax.grid(True, which="major", alpha=.25)
    ax.legend(frameon=False)
    ax.text(.03, .05, "Gudmundsson envelope · same pairing prescriptions\n"
            "MURCA: Yakovlev+2001 · bremsstrahlung: BCF2024", transform=ax.transAxes, fontsize=9)
    fig.text(.12, .025, "* Source-table caveats: BSk25 crust–core join; APR crust composition (see EOS_NOTES.md).", fontsize=8)
    fig.tight_layout(rect=(0, .05, 1, 1))
    fig.savefig(args.out / "cooling_five_eos.png", dpi=200)
    fig.savefig(args.out / "cooling_five_eos.pdf")
    settings = asdict(config)
    settings["final_years"] = None  # infinity = disabled; valid JSON
    (args.out / "settings.json").write_text(json.dumps(dict(cooling=settings,
         input=cfg, mesh=args.mesh), indent=2) + "\n")


if __name__ == "__main__":
    main()
