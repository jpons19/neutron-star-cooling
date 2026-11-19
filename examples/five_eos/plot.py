"""Plot reference five-EOS cooling data without evolving a star."""
import argparse,csv
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--input-dir',type=Path,default=HERE/'reference');p.add_argument('--output-dir',type=Path,default=HERE/'results')
a=p.parse_args();out=a.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
fig,ax=plt.subplots(figsize=(8.5,6));rows=[]
for n,c in zip(['BSk22','BSk24','BSk25','BSk26','APR'],['#4477AA','#228833','#EE7733','#AA3377','#222222']):
 d=np.loadtxt(a.input_dir/n/'cooling_curve.csv',delimiter=',',skiprows=1)
 label='DDFGOS(APR)*' if n=='APR' else n+('*' if n=='BSk25' else '')
 ax.loglog(*d.T,color=c,lw=2.2,ls='--' if n=='APR' else '-',label=label);rows.extend([[label,1.4,*r] for r in d])
ax.set(xlabel='Age [yr]',ylabel=r'$L_\gamma^\infty$ [erg s$^{-1}$]',xlim=(1,1.2e6),ylim=(8e30,1e35),title=r'Neutron-star cooling: $M=1.4\,M_\odot$, $B=0$')
ax.grid(which='major',alpha=.25);ax.legend(frameon=False)
ax.text(.03,.05,'Gudmundsson envelope · same pairing prescriptions\nMURCA: Yakovlev+2001 · bremsstrahlung: BCF2024',transform=ax.transAxes,fontsize=9)
fig.text(.12,.025,'* BSk25: adopted crust–core join; APR: provisional crust composition (see docs/EOS_NOTES.md).',fontsize=8)
fig.tight_layout(rect=(0,.05,1,1))
for ext in ['png','pdf']:fig.savefig(out/('cooling_five_eos.'+ext),dpi=200)
with (out/'cooling_five_eos.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['model','mass_Msun','time_years','L_infinity_erg_s']);w.writerows(rows)
print(out)
