import numpy as np, pandas as pd
from pathlib import Path
b=pd.read_csv("bands.csv"); t=b.t.values
ages=[3e2,1e3,3e3,1e4,3e4,1e5,3e5]
peak={27:"BEEHS 0.39",28:"EEHO 0.49",29:"EEHOr 0.17",30:"SYHHP 0.88",31:"T 0.88",32:"TTav 0.55",33:"TToa 0.62",12:"HGA12 deep 1.08",13:"Baldo 5.39",14:"Elgaroy 1.31"}
rows=[]
for rid,lab in [("D_BSk26_2.10_pstrong_nhigh_fe","26 AO 0.82 (current cold ref)")]+[(f"E_BSk26_2.10_pstrong_n{k}_fe",f"{k} {v}") for k,v in peak.items()]:
    c=np.loadtxt(next((Path("runs")/rid).rglob("cooling_curve.csv")),delimiter=",",skiprows=1)
    rows.append([lab]+[np.log10(np.interp(np.log10(a),np.log10(c[:,0]),c[:,1])) if a<=c[:,0].max() else np.nan for a in ages])
df=pd.DataFrame(rows,columns=["n-triplet (peak Tc, 1e9 K)"]+[f"{a:.0e}" for a in ages])
print(df.round(2).to_string(index=False))
print("previous Fe cold edge          ", np.round([np.interp(np.log10(a),np.log10(t),b.minimal_fe_lo) for a in ages],2))
