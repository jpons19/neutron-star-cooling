# BSk24: neutrino dominance and local emissivity profiles

Reference: M=1.4 Msun, B=0, mesh C, Gudmundsson envelope, gaps 7/12/8, Yakovlev modified Urca and BCF2024 nucleon bremsstrahlung. The rerun reproduces the prior BSk24 reference to rtol=1e-10.

Shading classifies the largest individual neutrino luminosity at infinity: Lnu_i_inf = integral Q_i exp(2 Phi) dV_proper. It does not classify local peak emissivity or compare an individual neutrino process with photons. Time boundaries are geometric midpoints between accepted samples and have timestep-level resolution. The plotted range starts at 1 yr. Snapshots are accepted states nearest the logarithmic midpoint of each interval; no isothermal profile is assumed.

Local Q is evaluated at the actual local temperature T_inf(r)/exp(Phi(r)). Density is baryon mass density rho_b = 1.66e-24 g * n_b, consistent with microphysics, not energy density epsilon/c^2. Curves are sorted in density; zeros are omitted from the logarithmic drawing, but retained in CSV. Panel vertical ranges differ and each spans approximately nine decades below its peak; weaker contributions can lie below the drawing range. Dotted vertical lines mark the first core cell density (mesh approximation). PBF core includes neutrons and protons together; modified/direct Urca include the implemented lepton branches.

| Zone | Start [yr] | End [yr] | Largest neutrino luminosity |
|---|---:|---:|---|
| 1 | 1 | 231.286 | modified_urca |
| 2 | 231.286 | 31978.3 | brems_nn |
| 3 | 31978.3 | 1.07183e+06 | pbf_core |

| Snapshot | Time [yr] | Leading neutrino fraction | Total Lnu_inf [erg/s] | Lgamma_inf [erg/s] |
|---|---:|---:|---:|---:|
| A | 15.258 | 49.362% (modified_urca) | 2.38405e+38 | 7.60857e+34 |
| B | 2750.36 | 60.975% (brems_nn) | 2.7994e+35 | 1.44425e+34 |
| C | 185844 | 99.906% (pbf_core) | 1.54128e+32 | 3.32242e+32 |

Last transition to photon dominance: approximately 135605 yr.

Independent integration of all three local emissivity profiles reproduces the recorded per-process neutrino luminosities to rtol=1e-12. No microphysics or evolution settings were changed for this diagnostic.
