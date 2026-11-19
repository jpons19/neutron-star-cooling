import csv, json, numpy as np, pandas as pd
from pathlib import Path
plan = pd.read_csv("plan.csv")
log = {json.loads(l)["id"]: json.loads(l) for l in open("runlog.jsonl")}
ages = [3e2, 1e3, 3e3, 1e4, 3e4, 1e5, 3e5, 1e6]
rows = []
for r in plan.itertuples():
    d = Path("runs") / r.id
    f = list(d.rglob("cooling_curve.csv"))
    if not f: continue
    c = np.loadtxt(f[0], delimiter=",", skiprows=1)
    t, L = c[:, 0], c[:, 1]
    rec = dict(id=r.id, block=r.block, eos=r.eos, mass=r.mass, p=r.p, n=r.n, env=r.env,
               t_end=t.max(), sec=log.get(r.id, {}).get("seconds"))
    for a in ages:
        rec[f"logL_{a:.0e}"] = np.log10(np.interp(np.log10(a), np.log10(t), L)) if a <= t.max() else np.nan
    txt = (Path("runs") / (r.id + ".log")).read_text()
    rec["warn"] = "unresolved" in txt.lower() or "warning" in txt.lower()
    rows.append(rec)
df = pd.DataFrame(rows); df.to_csv("summary.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
cols = ["id"] + [c for c in df.columns if c.startswith("logL")] + ["t_end", "warn"]
print(df[cols].round(2).to_string(index=False))
