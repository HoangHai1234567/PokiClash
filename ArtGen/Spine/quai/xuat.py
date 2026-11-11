# -*- coding: utf-8 -*-
"""Xuất rig của quai: atlas (xếp kệ, cạnh bội 8, gộp ảnh trùng, bảng 256 màu), JSON Spine 4.2, <mã>_game.json đúng trường
AolaActor đọc, .atomik (qua ArtGen/Spine/atomik.py) và nạp lại để kiểm, trang xem một file, tờ khung, lưới, chân dung, báo cáo.

    tong = xuat.xuat_het(sk, clips, "inbox/tm01_1/rig", "tm01_1", tieu_de="Giọt Lam", dang=1, so_dang=2, ma_goc=3211)
"""
import base64
import gzip
import hashlib
import io
import json
import math
import os
import shutil
import struct
import time

import numpy as np
from PIL import Image

from . import hoat, soi
from .khung import ZERO

HERE = os.path.dirname(os.path.abspath(__file__))
SPINE = os.path.dirname(HERE)
GAME_CLIPS = ["appear", "idle", "attack", "cast", "skill", "hit", "die", "evolve", "aura"]
NHAN = {"appear": "Xuất hiện", "idle": "Đứng", "attack": "Đánh thường", "cast": "Chiêu bắn", "skill": "Chiêu cuối", "hit": "Trúng đòn",
        "die": "Chết", "evolve": "Tiến hóa", "aura": "Aura (lặp chồng)"}


# ---------------------------------------------------------------- atlas
def xep_atlas(images, pad=3):
    """xếp kệ: ảnh cao trước; ảnh trùng điểm ảnh dùng chung một vùng (hai tên cùng bounds). Cạnh atlas làm tròn lên bội 8."""
    uniq, alias = {}, {}
    for nm, im in images.items():
        h = hashlib.md5(im.tobytes() + bytes(str(im.size), "ascii")).hexdigest()
        if h in uniq:
            alias[nm] = uniq[h]
        else:
            uniq[h] = nm
    items = sorted(((nm, images[nm]) for nm in uniq.values()), key=lambda kv: (-kv[1].height, -kv[1].width))
    area = sum((im.width + pad) * (im.height + pad) for _, im in items)
    widest = max(im.width for _, im in items) + 2 * pad
    W = max(widest, int(math.sqrt(area * 1.15)))
    W = (W + 7) // 8 * 8
    place, shelves, y = {}, [], pad
    for nm, im in items:
        for sh in shelves:
            if sh[1] + im.width + pad <= W and im.height <= sh[2]:
                place[nm] = (sh[1], sh[0], im.width, im.height)
                sh[1] += im.width + pad
                break
        else:
            shelves.append([y, pad + im.width + pad, im.height])
            place[nm] = (pad, y, im.width, im.height)
            y += im.height + pad
    H = (y + 7) // 8 * 8
    sheet = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for nm, (x, yy, _, _) in place.items():
        sheet.paste(images[nm], (x, yy))
    for a, b in alias.items():
        place[a] = place[b]
    return sheet, place


# ---------------------------------------------------------------- JSON Spine 4.2
def _att_json(sk, spec):
    t = spec["type"]
    if t == "mesh":
        vs = []
        for row in spec["verts"]:
            vs.append(len(row))
            for b, x, y, w in row:
                vs += [sk.bi[b], round(x, 2), round(y, 2), round(w, 4)]
        n = len(spec["verts"])
        return {"type": "mesh", "path": spec["path"], "uvs": [round(float(v), 5) for v in np.asarray(spec["uv"]).ravel()],
                "triangles": [int(i) for i in np.asarray(spec["tris"]).ravel()], "vertices": vs, "hull": int(spec["hull"] or n),
                "width": spec["width"], "height": spec["height"]}
    if t == "region":
        a = {"path": spec["path"], "x": round(spec["x"], 2), "y": round(spec["y"], 2), "width": spec["width"], "height": spec["height"]}
        if abs(spec.get("rotation", 0)) > 1e-4:
            a["rotation"] = round(spec["rotation"], 3)
        if abs(spec.get("scaleX", 1) - 1) > 1e-6:
            a["scaleX"] = round(spec["scaleX"], 5)
        if abs(spec.get("scaleY", 1) - 1) > 1e-6:
            a["scaleY"] = round(spec["scaleY"], 5)
        return a
    if t == "clipping":
        v = spec["verts"]
        return {"type": "clipping", "end": spec["end"], "vertexCount": len(v) // 2, "vertices": [round(x, 2) for x in v], "color": "ce3a3aff"}
    raise ValueError(t)


def ghi_spine(sk, anims, ra_dir, ten, bang_mau=True, khung_bao=None):
    """ghi <ten>.json, <ten>.atlas, <ten>.png. anims: {tên clip: animation JSON}. Trả (place, atlas RGBA đã lượng tử)."""
    os.makedirs(ra_dir, exist_ok=True)
    sheet, place = xep_atlas(sk.images)
    png = os.path.join(ra_dir, ten + ".png")
    if bang_mau:
        q = sheet.quantize(256, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.FLOYDSTEINBERG)
        q.save(png, optimize=True)
        atlas_rgba = q.convert("RGBA")
    else:
        sheet.save(png, optimize=True)
        atlas_rgba = sheet
    lines = [ten + ".png", f"size:{sheet.width},{sheet.height}", "filter:Linear,Linear", "pma:false"]
    for nm, (x, y, w, h) in place.items():
        lines += [nm, f"bounds:{x},{y},{w},{h}"]
    with open(os.path.join(ra_dir, ten + ".atlas"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    bones = []
    for b in sk.bones:
        o = {"name": b["name"]}
        if b["parent"]:
            o["parent"] = b["parent"]
        for k, src, d in (("length", "length", 0), ("x", "x", 0), ("y", "y", 0), ("rotation", "rot", 0), ("scaleX", "sx", 1), ("scaleY", "sy", 1)):
            if abs(b[src] - d) > 1e-6:
                o[k] = round(float(b[src]), 3)
        if b["noScale"]:
            o["inherit"] = "noScale"
        bones.append(o)
    slots = []
    for s in sk.slots:
        o = {"name": s["name"], "bone": s["bone"]}
        if s["att"]:
            o["attachment"] = s["att"]
        if s["alpha"] < 1:
            o["color"] = "ffffff%02x" % int(round(s["alpha"] * 255))
        slots.append(o)
    skin = {sn: {an: _att_json(sk, spec) for an, spec in m.items()} for sn, m in sk.atts.items() if m}
    bx = khung_bao or (-300, -20, 600, 600)
    data = {"skeleton": {"spine": "4.2.28", "x": round(bx[0], 1), "y": round(bx[1], 1), "width": round(bx[2], 1), "height": round(bx[3], 1),
                         "images": "", "audio": ""},
            "bones": bones, "slots": slots, "skins": [{"name": "default", "attachments": skin}],
            "events": {n: {} for n in sk.events}, "animations": anims}
    with open(os.path.join(ra_dir, ten + ".json"), "w", encoding="utf-8") as f:
        f.write(json.dumps(data, separators=(",", ":"), ensure_ascii=False))
    return place, atlas_rgba


# ---------------------------------------------------------------- thông tin trận
def thong_tin_tran(sk, ve, clips, frames, dang=1, so_dang=2, dung_yen=("cast", "skill"), lao=(), far=(), mieng="mieng", beam=1.0,
                   beamStyle="", impact=None, plain=None, cao=None, fps_tran=25, fps=30, bo_cao=()):
    """<mã>_game.json (AtomikGame của Unity, AolaActor đọc): fps, height (đỉnh dáng đứng khung 0 idle, pixel rig), hitClips/hitTimes
    (giờ trúng/nhả của từng clip: Clip.trung hoặc sự kiện trung/can/phun/gam), stay (clip đứng yên: sân không nhún tới), lunge
    (clip ngoài attack cũng lao), far (clip có xương far/fly*: thường rỗng vì VFX ở lớp riêng), muzzle (vị trí xương `mieng` ở
    khung nhả của cast, y lên, gốc ở chân), beam, beamStyle, move, shadow, impact* (khựng, rung, bật lùi, chớp màn; mặc định mạnh
    dần theo dạng), plain (slot vẽ không viền sticker)."""
    hc = [n for n in clips if n not in ("idle", "aura", "evolve", "appear", "die", "hit") and clips[n].gio_trung() is not None]
    g = {"fps": fps_tran, "height": 0.0, "hitClips": hc, "hitTimes": [round(clips[n].gio_trung(), 4) for n in hc],
         "lunge": [c for c in lao if c in clips], "stay": [c for c in dung_yen if c in clips], "far": [c for c in far if c in clips],
         "muzzle": [], "beam": float(beam), "beamStyle": beamStyle or "", "move": "move", "shadow": "shadow"}
    g["height"] = round(cao if cao else soi.chieu_cao(ve, frames["idle"][0], bo_cao), 2)
    if "cast" in clips and mieng in sk.bi:
        c = clips["cast"]
        t = c.gio_trung() if c.gio_trung() is not None else 0.5 * c.dur
        P = frames["cast"][min(len(frames["cast"]) - 1, int(round(t * fps)))]
        p = sk.the_gioi(P)[mieng][:2, 2]
        g["muzzle"] = [round(float(p[0]), 2), round(float(p[1]), 2)]
    if impact is None:
        p = 1.0 + 2.0 * (dang - 1) / max(1, so_dang - 1)
        impact = {"attack": (0.03 + 0.01 * p, 0.18 + 0.05 * p, 0.05 + 0.01 * p),
                  "skill": (0.06 + 0.045 * p, 0.3 + 0.17 * p, 0.07 + 0.035 * p) + (("#fff6c966",) if p >= 2.9 else ())}
    cl = [c for c in impact if c in clips]
    if cl:
        g["impactClips"] = cl
        g["impactStop"] = [round(float(impact[c][0]), 4) for c in cl]
        g["impactShake"] = [round(float(impact[c][1]), 4) for c in cl]
        g["impactPush"] = [round(float(impact[c][2]), 4) for c in cl]
        if any(len(impact[c]) > 3 for c in cl):
            g["impactFlash"] = [str(impact[c][3]) if len(impact[c]) > 3 else "" for c in cl]
    if plain:
        g["plain"] = list(plain)
    return g


# ---------------------------------------------------------------- .atomik
def ra_atomik(ra_dir, ten, game):
    import atomik
    out = os.path.join(ra_dir, ten + ".atomik")
    atomik.convert(os.path.join(ra_dir, ten + ".json"), os.path.join(ra_dir, ten + ".atlas"), out, ten, game)
    return out


def doc_atomik(path):
    raw = open(path, "rb").read()
    if raw[:4] != b"ATMK":
        raise ValueError("không phải .atomik")
    ver = struct.unpack("<H", raw[4:6])[0]
    body = gzip.decompress(raw[6:])
    n = struct.unpack("<I", body[:4])[0]
    js = json.loads(body[4:4 + n].decode("utf-8"))
    m = struct.unpack("<I", body[4 + n:8 + n])[0]
    png = Image.open(io.BytesIO(body[8 + n:8 + n + m]))
    return ver, js, png


def _s1(k, t):
    S = 7
    n = len(k) // S
    if n == 0:
        return 0.0
    if t <= k[0]:
        return k[1]
    if t >= k[(n - 1) * S]:
        return k[(n - 1) * S + 1]
    i = 0
    while i < n - 2 and t >= k[(i + 1) * S]:
        i += 1
    o, q = i * S, i * S + S
    if int(k[o + 2]) == 1:
        return k[o + 1]
    return k[o + 1] + (k[q + 1] - k[o + 1]) * (t - k[o]) / max(1e-6, k[q] - k[o])


def _s2(k, t):
    S = 12
    n = len(k) // S
    if n == 0:
        return 0.0, 0.0
    if t <= k[0]:
        return k[1], k[2]
    if t >= k[(n - 1) * S]:
        return k[(n - 1) * S + 1], k[(n - 1) * S + 2]
    i = 0
    while i < n - 2 and t >= k[(i + 1) * S]:
        i += 1
    o, q = i * S, i * S + S
    if int(k[o + 3]) == 1:
        return k[o + 1], k[o + 2]
    u = (t - k[o]) / max(1e-6, k[q] - k[o])
    return k[o + 1] + (k[q + 1] - k[o + 1]) * u, k[o + 2] + (k[q + 2] - k[o + 2]) * u


def atomik_dinh(js, clip, t):
    """tính đỉnh thế giới mọi slot đang hiện từ dữ liệu .atomik như AtomikPose (Sample + World + Skin): {slot: (N, 2)}."""
    B = js["bones"]
    lx = [b["x"] for b in B]
    ly = [b["y"] for b in B]
    lr = [b["rot"] for b in B]
    sx = [b["sx"] for b in B]
    sy = [b["sy"] for b in B]
    slots = js["slots"]
    att = [s["att"] for s in slots]
    al = [1 - s.get("fade", 0) for s in slots]
    an = next((a for a in js["anims"] if a["name"] == clip), None)
    if an:
        for tl in an["tls"]:
            i = tl["bone"]
            if tl["type"] == 0:
                lr[i] += _s1(tl["keys"], t)
            else:
                x, y = _s2(tl["keys"], t)
                if tl["type"] == 1:
                    lx[i] += x
                    ly[i] += y
                else:
                    sx[i] *= x
                    sy[i] *= y
        for k in an.get("sk", []):
            for j, tt in enumerate(k["times"]):
                if tt <= t + 1e-5:
                    att[k["slot"]] = k["atts"][j]
        for k in an.get("sa", []):
            al[k["slot"]] = min(1, max(0, _s1(k["keys"], t)))
    Wm = []
    for i, b in enumerate(B):
        r = math.radians(lr[i])
        cs, sn = math.cos(r), math.sin(r)
        a_, b_, c_, d_ = cs * sx[i], -sn * sy[i], sn * sx[i], cs * sy[i]
        p = b["parent"]
        if p < 0:
            Wm.append((a_, b_, c_, d_, lx[i], ly[i]))
            continue
        pa, pb, pc, pd, px, py = Wm[p]
        qa, qb, qc, qd = pa, pb, pc, pd
        if b.get("noScale"):
            n0, n1 = math.hypot(pa, pc), math.hypot(pb, pd)
            if n0 > 1e-6:
                qa, qc = pa / n0, pc / n0
            if n1 > 1e-6:
                qb, qd = pb / n1, pd / n1
        Wm.append((qa * a_ + qb * c_, qa * b_ + qb * d_, qc * a_ + qd * c_, qc * b_ + qd * d_, pa * lx[i] + pb * ly[i] + px, pc * lx[i] + pd * ly[i] + py))
    out = {}
    for si, s in enumerate(slots):
        if att[si] < 0 or al[si] < 0.01:
            continue
        a = js["atts"][att[si]]
        w = a["wInfo"]
        n = len(a["uvs"]) // 2
        V = np.zeros((n, 2))
        k = 0
        for v in range(n):
            cnt = int(w[k])
            k += 1
            for _ in range(cnt):
                bi, bx, by, ww = int(w[k]), w[k + 1], w[k + 2], w[k + 3]
                m = Wm[bi]
                V[v, 0] += (m[0] * bx + m[1] * by + m[4]) * ww
                V[v, 1] += (m[2] * bx + m[3] * by + m[5]) * ww
                k += 4
        out[s["name"]] = V
    return out


def kiem_atomik(path, ve, frames, clips=("idle",), fps=30):
    """nạp lại .atomik: đếm xương/slot/hình/clip/sự kiện, so đỉnh tính từ dữ liệu .atomik (như runtime Unity) với bộ vẽ Python ở vài
    khung mỗi clip. In và trả lệch lớn nhất (px rig): ~0 là toạ độ gắn, khoá, độ đậm khớp."""
    ver, js, png = doc_atomik(path)
    names = [a["name"] for a in js["anims"]]
    worst, where, w0, wh0 = 0.0, "", 0.0, ""
    for c in clips:
        if c not in frames or c not in names:
            continue
        fr = frames[c]
        for i in sorted({0, len(fr) // 3, (2 * len(fr)) // 3, len(fr) - 1}):
            t = i / fps
            A = atomik_dinh(js, c, min(t, next(a["dur"] for a in js["anims"] if a["name"] == c)))
            items, _ = ve.skin(fr[i])
            for nm, _, V, _, _, a, _, _ in items:
                if a < 0.01 or nm not in A or len(A[nm]) != len(V):
                    continue
                d = float(np.hypot(*(A[nm] - V).T).max())
                if i == 0 and d > w0:
                    w0, wh0 = d, f"{c}/{nm}"
                if d > worst:
                    worst, where = d, f"{c}@{t:.2f}s/{nm}"
    print(f"  nạp lại {os.path.basename(path)}: bản {ver}, {len(js['bones'])} xương, {len(js['slots'])} slot, {len(js['atts'])} hình, "
          f"clip {names}, {sum(len(a.get('ev', [])) for a in js['anims'])} sự kiện, atlas {png.size[0]}x{png.size[1]}, "
          f"game {'có' if js.get('game') else 'KHÔNG'}")
    print(f"    đỉnh tính từ .atomik so với bộ vẽ Python: khung 0 mọi clip lệch {w0:.3f} px ({wh0}) [toạ độ gắn, khoá đầu]; "
          f"giữa clip lệch tối đa {worst:.2f} px ({where}) [do lược khoá RDP]")
    return {"ver": ver, "clips": names, "lech": worst, "lech0": w0, "game": js.get("game")}


# ---------------------------------------------------------------- trang xem
def trang_xem(ra_dir, ten, tieu_de, clip_names, view, info, idle="idle", die="die", seq=None):
    tpl = open(os.path.join(HERE, "xem_mau.html"), encoding="utf-8").read()
    b64 = lambda ext: base64.b64encode(open(os.path.join(ra_dir, ten + ext), "rb").read()).decode()  # noqa: E731
    js = open(os.path.join(ra_dir, ten + ".json"), encoding="utf-8").read().replace("</", "<\\/")
    cl = [n for n in clip_names if n != "aura"]
    seq = seq or [n for n in ("appear", "idle", "attack", "idle", "cast", "idle", "skill", "idle", "hit", "idle", "evolve", "die") if n in cl]
    rp = {"__TITLE__": tieu_de or ten, "__NAME__": ten, "__IDLE__": idle, "__DIE__": die, "__INFO__": info.replace('"', "'"),
          "__CLIPS__": json.dumps([[n, NHAN.get(n, n)] for n in cl], ensure_ascii=False), "__SEQ__": json.dumps(seq),
          "__VIEWS__": json.dumps({}), "__VIEW__": json.dumps([round(v, 1) for v in view]),
          "__ATLAS__": b64(".atlas"), "__PNG__": b64(".png"), "__JSON__": js}
    for k, v in rp.items():
        tpl = tpl.replace(k, v)
    os.makedirs(os.path.join(ra_dir, "lib"), exist_ok=True)
    shutil.copyfile(os.path.join(SPINE, "lib", "spine-player.js"), os.path.join(ra_dir, "lib", "spine-player.js"))
    p = os.path.join(ra_dir, "xem.html")
    with open(p, "w", encoding="utf-8") as f:
        f.write(tpl)
    return p


# ---------------------------------------------------------------- tất cả
def slot_aura(sk, aura):
    """slot do clip aura điều khiển (độ đậm, hình, hoặc xương / tổ tiên xương bị aura dời): không tính vào chiều cao dáng đứng,
    không vẽ vào chân dung."""
    if not aura:
        return set()
    bones, out = set(), set()
    for P in aura:
        bones |= set(P.t)
        out |= set(P.alpha) | set(P.att)
    for s in sk.slots:
        b = s["bone"]
        while b is not None:
            if b in bones:
                out.add(s["name"])
                break
            b = sk.bones[sk.bi[b]]["parent"]
    return out - {"root"}


def xuat_het(sk, clips, ra_dir, ten, tieu_de="", frames=None, dang=1, so_dang=2, dung_yen=("cast", "skill"), lao=(), far=(),
             mieng="mieng", beam=1.0, beamStyle="", impact=None, plain=None, cao=None, can=(), ma_goc=None, khung=True, luoi=True,
             xem=True, chan_dung=True, tol=None, dich_mb=0.3, tran_mb=0.5, khop_idle=0.25, noi_them=None):
    """chạy hết: nướng (nếu frames chưa có), khoá, JSON + atlas + PNG, game.json, .atomik + nạp lại kiểm, đo lệch nối clip, tờ khung
    từng clip (aura ghép cùng giây), luoi.png, ảnh cận (can = [(tên ảnh, clip, giây, tâm (x, y) hoặc tên xương, bán kính)]),
    chân dung 512, xem.html, so_sanh.md (ma_goc: số monster gốc), báo cáo dung lượng. khop_idle: hoà chừng ấy giây cuối mỗi clip
    không lặp (trừ die, evolve) về khung 0 idle (xoá phần lò xo còn dư; 0 = tắt). noi_them: {tên: chuỗi} số đo nối thêm vào báo
    cáo (vd. tienhoa.lech_cuoi cho evolve). Trả dict số liệu."""
    t0 = time.time()
    os.makedirs(ra_dir, exist_ok=True)
    cd = {c.ten: c for c in clips}
    frames = dict(frames or {})
    for c in clips:
        if c.ten not in frames:
            frames[c.ten] = hoat.nuong(sk, c)
    if khop_idle:
        for c in clips:
            if not c.loop and c.ten not in ("die", "evolve"):
                frames[c.ten] = [P.copy() for P in frames[c.ten]]
                hoat.khop_cuoi(frames[c.ten], frames["idle"][0], khop_idle)
    anims, nk = {}, 0
    for c in clips:
        a, k = hoat.thanh_khoa(sk, c, frames[c.ten], tol=tol)
        anims[c.ten] = a
        nk += k
    ve0 = soi.Ve(sk)
    bx = ve0.bao(frames["idle"][0])
    place, atlas = ghi_spine(sk, anims, ra_dir, ten, khung_bao=(bx[0], bx[1], bx[2] - bx[0], bx[3] - bx[1]))
    ve = soi.Ve(sk, atlas, place)
    bo = slot_aura(sk, frames.get("aura"))
    game = thong_tin_tran(sk, ve, cd, frames, dang, so_dang, dung_yen, lao, far, mieng, beam, beamStyle, impact, plain, cao, bo_cao=bo)
    with open(os.path.join(ra_dir, ten + "_game.json"), "w", encoding="utf-8") as f:
        json.dump(game, f, ensure_ascii=False, indent=1)
    out = ra_atomik(ra_dir, ten, game)
    chk = kiem_atomik(out, ve, frames, clips=[c.ten for c in clips])
    # nối clip: khung cuối mỗi clip không lặp so với khung 0 idle
    aura = frames.get("aura")
    idle0 = frames["idle"][0]
    noi = {}
    for c in clips:
        fr = frames[c.ten]
        if c.ten in ("aura", "evolve"):
            continue
        if c.loop:
            d, w = soi.lech(ve, fr[-2], fr[0]) if len(fr) > 2 else (0.0, "")
            dd, _ = soi.lech(ve, fr[1], fr[0]) if len(fr) > 2 else (0.0, "")
            noi[c.ten] = (d, w, f"bước khép vòng {d:.2f} px (bước thường {dd:.2f})")
        elif c.ten == "die":
            items, _ = ve.skin(fr[-1])
            vis = [x[0] for x in items if x[5] > 0.02]
            noi[c.ten] = (0.0 if not vis else float("inf"), "", "khung cuối trống" if not vis else f"khung cuối CÒN HIỆN: {', '.join(vis[:5])}")
        else:
            d, w = soi.lech(ve, fr[-1], idle0)
            noi[c.ten] = (d, w, f"khung cuối lệch khung 0 idle {d:.2f} px" + (f" ({w})" if w else ""))
            if c.ten == "appear":
                items, _ = ve.skin(fr[0])
                vis = [x[0] for x in items if x[5] > 0.02]
                noi[c.ten] = (d, w, noi[c.ten][2] + ("; khung đầu trống" if not vis else f"; khung đầu còn hiện {len(vis)} slot"))
    for k, s in (noi_them or {}).items():
        noi[k] = (0.0, "", s)
    for k, (d, w, s) in noi.items():
        print(f"  nối {k}: {s}")
    if khung:
        for c in clips:
            if c.ten == "aura":
                continue
            fr = hoat.phu_aura(frames[c.ten], aura, sk) if aura else frames[c.ten]
            soi.to_khung(ve, fr, c, os.path.join(ra_dir, f"khung_{c.ten}.png"))
    if luoi:
        soi.anh_luoi(sk, os.path.join(ra_dir, "luoi.png"), ve)
    for item in can:
        nm_, cl_, t_, tam, r = item
        fr = frames[cl_][min(len(frames[cl_]) - 1, int(round(t_ * 30)))]
        if isinstance(tam, str):
            tam = tuple(sk.the_gioi(fr)[tam][:2, 2])
        soi.anh_can(ve, fr, tam, r, os.path.join(ra_dir, nm_ + ".png"))
    if chan_dung:
        soi.chan_dung(ve, idle0, os.path.join(ra_dir, "chan_dung.png"), bo=bo)
    tk = sk.tom_tat()
    js_kb = os.path.getsize(os.path.join(ra_dir, ten + ".json")) / 1024
    png_kb = os.path.getsize(os.path.join(ra_dir, ten + ".png")) / 1024
    at_kb = os.path.getsize(out) / 1024
    info = (f"{tk['xuong']} xương · {tk['slot']} slot · {tk['dinh']} đỉnh · {tk['tam_giac']} tam giác · {len(anims)} clip · {nk} khoá · "
            f".atomik {at_kb / 1024:.2f} MB")
    if xem:
        B = soi._union([ve.bao(frames[c.ten][len(frames[c.ten]) // 2]) for c in clips if c.ten != "aura"] + [bx], 0.1)
        trang_xem(ra_dir, ten, tieu_de, [c.ten for c in clips], ((B[0] + B[2]) / 2, (B[1] + B[3]) / 2, B[2] - B[0], B[3] - B[1]), info)
    muc = "ĐẠT" if at_kb / 1024 <= dich_mb else ("dưới trần" if at_kb / 1024 <= tran_mb else "VƯỢT TRẦN")
    print(f"  {ten}: {info}")
    print(f"  dung lượng: json {js_kb:.0f} KB + png {png_kb:.0f} KB (atlas {atlas.width}x{atlas.height}); .atomik {at_kb:.0f} KB "
          f"-> {muc} (đích {dich_mb} MB, trần {tran_mb} MB); {time.time() - t0:.1f} s")
    tong = dict(tk, khoa=nk, clip={c.ten: round(c.dur, 3) for c in clips}, json_kb=round(js_kb, 1), png_kb=round(png_kb, 1),
                atomik_kb=round(at_kb, 1), atlas=[atlas.width, atlas.height], game=game, noi={k: v[2] for k, v in noi.items()},
                lech_atomik=chk["lech"], lech_atomik0=chk["lech0"])
    with open(os.path.join(ra_dir, "bao_cao.json"), "w", encoding="utf-8") as f:
        json.dump(tong, f, ensure_ascii=False, indent=1)
    if ma_goc:
        from . import sosanh
        sosanh.so_sanh(ra_dir, ten, tong, ma_goc)
    return tong
