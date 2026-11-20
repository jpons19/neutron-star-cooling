# results_cooling

Neutron-star cooling sweeps run with the `neutron-star-cooling` solver, 19–20 November 2026.

Open `report.html` in a browser. It is self-contained, with the figures embedded, and holds the full discussion.

- **Gap/envelope/mass sweep:** 67 runs, sections 1–5 and 7 of the report.
  Data: `tables/run_table.csv`, `tables/cooling_sweep_curves.csv`, `tables/bands.csv`, `tables/run_qc.csv`, `tables/source_verdicts.txt`.
  Inputs: `runs_inputs/gap_sweep/`.
- **Mass sweep with default microphysics:** 50 runs (5 EOS × 10 masses, 1.2–2.0 M☉), section 6.
  Data: `tables/mass_sweep_table.csv`, `tables/mass_sweep_curves.csv`, `tables/mass_sweep_qc.csv`.
  Inputs: `runs_inputs/mass_sweep/`.
- **Figures:** `figures/fig1`–`fig5` (PNG).
- **Scripts:** `scripts/`. They expect the solver repository at `/home/claude/neutron-star-cooling`; edit the `CODE` path in `run.py` and `run_mass.py` to use them elsewhere.
