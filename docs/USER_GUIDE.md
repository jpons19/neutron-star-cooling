# User guide

## Environment

Open a terminal in the repository root. Create a virtual environment with the Python you intend to use, for example `python3.13 -m venv .venv` on macOS if that executable is installed, or `python3 -m venv .venv`. Activate it with `source .venv/bin/activate`, then run `python -m pip install -r code/requirements.txt`.

The workspace file points VSCode to `.venv/bin/python`, enables Python analysis of `code/`, and uses the root folder for terminal commands. If VSCode has a previously saved interpreter choice, use **Python: Select Interpreter** and choose this environment. No machine-specific absolute interpreter path is committed.

## Reference evolution

```bash
python code/cooling_driver.py --no-animation --check-energy --out results/reference
```

`--no-animation` permits unattended runs. Omit it for the live Matplotlib animation. BSk24/1.4 Msun/mesh C is the default; the initial redshifted temperature is 1e10 K. The structure is constructed from the specified EOS rather than reusing a central pressure from another model.

Input examples: `code/input_bsk22`, `input_bsk24`, `input_bsk25`, `input_bsk26`, `input_apr`. For example:

```bash
python code/cooling_driver.py --input code/input_apr --no-animation --out results/apr
```

Edit a copy of an input file to select masses, EOS, envelope (`gudmundsson`, `fe`, `accreted`), pairing switches/catalogue entries, and mesh (`A`, `B`, `C`, `D`). Preserve the positional header/pairing lines. Read `python code/superfluid.py` to display the implemented gap catalogue. Optional named settings follow the header. The three pairing switches are crust neutron singlet, core neutron triplet, and core proton singlet.

## Controls

- `--final-years 1000`: optional final-age limit; the last accepted step can pass this age.
- `--min-luminosity 1e31`: photon-luminosity cutoff at infinity.
- `--min-temperature`: optional minimum local temperature stop.
- `--check-energy`: independent thermal-energy accounting.
- `--murca y01`: reference modified Urca; `yl95` and `bottaro` select alternatives.
- `--old-rates`: legacy selection of all standard nucleonic rates; it is not just a modified-Urca switch.

Use `--help` for the full interface. Numerical defaults are defined in `code/config.py`; initially 20 fixed backward-Euler steps are followed by adaptive integration. The current maximum accepted cell temperature change is 1.25%. Late time-step growth remains subject to rejection. Mesh C is the reference prescription; mesh D can be used for a convergence study.

## Outputs

Each run writes a cooling curve and diagnostic CSVs below `--out`. Multi-star runs use per-star subfolders. Principal quantities:

| Output | Meaning |
|---|---|
| `cooling_curve.csv` | `time_years`, `L_infinity_erg_s`; photon luminosity at infinity |
| `temperature_profiles.csv` | Redshifted cell temperatures versus microphysical baryon mass density |
| `profile_times.csv` | Accepted step numbers and corresponding ages |
| `time_steps.csv` | Accepted steps, dt and maximum relative temperature change |
| `neutrino_processes.csv` | Per-process integrated neutrino luminosities at infinity and leading process |
| shaded cooling figure | Driver diagnostic; photons replace neutrino shading when total photon luminosity is larger |

The `examples/neutrino_zones` figure deliberately keeps **neutrino-only** shading at all times, marking photon dominance separately. Its classification therefore differs from the driver's late red shading; the underlying process luminosities are identical.

Local emissivity uses local temperature `T = T_inf / exp(Phi)`. The neutrino luminosity at infinity integrates `Q * exp(2 Phi) * dV_proper`. Microphysical density is `rho_b = 1.66e-24 * n_b` in g/cm3; EOS-pressure figures explicitly use `epsilon/c^2` instead.

## Interpretation

The five EOS tables provide composition and Landau effective masses. Raw provider files remain unchanged. BSk25 omits rows 291–296 in the reader, retaining 290 -> 297; BSk26 omits row 276. APR retains both Maxwell endpoints and a mesh face at the density jump. APR's inner-crust composition mapping remains provisional. The current PBF response is a documented working approximation; the gap scan does not compare weak-vertex prescriptions. A small energy residual is not proof of spatial convergence or of microphysical correctness.
