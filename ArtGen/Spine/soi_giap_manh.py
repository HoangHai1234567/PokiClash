# -*- coding: utf-8 -*-
"""Sói giáp sắt (soi_giap, rig monster_3428): MẢNH theo concept B đã duyệt (sói đen than, giáp gang + đồng thau). Ba loại mảnh:

  1. TỜ LIỀN (L): các mảnh LÔNG nối nhau gen thành hình liền rồi nướng vào khung từng part qua lưới (luật "khớp nối gen liền"):
     thân (hông + ngực/giáp ngực + bờm), chân gần, chân xa, tay gần, tay xa: mỗi nhóm một hình bóng liền, chỉ viền ngoài + ranh chất liệu.
  2. TỜ Ô (A, C): mảnh có viền riêng (vạt, mặt + ô MẶT HÁ gầm, đuôi, dây da, quai khiên, nút đai, mặt dây, ngón, mắt): tờ hướng dẫn là
     CHÍNH mảnh gốc cắt theo lưới, GPT đổi da giữ hình bóng (skill rig mục 23).
  3. LƯỢT MỚI (M1–M4): mảnh ĐỔI DÁNG gen "đúng chỗ, đúng cỡ" từ concept B: mũ (mặt nạ + mảnh đỉnh gộp), búa, giáp vai ba gai, khiên
     nghiêng, tấm gáy, hai tai dựng. Khiên nhìn thẳng (W_dunpai2) = khiên nghiêng lật ngang (con gốc cũng vậy).

    soi_giap_manh.py to        tờ A, C, L + mọi prompt → inbox/soi_giap_1/mau/, gui_gpt/soi_giap_1/luot_2_*.txt
    soi_giap_manh.py cat       cắt mọi tờ / lượt đã về → inbox/soi_giap_1/manh/ (<vùng>.png ×RES, moi.json, _iou.json, tờ so)
Ảnh mảnh gốc là của game tham khảo: chỉ dùng trong máy làm mẫu, không đăng công khai."""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import soi_giap as G  # noqa: E402
import soi_giap_da as D  # noqa: E402

W, H = 1536, 1024
S2 = 2                                   # siêu lấy mẫu khi vẽ tờ liền
RES = 2                                  # ảnh mảnh của mình = ảnh vùng của họ × RES
MANH = os.path.join(G.BASE, "manh")
CONCEPT = os.path.join(G.TAI, "L1_duyet.png")
GUI = D.GUI
INK = (43, 33, 24)
Wp = D.Wp
ghi = D.ghi

# bảng màu đo trên concept B
MAU = dict(long=(82, 78, 83), long_nhat=(196, 189, 194), gang=(75, 79, 88), gang_toi=(63, 66, 73), dong=(212, 164, 81),
           da=(103, 69, 52), vat=(94, 65, 50), vuot=(58, 52, 56), mat=(227, 141, 61))
HEX = {k: "#%02X%02X%02X" % v for k, v in MAU.items()}
CO_BOM = 1.0                             # dạng non đặt < 1: bờm co lại trên tờ liền


def goc_tat_ca(att="att_goc.json"):
    """{vùng: (hình đầu tiên dùng vùng đó, ảnh part cắt theo lưới)}, CẢ hình không bật ở idle (W_dunpai2, P_yanjin2)."""
    G._C.pop("att", None)
    _, imgs, _ = G.nap(att)
    Dj = json.load(open(os.path.join(G.scan(), att), encoding="utf-8"))
    out = {}
    for a in sorted(Dj["atts"], key=lambda a: a["order"]):
        r = a.get("region")
        if r in imgs and r not in out:
            out[r] = (a, G.part_goc(a))
    return out


def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


# ================================================================ 1. TỜ LIỀN
# nhóm: (tên, các slot theo THỨ TỰ VẼ của họ, sau → trước). Chất liệu từng slot ở CHAT.
LIEN = [("tay_gan", ["P_shouR31", "P_shouR2", "P_shouR1"]),
        ("than", ["P_shenti1", "P_shenti2", "P_tou2"]),
        ("tay_xa", ["P_shouL1", "P_shouL2", "P_shouL3"]),
        ("chan_gan", ["P_tuiR3", "P_tuiR2", "P_tuiR1"]),
        ("chan_xa", ["P_tuiL3", "P_tuiL2", "P_tuiL1"])]
HANG = [["tay_gan", "than", "tay_xa"], ["chan_gan", "chan_xa"]]
CHAT = {"P_shouR31": "ban_tay", "P_shouR2": "bao_tay", "P_shouR1": "long", "P_shouL1": "long", "P_shouL2": "bao_tay", "P_shouL3": "ban_tay",
        "P_shenti1": "long", "P_shenti2": "nguc", "P_tou2": "long", "P_tuiR3": "ban_chan", "P_tuiR2": "long", "P_tuiR1": "long",
        "P_tuiL3": "ban_chan", "P_tuiL2": "long", "P_tuiL1": "long"}


def _att_idle():
    Dj = json.load(open(os.path.join(G.scan(), "att_idle0.json"), encoding="utf-8"))
    return {a["slot"]: a for a in Dj["atts"] if a.get("region") and a["cur"]}


def _bong(a, T, shape):
    """mặt nạ hình bóng một part (tam giác lưới vẽ lên canvas theo phép T: thế giới → px canvas), lấy theo alpha ảnh part gốc."""
    _, imgs, _ = G.nap(G._C.get("att"))
    im = G.part_goc(a)
    uv, tr = G.luoi(a)
    P = T(np.array(a["xy"], float).reshape(-1, 2))
    lay = Image.new("RGBa", (shape[1], shape[0]), (0, 0, 0, 0))
    from quai.soi import _tris
    _tris(lay, im.convert("RGBa"), P, uv, tr)
    A = np.asarray(lay.convert("RGBA"))
    return A[..., 3] > 90, A[..., :3]


def to_lien():
    by = _att_idle()
    hop = {}
    for ten, ds in LIEN:
        P = np.concatenate([np.array(by[t]["xy"], float).reshape(-1, 2) for t in ds])
        hop[ten] = (P[:, 0].min(), P[:, 1].min(), P[:, 0].max(), P[:, 1].max())
    ke = 46
    rong = [sum(hop[t][2] - hop[t][0] for t in h_) for h_ in HANG]
    cao = [max(hop[t][3] - hop[t][1] for t in h_) for h_ in HANG]
    ti = min(min((W - ke * (len(h_) + 1)) / r for h_, r in zip(HANG, rong)), (H - ke * (len(HANG) + 1)) / sum(cao))
    goc = {}
    y = ke + (H - ke * (len(HANG) + 1) - sum(cao) * ti) / 2
    for h_, r, c in zip(HANG, rong, cao):
        k = (W - r * ti) / (len(h_) + 1)
        x = k
        for t in h_:
            x0, y0, x1, y1 = hop[t]
            # px = (ox + X·ti, oy − Y·ti); đáy các nhóm cùng hàng nằm trên một đường (y + c·ti)
            goc[t] = (x - x0 * ti, y + c * ti + y0 * ti)
            x += (x1 - x0) * ti + k
        y += c * ti + ke
    Hs, Ws = H * S2, W * S2
    can = np.full((Hs, Ws, 3), 255, np.uint8)
    for ten, ds in LIEN:
        ox, oy = goc[ten]
        T = lambda V, ox=ox, oy=oy: np.stack([(ox + V[:, 0] * ti) * S2, (oy - V[:, 1] * ti) * S2], 1)
        ms, cs = {}, {}
        for t in ds:
            ms[t], cs[t] = _bong(by[t], T, (Hs, Ws))
            ms[t] = cv2.morphologyEx(ms[t].astype(np.uint8), cv2.MORPH_CLOSE, el(3 * S2)).astype(bool)
            if t == "P_tou2" and CO_BOM < 1.0:                    # dạng non: bờm co còn chỏm lông quanh cổ (co về phía đầu, đầu phải hình)
                ys, xs = np.nonzero(ms[t])
                nep = xs > np.percentile(xs, 85)
                ax, ay = float(xs[nep].mean()), float(ys[nep].mean())
                M = np.float32([[CO_BOM, 0, ax * (1 - CO_BOM)], [0, CO_BOM, ay * (1 - CO_BOM)]])
                ms[t] = cv2.warpAffine(ms[t].astype(np.uint8), M, (Ws, Hs), flags=cv2.INTER_NEAREST).astype(bool)
        hop_m = np.zeros((Hs, Ws), bool)
        for t in ds:
            hop_m |= ms[t]
        hop_m = cv2.morphologyEx(hop_m.astype(np.uint8), cv2.MORPH_CLOSE, el(4 * S2)).astype(bool)
        nhan = np.zeros((Hs, Ws), np.uint8)              # nhãn chất liệu: 1 lông, 2 lông nhạt, 3 gang, 4 đồng, 5 vuốt
        for t in ds:                                     # sau → trước: mảnh trước đè
            m = ms[t]
            ch = CHAT[t]
            if ch == "long":
                nhan[m] = 1
            elif ch in ("ban_tay", "ban_chan"):
                nhan[m] = 2
                if ch == "ban_chan":                     # vuốt: chỗ ảnh gốc tối ở nửa trước bàn chân
                    lum = cs[t].astype(np.int32).sum(2) / 3
                    nhan[m & (lum < 95)] = 5
            elif ch == "bao_tay":
                nhan[m] = 3
                ys, xs = np.nonzero(m)
                P = np.c_[xs, ys].astype(float)
                c0 = P.mean(0)
                u, s_, vt = np.linalg.svd(P - c0, full_matrices=False)
                tr = (P - c0) @ vt[0]
                lo, hi = np.percentile(tr, 2), np.percentile(tr, 98)
                dai = hi - lo
                bang = (tr < lo + 0.13 * dai) | (tr > hi - 0.13 * dai)
                nhan[ys[bang], xs[bang]] = 4
            elif ch == "nguc":                           # giáp ngực = phần lông trắng phía trước của ngực gốc (nới, làm trơn)
                lum = cs[t].astype(np.int32).sum(2) / 3
                tr_ = m & (lum > 175)
                tr_ = cv2.morphologyEx(tr_.astype(np.uint8), cv2.MORPH_OPEN, el(6 * S2))
                tr_ = cv2.dilate(tr_, el(14 * S2))
                tr_ = cv2.morphologyEx(tr_, cv2.MORPH_CLOSE, el(20 * S2)).astype(bool) & m
                nhan[m] = 1
                nhan[tr_] = 3
                vanh = tr_ & ~cv2.erode(tr_.astype(np.uint8), el(9 * S2)).astype(bool)
                Y = np.arange(Hs)[:, None]
                ys, xs = np.nonzero(tr_)
                tren = Y < ys.min() + (ys.max() - ys.min()) * 0.45
                nhan[vanh & tren] = 4
        nhan[~hop_m] = 0
        bang_mau = {1: MAU["long"], 2: MAU["long_nhat"], 3: MAU["gang"], 4: MAU["dong"], 5: MAU["vuot"]}
        for k, c in bang_mau.items():
            can[(nhan == k) & hop_m] = c
        # nét mực: viền ngoài nhóm + ranh giữa hai chất liệu khác nhau (KHÔNG có nét giữa hai mảnh cùng chất lông)
        vien = hop_m & ~cv2.erode(hop_m.astype(np.uint8), el(7 * S2)).astype(bool)
        ranh = np.zeros_like(hop_m)
        for k in bang_mau:
            mk = (nhan == k).astype(np.uint8)
            ranh |= cv2.morphologyEx(mk, cv2.MORPH_GRADIENT, el(2 * S2)).astype(bool)
        ranh &= hop_m
        can[vien | ranh] = INK
    os.makedirs(G.MAU, exist_ok=True)
    p = os.path.join(G.MAU, "lien.png")
    Image.fromarray(can).resize((W, H), Image.LANCZOS).save(p)
    json.dump({"ti": ti, "goc": goc, "nhom": LIEN}, open(p[:-4] + ".json", "w"), indent=1)
    print(p, f"{ti:.3f} px / đơn vị")


# ================================================================ 2. TỜ Ô (mảnh gốc làm hướng dẫn)
TO = {
    "A": [[("P_tou1", 2.6), ("MAT_HA", 2.6), ("P_yaodai", 2.6), ("P_weiba", 2.6)],
          [("P_xianglian1", 3.0), ("P_shouR12", 3.0), ("W_dunpai6", 3.0), ("W_dunpai4", 3.0)]],
    "C": [[("P_shouL31", 4.5), ("P_shouR32", 4.5), ("P_diaozhui3", 4.5), ("P_diaozhui1", 4.5)],
          [("P_yanjin1", 7.0), ("P_yanjin2", 7.0)]],
}
HA_K = 1.55                                # ô mặt há: cao gấp HA_K lần ô mặt (chừa chỗ hàm dưới há xuống)
PX = {"A": "8", "C": "12"}
SO_PART = {"A": "Top row: a wolf face (muzzle with a black nose and a leather strap), the SAME face again in a taller box with empty "
                "space under it, a long ragged hanging cloth flap, a small bushy tail tip. Bottom row: a crescent leather neck strap, a "
                "curved leather shoulder strap, a curved leather shield strap with a small buckle, a thin long leather strap.",
           "C": "Top row: the claws of a paw, small fingers, a knot of rope, a small long pendant. Bottom row: an open eye (a small "
                "triangle-like eye shape) and a closed eye (a '>' shape), drawn very big."}
VI_TO = {"A": "mặt, ô mặt há, vạt, đuôi; dây cổ, dây vai, quai khiên, quai trong", "C": "vuốt tay xa, ngón tay gần, nút đai, mặt dây; mắt mở, mắt nhắm"}
MO_TA = {
    "A": [
        ("P_tou1", f"THE FACE (a wolf head seen from the side, turned to the right, its muzzle pointing right): fur on the top and the back "
                   f"of the head charcoal {HEX['long']}; the muzzle, the cheeks and the jaw pale grey {HEX['long_nhat']} with a few spiky "
                   f"fur tufts on the cheek edge; the nose at the right tip black; the diagonal leather strap across the face dark brown "
                   f"{HEX['da']} with a small brass {HEX['dong']} stud; the small white spot on the head stays a small pale mark; the mouth "
                   "CLOSED, a short firm mouth line with ONE small white fang poking down at its front. Do not draw an eye (the eye is a "
                   "separate part)."),
        ("MAT_HA", "THE SAME FACE, ROARING (the box is taller than the face: the top of the box holds the face of image 1, the lower part "
                   "is empty): keep the upper half of the face (the top of the head, the nose, the strap) EXACTLY as in the face box to its "
                   "left, at the same place inside this box; but the LOWER JAW is dropped wide open, hinged at the back of the cheek: a big "
                   "open mouth showing a dark red inside #5A2228, a pink tongue #B5525A, two long white fangs on top and two at the bottom "
                   "jaw, the lower jaw pale grey with charcoal fur underneath, reaching down into the empty lower part of the box. A fierce "
                   "battle roar."),
        ("P_yaodai", f"THE LONG HANGING CLOTH FLAP with a ragged lower edge: dark brown leather-cloth {HEX['vat']}, its top band (the part "
                     f"under the belt) the same colour with one ink line; the small diamond ornament at the top becomes a small square brass "
                     f"{HEX['dong']} plate; a few thin fold lines."),
        ("P_weiba", f"THE TAIL TIP (a bushy tuft pointing left): charcoal fur {HEX['long']} with a pale grey {HEX['long_nhat']} tip, spiky fur "
                    "edge."),
        ("P_xianglian1", f"THE NECK STRAP (a thick crescent): dark brown leather {HEX['da']}, one thin darker line along its middle."),
        ("P_shouR12", f"THE SHOULDER STRAP (a thick curved band): dark brown leather {HEX['da']}, one thin darker line along its middle."),
        ("W_dunpai6", f"THE SHIELD STRAP on the forearm (a thick curved band with a small buckle at its right end): dark brown leather "
                      f"{HEX['da']}, the buckle brass {HEX['dong']}."),
        ("W_dunpai4", f"THE THIN INNER STRAP (a long thin curved band): dark brown leather {HEX['da']}."),
    ],
    "C": [
        ("P_shouL31", f"THE CLAWS / FINGERS of a paw (three pale finger tips with dark claws): fingers pale grey {HEX['long_nhat']}, claws "
                      f"dark {HEX['vuot']}."),
        ("P_shouR32", f"SMALL FINGERS of a paw (pale finger tips with a small dark claw): pale grey {HEX['long_nhat']}, claws dark "
                      f"{HEX['vuot']}."),
        ("P_diaozhui3", f"THE KNOT at the side of the belt: dark brown leather {HEX['da']} with one thin line."),
        ("P_diaozhui1", f"THE PENDANT: now a ROUND BRASS DISC {HEX['dong']} with a thin ink ring line inside, filling the upper part of the "
                        "shape (its width = the width of the shape), and a short leather loop above it; nothing below the disc."),
        ("P_yanjin1", f"THE OPEN EYE (drawn very big): a narrow fierce eye slit, flat orange {HEX['mat']} with a small dark pupil and one "
                      "tiny pale dot, thick dark ink outline, a heavy upper lid line (an angry look). Same outline as image 1."),
        ("P_yanjin2", "THE CLOSED EYE (drawn very big): a thick dark ink '>' shape (a squeezed shut eye), same shape and place as image 1."),
    ],
}
CHUNG = (
    "TASK: RESKIN. Image 1 is a sheet of separate body PARTS of a 2D animation puppet (a big wolf warrior), each part drawn alone on "
    "white. Redraw the SAME sheet with every part REPAINTED as described below, so that the parts can be put back on the same puppet. "
    "For EVERY part keep exactly: its silhouette (the same outline), its size, its orientation and its place on the sheet (if the new "
    "picture were laid over image 1, every part must coincide with the old one), except where a part below says otherwise. Do NOT merge "
    "parts, do NOT add parts, do NOT move parts. Pure white (#FFFFFF) between the parts.")
STYLE2 = (
    "NEW LOOK (see image 2, the approved picture of OUR character, for the exact colours and drawing style): a charcoal-furred wolf "
    "warrior with blackened iron armour, brass trims and dark brown leather straps. Hand-drawn on paper: a wobbly dark-brown ink outline "
    "(#2B2118, about {px} px) running all the way round every part exactly on its silhouette, thinner ink lines for the few inner lines, "
    "and every area filled with ONE flat colour with visible coloured-pencil / wax-crayon hatching. The parts of image 1 are painted in a "
    "smooth digital style with mauve-grey fur and soft light / dark shading: do NOT copy that painting style or those colours; no shading, "
    "no highlights, no gradients, no glow, no shadows: flat colour only. SIMPLE: no extra details beyond what is listed.")
BG2 = "Plain pure-white background (#FFFFFF), no paper grain outside the parts, no labels, no numbers, no frame, nothing added."


def _o(V, r, z):
    """ảnh hướng dẫn của một ô (ảnh part gốc phóng z; ô mặt há = mặt gốc ở đỉnh một ô cao HA_K lần)."""
    if r == "MAT_HA":
        f = V["P_tou1"][1]
        big = f.resize((int(round(f.width * z)), int(round(f.height * z))), Image.LANCZOS)
        o = Image.new("RGBA", (big.width, int(round(big.height * HA_K))), (0, 0, 0, 0))
        o.alpha_composite(big, (0, 0))
        return o
    im = V[r][1]
    return im.resize((int(round(im.width * z)), int(round(im.height * z))), Image.LANCZOS)


def to_o():
    V = goc_tat_ca()
    O = {}
    for ma, hang in TO.items():
        can = Image.new("RGBA", (W, H), (255, 255, 255, 255))
        o = {}
        cao = []
        for h_ in hang:
            cs = [(r, z, _o(V, r, z)) for r, z in h_]
            cao.append((cs, max(c[2].height for c in cs)))
        ke_y = (H - sum(c[1] for c in cao)) // (len(cao) + 1)
        y = ke_y
        for cs, hh in cao:
            ke = (W - sum(c[2].width for c in cs)) // (len(cs) + 1)
            x = ke
            for r, z, big in cs:
                y0 = y + (hh - big.height) // 2
                can.alpha_composite(big, (x, y0))
                o[r] = dict(hop=[x, y0, big.width, big.height], z=z)
                if r == "MAT_HA":                         # khung ô mặt há: kẻ chữ nhật xám mảnh để GPT thấy chỗ được vẽ hàm
                    ImageDraw.Draw(can).rectangle([x - 2, y0 - 2, x + big.width + 2, y0 + big.height + 2], outline=(205, 205, 205), width=2)
                x += big.width + ke
            y += hh + ke_y
        p = os.path.join(G.MAU, f"goc_{ma}.png")
        can.convert("RGB").save(p)
        json.dump(o, open(p[:-4] + ".json", "w", encoding="utf-8"), indent=1)
        O[ma] = o
        print(p)
    return O


# ================================================================ 3. LƯỢT MỚI (đổi dáng, gen đúng chỗ từ concept B)
MOI = {
    "M1": [("mu", f"THE HELMET on the wolf's head: the blackened iron helmet {HEX['gang']} with its FLAT top, its front brim edged with "
                  f"brass {HEX['dong']} just above the eye, and the two dark iron fins sweeping back from its top. Draw it COMPLETE as ONE "
                  "closed shape, the parts hidden behind the ears and behind the back plate drawn too; its lower edge is the brass brim at "
                  "the front and a plain iron edge at the back. NO ears, NO face, NO fur, NO eye.",
            "mũ (đỉnh bằng, vành đồng, hai vây sắt; vẽ đủ phần nấp sau tai và tấm gáy; không tai, không mặt)"),
           ("bua", f"THE WHOLE WAR HAMMER at the lower left: the squared blackened iron block head {HEX['gang']} with its brass band, the "
                   "curved iron spike (beak) on its upper end, and the long dark iron handle with its two brass rings and its knob, going up "
                   "to the left. Draw it COMPLETE as ONE closed shape: the part of the handle hidden behind the fist drawn too (straight, the "
                   "same width), NO hand, NO fingers.",
            "cả cây búa (vẽ đủ đoạn cán nấp sau nắm tay, không tay)")],
    "M2": [("vai", f"THE BIG ROUND SHOULDER PLATE on the left shoulder: the blackened iron dome {HEX['gang']} with its brass rim {HEX['dong']} "
                   "and the THREE short iron spikes along its top. Draw it COMPLETE as ONE closed shape: its lower part hidden behind the "
                   "arm and the mane drawn too (the dome curves down and ends in a rounded lower edge). NO fur, NO arm.",
            "giáp vai tròn ba gai (vẽ đủ phần nấp)"),
           ("khien", f"THE BIG SHIELD on the right: the tall blackened iron shield {HEX['gang']} with its cut-off corners, the raised "
                     "vertical ridge down its front face, its thick darker side edge on the right, and its round brass rivets. Draw it "
                     "COMPLETE as ONE closed shape: the part hidden behind the arm, the paw and the head drawn too (plain iron, the ridge "
                     "running straight down). NO arm, NO paw, NO strap.",
            "khiên (vẽ đủ phần nấp sau tay, bàn tay, đầu; không tay, không quai)")],
    "M3": [("gay", f"THE TALL SQUARE BACK PLATE behind the head: the blackened iron plate {HEX['gang']} with its brass rim along its top "
                   "edge. Draw it COMPLETE as ONE closed shape: its lower part hidden behind the helmet, the head and the mane drawn too, "
                   "ending in a straight lower edge at about the height of the eye. NO helmet, NO head, NO fur.",
            "tấm gáy vuông (vẽ đủ phần nấp sau mũ, đầu, bờm)")],
    "M4": [("tai_gan", f"THE NEAR EAR (the bigger pointed ear standing up on the LEFT side of the helmet): charcoal fur {HEX['long']} "
                       f"outside, pale grey {HEX['long_nhat']} inside. Draw it COMPLETE as ONE closed shape: its base hidden under the "
                       "helmet drawn too, ending in a rounded base. NO helmet.",
            "tai gần (vẽ đủ gốc nấp dưới mũ)"),
           ("tai_xa", f"THE FAR EAR (the smaller pointed ear standing up on the RIGHT side of the helmet): charcoal fur {HEX['long']} "
                      f"outside, pale grey {HEX['long_nhat']} inside. Draw it COMPLETE as ONE closed shape: its base hidden behind the "
                      "helmet drawn too, ending in a rounded base. NO helmet.",
            "tai xa (vẽ đủ gốc nấp sau mũ)")],
}
# vùng (px trên concept 1536 × 1024) chứa từng mảnh mới: chọn cụm liền lớn nhất có tâm nằm trong vùng
VUNG = {"mu": (760, 60, 1330, 470), "bua": (180, 560, 680, 1024), "vai": (280, 60, 760, 520), "khien": (900, 0, 1300, 1024),
        "gay": (680, 0, 1000, 420), "tai_gan": (740, 120, 960, 360), "tai_xa": (960, 120, 1180, 360)}


def prompt():
    O = to_o()
    to_lien()
    hd = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2")[0].rstrip("\n")
    gd = ["", "## Lượt 2: mảnh theo concept B (2026-11-16)", "",
          "Ba loại: tờ LIỀN (L: lông thân, chân, tay gen liền rồi nướng vào từng mảnh), tờ Ô (A, C: mảnh gốc cắt theo lưới làm hướng dẫn, "
          "GPT đổi da giữ hình bóng), lượt MỚI (M1–M4: mảnh đổi dáng gen đúng chỗ từ concept B). Ảnh mảnh gốc là của game tham khảo: "
          "chỉ dùng trong máy làm mẫu, không đăng công khai.", ""]
    R2 = (CONCEPT, "the APPROVED picture of OUR character, 1536x1024, white background: a big charcoal-furred wolf warrior with a pale grey "
                   "muzzle and paws, orange eyes, a flat-topped blackened iron helmet with a brass brim, a round spiked shoulder plate, a "
                   "blackened iron breastplate with a brass rim and three brass rivets, iron bracers with brass bands, dark brown leather "
                   "straps and belt with a brass buckle, a long dark brown cloth flap, a tall blackened iron shield and an iron war hammer. "
                   "Take from it the colours, the materials and the hand-drawn look (wobbly brown ink line, crayon hatching, flat colour).",
          "Concept B đã duyệt: lấy màu, chất liệu, nét vẽ tay")
    # tờ ô
    for ma, o in O.items():
        mau = os.path.join(G.MAU, f"goc_{ma}.png")
        out = os.path.join(G.TAI, f"D_{ma}.png")
        p = os.path.join(GUI, f"luot_2_da_{ma}.txt")
        R = [(mau, "the PARTS SHEET, 1536x1024, white background: separate body parts of the puppet, each drawn alone, at the exact size "
                   "and place to keep. " + SO_PART[ma] + " They are painted in a smooth mauve-grey digital style.",
              f"Tờ mảnh gốc cắt từ rig con gốc (1536 × 1024, nền trắng): {VI_TO[ma]}. Hình số màu xám tím"), R2]
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {en}" for i, (r, en, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
              f"If a file with that name already exists, save as D_{ma}_2.png, D_{ma}_3.png ... in the same folder. Do not edit, move or "
              "delete any other file.", "", CHUNG, "", STYLE2.format(px=PX[ma]), "",
              "THE PARTS (coordinates are pixels on the 1536x1024 sheet, x from the left, y from the top):"]
        for i, (r, mt) in enumerate(MO_TA[ma], 1):
            x, y, cw, ch = o[r]["hop"]
            t.append(f"{i}. (about x = {x} to x = {x + cw}, y = {y} to y = {y + ch}) {mt}")
        t += ["", BG2]
        ghi(p, t)
        print(p)
        gd += [f"### Tờ `{ma}`: {VI_TO[ma]}", "", f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`; ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).",
               "", "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
        gd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
        gd += [""]
    # tờ liền
    gl = os.path.join(G.MAU, "lien.png")
    out = os.path.join(G.TAI, "N_lien.png")
    p = os.path.join(GUI, "luot_2_lien.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {Wp(CONCEPT)}: {R2[1]}",
         f"image 2 = {Wp(gl)}: BODY GUIDE, 1536x1024, white background, drawn by computer: FIVE flat silhouettes of the wolf's body "
         "parts WITHOUT the head, the helmet, the shoulder plate, the straps, the belt, the cloth flap, the shield and the hammer. Top row, "
         "left to right: the NEAR ARM (furry upper arm, iron bracer forearm with brass bands, pale paw closed in a fist), the TORSO (the "
         "furry hips at the bottom, the chest with the iron breastplate, the big shaggy fur mane at the top flowing to the left), the FAR "
         "ARM (furry upper arm, iron bracer forearm with brass bands, pale paw). Bottom row: the NEAR LEG and the FAR LEG (furry thigh and "
         "shin, a pale paw with dark claws). Charcoal = fur, pale grey = paws, dark grey = blackened iron, gold = brass. It gives the exact "
         "silhouettes, sizes and positions.", "",
         f"SAVE: save it as a PNG to {Wp(out)}",
         "If a file with that name already exists, save as N_lien_2.png, N_lien_3.png ... in the same folder. Do not edit, move or delete "
         "any other file.", "",
         "TASK: redraw image 2 cleanly in the hand-drawn style of image 1, landscape 1536x1024, pure-white background. Keep EXACTLY every "
         "silhouette of image 2: the same outline, the same size, the same position (if your picture were laid over image 2, the shapes "
         "must coincide). This sheet will be cut by a program into the body parts of a 2D animation rig.", "",
         "VERY IMPORTANT, ONE CONTINUOUS SURFACE PER SHAPE: each of the five shapes is ONE body part. Draw the dark-brown ink outline ONLY "
         "around the OUTSIDE of each shape and along the edges of the iron pieces (the breastplate, the bracers). INSIDE the fur draw NO "
         "outline at all: no line where the upper arm meets the shoulder, no line between the thigh and the shin, no line between the mane "
         "and the chest, no line between the hips and the chest. The fur colour and the crayon hatching run across the whole shape without "
         "any break.", "",
         f"- FUR: charcoal {HEX['long']} with loose crayon hatching and a few short spiky fur tufts drawn with thin lines on the outer "
         "edges (the mane is shaggy with spiky tufts along its outline).",
         f"- PAWS: pale grey {HEX['long_nhat']}; the near paw is a closed fist; the feet have short dark claws {HEX['vuot']} at the toe tips "
         "where image 2 shows dark marks.",
         f"- BREASTPLATE (on the torso, where image 2 shows dark grey): blackened iron {HEX['gang']}, a brass {HEX['dong']} rim along its "
         "top edge, three round brass rivets in a row across its upper part, one ink line down its middle; no muscles drawn on it.",
         f"- BRACERS (the forearms): blackened iron {HEX['gang']} with a brass {HEX['dong']} band at each end, where image 2 shows gold.",
         "- OUTLINE: dark-brown ink (#2B2118), about 7 px thick on this canvas, wobbly like a real pen, closed around each shape and lying "
         "just INSIDE its edge.",
         "Draw nothing else: no head, no face, no helmet, no shoulder plate, no straps, no belt, no cloth, no shield, no hammer, no ground.",
         "", "FLAT COLOUR, NO LIGHT, NO SHADOW: every area is one even colour, the crayon strokes are texture only. No shading, no darker "
         "side, no highlights, no gradients, no cast shadows. Pure white (#FFFFFF) background; no text, no labels, no frames."]
    ghi(p, t)
    print(p)
    gd += ["### Tờ liền `L`: lông thân, chân, tay", "", f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`; ảnh lưu vào `{Wp(out)}`.", "",
           "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|",
           f"| 1 | `{Wp(CONCEPT)}` | {R2[2]} |",
           f"| 2 | `{Wp(gl)}` | Tờ hướng dẫn tự dựng: năm hình bóng phẳng (tay gần, thân + giáp ngực + bờm, tay xa; chân gần, chân xa), lông than, "
           "bàn tay chân xám nhạt, gang sẫm, đồng thau; viền chỉ ở ngoài và ranh chất liệu |", ""]
    # lượt mới
    for ma, ds in MOI.items():
        out = os.path.join(G.TAI, f"M_{ma}.png")
        p = os.path.join(GUI, f"luot_2_moi_{ma}.txt")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(CONCEPT)}: {R2[1]}", "",
             f"SAVE: save it as a PNG to {Wp(out)}",
             f"If a file with that name already exists, save as M_{ma}_2.png, M_{ma}_3.png ... in the same folder. Do not edit, move or "
             "delete any other file.", "",
             "TASK: redraw image 1 keeping ONLY the piece(s) listed below, each in the SAME POSITION, at the SAME SIZE and the SAME ANGLE as "
             "in image 1 (laid over image 1 they must coincide); REMOVE everything else (the wolf, the fur, every other piece of armour, "
             "the shield or the hammer if not listed): pure white there. COMPLETE each kept piece into ONE closed shape with a dark-brown "
             "ink outline all the way round, drawing the parts that are hidden in image 1 as described:", ""]
        t += [f"- {en}" for _, en, _ in ds]
        t += ["", "Same drawing style and colours as image 1: wobbly dark-brown ink outline (about 7 px), flat colours with crayon hatching, "
              "no shading, no highlights, no glow. Pure-white background, nothing else on the canvas, no labels."]
        ghi(p, t)
        print(p)
        gd += [f"### Lượt `{ma}`: " + "; ".join(vi for _, _, vi in ds), "",
               f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`; ảnh mẫu duy nhất: concept B `{Wp(CONCEPT)}`; ảnh lưu vào `{Wp(out)}`.", ""]
    gd += ["Kiểm: tờ A, C mỗi mảnh đúng chỗ, cỡ, hình bóng mảnh gốc; tờ L hình bóng trùng tờ hướng dẫn, không nét trong lông; lượt M mảnh "
           "trùng chỗ concept, vẽ đủ phần khuất, không dính mảnh khác. Cắt: `py -3 -I ArtGen/Spine/soi_giap_manh.py cat`."]
    ghi(hd, (cu + "\n" + "\n".join(gd)).split("\n"))


# ================================================================ CẮT
def nen(A):
    trang = (A.min(2) > 238).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(trang, 4)
    bg = np.zeros(trang.shape, bool)
    Hh, Ww = trang.shape
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if x == 0 or y == 0 or x + w == Ww or y + h == Hh:
            bg |= lab == i
    return bg


def _moi_nhat(tien_to):
    fs = sorted([f for f in os.listdir(G.TAI) if f.startswith(tien_to) and f.endswith(".png")],
                key=lambda f: os.path.getmtime(os.path.join(G.TAI, f)))
    return os.path.join(G.TAI, fs[-1]) if fs else None


def _tron_thieu(a2, ag):
    """chỗ GPT vẽ hụt trong hình bóng gốc (sát mép ≤ 5 px): lấy màu gần nhất."""
    thieu = ag & (a2[..., 3] < 128) & cv2.dilate((a2[..., 3] >= 128).astype(np.uint8), el(5)).astype(bool)
    if thieu.any() and (a2[..., 3] >= 128).any():
        co = (a2[..., 3] >= 128).astype(np.uint8)
        _, lbl = cv2.distanceTransformWithLabels(1 - co, cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
        ys_, xs_ = np.nonzero(co)
        bang = np.zeros((lbl.max() + 1, 3), np.uint8)
        bang[lbl[ys_, xs_]] = a2[ys_, xs_, :3]
        a2[thieu, :3] = bang[lbl[thieu]]
        a2[thieu, 3] = 255
    return int(thieu.sum())


def cat_o(V, ious):
    for ma in TO:
        p = _moi_nhat(f"D_{ma}")
        if not p:
            print(f"tờ {ma}: chưa gen")
            continue
        A = np.asarray(Image.open(p).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
        print(f"tờ {ma}: {os.path.basename(p)}")
        o = json.load(open(os.path.join(G.MAU, f"goc_{ma}.json"), encoding="utf-8"))
        Gd = np.asarray(Image.open(os.path.join(G.MAU, f"goc_{ma}.png")).convert("RGB")).astype(np.int32)
        fg, fgG = ~nen(A), ~nen(Gd)
        n, lab, st, _ = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
        for r, d in o.items():
            x, y, cw, ch = d["hop"]
            pad = 14
            x0, y0, x1, y1 = max(0, x - pad), max(0, y - pad), min(W, x + cw + pad), min(H, y + ch + pad)
            if r == "MAT_HA":
                gm = np.ones((y1 - y0, x1 - x0), bool)
            else:
                gm = cv2.dilate(fgG[y0:y1, x0:x1].astype(np.uint8), el(10)).astype(bool)
            ids = [i for i in np.unique(lab[y0:y1, x0:x1][gm]) if i > 0 and st[i, 4] > 60]
            m = np.isin(lab, ids)
            m[:y0] = m[y1:] = False
            m[:, :x0] = m[:, x1:] = False
            # ô mặt há: GPT có thể vẽ hàm tràn xuống quá khung ô → lấy cả cụm, nới khung xuống
            if r == "MAT_HA":
                yy, xx = np.nonzero(np.isin(lab, ids))
                x0b, y0b = min(x, xx.min()), min(y, yy.min())
                x1b, y1b = max(x + cw, xx.max() + 1), max(y + ch, yy.max() + 1)
                m = np.isin(lab, ids)
                x, y, cw, ch = x0b, y0b, x1b - x0b, y1b - y0b
                d["hop_cat"] = [int(x), int(y), int(cw), int(ch)]
            rgb = A[y:y + ch, x:x + cw].astype(np.uint8)
            mm = m[y:y + ch, x:x + cw]
            al = cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.8)
            vien = mm & ~cv2.erode(mm.astype(np.uint8), el(2)).astype(bool)
            al = np.where(vien, np.minimum(al, np.clip((250.0 - rgb.min(2).astype(np.float32)) / 70.0, 0, 1)), al)
            im = Image.fromarray(np.dstack([rgb, (np.clip(al, 0, 1) * 255).astype(np.uint8)]), "RGBA")
            if r == "MAT_HA":
                f = V["P_tou1"][1]
                k = (f.width * RES) / float(o["P_tou1"]["hop"][2])      # cùng tỉ lệ px như mảnh mặt
                im2 = im.convert("RGBa").resize((max(1, int(round(cw * k))), max(1, int(round(ch * k)))), Image.LANCZOS).convert("RGBA")
                im2.save(os.path.join(MANH, "mat_ha.png"))
                d["k"] = k
                json.dump(o, open(os.path.join(G.MAU, f"goc_{ma}.json"), "w", encoding="utf-8"), indent=1)
                print(f"  mat_ha       {im2.size}  (khung cắt {d['hop_cat']})")
                continue
            goc = V[r][1]
            tw, th = goc.width * RES, goc.height * RES
            a2 = np.asarray(im.convert("RGBa").resize((tw, th), Image.LANCZOS).convert("RGBA")).copy()
            ag = np.asarray(goc.resize((tw, th), Image.LANCZOS))[..., 3] > 60
            if r != "P_diaozhui1":                                # mặt dây đổi dáng (đĩa tròn): không xén theo hình bóng cũ
                a2[..., 3] = np.where(cv2.dilate(ag.astype(np.uint8), el(3)).astype(bool), a2[..., 3], 0)
                va = _tron_thieu(a2, ag)
            else:
                va = 0
            Image.fromarray(a2, "RGBA").save(os.path.join(MANH, r + ".png"))
            b = fgG[y:y + ch, x:x + cw]
            iou = float((mm & b).sum()) / max(1, (mm | b).sum())
            ious[r] = round(iou, 3)
            print(f"  {r:13s} IoU {iou:.3f}  vá hụt {va} px")


def _the_gioi_o(a, w, h):
    """toạ độ thế giới (dáng idle 0) của từng pixel trong khung ảnh vùng (w × h) của một part, qua lưới của nó; NaN ngoài lưới."""
    U = np.array(a["uv"], float).reshape(-1, 2) * np.array([w, h])
    Vv = np.array(a["xy"], float).reshape(-1, 2)
    ys, xs = np.mgrid[0:h, 0:w]
    P = np.c_[xs.ravel() + 0.5, ys.ravel() + 0.5]
    Wd = np.full((len(P), 2), np.nan)
    tot = np.full(len(P), -9.0)
    for t in np.array(a["tris"]).reshape(-1, 3):
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
        Wd[hon] = b0[hon, None] * Vv[t[0]] + b1[hon, None] * Vv[t[1]] + b2[hon, None] * Vv[t[2]]
        tot[hon] = nho[hon]
    return Wd.reshape(h, w, 2)


def cat_lien(V):
    from quai import anh
    p = _moi_nhat("N_lien")
    if not p:
        print("tờ L: chưa gen")
        return
    L = json.load(open(os.path.join(G.MAU, "lien.json"), encoding="utf-8"))
    im = Image.open(p).convert("RGB")
    if im.size != (W, H):
        im = im.resize((W, H), Image.LANCZOS)
        p2 = os.path.join(G.MAU, "_N_lien_doi_co.png")
        im.save(p2)
        p = p2
    tt = anh.doc_to(p, dien_tich_min=600, gop_px=10)
    rgba = tt.rgba.astype(np.float32)
    rgba[..., :3] *= rgba[..., 3:4] / 255.0
    by = _att_idle()
    ti = L["ti"]
    print(f"tờ L: {os.path.basename(p)}")
    for ten, ds in L["nhom"]:
        ox, oy = L["goc"][ten]
        for s in ds:
            a = by[s]
            goc = V[a["region"]][1]
            w, h = goc.width * RES, goc.height * RES
            Wd = _the_gioi_o(a, w, h)
            ok = ~np.isnan(Wd[..., 0])
            mx = np.where(ok, ox + Wd[..., 0] * ti, -10).astype(np.float32)
            my = np.where(ok, oy - Wd[..., 1] * ti, -10).astype(np.float32)
            cell = cv2.remap(rgba, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
            al = cell[..., 3:4]
            cell[..., :3] = np.where(al > 1, cell[..., :3] * 255.0 / np.maximum(al, 1), 0)
            # chỉ lấy trong hình bóng của chính part (nới 1,4 px, mép mềm)
            sil = np.asarray(goc.resize((w, h), Image.LANCZOS))[..., 3].astype(np.float32) / 255.0
            sil = np.clip(cv2.GaussianBlur(cv2.dilate((sil > 0.25).astype(np.uint8), el(1.4 * RES)).astype(np.float32), (0, 0), 0.9 * RES)
                          * 2.0 - 0.5, 0, 1)
            cell[..., 3] *= sil
            out = np.clip(cell, 0, 255).astype(np.uint8)
            Image.fromarray(out, "RGBA").save(os.path.join(MANH, a["region"] + ".png"))
            phu = float((out[..., 3] > 127).sum()) / max(1, int((sil > 0.5).sum()))
            print(f"  {s:12s} {w}×{h}  phủ {phu:.2f} hình bóng")


def cat_moi():
    pm = os.path.join(MANH, "moi.json")
    moi = json.load(open(pm)) if os.path.exists(pm) else {}
    for ma, ds in MOI.items():
        p = _moi_nhat(f"M_{ma}")
        if not p:
            print(f"lượt {ma}: chưa gen")
            continue
        A = np.asarray(Image.open(p).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
        fg = ~nen(A)
        n, lab, st, _ = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
        for ten, _, _ in ds:
            x0, y0, x1, y1 = VUNG[ten]
            cand = [i for i in range(1, n) if st[i, 4] > 300 and x0 <= st[i, 0] + st[i, 2] / 2 <= x1 and y0 <= st[i, 1] + st[i, 3] / 2 <= y1]
            if not cand:
                print(f"  {ten}: KHÔNG thấy cụm")
                continue
            i = max(cand, key=lambda j: st[j, 4])
            m = lab == i
            x, y, w, h = st[i, :4]
            rgb = A[y:y + h, x:x + w].astype(np.uint8)
            mm = m[y:y + h, x:x + w]
            # lỗ giấy trắng khép kín trong mảnh (khoen, khe) giữ nguyên là thịt: nen() chỉ bỏ trắng nối mép tờ
            al = cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.8)
            Image.fromarray(np.dstack([rgb, (np.clip(al, 0, 1) * 255).astype(np.uint8)]), "RGBA").save(os.path.join(MANH, ten + ".png"))
            moi[ten] = dict(hop=[int(x), int(y), int(w), int(h)], nguon=os.path.basename(p))
            print(f"  {ten:8s} khung trên concept {x},{y} {w}×{h}  ({os.path.basename(p)})")
    json.dump(moi, open(pm, "w"), indent=1)


def khop_concept():
    """phép đồng dạng ảnh con gốc (goc_ca_con.png, px) → concept B (px): dò tỉ lệ + dời cho hình bóng trùng nhất (IoU), ghi
    mau/khop_concept.json {k, dx, dy}: concept = goc · k + (dx, dy). Kèm phép px gốc ↔ thế giới khung 0 idle (goc_ca_con.json)."""
    g = D._mat_na(os.path.join(G.MAU, "goc_ca_con.png")).astype(np.uint8)
    c = D._mat_na(CONCEPT).astype(np.uint8)
    q = 4                                              # dò thô trên ảnh thu 1/4
    gs, cs_ = cv2.resize(g, (W // q, H // q), interpolation=cv2.INTER_AREA) > 0, cv2.resize(c, (W // q, H // q), interpolation=cv2.INTER_AREA) > 0

    def iou_of(k, dx, dy, a, b, sc):
        M = np.array([[k, 0, dx / sc], [0, k, dy / sc]], np.float32)
        wa = cv2.warpAffine(a.astype(np.uint8), M, (b.shape[1], b.shape[0]), flags=cv2.INTER_NEAREST) > 0
        return (wa & b).sum() / max(1, (wa | b).sum())
    best = (0, None)
    cy0, cx0 = np.argwhere(g).mean(0)
    cy1, cx1 = np.argwhere(c).mean(0)
    for k in np.arange(1.20, 1.56, 0.02):
        dx0, dy0 = cx1 - k * cx0, cy1 - k * cy0
        for ddx in range(-80, 81, 8):
            for ddy in range(-80, 81, 8):
                v = iou_of(k, dx0 + ddx, dy0 + ddy, gs, cs_, q)
                if v > best[0]:
                    best = (v, (k, dx0 + ddx, dy0 + ddy))
    k0, dx0, dy0 = best[1]
    for k in np.arange(k0 - 0.02, k0 + 0.021, 0.005):          # tinh trên ảnh đủ cỡ
        for ddx in range(-8, 9, 2):
            for ddy in range(-8, 9, 2):
                v = iou_of(k, dx0 + ddx, dy0 + ddy, g > 0, c > 0, 1)
                if v > best[0]:
                    best = (v, (k, dx0 + ddx, dy0 + ddy))
    iou, (k, dx, dy) = best
    gj = json.load(open(os.path.join(G.MAU, "goc_ca_con.json")))
    out = dict(k=float(k), dx=float(dx), dy=float(dy), iou=float(iou), s=gj["s"], cx=gj["cx"], cy=gj["cy"])
    json.dump(out, open(os.path.join(G.MAU, "khop_concept.json"), "w"), indent=1)
    print(f"concept = gốc × {k:.3f} + ({dx:.1f}, {dy:.1f}); IoU {iou:.3f}")
    return out


def concept_ra_the_gioi(P, kc=None):
    """px concept B → thế giới khung 0 idle (y lên)."""
    kc = kc or json.load(open(os.path.join(G.MAU, "khop_concept.json")))
    P = np.asarray(P, float)
    gx, gy = (P[..., 0] - kc["dx"]) / kc["k"], (P[..., 1] - kc["dy"]) / kc["k"]
    return np.stack([(gx - W / 2) / kc["s"] + kc["cx"], -(gy - H / 2) / kc["s"] + kc["cy"]], -1)


def cat():
    os.makedirs(MANH, exist_ok=True)
    V = goc_tat_ca()
    pj = os.path.join(MANH, "_iou.json")
    ious = json.load(open(pj)) if os.path.exists(pj) else {}
    cat_o(V, ious)
    json.dump(ious, open(pj, "w"), indent=1)
    cat_lien(V)
    cat_moi()


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "to":
        prompt()
    elif cmd == "lien":
        to_lien()
    elif cmd == "cat":
        cat()
    elif cmd == "khop":
        khop_concept()
    else:
        print(__doc__)
