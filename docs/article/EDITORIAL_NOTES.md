# Editorial notes — first discussion draft, 16 November 2026

This is a prose first draft, not a submission-ready review. Preliminary matched-star numerical experiments are now included; no source exclusion is claimed. Author list and affiliations are deliberately unassigned.

## Priorities for the next revision

1. **PBF:** decide the recommended response (vector suppression alone versus anomalous axial vertices), with an equation-level comparison using identical gap/angular conventions. Distinguish published response corrections from the code's retained approximation. Do not interpret the current default as a recommendation.
2. **Modified Urca:** maintain separate labels for the 1979 framework, Yakovlev–Levenfish 1995, Yakovlev et al. 2001, Bottaro et al. 2024, and Shternin et al. 2018. Audit the latter two against the final published versions before quoting numerical enhancement factors. Alleged errors found in earlier project discussions are not asserted as established literature errata here.
3. **Bremsstrahlung:** compare raw interaction rates and rates with any historical short-range factors; record flavour counting explicitly. Avoid assuming independent multiplicative corrections.
4. **Envelope:** add exact provenance and validity ranges for every implemented Fe/light-element fit, including the 2003 variant retained in the code. Extend the discussion of diffusive nuclear burning with primary references before submission.
5. **Transport:** complete an equation-level comparison of the simplified code against coupled electron–muon transport. Verify the exact origin/version of the degenerate crust routine. Expand on neutron entrainment, collective modes and pasta/impurity uncertainties where relevant, with primary references.
6. **EOS:** use definitions of density-of-states masses appropriate to each EOS; check BSk publication errata and table versions. Do not equate Dirac and Landau masses.
7. **Observations:** construct a frozen, dated table with primary spectral and age references. The published Viganò (2013), Potekhin (2020), Marino (2024), and Cas A papers serve as an initial evidence map, not a newly homogenised catalogue. Keep contradictory age/atmosphere solutions separate. Exclude magnetars/high-B objects from the main B=0 sample and justify any CCO inclusion.
8. **Completeness:** the selected literature includes verified papers through 2025. This is not a systematic search of all 2026 publications. Add recent competing approaches, primary observations, and relevant corrections before claiming an up-to-date comprehensive review.

## Numerical figures and further work

- Normal-state Q(rho) and ratios to an explicitly identified Y01 reference, same EOS/composition/masses.
- Temperature-dependent heat capacity and emissivity for selected gap models; PBF response changed independently of the gap.
- Ts–Tb relations at common gravity and base density, parameterised by light-element column.
- Controlled cooling comparisons for matched stars, including integrated neutrino-process luminosities.
- Final source comparison retaining age, luminosity and atmospheric alternatives.

## Bibliography checks

39 cited entries. Most journal metadata were retrieved from Crossref and inspected for title agreement; broad search results returning a different paper were rejected. Older A&A entries without DOI use publisher/archive identifiers. arXiv/primary journal pages were checked for the main recent claims. This does not amount to a fresh line-by-line verification of every equation in all 39 papers. The source map in Appendix A also draws on the existing ns_cooling README audit.

## Editorial choices

- Minimal derivation: only the redshift conventions/global balance and Urca threshold are written explicitly.
- Reference recommendations are labelled as our assessment, not a literature consensus.
- Code-specific bug history stays out of the main scientific narrative; transferable lessons are retained.
- The abstract and conclusions are deliberately provisional until numerical and observational comparisons are complete.

## Incorporated on 19 November 2026

- Five-EOS reference cooling at 1.4 solar masses with common microphysics.
- Consolidated BSk25 row 290 -> 297 interface and BSk26 row-276 omission;
  original tables unchanged; APR Maxwell jump retained.
- Twenty one-channel gap-amplitude runs for BSk24/APR, and ratios to each reference.
- BSk24 neutrino-only dominance shading and actual-profile emissivities at three epochs.
- Exact reproduction of preceding reference tracks and local/global luminosity checks.

The experiments do not establish spatial convergence, resolve APR crust composition,
or validate the retained PBF response. Density support/shape variations remain to do.
