# Gap amplitude scan: BSk24 and APR

Twenty runs at 1.4 Msun: one reference and nine one-channel variations per EOS. The existing gap models are crust n = 7, core n = 12, core p = 8. Scale factors 0, 0.5 and 2 multiply Tc(rho) on faces and cells; the other two channels are unchanged. Scaling Tc is equivalent to scaling Delta0 with its conversion factor fixed. Momentum support and gap shape do not change. This is an amplitude sensitivity test, not an exploration of density shifts, widths or all gap models.

Fixed: mesh C, initial redshifted T=1e10 K, B=0, Gudmundsson envelope, Yakovlev MURCA and BCF2024 bremsstrahlung, original conductivities and other neutrino rates, composition and effective masses. Each EOS stellar structure is constructed once and reused unchanged. All runs use the same timestep settings and stop below Lgamma_inf=1e31 erg/s. Curves are not extrapolated.

APR retains its published Maxwell jump. Its unresolved crust-composition mapping remains provisional; the gap comparison within APR does not remove that limitation.

Energy closure is checked in time windows from 1 yr, using the microphysics of each run. Spatial convergence has not been established by this scan.

| EOS | Case | L(1e4 yr)/reference | L(1e5 yr)/reference | Cutoff age [kyr] | Max energy residual [%] |
|---|---|---:|---:|---:|---:|
| BSk24 | reference | 1 | 1 | 1071.83 | 0.106 |
| BSk24 | crust_n_x0 | 1.009 | 1.058 | 1132.45 | 0.096 |
| BSk24 | crust_n_x0.5 | 0.9986 | 0.9995 | 1069.27 | 0.103 |
| BSk24 | crust_n_x2 | 1 | 0.9995 | 1072.35 | 0.097 |
| BSk24 | core_n_x0 | 1 | 5.677 | 1639.99 | 0.012 |
| BSk24 | core_n_x0.5 | 1 | 5.677 | 1493.92 | 0.021 |
| BSk24 | core_n_x2 | 0.1345 | 0.589 | 981.21 | 0.087 |
| BSk24 | core_p_x0 | 0.2074 | 0.7116 | 1353.34 | 0.018 |
| BSk24 | core_p_x0.5 | 0.6479 | 0.7575 | 1044.26 | 0.063 |
| BSk24 | core_p_x2 | 1.144 | 1.088 | 1079.73 | 0.116 |
| APR | reference | 1 | 1 | 583.58 | 0.040 |
| APR | crust_n_x0 | 1.027 | 1.057 | 633.12 | 0.036 |
| APR | crust_n_x0.5 | 1 | 0.9999 | 583.69 | 0.042 |
| APR | crust_n_x2 | 1 | 0.9994 | 581.41 | 0.023 |
| APR | core_n_x0 | 5.675 | 6.739 | 1280.22 | 0.010 |
| APR | core_n_x0.5 | 1.14 | 0.8775 | 609.90 | 0.109 |
| APR | core_n_x2 | 1.269 | 1.172 | 572.22 | 0.011 |
| APR | core_p_x0 | 1.095 | 1.23 | 820.80 | 0.023 |
| APR | core_p_x0.5 | 1.004 | 1.003 | 581.76 | 0.019 |
| APR | core_p_x2 | 1.001 | 0.9996 | 582.33 | 0.092 |

Reference reproduction: {'BSk24': True, 'APR': True}

See the per-EOS settings and reference_Tc_profiles CSVs for normalization and actual stellar Tc ranges. The combined cooling_gap_scan.csv uses model,mass_Msun,time_years,L_infinity_erg_s.

Reference peak Tc sampled inside each star (K):

| EOS | Crust n | Core n | Core p |
|---|---:|---:|---:|
| BSk24 | 8.51058e+09 | 4.05675e+08 | 6.79475e+09 |
| APR | 8.51041e+09 | 9.16632e+08 | 6.79475e+09 |
