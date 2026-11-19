"""Controlled one-channel-at-a-time Tc amplitude scan; fixed stellar background."""
import sys
from pathlib import Path
REPO = Path(__file__).resolve().parents[2]
CODE = REPO / "code"
sys.path.insert(0, str(CODE))
HERE = Path(__file__).resolve().parent

import argparse,csv,json
from dataclasses import replace,asdict
from pathlib import Path
from time import perf_counter
import numpy as np
from config import CoolingConfig
from cooling import run_cooling
from input_model import read_parameters
from stellar_structure import StructureOptions,build_stellar_model
from mesh import mesh_spec
from emissivity import NEUTRINO_PROCESSES,modified_urca_emissivity
from emissivity_updated import use_updated_rates
from energy_balance import energy_budget,energy_closure
ROOT=CODE
CHANNELS={'crust_n':'tc_crust','core_n':'tc_n','core_p':'tc_p'}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('eos',choices=['BSk24','APR']);args=ap.parse_args()
    out=HERE/'results'/args.eos;out.mkdir(parents=True,exist_ok=True)
    cfg=read_parameters(ROOT/'input_bsk24');config=replace(CoolingConfig(),initial_temperature_8=cfg['Tinit8'])
    use_updated_rates();NEUTRINO_PROCESSES.register('modified_urca',replace=True)(modified_urca_emissivity)
    model=build_stellar_model(StructureOptions(args.eos,mass_solar=1.4,mesh=mesh_spec('C')),ROOT/'eos',cfg)
    base=model.background
    cases=[('reference',None,1.)]+[(f'{ch}_x{s:g}',ch,s) for ch in CHANNELS for s in [0.,.5,2.]]
    summary=[]
    for label,ch,s in cases:
        bg=base
        if ch:
            field=CHANNELS[ch]
            bg=replace(base,faces=replace(base.faces,**{field:getattr(base.faces,field)*s}),cells=replace(base.cells,**{field:getattr(base.cells,field)*s}))
            for fixed in ['rho','ye','yn','yp','xh','mstar_n','mstar_p','ephi']:
                assert np.array_equal(getattr(bg.cells,fixed),getattr(base.cells,fixed))
        start=perf_counter();run=run_cooling(bg,config)
        assert np.all(np.isfinite(run.luminosity_erg_s)) and np.all(run.luminosity_erg_s>0)
        curve=np.column_stack([run.times_years,run.luminosity_erg_s])
        np.savetxt(out/(label+'.csv'),curve,delimiter=',',header='time_years,L_infinity_erg_s',comments='')
        closure=energy_closure(energy_budget(run,bg),start_years=1,tolerance=.01)
        row=dict(eos=args.eos,case=label,channel=ch or 'reference',factor=s,final_years=float(curve[-1,0]),steps=run.completed_steps,rejected_steps=run.rejected_steps,stop_reason=run.stop_reason,energy_max_error=float(closure.max_error),seconds=perf_counter()-start)
        for key in CHANNELS.values(): row[key+'_max_K']=float(np.max(getattr(bg.cells,key)))
        for age in [10,100,1000,10000,100000,300000,1000000]:
            row['L_'+str(age)+'yr']=float(10**np.interp(np.log10(age),np.log10(curve[:,0]),np.log10(curve[:,1]))) if curve[0,0]<=age<=curve[-1,0] else None
        if ch is None:
            old=np.loadtxt(REPO/'examples/five_eos/reference'/args.eos/'cooling_curve.csv',delimiter=',',skiprows=1)
            row['baseline_matches_previous']=bool(old.shape==curve.shape and np.allclose(old,curve,rtol=1e-10,atol=0))
        summary.append(row);(out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
        print(json.dumps(row),flush=True)
    fields=list(CHANNELS.values())
    np.savetxt(out/'reference_Tc_profiles.csv',np.column_stack([base.cells.rho,*[getattr(base.cells,key) for key in fields]]),delimiter=',',header='rho_baryon_g_cm3,'+','.join(k+'_K' for k in fields),comments='')
    settings=asdict(config);settings['final_years']=None
    (out/'settings.json').write_text(json.dumps(dict(eos=args.eos,mass_solar=model.star.mass_solar,radius_km=model.star.radius_cm/1e5,mesh='C',input=cfg,cooling=settings,method='Scale Tc on both faces and cells; density support and shape fixed; one channel at a time.'),indent=2)+'\n')
if __name__=='__main__':main()
