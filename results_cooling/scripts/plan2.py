import csv
rows=[]
def add(block,eos,m,p,n,env):
    rows.append(dict(id=f"{block}_{eos}_{m:.2f}_p{p}_n{n}_{env}",block=block,eos=eos,mass=m,p=p,n=n,env=env,crust=7))
# D1: corrected cold setting at the heaviest no-direct-Urca masses
add("D","BSk26",2.1,"weak","low","fe"); add("D","APR",1.9,"weak","low","fe"); add("D","BSk24",1.55,"weak","low","fe")
add("D","BSk26",2.1,"strong","high","fe")
# D2: accreted envelope for hot and cold minimal-cooling settings on other EOS/masses
add("D","BSk26",1.7,"strong","off","accreted"); add("D","APR",1.2,"strong","off","accreted")
add("D","BSk24",1.4,"weak","low","accreted")
# D3: just above the BSk24 direct Urca threshold
add("D","BSk24",1.65,"off","high","fe"); add("D","BSk24",1.65,"strong","off","fe")
old=list(csv.DictReader(open("plan.csv")))
with open("plan.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=old[0].keys()); w.writeheader(); w.writerows(old+rows)
print(len(old)+len(rows))
