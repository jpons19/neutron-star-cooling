import numpy as np, pandas as pd
from pathlib import Path
plan = pd.read_csv("plan.csv")
DU = {"BSk22":1.153,"BSk24":1.598,"BSk25":1.626,"BSk26":9,"APR":1.982}
tg = np.logspace(np.log10(200), np.log10(3e6), 300)
curves = {}
for r in plan.itertuples():
    c = np.loadtxt(next((Path("runs")/r.id).rglob("cooling_curve.csv")), delimiter=",", skiprows=1)
    lt, lL = np.log10(c[:,0]), np.log10(c[:,1])
    y = np.interp(np.log10(tg), lt, lL, right=np.nan)
    y[tg > c[:,0].max()] = 29.0   # below the stop criterion: treat as < 1e30 (floor for band)
    curves[r.id] = dict(y=y, du=r.mass > DU[r.eos], env=r.env, eos=r.eos, m=r.mass, p=r.p, n=r.n)
def band(sel):
    ids=[k for k,v in curves.items() if sel(v)]; Y=np.array([curves[k]["y"] for k in ids])
    return ids, Y.max(0), Y.min(0), [ids[i] for i in Y.argmax(0)], [ids[i] for i in Y.argmin(0)]
sets = {"minimal_fe": lambda v: not v["du"] and v["env"]=="fe",
        "minimal_all": lambda v: not v["du"],
        "full": lambda v: True}
out = {"t": tg}
for name, sel in sets.items():
    ids, hi, lo, arghi, arglo = band(sel); out[name+"_hi"]=hi; out[name+"_lo"]=lo
    print(f"\n== {name}: {len(ids)} runs")
    for t in [3e2,1e3,3e3,1e4,3e4,1e5,3e5,1e6]:
        i=np.argmin(abs(tg-t))
        print(f" t={t:8.0e}  hi {hi[i]:.2f} [{arghi[i]}]   lo {lo[i]:.2f} [{arglo[i]}]")
pd.DataFrame(out).to_csv("bands.csv", index=False)
import pickle; pickle.dump(curves, open("curves.pkl","wb"))
