"""External M-R checks and safeguards for the new CompOSE packages."""
import hashlib
import json
import numpy as np
import pytest

from eos_table import CompOSETable
from tov import central_pressure_for_mass, integrate_star


@pytest.mark.parametrize("name", ["BSk24", "BSk25", "APR"])
def test_radius_matches_provider_at_14(root, name):
    """Reference: provider eos.mr, radius at 1.4 Msun; tolerance 0.3%."""
    eos = CompOSETable(root / "eos" / name)
    pc = central_pressure_for_mass(eos, 1.4)
    star = integrate_star(eos, pc)
    mr = eos.mass_radius[:np.argmax(eos.mass_radius[:, 1]) + 1]
    assert star.mass_solar == pytest.approx(1.4, abs=2e-6)
    assert star.radius_cm / 1e5 == pytest.approx(np.interp(1.4, mr[:, 1], mr[:, 0]), rel=.003)


def test_apr_maxwell_jump_is_not_smeared(root):
    """Published Maxwell endpoints: nb = 0.204751915 / 0.236917451 fm^-3."""
    eos = CompOSETable(root / "eos" / "APR")
    pt, = eos.transition_pressures
    state = eos.at_pressure(pt * np.array([1 - 1e-9, 1 + 1e-9]))
    assert state.nb_fm3 == pytest.approx([.20475191506138177, .2369174513559696], rel=1e-7)
    assert np.allclose(state.yp, state.ye + state.ymu, atol=1e-8, rtol=0)
    # The structure solver must also see the same jump, not a different interpolant.
    assert eos.energy_density(state.pressure) == pytest.approx(state.rho_energy, rel=1e-12)


def test_default_input_and_apr_jump_face(root):
    from input_model import read_parameters
    from stellar_structure import StructureOptions, build_stellar_model
    cfg = read_parameters(root / "input_bsk24")
    assert cfg["eos"] == "BSk24"
    assert cfg["mass"] == (1.4,)
    assert "central_pressure" not in cfg
    model = build_stellar_model(StructureOptions("APR", central_pressure=1.4775034568e35),
                                root / "eos", cfg)
    pt, = model.eos.transition_pressures
    xt = np.log(pt / model.star.pressure_central)
    assert np.count_nonzero(np.isclose(model.x_faces, xt, atol=1e-13, rtol=0)) == 1


@pytest.mark.parametrize("name", ["BSk25", "APR"])
def test_source_bytes_preserved(root, name):
    folder = root / "eos" / name
    hashes = json.loads((folder / "source.json").read_text())["sha256"]
    for filename, expected in hashes.items():
        assert hashlib.sha256((folder / filename).read_bytes()).hexdigest() == expected


def test_large_unknown_pressure_reversal_is_still_rejected(root, tmp_path):
    """Negative control: copying BSk25 under an unknown name must not relax validation."""
    import shutil
    folder = tmp_path / "unknown"
    shutil.copytree(root / "eos" / "BSk25", folder)
    with pytest.raises(ValueError, match="pressure reversal"):
        CompOSETable(folder)


def test_apr_thermodynamic_tolerance_does_not_hide_core_errors(root, tmp_path):
    """Negative control: the special crust tolerance must not allow a core error."""
    import shutil
    folder = tmp_path / "APR"
    shutil.copytree(root / "eos" / "APR", folder)
    path = folder / "eos.thermo"
    rows = path.read_text().splitlines()
    row = rows[-1].split()
    row[5] = str(float(row[5]) + .001)
    rows[-1] = " ".join(row)
    path.write_text("\n".join(rows) + "\n")
    with pytest.raises(ValueError, match="violated"):
        CompOSETable(folder)
