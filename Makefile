PYTHON ?= python3
.PHONY: help run quick plots test paper
help:
	@echo 'Targets: run, quick, plots, test, paper (activate .venv first)'
run:
	$(PYTHON) code/cooling_driver.py --no-animation --check-energy --out results/reference
quick:
	$(PYTHON) code/cooling_driver.py --no-animation --final-years 1000 --out results/short
plots:
	$(PYTHON) examples/five_eos/plot.py
	$(PYTHON) examples/gap_scan/plot.py
	$(PYTHON) examples/neutrino_zones/plot.py
	$(PYTHON) examples/eos_tables/plot_pressure.py
	$(PYTHON) examples/eos_tables/plot_mu.py
test:
	$(PYTHON) -m pytest -c code/pytest.ini code/tests -q
paper:
	cd docs/article && pdflatex -interaction=nonstopmode -halt-on-error main.tex
	cd docs/article && bibtex main
	cd docs/article && pdflatex -interaction=nonstopmode -halt-on-error main.tex
	cd docs/article && pdflatex -interaction=nonstopmode -halt-on-error main.tex
