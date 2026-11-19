# Validation of the packaged layout

Checks performed on 19 November 2026:

- All copied core solver/microphysics Python modules are byte-identical to the current working source. The package changes the folder layout and makes mesh C the input default.
- Packaged regression suite: **51 passed, 1 slow test deselected**. Warnings include documented EOS/composition/mesh approximations and an installed pytest-plugin deprecation; there were no test failures.
- Default BSk24 driver: non-interactive run to 1000 yr completed and wrote the expected CSVs and shaded cooling diagnostic. The accepted last age can exceed the requested limit.
- Reference-data plotting commands completed for five EOS, gap amplitudes, neutrino zones and both EOS-table diagnostics. Input references are kept separate from generated output.
- The BSk24 neutrino example reran the cooling and reproduced the original reference to rtol 1e-10. Integration of each saved emissivity profile reproduced the process luminosities to rtol 1e-12.
- The relocated five-EOS runner completed all five evolutions. Every track reproduces its packaged reference to rtol 1e-10 (same dimensions, no extrapolation).
- The article is supplied as the already compiled, visually checked 14-page PDF, with six figures and no unresolved references. TeX binaries/distribution are not bundled.

See `runtime_environment.json` for the Python/scientific-library versions used here. The current preparation runtime uses Python 3.12; the supplied VSCode setup uses your local `.venv` and does not claim a Python 3.13 validation run.

The complete twenty-run gap experiment was performed before packaging and its core modules are unchanged. Its relocated CLI/imports and plotting paths were checked; the twenty thermal evolutions were not all repeated solely to package these paths. The slow spatial-convergence test was not run in this packaging check.

These are internal regression/reproducibility checks. They do not resolve APR inner-crust composition, the PBF weak response, or the need for broader spatial convergence studies.
