# -*- coding: utf-8 -*-
"""Kỵ sĩ cổ đại bị nguyền (ky_nguyen, rig monster_3642): MẢNH theo concept C đã duyệt (inbox/ky_nguyen_1/tai_ve/L1_duyet.png: vua chiến
trận cổ, giáp sắt đen rỉ nặng viền vàng sờn, mũ vương miện gai, lửa linh hồn xanh, mũi tên + giáo gãy cắm trên giáp, áo choàng đỏ rượu).

Bốn loại tờ (skill pokiclash-spine-rig mục 00; memory khop-noi-gen-lien, reskin-theo-part-goc; mẫu quy_xich_manh.py):
  LIEN : khoảng RỖNG trong giáp (thân, dải dưới vai, hai bắp tay tối) nối nhau → MỘT tờ liền dựng từ rig, GPT vẽ lại sạch (viền chỉ ở
         ngoài), mã nướng vào khung từng part qua lưới.
  K1–K4: mảnh giữ hình bóng gốc (áo choàng, vạt trước, giáp vai, giáp ngực, cẳng tay giáp, giáp tay xa, chùm lông vũ → lửa xanh, sợi sau
         gáy → lửa xanh, khói, nắm tay + ngón, bàn tay xa + ngón): tờ = CHÍNH mảnh gốc cắt theo lưới phóng to; GPT đổi da, giữ hình bóng.
  KT   : gai tinh thể → giáo gãy / mũi tên gãy, đá bay → mảnh khiên vỡ / đầu mũi tên: tờ = mảnh gốc vẽ theo HƯỚNG THẾ GIỚI ở khung 0 idle
         (biết đầu nào cắm vào giáp); GPT vẽ vật mới dọc cùng trục, được phép tràn hình bóng; mảnh cứng một xương, ô 4 đỉnh mới (moi.json).
  R1   : mũ vương miện + kiếm gãy: gen "đúng chỗ, đúng cỡ" trên concept; mũ đặt theo phép căn, kiếm xoay / dời cho chuôi nằm đúng nắm tay rig.
         Mắt xanh cắt thẳng từ concept bằng mã → slot riêng `P_mat` trên xương mũ (appear: mắt bật sáng).

    ky_nguyen_manh.py can        căn concept lên hình con gốc → mau/can.json
    ky_nguyen_manh.py to         dựng mọi tờ hướng dẫn + file prompt → mau/*.png, gui_gpt/ky_nguyen_1/luot_2_*.txt
    ky_nguyen_manh.py cat [tờ]   cắt ảnh về (LIEN / K1..K4 / KT / R1 / MAT) → manh/<vùng>.png, manh/moi.json, tờ so manh/_so_*.png
Ảnh con gốc, mảnh gốc là của game tham khảo: chỉ dùng trong máy làm mẫu, không đăng công khai."""
import json
import math
import os
import sys

import cv2
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ky_nguyen as G  # noqa: E402
from quai.soi import _tris  # noqa: E402
from quai import anh  # noqa: E402

W, H = 1536, 1024
RES = 2                                   # ảnh mảnh của mình = ảnh vùng của họ × RES (atlas họ 0,5 px / đơn vị → mình 1 px / đơn vị)
GUI = os.path.join(HERE, "gui_gpt", "ky_nguyen_1")
CON = os.path.join(G.TAI, "L1_duyet.png")
SOI_GIAP = os.path.join(HERE, "inbox", "soi_giap_1", "tai_ve", "L1_duyet.png")
MANH = os.path.join(G.BASE, "manh")
INK = (43, 33, 24)
MUC = "#2B2118"

# màu đo trên concept C (trung vị ô 7 × 7)
MAU = dict(giap="#5A5352", giap_toi="#45403F", ri="#9B542F", vang="#A87C43", void="#2A2C25", lua="#84CD39", lua_nhat="#D3F495",
           mat="#8DD246", ao="#652831", go="#865438", long_ten="#B8B5B5", mui="#9E9B9C", gang="#4B474B", gang_toi="#3A3637")


def Wp(p):
    return os.path.normpath(p)


def ghi(p, lines):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def mat_na(rgb, nguong=28):
    m = ((255 - rgb.astype(np.int16)).max(2) > nguong).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, el(2))
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    k = np.zeros_like(m)
    cv2.drawContours(k, [c for c in cs if cv2.contourArea(c) > 400], -1, 1, -1)
    return k.astype(bool)


def _hex(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], np.int32)


# ================================================================ căn concept lên rig
def can():
    """tìm phép đồng dạng (tâm khung, tỉ lệ a, dời d) đưa hình con gốc (goc_ca_con) trùng hình bóng concept nhất."""
    g = mat_na(np.asarray(Image.open(os.path.join(G.MAU, "goc_ca_con.png")).convert("RGB")))
    c = mat_na(np.asarray(Image.open(CON).convert("RGB").resize((W, H))))
    k = 4
    gs = cv2.resize(g.astype(np.uint8), (W // k, H // k), interpolation=cv2.INTER_AREA)
    cs = cv2.resize(c.astype(np.uint8), (W // k, H // k), interpolation=cv2.INTER_AREA).astype(bool)
    C = np.array([W / 2, H / 2]) / k
    best = (0, 1.0, 0.0, 0.0)

    def thu(a, dx, dy):
        M = np.array([[a, 0, C[0] - a * C[0] + dx / k], [0, a, C[1] - a * C[1] + dy / k]], np.float32)
        w = cv2.warpAffine(gs, M, (W // k, H // k), flags=cv2.INTER_NEAREST).astype(bool)
        return (w & cs).sum() / max(1, (w | cs).sum())
    for a in np.arange(0.92, 1.121, 0.01):
        for dx in range(-48, 49, 4):
            for dy in range(-48, 49, 4):
                v = thu(a, dx, dy)
                if v > best[0]:
                    best = (v, a, dx, dy)
    _, a0, x0, y0 = best
    for a in np.arange(a0 - 0.01, a0 + 0.0101, 0.0025):
        for dx in range(int(x0) - 4, int(x0) + 5):
            for dy in range(int(y0) - 4, int(y0) + 5):
                v = thu(a, dx, dy)
                if v > best[0]:
                    best = (v, a, dx, dy)
    v, a, dx, dy = best
    gj = json.load(open(os.path.join(G.MAU, "goc_ca_con.json")))
    out = dict(iou=round(float(v), 4), a=float(a), dx=float(dx), dy=float(dy), s=gj["s"], cx=gj["cx"], cy=gj["cy"])
    json.dump(out, open(os.path.join(G.MAU, "can.json"), "w"), indent=1)
    print("căn:", out)
    return out


def phep_can():
    """(T: thế giới dáng gốc → px concept, Ti: ngược lại, px concept / đơn vị)."""
    j = json.load(open(os.path.join(G.MAU, "can.json")))
    s, cx, cy, a, dx, dy = j["s"], j["cx"], j["cy"], j["a"], j["dx"], j["dy"]
    C = np.array([W / 2, H / 2])

    def T(V):
        V = np.asarray(V, float).reshape(-1, 2)
        P = np.stack([W / 2 + (V[:, 0] - cx) * s, H / 2 - (V[:, 1] - cy) * s], 1)
        return C + a * (P - C) + np.array([dx, dy])

    def Ti(P):
        P = (np.asarray(P, float).reshape(-1, 2) - np.array([dx, dy]) - C) / a + C
        return np.stack([cx + (P[:, 0] - W / 2) / s, cy - (P[:, 1] - H / 2) / s], 1)
    return T, Ti, s * a


# ================================================================ dáng gốc: từng part trên khung concept
_CK = {}


def lop_goc():
    """{slot: (att, mặt nạ bool trên khung concept)} các hình đang bật ở khung 0 idle, theo thứ tự vẽ; + bản đồ slot trên cùng."""
    if "lop" in _CK:
        return _CK["lop"]
    T, _, _ = phep_can()
    G._C.pop("att", None)
    _, imgs, atts = G.nap("att_idle0.json")
    atts = [a for a in atts if a.get("region")]
    lop = {}
    top = np.full((H, W), -1, np.int32)
    for k, a in enumerate(atts):
        im = G.part_goc(a)
        uv, tr = G.luoi(a)
        lay = Image.new("RGBa", (W, H), (0, 0, 0, 0))
        _tris(lay, im.convert("RGBa"), T(np.array(a["xy"], float).reshape(-1, 2)), uv, tr)
        m = np.asarray(lay)[..., 3] > 110
        lop[a["slot"]] = (a, m)
        top[m] = k
    _CK["lop"] = (lop, top, [a["slot"] for a in atts])
    return _CK["lop"]


# ================================================================ LIEN: khoảng rỗng liền
LIEN = [("rong", ["P_shenti_1", "P_shenti_9", "P_z_dabi", "P_y_dabi"])]
BANG = {s_: ("void", "lua", "lua_nhat") for s_ in LIEN[0][1]}


def to_lien():
    lop, top, thu_tu = lop_goc()
    Cn = np.asarray(Image.open(CON).convert("RGB").resize((W, H), Image.LANCZOS))
    trang = Cn.min(2) > 236
    ten_mau = list(MAU)
    pal = np.stack([_hex(MAU[k]) for k in ten_mau])
    d = np.linalg.norm(Cn[..., None, :].astype(np.int32) - pal[None, None], axis=-1)
    gan_nhat = np.where(d.min(-1) < 40, d.argmin(-1), -1)
    can_ = np.full((H, W, 3), 255, np.uint8)
    info = {}
    for ten, ds in LIEN:
        m = np.zeros((H, W), bool)
        for s_ in ds:
            m |= lop[s_][1]
        m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_CLOSE, el(3)).astype(bool)
        idx = [thu_tu.index(s_) for s_ in ds]
        cua_minh = np.isin(top, idx)
        che = m & ~cua_minh & (top >= 0)
        hop_le = np.zeros((H, W), bool)
        for s_ in ds:
            hop_le |= (top == thu_tu.index(s_)) & np.isin(gan_nhat, [ten_mau.index(c) for c in BANG[s_]])
        nguon = m & ~trang & hop_le
        nguon &= ~cv2.dilate(che.astype(np.uint8), el(7)).astype(bool)
        nguon &= cv2.erode(m.astype(np.uint8), el(9)).astype(bool)
        g = np.zeros((H, W, 3), np.uint8)
        g[m] = _hex(MAU["void"])
        g[nguon] = Cn[nguon]
        g[m & ~cv2.erode(m.astype(np.uint8), el(3.5)).astype(bool)] = INK
        can_[m] = g[m]
        info[ten] = dict(slots=ds, off=[0, 0], phu=round(float(nguon.sum()) / max(1, m.sum()), 3))
        print(f"  {ten:9s} concept lộ {info[ten]['phu']:.0%} hình bóng")
    os.makedirs(G.MAU, exist_ok=True)
    Image.fromarray(can_).save(os.path.join(G.MAU, "lien.png"))
    json.dump(info, open(os.path.join(G.MAU, "lien.json"), "w"), indent=1)
    print(os.path.join(G.MAU, "lien.png"))
    return info


R_CON = ("the APPROVED picture of OUR character, 1536x1024, white background: an ancient cursed knight floating with no legs, turned to "
         "the right: blackened rusty iron armour with worn gold rims, a tall helm with a jagged iron crown and green soul fire rising out "
         "of it, two green eyes in a vertical slit, broken arrows and a broken spear stuck in the armour, a long sword cut on the chest "
         "with green fire inside, a faded wine-red torn cape, a big gauntlet holding a broken rusty sword with a ring crossguard and a "
         "green gem in the pommel, an open iron hand on the right. It gives the design, the colours, the ink line and the crayon hatching.")


def prompt_lien():
    gd = os.path.join(G.MAU, "lien.png")
    out = os.path.join(G.TAI, "N_lien.png")
    p = os.path.join(GUI, "luot_2_rong_lien.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {Wp(CON)}: {R_CON}",
         f"image 2 = {Wp(gd)}: VOID GUIDE, 1536x1024, white background, assembled by computer from image 1: ONE flat dark shape with a "
         "dark outline: the HOLLOW INSIDE of the empty armour (the dark void torso, the dark band under the big shoulder, the dark upper "
         "arm under the big shoulder on the left and the dark upper arm reaching to the right). In the knight it is hidden behind the "
         "armour plates almost everywhere; only its edges show between the plates.",
         "", f"SAVE: save it as a PNG to {Wp(out)}",
         "If a file with that name already exists, save as N_lien_2.png, N_lien_3.png ... in the same folder. Do not edit, move or "
         "delete any other file.", "",
         "TASK: redraw image 2 cleanly in the hand-drawn style of image 1, landscape 1536x1024, pure-white background. Keep EXACTLY the "
         "silhouette of image 2: the same outline, the same size, the same position (if your picture were laid over image 2, the shape "
         "must coincide). This sheet will be cut by a program into the body parts of a 2D animation puppet.", "",
         "VERY IMPORTANT, ONE CONTINUOUS SURFACE: draw the dark-brown ink outline ONLY around the OUTSIDE of the shape. Inside it draw no "
         "line where the arms meet the torso: no folds, no seams, no cut lines.", "",
         f"- FILL: flat near-black void {MAU['void']} everywhere, with visible crayon hatching as texture. Add only SIX to EIGHT small "
         f"GREEN SOUL-FIRE TONGUES ({MAU['lua']} with a pale {MAU['lua_nhat']} inner stroke, each with a thin ink outline) rising from the "
         "UPPER edge of the shape (on the band under the shoulder and on the top of the torso), small, pointing up, inside the silhouette.",
         f"- OUTLINE: dark-brown ink ({MUC}), about 7 px thick, wobbly like a real pen, closed around the shape, lying just INSIDE its edge.",
         "Draw nothing else: no armour, no helmet, no cape, no hands, no sword, no arrows, no ground.", "",
         "FLAT COLOUR, NO LIGHT, NO SHADOW: one even colour, the crayon strokes are texture only. No shading, no highlights, no gradients, "
         "no glow. Pure white (#FFFFFF) background; no text, no labels, no frames."]
    ghi(p, t)
    print(p)
    return p, gd, out


def _the_gioi_o(a, w, h):
    """toạ độ thế giới (khung 0 idle) của từng pixel trong khung ảnh vùng (w × h) của một part, qua lưới của nó; NaN ngoài lưới."""
    uv, tr = G.luoi(a)
    im = G.part_goc(a)
    U = uv / np.array([im.width, im.height], float) * np.array([w, h])
    V = np.array(a["xy"], float).reshape(-1, 2)
    ys, xs = np.mgrid[0:h, 0:w]
    P = np.c_[xs.ravel() + 0.5, ys.ravel() + 0.5]
    Wd = np.full((len(P), 2), np.nan)
    tot = np.full(len(P), -9.0)
    for t in np.asarray(tr).reshape(-1, 3):
        A_, B_, C_ = U[t[0]], U[t[1]], U[t[2]]
        v0, v1, v2 = B_ - A_, C_ - A_, P - A_
        den = v0[0] * v1[1] - v0[1] * v1[0]
        den = den if abs(den) > 1e-9 else 1e-9
        b1 = (v2[:, 0] * v1[1] - v2[:, 1] * v1[0]) / den
        b2 = (v0[0] * v2[:, 1] - v0[1] * v2[:, 0]) / den
        b0 = 1 - b1 - b2
        tol = 6.0 / max(1.0, float(np.sqrt(abs(den))))
        nho = np.minimum(np.minimum(b0, b1), b2)
        hon = (nho >= -tol) & (nho > tot)
        Wd[hon] = b0[hon, None] * V[t[0]] + b1[hon, None] * V[t[1]] + b2[hon, None] * V[t[2]]
        tot[hon] = nho[hon]
    return Wd.reshape(h, w, 2)


def cat_lien():
    path = anh.to_moi_nhat(G.TAI, "N_lien")
    if not path:
        print("LIEN: chưa gen")
        return
    T, _, _ = phep_can()
    L = json.load(open(os.path.join(G.MAU, "lien.json"), encoding="utf-8"))
    im = Image.open(path).convert("RGB")
    if im.size != (W, H):
        im = im.resize((W, H), Image.LANCZOS)
        path = os.path.join(G.MAU, "_N_lien_doi_co.png")
        im.save(path)
    tt = anh.doc_to(path, dien_tich_min=600, gop_px=10)
    rgba = tt.rgba.astype(np.float32)
    rgba[..., :3] *= rgba[..., 3:4] / 255.0
    lop, _, _ = lop_goc()
    os.makedirs(MANH, exist_ok=True)
    print("LIEN:", os.path.basename(path))
    so = []
    for ten, d in L.items():
        dx, dy = d["off"]
        for s_ in d["slots"]:
            a = lop[s_][0]
            goc = G.part_goc(a)
            w, h = goc.width * RES, goc.height * RES
            Wd = _the_gioi_o(a, w, h)
            ok = ~np.isnan(Wd[..., 0])
            P = T(np.nan_to_num(Wd.reshape(-1, 2))).reshape(h, w, 2)
            mx = np.where(ok, P[..., 0] + dx, -10).astype(np.float32)
            my = np.where(ok, P[..., 1] + dy, -10).astype(np.float32)
            cell = cv2.remap(rgba, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
            al = cell[..., 3:4]
            cell[..., :3] = np.where(al > 1, cell[..., :3] * 255.0 / np.maximum(al, 1), 0)
            sil = np.asarray(goc.resize((w, h), Image.LANCZOS))[..., 3] > 60
            sil = cv2.dilate(sil.astype(np.uint8), el(3)).astype(np.float32)
            sil = np.clip(cv2.GaussianBlur(sil, (0, 0), 1.2) * 2.0 - 0.5, 0.0, 1.0)
            cell[..., 3] *= sil
            out = np.clip(cell, 0, 255).astype(np.uint8)
            Image.fromarray(out, "RGBA").save(os.path.join(MANH, a["region"] + ".png"))
            so.append(Image.fromarray(out, "RGBA"))
            print(f"  {s_:12s} → {a['region']}.png {w}×{h}")
    _to_so(so, os.path.join(MANH, "_so_LIEN.png"))


def _to_so(ims, p):
    w_ = sum(i.width + 10 for i in ims) + 10
    h_ = max(i.height for i in ims) + 20
    o = Image.new("RGB", (w_, h_), (150, 150, 150))
    x = 10
    for i in ims:
        o.paste(i, (x, 10), i)
        x += i.width + 10
    o.save(p)
    print(p)


# ================================================================ K: mảnh rời giữ hình bóng gốc (tờ = mảnh gốc phóng to)
_GIAP = f"blackened rusty iron {MAU['giap']} (faces turned away darker {MAU['giap_toi']}) with 2 or 3 flat rust patches {MAU['ri']}"
_LUA_T = (f"a TONGUE OF GREEN SOUL FIRE of exactly this shape: flat bright green {MAU['lua']} with ONE pale green {MAU['lua_nhat']} inner "
          "tongue following its shape, ink outline all round; no feather lines")
TO_K = {
    "K1": [[("P_pifeng01", 1.9), ("P_pifeng00", 2.6)]],
    "K2": [[("P_jianjia", 2.1), ("P_xiongjia01", 2.3), ("P_y_xiaobi", 2.1)],
           [("P_xiongjia00", 3.6), ("P_z_xiaobi", 3.0)]],
    "K3": [[("P_yumao00", 3.4), ("P_yumao01", 3.4), ("P_yumao02", 3.4), ("P_yumao03", 3.4), ("P_yumao04", 3.4)],
           [("P_shenti_2", 5.0), ("P_shenti_3", 5.0), ("P_shenti_4", 5.0), ("P_shenti_5", 5.0), ("P_shenti_6", 5.0), ("P_shenti_7", 5.0),
            ("P_shenti_8", 5.0)]],
    "K4": [[("P_y_shou", 3.6), ("P_y_shouzhi00", 3.6), ("P_y_shouzhi01", 3.6), ("P_y_shouzhi02", 3.6), ("P_y_shouzhi03", 3.6),
            ("P_y_shouzhi04", 3.6)],
           [("P_z_shou", 3.6), ("P_z_shouzhi00", 3.6), ("P_z_shouzhi01", 3.6), ("P_z_shouzhi02", 3.6), ("P_z_shouzhi03", 3.6),
            ("P_z_shouzhi04", 3.6), ("P_z_shouzhi05", 3.6), ("P_z_shouzhi06", 3.6)]],
}
MO_TA_K = {
    "P_pifeng01": f"THE BIG TORN CAPE (hanging from behind the shoulders, its lower edge torn into ragged strips): faded dark WINE-RED cloth "
                  f"{MAU['ao']}, a frayed worn GOLD border {MAU['vang']} (a band about 16 px wide) running along its torn lower edges, a "
                  "few thin fold lines where image 1 has them. Keep every ragged strip and hole exactly; no purple, no gradient.",
    "P_pifeng00": f"THE TABARD (a long narrow cloth strip hanging down, its lower end torn): dark wine-red {MAU['ao']} with a worn gold "
                  f"border {MAU['vang']} along both long edges; no pattern, no sigil.",
    "P_jianjia": f"THE BIG SHOULDER PAULDRON (several overlapping curved plates, flanges rising behind): {_GIAP}, a thin worn gold rim "
                 f"{MAU['vang']} along the lower edge of each plate (broken in places); the leaf-shaped flanges at the back become JAGGED "
                 "BROKEN iron plate edges inside the same outline; no white, no leaves, no scrolls.",
    "P_xiongjia01": f"THE CHEST PLATE (a breastplate with a pointed lower edge): {_GIAP}, a thin worn gold rim {MAU['vang']} round its "
                    f"edge, and ONE long diagonal SWORD CUT across it from the upper right to the lower left: inside the cut flat green "
                    f"soul fire {MAU['lua']} with a pale {MAU['lua_nhat']} middle stroke. No emblem, no wings.",
    "P_y_xiaobi": f"THE BIG NEAR VAMBRACE (an armoured forearm, flanges at its top, a cuff at its lower end): {_GIAP}, worn gold bands "
                  f"{MAU['vang']} at its top rim and its lower cuff; on its front face ONE green rune {MAU['lua']}: a circle with one "
                  "slanted line through it, a thick flat green line with ink outline (instead of the purple mark). No white.",
    "P_xiongjia00": f"A SMALL ARMOUR PLATE: blackened iron {MAU['giap_toi']} with a thin worn gold rim {MAU['vang']}.",
    "P_z_xiaobi": f"THE FAR BRACER (a forearm with bands): {_GIAP}, two worn gold bands {MAU['vang']} (instead of the white bandage).",
    "P_yumao00": _LUA_T + ".", "P_yumao01": _LUA_T + ".", "P_yumao02": _LUA_T + ".", "P_yumao03": _LUA_T + ".", "P_yumao04": _LUA_T + ".",
    "P_shenti_2": f"a small GREEN FLAME WISP of exactly this shape: flat green {MAU['lua']}, ink outline.",
    "P_shenti_3": f"a small GREEN FLAME WISP: flat green {MAU['lua']} with a pale {MAU['lua_nhat']} inner stroke, ink outline.",
    "P_shenti_4": f"a small GREEN FLAME WISP: flat green {MAU['lua']}, ink outline.",
    "P_shenti_5": f"a small GREEN FLAME WISP: flat green {MAU['lua']} with a pale {MAU['lua_nhat']} inner stroke, ink outline.",
    "P_shenti_6": f"a tiny GREEN FLAME WISP: flat green {MAU['lua']}, ink outline.",
    "P_shenti_7": f"a tiny GREEN FLAME WISP: flat green {MAU['lua']}, ink outline.",
    "P_shenti_8": f"a small GREEN FLAME WISP: flat green {MAU['lua']}, ink outline.",
    "P_yanwu": f"a rising wisp of DARK SMOKE: flat charcoal grey #3E423C with two thin green {MAU['lua']} streaks along it, soft wavy "
               "ink outline.",
    "P_y_shou": f"THE BACK OF THE NEAR ARMOURED HAND (a gauntlet): blackened iron {MAU['gang']}, knuckle plate lines, one rust patch "
                f"{MAU['ri']}. No white.",
    "P_y_shouzhi00": f"an ARMOURED FINGER of the near gauntlet (two or three small plates): blackened iron {MAU['gang']}, plate lines.",
    "P_y_shouzhi01": f"an ARMOURED FINGER of the near gauntlet: blackened iron {MAU['gang']}, plate lines.",
    "P_y_shouzhi02": f"an ARMOURED FINGER of the near gauntlet: blackened iron {MAU['gang']}, plate lines.",
    "P_y_shouzhi03": f"an ARMOURED THUMB piece of the near gauntlet: blackened iron {MAU['gang']}, plate lines.",
    "P_y_shouzhi04": f"an ARMOURED THUMB tip of the near gauntlet: blackened iron {MAU['gang']}.",
    "P_z_shou": f"THE FAR OPEN HAND (an armoured hand, palm towards the viewer): blackened iron gauntlet {MAU['gang']}, the palm darker "
                f"{MAU['gang_toi']}, one rust patch {MAU['ri']}. No purple.",
    "P_z_shouzhi00": f"an ARMOURED FINGER of the far hand with a pointed tip: blackened iron {MAU['gang']}, segment lines. No purple.",
    "P_z_shouzhi01": f"an ARMOURED FINGER of the far hand with a pointed tip: blackened iron {MAU['gang']}, segment lines.",
    "P_z_shouzhi02": f"an ARMOURED FINGER of the far hand with a pointed tip: blackened iron {MAU['gang']}, segment lines.",
    "P_z_shouzhi03": f"an ARMOURED FINGER of the far hand with a pointed tip: blackened iron {MAU['gang']}, segment lines.",
    "P_z_shouzhi04": f"an ARMOURED FINGER segment of the far hand: blackened iron {MAU['gang']}.",
    "P_z_shouzhi05": f"an ARMOURED FINGER segment of the far hand: blackened iron {MAU['gang']}.",
    "P_z_shouzhi06": f"an ARMOURED FINGER segment of the far hand: blackened iron {MAU['gang']}.",
}
VI_K = {"K1": "áo choàng lớn + vạt trước (đỏ rượu, viền vàng sờn)",
        "K2": "giáp vai, giáp ngực (vết chém lửa xanh), cẳng tay giáp (ấn Ø xanh), mảnh giáp nhỏ, giáp tay xa",
        "K3": "năm lông vũ → năm lưỡi lửa xanh, bảy sợi sau gáy → lửa xanh nhỏ",
        "K4": "mu bàn tay gần + năm ngón, bàn tay xa + bảy ngón (găng sắt đen)"}
TA_K = {"K1": "two parts: on the left a big torn cape, on the right a long narrow cloth strip",
        "K2": "five parts: top row a big shoulder pauldron, a chest plate, a big armoured forearm; bottom row a small armour plate, a "
              "banded forearm",
        "K3": "twelve parts: top row five feathers of a helmet crest; bottom row seven small dark wisps",
        "K4": "fourteen parts drawn very big: top row the back of a gauntlet hand and five finger pieces; bottom row an open hand and "
              "seven finger pieces"}


def vung():
    """{slot / vùng: (att, ảnh part cắt theo lưới)} theo dáng gốc (att_goc)."""
    G._C.pop("att", None)
    _, imgs, _ = G.nap("att_goc.json")
    D = json.load(open(os.path.join(G.scan(), "att_goc.json"), encoding="utf-8"))
    atts = sorted([a for a in D["atts"] if a.get("region") in imgs], key=lambda a: (not a["cur"], a["order"]))   # cả hình ẩn (khói die)
    out = {}
    for a in atts:                                        # tên slot trước (vùng dùng chung: P_jianjia của slot P_jianjia, không của P_jianjia2)
        out.setdefault(a["slot"], (a, G.part_goc(a)))
    for a in atts:
        out.setdefault(a["region"], out.get(a["region"]) or (a, G.part_goc(a)))
    return out


def to_k(ma):
    V = vung()
    can_ = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    o = {}
    cao = []
    for h_ in TO_K[ma]:
        cs = []
        for r, z in h_:
            im = V[r][1]
            big = im.resize((int(round(im.width * z)), int(round(im.height * z))), Image.LANCZOS)
            cs.append((r, z, big))
        cao.append((cs, max(c[2].height for c in cs)))
    ke_y = (H - sum(c[1] for c in cao)) // (len(cao) + 1)
    y = ke_y
    for cs, hh in cao:
        ke = (W - sum(c[2].width for c in cs)) // (len(cs) + 1)
        assert ke >= 8 and ke_y >= 8, (ma, ke, ke_y)
        x = ke
        for r, z, big in cs:
            y0 = y + (hh - big.height) // 2
            can_.alpha_composite(big, (x, y0))
            o[r] = dict(hop=[x, y0, big.width, big.height], z=z, vung=V[r][0]["region"])
            x += big.width + ke
        y += hh + ke_y
    p = os.path.join(G.MAU, f"goc_{ma}.png")
    can_.convert("RGB").save(p)
    json.dump(o, open(p[:-4] + ".json", "w", encoding="utf-8"), indent=1)
    print(p)
    return o


def prompt_k(ma, o):
    mau = os.path.join(G.MAU, f"goc_{ma}.png")
    out = os.path.join(G.TAI, f"D_{ma}.png")
    p = os.path.join(GUI, f"luot_2_da_{ma}.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {Wp(mau)}: the PARTS SHEET, 1536x1024, white background: separate parts of a 2D animation puppet (a floating "
         f"armoured knight), each drawn alone, at the exact size and place to keep: {TA_K[ma]}. They are painted in a smooth white, gold "
         "and purple digital style.",
         f"image 2 = {Wp(CON)}: {R_CON} Take from it the colours, the materials and the hand-drawn look. The shapes come from image 1.",
         f"image 3 = {Wp(SOI_GIAP)}: another approved hero of the same game: the hand-drawn ink and crayon style and the flat colouring of "
         "dark iron to match. Do NOT copy its design.",
         "", f"SAVE: save it as a PNG to {Wp(out)}",
         f"If a file with that name already exists, save as D_{ma}_2.png, D_{ma}_3.png ... in the same folder. Do not edit, move or "
         "delete any other file.", "",
         "TASK: RESKIN. Redraw the SAME sheet with every part REPAINTED as described below, so that the parts can be put back on the same "
         "puppet. For EVERY part keep exactly: its silhouette (the same outline), its size, its orientation and its place on the sheet "
         "(if the new picture were laid over image 1, every part must coincide with the old one), and its main structural lines. Do NOT "
         "merge parts, do NOT add parts, do NOT move parts. Pure white (#FFFFFF) between the parts.", "",
         f"NEW LOOK (see image 2 for the exact colours and drawing style): hand-drawn on paper: a wobbly dark-brown ink outline ({MUC}, "
         "about 9 px) running all the way round every part exactly on its silhouette, thinner ink lines for the inner lines, and every "
         "area filled with ONE flat colour with visible coloured-pencil / wax-crayon hatching. The parts of image 1 are painted in a "
         "smooth digital cel style with white, gold and purple colours and soft light and dark planes: do NOT copy that painting style or "
         "those colours; no shading, no highlights, no white shine streaks, no gradients, no glow, no shadows: flat colour only. VERY "
         "SIMPLE: no extra details.", "",
         "THE PARTS (coordinates are pixels on the 1536x1024 sheet, x from the left, y from the top):"]
    for i, (r, d) in enumerate(o.items(), 1):
        x, y, cw, ch = d["hop"]
        t.append(f"{i}. (about x = {x} to x = {x + cw}, y = {y} to y = {y + ch}) {MO_TA_K[r]}")
    t += ["", "Plain pure-white background (#FFFFFF), no paper grain outside the parts, no labels, no numbers, no frame, nothing added."]
    ghi(p, t)
    print(p)
    return p, mau, out


def nen_trang(A):
    trang = (A.min(2) > 238).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(trang, 4)
    bg = np.zeros(trang.shape, bool)
    Hh, Ww = trang.shape
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if x == 0 or y == 0 or x + w == Ww or y + h == Hh:
            bg |= lab == i
    return bg


def cat_k(ma):
    path = anh.to_moi_nhat(G.TAI, f"D_{ma}")
    if not path:
        print(f"{ma}: chưa gen")
        return
    V = vung()
    os.makedirs(MANH, exist_ok=True)
    pj = os.path.join(MANH, "_iou.json")
    ious = json.load(open(pj)) if os.path.exists(pj) else {}
    A = np.asarray(Image.open(path).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
    print(f"{ma}:", os.path.basename(path))
    o = json.load(open(os.path.join(G.MAU, f"goc_{ma}.json"), encoding="utf-8"))
    Gd = np.asarray(Image.open(os.path.join(G.MAU, f"goc_{ma}.png")).convert("RGB")).astype(np.int32)
    fg = ~nen_trang(A)
    fgG = ~nen_trang(Gd)
    n, lab, st, _ = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
    so = []
    for r, d in o.items():
        x, y, cw, ch = d["hop"]
        pad = 14
        x0, y0, x1, y1 = max(0, x - pad), max(0, y - pad), min(W, x + cw + pad), min(H, y + ch + pad)
        gm = cv2.dilate(fgG[y0:y1, x0:x1].astype(np.uint8), el(10)).astype(bool)
        sub = lab[y0:y1, x0:x1]
        ids = [i for i in np.unique(sub[gm]) if i > 0 and st[i, 4] > 60]
        m = np.isin(lab, ids)
        m[:y0] = m[y1:] = False
        m[:, :x0] = m[:, x1:] = False
        rgb = A[y:y + ch, x:x + cw].astype(np.uint8)
        mm = m[y:y + ch, x:x + cw]
        al = cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.8)
        vien = mm & ~cv2.erode(mm.astype(np.uint8), el(2)).astype(bool)
        sang = rgb.min(2).astype(np.float32)
        al = np.where(vien, np.minimum(al, np.clip((250.0 - sang) / 70.0, 0, 1)), al)
        im = Image.fromarray(np.dstack([rgb, (np.clip(al, 0, 1) * 255).astype(np.uint8)]), "RGBA")
        goc = V[r][1]
        tw, th = goc.width * RES, goc.height * RES
        im2 = im.convert("RGBa").resize((tw, th), Image.LANCZOS).convert("RGBA")
        a2 = np.asarray(im2).copy()
        ag = np.asarray(goc.resize((tw, th), Image.LANCZOS))[..., 3] > 60
        gioi = cv2.dilate(ag.astype(np.uint8), el(3)).astype(bool)
        a2[..., 3] = np.where(gioi, a2[..., 3], 0)
        a2[..., 3] = np.where(~ag & (a2[..., :3].min(2) > 230), 0, a2[..., 3])
        thieu = ag & (a2[..., 3] < 128) & cv2.dilate((a2[..., 3] >= 128).astype(np.uint8), el(5)).astype(bool)
        if thieu.any() and (a2[..., 3] >= 128).any():
            co = (a2[..., 3] >= 128).astype(np.uint8)
            _, lbl = cv2.distanceTransformWithLabels(1 - co, cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
            ys_, xs_ = np.nonzero(co)
            bang = np.zeros((lbl.max() + 1, 3), np.uint8)
            bang[lbl[ys_, xs_]] = a2[ys_, xs_, :3]
            a2[thieu, :3] = bang[lbl[thieu]]
            a2[thieu, 3] = 255
        Image.fromarray(a2, "RGBA").save(os.path.join(MANH, d["vung"] + ".png"))
        b = fgG[y:y + ch, x:x + cw]
        iou = float((mm & b).sum()) / max(1, (mm | b).sum())
        ious[r] = round(iou, 3)
        so.append(Image.fromarray(a2, "RGBA"))
        print(f"  {r:14s} → {d['vung']}.png  IoU {iou:.3f}  vá hụt {int(thieu.sum())} px")
    json.dump(ious, open(pj, "w"), indent=1)
    _to_so(so, os.path.join(MANH, f"_so_{ma}.png"))


# ================================================================ KT: gai → giáo / mũi tên, đá → mảnh khiên (hướng thế giới, mảnh cứng)
_TEN = (f"a BROKEN ARROW stuck in the armour: a thin round wooden SHAFT {MAU['go']} starting at the BASE end (the arrow head is buried in "
        f"the armour there, not visible) and, near the TIP end, grey FEATHER FLETCHING {MAU['long_ten']} (two or three flat vanes with "
        "one ink line each); the tip end of the shaft cut straight")
_DAM = f"a small broken wooden ARROW SPLINTER {MAU['go']} with a jagged splintered end"
_KHIEN = (f"a small floating BROKEN PIECE of an old iron SHIELD (an irregular flat shard): rusty iron {MAU['giap']} with one rust patch "
          f"{MAU['ri']} and a worn gold rim {MAU['vang']} along one of its edges")
_DAU_TEN = f"a loose iron ARROWHEAD: a flat pointed triangle with two small barbs, grey iron {MAU['mui']} with one middle ridge line"
KT = [[("P_ci07", 1.5, f"a BROKEN SPEAR stuck in the armour: at the BASE end its grey iron spear-head {MAU['mui']} is half buried (only "
                       f"its wide upper half shows), and the long round wooden SHAFT {MAU['go']} runs from it all along the shard to the "
                       "TIP end, where it is BROKEN with a jagged splintered end (pale broken wood)"),
       ("P_ci08", 1.5, f"a SPEAR HEAD that has pierced through the armour from behind: at the BASE end a short piece of wooden shaft "
                       f"{MAU['go']}, then along the rest of the shard a pointed leaf-shaped grey iron spear-head {MAU['mui']} with one "
                       "middle ridge line, its point at the TIP end"),
       ("P_ci02", 1.7, _TEN), ("P_ci00", 1.7, _TEN), ("P_ci03", 2.0, _TEN)],
      [("P_ci04", 2.0, _TEN), ("P_ci05", 2.4, _TEN), ("P_ci06", 2.4, _TEN), ("P_ci11", 2.0, _TEN), ("P_ci09", 2.4, _TEN),
       ("P_ci01", 2.4, _DAM), ("P_ci10", 2.4, _DAM), ("P_ci12", 2.0, _DAM)],
      [("P_shitou00", 1.6, _KHIEN), ("P_shitou01", 1.6, _KHIEN), ("P_shitou02", 1.6, _DAU_TEN), ("P_shitou03", 1.6, _KHIEN),
       ("P_shitou04", 1.6, _DAU_TEN)]]
PAD_KT = 26                               # px quanh mỗi mảnh trên tờ (GPT được vẽ tràn hình bóng vào đây)


def _huong(v):
    """tên hướng (y ảnh hướng xuống)."""
    a = math.degrees(math.atan2(-v[1], v[0])) % 360
    ten = ["RIGHT", "UPPER RIGHT", "UP", "UPPER LEFT", "LEFT", "LOWER LEFT", "DOWN", "LOWER RIGHT"]
    return ten[int(((a + 22.5) % 360) // 45)]


def to_kt():
    """mỗi mảnh vẽ theo hướng thế giới ở khung 0 idle, phóng z px / đơn vị; ghi gốc toạ độ để cắt về thế giới."""
    G._C.pop("att", None)
    _, imgs, atts = G.nap("att_idle0.json")
    D = json.load(open(os.path.join(G.scan(), "att_idle0.json"), encoding="utf-8"))
    BW = {b["name"]: np.array([b["x"], b["y"]]) for b in D["bones"]}
    by = {a["slot"]: a for a in atts}
    o = {}
    hang = []

    def ve(sl, z, mt):
        a = by[sl]
        if True:
            V = np.array(a["xy"], float).reshape(-1, 2)
            x0w, y0w, x1w, y1w = V[:, 0].min(), V[:, 1].min(), V[:, 0].max(), V[:, 1].max()
            cw, ch = int(math.ceil((x1w - x0w) * z)) + 2 * PAD_KT, int(math.ceil((y1w - y0w) * z)) + 2 * PAD_KT
            T = (lambda Q, x0w=x0w, y1w=y1w, z=z: np.stack([(Q[:, 0] - x0w) * z + PAD_KT, (y1w - Q[:, 1]) * z + PAD_KT], 1))
            uv, tr = G.luoi(a)
            lay = Image.new("RGBa", (cw, ch), (0, 0, 0, 0))
            _tris(lay, G.part_goc(a).convert("RGBa"), T(V), uv, tr)
            lay = lay.convert("RGBA")
            # đầu cắm vào giáp = đầu trục chính gần gốc xương nhất
            al = np.asarray(lay)[..., 3] > 60
            ys, xs = np.nonzero(al)
            P = np.c_[xs, ys].astype(float)
            c = P.mean(0)
            _, _, vt = np.linalg.svd(P - c, full_matrices=False)
            d = vt[0]
            pr = (P - c) @ d
            e1, e2 = c + d * pr.min(), c + d * pr.max()
            g = T(BW[a["bone"]][None])[0]
            goc_, ngon = (e1, e2) if np.hypot(*(e1 - g)) < np.hypot(*(e2 - g)) else (e2, e1)
            return (sl, z, mt, lay, x0w, y1w, goc_, ngon)

    for h_ in KT:
        cs = [ve(*q) for q in h_]
        rong = sum(c[3].width for c in cs)
        cho = W - 16 * (len(cs) + 1)
        if rong > cho:                                    # hàng tràn ngang: co cả hàng
            f = cho / rong * 0.98
            cs = [ve(sl, z * f, mt) for sl, z, mt in h_]
        hang.append((cs, max(c[3].height for c in cs)))
    tong_cao = sum(h[1] for h in hang)
    if tong_cao > H - 16 * (len(hang) + 1):                # tràn dọc: co hết
        f = (H - 16 * (len(hang) + 1)) / tong_cao * 0.98
        hang = []
        for h_ in KT:
            cs = [ve(*q) for q in h_]
            rong = sum(c[3].width for c in cs)
            cho = W - 16 * (len(cs) + 1)
            f2 = f * min(1.0, cho / rong * 0.98) if rong * f > cho else f
            cs = [ve(sl, z * f2, mt) for sl, z, mt in h_]
            hang.append((cs, max(c[3].height for c in cs)))
    ke_y = (H - sum(h[1] for h in hang)) // (len(hang) + 1)
    assert ke_y >= 4, ke_y
    can_ = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    y = ke_y
    for cs, hh in hang:
        ke = (W - sum(c[3].width for c in cs)) // (len(cs) + 1)
        assert ke >= 4, ke
        x = ke
        for sl, z, mt, lay, x0w, y1w, goc_, ngon in cs:
            y0 = y + (hh - lay.height) // 2
            can_.alpha_composite(lay, (x, y0))
            o[sl] = dict(hop=[x, y0, lay.width, lay.height], z=z, x0w=float(x0w), y1w=float(y1w), xuong=by[sl]["bone"],
                         goc=[float(goc_[0] + x), float(goc_[1] + y0)], ngon=[float(ngon[0] + x), float(ngon[1] + y0)],
                         huong=_huong(ngon - goc_), mo_ta=mt)
            x += lay.width + ke
        y += hh + ke_y
    p = os.path.join(G.MAU, "goc_KT.png")
    can_.convert("RGB").save(p)
    json.dump(o, open(p[:-4] + ".json", "w", encoding="utf-8"), indent=1)
    print(p)
    return o


def prompt_kt(o):
    mau = os.path.join(G.MAU, "goc_KT.png")
    out = os.path.join(G.TAI, "D_KT.png")
    p = os.path.join(GUI, "luot_2_da_KT.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {Wp(mau)}: the PARTS SHEET, 1536x1024, white background: eighteen small separate parts of a 2D animation puppet, "
         "each alone: top two rows thirteen pointed purple crystal SHARDS (each one stuck in the knight's armour by one end), bottom row "
         "five small dark STONES. Each part is shown at the exact size, angle and place to keep.",
         f"image 2 = {Wp(CON)}: {R_CON} Take from it the colours, the look of the broken arrows and the broken spear stuck in the armour, "
         "and the hand-drawn style.",
         "", f"SAVE: save it as a PNG to {Wp(out)}",
         "If a file with that name already exists, save as D_KT_2.png, D_KT_3.png ... in the same folder. Do not edit, move or delete any "
         "other file.", "",
         "TASK: REPLACE each part of image 1 by the NEW OBJECT described below, drawn at the SAME place on the sheet, along the SAME axis "
         "(same angle), with the SAME length: lay the new object exactly over the old part. The new object may be a little wider than the "
         "old part (feathers, barbs), but stays inside its own area and never touches another part. Each part has a BASE end (the end "
         "that is stuck in the armour) and a TIP end (the free end); both are given in pixels. Do NOT add other objects.", "",
         f"STYLE: hand-drawn on paper like image 2: a wobbly dark-brown ink outline ({MUC}, about 6 px) round every object, every area ONE "
         "flat colour with visible crayon hatching. No shading, no highlights, no gradients, no glow, no shadows: flat colour only. The "
         "parts of image 1 are painted in a smooth purple digital style: do NOT copy it.", "",
         "THE PARTS (pixels on the 1536x1024 sheet, x from the left, y from the top):"]
    for i, (sl, d) in enumerate(o.items(), 1):
        x, y, cw, ch = d["hop"]
        gx, gy = d["goc"]
        nx, ny = d["ngon"]
        if sl.startswith("P_shitou"):
            t.append(f"{i}. (area x = {x} to {x + cw}, y = {y} to {y + ch}) the stone becomes {d['mo_ta']}, the same size as the stone.")
        else:
            t.append(f"{i}. (area x = {x} to {x + cw}, y = {y} to {y + ch}; BASE end at about ({gx:.0f}, {gy:.0f}), TIP end at about "
                     f"({nx:.0f}, {ny:.0f}), pointing to the {d['huong']}) the shard becomes {d['mo_ta']}.")
    t += ["", "Plain pure-white background (#FFFFFF), no labels, no numbers, no frame, nothing added."]
    ghi(p, t)
    print(p)
    return p, mau, out


def cat_kt():
    path = anh.to_moi_nhat(G.TAI, "D_KT")
    if not path:
        print("KT: chưa gen")
        return
    o = json.load(open(os.path.join(G.MAU, "goc_KT.json"), encoding="utf-8"))
    A = np.asarray(Image.open(path).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
    Gd = np.asarray(Image.open(os.path.join(G.MAU, "goc_KT.png")).convert("RGB")).astype(np.int32)
    fg = ~nen_trang(A)
    fgG = ~nen_trang(Gd)
    n, lab, st, cen = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
    pj = os.path.join(MANH, "moi.json")
    moi = json.load(open(pj)) if os.path.exists(pj) else {}
    os.makedirs(MANH, exist_ok=True)
    print("KT:", os.path.basename(path))
    so = []
    for sl, d in o.items():
        x, y, cw, ch = d["hop"]
        z = d["z"]
        gm = np.zeros((H, W), bool)
        gm[y:y + ch, x:x + cw] = fgG[y:y + ch, x:x + cw]
        ids = [i for i in range(1, n) if st[i, 4] > 30 and (x <= cen[i][0] < x + cw and y <= cen[i][1] < y + ch
                                                            or (gm & (lab == i)).sum() > 20)]
        m = np.isin(lab, ids)
        if not m.any():
            print(f"  {sl}: KHÔNG thấy mảnh")
            continue
        ys, xs = np.nonzero(m)
        x0, y0, x1, y1 = xs.min() - 3, ys.min() - 3, xs.max() + 4, ys.max() + 4
        mm = m[y0:y1, x0:x1]
        al = np.clip(cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.8) * 1.25, 0, 1)
        rgba = np.dstack([A[y0:y1, x0:x1].astype(np.uint8), (al * 255).astype(np.uint8)])
        im = Image.fromarray(rgba, "RGBA").convert("RGBa")
        im = im.resize((max(1, round(im.width / z)), max(1, round(im.height / z))), Image.LANCZOS).convert("RGBA")
        ten = "kt_" + sl[2:]
        im.save(os.path.join(MANH, ten + ".png"))

        def ve_the_gioi(px, py):
            return [d["x0w"] + (px - x - PAD_KT) / z, d["y1w"] - (py - y - PAD_KT) / z]
        goc4 = [ve_the_gioi(x0, y0), ve_the_gioi(x1, y0), ve_the_gioi(x1, y1), ve_the_gioi(x0, y1)]
        moi[ten] = dict(slot=sl, xuong=d["xuong"], hop=[int(x0), int(y0), int(x1), int(y1)], the_gioi=goc4, to="KT")
        so.append(im)
        print(f"  {sl:11s} → {ten}.png {im.size}  (xương {d['xuong']})")
    json.dump(moi, open(pj, "w"), indent=1)
    _to_so(so, os.path.join(MANH, "_so_KT.png"))


# ================================================================ R1: mũ + kiếm, gen đúng chỗ, đúng cỡ trên concept
R = {"R1": [("mu", "P_tou", "bone5",
             "the HELMET: the tall rusty iron helm with the jagged iron CROWN of five short points fused round its top rim and the single "
             "vertical eye slit down its front; draw the eye slit as a plain near-black gap WITHOUT the green eyes, and the inside of the "
             "open crown top plain near-black, WITHOUT the green flames above it; complete the helm down to its lower edge at the neck"),
            ("kiem", "P_jian", "bone23",
             "the SWORD: the round pommel with the green gem, the dark leather GRIP complete (also where the fist covered it: a straight "
             "even grip), the crossguard bar with the RING round the base of the blade, and the broken rusty blade with its jagged broken "
             "end, WITHOUT the fist and the fingers, WITHOUT the cape behind it")]}
VI_R = {"R1": "mũ vương miện (khe mắt tối, không mắt, không lửa) + kiếm gãy đủ chuôi"}
TAM_R = {"R1": {"mu": (865, 270), "kiem": (590, 800)}}


def prompt_r():
    ps = []
    for ma, ds in R.items():
        out = os.path.join(G.TAI, f"M_{ma}.png")
        p = os.path.join(GUI, f"luot_2_manh_{ma}.txt")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(CON)}: {R_CON}",
             "", f"SAVE: save it as a PNG to {Wp(out)}",
             f"If a file with that name already exists, save as M_{ma}_2.png, M_{ma}_3.png ... in the same folder. Do not edit, move or "
             "delete any other file.", "",
             f"TASK: redraw image 1 with ONLY the {len(ds)} pieces listed below, each in the SAME POSITION and at the SAME SIZE as in "
             "image 1 (if your picture were laid over image 1, every piece must sit exactly on its old place). REMOVE everything else "
             "(the body, the armour, the cape, the hands, the arrows, the spear, the flames) and leave pure white there. COMPLETE every "
             "piece into ONE CLOSED SHAPE with the ink outline all the way round: the parts of a piece that were hidden behind other "
             "things in image 1 are drawn too, continuing its shape naturally.", "", "THE PIECES:"]
        t += [f"{i}. {mt}." for i, (_, _, _, mt) in enumerate(ds, 1)]
        t += ["", f"STYLE: exactly the style of image 1: wobbly dark-brown ink outline ({MUC}, about 7 px), thin ink lines for the few inner "
              "lines, every area ONE flat colour with visible crayon hatching; the same colours as in image 1. No shading, no highlights, "
              "no gradients, no glow, no shadows.", "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no labels, no frame, nothing added."]
        ghi(p, t)
        ps.append((ma, p, out))
        print(p)
    return ps


def tach_manh(rgb, tam):
    """tách các mảnh: lòng tô chia vùng liền; mỗi vùng về mảnh có tâm gần nhất; mọi điểm của hình (cả viền) về mảnh của lòng tô gần nhất."""
    fg = ~nen_trang(rgb.astype(np.int32))
    lum = rgb.astype(np.int32).mean(2)
    trang = rgb.min(2) > 236
    r_, b_ = rgb[..., 0].astype(np.int32), rgb[..., 2].astype(np.int32)
    muc = (lum < 50) | ((lum < 62) & (r_ - b_ > 22))
    long_ = fg & ~muc & ~trang
    long_ = cv2.erode(long_.astype(np.uint8), el(1)).astype(bool)
    n, lab, st, cen = cv2.connectedComponentsWithStats(long_.astype(np.uint8), 8)
    ten = list(tam)
    C = np.array([tam[k] for k in ten], float)
    gan = np.zeros(n, np.int32) - 1
    for i in range(1, n):
        if st[i, 4] < 25:
            continue
        gan[i] = int(np.argmin(np.hypot(*(C - cen[i]).T)))
    hop = (lab > 0) & (gan[lab] >= 0)
    _, lbl = cv2.distanceTransformWithLabels((~hop).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
    ys, xs = np.nonzero(hop)
    bang = np.full(lbl.max() + 1, -1, np.int32)
    bang[lbl[ys, xs]] = gan[lab[ys, xs]]
    thuoc = bang[lbl]
    return {k: fg & ~trang & (thuoc == j) for j, k in enumerate(ten)}


def _truc(m):
    ys, xs = np.nonzero(m)
    P = np.c_[xs, ys].astype(float)
    c = P.mean(0)
    _, _, vt = np.linalg.svd(P - c, full_matrices=False)
    d = vt[0] if vt[0][0] >= 0 else -vt[0]
    return c, d


# tâm nắm tay gần trên concept (px concept, đọc bằng mắt: găng sắt đen cầm chuôi kiếm)
NAM_TAY_CON = (478.0, 716.0)
CHINH = {}                                 # chỉnh tay sau khi ghép: {tên: dict(dx, dy, s)} px concept


def cat_r():
    """mỗi tờ M_R*: tách mảnh, ghi manh/<tên>.png + moi.json. Mũ: chỗ concept (phép căn). Kiếm: xoay quanh nắm tay concept cho trục lưỡi trùng
    trục kiếm gốc, dời cho nắm tay concept về nắm tay rig."""
    T, Ti, spx = phep_can()
    lop, _, _ = lop_goc()
    pj = os.path.join(MANH, "moi.json")
    moi = json.load(open(pj)) if os.path.exists(pj) else {}
    os.makedirs(MANH, exist_ok=True)
    for ma, ds in R.items():
        path = anh.to_moi_nhat(G.TAI, f"M_{ma}")
        if not path:
            print(f"{ma}: chưa gen")
            continue
        print(f"{ma}:", os.path.basename(path))
        rgb = np.asarray(Image.open(path).convert("RGB").resize((W, H), Image.LANCZOS))
        ms = tach_manh(rgb, TAM_R[ma])
        for ten, sl, bn, _ in ds:
            mm0 = ms.get(ten)
            if mm0 is None or mm0.sum() < 50:
                print(f"  {ten}: KHÔNG thấy mảnh")
                continue
            ys, xs = np.nonzero(mm0)
            pad = 4
            x0, y0, x1, y1 = max(0, xs.min() - pad), max(0, ys.min() - pad), min(W - 1, xs.max() + pad), min(H - 1, ys.max() + pad)
            mm = mm0[y0:y1 + 1, x0:x1 + 1]
            al = np.clip(cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.8) * 1.25, 0, 1)
            rgba = np.dstack([rgb[y0:y1 + 1, x0:x1 + 1], (al * 255).astype(np.uint8)])
            k = 1.0 / spx * (RES * 0.5)
            out = Image.fromarray(rgba, "RGBA").convert("RGBa")
            out = out.resize((max(1, round(out.width * k)), max(1, round(out.height * k))), Image.LANCZOS).convert("RGBA")
            out.save(os.path.join(MANH, ten + ".png"))
            hop = np.array([[x0, y0], [x1 + 1, y0], [x1 + 1, y1 + 1], [x0, y1 + 1]], float)
            if ten == "kiem":
                cg, dg = _truc(lop["P_jian"][1])
                ck, dk = _truc(mm0)
                goc_xoay = math.atan2(dg[1], dg[0]) - math.atan2(dk[1], dk[0])
                Rm = np.array([[math.cos(goc_xoay), -math.sin(goc_xoay)], [math.sin(goc_xoay), math.cos(goc_xoay)]])
                tay = np.zeros((H, W), bool)
                for s_ in ("P_y_shou", "P_y_shouzhi00", "P_y_shouzhi01", "P_y_shouzhi02"):
                    tay |= lop[s_][1]
                ty, tx = np.nonzero(tay)
                nam_rig = np.array([tx.mean(), ty.mean()])
                ntc = np.array(NAM_TAY_CON)
                hop = (hop - ntc) @ Rm.T + nam_rig
                print(f"    kiếm: xoay {math.degrees(goc_xoay):+.1f}°, nắm tay concept {ntc} → rig {nam_rig.round(1)}")
            if ten in CHINH:
                c_ = CHINH[ten]
                tam = hop.mean(0)
                hop = tam + (hop - tam) * c_.get("s", 1.0) + np.array([c_.get("dx", 0.0), c_.get("dy", 0.0)])
            goc4 = Ti(hop)
            moi[ten] = dict(slot=sl, xuong=bn, hop=[int(x0), int(y0), int(x1 + 1), int(y1 + 1)], the_gioi=goc4.tolist(), to=ma)
            print(f"  {ten:9s} hộp {x0},{y0}–{x1},{y1}  → {ten}.png {out.size}  (thay {sl}, xương {bn})")
    json.dump(moi, open(pj, "w"), indent=1)


def cat_mat():
    """hai mắt xanh cắt thẳng từ concept (lòng xanh trong khe mắt + viền mực sát) → manh/mat.png, slot mới P_mat trên xương mũ."""
    T, Ti, spx = phep_can()
    Cn = np.asarray(Image.open(CON).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
    x0, y0, x1, y1 = 830, 225, 945, 300                     # khung khe mắt trên concept (đọc bằng mắt)
    sub = Cn[y0:y1, x0:x1]
    r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
    xanh = (g > 150) & (g - r > 40) & (g - b > 60)
    xanh = cv2.morphologyEx(xanh.astype(np.uint8), cv2.MORPH_OPEN, el(1))
    n, lab, st, _ = cv2.connectedComponentsWithStats(xanh, 8)
    keep = [i for i in range(1, n) if st[i, 4] > 30]
    xanh = np.isin(lab, keep)
    m = cv2.dilate(xanh.astype(np.uint8), el(3)).astype(bool)
    ys, xs = np.nonzero(m)
    a0, b0, a1, b1 = xs.min() - 2, ys.min() - 2, xs.max() + 3, ys.max() + 3
    mm = m[b0:b1, a0:a1]
    al = np.clip(cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.7) * 1.2, 0, 1)
    rgba = np.dstack([sub[b0:b1, a0:a1].astype(np.uint8), (al * 255).astype(np.uint8)])
    k = 1.0 / spx * (RES * 0.5)
    out = Image.fromarray(rgba, "RGBA").convert("RGBa")
    out = out.resize((max(1, round(out.width * k)), max(1, round(out.height * k))), Image.LANCZOS).convert("RGBA")
    os.makedirs(MANH, exist_ok=True)
    out.save(os.path.join(MANH, "mat.png"))
    hop = np.array([[a0, b0], [a1, b0], [a1, b1], [a0, b1]], float) + np.array([x0, y0])
    if "mu" in CHINH:
        c_ = CHINH["mu"]
        hop = hop + np.array([c_.get("dx", 0.0), c_.get("dy", 0.0)])
    pj = os.path.join(MANH, "moi.json")
    moi = json.load(open(pj)) if os.path.exists(pj) else {}
    moi["mat"] = dict(slot="P_mat", xuong="bone5", hop=[int(v) for v in hop[0].tolist() + hop[2].tolist()], the_gioi=Ti(hop).tolist(),
                      to="MAT", moi_slot=True, sau="P_tou")
    json.dump(moi, open(pj, "w"), indent=1)
    print("MAT → mat.png", out.size, f"{len(keep)} cụm xanh")


# ================================================================ HON: lưỡi kiếm hồn (chiêu cuối) mọc tiếp từ chỗ gãy của kiếm
HON_DAI = 0.92                             # mũi lưỡi hồn ở x = HON_DAI × bề ngang tờ


def _kiem_khung():
    """ảnh kiếm của mình (manh/kiem.png) + phép px ảnh → thế giới khung 0 idle (theo 4 góc moi.json) + trục chuôi → chỗ gãy (px ảnh)."""
    im = Image.open(os.path.join(MANH, "kiem.png")).convert("RGBA")
    A = np.asarray(im)
    Vw = np.array(json.load(open(os.path.join(MANH, "moi.json")))["kiem"]["the_gioi"], float)
    w, h = im.size
    src = np.array([[0, 0], [w, 0], [w, h], [0, h]], float)
    M, *_ = np.linalg.lstsq(np.c_[src, np.ones(4)], Vw, rcond=None)          # px ảnh → thế giới (affine)
    al = A[..., 3] > 120
    ys, xs = np.nonzero(al)
    P = np.c_[xs, ys].astype(float)
    c = P.mean(0)
    _, _, vt = np.linalg.svd(P - c, full_matrices=False)
    d = vt[0]
    xanh = al & (A[..., 1].astype(int) - A[..., 0] > 50) & (A[..., 1] > 150)
    gy, gx = np.nonzero(xanh)
    ngoc = np.array([gx.mean(), gy.mean()]) if len(gx) else c - d
    if (ngoc - c) @ d > 0:                                                    # d chĩa từ chuôi (ngọc) → chỗ gãy
        d = -d
    pr = (P - c) @ d
    return im, M, c, d, float(pr.min()), float(pr.max())


def to_hon():
    """tờ hướng dẫn: kiếm gãy của mình nằm ngang (chuôi trái, chỗ gãy chĩa phải) ở trái tờ; ghi phép tờ → px ảnh kiếm."""
    im, M, c, d, p0, p1 = _kiem_khung()
    dai = 470.0
    s = dai / (p1 - p0)
    goc = math.degrees(math.atan2(d[1], d[0]))
    big = im.convert("RGBa").resize((round(im.width * s), round(im.height * s)), Image.LANCZOS).rotate(goc, resample=Image.BICUBIC,
                                                                                                       expand=True).convert("RGBA")
    can_ = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    x_dau = 40.0
    tam_im = np.array([im.width / 2, im.height / 2])
    th = math.radians(-goc)
    Rm = np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
    chuoi = (c + d * p0 - tam_im) * s @ Rm.T                                 # đầu chuôi so với tâm ảnh xoay
    tam_to = np.array([x_dau - chuoi[0], H / 2 - chuoi[1]])
    can_.alpha_composite(big, (int(round(tam_to[0] - big.width / 2)), int(round(tam_to[1] - big.height / 2))))
    gay = tam_to + (c + d * p1 - tam_im) * s @ Rm.T
    p = os.path.join(G.MAU, "kiem_hon.png")
    can_.convert("RGB").save(p)
    json.dump(dict(s=s, goc=goc, tam_to=tam_to.tolist(), tam_im=tam_im.tolist(), gay=gay.tolist(), mui=[W * HON_DAI, float(gay[1])]),
              open(p[:-4] + ".json", "w"), indent=1)
    print(p, "chỗ gãy", gay.round(1))
    return p, gay


def prompt_hon():
    gd, gay = to_hon()
    out = os.path.join(G.TAI, "H_kiem.png")
    p = os.path.join(GUI, "luot_3_luoi_hon.txt")
    xm = int(W * HON_DAI)
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {Wp(gd)}: our character's BROKEN SWORD lying horizontally at the left of a 1536x1024 white sheet: the round pommel "
         "with a green gem at the far left, the dark leather grip, the gold crossguard bar with a gold ring round the blade, and the "
         f"short rusty iron blade broken off with a jagged end at about x = {gay[0]:.0f}, y = {gay[1]:.0f}.",
         f"image 2 = {Wp(CON)}: {R_CON} It gives the hand-drawn style and the colours of the green soul fire.",
         "", f"SAVE: save it as a PNG to {Wp(out)}",
         "If a file with that name already exists, save as H_kiem_2.png, H_kiem_3.png ... in the same folder. Do not edit, move or delete "
         "any other file.", "",
         "TASK: the cursed knight RESTORES his broken sword with SOUL MATTER. Keep the whole broken sword of image 1 EXACTLY as it is (same "
         "place, same size, same drawing: pommel, grip, crossguard, ring and the rusty iron stump with its jagged broken end). From the "
         f"jagged broken end draw a NEW LONG BLADE made of GREEN SOUL MATTER that continues the blade straight to the right, along the "
         f"same axis, to a sharp pointed tip at about x = {xm}, y = {gay[1]:.0f}: a VERY LONG greatsword blade (about three times "
         "the length of the whole broken sword).", "",
         f"THE SOUL BLADE: as wide as the iron blade at the break, keeping that width for most of its length and narrowing to the point "
         f"in its last fifth; a straight middle ridge line; flat bright soul green {MAU['lua']} with ONE pale green {MAU['lua_nhat']} "
         "stroke along its middle; along both edges a few short flame-like wisps licking off the blade (small pointed tongues, same green, "
         "ink outlined), more of them near the broken end where the soul matter grows out of the iron; the jagged iron end stays "
         "visible, the soul blade starts right at it.", "",
         f"STYLE: hand-drawn on paper like image 2: wobbly dark-brown ink outline ({MUC}, about 7 px) round the soul blade and its wisps, "
         "flat colour with visible crayon hatching. No glow, no halo, no light rays, no gradient, no sparkles, no shadow: flat shapes "
         "only (the glow will be added by the game).", "",
         "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), nothing else on the sheet, no labels, no frame."]
    ghi(p, t)
    print(p)
    return p


def cat_hon():
    """lưỡi hồn = phần GPT vẽ thêm bên phải chỗ gãy (nới 18 px về phía chuôi) → manh/luoi_hon.png + moi.json "luoi_hon" (4 góc thế giới
    khung 0 idle, xương bone23; rig gắn vào xương luoi_hon ở chỗ gãy)."""
    path = anh.to_moi_nhat(G.TAI, "H_kiem")
    if not path:
        print("HON: chưa gen")
        return
    j = json.load(open(os.path.join(G.MAU, "kiem_hon.json")))
    im, M, c, d, p0, p1 = _kiem_khung()
    A = np.asarray(Image.open(path).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
    fg = ~nen_trang(A)
    gx, gy = j["gay"]
    m = fg.copy()
    m[:, :int(gx - 18)] = False
    m[:int(gy - 260)] = False
    m[int(gy + 260):] = False
    n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), 8)
    ids = [i for i in range(1, n) if st[i, 4] > 200]
    m = np.isin(lab, ids)
    ys, xs = np.nonzero(m)
    x0, y0, x1, y1 = xs.min() - 2, ys.min() - 2, xs.max() + 3, ys.max() + 3
    mm = m[y0:y1, x0:x1].astype(np.float32)
    xx = np.arange(x1 - x0)[None, :] + x0                                     # mép trái (chỗ nối khúc sắt) mờ dần 14 px
    mm *= np.clip((xx - (gx - 18)) / 14.0, 0, 1)
    al = np.clip(cv2.GaussianBlur(mm, (0, 0), 0.8) * 1.2, 0, 1)
    rgba = np.dstack([A[y0:y1, x0:x1].astype(np.uint8), (al * 255).astype(np.uint8)])
    s = j["s"]
    out = Image.fromarray(rgba, "RGBA").convert("RGBa")
    out = out.resize((max(1, round(out.width / s)), max(1, round(out.height / s))), Image.LANCZOS).convert("RGBA")
    out.save(os.path.join(MANH, "luoi_hon.png"))
    th = math.radians(j["goc"])
    Rm = np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])          # ngược của R(−goc)
    tam_to, tam_im = np.array(j["tam_to"]), np.array(j["tam_im"])

    def to2w(q):
        qi = (np.asarray(q, float) - tam_to) @ Rm.T / s + tam_im
        return np.c_[qi, np.ones(len(qi))] @ M
    hop = np.array([[x0, y0], [x1, y0], [x1, y1], [x0, y1]], float)
    goc4 = to2w(hop)
    gay_w = to2w(np.array([[gx, gy]]))[0]
    mui_w = to2w(np.array([[x1, gy]]))[0]
    pj = os.path.join(MANH, "moi.json")
    moi = json.load(open(pj))
    moi["luoi_hon"] = dict(slot="P_jian_hon", xuong="bone23", hop=[int(x0), int(y0), int(x1), int(y1)], the_gioi=goc4.tolist(), to="HON",
                           gay=gay_w.tolist(), mui=mui_w.tolist())
    json.dump(moi, open(pj, "w"), indent=1)
    print("HON → luoi_hon.png", out.size, "dài", round(float(np.hypot(*(mui_w - gay_w)))), "đơn vị")


# ================================================================ HON2: phần lưỡi bị gãy VÁ bằng vật chất linh hồn (người dùng 2026-11-16: lượt HON
# trên bị trả: "phải match vào đúng các vết gãy của kiếm cùn, như sửa lại kiếm bằng vật liệu khác", "dài quá, cho ngắn đi", "hiện lên dần theo tay
# khi vuốt lên"). Hình bóng phần vá do MÃ dựng: kéo dài hai mép lưỡi sắt tới mũi, trừ phần sắt còn lại → mép trái phần vá trùng từng răng của
# vết gãy. GPT chỉ tô chất liệu bên trong; mã cắt lại đúng hình bóng đó, chia lát dọc lưỡi để rig cho hiện dần theo bàn tay.
HON_L = 650.0                              # đơn vị thế giới: chỗ gãy → mũi lưỡi vá
HON_N = 10                                 # số lát dọc lưỡi


def _ngang(tong_px=1400.0, x_dau=60.0):
    """kiếm gãy nằm ngang trên tờ (chuôi trái): phép tờ ↔ px ảnh kiếm ↔ thế giới."""
    im, M, c, d, p0, p1 = _kiem_khung()
    s = tong_px / ((p1 - p0) + HON_L)
    goc = math.degrees(math.atan2(d[1], d[0]))
    big = im.convert("RGBa").resize((round(im.width * s), round(im.height * s)), Image.LANCZOS).rotate(goc, resample=Image.BICUBIC,
                                                                                                       expand=True).convert("RGBA")
    tam_im = np.array([im.width / 2, im.height / 2])
    th = math.radians(-goc)
    Rm = np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
    chuoi = (c + d * p0 - tam_im) * s @ Rm.T
    tam_to = np.array([x_dau - chuoi[0], H / 2 - chuoi[1]])
    can_ = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    can_.alpha_composite(big, (int(round(tam_to[0] - big.width / 2)), int(round(tam_to[1] - big.height / 2))))
    gay = tam_to + (c + d * p1 - tam_im) * s @ Rm.T
    Ri = np.array([[math.cos(-th), -math.sin(-th)], [math.sin(-th), math.cos(-th)]])

    def to2w(q):
        qi = (np.asarray(q, float).reshape(-1, 2) - tam_to) @ Ri.T / s + tam_im
        return np.c_[qi, np.ones(len(qi))] @ M
    return can_, s, gay, to2w, (p1 - p0)


def to_hon2():
    can_, s, gay, to2w, dai_kiem = _ngang()
    A = np.asarray(can_)
    sat = A[..., 3] > 30
    x_gay, y_truc = float(gay[0]), float(gay[1])
    x_mui = x_gay + HON_L * s
    # hai mép lưỡi sắt: đoạn lưỡi trơn giữa vòng chắn và vết gãy (70–90 % chiều dài kiếm gãy tính từ đầu chuôi)
    xs_ = np.arange(int(x_gay - 0.30 * dai_kiem * s), int(x_gay - 0.10 * dai_kiem * s))
    tren, duoi = [], []
    for x in xs_:
        ys = np.nonzero(A[:, x, 3] > 128)[0]
        ys = ys[np.abs(ys - y_truc) < 0.25 * dai_kiem * s]
        if len(ys):
            tren.append((x, ys.min()))
            duoi.append((x, ys.max()))
    tren, duoi = np.array(tren, float), np.array(duoi, float)
    at, bt = np.polyfit(tren[:, 0], tren[:, 1], 1)
    ad, bd = np.polyfit(duoi[:, 0], duoi[:, 1], 1)
    x_a = x_gay - 0.30 * dai_kiem * s
    x_n = x_mui - 0.28 * HON_L * s                                           # từ đây lưỡi thu nhọn về mũi
    y_mui = 0.5 * ((at * x_mui + bt) + (ad * x_mui + bd))
    poly = np.array([[x_a, at * x_a + bt], [x_n, at * x_n + bt], [x_mui, y_mui], [x_n, ad * x_n + bd], [x_a, ad * x_a + bd]])
    m = np.zeros((H, W), np.uint8)
    cv2.fillPoly(m, [np.round(poly).astype(np.int32)], 1)
    vá = m.astype(bool) & ~cv2.dilate(sat.astype(np.uint8), el(1)).astype(bool)
    n, lab, st, _ = cv2.connectedComponentsWithStats(vá.astype(np.uint8), 8)
    vá = np.isin(lab, [i for i in range(1, n) if st[i, 4] > 40])
    # tờ hướng dẫn: kiếm sắt + phần vá tô xanh phẳng, viền mực ở mép NGOÀI phần vá (mép giáp sắt đã có nét gãy của sắt)
    g = np.full((H, W, 3), 255, np.uint8)
    al = A[..., 3:4].astype(np.float32) / 255.0
    g = (g * (1 - al) + A[..., :3] * al).astype(np.uint8)
    g[vá] = _hex(MAU["lua"])
    gan_sat = cv2.dilate((A[..., 3] > 128).astype(np.uint8), el(4)).astype(bool)
    vien = vá & ~cv2.erode(vá.astype(np.uint8), el(3)).astype(bool) & ~gan_sat
    g[vien] = INK
    os.makedirs(G.MAU, exist_ok=True)
    p = os.path.join(G.MAU, "kiem_va.png")
    Image.fromarray(g).save(p)
    Image.fromarray((vá * 255).astype(np.uint8)).save(os.path.join(G.MAU, "kiem_va_mask.png"))
    Image.fromarray(A[..., 3]).save(os.path.join(G.MAU, "kiem_va_sat.png"))
    json.dump(dict(s=s, gay=[x_gay, y_truc], mui=[x_mui, y_mui], x_a=x_a, dai_kiem=dai_kiem), open(p[:-4] + ".json", "w"), indent=1)
    print(p, f"chỗ gãy x {x_gay:.0f}, mũi x {x_mui:.0f}; phần vá {int(vá.sum())} px")
    return p


def prompt_hon2():
    gd = to_hon2()
    j = json.load(open(os.path.join(G.MAU, "kiem_va.json")))
    out = os.path.join(G.TAI, "H_va.png")
    p = os.path.join(GUI, "luot_3_kiem_va.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {Wp(gd)}: our character's SWORD lying horizontally on a 1536x1024 white sheet: the pommel with a green gem at the far "
         "left, the leather grip, the gold crossguard and ring, the short rusty iron blade broken off with a JAGGED edge, and, fitted "
         "exactly into that jagged edge, a FLAT LIGHT-GREEN SHAPE: the MISSING PART of the blade (it continues the blade to a pointed tip "
         f"at about x = {j['mui'][0]:.0f}).",
         f"image 2 = {Wp(CON)}: {R_CON} It gives the hand-drawn style and the colours of the green soul fire.",
         "", f"SAVE: save it as a PNG to {Wp(out)}",
         "If a file with that name already exists, save as H_va_2.png, H_va_3.png ... in the same folder. Do not edit, move or delete "
         "any other file.", "",
         "TASK: the cursed knight's broken sword is REPAIRED with a different material: GREEN SOUL MATTER fills the missing part of the "
         "blade. Redraw image 1 with EVERYTHING kept exactly in place: the iron sword unchanged (pommel, grip, crossguard, ring, rusty iron "
         "stump and its jagged broken edge), and the light-green shape keeping EXACTLY its outline (same size, same place, same straight "
         "edges, same point, its left edge following every tooth of the jagged broken edge): only REPAINT the inside of the green shape as "
         "soul matter. Draw nothing outside the green shape: no wisps, no flames, no sparks sticking out.", "",
         f"THE SOUL MATTER (inside the green shape only): flat bright soul green {MAU['lua']}; ONE pale green {MAU['lua_nhat']} middle line "
         "continuing the ridge line of the iron blade to the point; a few thin pale green crack-like veins branching from the jagged seam "
         "into the green (like a crystal or a glass repair), fewer towards the point; visible crayon hatching. The seam with the iron is "
         f"the iron's own dark ink line; the outer edges of the green part get the same wobbly dark-brown ink outline ({MUC}, about 6 px) "
         "as the rest of the sword.", "",
         "STYLE: hand-drawn on paper like image 2, flat colour. No glow, no halo, no light rays, no gradient, no shadow (the glow is added "
         "by the game).", "",
         "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), nothing else on the sheet, no labels, no frame."]
    ghi(p, t)
    print(p)
    return p


def cat_hon2():
    """phần vá = điểm ảnh GPT trong hình bóng phần vá (nới 3 px, không lấn sắt) → HON_N lát dọc lưỡi manh/hon_<k>.png + moi.json "hon_<k>"
    (slot P_jian_hon<k>, xương bone23, 4 góc thế giới khung 0 idle, a0 / a1 = đoạn dọc lưỡi tính từ chỗ gãy, đơn vị)."""
    path = anh.to_moi_nhat(G.TAI, "H_va")
    if not path:
        print("HON2: chưa gen")
        return
    j = json.load(open(os.path.join(G.MAU, "kiem_va.json")))
    _, s, gay, to2w, _ = _ngang()
    A = np.asarray(Image.open(path).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
    va = np.asarray(Image.open(os.path.join(G.MAU, "kiem_va_mask.png"))) > 127
    sat = np.asarray(Image.open(os.path.join(G.MAU, "kiem_va_sat.png"))) > 200
    m = cv2.dilate(va.astype(np.uint8), el(3)).astype(bool) & ~sat & ~(A.min(2) > 236)
    al = np.clip(cv2.GaussianBlur(m.astype(np.float32), (0, 0), 0.7) * 1.25, 0, 1) * m
    ys, xs = np.nonzero(m)
    x0, x1 = xs.min(), xs.max() + 1
    y0, y1 = ys.min() - 2, ys.max() + 3
    pj = os.path.join(MANH, "moi.json")
    moi = json.load(open(pj))
    for k_ in [k for k in moi if k.startswith("hon_") or k == "luoi_hon"]:
        moi.pop(k_)
    gay_w = to2w([j["gay"]])[0]
    mui_w = to2w([j["mui"]])[0]
    ax = (mui_w - gay_w) / np.linalg.norm(mui_w - gay_w)
    bien = np.linspace(x0, x1, HON_N + 1)
    for k in range(HON_N):
        # mỗi lát chồng 6 px sang hai lát kề (lát trên vẽ đè): mép lọc ảnh của lát này nằm trên lòng đặc của lát kia, không lộ vạch
        a, b = max(int(x0), int(math.floor(bien[k])) - 6), min(int(x1), int(math.ceil(bien[k + 1])) + 6)
        rgba = np.dstack([A[y0:y1, a:b].astype(np.uint8), (al[y0:y1, a:b] * 255).astype(np.uint8)])
        im = Image.fromarray(rgba, "RGBA").convert("RGBa")
        im = im.resize((max(2, round(im.width / s)), max(2, round(im.height / s))), Image.LANCZOS).convert("RGBA")
        im.save(os.path.join(MANH, f"hon_{k}.png"))
        hop = np.array([[a, y0], [b, y0], [b, y1], [a, y1]], float)
        Vw = to2w(hop)
        a0 = float((to2w([[bien[k], j["gay"][1]]])[0] - gay_w) @ ax)
        a1 = float((to2w([[bien[k + 1], j["gay"][1]]])[0] - gay_w) @ ax)
        moi[f"hon_{k}"] = dict(slot=f"P_jian_hon{k}", xuong="bone23", the_gioi=Vw.tolist(), to="HON2", a0=a0, a1=a1, gay=gay_w.tolist(),
                               mui=mui_w.tolist())
    # bản LIỀN một ảnh (rig dùng bản này + mặt nạ cắt chạy theo tay; các lát hon_k giữ lại để so, không vào rig)
    for k_ in [k for k in moi if k.startswith("hon_")]:
        moi.pop(k_)
    a, b = int(x0) - 2, int(x1) + 2
    rgba = np.dstack([A[y0:y1, a:b].astype(np.uint8), (al[y0:y1, a:b] * 255).astype(np.uint8)])
    im = Image.fromarray(rgba, "RGBA").convert("RGBa")
    im = im.resize((max(2, round(im.width / s)), max(2, round(im.height / s))), Image.LANCZOS).convert("RGBA")
    im.save(os.path.join(MANH, "hon_va.png"))
    a0 = float((to2w([[x0, j["gay"][1]]])[0] - gay_w) @ ax)
    moi["hon_va"] = dict(slot="P_jian_hon", xuong="bone23", the_gioi=to2w(np.array([[a, y0], [b, y0], [b, y1], [a, y1]], float)).tolist(),
                         to="HON2", a0=a0, gay=gay_w.tolist(), mui=mui_w.tolist())
    json.dump(moi, open(pj, "w"), indent=1)
    for f in ("luoi_hon.png",):
        if os.path.exists(os.path.join(MANH, f)):
            os.remove(os.path.join(MANH, f))
    # tờ so: kiếm sắt + phần vá ghép lại
    so = np.full((y1 - y0 + 40, W, 3), 150, np.uint8)
    A_sat = np.asarray(_ngang()[0])
    for yy in range(y1 - y0):
        pass
    sat_rgb = A_sat[y0:y1, :, :3].astype(np.float32)
    sat_a = A_sat[y0:y1, :, 3:4].astype(np.float32) / 255.0
    nen = so[20:20 + (y1 - y0)].astype(np.float32)
    nen = nen * (1 - sat_a) + sat_rgb * sat_a
    aa = al[y0:y1, :, None]
    nen = nen * (1 - aa) + A[y0:y1].astype(np.float32) * aa
    so[20:20 + (y1 - y0)] = nen.astype(np.uint8)
    Image.fromarray(so).save(os.path.join(MANH, "_so_HON2.png"))
    print(f"HON2 → {HON_N} lát hon_k.png, phần vá dài {float(np.hypot(*(mui_w - gay_w))):.0f} đơn vị; tờ so manh/_so_HON2.png")


# ================================================================ hướng dẫn
def huong_dan(ps):
    hd = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2")[0].rstrip("\n")
    gd = ["", "## Lượt 2: mảnh theo concept C đã duyệt (2026-11-16)", "",
          "Năm loại tờ (Claude tự gen và tự cắt; người dùng không cần làm gì). Ảnh mảnh gốc là của game tham khảo: chỉ dùng trong máy.", ""]
    for ten, p, rs, vi in ps:
        gd += [f"### {ten}", "", vi, "", f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`.", "",
               "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
        gd += [f"| {i} | `{Wp(r)}` | {v} |" for i, (r, v) in enumerate(rs, 1)]
        gd += [""]
    gd += ["Kiểm: hình bóng trùng tờ hướng dẫn; tờ khoảng rỗng không có nét mực ở chỗ nối; gai thành giáo / mũi tên đúng trục, đầu cắm đúng "
           "đầu; mũ, kiếm đúng chỗ, đúng cỡ như concept, vẽ đủ phần khuất; tô phẳng; nền trắng. Cắt: "
           "`py -3 -I ArtGen/Spine/ky_nguyen_manh.py cat`."]
    ghi(hd, (cu + "\n" + "\n".join(gd)).split("\n"))


def to_het():
    if not os.path.exists(os.path.join(G.MAU, "can.json")):
        can()
    to_lien()
    p1, gd1, out1 = prompt_lien()
    ps = [("Tờ khoảng rỗng liền", p1, [(CON, "Concept C đã duyệt"), (gd1, "Tờ hướng dẫn tự dựng: một hình tối liền (thân rỗng, dải dưới "
                                                                        "vai, hai bắp tay tối) đúng chỗ rig")],
           f"thân rỗng + dải dưới vai + hai bắp tay tối → `{Wp(out1)}`")]
    for ma in TO_K:
        o = to_k(ma)
        p, gd, out = prompt_k(ma, o)
        ps.append((f"Tờ mảnh giữ hình bóng {ma}", p, [(gd, f"Mảnh gốc cắt theo lưới, phóng to: {VI_K[ma]}"), (CON, "Concept C"),
                                                     (SOI_GIAP, "Sói giáp sắt: chỉ lấy nét, cách tô sắt")], f"{VI_K[ma]} → `{Wp(out)}`"))
    o = to_kt()
    p, gd, out = prompt_kt(o)
    ps.append(("Tờ gai → giáo / mũi tên, đá → mảnh khiên", p, [(gd, "Mười ba gai tinh thể + năm viên đá của con gốc, vẽ theo hướng ở dáng "
                                                                     "nghỉ"), (CON, "Concept C")],
               f"giáo gãy, mũi giáo xuyên ngực, mũi tên gãy, dằm tên, mảnh khiên vỡ, đầu mũi tên → `{Wp(out)}`"))
    for ma, p, out in prompt_r():
        ps.append((f"Tờ mảnh đổi dáng {ma}", p, [(CON, "Concept C đã duyệt")], f"{VI_R[ma]} → `{Wp(out)}`"))
    huong_dan(ps)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "can":
        can()
    elif cmd == "to":
        to_het()
    elif cmd == "cat":
        chi = sys.argv[2] if len(sys.argv) > 2 else ""
        if chi in ("", "LIEN"):
            cat_lien()
        for ma in TO_K:
            if chi in ("", ma):
                cat_k(ma)
        if chi in ("", "KT"):
            cat_kt()
        if chi in ("", "R1", "R"):
            cat_r()
        if chi in ("", "MAT"):
            cat_mat()
        if chi in ("HON",):
            cat_hon()
        if chi in ("", "HON2"):
            cat_hon2()
    elif cmd == "hon":
        prompt_hon()
    elif cmd == "hon2":
        prompt_hon2()
    else:
        print(__doc__)
