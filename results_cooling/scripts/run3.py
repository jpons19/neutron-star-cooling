import csv, subprocess, time, json, sys
from pathlib import Path
CODE=Path("/home/claude/neutron-star-cooling/code")
T="""Structure file (not used)
none
Initial temperature T_8
{t8}
Unused
800
Superfluidity
a) crust n
1 7
b) core n
{nf} {nm}
c) core p
{pf} {pm}
envelope_model = {env}

eos = {eos}
mass = {mass}
mesh = {mesh}
"""
out=Path("runs"); log=Path("runlog.jsonl"); log.touch()
done={json.loads(l)["id"] for l in log.read_text().splitlines()}
for r in csv.DictReader(open("plan3.csv")):
    if r["id"] in done: continue
    p,n=int(r["p"]),int(r["n"])
    inp=out/(r["id"]+".in")
    inp.write_text(T.format(t8=r["t8"],nf=1 if n else 0,nm=n or 12,pf=1 if p else 0,pm=p or 8,env=r["env"],eos=r["eos"],mass=r["mass"],mesh=r["mesh"]))
    t0=time.time()
    pr=subprocess.run([sys.executable,str(CODE/"cooling_driver.py"),"--input",str(inp.resolve()),"--no-animation","--check-energy",
                       "--min-luminosity",r["minL"],"--final-years","1e8","--out",str((out/r["id"]).resolve())],capture_output=True,text=True,cwd=CODE)
    (out/(r["id"]+".log")).write_text(pr.stdout+pr.stderr)
    with log.open("a") as f: f.write(json.dumps(dict(id=r["id"],rc=pr.returncode,seconds=round(time.time()-t0,1)))+"\n")
