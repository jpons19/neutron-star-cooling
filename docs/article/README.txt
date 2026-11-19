NEUTRON-STAR COOLING REVIEW — WORKING DRAFT UPDATED 19 NOVEMBER 2026

OVERLEAF
Upload the ZIP as a new project. Select main.tex as the main document and
pdfLaTeX as compiler. The bibliography uses BibTeX and aa.bst.
The compiled main.pdf is included for immediate reading.

FILES
main.tex              Review with preliminary EOS/gap comparisons, six figures and technical appendices.
references.bib        39 cited bibliographic entries.
aa.cls, aa.bst        A&A class v9.0 and bibliography style, unmodified.
EDITORIAL_NOTES.md     Remaining checks and proposed numerical figures.

FORMAT PROVENANCE
The A&A template files are mirrored by:
https://github.com/bardsoftware/template-AA
Class: aa.cls (2016/01/01 v9.0); style: bibtex/aa.bst.
Original notices are retained. This is an A&A-format working draft, not a
claim of compliance with the latest submission requirements. When preparing
submission, use the then-current official A&A/Overleaf template; main.tex
uses standard A&A commands and natbib citations.

Local build: pdflatex main; bibtex main; pdflatex main; pdflatex main.
The figures/ and data/ directories are included. Keep figures/ beside main.tex.
The numerical experiments are preliminary model comparisons; the systematic
microphysics comparison and observational catalogue remain incomplete.

Validation: 39 unique citation keys, no missing bibliography entries;
14-page updated PDF compiled, with six figures and page layout inspected. The older bundled class can
produce compatibility warnings with newer LaTeX/natbib releases; these do not
indicate duplicated entries in references.bib. Replace the class with the
current official template for the submission version.

UPDATE 19 NOVEMBER 2026
Six figures: five-EOS cooling, gap amplitudes and ratios, neutrino dominance/local
profiles, and EOS pressure/density/chemical-potential diagnostics.
The data/ folder contains reference parameters, run summaries, importable cooling
curves and three emissivity snapshots. The thermal solver is maintained separately.
