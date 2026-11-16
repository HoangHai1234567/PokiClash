# -*- coding: utf-8 -*-
"""Quỷ xích (quy_xich, rig monster_3408): MẢNH theo concept A đã duyệt (inbox/quy_xich_1/tai_ve/L1_duyet.png).

Ba loại mảnh (skill pokiclash-spine-rig mục 00; memory khop-noi-gen-lien, reskin-theo-part-goc):
  LIEN  : bề mặt nối nhau (bụng + ngực + cổ; từng tay hai khúc; từng chân hai khúc) → MỘT tờ liền dựng từ rig: hình bóng ở dáng gốc, tô
          bằng điểm ảnh concept đã căn lên rig, chỗ bị mảnh khác che lấp bằng màu gần nhất; GPT vẽ lại sạch, viền chỉ ở ngoài; mã nướng tờ
          vào khung từng part qua lưới (hai mảnh chồng nhau lấy CÙNG điểm ảnh: không có nét ở khớp).
  K     : mảnh rời giữ hình bóng gốc (cánh, đuôi, mặt, vuốt, ngón, giáp vai nhỏ, hai mảnh giáp cổ, hai mắt xích): tờ = CHÍNH mảnh gốc cắt
          theo lưới phóng to; GPT đổi da theo concept, giữ hình bóng.
  R1, R2: mảnh ĐỔI DÁNG, mảnh cứng một xương (đỉnh mũ, giáp vai to, ổ khoá, móc | má mũ hai bên, hai sừng, ba vây lưng): gen "đúng chỗ,
          đúng cỡ" trên concept, bỏ mọi thứ khác, vẽ đủ phần khuất. Toạ độ concept → thế giới dáng gốc qua phép căn.

    quy_xich_manh.py can        căn concept lên hình con gốc (phép đồng dạng khớp hình bóng nhất) → mau/can.json
    quy_xich_manh.py to         dựng mọi tờ hướng dẫn + file prompt → mau/lien.png, mau/goc_K.png, gui_gpt/quy_xich_1/luot_2_*.txt
    quy_xich_manh.py cat [tờ]   cắt ảnh về (LIEN / K / R) → manh/<vùng>.png, manh/moi.json (mảnh đổi dáng), tờ so manh/_so_*.png
Ảnh con gốc, mảnh gốc là của game tham khảo: chỉ dùng trong máy làm mẫu, không đăng công khai."""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import quy_xich as G  # noqa: E402
from quai.soi import _tris  # noqa: E402
from quai import anh  # noqa: E402

W, H = 1536, 1024
RES = 2                                   # ảnh mảnh của mình = ảnh vùng của họ × RES (atlas họ 0,5 px / đơn vị → mình 1 px / đơn vị)
GUI = os.path.join(HERE, "gui_gpt", "quy_xich_1")
CON = os.path.join(G.TAI, "L1_duyet.png")
CHIEN_SAT = os.path.join(HERE, "inbox", "chien_sat_1", "tai_ve", "L1_duyet.png")
MANH = os.path.join(G.BASE, "manh")
INK = (43, 33, 24)
MUC = "#2B2118"

# màu đo trên concept A (trung vị ô 7 × 7)
MAU = dict(da="#BE452E", giap="#66666C", giap_toi="#4C4C53", thep="#9FA2A7", quan="#3A383D", canh="#5E2C2D", xuong_canh="#3A3236",
           sung="#ECD7AC", vuot="#3A3236", mat="#F5BB3B", nanh="#EFE6D2")


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
    for a in np.arange(0.92, 1.081, 0.01):
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
    """(T: thế giới dáng gốc → px concept, Ti: ngược lại)."""
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


# ================================================================ LIEN: tờ thân liền
LIEN = [("than", ["P_duzi", "P_xionqiang", "P_bozi"]),
        ("tay_gan", ["P_shouR1", "P_shouR2"]),
        ("tay_xa", ["P_shouL1", "P_shouL2"]),
        ("chan_gan", ["P_tuiL1", "P_tuiL2"]),
        ("chan_xa", ["P_tuiR1", "P_tuiR2"])]


# bảng màu được phép lấy từ concept cho từng part (concept lệch chỗ vài chục px so với rig: màu tay, xích, giáp vai của concept rơi vào
# chỗ rig là bụng → chỉ nhận điểm ảnh có màu thuộc part đó); màu đầu tiên là màu lấp khi part không lộ chút nào
BANG = {"P_duzi": ("giap", "quan"), "P_xionqiang": ("giap",), "P_bozi": ("da",),
        "P_shouR1": ("da",), "P_shouR2": ("da", "giap"), "P_shouL1": ("da",), "P_shouL2": ("da", "giap"),
        "P_tuiL1": ("giap_toi", "giap", "quan"), "P_tuiL2": ("giap_toi", "giap", "quan"),
        "P_tuiR1": ("giap_toi", "giap", "quan"), "P_tuiR2": ("giap_toi", "giap", "quan")}


def _hex(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], np.int32)


def to_lien():
    lop, top, thu_tu = lop_goc()
    Cn = np.asarray(Image.open(CON).convert("RGB").resize((W, H), Image.LANCZOS))
    trang = Cn.min(2) > 236
    lum = Cn.astype(np.int32).mean(2)
    # màu gần nhất của từng điểm concept trong bảng màu thiết kế (khoảng cách < 48), −1 nếu không thuộc màu nào
    ten_mau = list(MAU)
    pal = np.stack([_hex(MAU[k]) for k in ten_mau])
    d = np.linalg.norm(Cn[..., None, :].astype(np.int32) - pal[None, None], axis=-1)
    gan_nhat = np.where(d.min(-1) < 48, d.argmin(-1), -1)
    muc = lum < 75
    can_ = np.full((H, W, 3), 255, np.uint8)
    info = {}
    hop = {}
    for ten, ds in LIEN:
        m = np.zeros((H, W), bool)
        for s_ in ds:
            m |= lop[s_][1]
        m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_CLOSE, el(3)).astype(bool)
        ys, xs = np.nonzero(m)
        hop[ten] = (xs.min(), ys.min(), xs.max(), ys.max(), m)
    x0, y0, x1, y1, _ = hop["tay_gan"]
    X0, Y0, X1, Y1, _ = hop["tay_xa"]
    a0, b0, a1, b1, _ = hop["chan_gan"]
    c0, d0, c1, d1, _ = hop["chan_xa"]
    off = {"than": (0, 0), "tay_gan": (24 - x0, 0), "tay_xa": (W - 24 - X1, 0),
           "chan_gan": (60 - a0, max(y1 + 50, 850) - b0), "chan_xa": (W - 60 - c1, max(Y1 + 50, 850) - d0)}
    for ten, ds in LIEN:
        _, _, _, _, m = hop[ten]
        idx = [thu_tu.index(s_) for s_ in ds]
        cua_minh = np.isin(top, idx)
        che = m & ~cua_minh & (top >= 0)                       # bị mảnh khác (đứng trước) che
        hop_le = np.zeros((H, W), bool)                         # điểm concept có màu thuộc bảng của part đang ở trên cùng chỗ đó
        for s_ in ds:
            k_ = thu_tu.index(s_)
            ok_ = np.isin(gan_nhat, [ten_mau.index(c) for c in BANG[s_]])
            if s_ in ("P_shouR2", "P_shouL2") and "giap" in BANG[s_]:   # vòng sắt chỉ ở đầu cổ tay: xa bắp tay ≥ 25 px
                bap = lop[s_.replace("2", "1")][1]
                ok_ &= ~(np.isin(gan_nhat, [ten_mau.index("giap")]) & cv2.dilate(bap.astype(np.uint8), el(25)).astype(bool))
            hop_le |= (top == k_) & ok_
        la = (~hop_le) & (~muc) & (~trang)                      # màu lạ (xích, tay, giáp vai của concept lệch chỗ)
        muc_ok = muc & ~cv2.dilate(la.astype(np.uint8), el(5)).astype(bool) & cua_minh
        nguon = m & ~trang & (hop_le | muc_ok)
        nguon &= ~cv2.dilate(che.astype(np.uint8), el(7)).astype(bool)
        nguon &= cv2.erode(m.astype(np.uint8), el(9)).astype(bool)     # bỏ dải sát mép (viền của concept lệch chỗ): kẻ viền mới
        nguon_mau = nguon & hop_le                              # lấp bằng màu tô, không loang mực
        g = np.zeros((H, W, 3), np.uint8)
        for s_ in ds:                                           # màu nền mặc định của từng part
            g[lop[s_][1] & m] = _hex(MAU[BANG[s_][0]])
        g[nguon] = Cn[nguon]
        lo = m & ~nguon
        if nguon_mau.sum() > 50:
            _, lbl = cv2.distanceTransformWithLabels((~nguon_mau).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
            yy, xx = np.nonzero(nguon_mau)
            bang = np.zeros((lbl.max() + 1, 3), np.uint8)
            bang[lbl[yy, xx]] = Cn[yy, xx]
            # chỉ lấp bằng nguồn gần (≤ 60 px), xa hơn giữ màu mặc định của part (tay xa, chân xa gần như khuất hẳn)
            dist = cv2.distanceTransform((~nguon_mau).astype(np.uint8), cv2.DIST_L2, 5)
            gan_ = lo & (dist <= 60)
            g[gan_] = bang[lbl[gan_]]
        g[m & ~cv2.erode(m.astype(np.uint8), el(3.5)).astype(bool)] = INK      # viền ngoài ~7 px
        dx, dy = off[ten]
        M = np.float32([[1, 0, dx], [0, 1, dy]])
        gm = cv2.warpAffine(m.astype(np.uint8), M, (W, H), flags=cv2.INTER_NEAREST).astype(bool)
        gg = cv2.warpAffine(g, M, (W, H), flags=cv2.INTER_NEAREST)
        can_[gm] = gg[gm]
        info[ten] = dict(slots=ds, off=[int(dx), int(dy)], phu=round(float(nguon.sum()) / max(1, m.sum()), 3))
        print(f"  {ten:9s} dời {dx:5d},{dy:4d}   concept lộ {info[ten]['phu']:.0%} hình bóng")
    os.makedirs(G.MAU, exist_ok=True)
    Image.fromarray(can_).save(os.path.join(G.MAU, "lien.png"))
    json.dump(info, open(os.path.join(G.MAU, "lien.json"), "w"), indent=1)
    print(os.path.join(G.MAU, "lien.png"))
    return info


def prompt_lien():
    gd = os.path.join(G.MAU, "lien.png")
    out = os.path.join(G.TAI, "N_lien.png")
    p = os.path.join(GUI, "luot_2_than_lien.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {Wp(CON)}: the APPROVED character, 1536x1024, white background: a fat red armoured demon with maroon bat wings, a "
         "round iron kettle helmet with ivory bull horns, a big round iron belly plate with a belt, two chains crossing the chest with a "
         "padlock, iron bracers and greaves, a thin red devil tail, holding a big iron meat hook on a chain. It gives the design, the "
         "colours, the ink line and the crayon hatching.",
         f"image 2 = {Wp(gd)}: BODY GUIDE, 1536x1024, white background, assembled by computer from image 1: FIVE separate flat shapes, "
         "each with a dark outline: in the MIDDLE the fat BODY (the round iron belly plate over the huge belly, the belt and the dark "
         "pants at the bottom, the upper chest and the red neck at the top); at the LEFT the NEAR ARM (a fat red arm hanging down: upper "
         "arm and forearm in one shape, an iron bracer at the wrist); at the RIGHT the FAR ARM (a fat red arm bent forward, upper arm, "
         "forearm and the base of the fist in one shape, an iron bracer near the wrist); at the bottom left and bottom right the TWO "
         "SHORT LEGS (a dark iron greave with a stubby foot each). Some places of image 2 are blurry smears: there the shape was hidden "
         "under other parts (the head, the shoulder pad, the chains, the hands) and the computer only spread the nearest colour.",
         "", f"SAVE: save it as a PNG to {Wp(out)}",
         "If a file with that name already exists, save as N_lien_2.png, N_lien_3.png ... in the same folder. Do not edit, move or "
         "delete any other file.", "",
         "TASK: redraw image 2 cleanly in the hand-drawn style of image 1, landscape 1536x1024, pure-white background. Keep EXACTLY every "
         "silhouette of image 2: the same outline, the same size, the same position (if your picture were laid over image 2, the five "
         "shapes must coincide). This sheet will be cut by a program into the body parts of a 2D animation puppet.", "",
         "VERY IMPORTANT, EACH SHAPE IS ONE CONTINUOUS SURFACE: draw the dark-brown ink outline ONLY around the OUTSIDE of each of the "
         "five shapes. Inside a shape draw no line where the upper arm meets the forearm, where the chest meets the belly, where the leg "
         "meets the foot; no folds, no creases, no cut lines. Clean up every blurry smear: continue the surrounding design through it.",
         "",
         f"- BODY (middle): the big rounded iron BELLY PLATE (dark gunmetal {MAU['giap']}) covers the round belly and the chest exactly as "
         "in image 1, with its two curved plate lines across the lower part (thin ink lines following the round belly) and the thick iron "
         f"BELT band ({MAU['giap']} with one ink line on each edge) at its lower edge; under the belt the dark pants ({MAU['quan']}) down to "
         f"the bottom of the shape. At the top of the shape (the neck under the head) red skin {MAU['da']}. Where the chains, the padlock, "
         "the hands and the shoulder pad lay in image 1 just continue the plate (plain gunmetal, the plate lines run on): draw NO chains, "
         "NO padlock, NO navel, NO hands on the body.",
         f"- ARMS: red skin {MAU['da']} with one plain iron bracer band ({MAU['giap']}, light steel {MAU['thep']} rim lines) near the "
         "wrist end, exactly where image 2 shows it; the rest plain red skin; no fingers, no claws (they are separate parts).",
         f"- LEGS: short dark iron greaves {MAU['giap_toi']}, the stubby foot at the bottom the same iron with one ink line.",
         f"- OUTLINE: dark-brown ink ({MUC}), about 7 px thick on this canvas, wobbly like a real pen, closed around each shape and lying "
         "just INSIDE its edge.",
         "Draw nothing else: no head, no wings, no horns, no tail, no chains, no hook, no ground.", "",
         "FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour, the crayon strokes are texture only. No shading, no darker "
         "side, no highlights, no gradients, no cast shadows. Pure white (#FFFFFF) background; no text, no labels, no frames."]
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
            # chỉ lấy trong HÌNH BÓNG của chính part (nới ít, mép mềm): khỏi mang mép thẳng của lưới và mẩu viền part bên cạnh
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
TO_K = [[("P_chibang", 3.0, 0), ("P_tou", 3.4, 0), ("P_jianjiaL", 3.8, 0), ("P_xiongjiaR1", 3.8, 0)],
        [("P_weiba", 3.0, 0), ("P_xiongjiaL1", 4.6, 0), ("W_suolian1", 4.6, 0), ("W_suolian2", 4.6, 0)],
        [("P_shouR31", 4.6, 0), ("P_shouR32", 4.6, 0), ("P_shouR33", 4.6, 0), ("P_shouL31", 4.6, 0), ("P_shouL32", 4.6, 0),
         ("P_shouL33", 4.6, 0)]]
MO_TA_K = {
    "P_chibang": f"A BAT WING (a long curved upper bone with three points along its lower edge and the membrane between them): the wing "
                 f"bones and the thick upper edge charcoal {MAU['xuong_canh']}, the membrane flat dark maroon {MAU['canh']}; keep the thin "
                 "lines of the finger bones.",
    "P_tou": f"THE FACE (a round head seen three-quarters to the right): flat red skin {MAU['da']} everywhere (the top of the head too, "
             f"it is hidden under the helmet), the two narrow slanted angry EYES filled flat yellow {MAU['mat']} with their ink outline "
             f"(no glow, no pupils), the small wavy frowning mouth line and the one tiny fang at its right corner ivory {MAU['nanh']}. "
             "No pink blush, no purple.",
    "P_jianjiaL": f"A SMALL SHOULDER PAD (far shoulder): the curved band becomes one rounded iron plate, dark gunmetal {MAU['giap']} with "
                  f"a light steel {MAU['thep']} rim line along its outer edge; the red crystal on top becomes a short conical iron SPIKE "
                  f"({MAU['giap_toi']}, one ridge line) of the same place and size.",
    "P_xiongjiaR1": f"A DARK ARMOUR PIECE at the near side of the neck: dark iron {MAU['giap_toi']}, plain, one ink line.",
    "P_weiba": f"THE DEVIL TAIL (a thin curved tail with an arrow-head tip on the left): the tail red skin {MAU['da']}, the arrow-head "
               f"tip iron {MAU['giap']}.",
    "P_xiongjiaL1": f"A NARROW DARK ARMOUR PIECE at the far side of the neck: dark iron {MAU['giap_toi']}, plain.",
    "W_suolian1": f"ONE CHAIN LINK seen from the side (a narrow upright bar): steel {MAU['thep']}, a darker steel line down its middle.",
    "W_suolian2": f"ONE CHAIN LINK seen from the front (an upright oval ring with a hole): steel {MAU['thep']}, the hole stays pure "
                  "white (a real hole), a thin ink outline inside and outside.",
    "P_shouR31": f"A FINGER of the near hand (a short thick finger): red skin {MAU['da']} with a small pointed dark claw "
                 f"{MAU['vuot']} at its tip.",
    "P_shouR32": "Another FINGER of the near hand: the same.",
    "P_shouR33": "Another FINGER of the near hand: the same.",
    "P_shouL31": f"A FINGER of the far hand wrapped round the hook shaft (a short thick curled finger): red skin {MAU['da']}, no claw.",
    "P_shouL32": "Another FINGER of the far hand: the same.",
    "P_shouL33": "Another FINGER of the far hand: the same.",
}


def vung():
    """{slot: (att, ảnh part cắt theo lưới)} theo dáng gốc (att_goc); chọn slot đầu tiên mang vùng đó."""
    G._C.pop("att", None)
    _, imgs, atts = G.nap("att_goc.json")
    out = {}
    for a in atts:
        out.setdefault(a["slot"], (a, G.part_goc(a)))
        out.setdefault(a["region"], (a, G.part_goc(a)))
    return out


def to_k():
    V = vung()
    can_ = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    o = {}
    cao = []
    for h_ in TO_K:
        cs = []
        for r, z, xoay in h_:
            im = V[r][1]
            big = im.resize((int(round(im.width * z)), int(round(im.height * z))), Image.LANCZOS)
            cs.append((r, z, xoay, big))
        cao.append((cs, max(c[3].height for c in cs)))
    ke_y = (H - sum(c[1] for c in cao)) // (len(cao) + 1)
    y = ke_y
    for cs, hh in cao:
        ke = (W - sum(c[3].width for c in cs)) // (len(cs) + 1)
        x = ke
        for r, z, xoay, big in cs:
            y0 = y + (hh - big.height) // 2
            can_.alpha_composite(big, (x, y0))
            o[r] = dict(hop=[x, y0, big.width, big.height], z=z, xoay=xoay, vung=V[r][0]["region"])
            x += big.width + ke
        y += hh + ke_y
    p = os.path.join(G.MAU, "goc_K.png")
    can_.convert("RGB").save(p)
    json.dump(o, open(p[:-4] + ".json", "w", encoding="utf-8"), indent=1)
    print(p)
    return o


def prompt_k(o):
    mau = os.path.join(G.MAU, "goc_K.png")
    out = os.path.join(G.TAI, "D_K.png")
    p = os.path.join(GUI, "luot_2_da_K.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {Wp(mau)}: the PARTS SHEET, 1536x1024, white background: fourteen separate body parts of a 2D animation puppet (a "
         "fat demon), each drawn alone, at the exact size and place to keep: top row a bat wing, the face, a small shoulder pad, a dark "
         "neck armour piece; middle row the devil tail, a narrow neck armour piece, a chain link seen from the side, a chain link seen "
         "from the front; bottom row six fingers (three of the near hand, three of the far hand), drawn very big. They are painted in a "
         "smooth purple-and-pink digital style.",
         f"image 2 = {Wp(CON)}: the APPROVED picture of OUR character, 1536x1024, white background: a fat red armoured demon with "
         "maroon bat wings, yellow eyes, dark gunmetal armour and steel chains. Take from it the colours, the materials and the "
         "hand-drawn look (wobbly brown ink line, crayon hatching, flat colour). The shapes come from image 1.",
         f"image 3 = {Wp(CHIEN_SAT)}: another approved hero of the same game: the hand-drawn ink and crayon style to match. Do NOT copy "
         "its design.",
         "", f"SAVE: save it as a PNG to {Wp(out)}",
         "If a file with that name already exists, save as D_K_2.png, D_K_3.png ... in the same folder. Do not edit, move or delete any "
         "other file.", "",
         "TASK: RESKIN. Redraw the SAME sheet with every part REPAINTED as described below, so that the parts can be put back on the same "
         "puppet. For EVERY part keep exactly: its silhouette (the same outline), its size, its orientation and its place on the sheet "
         "(if the new picture were laid over image 1, every part must coincide with the old one), and its main structural lines. Do NOT "
         "merge parts, do NOT add parts, do NOT move parts. Pure white (#FFFFFF) between the parts.", "",
         f"NEW LOOK (see image 2 for the exact colours and drawing style): hand-drawn on paper: a wobbly dark-brown ink outline ({MUC}, "
         "about 9 px) running all the way round every part exactly on its silhouette, thinner ink lines for the inner lines, and every "
         "area filled with ONE flat colour with visible coloured-pencil / wax-crayon hatching. The parts of image 1 are painted in a "
         "smooth digital cel style with purple and pink colours, soft light and dark planes and red glowing eyes: do NOT copy that "
         "painting style or those colours; no shading, no highlights, no white shine streaks, no gradients, no glow, no shadows: flat "
         "colour only. VERY SIMPLE: no extra details.", "",
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


def cat_k():
    path = anh.to_moi_nhat(G.TAI, "D_K")
    if not path:
        print("K: chưa gen")
        return
    V = vung()
    os.makedirs(MANH, exist_ok=True)
    pj = os.path.join(MANH, "_iou.json")
    ious = json.load(open(pj)) if os.path.exists(pj) else {}
    A = np.asarray(Image.open(path).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
    print("K:", os.path.basename(path))
    o = json.load(open(os.path.join(G.MAU, "goc_K.json"), encoding="utf-8"))
    Gd = np.asarray(Image.open(os.path.join(G.MAU, "goc_K.png")).convert("RGB")).astype(np.int32)
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
        a2[..., 3] = np.where(~ag & (a2[..., :3].min(2) > 230), 0, a2[..., 3])      # lỗ trắng (lòng mắt xích) trong suốt
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
        print(f"  {r:12s} → {d['vung']}.png  IoU {iou:.3f}  vá hụt {int(thieu.sum())} px")
    json.dump(ious, open(pj, "w"), indent=1)
    _to_so(so, os.path.join(MANH, "_so_K.png"))


# ================================================================ R1, R2: mảnh đổi dáng, gen đúng chỗ, đúng cỡ trên concept
# mỗi mảnh: (tên, slot của họ mà nó thay, xương bám, tả tiếng Anh)
R = {
    "R1": [("mu_dinh", "P_toukui2", "bone55",
            "the HELMET DOME: the round iron kettle-helmet dome with its raised ridge over the top and the flat BRIM BAND with its four "
            "round rivets along its lower edge, complete on its own (the parts of it hidden behind the horns are drawn too); WITHOUT "
            "the two cheek plates, without the horns"),
           ("vai_to", "P_jianjiaR", "bone26",
            "the BIG SHOULDER PAD on the viewer's left: the two overlapping curved iron plates with the light steel rim and the conical "
            "iron spike on top, complete (the part hidden behind the wing and the arm is drawn too)"),
           ("o_khoa", "P_suo", "bone40",
            "the PADLOCK in the middle of the chest: its rounded body with the keyhole and its shackle, complete, WITHOUT the chains"),
           ("moc", "W_wuqi", "bone14b2",
            "the HOOK WEAPON: the big iron meat-hook blade at the top, the collar ring, the whole thin iron SHAFT going down (complete "
            "where the fist covered it: a straight even shaft) and the small round RING at its lower end, WITHOUT the fist, WITHOUT the "
            "chain")],
    "R2": [("ma_trai", "P_toukui1", "bone12",
            "the LEFT CHEEK PLATE of the helmet: the rounded iron plate that comes down the left side of the face, complete (its top "
            "that was hidden under the brim is drawn too)"),
           ("ma_phai", "P_toukui3", "bone12",
            "the RIGHT CHEEK PLATE of the helmet: the small rounded iron plate on the right side of the face, complete (the part hidden "
            "behind the face is drawn too, as a plain plate)"),
           ("sung_to", "P_jiaoL1", "bone11",
            "the BIG RIGHT HORN: the thick ivory bull horn with its ring lines near the base, complete down to its round base (the base "
            "that was hidden by the helmet is drawn too)"),
           ("sung_nho", "P_jiaoR1", "bone11",
            "the SMALL LEFT HORN: the thick ivory horn on the left of the helmet, complete down to its round base"),
           ("vay_1", "P_jiejing1", "bone10",
            "the BIGGEST BACK FIN (the one nearest to the head): a flat triangular dark iron fin with one ridge line, complete down to "
            "its base (the part hidden behind the shoulder pad and the head is drawn too)"),
           ("vay_2", "P_jiejing2", "bone10", "the MIDDLE BACK FIN: the same kind of fin, smaller, complete"),
           ("vay_3", "P_jiejing3", "bone9", "the SMALLEST BACK FIN (the farthest from the head): the same kind of fin, smallest, complete")],
}
VI_R = {"R1": "đỉnh mũ + vành đinh, giáp vai to + gai, ổ khoá, móc (lưỡi + khâu + cán đủ + vòng cuối)",
        "R2": "má mũ trái, má mũ phải, sừng to, sừng nhỏ, ba vây lưng (vẽ đủ phần khuất)"}


def prompt_r():
    ps = []
    for ma, ds in R.items():
        out = os.path.join(G.TAI, f"M_{ma}.png")
        p = os.path.join(GUI, f"luot_2_manh_{ma}.txt")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(CON)}: the APPROVED picture of OUR character, 1536x1024, white background: a fat red armoured demon with "
             "maroon bat wings, a round iron kettle helmet with ivory bull horns, three dark iron fins on its back, a big iron shoulder "
             "pad with a spike, a big round iron belly plate, two chains crossing the chest with a padlock, holding a big iron meat hook "
             "on a chain.",
             "", f"SAVE: save it as a PNG to {Wp(out)}",
             f"If a file with that name already exists, save as M_{ma}_2.png, M_{ma}_3.png ... in the same folder. Do not edit, move or "
             "delete any other file.", "",
             f"TASK: redraw image 1 with ONLY the {len(ds)} pieces listed below, each in the SAME POSITION and at the SAME SIZE as in "
             "image 1 (if your picture were laid over image 1, every piece must sit exactly on its old place). REMOVE everything else "
             "(the body, the face, the arms, the wings, the tail, the chains, the legs and the other pieces) and leave pure white "
             "there. COMPLETE every piece into ONE CLOSED SHAPE with the ink outline all the way round: the parts of a piece that were "
             "hidden behind other things in image 1 are drawn too, continuing its shape naturally. The pieces stay separate from each "
             "other (a little white gap between them is fine, do not merge them).", "",
             "THE PIECES:"]
        t += [f"{i}. {mt}." for i, (_, _, _, mt) in enumerate(ds, 1)]
        t += ["", f"STYLE: exactly the style of image 1: wobbly dark-brown ink outline ({MUC}, about 7 px), thin ink lines for the few inner "
              "lines, every area ONE flat colour with visible crayon hatching; the same colours as in image 1. No shading, no highlights, "
              "no gradients, no glow, no shadows.", "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no labels, no frame, nothing added."]
        ghi(p, t)
        ps.append((ma, p, out))
        print(p)
    return ps


# tâm từng mảnh trên tờ GPT trả về (px tờ 1536 × 1024, đọc bằng mắt trên M_R1.png / M_R2.png lượt đầu)
TAM_R = {"R1": {"mu_dinh": (785, 240), "vai_to": (535, 410), "o_khoa": (780, 525), "moc": (1100, 560)},
         "R2": {"vay_3": (475, 345), "vay_2": (530, 315), "vay_1": (610, 265), "ma_trai": (710, 380), "sung_nho": (705, 215),
                "sung_to": (910, 200), "ma_phai": (890, 380)}}
# mảnh mà GPT dời chỗ: đặt theo CHỖ PART GỐC (tâm đáy + cao của part họ trên khung concept) thay vì chỗ trên tờ
THEO_GOC = ("vay_1", "vay_2", "vay_3")
# má mũ trái: GPT vẽ to và lấn sang phải, che mắt trái của mặt (mắt trái ở ~x 758 px concept): co 0,85 quanh góc trên phải, mép phải về 728
# cả cụm mũ (đỉnh, hai má, hai sừng) nâng 30 px: mắt của mặt rig (theo hình bóng mặt gốc) ở y 297–318 px concept, cao hơn mắt của
# concept ~25 px; vành mũ đặt theo concept (đáy 316) che mất mắt → đáy vành về ~286, ngay trên mắt như concept
NANG_MU = -30
CHINH = {"ma_trai": dict(s=0.85, dx=728 - 784, dy=NANG_MU), "mu_dinh": dict(dy=NANG_MU), "ma_phai": dict(dy=NANG_MU),
         "sung_to": dict(dy=NANG_MU), "sung_nho": dict(dy=NANG_MU)}


def tach_manh(rgb, tam):
    """tách các mảnh chạm viền nhau: lòng tô (không mực, không trắng) chia vùng liền; mỗi vùng về mảnh có tâm gần nhất; mọi điểm của hình
    (cả viền) về mảnh của lòng tô gần nhất. Trắng khép kín trong hình = lỗ (trong suốt). → {tên: mặt nạ bool}."""
    fg = ~nen_trang(rgb.astype(np.int32))
    lum = rgb.astype(np.int32).mean(2)
    trang = rgb.min(2) > 236
    # mực nâu sẫm (lum ~26–40, đỏ > lam rõ); sắt sẫm (lum ~70, xám trung tính) vẫn là lòng tô
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
    out = {}
    for j, k in enumerate(ten):
        out[k] = fg & ~trang & (thuoc == j)
    return out


def cat_r():
    """mỗi tờ M_R*: tách mảnh (tach_manh), ghi manh/<tên>.png + moi.json (4 góc thế giới khung 0 idle)."""
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
            k = 1.0 / spx * (RES * 0.5)             # px tờ → px ảnh mảnh của mình (1 px / đơn vị rig)
            out = Image.fromarray(rgba, "RGBA").convert("RGBa")
            out = out.resize((max(1, round(out.width * k)), max(1, round(out.height * k))), Image.LANCZOS).convert("RGBA")
            out.save(os.path.join(MANH, ten + ".png"))
            hop = np.array([[x0, y0], [x1 + 1, y0], [x1 + 1, y1 + 1], [x0, y1 + 1]], float)
            if ten in THEO_GOC:                      # đặt theo part gốc: đáy mảnh trùng đáy part gốc, cao bằng part gốc
                g = lop[sl][1]
                gy, gx = np.nonzero(g)
                cao_g = gy.max() - gy.min()
                s_ = cao_g / max(1.0, ys.max() - ys.min())
                dc = np.array([(xs.min() + xs.max()) / 2, ys.max()])
                gc = np.array([(gx.min() + gx.max()) / 2, gy.max()])
                hop = gc + (hop - dc) * s_
            if ten in CHINH:                         # chỉnh tay: co quanh góc trên phải rồi dời (px tờ)
                c_ = CHINH[ten]
                neo = np.array([hop[:, 0].max(), hop[:, 1].min()])
                hop = neo + (hop - neo) * c_.get("s", 1.0) + np.array([c_.get("dx", 0.0), c_.get("dy", 0.0)])
            goc4 = Ti(hop)
            moi[ten] = dict(slot=sl, xuong=bn, hop=[int(x0), int(y0), int(x1 + 1), int(y1 + 1)], the_gioi=goc4.tolist(), to=ma)
            print(f"  {ten:9s} hộp {x0},{y0}–{x1},{y1}  → {ten}.png {out.size}  (thay {sl}, xương {bn})"
                  + ("  [đặt theo part gốc]" if ten in THEO_GOC else ""))
    json.dump(moi, open(pj, "w"), indent=1)


# ================================================================ hướng dẫn
def huong_dan(ps):
    hd = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2")[0].rstrip("\n")
    gd = ["", "## Lượt 2: mảnh theo concept A đã duyệt (2026-11-16)", "",
          "Ba loại tờ (Claude tự gen và tự cắt; người dùng không cần làm gì). Ảnh mảnh gốc là của game tham khảo: chỉ dùng trong máy.", ""]
    for ten, p, rs, vi in ps:
        gd += [f"### {ten}", "", vi, "", f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`.", "",
               "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
        gd += [f"| {i} | `{Wp(r)}` | {v} |" for i, (r, v) in enumerate(rs, 1)]
        gd += [""]
    gd += ["Kiểm: hình bóng trùng tờ hướng dẫn; tờ thân liền không có nét mực ở chỗ nối; mảnh đổi dáng đúng chỗ, đúng cỡ như concept, vẽ đủ phần "
           "khuất; tô phẳng; nền trắng. Cắt: `py -3 -I ArtGen/Spine/quy_xich_manh.py cat`."]
    ghi(hd, (cu + "\n" + "\n".join(gd)).split("\n"))


def to_het():
    if not os.path.exists(os.path.join(G.MAU, "can.json")):
        can()
    to_lien()
    p1, gd1, out1 = prompt_lien()
    o = to_k()
    p2, gd2, out2 = prompt_k(o)
    pr = prompt_r()
    ps = [("Tờ thân liền", p1, [(CON, "Concept A đã duyệt"), (gd1, "Tờ hướng dẫn tự dựng: năm hình bóng phẳng (thân giữa, tay gần trái, "
                                                                     "tay xa phải, hai chân dưới), tô bằng màu concept đã căn lên rig")],
           f"bụng + ngực + cổ, hai tay, hai chân → `{Wp(out1)}`"),
          ("Tờ mảnh rời (khung part)", p2, [(gd2, "Mảnh gốc cắt theo lưới, phóng 3–4,6 lần: cánh, mặt, giáp vai nhỏ, giáp cổ, đuôi, hai mắt "
                                                  "xích, sáu ngón"), (CON, "Concept A"), (CHIEN_SAT, "Chiến binh sắt: chỉ lấy nét")],
           f"→ `{Wp(out2)}`")]
    for ma, p, out in pr:
        ps.append((f"Tờ mảnh đổi dáng {ma}", p, [(CON, "Concept A đã duyệt")], f"{VI_R[ma]} → `{Wp(out)}`"))
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
        if chi in ("", "K"):
            cat_k()
        if chi in ("", "R"):
            cat_r()
    else:
        print(__doc__)
