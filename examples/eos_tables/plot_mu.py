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
root=REPO;OUT=HERE/'results';OUT.mkdir(parents=True,exist_ok=True);f=CODE/'eos/BSk25'
a=np.loadtxt(f/'eos.thermo',skiprows=1);n=np.loadtxt(f/'eos.nb',skiprows=2)
mn=float((f/'eos.thermo').read_text().split()[0]);mu=mn*(1+a[:,5]);p=n*a[:,3]
fig,ax=plt.subplots(figsize=(9,6))
idx=np.arange(281,296);ci=np.arange(296,302)
ax.plot(mu[idx],p[idx],'o-',color='#2266aa',ms=5,label='Crust: original table')
ax.plot(mu[ci],p[ci],'s-',color='#d46922',ms=5,label='Homogeneous core: original table')
hi=np.arange(290,296)
ax.scatter(mu[hi],p[hi],s=90,facecolors='none',edgecolors='#b32931',lw=1.4,zorder=5,label='Crust rows 291–296 (currently omitted)')
ax.plot(mu[295:298],p[295:298],':',color='.55',lw=1.2,label='Raw crust–core connection')
for row,offset in [(290,(-60,12)),(294,(-8,15)),(295,(8,-20)),(296,(-65,-23)),(297,(10,-18)),(298,(10,0))]:
    ax.annotate(str(row+1),(mu[row],p[row]),xytext=offset,textcoords='offset points',fontsize=10,arrowprops=dict(arrowstyle='-',color='.5',lw=.6))
ax.set(xlim=(950.9,951.175),ylim=(.203,.227),xlabel=r'$\mu_b$ [MeV]',ylabel=r'$P$ [MeV fm$^{-3}$]',title='BSk25: pressure versus baryon chemical potential\nOriginal data near the crust–core transition')
ax.grid(alpha=.25);ax.legend(loc='upper left',fontsize=9)
fig.text(.5,.015,r'$\mu_b=m_n(1+Q_3)$, $P=n_bQ_1$. Labels: original data-row numbers. No Maxwell reconstruction or extrapolation.',ha='center',fontsize=9)
fig.tight_layout(rect=(0,.04,1,1));fig.savefig(OUT/'BSk25_pressure_mu_b.png',dpi=180)
