import csv
rows=[]
def add(block,eos,m,p,n,env="fe",mesh="C",t8="1.d2",minL="1e30",tag=""):
    pid=f"p{p}" if p else "poff"; nid=f"n{n}" if n else "noff"
    rows.append(dict(id=f"{block}_{eos}_{m:.2f}_{pid}_{nid}_{env}{tag}",block=block,eos=eos,mass=m,p=p,n=n,env=env,mesh=mesh,t8=t8,minL=minL))
# F: cold edge vs central density (strong p 8, four triplets)
for eos,m in (("BSk24",1.2),("BSk24",1.5),("BSk26",1.6)):
    for n in (26,33,31,12): add("F",eos,m,8,n)
# G: hot edge vs proton gap (no triplet)
for eos,m in (("BSk24",1.2),("BSk26",2.1)):
    for p in (20,18,21,23,24,25): add("G",eos,m,p,0)
# H: direct Urca onset map
for m in (1.62,1.66,1.75,1.95):
    add("H","BSk24",m,0,0); add("H","BSk24",m,8,26)
for m in (1.2,1.3,1.5): add("H","BSk22",m,0,0)
# I: envelope completion (accreted)
add("I","BSk26",2.1,8,26,"accreted"); add("I","BSk24",1.2,8,0,"accreted")
add("I","BSk24",1.75,0,0,"accreted"); add("I","BSk24",1.75,8,26,"accreted")
# J: late times, references to 1e27 erg/s
add("J","BSk26",1.7,8,0,"fe",minL="1e27"); add("J","BSk26",1.7,8,0,"accreted",minL="1e27")
add("J","BSk26",2.1,8,26,"fe",minL="1e27"); add("J","BSk26",2.1,8,26,"accreted",minL="1e27")
# K: numerical checks on references
add("K","BSk26",1.7,8,0,mesh="D",tag="_meshD"); add("K","BSk26",2.1,8,26,mesh="D",tag="_meshD")
add("K","BSk26",1.7,8,0,t8="1.d1",tag="_T1e9"); add("K","BSk26",2.1,8,26,t8="1.d1",tag="_T1e9")
with open("plan3.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
print(len(rows))
