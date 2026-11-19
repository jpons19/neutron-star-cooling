import sys
from pathlib import Path
REPO = Path(__file__).resolve().parents[2]
CODE = REPO / "code"
sys.path.insert(0, str(CODE))
HERE = Path(__file__).resolve().parent

from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=REPO;OUT=HERE/'results';OUT.mkdir(parents=True,exist_ok=True)
fig,axes=plt.subplots(2,3,figsize=(15,8.2))
for j,name in enumerate(['BSk25','BSk26','APR']):
    folder=CODE/'eos'/name
    a=np.loadtxt(folder/'eos.thermo',skiprows=1)
    nb=np.loadtxt(folder/'eos.nb',skiprows=2).reshape(-1)
    mn=float((folder/'eos.thermo').read_text().split()[0])
    p=nb*a[:,3]*1.602176634e33
    rho=nb*mn*(1+a[:,9])*1.7826619216e12
    mu=mn*(1+a[:,5])
    ax=axes[0,j]; ax.loglog(rho,p,color='#245b83',lw=1.4)
    ax.set(xlim=(1e6,4e15),ylim=(1e20,1e37),title=name if name!='APR' else 'DDFGOS(APR)',ylabel=r'$P$ [dyn cm$^{-2}$]')
    ax.grid(alpha=.25)
    az=axes[1,j]
    if name=='BSk25':
        lo,hi=284,303; highlight=np.arange(290,296); core=296
        desc='Raw rows 291–296 currently omitted'
    elif name=='BSk26':
        lo,hi=271,280; highlight=np.array([275]);core=275
        desc='Raw row 276 currently omitted'
    else:
        lo,hi=1876,1906;highlight=np.arange(1886,1895);core=None
        desc='Existing Maxwell plateau; endpoints retained'
    scale=1e32 if name!='APR' else 1e33
    az.plot(rho[lo:hi]/1e14,p[lo:hi]/scale,'o-',color='#245b83',ms=4,label='Original table')
    if name!='APR':
        az.scatter(rho[highlight]/1e14,p[highlight]/scale,s=68,facecolors='none',edgecolors='#c43e32',lw=1.7,label='Omitted by current reader',zorder=4)
        for k in [294,295,296] if name=='BSk25' else [274,275]:
            az.annotate(str(k+1),(rho[k]/1e14,p[k]/scale),xytext=(5,8 if k%2==0 else -15),textcoords='offset points',fontsize=8)
        print(name,'mu around join',[(k+1,float(mu[k])) for k in range(core-2,core+2)])
    else:
        ids=np.array([1885,1895]);az.scatter(rho[ids]/1e14,p[ids]/scale,s=65,color='#26843d',label='Maxwell endpoints',zorder=4)
        print(name,'mu endpoints',mu[ids], 'rho endpoints',rho[ids])
    az.set(xlabel=r'$\rho=\varepsilon/c^2$ [$10^{14}$ g cm$^{-3}$]',ylabel=r'$P$ [$10^{%d}$ dyn cm$^{-2}$]'%int(np.log10(scale)),title=desc)
    az.grid(alpha=.25);az.legend(fontsize=8,loc='best')
    axes[0,j].set_xlabel(r'$\rho=\varepsilon/c^2$ [g cm$^{-3}$]')
fig.suptitle('Original CompOSE tables: pressure versus mass–energy density',fontsize=16)
fig.text(.5,.012,'Top: global profiles. Bottom: transition details. Lines connect raw rows in density order; no reconstruction applied. Row labels exclude file header.',ha='center',fontsize=9)
fig.tight_layout(rect=(0,.035,1,.95))
fig.savefig(OUT/'eos_pressure_profiles.png',dpi=170)
