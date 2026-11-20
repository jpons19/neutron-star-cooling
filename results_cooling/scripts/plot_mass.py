import numpy as np, json, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
DU={"BSk22":1.153,"BSk24":1.598,"BSk25":1.626,"BSk26":None,"APR":1.982}
ec={"BSk22":"#e41a1c","BSk24":"#377eb8","BSk25":"#4daf4a","BSk26":"#984ea3","APR":"#ff7f00"}
ms=np.linspace(1.2,2.0,10); cmap=plt.get_cmap("plasma"); norm=Normalize(1.15,2.05)
fig,axs=plt.subplots(2,3,figsize=(15,9),sharex=False); axs=axs.ravel()
summ={}
for ax,eos in zip(axs,DU):
    for m in ms:
        f=list((Path("runs")/f"{eos}_{m:.3f}").rglob("cooling_curve.csv"))
        if not f: continue
        c=np.loadtxt(f[0],delimiter=",",skiprows=1); du=DU[eos] is not None and m>DU[eos]
        ax.plot(c[:,0],c[:,1],"--" if du else "-",color=cmap(norm(m)),lw=1.5)
        summ.setdefault(eos,[]).append((m,np.interp(4,np.log10(c[:,0]),c[:,1]),du))
    thr=f"direct Urca above {DU[eos]:.2f} M$_\\odot$ (dashed)" if DU[eos] else "no direct Urca below M$_{max}$"
    ax.set(xscale="log",yscale="log",xlim=(1e2,4e6),ylim=(1e30,1e35),xlabel="Age (yr)",ylabel=r"$L_\gamma^\infty$ (erg s$^{-1}$)")
    ax.set_title(f"{eos} — {thr}",loc="left",fontsize=10); ax.grid(alpha=.25)
ax=axs[5]
for eos,v in summ.items():
    v=np.array(v,dtype=object); m=v[:,0].astype(float); L=v[:,1].astype(float)
    ax.plot(m,L,"-o",color=ec[eos],ms=4,label=eos)
ax.set(yscale="log",xlabel="Mass (M$_\\odot$)",ylabel=r"$L_\gamma^\infty$ at 10$^4$ yr (erg s$^{-1}$)",ylim=(1e30,3e34))
ax.set_title("Luminosity at 10$^4$ yr vs mass",loc="left",fontsize=10); ax.grid(alpha=.25); ax.legend(fontsize=8)
fig.subplots_adjust(left=.06,right=.9,top=.92,bottom=.07,wspace=.28,hspace=.3)
cax=fig.add_axes([.925,.3,.012,.45]); fig.colorbar(ScalarMappable(norm=norm,cmap=cmap),cax=cax,label="Mass (M$_\\odot$), curves in panels 1–5")
fig.suptitle("Mass sweep, default microphysics (crust n 7, core n 12, core p 8; Gudmundsson envelope)",x=.02,ha="left",fontsize=12)
fig.savefig("/mnt/user-data/outputs/mass_sweep_by_eos.png",dpi=150,)
