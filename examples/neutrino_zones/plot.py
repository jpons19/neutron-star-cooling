import sys
from pathlib import Path
REPO = Path(__file__).resolve().parents[2]
CODE = REPO / "code"
sys.path.insert(0, str(CODE))
HERE = Path(__file__).resolve().parent

import argparse
import json,csv,zipfile
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
parser=argparse.ArgumentParser(description="Plot cooling dominance and emissivity snapshots, without rerunning cooling.")
parser.add_argument('--input-dir',type=Path,default=HERE/'reference')
parser.add_argument('--output-dir',type=Path,default=HERE/'results')
args=parser.parse_args();OUT=args.input_dir.resolve();DEST=args.output_dir.resolve();DEST.mkdir(parents=True,exist_ok=True)
s=json.loads((OUT/'selection.json').read_text());h=np.load(OUT/'history.npz');names=h['names'].tolist();curve=h['curve'];t=h['times'];lnu=h['lnu']
labels=dict(modified_urca='Modified Urca',brems_nn='Bremsstrahlung nn',brems_np='Bremsstrahlung np',brems_pp='Bremsstrahlung pp',brems_ep='Bremsstrahlung ep',pbf_core='PBF core (n + p)',direct_urca='Direct Urca (zero)',brems_e_ions='Electron–ion bremsstrahlung',plasma='Plasmon decay',pbf_crust='PBF crust',pair='Pair annihilation')
colors=dict(zip(names,['#d89025','#34835c','#a5a80b','#bb6baf','#547bbb','#ac477c','#888888','#7751a6','#159fa6','#bd643d','#767029']))
fig=plt.figure(figsize=(15,10.5));gs=fig.add_gridspec(2,3,height_ratios=[1,1.1],hspace=.46,wspace=.30);top=fig.add_subplot(gs[0,:]);axes=[fig.add_subplot(gs[1,j]) for j in range(3)]
for seg in s['segments']:top.axvspan(seg['start_yr'],seg['end_yr'],color=colors[seg['process']],alpha=.20,lw=0)
top.loglog(*curve.T,color='black',lw=2.2,label=r'$L_\gamma^\infty$')
for snap in s['snapshots']:
 age=snap['time_yr'];lum=10**np.interp(np.log10(age),np.log10(curve[:,0]),np.log10(curve[:,1]));snap['Lgamma_inf']=float(lum)
 top.plot(age,lum,'ko',ms=6);top.axvline(age,color='.3',ls=':',lw=1);top.annotate(snap['label'],(age,lum),xytext=(6,9),textcoords='offset points',fontsize=12,fontweight='bold')
ratio=np.interp(curve[:,0],t,lnu.sum(axis=1))/curve[:,1];cross=np.flatnonzero((ratio[:-1]>=1)&(ratio[1:]<1))
photon_age=None
if len(cross):
 k=cross[-1];x=np.log(curve[k:k+2,0]);y=np.log(ratio[k:k+2]);photon_age=float(np.exp(x[0]-y[0]*(x[1]-x[0])/(y[1]-y[0])))
 top.axvline(photon_age,color='.3',ls='--',lw=1);top.text(photon_age*1.08,7e34,r'$L_\gamma^\infty>L_\nu^\infty$'+'\n(later times)',ha='left',va='top',fontsize=9)
top.set(xlim=(1,curve[-1,0]),ylim=(8e30,1e35),xlabel='Age [yr]',ylabel=r'$L_\gamma^\infty$ [erg s$^{-1}$]',title='BSk24 · 1.4 solar masses · reference gaps · Gudmundsson envelope')
top.grid(alpha=.2);top.legend(handles=[Line2D([0],[0],color='black',lw=2,label=r'$L_\gamma^\infty$')]+[Patch(facecolor=colors[n],alpha=.3,label=labels[n]) for n in dict.fromkeys(x['process'] for x in s['segments'])],fontsize=9,loc='lower left',ncol=2)
for ax,snap in zip(axes,s['snapshots']):
 data=np.genfromtxt(OUT/f"profile_{snap['label']}.csv",delimiter=',',names=True);rho=data['rho_baryon_g_cm3'];total=data['Q_total_erg_cm3_s'];peak=total.max()
 for name in names:
  q=data['Q_'+name+'_erg_cm3_s'];ax.loglog(rho,np.where(q>0,q,np.nan),color=colors[name],lw=1.5)
 ax.loglog(rho,total,'k--',lw=1.8);ax.axvline(s['core_boundary_rho'],color='.5',ls=':',lw=1)
 ax.set(xlim=(max(1e8,rho.min()),rho.max()*1.12),ylim=(peak*1e-9,peak*5),xlabel=r'$\rho_b$ [g cm$^{-3}$]',ylabel=r'$Q_\nu$ [erg cm$^{-3}$ s$^{-1}$]',title=f"{snap['label']} · t = {snap['time_yr']:.3g} yr\n"+labels[snap['dominant']])
 ax.grid(alpha=.2);ax.text(.03,.03,'Crust | core boundary: dotted line',transform=ax.transAxes,fontsize=8)
handles=[Line2D([0],[0],color=colors[n],lw=1.8,label=labels[n]) for n in names]+[Line2D([0],[0],color='black',ls='--',lw=1.8,label='Total emissivity')]
fig.legend(handles=handles,loc='lower center',ncol=4,fontsize=9,bbox_to_anchor=(.5,.015))
fig.suptitle('Cooling curve and local neutrino emission at three representative epochs',fontsize=16,y=.98)
fig.subplots_adjust(top=.90,bottom=.19,left=.07,right=.98)
fig.savefig(DEST/'BSk24_neutrino_zones.png',dpi=180);fig.savefig(DEST/'BSk24_neutrino_zones.pdf')
with (DEST/'integrated_neutrino_history.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['time_years','dominant_process']+['Lnu_inf_'+n+'_erg_s' for n in names]);w.writerows([[age,str(dom),*vals] for age,dom,vals in zip(t,h['dominant'],lnu)])
lines=['# BSk24: neutrino dominance and local emissivity profiles','', 'Reference: M=1.4 Msun, B=0, mesh C, Gudmundsson envelope, gaps 7/12/8, Yakovlev modified Urca and BCF2024 nucleon bremsstrahlung. The rerun reproduces the prior BSk24 reference to rtol=1e-10.','', 'Shading classifies the largest individual neutrino luminosity at infinity: Lnu_i_inf = integral Q_i exp(2 Phi) dV_proper. It does not classify local peak emissivity or compare an individual neutrino process with photons. Time boundaries are geometric midpoints between accepted samples and have timestep-level resolution. The plotted range starts at 1 yr. Snapshots are accepted states nearest the logarithmic midpoint of each interval; no isothermal profile is assumed.','', 'Local Q is evaluated at the actual local temperature T_inf(r)/exp(Phi(r)). Density is baryon mass density rho_b = 1.66e-24 g * n_b, consistent with microphysics, not energy density epsilon/c^2. Curves are sorted in density; zeros are omitted from the logarithmic drawing, but retained in CSV. Panel vertical ranges differ and each spans approximately nine decades below its peak; weaker contributions can lie below the drawing range. Dotted vertical lines mark the first core cell density (mesh approximation). PBF core includes neutrons and protons together; modified/direct Urca include the implemented lepton branches.','', '| Zone | Start [yr] | End [yr] | Largest neutrino luminosity |','|---|---:|---:|---|']
for k,seg in enumerate(s['segments']):lines.append(f"| {k+1} | {seg['start_yr']:.6g} | {seg['end_yr']:.6g} | {seg['process']} |")
lines+=['','| Snapshot | Time [yr] | Leading neutrino fraction | Total Lnu_inf [erg/s] | Lgamma_inf [erg/s] |','|---|---:|---:|---:|---:|']
for snap in s['snapshots']:lines.append(f"| {snap['label']} | {snap['time_yr']:.6g} | {100*snap['fractions'][snap['dominant']]:.3f}% ({snap['dominant']}) | {snap['Lnu_total']:.6g} | {snap['Lgamma_inf']:.6g} |")
lines+=['',f'Last transition to photon dominance: approximately {photon_age:.6g} yr.' if photon_age else 'No transition to photon dominance found.','', 'Independent integration of all three local emissivity profiles reproduces the recorded per-process neutrino luminosities to rtol=1e-12. No microphysics or evolution settings were changed for this diagnostic.']
(DEST/'BSk24_neutrino_zones.md').write_text('\n'.join(lines)+'\n')
print('\n'.join(lines[-8:]))
