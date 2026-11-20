# results_cooling

Neutron-star cooling sweeps run with the `neutron-star-cooling` solver, 19–20 November 2026. 164 runs in total.

Open `report.html` in a browser. It is self-contained, with all eight figures embedded, and holds the full discussion.

- **Gap/envelope/mass sweep:** 67 runs, report sections 1–5.
  Data: `tables/run_table.csv`, `tables/cooling_sweep_curves.csv`, `tables/run_qc.csv`, `tables/bands.csv` (first version), `tables/source_verdicts.txt`.
  Inputs: `runs_inputs/gap_sweep/`.
- **Mass sweep with default microphysics:** 50 runs (5 EOS × 10 masses, 1.2–2.0 M☉), section 6.
  Data: `tables/mass_sweep_table.csv`, `tables/mass_sweep_curves.csv`, `tables/mass_sweep_qc.csv`.
  Inputs: `runs_inputs/mass_sweep/`.
- **Follow-up runs, blocks F–K:** 47 runs, section 7. They cover the cold edge at other central densities, the hot edge across proton gaps, the direct Urca map, accreted envelopes, late times down to 10^27 erg/s, and numerical checks.
  Data: `tables/followup_run_table.csv`, `tables/followup_curves.csv`, `tables/followup_qc.csv`.
  Inputs: `runs_inputs/followup_sweep/`.
- **Current bands and verdicts:** `tables/bands_v2.csv` (from all runs) and `tables/source_verdicts_v2.txt`.
- **Figures:** `figures/fig1`–`fig8` (PNG). `fig4` uses the rebuilt bands.
- **Scripts:** `scripts/`. They expect the solver repository at `/home/claude/neutron-star-cooling` and the sweep folders at `/home/claude/{sweep,msweep,sweep3}`; edit those paths to reuse them.
