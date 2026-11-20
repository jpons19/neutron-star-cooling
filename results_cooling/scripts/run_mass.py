import subprocess, time, json, sys, numpy as np
from pathlib import Path
CODE=Path("/home/claude/neutron-star-cooling/code")
T="""Structure file (not used)
none
Initial temperature T_8
1.d2
Unused
800
Superfluidity
a) crust n
1 7
b) core n
1 12
c) core p
1 8
envelope_model = gudmundsson

eos = {eos}
mass = {mass:.3f}
mesh = C
"""
out=Path("runs"); log=Path("runlog.jsonl"); log.touch()
done={json.loads(l)["id"] for l in log.read_text().splitlines()}
for eos in ["BSk22","BSk24","BSk25","BSk26","APR"]:
    for m in np.linspace(1.2,2.0,10):
        rid=f"{eos}_{m:.3f}"
        if rid in done: continue
        inp=out/(rid+".in"); inp.write_text(T.format(eos=eos,mass=m)); t0=time.time()
        p=subprocess.run([sys.executable,str(CODE/"cooling_driver.py"),"--input",str(inp.resolve()),"--no-animation","--check-energy",
                          "--min-luminosity","1e30","--out",str((out/rid).resolve())],capture_output=True,text=True,cwd=CODE)
        (out/(rid+".log")).write_text(p.stdout+p.stderr)
        with log.open("a") as f: f.write(json.dumps(dict(id=rid,rc=p.returncode,seconds=round(time.time()-t0,1)))+"\n")
