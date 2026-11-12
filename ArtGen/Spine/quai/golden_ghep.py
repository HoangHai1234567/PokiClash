"""Ghép Temp/GoldenRecalc.json (menu Unity "PokiClash/Thử/Tính lại golden sim, tướng trên nút ải") vào golden: sim.json, roster.json
"leads", battles.json, battle_events.json. Chỉ đổi ô khác, giữ định dạng file. Viết 2026-11-12 khi Gạc Đá (hai dạng) thay Dê Hoa
(ba dạng): boss tiến hóa một lần thay vì hai nên một trận golden và vài ô sim đổi. golden_thuy.py ghep_sim chỉ ghép sim.

    py -3 -I ArtGen/Spine/quai/golden_ghep.py [--kiem]
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
G = os.path.join(ROOT, "Assets", "02 Data", "Golden")
KIEM = "--kiem" in sys.argv


def so(v):
    """số nguyên ghi không phần thập phân như bản gốc."""
    if isinstance(v, float) and v.is_integer():
        return int(v)
    if isinstance(v, list):
        return [so(x) for x in v]
    if isinstance(v, dict):
        return {k: so(x) for k, x in v.items()}
    return v


def doc(ten):
    p = os.path.join(G, ten)
    raw = open(p, encoding="utf-8", newline="").read()
    return p, raw, json.loads(raw)


def ghi(p, raw, g, gon):
    if gon:
        out = json.dumps(g, separators=(",", ":"), ensure_ascii=False)
    else:
        out = json.dumps(g, indent=1, ensure_ascii=False)
        if "\r\n" in raw:
            out = out.replace("\n", "\r\n")
    out += "\r\n" if raw.endswith("\r\n") else ("\n" if raw.endswith("\n") else "")
    if not KIEM:
        open(p, "w", encoding="utf-8", newline="").write(out)


def main():
    rec = so(json.load(open(os.path.join(ROOT, "Temp", "GoldenRecalc.json"), encoding="utf-8")))
    # sim.json
    p, raw, g = doc("sim.json")
    zones = {z["zone"]: z for z in g["zones"]}
    doi = []
    for rz in rec["sim"]:
        st = {s["id"]: s for s in zones[rz["zone"]]["stages"]}
        for rs in rz["stages"]:
            cells = [{"win": int(c["win"]), "rounds": c["rounds"]} for c in rs["cells"]]
            if cells != st[rs["id"]]["cells"]:
                doi.append((rz["zone"], rs["id"]))
                st[rs["id"]]["cells"] = cells
    print("sim.json:", "không đổi" if not doi else f"{len(doi)} ải đổi: {doi[:12]}")
    if doi:
        ghi(p, raw, g, gon=not raw.lstrip().startswith("{\n") and "\n " not in raw[:200])
    # roster.json leads
    p, raw, g = doc("roster.json")
    cu = {x["id"]: x for x in g["leads"]}
    doi = [x["id"] for x in rec["leads"] if cu.get(x["id"]) != x]
    print("roster.json leads:", "không đổi" if not doi else f"{len(doi)} nút đổi: {doi[:12]}")
    if doi:
        for x in rec["leads"]:
            cu[x["id"]].update(x)
        ghi(p, raw, g, gon=False)
    # battles.json
    p, raw, g = doc("battles.json")
    moi = {b["seed"]: b for b in rec["battles"]}
    doi = []
    for b in g["battles"]:
        m = moi[b["seed"]]
        if any(b.get(k) != v for k, v in m.items()):
            doi.append(b["seed"])
            b.update(m)
    print("battles.json:", "không đổi" if not doi else f"{len(doi)} trận đổi: hạt giống {doi}")
    if doi:
        ghi(p, raw, g, gon=True)
    # battle_events.json
    p, raw, g = doc("battle_events.json")
    doi = []
    for i, (b, m) in enumerate(zip(g["battles"], rec["detail"])):       # bản tính lại: mỗi trận là mảng sự kiện; golden: {seed, evs}
        evs = m["evs"] if isinstance(m, dict) else m
        if b["evs"] != evs:
            doi.append(b.get("seed", i))
            b["evs"] = evs
    print("battle_events.json:", "không đổi" if not doi else f"{len(doi)} trận đổi: hạt giống {doi}")
    if doi:
        ghi(p, raw, g, gon=True)


if __name__ == "__main__":
    main()
