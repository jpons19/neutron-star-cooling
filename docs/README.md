# Documentation

| File | Purpose |
|---|---|
| [USER_GUIDE.md](USER_GUIDE.md) | Installation, configuration and output conventions |
| [EOS_NOTES.md](EOS_NOTES.md) | EOS provenance, adopted pressure omissions and unresolved APR composition |
| [REPRODUCIBILITY.md](REPRODUCIBILITY.md) | Reference runs, figures and CSV conventions |
| [VALIDATION.md](VALIDATION.md) | Checks on the packaged layout |
| [IMPLEMENTATION_HISTORY.txt](IMPLEMENTATION_HISTORY.txt) | Historical solver decisions and literature audit; original paths may be obsolete |
| [article/main.tex](article/main.tex) | Working manuscript source |
| [article/main.pdf](article/main.pdf) | Compiled 14-page manuscript with six figures |

Compile the article in `docs/article/` with pdfLaTeX and BibTeX, or upload that folder as a separate Overleaf project. Select `main.tex` as the main file. Keep `figures/` beside it. The supplied A&A class and bibliography style retain their original notices.

```bash
cd docs/article
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

The included PDF was compiled and visually inspected. A local TeX distribution is optional for using the cooling solver or regenerating Python figures.
