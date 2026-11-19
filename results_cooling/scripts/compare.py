import numpy as np, pandas as pd
b = pd.read_csv("bands.csv"); t = b.t.values
s = pd.read_csv("/home/claude/ns-thermal-catalogue/data/current_plot_sample.csv")
s = s[s.age_basis=="independent"]
def verdict(r, band):
    alo = r.age_yr_lo if np.isfinite(r.age_yr_lo) else r.display_age_yr
    ahi = r.age_yr_hi if np.isfinite(r.age_yr_hi) else r.display_age_yr
    m = (t >= alo*0.999) & (t <= ahi*1.001)
    if not m.any(): m = np.abs(np.log(t/r.display_age_yr)) == np.abs(np.log(t/r.display_age_yr)).min()
    Lhi = np.log10(r.L_inf_erg_s if r.luminosity_upper_limit or not np.isfinite(r.L_inf_erg_s_hi) else r.L_inf_erg_s_hi)
    Llo = -np.inf if r.luminosity_upper_limit else np.log10(r.L_inf_erg_s_lo if np.isfinite(r.L_inf_erg_s_lo) else r.L_inf_erg_s)
    lo, hi = b[band+"_lo"].values[m], b[band+"_hi"].values[m]
    if (Lhi < lo).all(): return f"BELOW by >= {np.min(lo-Lhi):.2f} dex"
    if (Llo > hi).all(): return f"ABOVE by >= {np.min(Llo-hi):.2f} dex"
    return "inside"
rows=[]
for r in s.itertuples():
    rows.append((r.name, f"{r.age_yr_lo:.3g}-{r.age_yr_hi:.3g}", "UL" if r.luminosity_upper_limit else "", verdict(r,"minimal_fe"), verdict(r,"minimal_all")))
print(pd.DataFrame(rows, columns=["source","age","","vs minimal Fe","vs minimal Fe+accreted"]).to_string(index=False))
