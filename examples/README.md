# Reproducible examples

Run from the repository root after activating `.venv`. Every example separates committed `reference/` files from regenerated `results/` files. Plotting reads reference data by default and does not overwrite it.

| Example | Replot reference data | Recompute numerical data |
|---|---|---|
| Five EOS | `python examples/five_eos/plot.py` | `python examples/five_eos/run.py` |
| Gap amplitudes | `python examples/gap_scan/plot.py` | `python examples/gap_scan/run.py BSk24` and `python examples/gap_scan/run.py APR` |
| Neutrino zones | `python examples/neutrino_zones/plot.py` | `python examples/neutrino_zones/run.py` |
| EOS tables | `python examples/eos_tables/plot_pressure.py` and `python examples/eos_tables/plot_mu.py` | Same commands; they read the raw bundled EOS tables |

To plot a new cooling calculation rather than reference data:

```bash
python examples/gap_scan/plot.py --input-dir examples/gap_scan/results
python examples/neutrino_zones/plot.py --input-dir examples/neutrino_zones/results
python examples/five_eos/plot.py --input-dir examples/five_eos/results
```

All plotting commands accept their shown defaults; gap/neutrino/five-EOS plotters also accept `--output-dir`. The two raw-table plotters always write to their own `results/` directory.

The gap scan has ten runs per EOS: reference, then factors 0, 0.5 and 2 for one channel at a time. Gap momentum support/shape, stellar structure and all unrelated controls are fixed. Both BSk24 and APR computations must finish before plotting the combined result.

The neutrino example selects accepted states nearest the logarithmic midpoint of three distinct global-dominance zones, then evaluates every registered emissivity at the actual local thermal profile. It reproduces the reference BSk24 cooling history before constructing the diagnostic.

Reference timings depend on hardware. A reference star took tens of seconds in the preparation environment; the twenty-run gap experiment takes several minutes. These are runtime estimates, not performance guarantees.
