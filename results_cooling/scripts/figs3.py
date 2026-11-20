import numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
exec(open("collect.py").read())
R={d["id"]:d for d in recs if d["c"] is not None}
plt.rcParams.update({"font.size":10,"axes.spines.top":False,"axes.spines.right":False})
def L(d,a):
    c=d["c"]; return 10**np.interp(np.log10(a),np.log10(c[:,0]),np.log10(c[:,1])) if a<=c[:,0].max() else np.nan
COLD="D_BSk26_2.10_pstrong_nhigh_fe"; HOT="C_BSk26_1.70_pstrong_noff_fe"
def fmt(ax,t,xl=(1e2,4e6),yl=(1e30,1e35)):
    ax.set(xscale="log",yscale="log",xlim=xl,ylim=yl,xlabel="Age (yr)",ylabel=r"$L_\gamma^\infty$ (erg s$^{-1}$)"); ax.set_title(t,loc="left",fontsize=10.5); ax.grid(alpha=.25)
# ---- bands from all runs (excluding numerical-check block K)
tg=np.logspace(np.log10(100),np.log10(1e7),400); B={}
use=[d for d in R.values() if d["block"]!="K"]
def y(d):
    c=d["c"]; v=np.interp(np.log10(tg),np.log10(c[:,0]),np.log10(c[:,1]))
    v[tg>c[:,0].max()]=np.log10(d["minL"])-1; return v
Y={d["id"]:y(d) for d in use}
sets={"minimal_fe":lambda d: not d["du"] and d["env"] in("fe","gudmundsson"),"minimal_all":lambda d: not d["du"],"full":lambda d:True}
for k,s in sets.items():
    A=np.array([Y[d["id"]] for d in use if s(d)]); B[k+"_hi"]=A.max(0); B[k+"_lo"]=A.min(0)
    ids=[d["id"] for d in use if s(d)]; B[k+"_lo_id"]=[ids[i] for i in A.argmin(0)]; B[k+"_hi_id"]=[ids[i] for i in A.argmax(0)]
bands=pd.DataFrame({"t":tg,**{k:v for k,v in B.items()}}); bands.to_csv("bands_v2.csv",index=False)
# ---- fig6: F and G
fig,axs=plt.subplots(1,2,figsize=(12.5,4.9),sharey=True)
cm={26:"#2166ac",33:"#4dac26",31:"#d6604d",12:"#8073ac"}; nm={26:"AO",33:"TToa",31:"T",12:"HGA12 deep"}; ls={("BSk24",1.2):":",("BSk24",1.5):"--",("BSk26",1.6):"-."}
for d in R.values():
    if d["block"]=="F": axs[0].plot(d["c"][:,0],d["c"][:,1],ls[(d["eos"],d["mass"])],color=cm[d["n"]],lw=1.2)
axs[0].plot(R[COLD]["c"][:,0],R[COLD]["c"][:,1],"-",color="k",lw=2.2,label="cold reference (AO, BSk26 2.1)")
from matplotlib.lines import Line2D
h=[Line2D([],[],color=c,lw=2,label=nm[k]) for k,c in cm.items()]+[Line2D([],[],color="0.3",ls=v,label=f"{k[0]} {k[1]} M$_\\odot$") for k,v in ls.items()]+[Line2D([],[],color="k",lw=2.2,label="cold reference")]
axs[0].legend(handles=h,fontsize=7.5,loc="lower left",ncol=2); fmt(axs[0],"(a) Block F: triplet gaps at three more central densities (strong p, Fe)")
pc={8:"k",18:"#1b9e77",21:"#d95f02",23:"#7570b3",24:"#e7298a",25:"#66a61e"}; pn={8:"HGA12≈CCDK (ref.)",18:"BCLL",21:"CCYms",23:"EEHO",24:"EEHOr",25:"T"}
for (eos,m,lsx) in (("BSk24",1.2,"-"),("BSk26",2.1,"--")):
    for p in pc:
        rid=f"C_{eos}_{m:.2f}_pstrong_noff_fe" if p==8 else f"G_{eos}_{m:.2f}_p{p}_noff_fe"
        d=R[rid]; axs[1].plot(d["c"][:,0],d["c"][:,1],lsx,color=pc[p],lw=2 if p==8 else 1.2)
h=[Line2D([],[],color=c,lw=2,label=pn[k]) for k,c in pc.items()]+[Line2D([],[],color="0.3",ls="-",label="BSk24 1.2 M$_\\odot$"),Line2D([],[],color="0.3",ls="--",label="BSk26 2.1 M$_\\odot$")]
axs[1].legend(handles=h,fontsize=7.5,loc="lower left",ncol=2); fmt(axs[1],"(b) Block G: proton gaps, no triplet gap (Fe)")
fig.tight_layout(); fig.savefig("fig6_edges_checks.png",dpi=150); plt.close()
# ---- fig7: direct Urca map at 1e4 yr
fig,ax=plt.subplots(figsize=(12,5.8))
def series(ids,**k):
    pts=sorted((R[i]["mass"],L(R[i],1e4)) for i in ids if i in R); m,l=zip(*pts); ax.plot(m,l,**k)
series([i for i in R if i.startswith("H_BSk24") and "poff_noff" in i],marker="o",color="#377eb8",ls="-",label="BSk24, no gaps")
series([i for i in R if i.startswith("H_BSk24") and "p8_n26" in i]+["F_BSk24_1.50_p8_n26_fe","F_BSk24_1.20_p8_n26_fe"],marker="s",color="#377eb8",ls="--",label="BSk24, strong p + AO triplet (cold-reference gaps)")
series([i for i in R if i.startswith("H_BSk22")]+["B_BSk22_1.40_poff_noff_fe"],marker="o",color="#e41a1c",ls="-",label="BSk22, no gaps")
for eos,c in (("BSk22","#e41a1c"),("BSk24","#377eb8"),("BSk25","#4daf4a"),("APR","#ff7f00")):
    series([i for i in R if i.startswith(f"M_{eos}_")],color=c,ls=":",lw=1,marker=".",label=f"{eos}, default gaps (mass sweep)")
for rid,mk in (("I_BSk24_1.75_poff_noff_accreted","o"),("I_BSk24_1.75_p8_n26_accreted","s")):
    ax.plot(1.75,L(R[rid],1e4),mk,mfc="white",color="#377eb8",ms=7)
ax.plot([],[],"o",mfc="white",color="#377eb8",label="BSk24 1.75 M$_\\odot$, accreted envelope")
ax.axhspan(1e29,3e31,color="#2166ac",alpha=.10); ax.axhline(3e31,color="#2166ac",lw=1.2)
ax.text(1.205,2.2e31,"J0007+7303: catalogue limit 3×10$^{31}$ (BB alternative up to ~10$^{32}$)",fontsize=7.5,color="#2166ac",va="top")
ax.axhline(9.6e31,color="#2166ac",lw=.8,ls=":")
ax.axhspan(1.2e31,8.2e31,color="#c51b7d",alpha=.10); ax.text(1.97,7e31,"B2334+61 near branch",fontsize=7.5,color="#c51b7d",ha="right",va="top")
for t,c,yy in (("BSk22",1.153,5e33),("BSk24",1.598,5e33),("BSk25",1.626,1.6e33),("APR",1.982,5e33)): ax.axvline(c,color="0.75",lw=.8,ls="--"); ax.text(c+.004,yy,t+"\nthreshold",fontsize=6.5,color="0.5")
ax.set(yscale="log",xlim=(1.15,2.02),ylim=(1e29,2e34),xlabel="Mass (M$_\\odot$)",ylabel=r"$L_\gamma^\infty$ at 10$^4$ yr (erg s$^{-1}$)")
ax.set_title("Direct Urca map: luminosity at 10$^4$ yr vs mass (Fe or Gudmundsson envelope unless marked)",loc="left",fontsize=10.5); ax.grid(alpha=.25); ax.legend(fontsize=7.5,loc="upper left",bbox_to_anchor=(1.01,1),frameon=False)
fig.tight_layout(); fig.savefig("fig7_durca_map.png",dpi=150); plt.close()
# ---- fig8: late times
s=pd.read_csv("/home/claude/ns-thermal-catalogue/data/current_plot_sample.csv")
fig,ax=plt.subplots(figsize=(10,6))
for rid,c,lsx,lab in (("J_BSk26_1.70_p8_noff_fe","#b2182b","-","hot reference, Fe"),("J_BSk26_1.70_p8_noff_accreted","#b2182b","--","hot reference, accreted"),
                      ("J_BSk26_2.10_p8_n26_fe","#2166ac","-","cold reference, Fe"),("J_BSk26_2.10_p8_n26_accreted","#2166ac","--","cold reference, accreted")):
    if rid in R: ax.plot(R[rid]["c"][:,0],R[rid]["c"][:,1],lsx,color=c,lw=1.8,label=lab)
for r in s.itertuples():
    ind=r.age_basis=="independent"; hs=r.source_class=="HotSpotPSR" if "source_class" in s.columns else False
    if not ind and r.display_age_yr<1e5: continue
    col="k" if ind else ("#8c6bb1" if "hot" in str(r.source_class).lower() else "0.55")
    mk=("v" if r.luminosity_upper_limit else "o") if ind else ("s" if "hot" in str(r.source_class).lower() else "D")
    ax.plot(r.display_age_yr,r.L_inf_erg_s,mk,color=col,mfc=col if ind else "white",ms=5)
    if ind and np.isfinite(r.L_inf_erg_s_lo): ax.plot([r.display_age_yr]*2,[r.L_inf_erg_s_lo,r.L_inf_erg_s_hi],color=col,lw=.8)
    if ind and np.isfinite(r.age_yr_lo): ax.plot([r.age_yr_lo,r.age_yr_hi],[r.L_inf_erg_s]*2,color=col,lw=.8)
    ax.annotate(r.name.replace("PSR ",""),(r.display_age_yr,r.L_inf_erg_s),xytext=(3,3),textcoords="offset points",fontsize=6.5,color=col)
ax.plot([],[],"o",color="k",label="independent age"); ax.plot([],[],"D",color="0.55",mfc="white",label="characteristic age only"); ax.plot([],[],"s",color="#8c6bb1",mfc="white",label="small hot spot (characteristic age)")
fmt(ax,"Block J: references followed to 10$^{27}$ erg s$^{-1}$, with sources older than 10$^5$ yr",xl=(1e5,3e7),yl=(1e27,1e34)); ax.legend(fontsize=7.5,loc="upper right")
fig.tight_layout(); fig.savefig("fig8_late_times.png",dpi=150); plt.close()
print("ok")
