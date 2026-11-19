# Cooling code

Run commands from the repository root:

```bash
python code/cooling_driver.py --help
python code/cooling_driver.py --input code/input_bsk24 --no-animation --check-energy --out results/bsk24
python code/cooling_driver.py --input code/input_apr --no-animation --out results/apr
```

This folder uses ordinary local Python modules; no editable package installation is required. Dependencies are NumPy, SciPy and Matplotlib; pytest is optional for tests. No Fortran compiler or external EOS download is needed for the five bundled models.

`input_bsk24` is the default. Input files select EOS, mass, envelope and pairing catalogue entries. All packaged inputs use mesh C. The physics/numerical modules are copied unchanged from the latest working solver; only the layout and input mesh defaults were adjusted for this repository.

See [`../docs/USER_GUIDE.md`](../docs/USER_GUIDE.md) for configuration, diagnostics and outputs. Historical implementation notes are archived in `docs/IMPLEMENTATION_HISTORY.txt`; use the user guide for current commands.
