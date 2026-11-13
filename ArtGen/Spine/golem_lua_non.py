# -*- coding: utf-8 -*-
"""Golem lõi lửa DẠNG 1 ("Nham Con", mã làm việc golem_lua_non): dạng non của golem lõi lửa đã duyệt (golem_lua_1 = dạng 2 trong game,
suất `nham_than` đảo Hỏa). Cùng rig, cùng clip với dạng 2 (golem_lua_rig.py, biến môi trường GL_NON=1).

Người dùng (2026-11-13): "làm dạng 1 và vfx riêng đi"; chọn hướng A "mồi lửa" (ba ngọn lửa nhỏ, bốn lỗ còn lại tắt, vuốt cụt).

"Tỉ lệ trước, concept sau" (như Hỏa Nhãn dạng 2): hình bố cục = mảnh dạng 2 đã cắt (inbox/golem_lua_1/manh, toạ độ khung concept
1536 × 1024) xếp lại ở tỉ lệ dạng non: lửa ngắn lại quanh gốc lửa, bàn tay + vuốt nhỏ lại quanh chỗ chạm đất, đầu / mắt to ra quanh tâm;
lỗ lửa "tắt" hiện mảnh nguội (`_nguoi`) và bỏ lưỡi lửa.

Mảnh dạng 1 (`manh`): các tấm đá DÙNG LẠI mảnh dạng 2 (cùng thiết kế, đã kiểm ở mọi clip); chỉ thay thứ khác dạng 2 bằng hình vẽ mới từ tờ
`tai_ve/M_1.png` (build_golem_lua_non.py manh): ba ngọn lửa nhỏ, sáu vuốt cụt, lõi lửa dịu. Bàn tay ×0,86 quanh chỗ chạm đất, mắt ×1,15;
bốn lỗ tắt: mảnh nguội nướng thẳng vào tấm của nó, bỏ bốn lưỡi lửa nhỏ.

    golem_lua_non.py bo_cuc     → inbox/golem_lua_non/mau/bo_cuc_<hướng>.png + bo_cuc.json
    golem_lua_non.py manh       → inbox/golem_lua_non/manh/<tên>.png + dat.json + _so_ghep.png
"""
import json
import os
import shutil
import sys

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
MANH2 = os.path.join(HERE, "inbox", "golem_lua_1", "manh")
BASE = os.path.join(HERE, "inbox", "golem_lua_non")
MAU = os.path.join(BASE, "mau")
TAI = os.path.join(BASE, "tai_ve")
MANH = os.path.join(BASE, "manh")
W, H = 1536, 1024

LUA_LON = ("lua_vai", "lua_dinh", "lua_tran")
LUA_NHO = ("lua_dinh_nho", "lua_sau_dau", "lua_co_tay", "lua_hong")
NGUOI_CUA = {"lua_dinh_nho": "dinh_nguoi", "lua_sau_dau": "dau_nguoi", "lua_co_tay": "co_tay_gan_nguoi", "lua_hong": "hong_nguoi"}
TAY = {"gan": ("tay_gan", "vuot_gan1", "vuot_gan2", "vuot_gan3"), "xa": ("tay_xa", "vuot_xa1", "vuot_xa2", "vuot_xa3")}
DAU = ("dau", "dau_nguoi", "dau_vanh", "mat", "vong_tran_sau", "vong_tran_nguoi", "vong_tran_truoc", "lua_tran", "lua_sau_dau", "ham",
       "hong_lua")
VAI = ("vai", "vai_nguoi", "vong_vai_sau", "vong_vai_truoc", "lua_vai")

# hướng → tỉ lệ. lua: lưỡi lớn; lua_nho: None = tắt (hiện mảnh nguội), số = còn cháy ở tỉ lệ đó
HUONG = {
    "moi_lua": dict(lua=0.55, lua_nho=None, tay=0.86, vuot=0.72, dau=1.0, mat=1.15, vai=1.0),
    "cuoi_tron": dict(lua=0.5, lua_nho=None, tay=0.80, vuot=0.65, dau=1.16, mat=1.3, vai=0.92),
    "du_lua": dict(lua=0.55, lua_nho=0.6, tay=0.86, vuot=0.72, dau=1.0, mat=1.15, vai=1.0),
}
CHON = "moi_lua"
K_LUA = 0.72        # ba ngọn lửa của tờ M_1 thu quanh gốc cho bằng lửa trong concept
K_VUOT = 0.74       # vuốt: phần chiều cao ô vuốt bố cục
K_CHOM = 0.45       # phần trên của vuốt chờm lên bàn tay
BO_THEM = {"hong_vanh"}   # nửa trước cổ lỗ hông: không còn lửa, chỉ lộ một vệt cong tối dưới khối ngực


def doc():
    dat = json.load(open(os.path.join(MANH2, "dat.json"), encoding="utf-8"))
    return dat, dat["_thu_tu"]


def hop(dat, ten):
    b = None
    for t in ten:
        x, y = dat[t]["goc"]
        w, h = dat[t]["co"]
        r = (x, y, x + w, y + h)
        b = r if b is None else (min(b[0], r[0]), min(b[1], r[1]), max(b[2], r[2]), max(b[3], r[3]))
    return b


def bien_doi(dat, thu_tu, k):
    """phép xếp lại của một hướng: trả (ap(điểm, tên mảnh) → điểm mới, mảnh bỏ, mảnh nguội hiện)."""
    bien = {t: [] for t in thu_tu}                # tên → [(tỉ lệ, tâm)]

    def them(ten, s, tam):
        for t in ten:
            if t in bien and abs(s - 1) > 1e-6:
                bien[t].append((s, tam))

    b = hop(dat, ["dau"])
    them(DAU, k["dau"], ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2))
    b = hop(dat, ["vai"])
    them(VAI, k["vai"], ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2))
    b = hop(dat, ["mat"])
    them(["mat", "mat_tat"], k["mat"], ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2))
    for ben, ten in TAY.items():
        b = hop(dat, ten)
        them(ten, k["tay"], ((b[0] + b[2]) / 2, b[3]))          # quanh chỗ chạm đất
        for v in ten[1:]:
            bv = hop(dat, [v])
            them([v], k["vuot"] / k["tay"], ((bv[0] + bv[2]) / 2, bv[1] + 0.25 * (bv[3] - bv[1])))   # vuốt cụt: co về phía gốc vuốt
    bo, hien_nguoi = set(), set()
    for t in LUA_LON:
        them([t], k["lua"], tuple(dat[t]["goc_lua"]))
    for t in LUA_NHO:
        if k["lua_nho"] is None:
            bo.add(t)
            hien_nguoi.add(NGUOI_CUA[t])
        else:
            them([t], k["lua_nho"], tuple(dat[t]["goc_lua"]))

    def ap(p, t):
        x, y = p
        for s, (cx, cy) in bien.get(t, ()):
            x, y = cx + (x - cx) * s, cy + (y - cy) * s
        return x, y

    return ap, bo, hien_nguoi


def o_moi(dat, ap, t):
    x0, y0 = ap(dat[t]["goc"], t)
    x1, y1 = ap((dat[t]["goc"][0] + dat[t]["co"][0], dat[t]["goc"][1] + dat[t]["co"][1]), t)
    return x0, y0, x1, y1


def bo_cuc(kieu):
    dat, thu_tu = doc()
    k = HUONG[kieu]
    ap, bo, hien_nguoi = bien_doi(dat, thu_tu, k)
    im = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    khung = None
    lua = {}
    for t in thu_tu:
        if t in bo or t in ("loi_tat", "mat_tat"):
            continue
        if t.endswith("_nguoi") and t not in hien_nguoi:
            continue
        a = Image.open(os.path.join(MANH2, t + ".png")).convert("RGBA")
        x0, y0, x1, y1 = o_moi(dat, ap, t)
        w, h = max(1, round(x1 - x0)), max(1, round(y1 - y0))
        if (w, h) != a.size:
            a = a.resize((w, h), Image.LANCZOS)
        im.alpha_composite(a, (round(x0), round(y0)))
        bb = a.getbbox()
        if bb:
            r = (round(x0) + bb[0], round(y0) + bb[1], round(x0) + bb[2], round(y0) + bb[3])
            khung = r if khung is None else (min(khung[0], r[0]), min(khung[1], r[1]), max(khung[2], r[2]), max(khung[3], r[3]))
            if t.startswith("lua_"):
                g = ap(dat[t]["goc_lua"], t)
                lua[t] = {"goc": [round(g[0]), round(g[1])], "hop": list(r)}
    os.makedirs(MAU, exist_ok=True)
    p = os.path.join(MAU, f"bo_cuc_{kieu}.png")
    im.convert("RGB").save(p)
    print(p, "khung", khung, "lửa", sorted(lua))
    return {"khung": list(khung), "lua": lua, "ti_le": k}


# ---------------------------------------------------------------- mảnh dạng 1
def manh(dich_vuot=None):
    import cv2
    import numpy as np
    sys.path.insert(0, HERE)
    import mat_lua_manh as ML
    from golem_lua_manh import LOI_TAT
    from build_golem_lua_non import LUA_NON, VUOT_NON, LOI_TAM

    dat, thu_tu = doc()
    ap, bo, hien_nguoi = bien_doi(dat, thu_tu, HUONG[CHON])
    if os.path.isdir(MANH):
        shutil.rmtree(MANH)
    os.makedirs(MANH)
    ra, anh_ = {}, {}

    def luu(t, im, goc, goc_cu=None):
        d = dict(dat[t]) if t in dat else dict(slot=None)
        d["goc"] = [int(round(goc[0])), int(round(goc[1]))]
        d["co"] = [im.width, im.height]
        ra[t] = d
        anh_[t] = im
        im.save(os.path.join(MANH, t + ".png"))

    # 1. mảnh dạng 2 dùng lại (xếp lại theo tỉ lệ dạng non); bỏ bốn lưỡi lửa nhỏ; lỗ tắt: nướng mảnh nguội vào tấm
    nuong = {v[:-len("_nguoi")]: v for v in hien_nguoi}
    for t in thu_tu:
        if t in bo or t in BO_THEM:
            continue
        a = Image.open(os.path.join(MANH2, t + ".png")).convert("RGBA")
        if t in nuong:
            n = Image.open(os.path.join(MANH2, nuong[t] + ".png")).convert("RGBA")
            a.alpha_composite(n, (dat[nuong[t]]["goc"][0] - dat[t]["goc"][0], dat[nuong[t]]["goc"][1] - dat[t]["goc"][1]))
        x0, y0, x1, y1 = o_moi(dat, ap, t)
        w, h = max(1, round(x1 - x0)), max(1, round(y1 - y0))
        if (w, h) != a.size:
            a = a.resize((w, h), Image.LANCZOS)
        luu(t, a, (x0, y0))

    # 2. tờ M_1: ba ngọn lửa nhỏ, sáu vuốt cụt, lõi dịu
    A = ML.doc(os.path.join(TAI, "M_1.png"))
    if A.shape[:2] != (H, W):
        raise SystemExit(f"tờ M_1: cỡ {A.shape[1]}x{A.shape[0]}, phải {W}x{H}")
    fg = ~ML.nen(A)
    fg = cv2.morphologyEx(fg.astype(np.uint8), cv2.MORPH_OPEN, ML.el(1)).astype(bool)
    n, lab, st, cen = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
    cum = [i for i in range(1, n) if st[i, 4] >= 250]
    loi_i = min(cum, key=lambda i: (cen[i][0] - LOI_TAM[0]) ** 2 + (cen[i][1] - LOI_TAM[1]) ** 2)
    lua_i = {}
    for ten, (gx, gy), w_, tip, ww, _ in LUA_NON:
        ung = [i for i in cum if i != loi_i and i not in lua_i.values() and cen[i][1] < 620]
        lua_i[ten] = min(ung, key=lambda i: min(np.hypot(*(np.argwhere(lab == i)[:, ::-1] - (gx, gy)).T)))
    vuot_i = sorted([i for i in cum if i != loi_i and i not in lua_i.values() and cen[i][1] > 650], key=lambda i: cen[i][0])
    print(f"  tờ M_1: {len(cum)} cụm; lửa {len(lua_i)}, vuốt {len(vuot_i)}, lõi 1")
    if len(vuot_i) != 6:
        raise SystemExit(f"tờ M_1: cần 6 vuốt, thấy {len(vuot_i)}")

    # lửa: đặt gốc (đầu mút xa ngọn nhất) vào đúng chỗ lửa chui vào lỗ của dạng 2
    for ten, (gx, gy), w_, tip, ww, _ in LUA_NON:
        m = lab == lua_i[ten]
        im, goc = ML.manh_rgba(A, m)
        P_ = np.argwhere(m)[:, ::-1].astype(float)
        dinh = P_[np.argmax(np.hypot(*(P_ - (gx, gy)).T))]                 # ngọn: xa gốc khai nhất
        d = np.hypot(*(P_ - dinh).T)
        goc_thuc = P_[d > np.quantile(d, 0.93)].mean(0)                    # cụm điểm xa ngọn nhất = đầu gốc
        gl = dat[ten]["goc_lua"]
        im = im.resize((max(2, round(im.width * K_LUA)), max(2, round(im.height * K_LUA))), Image.LANCZOS)   # GPT vẽ lửa to hơn concept
        vt = (gl[0] - (goc_thuc[0] - goc[0]) * K_LUA, gl[1] - (goc_thuc[1] - goc[1]) * K_LUA)
        luu(ten, im, vt)
        ra[ten]["goc_lua"] = [int(gl[0]), int(gl[1])]
        ra[ten]["slot"] = None
        print(f"    {ten}: {im.size}, gốc lửa GPT vẽ lệch ({gl[0] - goc_thuc[0]:+.0f}, {gl[1] - goc_thuc[1]:+.0f})")

    # vuốt: rig vẽ vuốt TRƯỚC bàn tay như dạng 2 nên cả vuốt lộ ra (GPT vẽ vuốt to hơn concept, kèm phần "bị bàn tay che"): thu về cỡ
    # vuốt trong concept (K_VUOT lần chiều cao ô bố cục) rồi đặt như móng trên bàn chân thú: ba vuốt rải đều theo bề
    # ngang bàn tay, K_CHOM phần trên vuốt chờm lên mép dưới bàn tay ở đúng cột đó
    dv = dich_vuot or {}
    for ten, i in zip(VUOT_NON, vuot_i):
        im, _ = ML.manh_rgba(A, lab == i)
        x0, y0, x1, y1 = o_moi(dat, ap, ten)
        kv = K_VUOT * (y1 - y0) / im.height
        im = im.resize((max(2, round(im.width * kv)), max(2, round(im.height * kv))), Image.LANCZOS)
        bb = im.getbbox()
        tay = "tay_gan" if "gan" in ten else "tay_xa"
        ta = np.asarray(anh_[tay])[..., 3] > 128
        tx, ty = ra[tay]["goc"]
        thu = [v for v in VUOT_NON if ("gan" in v) == ("gan" in ten)].index(ten)      # trái → phải trong bàn tay
        cx = tx + (0.22, 0.52, 0.80)[thu] * ta.shape[1]                              # rải đều dọc mép dưới bàn tay như concept
        cot = np.nonzero(ta[:, int(round(cx - tx))])[0]
        day = ty + (cot.max() if len(cot) else ta.shape[0])
        ox, oy = dv.get(ten, (0, 0))
        luu(ten, im, (cx - (bb[0] + bb[2]) / 2 + ox, day - bb[1] - K_CHOM * (bb[3] - bb[1]) + oy))
        ra[ten]["slot"] = None
        print(f"    {ten}: {im.size} (ô bố cục {round(x1 - x0)}x{round(y1 - y0)}), tâm x {cx:.0f}, mép dưới bàn tay y {day}")

    # lõi: về cỡ và chỗ của lõi dạng 2 (lấp kín khe vỏ ngực); lõi tắt đổi màu bằng mã
    im, _ = ML.manh_rgba(A, lab == loi_i)
    w2, h2 = dat["loi"]["co"]
    im = im.resize((w2, h2), Image.LANCZOS)
    luu("loi", im, dat["loi"]["goc"])
    luu("loi_tat", ML.doi_mau(im, LOI_TAT), dat["loi"]["goc"])
    # bàn tay, mắt đã đổi cỡ: không dùng làm mốc khớp khung concept ↔ rig (rig lấy khớp khung của dạng 2: GL_KHOP)
    for t in list(TAY["gan"]) + list(TAY["xa"]) + ["mat", "mat_tat"]:
        ra[t]["slot"] = None

    ra["_thu_tu"] = [t for t in thu_tu if t in anh_]
    json.dump(ra, open(os.path.join(MANH, "dat.json"), "w", encoding="utf-8"), indent=1)
    # ghép lại cạnh concept đã duyệt
    C = Image.open(os.path.join(TAI, "L1_duyet.png")).convert("RGB")
    ghep = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    for t in ra["_thu_tu"]:
        if not t.endswith("_tat") and not t.endswith("_nguoi"):
            ghep.alpha_composite(anh_[t], tuple(ra[t]["goc"]))
    so = Image.new("RGB", (W * 2 + 10, H), (255, 255, 255))
    so.paste(C, (0, 0))
    so.paste(ghep.convert("RGB"), (W + 10, 0))
    so.save(os.path.join(MANH, "_so_ghep.png"))
    d = np.abs(np.asarray(ghep.convert("RGB")).astype(int) - np.asarray(C).astype(int)).max(2)
    print(f"  {len(ra) - 1} mảnh → {MANH}; ghép so concept: {100.0 * (d > 60).mean():.2f}% điểm lệch màu rõ")


def main(a):
    if a and a[0] == "bo_cuc":
        ra = {kieu: bo_cuc(kieu) for kieu in HUONG}
        json.dump(ra, open(os.path.join(MAU, "bo_cuc.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    elif a and a[0] == "manh":
        manh()
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
