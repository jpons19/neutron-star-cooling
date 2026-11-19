"""Plot and export the completed controlled gap amplitude experiment."""
import sys
from pathlib import Path
REPO = Path(__file__).resolve().parents[2]
CODE = REPO / "code"
sys.path.insert(0, str(CODE))
HERE = Path(__file__).resolve().parent

import argparse
import csv,json,zipfile
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
parser=argparse.ArgumentParser(description="Plot gap scan results without rerunning cooling.")
parser.add_argument('--input-dir',type=Path,default=HERE/'reference')
parser.add_argument('--output-dir',type=Path,default=HERE/'results')
args=parser.parse_args();OUT=args.input_dir.resolve();DEST=args.output_dir.resolve();DEST.mkdir(parents=True,exist_ok=True)
channels=['crust_n','core_n','core_p'];titles=[r'Crust neutrons $^1S_0$',r'Core neutrons $^3P_2$',r'Core protons $^1S_0$']
styles=[(0,'#4477aa','--'),(.5,'#ee7733','-'),(2,'#aa3377','-')]
fig,ax=plt.subplots(2,3,figsize=(15,8),sharex=True,sharey=True)
fr,ar=plt.subplots(2,3,figsize=(15,7.5),sharex=True,sharey=True)
rows=[];summary=[]
for i,eos in enumerate(['BSk24','APR']):
    summary.extend(json.loads((OUT/eos/'summary.json').read_text()))
    ref=np.loadtxt(OUT/eos/'reference.csv',delimiter=',',skiprows=1)
    for case in ['reference']+[f'{ch}_x{s:g}' for ch in channels for s in [0,.5,2]]:
        dat=np.loadtxt(OUT/eos/(case+'.csv'),delimiter=',',skiprows=1)
        rows.extend([[f'{eos}_{case}',1.4,*r] for r in dat])
    for j,ch in enumerate(channels):
        a=ax[i,j];b=ar[i,j]
        a.loglog(*ref.T,color='black',lw=2,label='Reference (s = 1)');b.axhline(1,color='black',lw=1.5)
        for s,c,ls in styles:
            data=np.loadtxt(OUT/eos/f'{ch}_x{s:g}.csv',delimiter=',',skiprows=1)
            label='Pairing off (s = 0)' if s==0 else f's = {s:g}'
            a.loglog(*data.T,color=c,ls=ls,label=label,lw=1.6)
            mask=(data[:,0]>=ref[0,0])&(data[:,0]<=ref[-1,0])
            t=data[mask,0];lref=10**np.interp(np.log10(t),np.log10(ref[:,0]),np.log10(ref[:,1]))
            b.loglog(t,data[mask,1]/lref,color=c,ls=ls,label=label,lw=1.6)
        for p in [a,b]:
            p.grid(which='major',alpha=.25);p.set_xlim(1,2e6);p.set_title(eos+' · '+titles[j]);p.set_xlabel('Age [yr]')
        a.set_ylim(8e30,1e35);a.set_ylabel(r'$L_\gamma^\infty$ [erg s$^{-1}$]');a.legend(fontsize=8)
        b.set_ylabel(r'$L_\gamma^\infty / L_{\rm reference}^\infty$');b.legend(fontsize=8)
fig.suptitle(r'Gap amplitude sensitivity: $T_c(\rho)\to sT_c(\rho)$, one channel at a time',fontsize=15)
fig.text(.5,.012,r'$M=1.4\,M_\odot$, $B=0$, Gudmundsson envelope, mesh C. Gap shapes/support fixed; other two channels remain at s = 1.',ha='center',fontsize=10)
fig.tight_layout(rect=(0,.04,1,.95));fig.savefig(DEST/'gap_scan_luminosity.png',dpi=170);fig.savefig(DEST/'gap_scan_luminosity.pdf')
fr.suptitle('Luminosity ratios relative to each EOS reference',fontsize=15)
fr.text(.5,.012,'Ratios use log–log interpolation only where both tracks exist. Runs stop below 1e31 erg/s; no extrapolation.',ha='center',fontsize=10)
fr.tight_layout(rect=(0,.04,1,.95));fr.savefig(DEST/'gap_scan_ratios.png',dpi=170);fr.savefig(DEST/'gap_scan_ratios.pdf')
with (DEST/'cooling_gap_scan.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['model','mass_Msun','time_years','L_infinity_erg_s']);w.writerows(rows)
with (DEST/'summary.csv').open('w',newline='') as f:
    fields=list(dict.fromkeys(k for r in summary for k in r));w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(summary)
lines=['# Gap amplitude scan: BSk24 and APR','', 'Twenty runs at 1.4 Msun: one reference and nine one-channel variations per EOS. The existing gap models are crust n = 7, core n = 12, core p = 8. Scale factors 0, 0.5 and 2 multiply Tc(rho) on faces and cells; the other two channels are unchanged. Scaling Tc is equivalent to scaling Delta0 with its conversion factor fixed. Momentum support and gap shape do not change. This is an amplitude sensitivity test, not an exploration of density shifts, widths or all gap models.','', 'Fixed: mesh C, initial redshifted T=1e10 K, B=0, Gudmundsson envelope, Yakovlev MURCA and BCF2024 bremsstrahlung, original conductivities and other neutrino rates, composition and effective masses. Each EOS stellar structure is constructed once and reused unchanged. All runs use the same timestep settings and stop below Lgamma_inf=1e31 erg/s. Curves are not extrapolated.','', 'APR retains its published Maxwell jump. Its unresolved crust-composition mapping remains provisional; the gap comparison within APR does not remove that limitation.','', 'Energy closure is checked in time windows from 1 yr, using the microphysics of each run. Spatial convergence has not been established by this scan.','', '| EOS | Case | L(1e4 yr)/reference | L(1e5 yr)/reference | Cutoff age [kyr] | Max energy residual [%] |','|---|---|---:|---:|---:|---:|']
for r in summary:
    ref=next(s for s in summary if s['eos']==r['eos'] and s['case']=='reference')
    vals=[r['eos'],r['case']]+[f"{r['L_'+str(t)+'yr']/ref['L_'+str(t)+'yr']:.4g}" if r['L_'+str(t)+'yr'] is not None and ref['L_'+str(t)+'yr'] is not None else 'outside track' for t in [10000,100000]]+[f"{r['final_years']/1000:.2f}",f"{100*r['energy_max_error']:.3f}"]
    lines.append('| '+' | '.join(vals)+' |')
lines+=['','Reference reproduction: '+str({r['eos']:r['baseline_matches_previous'] for r in summary if r['case']=='reference'}),'','See the per-EOS settings and reference_Tc_profiles CSVs for normalization and actual stellar Tc ranges. The combined cooling_gap_scan.csv uses model,mass_Msun,time_years,L_infinity_erg_s.']
lines += ['', 'Reference peak Tc sampled inside each star (K):', '', '| EOS | Crust n | Core n | Core p |', '|---|---:|---:|---:|']
for r in summary:
    if r['case']=='reference':
        lines.append('| '+r['eos']+' | '+' | '.join(f"{r[k+'_max_K']:.6g}" for k in ['tc_crust','tc_n','tc_p'])+' |')
(DEST/'gap_scan_report.md').write_text('\n'.join(lines)+'\n')
print('\n'.join(lines[-25:]))
