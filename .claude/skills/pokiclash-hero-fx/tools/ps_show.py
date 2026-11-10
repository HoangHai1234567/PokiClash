"""In công thức từng emitter của các prefab (theo tên file, không đuôi) từ JSONL của ps_dump.py, mỗi emitter một dòng.
Chạy: py -3 -I ps_show.py <etfx.jsonl> ToonFightAction ExplosionFireballSoftFire ...
"""
import json,sys,re
sys.stdout.reconfigure(encoding="utf-8")
rows={}
for l in open(sys.argv[1],encoding="utf-8"):
    r=json.loads(l); rows[r["prefab"].split("/")[-1][:-7]]=r
def f(v):
    if isinstance(v,float): return f"{v:.3g}"
    if isinstance(v,list) and v and isinstance(v[0],(int,float)): return "..".join(f(x) for x in v)
    if isinstance(v,dict) and "curve" in v: return "c["+" ".join(f"{t:.2f}:{x:.2f}" for t,x in v["curve"])+f"]x{f(v['mul'])}"
    if isinstance(v,dict) and "curve_max" in v: return "C["+" ".join(f"{t:.2f}:{x:.2f}" for t,x in v["curve_max"])+f"]x{f(v['mul'])}"
    if isinstance(v,dict) and "c" in v: return "g["+" ".join(f"{t}:{c}" for t,c in v["c"])+" | a "+" ".join(f"{t}:{a}" for t,a in v["a"])+"]"
    return str(v)
for name in sys.argv[2:]:
    r=rows.get(name)
    if not r: print("?? ",name); continue
    print(f"\n#### {r['prefab']}  ({len(r['ps'])} hệ)")
    for s in r["ps"]:
        m=s["mods"]; mt=s.get("mat",{})
        b="ADD" if mt.get("_DstBlend")==1 else "AB"
        out=[s["path"].split("/")[-1], f"{s.get('render')}/{b}", str(mt.get("tex") or mt.get("name") or "").split("/")[-1]]
        if s.get("mesh"): out.append("mesh="+s["mesh"])
        out.append(f"loop={s.get('loop')} dur={f(s.get('dur'))} delay={f(s.get('delay'))}")
        out.append(f"life={f(s.get('life'))} spd={f(s.get('speed'))} size={f(s.get('size'))} grav={f(s.get('grav'))} rot={f(s.get('rot'))}")
        if s.get("color") not in ("#ffffffff",None): out.append("col="+f(s.get("color")))
        sh=s.get("shape")
        if sh: out.append(f"shape={sh['type']} a={sh['angle']} r={f(sh['r'])} arc={sh['arc']} rnd={sh['rnd']}")
        if s.get("rate"): out.append("rate="+f(s["rate"]))
        if s.get("bursts"): out.append("bursts="+";".join(f"t{f(t)}:{f(c)}x{n}/{f(iv)}" for t,c,n,iv in s["bursts"]))
        if s.get("stretch"): out.append(f"stretch len={s['stretch']['len']} vel={s['stretch']['vel']}")
        for k in ("size_life","color_life","rot_life"):
            if k in m: out.append(k+"="+f(m[k]))
        if "sheet" in m: out.append(f"sheet={m['sheet']['tiles']} fot={f(m['sheet']['fot'])} start={f(m['sheet']['start'])} cyc={m['sheet']['cycles']}")
        if "limit" in m: out.append(f"limit mag={f(m['limit']['mag'])} damp={m['limit']['dampen']} drag={f(m['limit']['drag'])}")
        if "noise" in m: out.append("noise="+json.dumps(m["noise"]))
        if "vel" in m and m["vel"]: out.append("vel="+json.dumps(m["vel"]))
        if "force" in m: out.append("force="+json.dumps(m["force"]))
        if "sub" in m: out.append("sub="+str(m["sub"]))
        for k in ("collision","inherit","trail","rot_speed"):
            if k in m: out.append(k)
        print("  - "+" | ".join(out))
