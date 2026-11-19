# EOS packages and the five-model comparison

The default is **BSk24, 1.4 solar masses**, selected in `input_bsk24`.
`cooling_driver.py`, `make cooling` and `compare_emissivities.py` use this input
unless another is supplied. Use `mass = 1.4`, rather than copying a central
pressure between EOS. BSk22, BSk24, BSk25, BSk26 and APR are available.

## Sources

- BSk25: [PCP(BSK25), CompOSE 257](https://compose.obspm.fr/eos/257).
  Goriely, Chamel & Pearson (2013), PRC 88, 024308; Pearson et al. (2018),
  MNRAS 481, 2994, with the 2019 erratum. Further references are in the provider README.
- APR: [DDFGOS(APR), CompOSE 327](https://compose.obspm.fr/eos/327).
  Akmal, Pandharipande & Ravenhall (1998), PRC 58, 1804;
  Constantinou et al. (2014), PRC 89, 065802; Davis et al. (2024),
  A&A 687, A44, and the 2025 work cited by the CompOSE data sheet.
  This is specifically the CUTER reconstruction with a Maxwell phase transition,
  not an arbitrary APR parametrization or an APR core joined to BSk crust.

Downloaded on 2026-11-19. Each new folder contains the original provider files,
data sheet and README, plus `source.json` with URLs and SHA-256 hashes.
The source bytes are not modified. Both packages supply electron and muon
fractions and neutron/proton Landau effective masses, which the cooling model uses.
The web summary lists APR as npeN, but its actual composition file includes muons.

## Explicit handling of source-table features

### BSk25: consolidated discrete crust–core interface

Pressure reverses in the last inner-crust rows and at the first core row.
The generic reader correctly rejects this (~5% local reversal). Merely sorting
the table or relaxing the universal monotonicity test would mix phases.

For this particular package, the reader retains the first homogeneous core row
(data row 297, nb=0.0855534 fm^-3, P=0.2105624368 MeV fm^-3) and omits
crust rows 291–296, whose pressure exceeds that core onset. The last retained
crust row is 290. All fields use the same mask.

Decision consolidated with the user on 2026-11-19 after inspection of the raw
P(rho) and P(mu_b) profiles: retain the direct connection from row 290 to row
297 as the adopted discrete approximation to Maxwell coexistence at the
available table resolution. The nearby crust and core branches motivate this
choice. No precise coexistence crossing has been solved, no equality of P and
mu_b has been imposed on these two rows, and no interpolated Maxwell plateau
has been added. This is an adopted interface prescription, not an exact
thermodynamic reconstruction or a provider-issued correction.
The omission is warned about; the adapter fails if its expected row count changes.
Other EOS retain the original <=0.1% pressure-reversal policy.

### BSk26: consolidated single-row omission

Decision consolidated with the user on 2026-11-19: omit data row 276, whose
pressure is 0.037% below row 275. The existing monotonicity filter already
implements this omission consistently in all interpolated fields. Original
source files remain unchanged.

### APR: Maxwell jump

Rows 1886–1896 describe a constant-pressure Maxwell interval at
P=5.8692415398 MeV fm^-3. The endpoint baryon densities are
0.2047519151 and 0.2369174514 fm^-3. The reader keeps both endpoints at
identical pressure and omits only interior rows 1887–1895. Interpolation on
either side preserves the finite jump; the high-density endpoint is selected
at the transition pressure. The TOV RHS sees that same discontinuity, and the
cooling mesh includes a face exactly at it. No finite radial layer of interpolated
mixed matter is introduced. Charge-neutrality validation applies to the retained
homogeneous endpoints; the discarded mixed rows do not satisfy it individually.

### APR: unresolved source consistency issues

The raw crust has max |(epsilon+P)/(nb mu_b)-1| = 3.97e-4.
For APR crust only, a warning and a bounded tolerance of 5e-4 replace the
generic 1e-5 check. The core keeps 1e-5. No pressure or energy values are altered.

More significantly, the supplied inner-crust values of Ye, Yn, A and Z do not
satisfy Ye=(1-Yn) Z/A in the conventions assumed by this code. The discrepancy
reaches approximately 78% on this stellar mesh. The existing warning remains
visible. This first comparison retains the tabulated Ye and Yn and uses the
existing xh=1-Yn mapping; **APR crust transport and heat capacity must therefore
be regarded as provisional** pending clarification of the cluster definitions
or a corrected composition table. Good mass–radius agreement does not validate
this mapping. Do not silently enforce neutrality by changing Ye or Yn.

The APR structural phase transition is included, but the cooling calculation
uses the existing nucleonic/leptonic neutrino channels. No extra pion-condensate
emissivity is introduced. Thus this is a comparison with common cooling
prescriptions, not a complete calculation of all possible APR phase microphysics.

## Reproduction and interpretation

Run `python examples/five_eos/run.py` (no animation). It constructs all stars at 1.4 Msun,
uses the same mesh preset C, initial redshifted temperature 1e10 K, gap choices
(crust 7, core neutron 12, proton 8), corrected Gudmundsson envelope,
Yakovlev et al. (2001) MURCA and BCF2024 nucleon bremsstrahlung. It retains
the refined 1.25% temperature-change criterion and stops each star when
L_gamma at infinity falls below 1e31 erg/s. `--mesh A` reproduces the coarser preliminary comparison; `--mesh D` enables
a spatial convergence study without changing physics.

Output in `results_eos/`: one overlaid luminosity plot (PNG/PDF), per-EOS
CSV curves/profiles, `summary.json`, `settings.json` and energy-closure reports.
Radii are checked against the provider's `eos.mr` interpolated at 1.4 Msun.
These are code-consistency and published-structure checks, not independent
validation of the cooling curves. The comparison changes structure, composition,
effective masses and density-dependent pairing profiles together. BSk22 may open
direct Urca at this mass; its existing mesh-resolution warning is retained.

The tests in `tests/test_eos_additions.py` check provider radii, the Maxwell jump,
unchanged source files and negative controls for invalid EOS data.

## Results of this run (mesh C, generated from summary.json)

| EOS | R [km] | Final age [yr] | Max closure error [%] | Direct Urca cells |
|---|---:|---:|---:|---:|
| BSk22 | 13.040 | 765032 | 0.063 | 18 |
| BSk24 | 12.574 | 1071833 | 0.106 | 0 |
| BSk25 | 12.375 | 911449 | 0.155 | 0 |
| BSk26 | 11.771 | 740166 | 0.339 | 0 |
| APR | 11.491 | 583575 | 0.040 | 0 |

Closure refers to decade windows starting at 1 yr, excluding unresolved startup.
All runs reached the luminosity cutoff. These diagnostics do not settle the source
composition questions above. The mesh-A comparison is summarized in
results_eos/mesh_check.json; no claim of full spatial convergence is made.

Repository layout: EOS source files live in `code/eos/`; executable examples and curated results live in `examples/`. Run example commands from the repository root. Paths in earlier run descriptions above refer to the original working layout.
