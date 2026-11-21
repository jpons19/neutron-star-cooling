"""Tests of the output area (decision D-028).

Run from the repository root when this area changes, or on request:
`python -m pytest -c code/pytest.ini code/tests/test_output.py -q`

Code covered: cooling_driver.py, cooling_animation.py, compare_emissivities.py, neutrino_dominance.py.
Every test states a hypothesis, a reference and a criterion, in the style of the validation steps of the GitHub code.
"""

import cooling_animation as ca
import matplotlib.pyplot as plt
import pytest
import numpy as np
import subprocess
import sys
from cooling import CoolingRun


# ------------------------------------------------------------------ command line
def run_driver(root, *args):
    """Run the driver; the legacy reference star (input_bsk26) is used unless --input is given."""
    given = "--input" in map(str, args)
    default = [] if given else ["--input", str(root / "input_bsk26")]
    return subprocess.run(
        [sys.executable, str(root / "cooling_driver.py"), "--no-animation", *default, *map(str, args)],
        capture_output=True, text=True, cwd=root,
    )  # fmt: skip


def test_driver_writes_all_outputs(root, tmp_path):
    """Hypothesis: one short run of the driver writes every output file (smoke test).
    Reference: the list of output files in the README.
    Criterion: all files are non-empty, the energy summary is printed, and a single star uses the
        flat layout.
    """
    result = run_driver(root, "--final-years", 30, "--out", tmp_path / "o", "--check-energy")
    assert result.returncode == 0, result.stderr
    for name in (
        "cooling_curve.csv",
        "temperature_profiles.csv",
        "profile_times.csv",
        "time_steps.csv",
        "energy_budget.csv",
    ):
        assert (tmp_path / "o" / name).stat().st_size > 0
    assert "Energy balance" in result.stdout and "Accepted steps" in result.stdout
    assert not (tmp_path / "o" / "cooling_curves.csv").exists()  # one star: the flat layout


@pytest.fixture(scope="module")
def entries():
    """Synthetic histories with different time grids, end times and cell counts.

    Temperatures use the CoolingRun units (T_inf / 1e8 K). Unsorted radii
    exercise the animation's ordering without building stars or evolving them.
    """
    def history(times, radius):
        times = np.asarray(times, dtype=float)
        radius = np.asarray(radius, dtype=float)
        profiles = {
            i: (8.0 + radius / 12.0) / (1.0 + t) ** 0.2
            for i, t in enumerate(times)
        }
        run = CoolingRun(
            times_years=times[1:],
            luminosity_erg_s=1e35 / (1.0 + times[1:]) ** 0.6,
            profiles=profiles,
            completed_steps=len(times) - 1,
            stop_reason="final_time",
            step_times_years=times,
            relative_changes=np.array([
                np.max(np.abs(profiles[i] / profiles[i - 1] - 1.0))
                for i in range(1, len(times))
            ]),
            rejected_steps=0,
        )
        return run, radius

    return [
        ("table", *history([0, 0.1, 2, 30, 1000], [11.8, 7.0, 2.0])),
        ("1.40 Msun", *history([0, 0.2, 5, 100], [12.0, 8.0, 4.0, 1.0])),
    ]


def test_the_figure_shows_every_star(entries):
    """Hypothesis: the figure shows every star, and its complete curve at the last frame (smoke test).
    Reference: the structure of the figure: legend, frame titles and curves.
    Criterion: legend labels, frame titles and the length of every line.
    """
    fig, animation = ca.cooling_animation(entries, interval_ms=1, frames=30)
    fig.canvas.draw()  # starts the animation, as the window does
    draw = fig._cooling_controls[3]
    ax_l, ax_t = fig.axes[0], fig.axes[1]
    assert [t.get_text() for t in ax_l.get_legend().get_texts()] == ["table", "1.40 Msun"]
    draw(0)
    assert "Frame 1/30" in fig._suptitle.get_text()
    draw(29)
    assert "Frame 30/30" in fig._suptitle.get_text() and "Final" in fig._suptitle.get_text()
    profiles = [line for line in ax_t.lines]
    assert [len(p.get_xdata()) for p in profiles] == [len(e[2]) for e in entries]
    assert ax_t.get_xlabel() == "Radius [km]"
    for profile, (_, run, radius) in zip(profiles, entries):
        order = np.argsort(radius)
        np.testing.assert_allclose(profile.get_xdata(), radius[order])
        np.testing.assert_allclose(profile.get_ydata(), np.log10(run.profiles[run.completed_steps][order] * 1e8))
    curves = [line for line in ax_l.lines if line.get_linestyle() == "-"]
    assert [len(c.get_xdata()) for c in curves] == [
        len(e[1].times_years) for e in entries
    ]  # complete at the last frame
    plt.close(fig)
