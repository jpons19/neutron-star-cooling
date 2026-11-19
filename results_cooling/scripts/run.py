import csv, subprocess, time, json, sys
from pathlib import Path
CODE = Path("/home/claude/neutron-star-cooling/code")
GAPP = {"off": (0, 8), "weak": (1, 17), "strong": (1, 8)}
GAPN = {"off": (0, 12), "low": (1, 27), "high": (1, 26), "ref12": (1, 12), **{f"m{k}": (1, k) for k in range(11, 34)}}
TEMPLATE = """Structure file (not used)
none
Initial temperature T_8
1.d2
Unused
800
Superfluidity
a) crust n
1 {crust}
b) core n
{nf} {nm}
c) core p
{pf} {pm}
envelope_model = {env}

eos = {eos}
mass = {mass}
mesh = C
"""
out = Path("runs"); out.mkdir(exist_ok=True)
log = open("runlog.jsonl", "a")
done = {json.loads(l)["id"] for l in open("runlog.jsonl")} if Path("runlog.jsonl").stat().st_size else set()
for r in csv.DictReader(open("plan.csv")):
    if r["id"] in done: continue
    nf, nm = GAPN[r["n"]]; pf, pm = GAPP[r["p"]]
    inp = out / (r["id"] + ".in")
    inp.write_text(TEMPLATE.format(crust=r["crust"], nf=nf, nm=nm, pf=pf, pm=pm, env=r["env"], eos=r["eos"], mass=r["mass"]))
    t0 = time.time()
    p = subprocess.run([sys.executable, str(CODE / "cooling_driver.py"), "--input", str(inp.resolve()), "--no-animation",
                        "--check-energy", "--min-luminosity", "1e30", "--out", str((out / r["id"]).resolve())],
                       capture_output=True, text=True, cwd=CODE)
    (out / (r["id"] + ".log")).write_text(p.stdout + p.stderr)
    rec = dict(id=r["id"], rc=p.returncode, seconds=round(time.time() - t0, 1))
    log.write(json.dumps(rec) + "\n"); log.flush(); print(rec, flush=True)
