import numpy as np, pandas as pd, pickle, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
b = pd.read_csv("bands.csv"); t=b.t; C = pickle.load(open("curves.pkl","rb"))
s = pd.read_csv("/home/claude/ns-thermal-catalogue/data/current_plot_sample.csv"); s=s[s.age_basis=="independent"]
fig, ax = plt.subplots(figsize=(10,6.6))
def fb(lo,hi,**k): ax.fill_between(t,10**np.maximum(b[lo],30),10**np.maximum(b[hi],30),**k)
fb("full_lo","full_hi",color="0.88",label="All 164 runs (incl. direct Urca)")
fb("minimal_all_lo","minimal_all_hi",color="#9ecae1",alpha=.6,label="Minimal cooling, Fe + accreted")
fb("minimal_fe_lo","minimal_fe_hi",color="#3182bd",alpha=.45,label="Minimal cooling, Fe only")
for k,st,lab in [("C_BSk26_1.70_pstrong_noff_fe","-","Hot ref: strong p, no n-triplet (BSk26 1.7, Fe)"),
                 ("D_BSk26_1.70_pstrong_noff_accreted","--","  same, accreted envelope"),
                 ("D_BSk26_2.10_pstrong_nhigh_fe","-","Cold ref: strong p, high n-triplet (BSk26 2.1, Fe)"),
                 ("A_BSk24_1.40_pstrong_nhigh_accreted","--","  strong p, high n-triplet, accreted (BSk24 1.4)")]:
    y=C[k]["y"]; m=y>29.5
    ax.plot(t[m],10**y[m],st,color="#b2182b" if "noff" in k else "#2166ac",lw=1.8,label=lab)
for r in s.itertuples():
    x, y = r.display_age_yr, r.L_inf_erg_s
    xe = [[x-r.age_yr_lo],[r.age_yr_hi-x]] if np.isfinite(r.age_yr_lo) else None
    if r.luminosity_upper_limit:
        ax.errorbar(x,y,xerr=xe,yerr=[[0.5*y],[0]],uplims=True,fmt="v",color="k",ms=5,lw=.9,capsize=2)
    else:
        ax.errorbar(x,y,xerr=xe,yerr=[[y-r.L_inf_erg_s_lo],[r.L_inf_erg_s_hi-y]],fmt="o",color="k",ms=4,lw=.9,capsize=2)
    nm=r.name.replace("PSR ","").replace("CXOU J085201.4-461753","Vela Jr").replace("CXOU J232327.8+584842","Cas A").replace("CXOU J061705.3+222127","IC 443")
    ax.annotate(nm,(x,y),xytext=(4,4),textcoords="offset points",fontsize=7)
ax.axhspan(1e28,1e30,color="white",hatch="///",ec="0.8",lw=0,zorder=0); ax.text(3e3,2.2e28,"below the 1e30 erg/s stop criterion: not computed",fontsize=8,color="0.35")
ax.set(xscale="log",yscale="log",xlim=(2e2,3e6),ylim=(1e28,1e35),xlabel="Age (yr)",ylabel=r"$L_\gamma^\infty$ (erg s$^{-1}$)",
       title="Cooling bands from all 164 runs vs independent-age sources (current catalogue values)")
ax.legend(fontsize=7.5,loc="upper right"); fig.tight_layout(); fig.savefig("/home/claude/sweep3/fig4_bands_vs_sources_v2.png",dpi=160)
