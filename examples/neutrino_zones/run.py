"""Reference BSk24 cooling: integrated neutrino dominance and local emissivities."""
import sys
from pathlib import Path
REPO = Path(__file__).resolve().parents[2]
CODE = REPO / "code"
sys.path.insert(0, str(CODE))
HERE = Path(__file__).resolve().parent

import csv,json
from pathlib import Path
from dataclasses import replace
import numpy as np
from config import CoolingConfig
from cooling import run_cooling
from input_model import read_parameters
from stellar_structure import StructureOptions,build_stellar_model
from mesh import mesh_spec
from emissivity import NEUTRINO_PROCESSES,modified_urca_emissivity
from emissivity_updated import use_updated_rates
from thermal_geometry import thermal_geometry
from state import LocalState
ROOT=CODE;OUT=HERE/'results';OUT.mkdir(parents=True,exist_ok=True)
cfg=read_parameters(ROOT/'input_bsk24');config=replace(CoolingConfig(),initial_temperature_8=cfg['Tinit8'])
use_updated_rates();NEUTRINO_PROCESSES.register('modified_urca',replace=True)(modified_urca_emissivity)
model=build_stellar_model(StructureOptions('BSk24',mass_solar=1.4,mesh=mesh_spec('C')),ROOT/'eos',cfg)
bg=model.background;run=run_cooling(bg,config)
ref=np.loadtxt(REPO/'examples/five_eos/reference/BSk24/cooling_curve.csv',delimiter=',',skiprows=1)
assert np.allclose(ref,np.column_stack([run.times_years,run.luminosity_erg_s]),rtol=1e-10,atol=0)
t=run.step_times_years[1:];d=np.asarray(run.dominant_neutrino_process[1:]);edges=np.r_[t[0],np.sqrt(t[:-1]*t[1:]),t[-1]]
boundaries=np.r_[0,np.flatnonzero(d[1:]!=d[:-1])+1,len(d)]
segments=[]
for a,b in zip(boundaries[:-1],boundaries[1:]):
 lo=max(1.,float(edges[a]));hi=float(edges[b])
 if hi>lo:segments.append(dict(process=str(d[a]),start_yr=lo,end_yr=hi,log_width=float(np.log10(hi/lo))))
print('SEGMENTS',json.dumps(segments),flush=True)
selected=[];seen=set()
for seg in sorted(segments,key=lambda x:x['log_width'],reverse=True):
 if seg['process'] not in seen:
  selected.append(seg);seen.add(seg['process'])
 if len(selected)==3:break
if len(selected)<3:
 for seg in sorted(segments,key=lambda x:x['log_width'],reverse=True):
  if seg not in selected:selected.append(seg)
  if len(selected)==3:break
if len(selected)<3:raise RuntimeError('Fewer than three dominance intervals; selection needs review')
selected.sort(key=lambda s:s['start_yr'])
geo=thermal_geometry(bg);weights=geo.volumes*1e15*bg.cells.ephi**2
names=[name for name,_ in run.neutrino_processes];snaps=[]
for k,seg in enumerate(selected):
 target=np.sqrt(seg['start_yr']*seg['end_yr']);step=int(np.argmin(abs(np.log(run.step_times_years[1:]/target))))+1
 T=run.profiles[step]*1e8/bg.cells.ephi;state=LocalState(T,bg.cells)
 q=np.array([fn(state) for _,fn in run.neutrino_processes]);assert np.all(np.isfinite(q)) and np.all(q>=0)
 l=q@weights;assert np.allclose(l,run.neutrino_luminosities[step],rtol=1e-12,atol=1e-50)
 row=dict(label=chr(65+k),step=step,time_yr=float(run.step_times_years[step]),dominant=names[int(np.argmax(l))],Lnu_total=float(l.sum()),fractions={n:float(v/l.sum()) for n,v in zip(names,l)},interval=seg)
 snaps.append(row)
 order=np.argsort(bg.cells.rho)
 with (OUT/f'profile_{chr(65+k)}.csv').open('w',newline='') as f:
  w=csv.writer(f);w.writerow(['rho_baryon_g_cm3','radius_km','T_local_K','T_inf_K','ephi','proper_volume_cm3','core']+['Q_'+n+'_erg_cm3_s' for n in names]+['Q_total_erg_cm3_s'])
  w.writerows(np.column_stack([bg.cells.rho,(bg.radius_km[:-1]+bg.radius_km[1:])/2,T,run.profiles[step]*1e8,bg.cells.ephi,geo.volumes*1e15,bg.cells.xh==0,*q,q.sum(axis=0)])[order])
np.savez_compressed(OUT/'history.npz',times=run.step_times_years,lnu=run.neutrino_luminosities,names=np.array(names),dominant=run.dominant_neutrino_process,curve=np.column_stack([run.times_years,run.luminosity_erg_s]))
(OUT/'selection.json').write_text(json.dumps(dict(eos='BSk24',mass_solar=model.star.mass_solar,radius_km=model.star.radius_cm/1e5,segments=segments,snapshots=snaps,core_boundary_rho=float(np.min(bg.cells.rho[bg.cells.xh==0]))),indent=2)+'\n')
print('SELECTED',json.dumps(snaps),flush=True)
