import base64, pathlib
F = pathlib.Path("figures")
def img(name, alt):
    b = base64.b64encode((F/name).read_bytes()).decode()
    return f'<img src="data:image/png;base64,{b}" alt="{alt}">'
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Neutron-star cooling: gap, envelope and mass sweep</title>
<style>
:root {{
  --paper:#ffffff; --ink:#1d2430; --muted:#5b6573; --rule:#d9dee5;
  --cold:#2c5f8f; --hot:#a32a2a; --tint:#f2f5f8;
  --serif: Charter, "Bitstream Charter", "Sitka Text", Cambria, Georgia, serif;
  --sans: "Avenir Next", "Segoe UI", "Helvetica Neue", Arial, sans-serif;
}}
@media (prefers-color-scheme: dark) {{
  :root {{ --paper:#171b21; --ink:#e3e7ec; --muted:#a2acb8; --rule:#323a45; --cold:#8db8e0; --hot:#e58f86; --tint:#1f252d; color-scheme:dark; }}
}}
html {{ background:var(--paper); }}
body {{ margin:0; background:var(--paper); color:var(--ink); font-family:var(--serif); font-size:17.5px; line-height:1.62; }}
main {{ max-width:1080px; margin:0 auto; padding:56px 28px 96px; }}
.prose, h1, h2, h3, .lede, .meta {{ max-width:70ch; }}
h1, h2, h3 {{ font-family:var(--sans); font-weight:600; line-height:1.25; letter-spacing:-0.005em; }}
h1 {{ font-size:2.05rem; margin:0 0 .4rem; }}
h2 {{ font-size:1.32rem; margin:3.2rem 0 .8rem; padding-top:1.1rem; border-top:1px solid var(--rule); }}
h3 {{ font-size:1.05rem; margin:2rem 0 .4rem; }}
.meta {{ font-family:var(--sans); color:var(--muted); font-size:.92rem; margin-bottom:2rem; }}
.lede {{ font-size:1.12rem; }}
p, li {{ max-width:70ch; }}
a {{ color:var(--cold); }}
a:focus-visible {{ outline:2px solid var(--cold); outline-offset:2px; }}
figure {{ margin:2rem 0 2.4rem; }}
figure img {{ display:block; width:100%; height:auto; background:#fff; border:1px solid var(--rule); border-radius:3px; }}
figcaption {{ font-family:var(--sans); font-size:.9rem; color:var(--muted); margin-top:.6rem; max-width:80ch; line-height:1.5; }}
figcaption b {{ color:var(--ink); }}
.scroll {{ overflow-x:auto; margin:1.2rem 0 1.8rem; }}
table {{ border-collapse:collapse; font-family:var(--sans); font-size:.9rem; min-width:560px; }}
th, td {{ padding:.42rem .8rem; border-bottom:1px solid var(--rule); text-align:left; vertical-align:top; }}
th {{ font-weight:600; }}
td.num {{ font-variant-numeric:tabular-nums; text-align:right; }}
tr.below td:last-child {{ color:var(--cold); font-weight:600; }}
.verdict {{ border-left:4px solid var(--cold); background:var(--tint); padding:1rem 1.3rem; margin:1.6rem 0; max-width:70ch; }}
.verdict p {{ margin:.3rem 0; }}
.hot {{ color:var(--hot); font-weight:600; }}
.cold {{ color:var(--cold); font-weight:600; }}
code {{ font-size:.88em; }}
</style>
</head>
<body>
<main>

<h1>Neutron-star cooling: how much do pairing gaps, envelope and mass move the curves?</h1>
<p class="meta">Working report, 19 November 2026. 67 runs of the <code>neutron-star-cooling</code> solver, compared with the <code>ns-thermal-catalogue</code> review values of the same date.</p>

<p class="lede">The five reference cooling curves used in the catalogue differed from each other by up to a factor of ten at 1–30 kyr. This sweep shows that the difference comes mainly from the pairing gaps and the envelope, not from the equation of state. It also gives a minimal-cooling band against which the observed sources can be tested.</p>

<div class="verdict">
<p><b>Main results</b></p>
<p>Without direct Urca, the core neutron-triplet gap is the dominant choice, followed by the core proton gap and the envelope composition. EOS and mass shift the curves by at most about 0.5 dex.</p>
<p>The lower edge of the minimal-cooling band is robust. It is the same within 0.06 dex across 11 published triplet gap models.</p>
<p>Against that band, <span class="cold">PSR J0007+7303</span> is the only source that is clearly too cold: at least 1.1 dex below. Vela Jr and J0205+6449 are marginally below (about 0.2 dex). B1727−47 is below only if its envelope is iron.</p>
</div>

<h2>1. What was run</h2>
<p>All runs use the solver as published: mesh C, initial redshifted temperature 10<sup>10</sup> K, B = 0, the Yakovlev et al. (2001) modified Urca rates and BCF2024 bremsstrahlung. Each run stops when L<sub>γ</sub><sup>∞</sup> falls below 10<sup>30</sup> erg/s. The crust neutron gap is fixed to the default (model 7), because the solver’s own earlier scan showed it changes L by at most 6%.</p>
<p>Direct Urca opens at 1.15 M<sub>☉</sub> for BSk22, 1.60 for BSk24, 1.63 for BSk25 and 1.98 for APR, and never for BSk26, whose maximum mass is 2.17 M<sub>☉</sub>. Throughout, “minimal cooling” means every run below its EOS threshold.</p>

<div class="scroll"><table>
<thead><tr><th>Block</th><th>Runs</th><th>What varies</th><th>What is fixed</th></tr></thead>
<tbody>
<tr><td>A</td><td class="num">14</td><td>Proton gap (off / weak AO / strong HGA12≈CCDK) × triplet gap (off / low BEEHS / high AO); envelope Fe or accreted for the four corners; one baseline with the original defaults</td><td>BSk24, 1.4 M<sub>☉</sub></td></tr>
<tr><td>B</td><td class="num">4</td><td>Proton and triplet gaps in a star with active direct Urca</td><td>BSk22, 1.4 M<sub>☉</sub>, Fe</td></tr>
<tr><td>C</td><td class="num">30</td><td>All 5 EOS × 3 masses chosen around each threshold, at a provisional hot and cold gap setting</td><td>Fe envelope</td></tr>
<tr><td>D</td><td class="num">9</td><td>Follow-ups: the corrected cold setting in the heaviest stars without direct Urca; accreted versions of the extremes; BSk24 at 1.55 and 1.65 M<sub>☉</sub> on either side of its threshold</td><td>—</td></tr>
<tr><td>E</td><td class="num">10</td><td>Ten more triplet gap models, peak T<sub>c</sub> 0.17–5.4 × 10<sup>9</sup> K</td><td>BSk26, 2.1 M<sub>☉</sub>, strong proton gap, Fe</td></tr>
</tbody></table></div>
<p>Each run took 19–51 s on one core, about 35 minutes in total. Every run closed its energy balance; the largest error was 1.5% against a 2% tolerance, and the median was 0.02%. Per-run details are in <code>tables/run_qc.csv</code>.</p>

<h2>2. Pairing gaps and envelope in a single star</h2>
<figure>
{img("fig1_gaps_envelope.png","Cooling curves for BSk24 at 1.4 solar masses: nine gap combinations with an iron envelope, and four combinations compared between iron and accreted envelopes")}
<figcaption><b>Figure 1.</b> BSk24, 1.4 M<sub>☉</sub>, no direct Urca. (a) All nine combinations of proton gap (colour) and neutron-triplet gap (line style), Fe envelope. (b) The four extreme combinations with Fe (solid) and accreted (dashed) envelopes.</figcaption>
</figure>
<p><b>The proton gap sets the overall level.</b> A strong proton gap suppresses modified Urca throughout the core and raises L by about a factor of 4 at 10<sup>4</sup> yr (log L 33.93 compared with 33.33 with no proton gap). The weak AO proton gap is close to having no gap at all.</p>
<p><b>The triplet gap sets the drops.</b> Each sharp fall in panel (a) is the onset of pair-breaking emission, when the core temperature falls below the critical temperature of the triplet gap. With the high-T<sub>c</sub> AO gap this happens before 300 yr. With the low BEEHS gap it happens near 10<sup>3</sup> yr without proton pairing, but only at 1–3 × 10<sup>4</sup> yr with a strong proton gap. That interaction is why gap channels cannot be scanned one at a time. Once their drop has happened, all combinations with a triplet gap lie within about 0.3 dex of each other (log L 32.4–32.7 at 3 × 10<sup>4</sup> yr).</p>
<p>This also explains the original five reference curves. With the default deep triplet gap, the critical temperature reached inside the star depends on the central density. It is 0.41 × 10<sup>9</sup> K in BSk24 but 0.92 × 10<sup>9</sup> K in APR, so the drop happens at about 3 × 10<sup>4</sup> yr in one and about 300 yr in the other. The apparent EOS dependence was really a gap-placement effect.</p>
<p><b>The envelope effect reverses with age</b> (panel b). An accreted (light-element) envelope has a higher surface temperature for the same base temperature. It is therefore 0.5–0.8 dex brighter while the star is cooled mainly by neutrinos, but it then cools faster once photons dominate. The crossover is near 10<sup>5</sup> yr for weakly paired stars and near 2 × 10<sup>4</sup> yr for strongly paired ones, whose heat capacity is small. The extreme case, strong proton plus high triplet gap with an accreted envelope, falls below 10<sup>30</sup> erg/s by 80 kyr. The run with the original default gaps reproduces the existing BSk24 reference curve within 0.07 dex.</p>

<h2>3. Mass and equation of state</h2>
<figure>
{img("fig2_mass_eos.png","Cooling curves for five equations of state at three masses each, for a hot and a cold gap setting")}
<figcaption><b>Figure 2.</b> All five EOS at three masses each (thin lines: lighter star, thick lines: heavier). Solid lines: no direct Urca. Dashed lines: direct Urca active. (a) Strong proton gap, no triplet gap. (b) No proton gap, high (AO) triplet gap. Fe envelope.</figcaption>
</figure>
<p><b>Without direct Urca, EOS and mass matter little</b> (solid lines). In the cold setting, every star without direct Urca lies within about 0.1 dex up to 10<sup>4</sup> yr. In the hot setting the two heaviest stars without direct Urca, BSk26 at 2.1 M<sub>☉</sub> and APR at 1.7 M<sub>☉</sub>, form a second family about 0.4 dex lower. The strong proton gap only extends to k<sub>F</sub> ≈ 1.3 fm<sup>−1</sup>, so their dense centres keep unsuppressed modified Urca.</p>
<p><b>With direct Urca, “hot” and “cold” swap.</b> The proton gap does not reach the dense centre where direct Urca operates, but the high triplet gap does, and suppresses it there. So in heavy stars the nominally hot setting (dashed lines in a) is the colder of the two. For example, BSk24 at 1.7 M<sub>☉</sub> has log L 30.99 at 10<sup>4</sup> yr in the hot setting and 31.90 in the cold one. With no gaps at all, BSk22 at 1.4 M<sub>☉</sub> falls below 10<sup>30</sup> erg/s by 22 kyr.</p>
<p>The transition is sharp. BSk24 gives log L 32.70 at 1.55 M<sub>☉</sub> and 31.5–32.0 at 1.65 M<sub>☉</sub>, a change of about 1 dex for 0.1 M<sub>☉</sub>. In practice there is no lower floor once direct Urca is allowed: some heavy, weakly paired star can always explain a cold source. The physically informative comparison is therefore with the minimal-cooling band.</p>

<h2>4. How robust is the cold edge?</h2>
<figure>
{img("fig3_triplet_scan.png","Eleven neutron-triplet gap models compared in the same star, together with the hot reference without a triplet gap")}
<figcaption><b>Figure 3.</b> Eleven neutron-triplet gap models in the coldest star without direct Urca (BSk26, 2.1 M<sub>☉</sub>, strong proton gap, Fe envelope). Thick blue: AO, the model used for the cold edge. Red: the hot reference, which has no triplet gap.</figcaption>
</figure>
<p>The cold edge comes from one gap model, so it was tested against ten alternatives. AO stays the coldest from 3 × 10<sup>3</sup> yr onwards. Before that, HGA12-deep is lower by only 0.06 dex. So the cold edge is essentially independent of which published triplet gap is assumed.</p>
<p>A larger gap does not give a colder star. The Baldo model (peak T<sub>c</sub> 5.4 × 10<sup>9</sup> K) pairs the whole core so early that the pair-breaking emission is over before the ages that matter, and then suppressed. The coldest models are those whose pair-breaking emission is strongest at the relevant ages, here AO and TToa.</p>
<p>At the other extreme, EEHOr (peak T<sub>c</sub> 0.17 × 10<sup>9</sup> K) is barely active and stays near the hot reference until about 10<sup>5</sup> yr. Most of the width of the minimal-cooling band therefore comes from a single microphysical uncertainty: the strength and density profile of the core neutron-triplet gap.</p>

<h2>5. The bands compared with the sources</h2>
<figure>
{img("fig4_bands_vs_sources.png","Minimal-cooling and full bands with the hot and cold reference curves, and the independent-age sources from the catalogue")}
<figcaption><b>Figure 4.</b> Dark blue: minimal-cooling band with Fe envelopes. Light blue: the same band including accreted envelopes. Grey: all 67 runs including direct Urca. Red lines: hot reference (solid Fe, dashed accreted). Blue lines: cold reference (solid Fe, dashed accreted). Points: the 18 independent-age sources with the catalogue’s current adopted or provisional values. The hatched region below 10<sup>30</sup> erg/s was not computed.</figcaption>
</figure>
<p>A source counts as below the band only if its whole error box lies below the band at every age in its range. Upper limits are treated as boxes extending to zero luminosity.</p>
<div class="scroll"><table>
<thead><tr><th>Source</th><th>Age range (yr)</th><th>Against minimal cooling, Fe</th><th>Against minimal cooling, Fe + accreted</th></tr></thead>
<tbody>
<tr class="below"><td>PSR J0007+7303 (upper limit)</td><td>9–13 × 10<sup>3</sup></td><td>below by ≥ 1.08 dex</td><td>below by ≥ 1.08 dex</td></tr>
<tr class="below"><td>PSR B1727−47 (upper limit)</td><td>40–80 × 10<sup>3</sup></td><td>below by ≥ 0.31 dex</td><td>inside</td></tr>
<tr class="below"><td>Vela Jr (CXOU J085201.4−461753)</td><td>1.6–5.1 × 10<sup>3</sup></td><td>below by ≥ 0.19 dex</td><td>below by ≥ 0.19 dex</td></tr>
<tr class="below"><td>PSR J0205+6449 (3C 58)</td><td>0.8–7 × 10<sup>3</sup></td><td>below by ≥ 0.18 dex</td><td>below by ≥ 0.18 dex</td></tr>
<tr><td>PSR B2334+61 (current box)</td><td>6.9–41 × 10<sup>3</sup></td><td>inside</td><td>inside</td></tr>
<tr><td>Cas A, Crab (upper limit), IC 443, Vela, S147, Monogem, B1951+32 (upper limit), J0357, five XINS</td><td>—</td><td>inside</td><td>inside</td></tr>
<tr><td>PSR B0950+08</td><td>0.6–7.6 × 10<sup>6</sup></td><td colspan="2">not assessable: below the 10<sup>30</sup> erg/s stop</td></tr>
</tbody></table></div>
<p><b>J0007+7303 is the robust case.</b> Even if its luminosity ceiling were 2–3 times higher, which is plausible given the spectral model, it would still lie at least about 0.6 dex below the band. That requires enhanced cooling, for example direct Urca in a heavier star.</p>
<p><b>Vela Jr and J0205+6449 are marginal.</b> They are about 0.2 dex below, which is within their distance and emitting-component systematics. For J0205 the lower part of the box comes from a small-area hot-spot fit, which is not a measurement of cooling luminosity.</p>
<p><b>B1727−47 depends on the envelope.</b> With an accreted envelope, the strongly paired cold edge drops fast enough after 3 × 10<sup>4</sup> yr to reach its upper limit.</p>
<p><b>B2334+61 depends on the distance branch.</b> It is inside the band with the current hybrid box, which pairs the near-distance age with the far-distance luminosity. On the self-consistent near-distance branch (about 7.7 kyr) it would be 0.8–1.3 dex below: 0.8 dex with the whole-surface atmosphere fit that is valid near 1 kpc, more with the hot-spot interpretation. On the far branch its age is unknown but probably older, and it would be inside. This is the first source to discuss next.</p>
<p>No source is above the band. Cas A is inside it, but at ages where several triplet gap models produce their pair-breaking drop (Figure 3), so it is the source most sensitive to that choice. S147, the most luminous source near 30 kyr, sits well inside the band, about 0.8 dex below the Fe hot edge.</p>

<h2>6. Reference models</h2>
<div class="scroll"><table>
<thead><tr><th>Reference</th><th>Definition</th><th>How closely it follows the band edge</th></tr></thead>
<tbody>
<tr><td class="cold">Cold (minimal cooling)</td><td>Strong proton gap (HGA12≈CCDK) + AO triplet gap; BSk26, 2.1 M<sub>☉</sub>; Fe envelope. For the light-element case, the accreted version is colder after about 2 × 10<sup>4</sup> yr.</td><td>Within 0.18 dex of the Fe lower edge at all ages (rms 0.06 dex); stable across 11 triplet models</td></tr>
<tr><td class="hot">Hot (minimal cooling)</td><td>Strong proton gap, no triplet gap; BSk26, 1.7 M<sub>☉</sub>. Accreted envelope up to about 1.5 × 10<sup>5</sup> yr, Fe afterwards.</td><td>Within 0.49 dex as a single Fe run (rms 0.38). Only the composite follows the hot edge at all ages.</td></tr>
</tbody></table></div>
<p>The two references differ essentially in one choice: whether the core neutrons pair into a triplet state with a gap large enough to trigger pair-breaking emission at the relevant ages. Neither was tuned to the observed sources.</p>

<h2>7. Limitations</h2>
<ul>
<li>Only three proton gap options were sampled. The triplet gap was tested broadly (11 models), but at one mass and with one proton gap.</li>
<li>The magnetic field is zero. Only fully iron and fully accreted envelopes were run, with no partially accreted cases.</li>
<li>The solver’s documented approximations remain: the pair-breaking response, the APR crust composition, and the BSk25 and BSk26 table rows omitted by the reader. Spatial convergence was not re-tested; only mesh C was used.</li>
<li>Comparisons below 10<sup>30</sup> erg/s, after about 1 Myr, are not possible with these runs.</li>
<li>The source boxes are the catalogue’s current working values. Their own open issues (hot-spot versus whole-surface components, distance branches) are discussed in the catalogue audit and affect the verdicts above.</li>
</ul>

<h2>Contents of this folder</h2>
<ul>
<li><code>report.html</code>: this report, with the figures embedded.</li>
<li><code>figures/</code>: the four figures as separate PNG files.</li>
<li><code>tables/run_table.csv</code>: one row per run, giving its settings, direct-Urca flag, log L at eight ages and final age.</li>
<li><code>tables/cooling_sweep_curves.csv</code>: all 67 cooling curves, in the same format as <code>cooling_five_eos.csv</code> in the catalogue.</li>
<li><code>tables/bands.csv</code>: the upper and lower edges of the three bands on a common age grid.</li>
<li><code>tables/run_qc.csv</code>: runtime and energy-closure error per run.</li>
<li><code>tables/source_verdicts.txt</code>: the source comparison.</li>
<li><code>tables/plan.csv</code>: the run plan.</li>
<li><code>runs_inputs/</code>: the 67 solver input files.</li>
<li><code>scripts/</code>: plan, runner, analysis and plotting scripts. These expect the solver repository next to the sweep folder.</li>
</ul>
</main>
</body>
</html>
"""
pathlib.Path("report.html").write_text(html, encoding="utf-8")
print(len(html)//1024, "kB")
