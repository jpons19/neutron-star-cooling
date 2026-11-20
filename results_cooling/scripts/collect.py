"""Collect all runs from the three sweeps into one table of curves + metadata."""
import numpy as np, pandas as pd, json
from pathlib import Path
DU={"BSk22":1.153,"BSk24":1.598,"BSk25":1.626,"BSk26":9,"APR":1.982}
PMAP={"off":0,"weak":17,"strong":8}; NMAP={"off":0,"low":27,"high":26,"ref12":12}
recs=[]
def load(d,rid):
    f=list((Path(d)/"runs"/rid).rglob("cooling_curve.csv"))
    return np.loadtxt(f[0],delimiter=",",skiprows=1) if f else None
for r in pd.read_csv("/home/claude/sweep/plan.csv").itertuples():
    n = NMAP.get(r.n, int(str(r.n)[1:]) if str(r.n).startswith("m") else None)
    recs.append(dict(id=r.id,sweep="gap",block=r.block,eos=r.eos,mass=r.mass,p=PMAP[r.p],n=n,env=r.env,mesh="C",t8="1.d2",minL=1e30,c=load("/home/claude/sweep",r.id)))
for eos in DU:
    for m in np.linspace(1.2,2.0,10):
        rid=f"{eos}_{m:.3f}"
        recs.append(dict(id="M_"+rid,sweep="mass",block="M",eos=eos,mass=round(m,3),p=8,n=12,env="gudmundsson",mesh="C",t8="1.d2",minL=1e30,c=load("/home/claude/msweep",rid)))
for r in pd.read_csv("plan3.csv").itertuples():
    recs.append(dict(id=r.id,sweep="gap3",block=r.block,eos=r.eos,mass=r.mass,p=r.p,n=r.n,env=r.env,mesh=r.mesh,t8=r.t8,minL=float(r.minL),c=load(".",r.id)))
for d in recs: d["du"]=d["mass"]>DU[d["eos"]]
