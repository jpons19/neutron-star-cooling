"""Run plan: 48 runs in three blocks. Writes plan.csv."""
import csv
P = {"off": (0, 8), "weak": (1, 17), "strong": (1, 8)}      # core proton 1S0: off / Ho15 AO / HGA12 (~CCDK, code default)
N = {"off": (0, 12), "low": (1, 27), "high": (1, 26)}       # core neutron 3P2: off / Ho15 BEEHS / Ho15 AO
rows = []
def add(block, eos, m, p, n, env, crust=7):
    rows.append(dict(id=f"{block}_{eos}_{m:.2f}_p{p}_n{n}_{env}", block=block, eos=eos, mass=m,
                     p=p, n=n, env=env, crust=crust))
# Block A: gaps x envelope, BSk24 1.4 Msun (no direct Urca)
for p in P:
    for n in N:
        add("A", "BSk24", 1.4, p, n, "fe")
for p in ("off", "strong"):
    for n in ("off", "high"):
        add("A", "BSk24", 1.4, p, n, "accreted")
rows.append(dict(id="A_BSk24_1.40_baseline_7-12-8_fe", block="A", eos="BSk24", mass=1.4, p="strong", n="ref12", env="fe", crust=7))
# Block B: gaps vs active direct Urca, BSk22 1.4 Msun
for p in ("off", "strong"):
    for n in ("off", "high"):
        add("B", "BSk22", 1.4, p, n, "fe")
# Block C: mass x EOS at the two provisional corners
masses = {"BSk22": (1.1, 1.6, 2.1), "BSk24": (1.2, 1.7, 2.1), "BSk25": (1.2, 1.7, 2.1),
          "BSk26": (1.2, 1.7, 2.1), "APR": (1.2, 1.7, 2.1)}
for eos, ms in masses.items():
    for m in ms:
        add("C", eos, m, "strong", "off", "fe")   # provisional hot corner
        add("C", eos, m, "off", "high", "fe")     # provisional cold corner
with open("plan.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
print(len(rows), "runs")
