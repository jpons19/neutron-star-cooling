# Reproducibility

Snapshot date: 19 November 2026. No reference curves are observational fits.

The core solver/microphysics Python modules are copied byte-for-byte from the current working version. The repository changes their organisation, moves standalone experiment scripts into `examples/`, replaces workspace-specific paths, and makes mesh C the default in the input files. The example scripts explicitly use mesh C.

Curated data:

- `examples/five_eos/reference`: five per-EOS CSV tracks, energy-closure reports, settings/summary and the combined import CSV.
- `examples/gap_scan/reference`: twenty CSV tracks, per-run diagnostic summaries, reference Tc profiles, combined import CSV and reference figures.
- `examples/neutrino_zones/reference`: integrated history, three local emissivity/temperature CSVs, selected times, and history arrays used for shading.
- `examples/eos_tables/reference`: P(rho) and P(mu_b) diagnostics. Their scripts read `code/eos/` directly.
- `docs/article/data`: the datasets archived with the manuscript; they duplicate selected example data intentionally so the article folder is portable.

Importable cooling CSV schema: `model,mass_Msun,time_years,L_infinity_erg_s`. Luminosity means photon luminosity at infinity in erg/s. Raw per-track CSVs have only `time_years,L_infinity_erg_s`. Tracks stop below 1e31 erg/s and are not extrapolated.

All scalar summaries and ratio tables originate in saved simulation output; interpolation for time-specific comparisons is logarithmic and restricted to the overlap of tracks. Dominance means the largest integrated individual neutrino process, not necessarily >50% of total neutrino losses.

Reference choices: target M=1.4 Msun, B=0, Gudmundsson envelope, pairing models 7/12/8, initial uniform T_inf=1e10 K, mesh C, maximum accepted relative cell temperature change 1.25%. See each reference `settings.json`. Actual software versions used for the packaging checks are recorded in `runtime_environment.json`; Python 3.13 is the intended local environment but is not claimed to have been tested here unless recorded there.

The gap-scan references reproduce the previous five-EOS BSk24/APR tracks to rtol 1e-10. All twenty gap runs had energy-closure residuals below 0.12% from 1 yr onward. Integrated snapshot emissivities agree with recorded per-process luminosities to rtol 1e-12. These checks establish internal consistency, not independent physical validation. Spatial convergence, PBF response and APR crust composition remain separate questions.

To refresh committed references after a deliberate physics/configuration change, first run into `results/`, inspect the new outputs and diagnostics, and only then explicitly replace selected files in `reference/`. `.gitignore` excludes generated results but retains curated references.
