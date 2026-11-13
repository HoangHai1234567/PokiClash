# -*- coding: utf-8 -*-
"""Voọc Tướng (tho_hoang, mã làm việc kiem_si) DẠNG 1: voọc non trên CÙNG rig của dạng lớn (inbox/kiem_si_1), theo skill
pokiclash-spine-rig mục "DẠNG KHÁC trên CÙNG rig gốc": đổi tỉ lệ ở rig trước, dựng hình bố cục bằng da dạng lớn, rồi mới gen concept.

File riêng (không sửa kiem_si*.py của máy kia, tránh đụng nhau khi đồng bộ git): nạp kiem_si_rig.dung() của dạng lớn (mọi mảnh đã gắn
ở dáng gốc của dạng lớn) rồi nhân tỉ lệ ở xương GỐC của từng cụm SAU khi gắn: điểm gắn tính theo dáng lớn nên tự co theo xương.

Hai tay cùng nắm MỘT thanh kiếm (tay gần nắm vỏ, tay xa nắm chuôi; chuôi là con của vỏ, vỏ là con của bàn tay gần): KHÔNG co riêng từng
tay hay riêng thanh kiếm (tay xa trượt khỏi chuôi), mà co cả nửa thân trên quanh hông (bone3) rồi phóng riêng đầu (bone6: mũ + đầu).

    kiem_si_non.py bo_cuc          dáng gốc (= khung 0 idle) trên nền trắng 1536 × 1024 → inbox/kiem_si_non/mau/bo_cuc.png
                                   + tờ so dạng lớn | dạng non cùng tỉ lệ → inbox/kiem_si_non/mau/so_ti_le.png
    kiem_si_non.py soi <clip> <giây,giây,...> [tỉ lệ]    khung lớn nền xám (da dạng lớn) → inbox/kiem_si_non/rig/soi_<clip>.png
Chạy qua quai/khoa.py nang. Xương và chuyển động nền là của nhà phát hành game tham khảo: dùng nội bộ."""
import json
import os
import sys

os.environ["KS_DANG"] = "1"                      # mảnh, concept, dat.json của dạng lớn
import numpy as np  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from quai import khung, hoat, soi  # noqa: E402
from quai.khung import goc_mat  # noqa: E402
import kiem_si_rig as R  # noqa: E402

TEN = "kiem_si_non"
BASE = os.path.join(HERE, "inbox", TEN)
MAU = os.path.join(BASE, "mau")
RA = os.path.join(BASE, "rig")

# tỉ lệ nhân ở xương gốc của cụm (đều hai trục: chuỗi có khớp gập mà co lệch trục thì xương con bị xiên)
TI = {
    "bone3": 0.80,        # cả nửa thân trên quanh hông: ngực, hai tay, tấm vai, giáp, hai kiếm, áo tơi, đuôi (hai tay vẫn cùng nắm kiếm)
    # mũ + đầu (con của ngực), so với thân đã co. Hướng có giáp (lượt 1): 1,40 (đầu ≈ 1,12 lần dạng lớn); hướng không giáp chibi
    # (lượt 2, không có mũ nên đầu phải to hơn nữa): 1,55 (≈ 1,24 lần)
    "bone6": float(os.environ.get("KS_NON_DAU", "1.55")),
    "Rh": 0.85, "Lq": 0.85,   # bàn chân + giáp ống chân (bám đích chân, gốc ở lòng bàn chân)
    "x_la_to_0": 0.55, "x_la_nho_0": 0.55,   # lá mào: còn mầm lá nhỏ
    "x_duoi_0": 0.85,     # đuôi
}
HA_HONG = 0.14            # hạ hông (bone2) bằng phần này của độ cao hông ở dáng gốc: chân ngắn lại (đùi là lưới giãn)
# Hướng KHÔNG GIÁP (người dùng 2026-11-13: "làm dạng 1 chibi cute kiểu con khỉ không giáp cầm kiếm cũ cùn hoặc cành cây thôi"): bố cục ẩn
# mọi mảnh giáp, mũ, mào, áo tơi, vỏ kiếm và cả kiếm ngắn; lưỡi kiếm dài (k_A_4, trên xương bone51, nằm sẵn dọc vỏ) hiện ra ở dáng nghỉ:
# một món vũ khí trần hai tay cùng nắm. Bao tay, giáp ống chân còn để làm chỗ cho cẳng tay, ống chân trần (prompt dặn vẽ lông).
AN_TRAN = ["vai_g", "vai_x", "tua_g1", "tua_g2", "tua_g3", "tua_x", "giap", "mu", "la_to", "la_nho", "kp_ao",
           "k_A_1", "k_B_1", "k_B_2", "k_B_3"]
# Người dùng chọn hướng kiếm cũ cùn rồi dặn (2026-11-13): "kiếm cùn ở trong, bao kiếm ở ngoài bằng gỗ": vỏ kiếm dài (k_A_1) HIỆN như dạng lớn
# (tay gần nắm miệng vỏ, tay xa nắm chuôi), lưỡi cùn nằm trong vỏ; vẫn bỏ kiếm ngắn.
AN_BAO = [s for s in AN_TRAN if s != "k_A_1"]
AN = {"tran": AN_TRAN, "bao": AN_BAO}


def dinh_so(dat):
    """đỉnh SỌ trên ảnh đầu (px ảnh): hàng cao nhất mà phần đặc rộng hơn 40 % bề ngang ảnh (bỏ chỏm tóc, nút khăn)."""
    import kiem_si_manh as KM
    al = np.asarray(Image.open(os.path.join(KM.MANH, dat["dau"]["anh"] + ".png")).convert("RGBA"))[..., 3] > 120
    for y in range(al.shape[0]):
        xs = np.nonzero(al[y])[0]
        if len(xs) and xs.max() - xs.min() > 0.4 * al.shape[1]:
            return float((xs.min() + xs.max()) / 2), float(y)
    return al.shape[1] / 2, 0.0


def dung_non(cao_tu="mu"):
    sk, info = R.dung()
    W_cu = dict(sk.W0)
    if cao_tu == "dau":                          # dạng 1 không mũ: chiều cao game = đỉnh sọ (không tính chỏm tóc)
        dinh_cu = info["the_gioi"]("dau", [dinh_so(info["dat"])])[0]
        xb_cao = "bone7"
    else:
        w_mu, h_mu = info["dat"]["mu"]["co"]
        dinh_cu = info["the_gioi"]("mu", [[w_mu * 0.6, h_mu * 0.14]])[0]   # đỉnh bát mũ (cách dạng lớn đo chiều cao game)
        xb_cao = "bone6"
    cao_hong = float(W_cu["bone3"][1, 2])
    for nm, k in TI.items():
        b = sk.bones[sk.bi[nm]]
        b["sx"] *= k
        b["sy"] *= k
    sk.bones[sk.bi["bone2"]]["y"] -= HA_HONG * cao_hong
    sk.W0 = sk.the_gioi(khung.Pose())
    p = sk.W0[xb_cao] @ np.linalg.solve(W_cu[xb_cao], np.r_[dinh_cu, 1.0])
    cao = float(p[1])
    far = sk.bones[sk.bi["far"]]
    far["x"], far["y"] = 0.9 * cao + 60.0, 0.45 * cao
    sk.W0 = sk.the_gioi(khung.Pose())
    print(f"dạng non: chiều cao game {cao:.0f} (dạng lớn {info['cao']:.0f}); hông hạ {HA_HONG * cao_hong:.1f} đơn vị")
    info = dict(info, cao=cao, cao_lon=info["cao"])
    return sk, info, W_cu


# ---------------------------------------------------------------- RIG DẠNG 1 (concept duyệt 2026-11-13: tai_ve/L3_bao_go.png)
MANH_NON = os.path.join(BASE, "manh")             # kiem_si_non_manh.py: mảnh dạng lớn đổi màu + mảnh vẽ mới + dat.json dạng 1
MANH_LON = os.path.join(HERE, "inbox", "kiem_si_1", "manh")
# slot dạng 1 bỏ hẳn (không giáp, không mũ, không áo tơi, một kiếm): bỏ trước khi dựng clip để ảnh ảo ảnh chiêu cuối chụp đúng hình khỉ con
BO_SLOT = ["vai_g", "vai_x", "tua_g1", "tua_g2", "tua_g3", "tua_x", "giap", "mu", "kp_ao", "k_B_1", "k_B_2", "k_B_3", "k_B_5", "k_B_6"]
TI_KHAN = 0.85                 # hai đuôi khăn (trên chuỗi xương lá mào cũ, con của mũ bone6 đã × 1,55)
PXU_NHE = 0.26                 # bản NHẸ của dạng lớn gộp vào rig dạng 1 cho clip tiến hóa (dạng lớn thật: 0,56)
TIEU_DE_NON = "Voọc Tướng dạng 1 (kiem_si_non): khỉ voọc con không giáp, kiếm cũ cùn trong vỏ gỗ, tướng thứ 8 đảo Mộc"
E_DUR, E_B0 = 3.0, 1.10        # clip tiến hóa: dài; giây dạng lớn bắt đầu chạy idle


def bo_slot(sk, ten):
    """bỏ hẳn slot (cùng hình, lưới) khỏi rig; ảnh không còn hình nào dùng thì bỏ khỏi atlas."""
    ten = set(ten)
    sk.slots = [s for s in sk.slots if s["name"] not in ten]
    sk.si = {s["name"]: i for i, s in enumerate(sk.slots)}
    for t in ten:
        sk.atts.pop(t, None)
    for k in [k for k in sk.luoi if k[0] in ten]:
        sk.luoi.pop(k)
    dung_ = {spec.get("path") for v in sk.atts.values() for spec in v.values()}
    for k in [k for k in sk.images if k not in dung_]:
        sk.images.pop(k)


def dung_lon_nhe():
    """dạng lớn bản nhẹ (ảnh atlas PXU_NHE) + khung idle của nó, cho clip tiến hóa. Không ảo ảnh."""
    import kiem_si_manh as KM
    import kiem_si_clip as KC
    KM.MANH, pxu = MANH_LON, R.PXU
    R.PXU = PXU_NHE
    sk2, info2 = R.dung()
    R.PXU = pxu
    clips2, _ = KC.lam_clip(sk2, info2)
    idle2 = hoat.nuong(sk2, [c for c in clips2 if c.ten == "idle"][0])
    bo_slot(sk2, [s["name"] for s in sk2.slots if s["name"].startswith("ao_")])
    return sk2, idle2, info2["cao"]


# ĐÙI GẬP (người dùng: mẩu lông thô thò ra cạnh hông ở chiêu cuối): lưới đùi bám cứng hông ở 30 % phía trên rồi chuyển sang cổ chân trong 40 % giữa,
# nên ở thế cúi sâu của chuyển động gốc (hông hạ gần đầu gối) đoạn trên GẬP lên đoạn giữa, mặt sau ảnh lộ ra thành mẩu thô (dạng lớn cũng gập
# 34 khung chiêu cuối, được áo tơi lá che). Gắn lại trọng số đùi ở dáng gốc: chuyển mềm suốt chiều dài, đầu đùi chỉ theo hông DUI_HONG phần:
# đếm trên 6 clip: không còn khung nào gập (bản cũ: chiêu cuối 33 khung).
DUI_W = {"dui_s": "Rh", "dui_t": "Lq"}
DUI_HONG = 0.65


def gan_lai_dui(sk):
    sk_, _ = soi.Ve(sk).skin(khung.Pose())
    by = {x[0]: x for x in sk_}

    def muot(x):
        x = min(1.0, max(0.0, x))
        return x * x * (3 - 2 * x)
    for slot, dich in DUI_W.items():
        _, an, V, uv, _, _, _, _ = by[slot]
        rows = []
        for (x, y), (_, v) in zip(V, uv):
            w3 = (1 - muot(v)) * DUI_HONG
            row = []
            for b, w in (("bone3", w3), (dich, 1 - w3)):
                if w > 1e-4:
                    L = np.linalg.solve(sk.W0[b], np.array([x, y, 1.0]))
                    row.append((b, float(L[0]), float(L[1]), float(w)))
            rows.append(row)
        sk.atts[slot][an]["verts"] = rows


def dung_rig():
    """rig dạng 1 trên mảnh dạng 1: khung cẳng tay đã nới thì đổi toạ độ hai khớp (HAI) theo khung mới; bỏ slot giáp; đuôi khăn."""
    import kiem_si_manh as KM
    KM.MANH = MANH_NON
    dat = json.load(open(os.path.join(MANH_NON, "dat.json"), encoding="utf-8"))
    hai_cu = dict(R.HAI)
    for t, (u0, u1, b0, b1) in hai_cu.items():
        l, tp, r, bt = dat[t].get("noi", [0, 0, 0, 0])
        w, h = dat[t]["co"]
        w0, h0 = w - l - r, h - tp - bt
        f = lambda u: ((u[0] * w0 + l) / w, (u[1] * h0 + tp) / h)          # noqa: E731
        R.HAI[t] = (f(u0), f(u1), b0, b1)
    TI["x_la_to_0"] = TI["x_la_nho_0"] = TI_KHAN
    import kiem_si_non_manh as NM
    duoi_cu = list(R.DUOI_J)
    R.DUOI_J[:] = [tuple(float(v) for v in NM.doi_diem_duoi(p)) for p in duoi_cu]     # khớp đuôi dời cùng ảnh đuôi (dat.json dạng 1)
    try:
        sk, info, W_cu = dung_non(cao_tu="dau")
    finally:
        R.HAI.clear()
        R.HAI.update(hai_cu)
        R.DUOI_J[:] = duoi_cu
    bo_slot(sk, BO_SLOT)
    gan_lai_dui(sk)
    return sk, info, W_cu


# Người dùng 2026-11-13 (ảnh chụp rig dạng 1): "chiêu cuối lỗi" (một khối lông + chỏm đuôi bay lên trên đầu), "đánh thường lỗi lộ đuôi". Nguyên
# nhân: ở con gốc bone31 (nửa cánh cứng trái = áo tơi lá của dạng lớn) và bone32 (nửa cánh phải = mảng lưng lông kp_lung) BẬT LÊN như cánh lúc
# rút hai kiếm / xoay người; dạng lớn có mũ, tấm vai, áo tơi che, dạng 1 không. Đuôi bám bone31. Sửa ở NGUỒN: bỏ chuyển động của hai xương này
# khỏi dữ liệu chuyển động của họ (cả clip lẫn ảnh ảo ảnh chiêu cuối), bỏ gió trên bone31: mảng lưng và đuôi bám theo lưng (bone33).
DUNG_YEN = ("bone31", "bone32")
DUOI_GIU = 0.85          # phần xoay của lưng được bù ở gốc đuôi


def lam_clip_non(sk, info):
    import kiem_si_clip as KC
    cd0 = KC.chuyen_dong

    def cd_non():
        out = cd0()
        for _, (_, res) in out.items():
            for b in DUNG_YEN:
                res.pop(b, None)
        return out
    KC.chuyen_dong = cd_non
    try:
        clips, them = KC.lam_clip(sk, dict(info, ao=[]))
    finally:
        KC.chuyen_dong = cd0
    # ĐUÔI GIỮ HƯỚNG: lúc xoay người quật kiếm (attack) cả lưng xoay, đuôi bám lưng thõng xuống thành vòng ("lộ đuôi"). Bù cho gốc đuôi phần
    # xoay thế giới của xương cha (bone31, đã đứng yên so với lưng) để đuôi vẫn dựng lên; phần đung đưa của chính đuôi giữ nguyên. Chết thì không bù.
    ref = goc_mat(sk.W0["bone31"])
    for c in clips:
        if c.ten in ("die",):
            continue
        f0 = c.fn

        def fn(t, P, f0=f0):
            f0(t, P)
            d = ((ref - goc_mat(sk.the_gioi(P)["bone31"]) + 180.0) % 360.0) - 180.0
            P.rot("x_duoi_0", d * DUOI_GIU)
        c.fn = fn
    return clips, them


# ---------------------------------------------------------------- CHÂN LIỀN (người dùng: "chân không nối đúng khớp")
# Ống chân lông (thay giáp tre) là khối có viền mực kín, vẽ đè lên đùi → ở đầu gối hiện vạch viền và chỗ nối lệch. Theo skill ("các khúc NỐI
# NHAU thì gen LIỀN một ảnh rồi cắt"): mỗi chân (đùi + ống chân) là MỘT hình bóng ở dáng gốc của rig dạng 1, gen một lần (viền chỉ quanh mép ngoài),
# rồi mỗi mảnh lấy điểm ảnh của chính tờ đó qua lưới của nó (thế giới dáng gốc → tờ): hai mảnh chồng nhau lấy CÙNG điểm ảnh, không có nét ở khớp.
CHAN_NHOM = {"s": ["dui_s", "ong_s"], "t": ["dui_t", "ong_t"]}
CHAN_TO = os.path.join(MAU, "chan_lien.png")
NET_CHAN = 6                   # px làm đậm mực mỗi phía trên tờ chân liền
DUI_CAT = {}                   # thử bỏ đầu hông đùi sau (0,30) thì lộ mép cắt ở clip đi: không dùng


def _chan_ve(sk):
    ve = soi.Ve(sk)
    nhom = {}
    for k, ds in CHAN_NHOM.items():
        P = khung.Pose()
        for s in sk.slots:
            if s["name"] not in ds:
                P.alpha[s["name"]] = 0.0
        nhom[k] = (P, ve.bao(P))
    return ve, nhom


def chan_to():
    sk, info, _ = dung_rig()
    ve, nhom = _chan_ve(sk)
    W_, H_ = 1536, 1024
    rong = sum(b[2] - b[0] for _, b in nhom.values())
    cao = max(b[3] - b[1] for _, b in nhom.values())
    ti = min((W_ - 300) / rong, (H_ - 260) / cao)
    can = np.full((H_, W_, 3), 255, np.uint8)
    ke = (W_ - rong * ti) / 3
    x, o = ke, {}
    import cv2
    for k, (P, b) in nhom.items():
        im = np.asarray(ve.ve(P, b, ti, bg=None, ss=2).convert("RGBA"))
        m = im[..., 3] > 100
        m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
        cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)       # lấp lỗ kín bên trong
        m = cv2.drawContours(np.zeros_like(m), cs, -1, 1, -1).astype(bool)
        y0 = int(round((H_ - im.shape[0]) / 2))
        x0 = int(round(x))
        sub = can[y0:y0 + m.shape[0], x0:x0 + m.shape[1]]
        sub[m] = (119, 110, 102)
        mp = np.pad(m, 12)
        vien = mp & ~cv2.erode(mp.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))).astype(bool)
        sub[vien[12:-12, 12:-12]] = (43, 33, 24)
        o[k] = dict(bx=[float(v) for v in b], ti=float(ti), goc=[x0, y0], co=[int(m.shape[1]), int(m.shape[0])])
        x += (b[2] - b[0]) * ti + ke
    os.makedirs(MAU, exist_ok=True)
    Image.fromarray(can).save(CHAN_TO)
    json.dump(o, open(CHAN_TO[:-4] + ".json", "w"), indent=1)
    print(CHAN_TO, {k: v["goc"] + v["co"] for k, v in o.items()})
    tai = os.path.join(BASE, "tai_ve")
    duyet = os.path.join(tai, "L3_bao_go.png")
    hop = {k: f"x = {v['goc'][0]} to {v['goc'][0] + v['co'][0]}, y = {v['goc'][1]} to {v['goc'][1] + v['co'][1]}" for k, v in o.items()}
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {CHAN_TO}: a PARTS GUIDE SHEET, 1536x1024, white background, made by computer: TWO flat grey silhouettes with a dark "
         "outline, each ONE whole LEG of a small monkey for a 2D animation rig (the thigh and the lower leg together, seen from the side, in the "
         "monkey's crouching stance): left = the rear leg, right = the front leg. The upper end of each silhouette goes into the hip (it will "
         "be hidden under a leaf skirt), the lower end is the ankle (a separate bare foot is attached below it, NOT drawn here). The "
         "silhouettes are exact: outline, size, orientation and place must be kept.",
         f"image 2 = {duyet}: the APPROVED character, 1536x1024, white background: a cute chibi baby langur with soft grey fur. It gives the "
         "fur colour, the fur ticks, the wobbly dark-brown ink line and the crayon hatching. Do NOT copy its pose.",
         "", f"SAVE: save it as a PNG to {os.path.join(tai, 'L_chan.png')}",
         "If a file with that name already exists, save as L_chan_2.png, L_chan_3.png ... in the same folder. Do not edit, move or delete any "
         "other file.", "",
         "TASK: redraw image 1 CLEANLY in the hand-drawn style of image 2. Keep EACH silhouette exactly: the same outline, the same size, the "
         "same orientation, the same place on the sheet (laid over image 1, each shape must coincide with its silhouette).",
         f"- Each of the two shapes ({hop['s']} and {hop['t']}) is ONE CONTINUOUS FURRY LEG: fill the whole silhouette with the soft grey fur "
         "(#777066) of image 2 with crayon hatching and a few short curved fur ticks (thin darker pencil strokes) spread over the whole leg. "
         "The dark-brown ink outline (about 6 px) runs ONLY around the outer edge of the silhouette, with small low fur tufts that stay on the "
         "edge. IMPORTANT: NO line, NO crease, NO cuff, NO band, NO colour change ACROSS the leg anywhere (not at the knee, not at the ankle): "
         "the thigh and the lower leg are one single piece of fur.",
         "- Nothing else: no foot, no toes, no armour, no shadows, no glow, no labels.", "",
         "FLAT COLOUR, NO LIGHT, NO SHADOW: one even grey; the pencil and crayon strokes are texture only; no shading, no highlights, no gradients. "
         "Plain pure-white background (#FFFFFF) around the two legs; no frame, no text."]
    p = os.path.join(HERE, "gui_gpt", "kiem_si_non", "luot_5_chan_lien.txt")
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    print(p)


def chan_cat():
    import cv2
    import kiem_si_manh as KM
    sk, info, _ = dung_rig()
    o = json.load(open(CHAN_TO[:-4] + ".json"))
    tai = os.path.join(BASE, "tai_ve")
    ds = sorted([f for f in os.listdir(tai) if f == "L_chan.png" or (f.startswith("L_chan_") and f[7:-4].isdigit())],
                key=lambda f: int(f[7:-4]) if f != "L_chan.png" else 1)
    to_ = np.asarray(Image.open(os.path.join(tai, ds[-1])).convert("RGB").resize((1536, 1024), Image.LANCZOS))
    fg = ~KM.nen(to_.astype(np.int32), 10 ** 9)
    # tờ vẽ ở ~7,4 px mỗi đơn vị rig (gấp ~3 lần các mảnh khác, ~2,5 px): viền 6 px của tờ vào rig chỉ dày 1/3 viền thân (chân trông nhạt, mép
    # răng cưa không nét). Làm đậm vùng MỰC (không đụng nét chì vân lông nhạt hơn) NET_CHAN px mỗi phía trước khi lấy mẫu, như bàn tay dạng lớn.
    muc = cv2.dilate((to_.max(2) < 80).astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * NET_CHAN + 1, 2 * NET_CHAN + 1))) > 0
    to_ = to_.copy()
    to_[muc] = (43, 33, 24)
    fg = ((fg | muc).astype(np.uint8)) * 255
    dat = json.load(open(os.path.join(MANH_NON, "dat.json"), encoding="utf-8"))
    sk_, _ = soi.Ve(sk).skin(khung.Pose())
    by = {x[0]: x for x in sk_}
    so = []
    for k, ds_ in CHAN_NHOM.items():
        g = o[k]
        x0w, _, _, y1w = g["bx"]
        T = lambda V, g=g, x0w=x0w, y1w=y1w: np.stack([g["goc"][0] + (V[:, 0] - x0w) * g["ti"], g["goc"][1] + (y1w - V[:, 1]) * g["ti"]], -1)  # noqa: E731
        for s in ds_:
            _, _, V, uv, tris, _, _, _ = by[s]
            ten = dat[s]["anh"]
            p = os.path.join(MANH_NON, ten + ".png")
            # HÌNH BÓNG lấy từ nguồn CỐ ĐỊNH, không từ ảnh đang có (lần chạy trước đã ghi đè nó): đùi = ảnh dạng lớn (cùng hình bóng với bản đổi
            # màu); ống chân = bản cắt tờ N2, sao lưu lần đầu vào manh/_truoc_chan/
            luu = os.path.join(MANH_NON, "_truoc_chan")
            os.makedirs(luu, exist_ok=True)
            if ten.startswith("dui"):
                nguon = os.path.join(MANH_LON, ten + ".png")
            else:
                nguon = os.path.join(luu, ten + ".png")
                if not os.path.exists(nguon):
                    import shutil
                    shutil.copy2(p, nguon)
            cu = np.asarray(Image.open(nguon).convert("RGBA"))
            h, w = cu.shape[:2]
            rgb = np.zeros((h, w, 3), np.uint8)
            mfg = np.zeros((h, w), np.uint8)
            S_ = T(V).astype(np.float32)
            D_ = (np.asarray(uv, float) * np.array([w, h])).astype(np.float32)
            for tr in tris:
                M = cv2.getAffineTransform(S_[tr], D_[tr])
                mk = np.zeros((h, w), np.uint8)
                cv2.fillConvexPoly(mk, np.round(D_[tr]).astype(np.int32), 1)
                cv2.polylines(mk, [np.round(D_[tr]).astype(np.int32)], True, 1, 2)
                wr = cv2.warpAffine(to_, M, (w, h), flags=cv2.INTER_LINEAR, borderValue=(255, 255, 255))
                wf = cv2.warpAffine(fg, M, (w, h), flags=cv2.INTER_LINEAR, borderValue=0)
                rgb[mk > 0] = wr[mk > 0]
                mfg[mk > 0] = wf[mk > 0]
            a_cu = cv2.dilate((cu[..., 3] > 60).astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
            a = np.minimum(mfg.astype(np.float32) / 255.0, a_cu.astype(np.float32))
            a = cv2.GaussianBlur(a, (0, 0), 0.7)
            out = np.dstack([rgb, (np.clip(a, 0, 1) * 255).astype(np.uint8)])
            out[..., :3][out[..., 3] == 0] = 0
            Image.fromarray(out, "RGBA").save(p)
            phu = float(((out[..., 3] > 120) & (cu[..., 3] > 120)).sum()) / max(1, float((cu[..., 3] > 120).sum()))
            print(f"  {s:6s} ({ten}): lấy từ tờ chân liền, phủ {phu * 100:.0f} % hình bóng cũ")
            so.append(Image.fromarray(out, "RGBA"))
    # đầu HÔNG của đùi sau (ảnh dui1, phần v < DUI_CAT bám hẳn bone3, lúc đứng luôn nằm dưới váy / lưng) chìa ra quá mép trái váy ở chiêu cuối
    # (thân nhổm lên, xoay): bỏ phần đó, mép cắt mờ dần 4 % bề cao ảnh
    for ten, v0 in DUI_CAT.items():
        p = os.path.join(MANH_NON, ten + ".png")
        a = np.asarray(Image.open(p).convert("RGBA")).astype(np.float32)
        h = a.shape[0]
        v = (np.arange(h, dtype=np.float32) / h)[:, None]
        a[..., 3] *= np.clip((v - v0) / 0.04, 0, 1)
        Image.fromarray(a.astype(np.uint8), "RGBA").save(p)
        print(f"  {ten}: bỏ đầu hông v < {v0:.2f}")
    print("→", MANH_NON)


def lam_rig():
    from quai import tienhoa, xuat
    sk2, idle2, cao2 = dung_lon_nhe()
    sk, info, _ = dung_rig()
    clips, them = lam_clip_non(sk, info)
    ti = info["cao"] / cao2
    M = tienhoa.gop(sk, sk2)

    def bung(t, P, fl):                            # dạng lớn hiện ra đang chạy idle chậm, vươn người, ngẩng đầu rồi về dáng thủ
        n = len(idle2) - 1
        x = min(1.0, max(0.0, (t - E_B0) / (E_DUR - E_B0))) * n
        i0 = min(int(x), n)
        i1 = min(i0 + 1, n)
        w = x - i0
        for b in set(idle2[i0].t) | set(idle2[i1].t):
            v0, v1 = idle2[i0].t.get(b, khung.ZERO), idle2[i1].t.get(b, khung.ZERO)
            P.t["n_" + b] = [v0[q] * (1 - w) + v1[q] * w for q in range(5)]
        P.move("n_bone", 0.0, 30.0 * fl)
        P.rot("n_bone5", 4.0 * fl)
        P.rot("n_bone6", 6.0 * fl)

    ev = tienhoa.clip_tien_hoa(M, sk, sk2, idle2[0], tiB=ti, dur=E_DUR, fnB=bung, gam=(1.45, 1.85, 2.25, 2.65), mem=[])
    _, _, s_ev = tienhoa.lech_cuoi(M, hoat.nuong(M, ev), sk2, idle2[0], ti)
    noi = dict(them or {}, evolve=s_ev + f" (dạng lớn co {ti:.3f} trong rig gộp)")
    print("  evolve:", noi["evolve"])
    xuat.xuat_het(M, clips + [ev], RA, TEN, TIEU_DE_NON, dang=1, so_dang=2, dung_yen=("skill",), lao=("cast",), far=("skill",),
                  cao=info["cao"], ma_goc=None, tol={"rotate": 0.05, "translate": 0.12, "scale": 0.001}, khop_idle=0.2, noi_them=noi)


def lam_lon2():
    """dạng lớn xuất lại là DẠNG 2 trên 2 (cho lúc vào game làm dòng hai dạng) → inbox/kiem_si_non/rig_lon/."""
    import kiem_si_manh as KM
    import kiem_si_clip as KC
    from quai import xuat
    KM.MANH = MANH_LON
    sk, info = R.dung()
    clips, them = KC.lam_clip(sk, info)
    xuat.xuat_het(sk, clips, os.path.join(BASE, "rig_lon"), "kiem_si_1", R.TIEU_DE, dang=2, so_dang=2, dung_yen=("skill",), lao=("cast",),
                  far=("skill",), cao=info["cao"], ma_goc=None, tol={"rotate": 0.05, "translate": 0.12, "scale": 0.001}, khop_idle=0.2,
                  noi_them=them)


def ve_dang(sk, P=None, bg=(255, 255, 255), sc=None, bx=None):
    ve = soi.Ve(sk)
    P = P or khung.Pose()
    bx = bx or ve.bao(P)
    sc = sc or min(1240.0 / (bx[2] - bx[0]), 900.0 / (bx[3] - bx[1]))
    return ve.ve(P, bx, sc, bg=bg, ss=2).convert("RGB"), sc, bx


def main(a):
    if a and a[0] == "rig":                        # rig dạng 1 đủ clip + tiến hóa → inbox/kiem_si_non/rig/
        return lam_rig()
    if a and a[0] == "lon2":
        return lam_lon2()
    if a and a[0] in ("chan_to", "chan_cat"):
        return {"chan_to": chan_to, "chan_cat": chan_cat}[a[0]]()
    if a and a[0] == "soi_rig":                    # soi_rig <clip> <giây,...> [tỉ lệ]: khung lớn của rig dạng 1 (mảnh dạng 1)
        sk, info, _ = dung_rig()
        clips, _ = lam_clip_non(sk, info)
        c = [x for x in clips if x.ten == a[1]][0]
        fr = hoat.nuong(sk, c)
        ts = [float(x) for x in a[2].split(",")]
        ve = soi.Ve(sk)
        Ps = [fr[min(len(fr) - 1, int(round(t * 30)))] for t in ts]
        Bx = soi._union([ve.bao(P) for P in Ps], 0.04)
        sc = float(a[3]) if len(a) > 3 else 1.0
        ims = [ve.ve(P, Bx, sc, bg=(150, 150, 150), ss=2).convert("RGB") for P in Ps]
        cot = min(len(ims), 6)
        out = Image.new("RGB", (ims[0].width * cot, ims[0].height * ((len(ims) + cot - 1) // cot)), (150, 150, 150))
        for i, im in enumerate(ims):
            out.paste(im, ((i % cot) * im.width, (i // cot) * im.height))
        os.makedirs(RA, exist_ok=True)
        pth = os.path.join(RA, f"soi1_{a[1]}.png")
        out.save(pth)
        print(pth, out.size)
        return
    sk, info, W_cu = dung_non()
    if not a or a[0] == "bo_cuc":
        im, sc, bx = ve_dang(sk)
        out = Image.new("RGB", (1536, 1024), (255, 255, 255))
        o = ((1536 - im.width) // 2, (1024 - im.height) // 2)
        out.paste(im, o)
        os.makedirs(MAU, exist_ok=True)
        pth = os.path.join(MAU, "bo_cuc.png")
        out.save(pth)
        json.dump({"sc": sc, "bx": [float(v) for v in bx], "o": list(o)}, open(os.path.join(MAU, "bo_cuc.json"), "w"))
        print(pth, f"{sc:.4f} px mỗi đơn vị rig; khung", [round(float(v)) for v in bx])
        # tờ so: dạng lớn (dựng lại, chưa đổi tỉ lệ) | dạng non, CÙNG tỉ lệ px / đơn vị, chung đường đất
        sk_lon, _ = R.dung()
        ve_l, ve_n = soi.Ve(sk_lon), soi.Ve(sk)
        bl, bn = ve_l.bao(khung.Pose()), ve_n.bao(khung.Pose())
        y0, y1 = min(bl[1], bn[1]), max(bl[3], bn[3])
        s2 = 820.0 / (y1 - y0)
        il = ve_l.ve(khung.Pose(), (bl[0], y0, bl[2], y1), s2, bg=(255, 255, 255), ss=2).convert("RGB")
        inn = ve_n.ve(khung.Pose(), (bn[0], y0, bn[2], y1), s2, bg=(255, 255, 255), ss=2).convert("RGB")
        so = Image.new("RGB", (il.width + inn.width + 60, max(il.height, inn.height) + 50), (255, 255, 255))
        so.paste(il, (10, 40))
        so.paste(inn, (il.width + 50, 40))
        d = ImageDraw.Draw(so)
        d.text((14, 10), f"dang lon (cao game {info['cao_lon']:.0f})", fill=(40, 30, 20))
        d.text((il.width + 54, 10), f"dang non (cao game {info['cao']:.0f})", fill=(40, 30, 20))
        pth = os.path.join(MAU, "so_ti_le.png")
        so.save(pth)
        print(pth, so.size)
        return
    if a[0] in ("bo_cuc_tran", "bo_cuc_bao"):      # bố cục không giáp (tran: vũ khí trần; bao: kiếm trong vỏ gỗ) → mau/<lệnh>.png
        kieu = a[0][7:]
        P = khung.Pose()
        for s_ in AN[kieu]:
            P.alpha[s_] = 0.0
        out = Image.new("RGB", (1536, 1024), (255, 255, 255))
        goc = os.path.join(MAU, "bo_cuc_tran.json")
        if kieu == "bao" and os.path.exists(goc):
            # CÙNG hệ toạ độ với bố cục "tran" (concept L2_kiem_cun vẽ theo nó): vỏ chìa xa hơn sang trái thì vẽ khung rộng hơn rồi dán lệch
            g = json.load(open(goc))
            sc, (tx0, _, _, ty1), (tox, toy) = g["sc"], g["bx"], g["o"]
            im, _, bx = ve_dang(sk, P, sc=sc)
            o = (int(round(tox + (bx[0] - tx0) * sc)), int(round(toy + (ty1 - bx[3]) * sc)))
        else:
            im, sc, bx = ve_dang(sk, P)
            o = ((1536 - im.width) // 2, (1024 - im.height) // 2)
        out.paste(im, o)
        os.makedirs(MAU, exist_ok=True)
        pth = os.path.join(MAU, f"bo_cuc_{kieu}.png")
        out.save(pth)
        json.dump({"sc": sc, "bx": [float(v) for v in bx], "o": list(o), "dau": TI["bone6"]},
                  open(os.path.join(MAU, f"bo_cuc_{kieu}.json"), "w"))
        print(pth, f"{sc:.4f} px mỗi đơn vị rig; khung", [round(float(v)) for v in bx])
        return
    if a[0] == "vung":                             # toạ độ từng mảnh trên hình bố cục (px); vung tran|bao: bố cục không giáp
        kieu = a[1] if len(a) > 1 else None
        bc = json.load(open(os.path.join(MAU, f"bo_cuc_{kieu}.json" if kieu else "bo_cuc.json")))
        sc, (x0, y0, x1, y1), (ox, oy) = bc["sc"], bc["bx"], bc["o"]
        to_px = lambda w: (ox + (w[0] - x0) * sc, oy + (y1 - w[1]) * sc)      # noqa: E731
        P0 = khung.Pose()
        for s_ in AN.get(kieu, []):
            P0.alpha[s_] = 0.0
        sk_, _ = soi.Ve(sk).skin(P0)
        for nm, _, V, _, _, al, _, _ in sk_:
            if al <= 0.01:
                continue
            p0, p1 = to_px((V[:, 0].min(), V[:, 1].max())), to_px((V[:, 0].max(), V[:, 1].min()))
            print(f"  {nm:12s} x {p0[0]:5.0f}–{p1[0]:5.0f}  y {p0[1]:5.0f}–{p1[1]:5.0f}")
        # điểm trên concept dạng lớn (px khung concept, theo prompt luot_1_concept_khi_mu) → bố cục dạng non, theo xương mang nó
        MOC = {"mắt": ((1020, 490), "bone7"), "tay gần": ((860, 790), "bone24"), "tay xa": ((1055, 815), "bone20"),
               "mũi vỏ kiếm dài": ((222, 470), "bone47"), "đầu chuôi kiếm dài": ((1230, 820), "bone51"),
               "huy hiệu tấm vai": ((585, 400), "bone43"), "chóp lá mào to": ((1330, 70), "x_la_to_1"),
               "chóp đuôi": ((555, 110), "x_duoi_4"), "chân sau": ((555, 920), "Rh"), "chân trước": ((935, 925), "Lq")}
        for ten, (p, b) in MOC.items():
            w = info["px_tg"](p)
            w2 = sk.W0[b] @ np.linalg.solve(W_cu[b], np.r_[w, 1.0])
            q = to_px(w2[:2])
            print(f"  mốc {ten:20s} ({q[0]:.0f}, {q[1]:.0f})")
        return
    if a[0] == "soi":                              # soi <clip> <giây,...> [tỉ lệ]
        import kiem_si_clip as KC
        clips, _ = KC.lam_clip(sk, info)
        c = [x for x in clips if x.ten == a[1]][0]
        fr = hoat.nuong(sk, c)
        ts = [float(x) for x in a[2].split(",")]
        ve = soi.Ve(sk)
        Ps = [fr[min(len(fr) - 1, int(round(t * 30)))] for t in ts]
        Bx = soi._union([ve.bao(P) for P in Ps], 0.04)
        sc = float(a[3]) if len(a) > 3 else 1.0
        ims = [ve.ve(P, Bx, sc, bg=(150, 150, 150), ss=2).convert("RGB") for P in Ps]
        cot = min(len(ims), 6)
        hang = (len(ims) + cot - 1) // cot
        out = Image.new("RGB", (ims[0].width * cot, ims[0].height * hang), (150, 150, 150))
        for i, im in enumerate(ims):
            out.paste(im, ((i % cot) * im.width, (i // cot) * im.height))
        os.makedirs(RA, exist_ok=True)
        pth = os.path.join(RA, f"soi_{a[1]}.png")
        out.save(pth)
        print(pth, out.size)


if __name__ == "__main__":
    main(sys.argv[1:])
