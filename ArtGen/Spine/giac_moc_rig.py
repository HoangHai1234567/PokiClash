# -*- coding: utf-8 -*-
"""Thú một sừng đảo Mộc (giac_moc, "thú cổ thụ"; tướng thứ 9 đảo Mộc): hình của mình chạy trên ĐÚNG rig của con gốc monster_3804.
Ghi chú: inbox/giac_moc_ghichu.md. Cách làm như huou_go_rig.py (skill pokiclash-spine-rig mục 00):
- XƯƠNG: đủ mọi xương của họ, đúng cha – con, đúng biến đổi riêng ở dáng gốc; thêm `move` (cha của mọi thứ), `mieng` (đỉnh sừng: chỗ tụ
  cầu và bắn tia của chiêu mana), `cau` (cỡ quả cầu cho VFX), `tim` (quả tim trong ngực: chỗ + cỡ cho VFX chiêu cuối).
- MẢNH: mỗi part của họ một ảnh của mình vẽ đúng khung ảnh vùng (giac_moc_manh.py: tờ khung part + tờ thân liền) lắp vào NGUYÊN lưới
  của họ (đỉnh, tam giác, uv, trọng số). BỎ: hai cụm lỗ trên lòng ngực, đầu + sừng + sừng nhỏ của họ. Mảnh của mình: `dau` (đầu LIỀN
  sừng, cắt từ concept "đúng chỗ, đúng cỡ", cứng trên xương đầu bone65; vẽ SAU mào đầu để mào nằm sau đầu như concept), `tim` (quả
  tim, cứng trên xương `tim`, ngay trên lòng ngực và dưới các tấm vỏ).
- CHUYỂN ĐỘNG: clip dựng ở tầng điều khiển (giac_moc_clip.py), runtime Spine thật nướng ra scan/sample_moi.json (đã áp path, IK,
  physics) → lệch so với dáng gốc cho mọi xương. Kênh riêng (kenh_rieng.json): bay → `move`, cau → `cau`, tim → `tim`, hien → độ đậm.
Xương, lưới và chuyển động gốc là của nhà phát hành game gốc; hình là của mình. Dùng nội bộ, không đăng công khai.

    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/giac_moc_rig.py        → inbox/giac_moc_1/rig/
    py -3 -I ArtGen/Spine/giac_moc_rig.py soi <clip> <giây,giây,...> [tỉ lệ] [luoi]          → rig/soi_<clip>.png (khung lớn nền xám)
    py -3 -I ArtGen/Spine/giac_moc_rig.py khop                                              → in phép khớp concept ↔ sơ đồ, mau/_khop.png
Biến môi trường: GM_AN=slot,slot (ẩn vài slot để soi lớp dưới); GM_THIEU=1 (part chưa có ảnh thì tô phẳng giữ chỗ)."""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "mo_xe"))
from quai import anh, luoi, trongso, khung, hoat, xuat, soi  # noqa: E402
from quai.hoat import Clip  # noqa: E402
import giac_moc as G  # noqa: E402
import giac_moc_manh as M  # noqa: E402
import giac_moc_bo_cuc as BC  # noqa: E402
import giac_moc_clip as RC  # noqa: E402

TEN_RIG = "giac_moc_1"
D_PX = float(os.environ.get("GM_DPX", "0.5"))        # pixel ảnh atlas cho mỗi đơn vị rig (con cao ~1500 đơn vị)
BO_TEN = ("shadow",)
BO_PART = M.BO_PART
CLIPS = [("appear", "gm_appear", False), ("idle", "gm_idle", True), ("walk", "gm_walk", True), ("attack", "gm_attack", False),
         ("cast", "gm_cast", False), ("skill", "gm_skill", False), ("hit", "gm_hit", False), ("die", "gm_die", False)]
VE_NGHI = ("appear", "attack", "cast", "skill", "hit")
TAN = 0.45
IMPACT = {"attack": (0.07, 0.42, 0.07), "skill": (0.22, 1.0, 0.18, "#fff3c066")}
AN = tuple(x for x in os.environ.get("GM_AN", "").split(",") if x)
THIEU = os.environ.get("GM_THIEU") == "1"
# các mốc trên concept (px, L1_duyet.png 1024 × 1536)
NGON_SUNG_PX = (972.0, 520.0)                # tâm tinh thể ở đỉnh sừng: chỗ tụ cầu
DAU_SAU = "P_toufa1"                         # slot `dau` chèn ngay sau slot này (mào đầu nằm sau đầu)
LECH = {"dau": (0.0, 0.0)}                   # chỉnh tay chỗ đặt đầu (đơn vị rig), sau khi soi
THAN_LIEN = tuple(M.LIEN["gan"]) + tuple(t for ds in M.LIEN["xa"] for t in ds)
MAU_THAN_BU = (19.0, 21.0, 11.0)
# vùng ảnh lưu to hơn trong atlas: lưới của họ kéo giãn cục bộ ở dáng nghỉ (B_beimao_06: ngạnh lá giãn 2,2 lần → mép răng cưa nhoè)
PHONG = {"B_beimao_06": 2.0}
TIM_R = 104.0                                # bán kính quả tim (đơn vị rig) ở cỡ 1


def nap_goc():
    scan = G.scan()
    D = json.load(open(os.path.join(scan, "att_goc.json"), encoding="utf-8"))
    D0 = json.load(open(os.path.join(scan, "att_idle0.json"), encoding="utf-8"))
    I = json.load(open(os.path.join(scan, "info.json"), encoding="utf-8"))
    return D, D0, I, scan


def anh_part(ten):
    z = M.zs().get(ten)
    pth = os.path.join(M.MANH, "part", ten + ".png")
    if z is None or not os.path.exists(pth):
        if not THIEU:
            raise SystemExit("thiếu ảnh part " + pth)
        im_, m = M.thiet_ke(ten, 2.0)
        g = Image.fromarray(np.dstack([im_, np.where(m, 255, 0).astype(np.uint8)]), "RGBA")
        z = 2.0
    else:
        g = Image.open(pth).convert("RGBA")
    kq = D_PX / (M.A_TL * z) * PHONG.get(ten, 1.0)
    g = g.convert("RGBa").resize((max(2, round(g.width * kq)), max(2, round(g.height * kq))), Image.LANCZOS).convert("RGBA")
    if ten in THAN_LIEN:
        # tờ thân liền Codex tô sẫm hơn concept (trung vị 149, 90, 52 so với 168, 111, 63): kéo màu vỏ cây về concept, không đụng nét
        # mực và bàn chân rễ sẫm (đo 2026-11-13; thân sẫm thì bầu vỏ ngực không nổi lên)
        A = np.asarray(g).astype(np.float32)
        sang = A[..., :3].max(axis=2)
        k = np.clip((sang - 112.0) / 26.0, 0.0, 1.0)[..., None]
        A[..., :3] = np.clip(A[..., :3] + np.array(MAU_THAN_BU, np.float32) * k, 0, 255)
        g = Image.fromarray(A.astype(np.uint8), "RGBA")
    return anh.loang_mau(g)


# ---------------------------------------------------------------- concept ↔ rig (dáng khung 0 idle)
_KH = {}


def khop(ve=False):
    """phép đồng dạng đưa pixel concept (L1_duyet.png) về pixel sơ đồ bố cục (bo_cuc_co_thu_nghi.png, dựng từ rig ở khung 0 idle):
    p' = tam + (p − tam) × s + (tx, ty). Dò s, tx, ty cho hình bóng hai ảnh trùng nhau nhất. Trả hàm px concept → thế giới rig (idle0)."""
    if not _KH:
        c = np.asarray(Image.open(os.path.join(G.TAI, "L1_duyet.png")).convert("RGB"))
        g = np.asarray(Image.open(os.path.join(G.MAU, "bo_cuc_co_thu_nghi.png")).convert("RGB"))
        mc = (c.min(2) < 236).astype(np.uint8)
        mg = (g.min(2) < 236).astype(np.uint8)
        H_, W_ = mg.shape
        tam = np.array([W_ / 2, H_ / 2])
        best = (-1, 1.0, 0, 0)
        k4 = 4
        gs = cv2.resize(mg, (W_ // k4, H_ // k4), interpolation=cv2.INTER_AREA)
        for s in np.arange(0.94, 1.061, 0.01):
            Mx = np.array([[s, 0, tam[0] * (1 - s)], [0, s, tam[1] * (1 - s)]], float)
            cs = cv2.warpAffine(mc, Mx, (W_, H_), flags=cv2.INTER_NEAREST)
            cs = cv2.resize(cs, (W_ // k4, H_ // k4), interpolation=cv2.INTER_AREA)
            for ty in range(-10, 11, 2):
                for tx in range(-10, 11, 2):
                    sh = np.roll(np.roll(cs, ty, 0), tx, 1)
                    iou = (sh & gs).sum() / max(1, (sh | gs).sum())
                    if iou > best[0]:
                        best = (iou, float(s), tx * k4, ty * k4)
        iou, s, tx, ty = best
        sc = BC.ti_le()
        T = BC.khung_T(BC.DANG["nghi"], sc)
        o = T(np.array([0.0, 0.0]))
        _KH.update(s=s, tx=tx, ty=ty, iou=iou, tam=tam, sc=sc, ox=float(o[0]), oy=float(o[1]))
        print(f"khớp concept ↔ sơ đồ: s = {s:.3f}, dời ({tx}, {ty}) px, IoU {iou:.3f}; sơ đồ {sc:.4f} px mỗi đơn vị rig")
        if ve:
            Mx = np.array([[s, 0, tam[0] * (1 - s) + tx], [0, s, tam[1] * (1 - s) + ty]], float)
            cw = cv2.warpAffine(c, Mx, (W_, H_), borderValue=(255, 255, 255))
            out = (cw.astype(float) * 0.6 + 255 * 0.4)
            out[cv2.morphologyEx(mg, cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)).astype(bool)] = (255, 0, 200)
            Image.fromarray(out.astype(np.uint8)).save(os.path.join(G.MAU, "_khop.png"))
            print(os.path.join(G.MAU, "_khop.png"))
    k = _KH

    def px_rig(p):
        p = np.asarray(p, float)
        q = k["tam"] + (p - k["tam"]) * k["s"] + np.array([k["tx"], k["ty"]])
        return np.stack([(q[..., 0] - k["ox"]) / k["sc"], (k["oy"] - q[..., 1]) / k["sc"]], -1)

    return px_rig, k["s"] / k["sc"]              # (hàm đổi, đơn vị rig cho mỗi px concept)


def manh_dau():
    """đầu liền sừng cắt từ tờ M_dau ("đúng chỗ, đúng cỡ") → (ảnh RGBA cắt sát, x0, y0 px concept)."""
    path = anh.to_moi_nhat(G.TAI, "M_dau")
    if not path:
        raise SystemExit("thiếu tờ M_dau")
    tt = anh.doc_to(path, dien_tich_min=600, gop_px=18)
    m_ = max(tt.manh, key=lambda m: m["dt"])
    mk = np.isin(tt.lab, m_["ids"])
    ys, xs = np.nonzero(mk)
    x0, x1, y0, y1 = max(0, xs.min() - 4), xs.max() + 5, max(0, ys.min() - 4), ys.max() + 5
    cell = tt.rgba[y0:y1, x0:x1].copy()
    cell[..., 3] = (cell[..., 3] * anh.gian(mk[y0:y1, x0:x1], 2)).astype(np.uint8)
    return Image.fromarray(cell, "RGBA"), int(x0), int(y0)


def gan_nguyen(sk, slot, anh_ten, att, ten, Wc, hinh=None):
    im = sk.images[anh_ten]
    L = luoi.Luoi(np.array(att["uv"], float).reshape(-1, 2) * np.array([im.width, im.height]), np.array(att["tris"]).reshape(-1, 3),
                  att["hull"], att["hull"], im.width, im.height, ten=slot)
    V = np.array(att["xy"], float).reshape(-1, 2)
    sk.luoi_gan(slot, anh_ten, L, trongso.cung(L.n, "move"), the_gioi=V, ten=hinh)
    rows = []
    for p, ws in zip(V, att["w"]):
        row = [(ten[k], *[float(v) for v in (np.linalg.inv(Wc[ten[k]]) @ np.array([p[0], p[1], 1.0]))[:2]], float(w)) for k, w in ws if w > 0.002]
        tot = sum(r[3] for r in row) or 1.0
        rows.append([(n, x, y, w / tot) for n, x, y, w in row])
    sk.atts[slot][hinh or anh_ten]["verts"] = rows
    return L


def cho_tim(by, ten, Wc):
    """chỗ đặt quả tim: điểm RỘNG NHẤT của lòng ngực (trong ảnh vùng của nó) → thế giới dáng gốc; xương bám nặng nhất quanh đó."""
    a = by["P_shenti_02"]
    _, imgs, _ = G.nap("att_goc.json")
    im = imgs[a["region"]]
    al = (np.asarray(G.part_goc(a))[..., 3] > 100).astype(np.uint8)
    d = cv2.distanceTransform(np.pad(al, 2), cv2.DIST_L2, 5)[2:-2, 2:-2]
    cy, cx = np.unravel_index(d.argmax(), d.shape)
    U = np.array(a["uv"], float).reshape(-1, 2) * np.array([im.width, im.height])
    V = np.array(a["xy"], float).reshape(-1, 2)
    kc = np.hypot(U[:, 0] - cx, U[:, 1] - cy)
    w = 1.0 / (kc + 6.0) ** 2
    w /= w.sum()
    tam = (V * w[:, None]).sum(0)
    # chính xác hơn: toạ độ trọng tâm trong tam giác chứa điểm
    for t in np.array(a["tris"]).reshape(-1, 3):
        A_, B_, C_ = U[t[0]], U[t[1]], U[t[2]]
        v0, v1, v2 = B_ - A_, C_ - A_, np.array([cx, cy], float) - A_
        den = v0[0] * v1[1] - v0[1] * v1[0]
        if abs(den) < 1e-9:
            continue
        b1 = (v2[0] * v1[1] - v2[1] * v1[0]) / den
        b2 = (v0[0] * v2[1] - v0[1] * v2[0]) / den
        if b1 >= -1e-6 and b2 >= -1e-6 and b1 + b2 <= 1 + 1e-6:
            tam = (1 - b1 - b2) * V[t[0]] + b1 * V[t[1]] + b2 * V[t[2]]
            w = np.zeros(len(V))
            w[t[0]], w[t[1]], w[t[2]] = 1 - b1 - b2, b1, b2
            break
    nang = {}
    for wi, ws in zip(w, a["w"]):
        for k, x in ws:
            nang[ten[k]] = nang.get(ten[k], 0.0) + wi * x
    xg = max(nang, key=nang.get)
    return tam, xg, float(d.max()) / M.A_TL, sorted(nang.items(), key=lambda q: -q[1])[:4]


def dung():
    D, D0, I, scan = nap_goc()
    IB = I["bones"]
    ten = [b["name"] for b in IB]
    assert ten == [b["name"] for b in D["bones"]]
    px_rig, u_px = khop()
    sk = khung.Sk(TEN_RIG)
    sk.xuong("root")
    sk.xuong("move", "root")
    for b in IB:
        if b["name"] == "root" or b["name"] in BO_TEN:
            continue
        cha = ten[b["parent"]]
        sk.xuong(b["name"], "move" if cha == "root" else cha, b["x"], b["y"], goc=b["rot"], dai=b["len"], sx=b["sx"], sy=b["sy"])
    Wc = {b["name"]: np.array([[b["a"], b["b"], b["x"]], [b["c"], b["d"], b["y"]], [0.0, 0.0, 1.0]]) for b in D["bones"]}
    W0 = {b["name"]: np.array([[b["a"], b["b"], b["x"]], [b["c"], b["d"], b["y"]], [0.0, 0.0, 1.0]]) for b in D0["bones"]}
    by = {a["slot"]: a for a in D["atts"]}
    slots = [s["name"] for s in I["slots"] if s["name"] not in BO_TEN and s["name"] in by and by[s["name"]].get("region")]
    dat_y = min(np.array(by[s]["xy"], float).reshape(-1, 2)[:, 1].min() for s in slots if "_tui" in s and "_3" in s)

    def idle_ve_goc(p, xg):
        """điểm thế giới ở khung 0 idle, cứng theo xương xg → thế giới dáng gốc."""
        return (Wc[xg] @ (np.linalg.inv(W0[xg]) @ np.array([p[0], p[1], 1.0])))[:2]

    # ---- đầu liền sừng (cắt từ concept)
    g_dau, dx0, dy0 = manh_dau()
    kq = u_px * D_PX
    im_dau = anh.loang_mau(g_dau.convert("RGBa").resize((max(2, round(g_dau.width * kq)), max(2, round(g_dau.height * kq))), Image.LANCZOS).convert("RGBA"))
    goc_px = [(dx0, dy0), (dx0 + g_dau.width, dy0), (dx0 + g_dau.width, dy0 + g_dau.height), (dx0, dy0 + g_dau.height)]   # TL, TR, BR, BL
    V_dau = np.array([idle_ve_goc(px_rig(np.array(p, float)) + np.array(LECH["dau"]), "bone65") for p in goc_px])
    ngon = idle_ve_goc(px_rig(np.array(NGON_SUNG_PX)), "bone65")
    # ---- quả tim
    tam_tim, xg_tim, rong_long, nang = cho_tim(by, ten, Wc)
    lp = np.linalg.solve(Wc[xg_tim], np.array([tam_tim[0], tam_tim[1], 1.0]))
    goc_x = float(np.degrees(np.arctan2(Wc[xg_tim][1, 0], Wc[xg_tim][0, 0])))
    sk.xuong("tim", xg_tim, float(lp[0]), float(lp[1]), goc=-goc_x)
    p_tim = os.path.join(M.MANH, "part", "tim.png")
    tong = [0, 0]
    IM = {}
    for s in slots:
        r = by[s]["region"]
        if r not in BO_PART and r not in IM:
            IM[r] = anh_part(r)

    def gan_dau():
        sk.anh("dau", im_dau)
        sk.slot("dau", "move", "dau", an="dau" in AN)
        w_, h_ = im_dau.width, im_dau.height
        Lq = luoi.Luoi(np.array([[0, 0], [w_, 0], [w_, h_], [0, h_]], float), np.array([[0, 1, 2], [0, 2, 3]]), 4, 4, w_, h_, ten="dau")
        sk.luoi_gan("dau", "dau", Lq, [{"bone65": 1.0}] * 4, the_gioi=V_dau)

    def gan_tim():
        if not os.path.exists(p_tim) and not THIEU:
            raise SystemExit("thiếu ảnh " + p_tim)
        if os.path.exists(p_tim):
            g = Image.open(p_tim).convert("RGBA")
            bb = g.getbbox()
            g = g.crop(bb)
        else:
            c_, m_ = M.o_them("tim", 2.0)
            g = Image.fromarray(np.dstack([c_, np.where(m_, 255, 0).astype(np.uint8)]), "RGBA")
        px = 2 * TIM_R * D_PX
        g = anh.loang_mau(g.convert("RGBa").resize((max(2, round(px)), max(2, round(px * g.height / g.width))), Image.LANCZOS).convert("RGBA"))
        sk.anh("tim", g)
        sk.slot("tim", "move", "tim", an="tim" in AN)
        r = TIM_R
        V = np.array([tam_tim + (-r, r), tam_tim + (r, r), tam_tim + (r, -r), tam_tim + (-r, -r)], float)
        Lq = luoi.Luoi(np.array([[0, 0], [g.width, 0], [g.width, g.height], [0, g.height]], float), np.array([[0, 1, 2], [0, 2, 3]]), 4, 4,
                       g.width, g.height, ten="tim")
        sk.luoi_gan("tim", "tim", Lq, [{"tim": 1.0}] * 4, the_gioi=V)

    for s in slots:
        a = by[s]
        r = a["region"]
        if r in BO_PART:
            continue
        sk.slot(s, "move", r, an=s in AN)
        if r not in sk.images:
            sk.anh(r, IM[r])
        L = gan_nguyen(sk, s, r, a, ten, Wc)
        tong[0] += L.n
        tong[1] += len(L.tris)
        if s == "P_shenti_02":
            gan_tim()
        if s == DAU_SAU:
            gan_dau()
    lp = np.linalg.solve(Wc["bone65"], np.array([ngon[0], ngon[1], 1.0]))
    g65 = float(np.degrees(np.arctan2(Wc["bone65"][1, 0], Wc["bone65"][0, 0])))
    sk.xuong("mieng", "bone65", float(lp[0]), float(lp[1]), goc=-g65)           # trục x nằm ngang thế giới ở dáng gốc
    sk.xuong("cau", "mieng", 0.0, 0.0)
    for e, m in (("trung", "khung trúng"), ("dam", "attack: chân dậm xuống đất"), ("tu", "bắt đầu tụ năng lượng"), ("phun", "bắn tia"),
                 ("het_phun", "hết tia"), ("mo", "skill: vỏ ngực bắt đầu mở"), ("dong", "skill: vỏ ngực đóng lại"),
                 ("dap_dat", "appear: đáp xuống đất")):
        sk.su_kien(e, m)
    print(f"{len(sk.bones)} xương, {len(sk.slots)} slot, {tong[0]} đỉnh, {tong[1]} tam giác (lưới của họ); mặt đất y = {dat_y:.1f}; "
          f"tim ở ({tam_tim[0]:.0f}, {tam_tim[1]:.0f}) bám {xg_tim} {[(n, round(w, 2)) for n, w in nang]}, lòng ngực rộng nhất {2 * rong_long:.0f}; "
          f"đỉnh sừng ({ngon[0]:.0f}, {ngon[1]:.0f})")
    return sk, dict(scan=scan, IB=IB, ten=ten, slots=[s["name"] for s in I["slots"]], dat_y=dat_y)


def chuyen_dong(sk, info):
    S = json.load(open(os.path.join(info["scan"], "sample_moi.json"), encoding="utf-8"))
    IB, ten = info["IB"], info["ten"]
    ids = [i for i, n in enumerate(ten) if n in sk.bi and n != "root"]
    out = {}
    for clip, v in S.items():
        fr = v["frames"]
        L = np.array([F["l"] for F in fr], float)                     # (khung, xương, ≥5): x, y, xoay, tỉ lệ x, y
        res = {}
        for i in ids:
            b0 = IB[i]
            A = np.stack([L[:, i, 2] - b0["rot"], L[:, i, 0] - b0["x"], L[:, i, 1] - b0["y"], L[:, i, 3] / (b0["sx"] or 1.0),
                          L[:, i, 4] / (b0["sy"] or 1.0)], 1)
            A[:, 0] = np.degrees(np.unwrap(np.radians(A[:, 0])))
            A[:, 0] -= 360.0 * round((A[0, 0] if clip == "gm_die" else A[-1, 0]) / 360.0)
            if np.abs(A[:, :3]).max() > 1e-3 or np.abs(A[:, 3:] - 1).max() > 1e-4:
                res[ten[i]] = A
        out[clip] = (float(v["dur"]), res)
    return out


def lam_clip(sk, info):
    CD = chuyen_dong(sk, info)
    KR = json.load(open(os.path.join(info["scan"], "kenh_rieng.json"), encoding="utf-8"))

    def kenh(goc, ten_, tau):
        k = KR[goc][ten_]
        x = min(len(k) - 1, max(0.0, tau) * 30.0)
        i0 = int(x)
        i1 = min(i0 + 1, len(k) - 1)
        w = x - i0
        return (np.array(k[i0], float) * (1 - w) + np.array(k[i1], float) * w)

    def dat_dang(P, goc, tau, lap):
        dur, R = CD[goc]
        n = int(round(dur * 30)) + 1
        tq = tau % dur if lap else min(max(tau, 0.0), dur)
        x = tq * 30.0
        i0 = min(int(x), n - 1)
        i1 = min(i0 + 1, n - 1)
        w = x - i0
        for b, A in R.items():
            v = A[min(i0, len(A) - 1)] * (1 - w) + A[min(i1, len(A) - 1)] * w
            if abs(v[0]) > 1e-4:
                P.rot(b, float(v[0]))
            if abs(v[1]) > 1e-4 or abs(v[2]) > 1e-4:
                P.move(b, float(v[1]), float(v[2]))
            if abs(v[3] - 1) > 1e-5 or abs(v[4] - 1) > 1e-5:
                P.scale(b, float(v[3]), float(v[4]))
        bx, by_ = kenh(goc, "bay", tq)
        if abs(bx) > 1e-4 or abs(by_) > 1e-4:
            P.move("move", float(bx), float(by_))
        c = float(kenh(goc, "cau", tq))
        P.scale("cau", max(0.01, c))
        tm = float(kenh(goc, "tim", tq))
        if abs(tm - 1) > 1e-4:
            P.scale("tim", tm)
        return float(kenh(goc, "hien", tq))

    out = []
    for ten_, goc, lap in CLIPS:
        dur = CD[goc][0]
        ev = RC.SU_KIEN.get(goc, [])
        if ten_ == "die":
            def fn(t, P, goc=goc, dur=dur):
                dat_dang(P, goc, t, False)
                a = float(np.clip(1.0 - (t - dur) / (TAN - 0.1), 0.0, 1.0))
                for sl in sk.slots:
                    P.alpha[sl["name"]] = a * P.alpha.get(sl["name"], sl["alpha"])
            out.append(Clip(ten_, dur + TAN, fn, ev=ev))
        elif ten_ == "appear":
            def fn(t, P, goc=goc):
                h = dat_dang(P, goc, t, False)
                if h < 0.999:
                    for sl in sk.slots:
                        P.alpha[sl["name"]] = h * sl["alpha"]
            out.append(Clip(ten_, dur, fn, ev=ev))
        else:
            out.append(Clip(ten_, dur, (lambda t, P, goc=goc, lap=lap: dat_dang(P, goc, t, lap) and None), loop=lap, ev=ev))
    return out, dat_dang


def main(a):
    if a and a[0] == "khop":
        khop(ve=True)
        return
    sk, info = dung()
    clips, dat_dang = lam_clip(sk, info)
    ra = os.environ.get("GM_RA") or os.path.join(G.BASE, "rig")
    if a and a[0] == "soi":
        c = [x for x in clips if x.ten == a[1]][0]
        fr = hoat.nuong(sk, c)
        ts = [float(x) for x in a[2].split(",")]
        ve = soi.Ve(sk)
        Ps = [fr[min(len(fr) - 1, int(round(t * 30)))] for t in ts]
        Bx = soi._union([ve.bao(P) for P in Ps], 0.04)
        sc = float(a[3]) if len(a) > 3 else 1.0
        kw = dict(luoi=True, mau_luoi=(10, 10, 10, 90)) if len(a) > 4 else {}
        ims = [ve.ve(P, Bx, sc, bg=(150, 150, 150), ss=2, **kw).convert("RGB") for P in Ps]
        cot = min(len(ims), 4)
        hang = (len(ims) + cot - 1) // cot
        out = Image.new("RGB", (ims[0].width * cot, ims[0].height * hang), (150, 150, 150))
        for i, im in enumerate(ims):
            out.paste(im, ((i % cot) * im.width, (i // cot) * im.height))
        os.makedirs(ra, exist_ok=True)
        pth = os.path.join(ra, f"soi_{a[1]}.png")
        out.save(pth)
        print(pth, out.size)
        return
    frames = {c.ten: hoat.nuong(sk, c) for c in clips}
    for c in clips:
        if c.ten in VE_NGHI:
            frames[c.ten] = [P.copy() for P in frames[c.ten]]
            hoat.khop_cuoi(frames[c.ten], frames["idle"][0], 0.2)
    cao = soi.chieu_cao(soi.Ve(sk), frames["idle"][0], ("dau", "P_toufa2", "P_toufa3", "P_toufa4", "P_toufa5", "P_beifa_1", "P_beifa_2"))
    if a and a[0] == "duong":                  # đường đi của xương (chia cho chiều cao game) cho VFX: HatGiac.cs chép bảng này
        for clip_, xg, buoc in (("cast", "mieng", 3), ("skill", "tim", 6), ("attack", "TQR_2", 3)):
            fr = frames[clip_]
            pts = [sk.the_gioi(fr[i])[xg][:2, 2] / cao for i in range(0, len(fr), buoc)]
            print(f"{clip_} / {xg}, mỗi {buoc / 30:.2f} s, chia chiều cao {cao:.1f}:")
            print("  " + ", ".join(f"{p[0]:.3f}f, {p[1]:.3f}f" for p in pts))
        return
    xuat.xuat_het(sk, clips, ra, TEN_RIG, "Thú cổ thụ một sừng (giac_moc): tướng thứ 9 đảo Mộc", frames=frames, dang=1, so_dang=1,
                  dung_yen=("attack", "cast", "skill"), ma_goc=None, khop_idle=0, cao=cao, noi_them={}, impact=IMPACT,
                  tol={"rotate": 0.08, "translate": 0.2, "scale": 0.0015}, dich_mb=1.0, tran_mb=1.5)


if __name__ == "__main__":
    main(sys.argv[1:])
