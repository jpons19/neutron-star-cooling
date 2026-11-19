import numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
plt.rcParams.update({"font.size":10,"axes.spines.top":False,"axes.spines.right":False})
def cur(rid):
    c=np.loadtxt(next((Path("runs")/rid).rglob("cooling_curve.csv")),delimiter=",",skiprows=1); return c[:,0],c[:,1]
def fmt(ax,title):
    ax.set(xscale="log",yscale="log",xlim=(1e2,4e6),ylim=(1e30,2e35),xlabel="Age (yr)",ylabel=r"$L_\gamma^\infty$ (erg s$^{-1}$)")
    ax.set_title(title,loc="left",fontsize=10.5); ax.grid(alpha=.25,which="major")

# F1: gaps x envelope, BSk24 1.4
fig,axs=plt.subplots(1,2,figsize=(12,4.8),sharey=True)
pc={"off":"#1b9e77","weak":"#7570b3","strong":"#d95f02"}; ns={"off":"-","low":"--","high":":"}
for p in pc:
    for n in ns:
        t,L=cur(f"A_BSk24_1.40_p{p}_n{n}_fe"); axs[0].plot(t,L,ns[n],color=pc[p],lw=1.7,label=f"p {p}, n {n}")
fmt(axs[0],"(a) Core gaps, Fe envelope — BSk24, 1.4 M$_\\odot$"); axs[0].legend(fontsize=7.5,ncol=3,loc="lower left")
for p in ("off","strong"):
    for n in ("off","high"):
        for env,ls in (("fe","-"),("accreted","--")):
            t,L=cur(f"A_BSk24_1.40_p{p}_n{n}_{env}")
            axs[1].plot(t,L,ls,color=pc[p],lw=1.7 if n=="off" else 1.0,label=f"p {p}, n {n}, {env}")
fmt(axs[1],"(b) Envelope: Fe (solid) vs accreted (dashed)"); axs[1].legend(fontsize=7.5,loc="lower left")
fig.tight_layout(); fig.savefig("fig1_gaps_envelope.png",dpi=150); plt.close()

# F2: mass x EOS
plan=pd.read_csv("plan.csv"); C=plan[plan.block=="C"]
DU={"BSk22":1.153,"BSk24":1.598,"BSk25":1.626,"BSk26":9,"APR":1.982}
ec={"BSk22":"#e41a1c","BSk24":"#377eb8","BSk25":"#4daf4a","BSk26":"#984ea3","APR":"#ff7f00"}
fig,axs=plt.subplots(1,2,figsize=(12,4.8),sharey=True)
for ax,(p,n,title) in zip(axs,[("strong","off","(a) Hot setting: strong p gap, no n-triplet"),("off","high","(b) Cold setting: no p gap, AO n-triplet")]):
    for r in C[(C.p==p)&(C.n==n)].itertuples():
        t,L=cur(r.id); du=r.mass>DU[r.eos]
        ax.plot(t,L,"--" if du else "-",color=ec[r.eos],lw=1.0+0.5*(r.mass>1.5),alpha=.9)
    fmt(ax,title)
from matplotlib.lines import Line2D
h=[Line2D([],[],color=c,lw=2,label=e) for e,c in ec.items()]+[Line2D([],[],color="k",ls="-",label="no direct Urca"),Line2D([],[],color="k",ls="--",label="direct Urca active")]
axs[0].legend(handles=h,fontsize=8,loc="lower left")
fig.tight_layout(); fig.savefig("fig2_mass_eos.png",dpi=150); plt.close()

# F3: triplet scan
lab={26:"AO 0.82",27:"BEEHS 0.39",28:"EEHO 0.49",29:"EEHOr 0.17",30:"SYHHP 0.88",31:"T 0.88",32:"TTav 0.55",33:"TToa 0.62",12:"HGA12 deep 1.08",13:"Baldo 5.39",14:"Elgaroy 1.31"}
cmap=plt.get_cmap("viridis")
fig,ax=plt.subplots(figsize=(8.5,5))
t,L=cur("C_BSk26_1.70_pstrong_noff_fe"); ax.plot(t,L,color="#b2182b",lw=2.2,label="no n-triplet (hot reference, 1.7 M$_\\odot$)")
for i,(k,v) in enumerate(lab.items()):
    rid="D_BSk26_2.10_pstrong_nhigh_fe" if k==26 else f"E_BSk26_2.10_pstrong_n{k}_fe"
    t,L=cur(rid); ax.plot(t,L,color="#2166ac" if k==26 else cmap(i/11),lw=2.6 if k==26 else 1.1,label=f"{k} {v}")
fmt(ax,"Core neutron-triplet gap models — BSk26, 2.1 M$_\\odot$, strong p gap, Fe\n(label: catalogue number, model, peak $T_c$ in 10$^9$ K)")
ax.legend(fontsize=7,ncol=2,loc="lower left"); fig.tight_layout(); fig.savefig("fig3_triplet_scan.png",dpi=150)
