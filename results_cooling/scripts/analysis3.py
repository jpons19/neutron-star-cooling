import numpy as np, pandas as pd, json
exec(open("collect.py").read())
R={d["id"]:d for d in recs if d["c"] is not None}
def logL(d,a):
    c=d["c"]; 
    return np.log10(np.interp(np.log10(a),np.log10(c[:,0]),c[:,1])) if a<=c[:,0].max() else np.nan
ages=[3e2,1e3,3e3,1e4,3e4,1e5,3e5,1e6]
def row(d): return [d["id"]]+[round(logL(d,a),2) for a in ages]+[f"{d['c'][:,0].max():.3g}"]
cols=["id"]+[f"{a:.0e}" for a in ages]+["t_end"]
pd.set_option("display.width",250); pd.set_option("display.max_rows",200)
COLD="D_BSk26_2.10_pstrong_nhigh_fe"; HOT="C_BSk26_1.70_pstrong_noff_fe"
print("== F: cold edge vs central density (reference first)")
print(pd.DataFrame([row(R[COLD])]+[row(d) for d in R.values() if d["block"]=="F"],columns=cols).to_string(index=False))
print("\n== G: hot edge vs proton gap (references first)")
print(pd.DataFrame([row(R[HOT]),row(R["C_BSk24_1.20_pstrong_noff_fe"]),row(R["C_BSk26_2.10_pstrong_noff_fe"])]+[row(d) for d in R.values() if d["block"]=="G"],columns=cols).to_string(index=False))
print("\n== H/I: direct Urca + accreted")
print(pd.DataFrame([row(d) for d in R.values() if d["block"] in "HI"],columns=cols).to_string(index=False))
print("\n== J/K: references extended / numerical checks")
print(pd.DataFrame([row(d) for d in R.values() if d["block"] in "JK"]+[row(R[COLD]),row(R[HOT])],columns=cols).to_string(index=False))
