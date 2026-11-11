"""Dòng Hải Long, dạng 1 và 2 (mã tm10_1, tm10_2; dạng 3 = hai_long.py bản 4). Dùng lại bộ máy của hai_long.py (giải cổ, dải lưới
B-spline, râu dây mềm, băng chuyền sóng, aura, mặt nạ cắt) bằng cách vá các hằng của nó cho từng dạng, nạp mảnh thân từ
inbox/tm10_<k>/manh và mảnh nước dùng lại của dạng 3 (inbox/hai_long/manh). Tiến hóa: gộp rig dạng sau (JSON Spine đã xuất) vào rig
dạng này ở mức JSON (xương tiền tố n_ dưới xương evo co theo tỉ lệ chiều cao; slot ẩn mặc định) và clip `evolve` 2,8 s kết thúc đúng
khung 0 idle (+ aura giây 0) của dạng sau. Đặc tả: ArtGen/Spine/quai/DAC_TA_LO_THUY.md mục 5.

    py -3 -I ArtGen/Spine/tm10.py cat 2         cắt inbox/tm10_2/tai_ve/M01.png, M02.png -> inbox/tm10_2/manh/
    py -3 -I ArtGen/Spine/quai/khoa.py nang -- D:/spine-venv/Scripts/python -I ArtGen/Spine/tm10.py rig 2
                                                dựng inbox/tm10_2/rig/tm10_2.json|.atlas|.png|.atomik|_game.json, xem.html
Soi: hai_long_soi.py --rig=inbox/tm10_2/rig --name=tm10_2 sheet|can|luoi|lech. Mảnh chưa có thì hình giữ chỗ (dựng song song lúc chờ gen).
"""
import copy
import json
import math
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import hai_long as HL  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
BODY = {"head_k", "jaw_k", "mouth", "head_n", "jaw_n", "whisker", "lid_k", "lid_n", "tongue_k", "tongue_n", "neck_k", "neck_n", "coil", "tail"}
WATER = {k for k in HL.PIECES if k not in BODY and k not in HL.UNUSED}
NEXT_RIG = os.path.join(HERE, "inbox", "hai_long", "rig")   # dạng 3 bản 4 (đã xuất)

# ---------------------------------------------------------------- cấu hình từng dạng
FORMS = {
    2: dict(
        name="tm10_2", title="Hải Long Tam Thủ", inbox=os.path.join(HERE, "inbox", "tm10_2"),
        # đầu: id, loại cổ/đầu, cỡ, chỗ trồi x, hướng trồi, đầu lúc nghỉ (x, y, góc), biên độ đung đưa, pha. Thứ tự = thứ tự vẽ sau → trước
        heads=[   # so_concept.png: đầu rig hơi nhỏ và thấp so với concept -> nới cỡ, nâng hai đầu bên
            dict(id="a", kind="n", size=0.90, ex=-175, dirE=126, H=(-430, 560), psi=4, arr=74, sway=(30, 20, 5), ph=0.38),
            dict(id="d", kind="n", size=0.90, ex=195, dirE=78, H=(380, 385), psi=-16, arr=40, sway=(28, 16, 6), ph=0.72),
            dict(id="k", kind="k", size=1.02, ex=0, dirE=80, H=(-40, 690), psi=-4, arr=64, sway=(24, 18, 4), ph=0.0),
        ],
        n_front=1,                 # số đầu cuối danh sách vẽ TRƯỚC lớp nước giữa (hai_long: HEADS[:2] sau, HEADS[2:] trước)
        # vòng 2 (Claude điều phối soi): nước VỪA, thấy rõ vòng thân trái và đuôi phải -> 11 cuộn nhỏ, tránh chỗ vòng thân (x≈-125) và đuôi (x≈305)
        water_x=0.5, water_s=0.5,
        waves_keep=[0, 2, 4, 5, 8, 9, 10, 11, 15, 16, 21],
        wide=0.5,                  # mảng nền, dải nước co ngang
        coil_x=-400, tail_x=430, dens=1.5,   # cao ~730 so với dạng 3 cao 1100: lưới dày gấp 1,5 (bước ~17 đơn vị ≈ 2,3% chiều cao)
        tgt=(1150.0, 380.0),
        geo=dict(WHISK_ROT={"b": -20.0, "f": 5.0}, WHISK_SC={"b": 0.42, "f": 0.5}, WREST=9.0, BREATHE=(1.5, 1.5),
                 JAW_CLOSE={"k": 9.0, "n": 9.0}),   # râu ngắn chĩa ra trước cong nhẹ như concept; idle chỉ hé miệng
        next_json=os.path.join(NEXT_RIG, "hai_long.json"), next_name="hai_long",
    ),
    # dạng 1: rồng biển con MỘT đầu, chibi; "cổ to" = cả thân (tờ M02 dạng 1: thân duỗi thẳng 1300 × 230), không vòng thân; nước ít.
    1: dict(
        name="tm10_1", title="Hải Long Nhi", inbox=os.path.join(HERE, "inbox", "tm10_1"),
        # so_concept lần 1: nước quá rộng (rộng/cao 1,37 so với 0,80), đầu nhỏ so với thân -> 6 cuộn sóng sát thân, đầu phóng 1,45
        heads=[dict(id="k", kind="k", size=0.80, ex=-70, dirE=100, H=(50, 400), psi=-8, arr=76, sway=(22, 16, 4), ph=0.0, head_scale=1.45)],
        # vòng 2: vũng nước NHỎ như concept: 3 cuộn thấp sát gốc thân, bỏ mảng nền / dải sau / dải gợn
        n_front=1, water_x=0.3, water_s=0.4,
        waves_keep=[12, 16, 20], wide=0.25, no_water_parts=("mound", "band2", "ripple"),
        coil_x=-9999, tail_x=250, no_coil=True, skip={"neck_n", "head_n", "jaw_n", "lid_n", "tongue_n"}, dens=1.45,
        tgt=(1150.0, 300.0),
        # hình học đầu chibi (tỉ lệ ảnh đầu 430 × 320, đọc trên tờ M01): gáy ở dưới trái sau bờm, bản lề hàm dưới má, râu cụt ở mõm
        geo=dict(ANCHOR={"head_k": (0.42, 0.80), "jaw_k": (0.10, 0.30)},
                 HEAD_GEO={"jaw": (0.13, 0.012), "mouth": (0.30, -0.06), "wh_f": (0.52, 0.12), "wh_b": (0.49, 0.10)},
                 MANE={"k": (0.30, 0.42, 0.12)}, MUZZLE=(0.46, 0.03), NECK_THICK={"k": 1.0},
                 WHISK_ROT={"b": -15.0, "f": 8.0}, WHISK_SC={"b": 0.3, "f": 0.36}, WREST=10.0, BREATHE=(1.5, 1.5),
                 JAW_SC_K={"k": 0.55}, JAW_CLOSE={"k": 12.0}),   # hàm chibi nhỏ, khép thêm 12° lúc nghỉ (dò hàm yếu thì giữ 0,55)
        next_json=os.path.join(HERE, "inbox", "tm10_2", "rig", "tm10_2.json"), next_name="tm10_2",
    ),
}


def cfg(k):
    return FORMS[k]


# ---------------------------------------------------------------- 1. cắt mảnh
def assign2(sc, comps, w, h, k=2):
    """tờ của dạng 2: M01 lưới 4 × 3 (đầu k, hàm k, lòng miệng, mí k / đầu n, hàm n, lưỡi k, mí n / râu, lưỡi n, trống, trống);
    M02 như tờ M02 của dạng 3. Dạng 1: M01 lưới 3 × 2 (đầu, hàm, lòng miệng / mí, lưỡi, râu cụt), M02 hai hàng (thân, chóp đuôi)."""
    cx = lambda c: (c[0] + c[2]) / 2
    cy = lambda c: (c[1] + c[3]) / 2
    area = lambda c: int(c[4].sum())
    if sc == "M02":
        if k == 1:
            rows = sorted(comps, key=area, reverse=True)[:2]
            rows.sort(key=cy)
            return {"neck_k": rows[0], "tail": rows[1]} if len(rows) == 2 else {}
        return HL.assign("M02", comps, w, h)
    if k == 1:
        grid = [["head_k", "jaw_k", "mouth"], ["lid_k", "tongue_k", "whisker"]]
        ncol, nrow = 3, 2
    else:
        grid = [["head_k", "jaw_k", "mouth", "lid_k"], ["head_n", "jaw_n", "tongue_k", "lid_n"], ["whisker", "tongue_n", None, None]]
        ncol, nrow = 4, 3
    names = {}
    for c in comps:
        col, row = min(ncol - 1, int(cx(c) / (w / ncol))), min(nrow - 1, int(cy(c) / (h / nrow)))
        nm = grid[row][col]
        if nm is None:
            continue
        if nm not in names or area(c) > area(names[nm]):
            names[nm] = c
    return names


def cat(k):
    C = cfg(k)
    tai, manh = os.path.join(C["inbox"], "tai_ve"), os.path.join(C["inbox"], "manh")
    os.makedirs(manh, exist_ok=True)
    import glob
    from PIL import ImageDraw
    import cv2
    for sc in ("M01", "M02"):
        fs = sorted(glob.glob(os.path.join(tai, sc + "*.png")), key=os.path.getmtime)
        if not fs:
            print(sc, ": chưa có ảnh")
            continue
        p = fs[-1]
        comps, rgba = HL.components(p)
        h, w = rgba.shape[:2]
        names = assign2(sc, comps, w, h, k)
        want = [n for n in BODY if (n in ("neck_k", "neck_n", "coil", "tail")) == (sc == "M02") and n not in C.get("skip", ()) and not (n == "coil" and C.get("no_coil"))]
        print(sc, os.path.basename(p), f"{len(comps)} mảnh rời ->", ", ".join(f"{n} {names[n][2] - names[n][0]}x{names[n][3] - names[n][1]}" for n in want if n in names),
              "| THIẾU: " + ", ".join(n for n in want if n not in names) if any(n not in names for n in want) else "")
        for nm, c in names.items():
            x0, y0, x1, y1, m = c
            pad = 4
            x0, y0, x1, y1 = max(0, x0 - pad), max(0, y0 - pad), min(w, x1 + pad), min(h, y1 + pad)
            im = rgba[y0:y1, x0:x1].copy()
            keep = cv2.dilate(m[y0:y1, x0:x1].astype(np.uint8), np.ones((5, 5), np.uint8))
            im[..., 3] = (im[..., 3] * keep).astype(np.uint8)
            Image.fromarray(im, "RGBA").save(os.path.join(manh, nm + ".png"))
    ims = [(n, Image.open(os.path.join(manh, n + ".png"))) for n in sorted(BODY) if os.path.exists(os.path.join(manh, n + ".png"))]
    if ims:
        W_ = 1800
        x = y = 10
        row = 0
        sheet = Image.new("RGB", (W_, 1800), (120, 124, 132))
        d = ImageDraw.Draw(sheet)
        for n, im in ims:
            im = im.copy()
            im.thumbnail((560, 300))
            if x + im.width + 10 > W_:
                x, y, row = 10, y + row + 26, 0
            sheet.paste(im, (x, y + 16), im)
            d.text((x, y), n, fill=(255, 255, 255))
            x += im.width + 14
            row = max(row, im.height + 16)
        sheet.crop((0, 0, W_, y + row + 20)).save(os.path.join(manh, "_soi.png"))
        print(os.path.join(manh, "_soi.png"))


# ---------------------------------------------------------------- 2. nạp mảnh (thân của dạng này, nước của dạng 3)
def load_pieces_form(k):
    C = cfg(k)
    out, fake = {}, []
    for nm in HL.PIECES:
        if nm in HL.UNUSED:
            continue
        d = os.path.join(C["inbox"], "manh") if nm in BODY else HL.MANH
        p = os.path.join(d, nm + ".png")
        if nm in C.get("skip", ()) or (nm == "coil" and C.get("no_coil")):
            im = Image.new("RGBA", (8, 8), (0, 0, 0, 0))   # mảnh dạng này không có: ảnh trong suốt tí hon (không tốn atlas)
        elif os.path.exists(p):
            im = Image.open(p).convert("RGBA")
        else:
            im = HL.placeholder(nm)
            fake.append(nm)
        im = im.crop(im.getbbox())
        s = HL.SC * HL.PSC.get(nm, 1.0)
        im = im.resize((max(2, round(im.width * s)), max(2, round(im.height * s))), Image.LANCZOS)
        out[nm] = HL.bleed(im)
    if fake:
        print("mảnh giữ chỗ:", ", ".join(fake))
    return out


# ---------------------------------------------------------------- 3. vá hai_long cho dạng k rồi dựng
def patch(k):
    C = cfg(k)
    HL.HEADS = C["heads"]
    kp = os.path.join(C["inbox"], "rig", "khop.json")   # tm10_khop.py khop <k>: đầu khớp vào concept bằng dò tự động (DAC_TA mục 5)
    if os.path.exists(kp):
        KJ = json.load(open(kp, encoding="utf-8"))
        rh = KJ.get("rig_heads", {})
        for key in ("coil_x", "tail_x"):
            if key in KJ.get("extra", {}) and not (key == "coil_x" and C.get("no_coil")):
                C[key] = KJ["extra"][key]
                print(f"{key} theo concept: {C[key]}")
        for h in HL.HEADS:
            if h["id"] in rh:
                r = rh[h["id"]]
                h.update(size=r["size"], H=tuple(r["H"]), psi=r["psi"], ex=r["ex"], dirE=r["dirE"])
                for key in ("arr", "ka", "kb", "rest", "thick"):
                    if key in r:
                        h[key] = r[key]
                h.pop("head_scale", None)
        # hàm dưới dò theo concept: tỉ lệ và bản lề theo loại đầu; lòng miệng giữ lệch so với bản lề như dạng 3 (×tỉ lệ hàm)
        for kind, jw in KJ.get("jaws", {}).items():
            if jw.get("score", 0) < 0.15:
                print(f"hàm {kind}: dò yếu ({jw.get('score')}), giữ hằng")
                continue
            base = dict(HL.HEAD_GEO_K.get(kind, HL.HEAD_GEO))
            jx, jy = jw["jaw"]
            k_ = jw["sc"] / 0.86
            base["jaw"] = (jx, jy)
            base["mouth"] = (jx + 0.21 * k_, jy - 0.117 * k_)
            HL.HEAD_GEO_K[kind] = base
            HL.JAW_SC_K[kind] = jw["sc"]
            print(f"hàm {kind} theo concept: JAW_SC {jw['sc']}, bản lề {base['jaw']}")
        C["_parts"] = KJ.get("parts", {})
    # mật độ lưới theo CHIỀU CAO con (DAC_TA mục 5): dạng 3 bản 4 cao 1100 có bước ~26 đơn vị; dạng nhỏ hơn thì dày lên theo tỉ lệ
    dens = C.get("dens", 1.0)
    HL.STRIP_PER = max(3, int(round(3 * dens)))
    HL.STRIP_ROWS = max(7, int(round(7 * dens)))
    HL.HEAD_G = (int(round(14 * dens)), int(round(10 * dens)))
    HL.MOUTH_G = (int(round(7 * dens)), int(round(4 * dens)))
    HL.JAW_G = (int(round(9 * dens)), int(round(4 * dens)))
    HL.COIL_G = (int(round(13 * dens)), int(round(8 * dens)))
    HL.WAVE_G = 8
    print(f"mật độ lưới × {dens}: cột/đốt {HL.STRIP_PER}, đầu {HL.HEAD_G}, hàm {HL.JAW_G}, miệng {HL.MOUTH_G}, vòng thân {HL.COIL_G}")
    for h in HL.HEADS:
        print(f"đầu {h['id']}: size {h['size']}, H {h['H']}, psi {h['psi']}, ex {h['ex']}, dirE {h['dirE']}, arr {h['arr']}, ka {h.get('ka', 0.52)}, kb {h.get('kb', 0.42)}")
    W_ = []
    for i in C["waves_keep"]:
        w = dict(HL.WAVES[i])
        w["x"] = round(w["x"] * C["water_x"])
        w["s"] = round(w["s"] * C["water_s"], 3)
        W_.append(w)
    HL.WAVES = W_
    HL.TGT = C["tgt"]
    for nm, v in C.get("geo", {}).items():   # hình học đầu riêng của dạng (dict: cập nhật đè; bộ: thay)
        if isinstance(v, dict):
            getattr(HL, nm).update(v)
        else:
            setattr(HL, nm, v)
    HL.NAME = C["name"]
    HL.RIG = os.path.join(C["inbox"], "rig")
    HL.INBOX = C["inbox"]
    HL._LID.clear()


def build_rig_form(k, pc):
    C = cfg(k)
    # hai_long.build_rig vẽ HEADS[:2] sau lớp nước giữa, HEADS[2:] trước: với 3 đầu thì hai đầu bên sau, thủ lĩnh trước
    HL.HEADS = C["heads"]
    sk, info = HL.build_rig(pc)
    # co mảng nền, dải nước; dời vòng thân, đuôi
    for nm in ("mound", "band", "band2", "ripple"):
        b = sk.bones[sk.bi[nm]]
        b["scaleX"] = round(b.get("scaleX", 1.0) * C["wide"], 3)
        if nm == "mound" and C["wide"] < 0.6:
            b["scaleY"] = round(b.get("scaleY", 1.0) * (C["wide"] / 0.8), 3)
    # đầu phóng riêng (chibi: đầu to so với thân); lưới đầu, hàm, mí, râu là con của xương đầu nên phóng theo
    for h in C["heads"]:
        hs = h.get("head_scale", 1.0)
        if hs != 1.0:
            b = sk.bones[sk.bi["h" + h["id"]]]
            b["scaleX"] = round(b.get("scaleX", 1.0) * hs, 3)
            b["scaleY"] = round(b.get("scaleY", 1.0) * hs, 3)
    sk.bones[sk.bi["coil"]]["x"] = float(C["coil_x"])
    bt = sk.bones[sk.bi["tail"]]
    bt["x"] = round(bt["x"] + (C["tail_x"] - 500), 2)
    # vòng thân, đuôi đặt theo mảnh dò trên concept (vòng 2): vị trí, góc, tỉ lệ
    P_ = C.get("_parts", {})
    kh = json.load(open(os.path.join(C["inbox"], "rig", "khop.json"), encoding="utf-8")) if P_ else {}
    f_ = kh.get("f", 1.0)
    if "coil" in P_ and not C.get("no_coil"):
        p = P_["coil"]
        cim = pc["coil"]
        s_ = p["sc"] * f_ / (HL.SC * 0.82)                       # lưới vòng thân vẽ ở csc = 0,82 của px atlas
        offy = cim.height * 0.82 / 2 - 34                         # tâm ảnh so với gốc xương vòng thân (hệ xương, trước khi phóng)
        r = math.radians(p["ang"])
        b = sk.bones[sk.bi["coil"]]
        b["x"], b["y"] = round(p["X"] + math.sin(r) * offy * s_, 2), round(p["Y"] - math.cos(r) * offy * s_, 2)
        b["rotation"], b["scaleX"], b["scaleY"] = round(p["ang"], 2), round(s_, 3), round(s_, 3)
        print(f"vòng thân theo concept: ({b['x']}, {b['y']}) góc {p['ang']} tỉ lệ {s_:.2f}")
    if "tail" in P_:
        p = P_["tail"]
        tim = pc["tail"]
        s_ = p["sc"] * f_ / (HL.SC * 0.8)
        L_ = tim.width * 0.8                                      # dải đuôi từ gốc xương dọc trục x
        r = math.radians(p["ang"])
        b = sk.bones[sk.bi["tail"]]
        b["x"], b["y"] = round(p["X"] - math.cos(r) * L_ / 2 * s_, 2), round(p["Y"] - math.sin(r) * L_ / 2 * s_, 2)
        b["rotation"], b["scaleX"], b["scaleY"] = round(p["ang"], 2), round(s_, 3), round(s_, 3)
        print(f"đuôi theo concept: ({b['x']}, {b['y']}) góc {p['ang']} tỉ lệ {s_:.2f}")
    for nm in C.get("no_water_parts", ()):   # dạng 1: vũng nhỏ, không mảng nền / dải sau / dải gợn
        for s in sk.slots:
            if s["name"] == nm:
                s.pop("attachment", None)
    # concept dạng 2: chỉ thủ lĩnh có râu; đầu phụ bỏ hình râu (xương vẫn còn, khoá râu vô hại)
    no_whisker = {h["id"] for h in C["heads"] if h["kind"] == "n"}
    for s in sk.slots:
        if len(s["name"]) == 3 and s["name"][0] == "r" and s["name"][1] in no_whisker and s["name"][2] in "bf":
            s.pop("attachment", None)
        if C.get("no_coil") and s["name"] == "coil":
            s.pop("attachment", None)
    return sk, info


# ---------------------------------------------------------------- 4. clip riêng của dạng 2
def clip_attack_2(info):
    """ba đầu: đầu thấp bên phải (d) rụt về rồi phóng ra cắn ở 0,45 s; thủ lĩnh (k) bổ chéo xuống cắn ở 0,68 s; đầu trái (a) ngả ra sau
    lấy thăng bằng rồi chồm theo gầm."""
    D = HL.TW
    c = HL.Clip("attack", D, info)
    z = (0, 0, 0, 0)
    K = HL.K
    tr = {
        "d": K((0, z, "lin"), (0.30, (-150, 40, 16, 4), "io"), (0.38, (-160, 44, 18, 30), "lin"), (0.45, (330, -30, -4, 44), "in"), (0.50, (345, -34, -6, 0), "lin"),
               (0.62, (330, -28, -4, 0), "lin"), (1.05, (-20, 8, 2, 0), "io"), (D, z, "io")),
        "k": K((0, z, "lin"), (0.48, (-120, 70, 20, 6), "io"), (0.60, (-130, 76, 22, 34), "lin"), (0.68, (260, -170, -24, 46), "in"), (0.73, (272, -180, -26, 0), "lin"),
               (0.86, (260, -170, -24, 0), "lin"), (1.25, (-14, 10, 3, 0), "io"), (D, z, "io")),
        "a": K((0, z, "lin"), (0.45, (-70, 20, 12, 0), "io"), (0.78, (40, 12, -4, 16), "out"), (1.3, z, "io"), (D, z, "lin")),
    }
    WY = HL.WY
    c.fx += [(0.30, info["heads"]["d"]["E"][0] + 30, WY, 0.55, "toe_nho"), (0.47, info["heads"]["d"]["E"][0] + 120, WY, 0.8, "toe_nho"),
             (0.70, info["heads"]["k"]["E"][0] + 140, WY, 0.9, "toe")]
    c.events += [(0.45, "can", "d"), (0.68, "can", "k")]
    for hid, th_ in (("d", 0.45), ("k", 0.68)):
        c.raw("h" + hid, "scale", [(0, (1, 1)), (th_ - 0.07, (1, 1)), (th_, (1.15, 0.92)), (th_ + 0.07, (0.96, 1.04)), (th_ + 0.2, (1, 1)), (D, (1, 1))])
    HL.animate_heads(c, tr, sway=lambda t: 1 - HL.ease(t / 0.25, "io") * (1 - HL.ease((t - 1.1) / 0.5, "io")))
    HL.animate_water(c)
    HL.animate_fx(c)
    return c


def clip_attack_1(info):
    """dạng 1 (một đầu): rụt về lấy đà 0,3 s rồi vươn cả thân ra mổ một nhát ở 0,45 s, giữ có trôi, về."""
    D = HL.TW
    c = HL.Clip("attack", D, info)
    z = (0, 0, 0, 0)
    K = HL.K
    tr = {"k": K((0, z, "lin"), (0.28, (-120, 30, 14, 4), "io"), (0.37, (-130, 34, 16, 30), "lin"), (0.45, (250, -70, -12, 44), "in"),
                 (0.50, (262, -76, -14, 0), "lin"), (0.64, (250, -70, -12, 0), "lin"), (1.1, (-16, 6, 2, 0), "io"), (D, z, "io"))}
    WY = HL.WY
    c.fx += [(0.28, info["heads"]["k"]["E"][0] - 20, WY, 0.5, "toe_nho"), (0.47, info["heads"]["k"]["E"][0] + 110, WY, 0.8, "toe")]
    c.events += [(0.45, "can", "k")]
    c.raw("hk", "scale", [(0, (1, 1)), (0.38, (1, 1)), (0.45, (1.15, 0.92)), (0.52, (0.96, 1.04)), (0.65, (1, 1)), (D, (1, 1))])
    HL.animate_heads(c, tr, sway=lambda t: 1 - HL.ease(t / 0.25, "io") * (1 - HL.ease((t - 1.1) / 0.5, "io")))
    HL.animate_water(c)
    HL.animate_fx(c)
    return c


# ---------------------------------------------------------------- 5. gộp rig dạng sau (JSON) và clip evolve
def pose0(J, clips=("idle", "aura")):
    """dáng của dạng sau ở giây 0 của idle + aura: {xương: {rotate: v, translate: (x, y), scale: (x, y)}}, {slot: alpha}."""
    bones, slots = {}, {}
    for cn in clips:
        A = J["animations"].get(cn, {})
        for b, tl in A.get("bones", {}).items():
            e = bones.setdefault(b, {"rotate": 0.0, "translate": [0.0, 0.0], "scale": [1.0, 1.0]})
            for kind, ks in tl.items():
                k0 = ks[0]
                if k0.get("time", 0.0) > 1e-6:
                    continue
                if kind == "rotate":
                    e["rotate"] += k0["value"]
                elif kind == "translate":
                    e["translate"][0] += k0["x"]
                    e["translate"][1] += k0["y"]
                else:
                    e["scale"][0] *= k0["x"]
                    e["scale"][1] *= k0["y"]
        for s, tl in A.get("slots", {}).items():
            ks = tl["alpha"]
            if ks and ks[0].get("time", 0.0) <= 1e-6:
                slots[s] = slots.get(s, 1.0) * ks[0]["value"]
    return bones, slots


def merge_next(sk, pc, k, info):
    """thêm dạng sau vào sk (tiền tố n_, dưới xương evo co theo tỉ lệ chiều cao). Trả (tiB, dáng giây 0 của dạng sau)."""
    C = cfg(k)
    J = json.load(open(C["next_json"], encoding="utf-8"))
    # mảnh của dạng sau: nước dùng chung (cùng ảnh atlas), thân thêm tiền tố
    HL_RIG_SAVE = (HL.MANH,)
    pc3 = HL.load_pieces()   # đọc từ inbox/hai_long/manh (hằng MANH của hai_long không bị vá)
    for nm, im in pc3.items():
        if nm in BODY:
            pc["n_" + nm] = im
            if nm.startswith("neck_"):   # dải cổ cắt 55 % phía chân (tm10_lai.apply_lai) của dạng sau
                pc["n_" + nm + "_c"] = im.crop((0, 0, int(im.width * 0.55), im.height))
    # mảnh cắt từ concept (cách lai) của dạng sau: nạp từ manh_lai của dạng đó (cùng tỉ lệ f, bleed như apply_lai), tiền tố n_
    lai_dir = os.path.join(os.path.dirname(os.path.dirname(C["next_json"])), "manh_lai")
    if os.path.exists(os.path.join(lai_dir, "lai.json")):
        import tm10_lai
        for nm in tm10_lai.pieces_of(lai_dir):
            pc["n_" + nm] = tm10_lai.load_piece(lai_dir, nm)
    hA = height_of(info)
    hB = J.get("_height") or 1099.5
    g3 = os.path.join(os.path.dirname(C["next_json"]), C["next_name"] + "_game.json")
    if os.path.exists(g3):
        hB = json.load(open(g3, encoding="utf-8")).get("height", hB)
    tiB = round(hA / hB, 4)
    sk.bone("evo", "root", 0, 0, 0, 0, tiB, tiB)
    # rig dạng sau có thể đã gộp dạng sau nữa (tm10_2 chứa n_* của dạng 3): chỉ lấy phần riêng của nó
    J["bones"] = [b for b in J["bones"] if not b["name"].startswith("n_") and b["name"] != "evo"]
    J["slots"] = [s for s in J["slots"] if not s["name"].startswith("n_")]
    J_bones = J["bones"]
    for b in J_bones:
        if b["name"] == "root":
            continue
        nb = dict(b)
        nb["name"] = "n_" + b["name"]
        nb["parent"] = "evo" if b.get("parent") == "root" else "n_" + b["parent"]
        sk.bi[nb["name"]] = len(sk.bones)
        sk.bones.append(nb)
    old_names = [b["name"] for b in J_bones]
    nb_of = lambda nm: "evo" if nm == "root" else "n_" + nm
    atts3 = next(s for s in J["skins"] if s["name"] == "default")["attachments"]
    for s in J["slots"]:
        ns = {"name": "n_" + s["name"], "bone": nb_of(s["bone"]), "color": "ffffff00"}
        if "attachment" in s:
            ns["attachment"] = "n_" + s["attachment"]
        sk.slots.append(ns)
        for an, a in atts3.get(s["name"], {}).items():
            a2 = copy.deepcopy(a)
            if "path" in a2 and (a2["path"] in BODY or a2["path"].startswith("lai_") or (a2["path"].startswith("neck_") and a2["path"].endswith("_c"))):
                a2["path"] = "n_" + a2["path"]
            if a2.get("type") == "clipping":
                a2["end"] = "n_" + a2["end"]
            if a2.get("type") == "mesh":
                v, out, i = a2["vertices"], [], 0
                nv = len(a2["uvs"]) // 2
                for _ in range(nv):
                    n = int(v[i]); i += 1
                    out.append(n)
                    for _ in range(n):
                        bi = int(v[i])
                        out += [sk.bi[nb_of(old_names[bi])], v[i + 1], v[i + 2], v[i + 3]]
                        i += 4
                a2["vertices"] = out
            sk.atts.setdefault(ns["name"], {})["n_" + an] = a2
    b0, s0 = pose0(J)
    vis = {}   # độ đậm mặc định của slot dạng sau khi nó hiện (idle + aura giây 0)
    for s in J["slots"]:
        base = int(s["color"][6:8], 16) / 255.0 if "color" in s else 1.0
        vis["n_" + s["name"]] = base * s0.get(s["name"], 1.0)
    return tiB, b0, vis, hB


def height_of(info):
    hk = info["heads"]["k"]
    hs = next((h.get("head_scale", 1.0) for h in HL.HEADS if h["id"] == "k"), 1.0)
    return round(hk["H"][1] + info["pieces"]["head_k"].height * 0.75 * hk["size"] * hs + 60.0, 2)


def clip_evolve(info, b0, vis, sk):
    """2,8 s: ba đầu ngửa gồng (0–1,0 s), nước dâng; 1,05–1,35 s dạng này tan (lốc là VFX của game, sự kiện doi_dang); 1,12–1,45 s dạng
    sau hiện lớn dần (evo 0,86 → 1,05 → 1); 1,55–2,4 s năm đầu gầm (hàm há, đầu ngửa nhẹ); 0,35 s cuối về đúng khung 0 idle dạng sau."""
    D = 2.8
    c = HL.Clip("evolve", D, info)
    z = (0, 0, 0, 0)
    K = HL.K
    tr = {}
    for h in HL.HEADS:
        hid = h["id"]
        back = {"k": (-60, 50, 24, 30), "a": (-50, 30, 22, 26), "d": (-70, 24, 26, 26)}.get(hid, (-50, 30, 22, 26))
        tr[hid] = K((0, z, "lin"), (0.35, (back[0] * 0.4, back[1] * 0.4, back[2] * 0.4, 6), "io"), (0.95, back, "io"), (1.05, (back[0] - 10, back[1] + 10, back[2] + 4, 40), "out"),
                    (1.35, (back[0] - 10, back[1] + 10, back[2] + 4, 40), "lin"), (D, (back[0] - 10, back[1] + 10, back[2] + 4, 40), "lin"))
    c.events += [(0.1, "tu_luc", ""), (1.2, "doi_dang", ""), (1.55, "gam", ""), (2.4, "het_gam", "")]
    WY = HL.WY
    c.fx += [(0.9, 0, WY - 30, 1.3, "vong"), (1.08, -80, WY, 1.2, "toe"), (1.14, 120, WY, 1.2, "toe"), (1.2, 0, WY - 30, 1.6, "vong")]
    HL.lids(c, {h["id"]: [(1.0, D)] for h in HL.HEADS})
    HL.animate_heads(c, tr, sway=lambda t: 1 - HL.ease(t / 0.5, "io"))
    HL.animate_water(c, grow=lambda t: 1 + 0.18 * HL.ease(t / 1.0, "io") * (1 - HL.ease((t - 1.3) / 0.25, "io")),
                     calm=lambda t: 1 - 0.5 * HL.ease((t - 0.3) / 0.7, "io"))
    HL.animate_fx(c)
    # dạng này tan 1,05 → 1,35 s (mọi slot của dạng này, kể cả sóng: runtime nhân với aura)
    own = [s["name"] for s in sk.slots if not s["name"].startswith("n_") and s["name"] not in ("cat",) and not s["name"].startswith(("cr", "dr", "rg"))]
    hids = {h["id"] for h in HL.HEADS}
    for s in own:
        if s[0] == "l" and s[1:] in hids:        # lưỡi: chỉ thò ở die (dây mềm); gồng evolve thì nấp trong miệng (lỗi que thẳng đã gặp)
            c.alpha(s, [(0.0, 0.0), (D, 0.0)])
        elif s[0] == "e" and s[1:] in hids:      # mí: theo lịch nhắm 1,0 s → tan cùng dạng này (không đè lịch lids bằng 1,0 từ giây 0)
            c.alpha(s, [(0.0, 0.0), (0.97, 0.0), (1.0, 1.0), (1.05, 1.0), (1.35, 0.0), (D, 0.0)])
        else:
            c.alpha(s, [(0.0, 1.0), (1.05, 1.0), (1.35, 0.0), (D, 0.0)])
    # dạng sau: đứng ở dáng giây 0 idle + aura; hiện 1,12 → 1,45; evo 0,86 → 1,05 → 1
    for b, e in b0.items():
        nb = "n_" + b
        if nb not in sk.bi:
            continue
        if abs(e["rotate"]) > 0.02:
            c.raw(nb, "rotate", [(0, e["rotate"]), (D, e["rotate"])])
        if abs(e["translate"][0]) > 0.02 or abs(e["translate"][1]) > 0.02:
            c.raw(nb, "translate", [(0, tuple(e["translate"])), (D, tuple(e["translate"]))])
        if abs(e["scale"][0] - 1) > 0.002 or abs(e["scale"][1] - 1) > 0.002:
            c.raw(nb, "scale", [(0, tuple(e["scale"])), (D, tuple(e["scale"]))])
    for s, a in vis.items():
        if a > 0.001:
            c.alpha(s, [(0.0, 0.0), (1.12, 0.0), (1.45, a), (D, a)])
    c.raw("evo", "scale", [(0, (0.86, 0.86)), (1.12, (0.86, 0.86)), (1.45, (1.05, 1.05)), (1.7, (1.0, 1.0)), (D, (1.0, 1.0))])
    # gầm: hàm há, đầu ngửa nhẹ, rung hai dáng, về 0 trước 2,45 s (cộng thêm vào dáng giây 0)
    jaws = [b for b in sk.bi if b.startswith("n_j") and len(b) == 4]
    heads = [b for b in sk.bi if b.startswith("n_h") and len(b) == 4]
    for i, nb in enumerate(sorted(jaws)):
        dl = 0.04 * i
        ks = [(0, 0.0), (1.45, 0.0), (1.55 + dl, -40.0)]
        t = 1.6 + dl
        while t < 2.3:
            ks.append((t, -40.0 + (3.0 if int(t * 15) % 2 == 0 else -3.0)))
            t += 2.0 / HL.FPS
        ks += [(2.4, -36.0), (2.62, 0.0), (D, 0.0)]
        c.raw(nb, "rotate", [(t_, v + b0.get(nb[2:], {"rotate": 0.0})["rotate"]) for t_, v in ks])
    for i, nb in enumerate(sorted(heads)):
        dl = 0.04 * i
        base = b0.get(nb[2:], {"rotate": 0.0})["rotate"]
        c.raw(nb, "rotate", [(0, base), (1.45, base), (1.58 + dl, base + 9.0), (2.35, base + 7.0), (2.6, base), (D, base)])
    return c


# ---------------------------------------------------------------- 6. dựng
def rig(k):
    C = cfg(k)
    patch(k)
    os.makedirs(HL.RIG, exist_ok=True)
    pc = load_pieces_form(k)
    sk, info = build_rig_form(k, pc)
    # cách lai (2026-11-11): mảnh cắt thẳng từ concept thay mảnh GPT phần trên mặt nước (tm10_lai.py cat <k> trước)
    lai_meta = None
    if os.path.exists(os.path.join(C["inbox"], "manh_lai", "lai.json")):
        import tm10_lai
        lai_meta = tm10_lai.apply_lai(sk, pc, info, k, C)
        HL.JAW_CLOSE = {kind: 1.5 for kind in ("k", "n")}   # hàm concept đã hé sẵn: idle chỉ khép thêm chút
        HL.BREATHE = (1.0, 1.0)
    atk = clip_attack_1 if k == 1 else clip_attack_2
    clips = [HL.clip_idle(info), HL.clip_xuat_hien(info), atk(info), HL.clip_chieu_phun(info), HL.clip_chieu(info),
             HL.clip_trung_don(info), HL.clip_chet(info), HL.clip_aura(info)]
    tiB, b0, vis, hB = merge_next(sk, pc, k, info)
    clips.append(clip_evolve(info, b0, vis, sk))
    # bỏ khoá của xương / slot không có (hàm clip của hai_long viết cho 5 đầu)
    slot_names = {s["name"] for s in sk.slots}
    for c in clips:
        c.bones = {b: v for b, v in c.bones.items() if b in sk.bi}
        c.slots = {s: v for s, v in c.slots.items() if s in slot_names}
    HL.EVENTS.update({"tu_luc": "bắt đầu tụ lực tiến hóa", "doi_dang": "lốc đậm nhất, đổi dạng"})
    HL.LABELS["evolve"] = "8 Tiến hóa"
    used = {a.get("path", an) for atts in sk.atts.values() for an, a in atts.items() if a.get("type", "region") in ("region", "mesh")}
    pc_atlas = {n: im for n, im in pc.items() if n in used}     # atlas chỉ chứa mảnh còn dùng (mảnh GPT bị mảnh concept thay thì bỏ)
    stat = HL.export(sk, clips, pc_atlas)
    HL.viewer([c for c in clips], stat)
    xem = os.path.join(HL.RIG, "xem.html")
    t = open(xem, encoding="utf-8").read().replace("Hải Long Ngũ Đầu", C["title"])
    open(xem, "w", encoding="utf-8").write(t)
    g = HL.game_info(info, clips)
    g["height"] = height_of(info) if lai_meta is None else round(lai_meta["height_rig"] + 60.0, 2)
    g["_evolve"] = {"tiB": tiB, "height_next": hB, "next": C["next_name"]}
    HL.to_atomik(g)
    print(f"dạng {k}: chiều cao {g['height']} / dạng sau {hB} -> evo {tiB}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "rig"
    k = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    if cmd == "cat":
        cat(k)
    else:
        rig(k)
