import numpy as np, pandas as pd, pickle
C = pickle.load(open("curves.pkl","rb")); b = pd.read_csv("bands.csv"); t = b.t.values
rng = (t >= 3e2) & (t <= 2e6)
def score(edge, sign, pool):
    res=[]
    for k,v in C.items():
        if not pool(v): continue
        e, y = b[edge].values, v["y"]
        ok = rng & (e > 30.0)
        d = sign*(e[ok]-y[ok])   # >=0 distance from edge, in dex
        res.append((k, d.max(), np.sqrt((d**2).mean())))
    return sorted(res, key=lambda r: r[2])[:5]
print("HOT reference vs minimal_all upper edge (max dev, rms dev, dex):")
for r in score("minimal_all_hi", +1, lambda v: not v["du"]): print("  %-40s %.2f %.2f" % r)
print("COLD (minimal) reference vs minimal_all lower edge:")
for r in score("minimal_all_lo", -1, lambda v: not v["du"]): print("  %-40s %.2f %.2f" % r)
print("COLD (minimal, Fe only) vs minimal_fe lower edge:")
for r in score("minimal_fe_lo", -1, lambda v: not v["du"] and v["env"]=="fe"): print("  %-40s %.2f %.2f" % r)
