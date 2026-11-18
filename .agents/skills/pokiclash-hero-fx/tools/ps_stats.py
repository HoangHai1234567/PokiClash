"""Gom số theo loại lớp (tia văng, gai, vòng, quầng, khói, lõi lửa) của nhóm Combat: phân vị đời, tốc, cỡ, trọng lực, cản,
số hạt bắn, alpha giữ tới đâu, dáng đường cỡ. Chạy: py -3 -I ps_stats.py <etfx.jsonl>
"""
import json,sys,re,collections,statistics as st
sys.stdout.reconfigure(encoding="utf-8")
def num(v):
    if isinstance(v,(int,float)): return float(v)
    if isinstance(v,list) and v and all(isinstance(x,(int,float)) for x in v): return sum(v)/len(v)
    if isinstance(v,dict) and "mul" in v: return float(v["mul"])
    return None
def hi(v):
    if isinstance(v,list) and v and all(isinstance(x,(int,float)) for x in v): return max(v)
    return num(v)
G=collections.defaultdict(lambda: collections.defaultdict(list))
def kind(s):
    n=s["path"].split("/")[-1].lower(); t=str((s.get("mat") or {}).get("tex","")).lower()
    if "glow" in n or "glow" in t: return "glow"
    if "smoke" in n or "cloud" in n or "dust" in n or "cloud" in t: return "smoke/cloud"
    if "spark" in n or "ember" in n or "droplet" in n or "debris" in n or "stripe" in n: return "spark/debris"
    if "spike" in n or "triangle" in t or "wave3" in t or "line_sharp" in t: return "spike"
    if "ring" in n or "nova" in n or "ring" in t or "shockwave" in t: return "ring"
    if "fire" in n or "flame" in n or "explosion" in t or "fire" in t: return "fire/core"
    return None
for l in open(sys.argv[1],encoding="utf-8"):
    r=json.loads(l)
    if r["prefab"].startswith("Demo") or not r["prefab"].split("/")[1] in ("Combat",): continue
    for s in r["ps"]:
        if s.get("loop"): continue
        k=kind(s)
        if not k: continue
        g=G[k]
        for nm,v in (("life",num(s.get("life"))),("speed",hi(s.get("speed"))),("size",hi(s.get("size"))),("grav",num(s.get("grav")))):
            if v is not None: g[nm].append(v)
        lim=s["mods"].get("limit")
        g["damp"].append(lim["dampen"] if lim else 0)
        if s.get("bursts"): g["burst"].append(sum(hi(b[1]) or 0 for b in s["bursts"]))
        sl=s["mods"].get("size_life")
        if isinstance(sl,dict) and sl.get("curve"):
            c=sl["curve"]; a,b=c[0][1],c[-1][1]
            g["sizeshape"].append("grow" if b>a+0.2 else ("shrink" if a>b+0.2 else ("up-down" if max(x for _,x in c)>max(a,b)+0.2 else "flat")))
        cl=s["mods"].get("color_life")
        if isinstance(cl,dict) and cl.get("a"):
            aks=cl["a"]
            last1=[t for t,a in aks if a>=0.9]
            g["alpha_hold_until"].append(max(last1) if last1 else 0)
        g["stretched"].append(1 if s.get("render")=="stretched" else 0)
        g["sheet"].append(1 if "sheet" in s["mods"] else 0)
        g["noise"].append(1 if "noise" in s["mods"] else 0)
        g["delay"].append(num(s.get("delay")) or 0)
def q(a):
    a=sorted(a); n=len(a)
    return f"{a[n//4]:.2f}/{a[n//2]:.2f}/{a[(3*n)//4]:.2f}"
for k,g in G.items():
    print(f"== {k}  n={len(g['life'])}")
    for nm in ("life","speed","size","grav","damp","burst","alpha_hold_until","delay"):
        if g[nm]: print(f"   {nm:16s} p25/p50/p75 = {q(g[nm])}")
    print("   sizeshape",collections.Counter(g["sizeshape"]).most_common(),"stretched %.0f%%"%(100*st.mean(g["stretched"])),"sheet %.0f%%"%(100*st.mean(g["sheet"])),"noise %.0f%%"%(100*st.mean(g["noise"])))
