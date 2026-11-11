# -*- coding: utf-8 -*-
"""so_sanh.md: số đo rig của mình so với con gốc Sword x Staff (scan/monster_<số>/info.json do mo_xe/chay.py info quét, file .skel,
.atlas, .png ở web/assets/Monster/monster_<số>/)."""
import json
import os

REF = r"D:\RefAnimation\SwordxStaff"


def so_goc(ma):
    p = os.path.join(REF, "scan", f"monster_{ma}", "info.json")
    if not os.path.exists(p):
        return None
    d = json.load(open(p, encoding="utf-8"))
    atts = [a for s in d.get("skins", []) for a in s.get("atts", [])]
    nv = sum(a.get("verts", 4 if a["type"] == "_RegionAttachment" else 0) for a in atts)
    nt = sum(a.get("tris", 2 if a["type"] == "_RegionAttachment" else 0) for a in atts)
    meshes = [a for a in atts if a["type"] == "_MeshAttachment"]
    nk = sum(t.get("frames", 0) for a in d.get("anims", []) for t in a.get("tls", []))
    deform = sum(1 for a in d.get("anims", []) for t in a.get("tls", []) if t["type"] == "DeformTimeline")
    fdir = os.path.join(REF, "web", "assets", "Monster", f"monster_{ma}")
    size = sum(os.path.getsize(os.path.join(fdir, f)) for f in os.listdir(fdir)) if os.path.isdir(fdir) else 0
    return {"xuong": len(d["bones"]), "slot": len(d["slots"]), "dinh": nv, "tam_giac": nt, "khoa": nk, "mb": size / 1e6,
            "luoi": len(meshes), "manh": len(atts) - len(meshes), "max_xuong_dinh": max((a.get("maxInf", 1) for a in meshes), default=0),
            "ik": len(d.get("ik") or []), "transform": len(d.get("transform") or []), "deform": deform,
            "clip": [(a["name"], a["dur"]) for a in d.get("anims", [])]}


def so_sanh(ra_dir, ten, tong, ma):
    """ghi ra_dir/so_sanh.md. tong: dict do xuat.xuat_het trả (xuong, slot, dinh, tam_giac, khoa, atomik_kb, json_kb, png_kb, clip, noi)."""
    g = so_goc(ma)
    L = [f"# {ten}: so với con gốc monster_{ma}", ""]
    mine_mb = tong["atomik_kb"] / 1024
    if g is None:
        L.append(f"(chưa có scan/monster_{ma}/info.json)")
    L += ["| | của mình | con gốc |", "|---|---|---|"]
    rows = [("Xương", tong["xuong"], g and g["xuong"]), ("Slot", tong["slot"], g and g["slot"]), ("Đỉnh lưới", tong["dinh"], g and g["dinh"]),
            ("Tam giác", tong["tam_giac"], g and g["tam_giac"]), ("Khoá", tong["khoa"], g and g["khoa"]),
            ("MB", f"{mine_mb:.2f} (.atomik; json {tong['json_kb']:.0f} KB + png {tong['png_kb']:.0f} KB)",
             g and f"{g['mb']:.2f} (.skel + .atlas + .png)"),
            ("Clip", ", ".join(f"{k} {v:.2f}s" for k, v in tong["clip"].items()), g and ", ".join(f"{n} {d:.2f}s" for n, d in g["clip"]))]
    if g:
        rows += [("Lưới / mảnh cứng (gốc)", "", f"{g['luoi']} / {g['manh']}, tối đa {g['max_xuong_dinh']} xương mỗi đỉnh, IK {g['ik']}, "
                                                f"transform {g['transform']}, deform {g['deform']} timeline")]
    for nm, a, b in rows:
        L.append(f"| {nm} | {a} | {'' if b is None else b} |")
    if tong.get("noi"):
        L += ["", "## Nối clip (khung cuối so với khung 0 idle)", ""]
        L += [f"- {k}: {v}" for k, v in tong["noi"].items()]
    L += ["", f"Lệch .atomik nạp lại so với bộ vẽ Python: khung 0 {tong.get('lech_atomik0', 0):.3f} px (toạ độ gắn); giữa clip "
              f"{tong.get('lech_atomik', 0):.2f} px (lược khoá RDP)."]
    with open(os.path.join(ra_dir, "so_sanh.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    return os.path.join(ra_dir, "so_sanh.md")
