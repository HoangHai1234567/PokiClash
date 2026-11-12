# -*- coding: utf-8 -*-
"""Chim bảo hộ rừng cánh lá (chim_la; tướng thứ 6 đảo Mộc): hình của mình chạy trên ĐÚNG rig của con gốc monster_3630.
Ghi chú: inbox/chim_la_ghichu.md. Cách làm như huou_go_rig.py (skill pokiclash-spine-rig mục 00):
- XƯƠNG: đủ mọi xương của họ, đúng cha – con, đúng biến đổi riêng ở dáng gốc; thêm `move`. Riêng các chuỗi xương MÀO được nắn thẳng
  theo năm chiếc lá mào của mình (đổi dáng mảnh nhận diện; vẫn nhận độ lệch xoay của clip gốc nên lá đung đưa như mào của họ).
- MẢNH: mọi part vẽ đúng khung ảnh vùng (chim_la_manh.py) lắp vào NGUYÊN lưới của họ, kể cả bộ chibangR3 (mặt kia của cánh gần) và bộ
  slot chân thứ hai (ẩn sẵn, clip bật). Bỏ mắt (vẽ trong ảnh đầu; `dau_nham` = ảnh đầu mắt nhắm bật khi họ đổi hình mắt), lưỡi, mào của
  họ. Mảnh thêm: năm lá mào (dải lưới trên chuỗi xương mào), vòng gỗ ở trán, hoa trên cành cánh, mầm lá trên tảng đá cuối chuỗi.
- CHIÊU MANA: lá của cánh bay ra găm rồi quay về (người dùng tả lá CỦA CÁNH): bản sao lưới lá trên xương `la_<i>` (con của `fly_<i>`,
  con của root; game co quãng theo chỗ đối thủ qua xương `far`), lá thật ẩn trong lúc bay; về tới thì trùng chỗ lá thật.
- CHUYỂN ĐỘNG: clip dựng ở tầng điều khiển (chim_la_clip.py), runtime Spine thật nướng ra scan/sample_moi.json → lệch so với dáng
  gốc cho mọi xương; slot ẩn / hiện theo trường n, a của mẫu. Kênh riêng (kenh_rieng.json): bay → xương `move`, mo → độ đậm cả con,
  la → lá bay. Thiên thạch của chiêu cuối là VFX: rig chỉ đặt sự kiện goi / roi / trung.
Xương, lưới và chuyển động gốc là của nhà phát hành game gốc; hình là của mình. Dùng nội bộ, không đăng công khai.

    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/chim_la_rig.py        → inbox/chim_la_1/rig/
    py -3 -I ArtGen/Spine/chim_la_rig.py soi <clip> <giây,giây,...> [tỉ lệ] [luoi]          → rig/soi_<clip>.png (khung lớn nền xám)
"""
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
sys.path.insert(0, os.path.join(HERE, "mo_xe"))
from quai import anh, luoi, trongso, khung, hoat, xuat, soi  # noqa: E402
from quai.khung import Dat  # noqa: E402
from quai.hoat import Clip  # noqa: E402
import chim_la as CL  # noqa: E402
import chim_la_manh as M  # noqa: E402
import chim_la_clip as RC  # noqa: E402

DANG = os.environ.get("CL_DANG", "lon")           # lon = dạng 2 (chim trưởng thành, đã duyệt); non = dạng 1 (chim non, cùng rig, đổi tỉ lệ)
TEN = "chim_la_1" if DANG == "lon" else "chim_la_non"
RA = os.environ.get("CL_RA") or os.path.join(HERE, "inbox", TEN, "rig")
NHE = os.environ.get("CL_NHE") == "1"             # bản NHẸ của dạng lớn (ảnh nhỏ, không lá bay) để gộp vào rig dạng non cho clip tiến hóa
if DANG == "non":
    M.MANH = os.path.join(HERE, "inbox", "chim_la_non", "manh")      # da chim non (chim_la_non.py: đổi màu + đầu mới)
KG = 1.0
D_PX = float(os.environ.get("CL_DPX", "0.3" if NHE else "0.5"))      # pixel ảnh atlas cho mỗi đơn vị rig (con cao ~900 đơn vị, sải cánh ~1750)
BO_XUONG = ("shadow", "L1", "L2")
BO_SLOT = ("shadow", "P_chiabangL_01", "P_chiabangL_04", "P_mao_02") + M.BO   # mao_02: túm lông kem không viền đè lên đùi lục xám, nhìn như miếng vá → bỏ;     # L_01: khúc cành gốc cánh xa nằm ngay sau mỏ, nhìn như chim ngậm que → bỏ
CLIPS = [("appear", "ca_appear", False), ("idle", "ca_idle", True), ("walk", "ca_walk", True), ("attack", "ca_attack", False),
         ("cast", "ca_cast", False), ("skill", "ca_skill", False), ("hit", "ca_hit", False), ("die", "ca_die", False)]
VE_NGHI = ("appear", "attack", "cast", "skill", "hit")
TAN = 0.45
IMPACT = {"attack": (0.07, 0.36, 0.10), "skill": (0.22, 1.0, 0.18, "#f2ead266")}
# mào: (chuỗi xương của họ được nắn thẳng, chỉ số lá trong CL.QUAT / tờ X); thứ tự vẽ sau → trước
MAO = [(["bone110", "bone113", "bone114"], 0), (["bone95"], 4), (["bone96", "bone97", "bone98"], 1),
       (["bone99", "bone100", "bone101", "bone102", "bone103"], 3), (["bone104", "bone105", "bone106", "bone107", "bone108", "bone109"], 2)]
# DẠNG NON (skill mục 00 "DẠNG KHÁC trên CÙNG rig gốc"): nhân tỉ lệ ở xương GỐC của chuỗi SAU KHI đã gắn xong mọi mảnh ở dáng gốc
# của dạng lớn (mọi điểm gắn tính theo dáng lớn nên co giãn theo xương, không phải gắn lại). bone144 là NoScale nên nhân riêng.
TI_NON = {"bone41": 0.86, "bone42": 0.86, "bone6": 1.34, "bone123": 0.60, "bone144": 0.60, "bone178": 0.60, "bone67": 0.60, "bone46": 0.65, "bone116": 0.74,
          "bone9": 0.86, "bone12": 0.86, "bone220": 0.86, "bone120": 0.8}
BO_NON = ("P_xiongjia_01", "P_xiongjia_02", "P_xiongjia_03", "P_xiongjia_04",       # chim non chưa có bùa đá
          "P_weiba1_06", "P_weiba1_05", "P_weiba1_04", "P_weiba1_03", "P_weiba1_02", "P_weiba1_01",      # chỉ còn hai chuỗi đá ngắn
          "P_weiba4_05", "P_weiba4_04", "P_weiba4_03", "P_weiba4_02", "P_weiba4_01",
          "P_xiongjia_06", "P_xiongjia_07",       # cụm lá ở vai: đầu to lên thì nó nằm trơ trên vai
          "P_chiabangL_05", "P_chiabangL_03")     # hai khúc cành trong của cánh xa: đầu to lên thì chúng chạm mỏ (như ngậm que)
# mào chim non: hai lá chữ V (mầm hai lá) trên hai chuỗi xương mào dài; (chuỗi, chỉ số lá, hệ số dài so với dạng lớn)
# (chuỗi, chỉ số lá, hệ số dài so với dạng lớn, xoay thêm độ)
MAO_NON = [(["bone99", "bone100", "bone101", "bone102", "bone103"], 3, 0.52, -16.0),
           (["bone104", "bone105", "bone106", "bone107", "bone108", "bone109"], 2, 0.50, 12.0)]
HOA = ["P_chibangR1_02", "P_chibangR2_2", "P_chibangR1_01", "P_chiabangL_02", "P_chiabangL_03", "P_chiabangL_05", "P_chibangR3_02"]   # L_01 nằm sát mỏ: không đặt hoa
HOA_CO = 44.0                                      # đường kính bông hoa (đơn vị rig)
MAM = ["P_weiba1_01", "P_weiba2_01", "P_weiba3_01", "P_weiba4_01"]
MAM_CAO = 64.0
VONG_RONG = 150.0
# lá bay của chiêu mana: slot lá dài của cánh gần (bộ R1) và cánh xa
LA_BAY = ["P_chibangR1_06", "P_chibangR1_05", "P_chibangR1_04", "P_chibangR1_10", "P_chibangR1_11",
          "P_chiabangL_07", "P_chiabangL_010", "P_chiabangL_08", "P_chiabangL_09", "P_chiabangL_11"]


def nap_goc():
    scan = CL.scan()
    D = json.load(open(os.path.join(scan, "att_goc.json"), encoding="utf-8"))
    D0 = json.load(open(os.path.join(scan, "att_idle0.json"), encoding="utf-8"))
    I = json.load(open(os.path.join(scan, "info.json"), encoding="utf-8"))
    return D, D0, I, scan


def anh_part(ten, a_tl):
    """ảnh part của mình thu về cỡ atlas; chưa gen xong thì lấy ô hướng dẫn (hình phẳng) làm ảnh giữ chỗ."""
    pth = os.path.join(M.MANH, "part", ten + ".png")
    pz = os.path.join(M.MANH, "part", "_z.json")
    zs = json.load(open(pz)) if os.path.exists(pz) else {}
    if os.path.exists(pth) and ten in zs:
        g, z = Image.open(pth).convert("RGBA"), zs[ten]
    else:
        z = 2.0
        im, m = M.thiet_ke(ten, z)
        g = Image.fromarray(np.dstack([im, (m * 255).astype(np.uint8)]), "RGBA")
        THIEU.append(M.ngan(ten))
    kq = D_PX / (a_tl * z)
    g = g.convert("RGBa").resize((max(2, round(g.width * kq)), max(2, round(g.height * kq))), Image.LANCZOS).convert("RGBA")
    return anh.loang_mau(g)


THIEU = []


def anh_them(ten):
    """ảnh ô thêm (tờ X) cắt sát; chưa có thì lấy ô hướng dẫn."""
    pth = os.path.join(M.MANH, "part", ten + ".png")
    if os.path.exists(pth):
        g = Image.open(pth).convert("RGBA")
    else:
        im, m = M.o_them(ten)
        g = Image.fromarray(np.dstack([im, (m * 255).astype(np.uint8)]), "RGBA")
        THIEU.append(ten)
    a = np.asarray(g)[..., 3] > 40
    ys, xs = np.nonzero(a)
    return g.crop((int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1))


def thu(g, k):
    return anh.loang_mau(g.convert("RGBa").resize((max(2, round(g.width * k)), max(2, round(g.height * k))), Image.LANCZOS).convert("RGBA"))


def gan_nguyen(sk, slot, anh_ten, att, ten, Wc, hinh=None):
    im = sk.images[anh_ten]
    L = luoi.Luoi(np.array(att["uv"], float).reshape(-1, 2) * np.array([im.width, im.height]), np.array(att["tris"]).reshape(-1, 3),
                  att["hull"], att["hull"], im.width, im.height, ten=slot)
    V = np.array(att["xy"], float).reshape(-1, 2) * KG
    sk.luoi_gan(slot, anh_ten, L, trongso.cung(L.n, "move"), the_gioi=V, ten=hinh)
    rows = []
    for p, ws in zip(V, att["w"]):
        row = [(ten[k], *[float(v) for v in (np.linalg.inv(Wc[ten[k]]) @ np.array([p[0], p[1], 1.0]))[:2]], float(w)) for k, w in ws if w > 0.002]
        tot = sum(r[3] for r in row) or 1.0
        rows.append([(n, x, y, w / tot) for n, x, y, w in row])
    sk.atts[slot][hinh or anh_ten]["verts"] = rows
    return L


def xuong_chinh(att, ten):
    """xương nặng nhất của một lưới (tổng trọng số)."""
    tong = {}
    for ws in att["w"]:
        for k, w in ws:
            tong[k] = tong.get(k, 0.0) + w
    return ten[max(tong, key=tong.get)]


def ts_gan_nhat(att, ten, p):
    V = np.array(att["xy"], float).reshape(-1, 2) * KG
    i = int(np.argmin(np.hypot(*(V - np.asarray(p, float)).T)))
    d = {ten[k]: float(w) for k, w in att["w"][i] if w > 0.01}
    s = sum(d.values()) or 1.0
    return {k: v / s for k, v in d.items()}


def cho_day(att, im_part):
    """điểm thế giới (dáng gốc) ở chỗ DÀY nhất của một part (cho hoa trên cành)."""
    a = np.asarray(im_part)[..., 3] > 127
    dt = cv2.distanceTransform(a.astype(np.uint8), cv2.DIST_L2, 5)
    y, x = np.unravel_index(int(np.argmax(dt)), dt.shape)
    Wd = M.the_gioi_o(att, im_part.width, im_part.height)
    return Wd[y, x] * KG


def dung():
    D, D0, I, scan = nap_goc()
    IB = I["bones"]
    ten = [b["name"] for b in IB]
    assert ten == [b["name"] for b in D["bones"]]
    a_tl = M.a_tl()
    Wc = {b["name"]: np.array([[b["a"], b["b"], b["x"] * KG], [b["c"], b["d"], b["y"] * KG], [0.0, 0.0, 1.0]]) for b in D["bones"]}
    Wi = {b["name"]: np.array([[b["a"], b["b"], b["x"] * KG], [b["c"], b["d"], b["y"] * KG], [0.0, 0.0, 1.0]]) for b in D0["bones"]}
    # sơ đồ bố cục (dáng idle 0 s) → thế giới dáng gốc, đi qua xương đầu
    CL.ATT = "att_idle0.json"
    CL._C.clear()
    T, sc = CL.khung_T()
    o = T(np.array([0.0, 0.0]))
    CL.ATT = "att_goc.json"
    CL._C.clear()
    M._T.clear()
    Dau = Wc["bone8"] @ np.linalg.inv(Wi["bone8"])

    def px_goc(p):
        q = np.array([(p[0] - o[0]) / sc * KG, (o[1] - p[1]) / sc * KG, 1.0])
        return (Dau @ q)[:2]

    # mào: nắn chuỗi xương theo lá
    nan = {}
    la_mao = []
    for ch, i, he, xo_ in ([(c_, i_, 1.0, 0.0) for c_, i_ in MAO] if DANG == "lon" else MAO_NON):
        g_, n_ = px_goc(CL.QUAT[i][0]), px_goc(CL.QUAT[i][1])
        cx_, sx_ = math.cos(math.radians(xo_)), math.sin(math.radians(xo_))
        n_ = g_ + np.array([[cx_, -sx_], [sx_, cx_]]) @ (n_ - g_) * he
        dai = float(np.hypot(*(n_ - g_)))
        goc = math.degrees(math.atan2(n_[1] - g_[1], n_[0] - g_[0]))
        dot = dai / len(ch)
        nan[ch[0]] = ("tg", float(g_[0]), float(g_[1]), goc, dot)
        for b in ch[1:]:
            nan[b] = ("rieng", dot, 0.0, 0.0, dot)
        la_mao.append((ch, i, g_, goc, dai, dot))

    sk = khung.Sk(TEN)
    sk.xuong("root")
    sk.xuong("move", "root")
    for b in IB:
        if b["name"] == "root" or b["name"] in BO_XUONG:
            continue
        cha = ten[b["parent"]]
        cha = "move" if cha == "root" else cha
        if b["name"] in nan:
            k, x, y, g, d = nan[b["name"]]
            sk.xuong(b["name"], cha, x, y, goc=g, dai=d, the_gioi=(k == "tg"))
        else:
            # inherit 3 = NoScale của Spine (bone144: gốc hai nhánh cánh gần; cha của nó co giãn trong clip)
            sk.xuong(b["name"], cha, b["x"] * KG, b["y"] * KG, goc=b["rot"], dai=b["len"] * KG, sx=b["sx"], sy=b["sy"],
                     khong_ti_le=(b.get("inherit") == 3))
    by = {a["slot"]: a for a in D["atts"]}
    bo = BO_SLOT + (BO_NON if DANG == "non" else ())
    slots = [s["name"] for s in I["slots"] if s["name"] not in bo and s["name"] in by]
    tong = [0, 0]
    an_san, theo_host, canh_xuong = [], {}, {}
    IM = {}

    def im_cua(r):
        if r not in IM:
            IM[r] = anh_part(r, a_tl)
        return IM[r]

    # khúc cành: đo trục dài, nửa bề dày, chiều dài giữa hai tâm đầu tròn của từng ảnh; rồi ghép ảnh với đốt xương theo chiều dài
    do_canh = {}
    for r_ in sorted(set(a_["region"] for a_ in D["atts"] if CL.loai(a_["region"]) == "canh")):
        im_ = im_cua(r_)
        ys_, xs_ = np.nonzero(np.asarray(im_)[..., 3] > 127)
        Pp = np.stack([xs_, ys_], 1).astype(float)
        cc = Pp.mean(0)
        ui = np.linalg.svd(Pp - cc, full_matrices=False)[2][0]
        vi = np.array([-ui[1], ui[0]])
        ta = (Pp - cc) @ ui
        rc = float(np.percentile(np.abs((Pp - cc) @ vi), 75))
        do_canh[r_] = (im_, ui, vi, rc, cc + ui * (np.percentile(ta, 0.5) + rc), float(np.percentile(ta, 99.5) - np.percentile(ta, 0.5) - 2 * rc))
    can = sorted([(float(IB[ten.index(xuong_chinh(by[s_], ten))]["len"]) * KG * D_PX, s_) for s_ in slots if CL.loai(by[s_]["region"]) == "canh"],
                 reverse=True)
    chon_canh, con = {}, set(do_canh)
    for dai_px, s_ in can:
        ung = con or set(do_canh)
        r_ = min(ung, key=lambda q: abs(math.log(max(1.0, do_canh[q][5]) / dai_px)))
        chon_canh[s_] = r_
        con.discard(r_)
    hoa_g, mam_g, vong_g = anh_them("hoa" if DANG == "lon" else "nu"), anh_them("mam"), anh_them("vong")
    sk.anh("hoa", thu(hoa_g, (HOA_CO if DANG == "lon" else 30.0) * D_PX / hoa_g.width))      # dạng non: nụ hoa thay cho hoa nở
    sk.anh("mam", thu(mam_g, MAM_CAO * D_PX / mam_g.height))
    sk.anh("vong", thu(vong_g, VONG_RONG * D_PX / vong_g.width))
    da_mao = False
    thu_tu_ho = [s["name"] for s in I["slots"]]
    for s in thu_tu_ho:
        if s.startswith("P_toushi"):
            if not da_mao:                         # năm lá mào của mình, sau đầu (chỗ slot mào đầu tiên của họ)
                da_mao = True
                for ch, i, g_, goc, dai, dot in la_mao:
                    g = anh_them(f"mao_{i + 1}")
                    im = thu(g, dai * D_PX / g.height)
                    nm = f"mao_{i + 1}"
                    sk.anh(nm, im)
                    sk.slot(nm, ch[0], nm)
                    hang = 2 * len(ch) + 1
                    L = luoi.luoi_o(im.width, im.height, 3, max(3, hang), ten=nm)
                    dat = Dat(float(g_[0]), float(g_[1]), goc=goc - 90.0, ti=dai / im.height, neo=(0.5, 1.0))
                    s_doc = (im.height - L.pts[:, 1]) * dai / im.height
                    sk.luoi_gan(nm, nm, L, trongso.chuoi(s_doc, dot, ch), dat=dat)
            if s == "P_toushi_01" and DANG == "lon":     # vòng gỗ ở trán, trước đầu
                c = px_goc((797.0, 301.0))
                gq = khung.goc_mat(Wc["bone8"]) - khung.goc_mat(Wi["bone8"])
                sk.slot("vong", "bone8", "vong")
                sk.manh("vong", "vong", Dat(float(c[0]), float(c[1]), goc=gq, ti=1.0 / D_PX))
            continue
        if s not in slots:
            continue
        a = by[s]
        r = a["region"]
        an = not a["cur"]
        if r in MAM and a["cur"] and DANG == "lon":                # mầm hai lá mọc trên tảng đá cuối chuỗi: vẽ ngay SAU tảng đá (gốc mầm khuất)
            V = np.array(a["xy"], float).reshape(-1, 2) * KG
            dinh = V[int(np.argmax(V[:, 1]))]
            xg = xuong_chinh(a, ten)
            sk.slot("mam_" + s, xg, "mam")
            sk.manh("mam_" + s, "mam", Dat(float(dinh[0]), float(dinh[1]) - 10.0, ti=1.0 / D_PX, neo=(0.5, 1.0)))
            theo_host["mam_" + s] = s
        la_canh = CL.loai(r) == "canh"
        sk.slot(s, "move", chon_canh[s] if la_canh else r, an=an)
        if an:
            an_san.append(s)
        if r not in sk.images and not la_canh:
            sk.anh(r, im_cua(r))
        if la_canh:
            # cành cánh = CÁNH TAY CÓ KHỚP: mỗi khúc cành nằm đúng dọc MỘT đốt xương cánh (gốc xương → mút xương), hai đầu tròn của ảnh
            # chồm qua hai khớp, bám cứng đốt đó → các khúc luôn dính nhau ở khớp, cánh gập cũng không rời (người dùng 2026-11-12:
            # "các khớp gỗ ở cánh không match nhau"; bản trước đặt khúc cành theo chỗ của dải hoa văn cũ nên rời nhau).
            xb = xuong_chinh(a, ten)
            Wb = Wc[xb]
            O = Wb[:2, 2]
            ub = Wb[:2, 0] / np.hypot(*Wb[:2, 0])
            dai_x = float(IB[ten.index(xb)]["len"]) * KG
            vb = np.array([-ub[1], ub[0]])
            r = chon_canh[s]                       # ảnh khúc cành có chiều dài tự nhiên gần đốt xương này nhất (ít phải kéo giãn)
            if r not in sk.images:
                sk.anh(r, im_cua(r))
            im_, ui, vi, rc, p0c, Li = do_canh[r]
            sa = dai_x / max(1.0, Li)
            sb = (1.0 / D_PX) * float(np.clip(sa * D_PX, 0.9, 1.25))            # khúc bị kéo dài thì mập lên chút cho cân
            goc4 = []
            for cx_, cy_ in ((0, 0), (im_.width, 0), (im_.width, im_.height), (0, im_.height)):
                d_ = np.array([cx_, cy_], float) - p0c
                goc4.append(O + ub * float(d_ @ ui) * sa + vb * float(d_ @ vi) * sb)
            L = luoi.Luoi(np.array([[0, 0], [im_.width, 0], [im_.width, im_.height], [0, im_.height]], float), np.array([[0, 1, 2], [0, 2, 3]]),
                          4, 4, im_.width, im_.height, ten=s)
            sk.luoi_gan(s, r, L, trongso.cung(4, xb), the_gioi=np.array(goc4))
            canh_xuong[s] = (xb, O, ub, dai_x)
        else:
            L = gan_nguyen(sk, s, r, a, ten, Wc)
        tong[0] += L.n
        tong[1] += len(L.tris)
        if s == "P_tou_01":                        # ảnh đầu mắt nhắm (bật khi họ đổi hình mắt lúc trúng đòn / chết)
            sk.anh("dau_nham", dau_nham(sk.images[r], a, by["P_yanjing_01"], to=(DANG == "non")))
            sk.slot("dau_nham", "move", "dau_nham", an=True)
            gan_nguyen(sk, "dau_nham", "dau_nham", a, ten, Wc)
        if a["region"] in HOA:                       # hoa trên cành cánh: ô cứng bám theo trọng số của cành ngay chỗ đó
            xb, O, ub, dai_x = canh_xuong[s]
            k_ = sum(map(ord, s))
            p = O + ub * dai_x * (0.38 + 0.07 * (k_ % 5))                    # hoa nằm trên thân khúc cành, mỗi khúc một chỗ khác
            nm = "hoa_" + s
            sk.slot(nm, "move", "hoa", an=an)
            Lq = luoi.luoi_o(sk.images["hoa"].width, sk.images["hoa"].height, 2, 2, ten=nm)
            sk.luoi_gan(nm, "hoa", Lq, trongso.cung(4, xb), dat=Dat(float(p[0]), float(p[1]), goc=(k_ % 5) * 14.0, ti=1.0 / D_PX))
            theo_host[nm] = s
    # mỏ: chỗ bắn / chỗ mổ
    V = np.array(by["P_zui_01"]["xy"], float).reshape(-1, 2) * KG
    mui = V[int(np.argmax(V[:, 0]))]
    lp = np.linalg.solve(Wc["bone8"], np.array([mui[0], mui[1], 1.0]))
    sk.xuong("mieng", "bone8", float(lp[0]), float(lp[1]))
    # lá bay của chiêu mana: fly_k (con của root, dáng gốc ở gốc toạ độ: game tính phần quãng = x / x của far) > la_k (độ lệch + góc);
    # bản sao lưới lá bám 100% la_k theo toạ độ của lá trong hệ xương chính của nó → la_k trùng xương đó thì bản sao trùng lá thật
    bay = []
    for k, s in enumerate(() if NHE else LA_BAY):
        a = by[s]
        xb = xuong_chinh(a, ten)
        sk.xuong(f"fly_{k}", "root", 0.0, 0.0)
        sk.xuong(f"la_{k}", f"fly_{k}", 0.0, 0.0)
        V = np.array(a["xy"], float).reshape(-1, 2) * KG
        Lc = (np.linalg.inv(Wc[xb]) @ np.c_[V, np.ones(len(V))].T).T[:, :2]
        im = sk.images[a["region"]]
        L = luoi.Luoi(np.array(a["uv"], float).reshape(-1, 2) * np.array([im.width, im.height]), np.array(a["tris"]).reshape(-1, 3),
                      a["hull"], a["hull"], im.width, im.height, ten=f"bay_{k}")
        sk.slot(f"bay_{k}", f"la_{k}", a["region"], an=True)
        sk.luoi_gan(f"bay_{k}", a["region"], L, trongso.cung(L.n, f"la_{k}"), the_gioi=Lc)
        u = np.linalg.svd(Lc - Lc.mean(0), full_matrices=False)[2][0]           # trục dài của lá (hướng ra ngọn = cùng phía trục x xương)
        if u[0] < 0:
            u = -u
        bay.append(dict(slot=s, xb=xb, truc=math.degrees(math.atan2(u[1], u[0]))))
    if DANG == "non":                              # đổi tỉ lệ SAU khi gắn xong
        for nm, k_ in TI_NON.items():
            b_ = sk.bones[sk.bi[nm]]
            b_["sx"] *= k_
            b_["sy"] *= k_
        sk.W0 = sk.the_gioi(khung.Pose())
        for k, lb in enumerate(bay):               # lá bay co đúng bằng lá thật trên cánh
            tl = float(np.hypot(*sk.W0[lb["xb"]][:2, 0]) / np.hypot(*Wc[lb["xb"]][:2, 0]))
            b_ = sk.bones[sk.bi[f"la_{k}"]]
            b_["sx"] = b_["sy"] = tl
        sk.W0 = sk.the_gioi(khung.Pose())
    # chiều cao game: đỉnh đầu ở dáng gốc (không tính mào, cánh)
    hinh_dau = sk.atts["P_tou_01"]["P_tou_01"]
    cao = max(sum(w * (sk.W0[b] @ np.array([x, y, 1.0]))[1] for b, x, y, w in row) for row in hinh_dau["verts"])
    cao = float(cao)
    sk.xuong("far", "root", 1.25 * cao, 0.45 * cao)        # xa hơn mọi chỗ lá xuất phát (game tính phần quãng theo x so với far)
    S = json.load(open(os.path.join(scan, "sample_moi.json"), encoding="utf-8"))
    for e, m in (("trung", "khung đòn trúng (mỏ chạm / lá găm / thiên thạch nện)"), ("tu", "bắt đầu lấy đà / tụ lực"), ("nem", "lá rời cánh"),
                 ("ve", "lá rút khỏi đối thủ bay về"), ("toi", "lá về tới cánh / appear: tới chỗ"), ("goi", "bung cánh gọi thiên thạch"),
                 ("roi", "thiên thạch hiện trên cao, bắt đầu rơi")):
        sk.su_kien(e, m)
    print(f"{len(sk.bones)} xương, {len(sk.slots)} slot, {tong[0]} đỉnh, {tong[1]} tam giác (lưới của họ); chiều cao game {cao:.0f}; ảnh vùng của họ "
          f"{a_tl:.3f} px mỗi đơn vị; slot ẩn sẵn {len(an_san)}" + (f"; CHƯA có ảnh ({len(THIEU)}): {', '.join(THIEU[:12])}…" if THIEU else ""))
    return sk, dict(scan=scan, IB=IB, ten=ten, slots=thu_tu_ho, cao=cao, S=S, bay=bay, theo_host=theo_host, nan=nan)


def dau_nham(im, att_dau, att_mat, to=False):
    """ảnh đầu với mắt nhắm: tô vùng mắt bằng màu mặt gần đó rồi kẻ một nét mí cong. to: mắt to tròn của chim non."""
    A = np.asarray(im).copy()
    h, w = A.shape[:2]
    pe = M.uv_cua(att_dau, np.array(att_mat["xy"], float).reshape(-1, 2).mean(0)) * np.array([w, h])
    z = (w / 169.0)
    cx, cy = int(pe[0]), int(pe[1])
    rx, ry = int(10.5 * z), int(6.5 * z)
    if to:
        cx, cy = int(pe[0] - 1.0 * z), int(pe[1] + 0.6 * z)
        rx = ry = int(11.0 * z)
    mk = np.zeros((h, w), np.uint8)
    cv2.ellipse(mk, (cx, cy), (rx, ry), 14, 0, 360, 1, -1)
    # màu mặt: trung vị các điểm sáng quanh mắt (ngoài vùng mắt)
    quanh = cv2.dilate(mk, np.ones((int(9 * z) | 1, int(9 * z) | 1), np.uint8)).astype(bool) & ~mk.astype(bool) & (A[..., 3] > 200)
    sang = quanh & (A[..., :3].min(axis=2) > 150)
    mau = np.median(A[..., :3][sang], axis=0) if sang.sum() > 10 else np.array(M.PAL["ma"])
    rgb = np.ascontiguousarray(A[..., :3])
    rgb[mk.astype(bool)] = mau
    cv2.ellipse(rgb, (cx, cy - int(1.0 * z)), ((int(8.6 * z), int(4.6 * z)) if to else (int(8.0 * z), int(3.6 * z))), 14, 20, 160, CL.INK,
                max(1, int(round(1.9 * z))), cv2.LINE_AA)
    A[..., :3] = rgb
    return Image.fromarray(A, "RGBA")


def chuyen_dong(sk, info):
    S = info["S"]
    IB, ten, SL = info["IB"], info["ten"], info["slots"]
    # xương có dùng: có trọng số ở một hình nào đó, hoặc là tổ tiên của xương như thế
    dung_ = set()
    for sl, hs in sk.atts.items():
        for h in hs.values():
            if h.get("type") == "mesh":
                for row in h["verts"]:
                    dung_.update(r[0] for r in row)
            elif "bone" in h:
                dung_.add(h["bone"])
    for sl in sk.slots:
        dung_.add(sl["bone"])
    cha = {b["name"]: b["parent"] for b in sk.bones}
    for b in list(dung_):
        while b:
            dung_.add(b)
            b = cha.get(b)
    ids = [i for i, n in enumerate(ten) if n in sk.bi and n != "root" and n in dung_]
    out = {}
    for clip, v in S.items():
        fr = v["frames"]
        res = {}
        for i in ids:
            b0 = IB[i]
            A = np.array([[F["l"][i][2] - b0["rot"], (F["l"][i][0] - b0["x"]) * KG, (F["l"][i][1] - b0["y"]) * KG,
                           F["l"][i][3] / (b0["sx"] or 1.0), F["l"][i][4] / (b0["sy"] or 1.0)] for F in fr])
            A[:, 0] = np.degrees(np.unwrap(np.radians(A[:, 0])))
            A[:, 0] -= 360.0 * round((A[0, 0] if clip == "ca_die" else A[-1, 0]) / 360.0)
            if ten[i] in info["nan"] and info["nan"][ten[i]][0] == "rieng":
                A[:, 1:3] = 0.0                    # đốt mào đã nắn thẳng: chỉ nhận độ lệch xoay
            if np.abs(A[:, :3]).max() > 1e-3 or np.abs(A[:, 3:] - 1).max() > 1e-4:
                res[ten[i]] = A
        dam = [{SL[j]: (0.0 if n is None else float(F["a"][j])) for j, n in enumerate(F["n"]) if SL[j] in sk.si} for F in fr]
        j_mat = SL.index("P_yanjing_01")
        nham = [F["n"][j_mat] == "P_yanjing_02" for F in fr]
        out[clip] = (float(v["dur"]), res, dam, nham, fr)
    return out


def lam_clip(sk, info):
    CD = chuyen_dong(sk, info)
    KR = json.load(open(os.path.join(info["scan"], "kenh_rieng.json"), encoding="utf-8"))
    mac_dinh = {sl["name"]: sl["alpha"] for sl in sk.slots}
    bay, host = info["bay"], info["theo_host"]
    far = sk.W0["far"][:2, 2]
    rng = np.random.default_rng(7)
    # người dùng 2026-11-12: "lá phải bắn vào trúng mục tiêu, nên kết hợp giữa điều khiển bằng code và animation": đích bay là xương
    # `far` (game dời tới đúng tâm đối thủ rồi co quãng từng xương fly_*: AolaActor.FarAtomik), nên lá chỉ tản HẸP quanh `far`
    # (± 9% chiều cao thân) để mọi chiếc đều găm vào thân đối thủ; đoạn về thì bám chỗ lá thật theo từng khung (animation) cho khớp.
    lech = [(float(rng.uniform(-36, 14)), float(rng.uniform(-80, 80)), float(rng.uniform(50, 140)) * (1 if k % 2 else -1), float(rng.uniform(-12, 12)))
            for k in range(len(bay))]

    def kenh(goc, ten_, tau):
        k = KR[goc][ten_]
        x = min(len(k) - 1, max(0.0, tau) * 30.0)
        i0 = int(x)
        i1 = min(i0 + 1, len(k) - 1)
        w = x - i0
        return (np.array(k[i0], float) * (1 - w) + np.array(k[i1], float) * w)

    neo_nem, truoc = {}, {}

    def dat_xuong(P, goc, tq):
        """chỉ phần xương của clip nguồn ở giây tq (+ độ dời move)."""
        dur, R, dam, nham, fr = CD[goc]
        n = len(dam)
        x = tq * 30.0
        i0 = min(int(x), n - 1)
        i1 = min(i0 + 1, n - 1)
        w = x - i0
        for b, A in R.items():
            v = A[i0] * (1 - w) + A[i1] * w
            if abs(v[0]) > 1e-4:
                P.rot(b, float(v[0]))
            if abs(v[1]) > 1e-4 or abs(v[2]) > 1e-4:
                P.move(b, float(v[1]), float(v[2]))
            if abs(v[3] - 1) > 1e-5 or abs(v[4] - 1) > 1e-5:
                P.scale(b, float(v[3]), float(v[4]))
        bx, by_ = kenh(goc, "bay", tq)
        if abs(bx) > 1e-4 or abs(by_) > 1e-4:
            P.move("move", float(bx) * KG, float(by_) * KG)
        return x, n

    def dat_dang(P, goc, tau, lap):
        dur, R, dam, nham, fr = CD[goc]
        tq = tau % dur if lap else min(max(tau, 0.0), dur)
        x, n = dat_xuong(P, goc, tq)
        ir = min(int(round(x)), n - 1)
        for s, a in dam[ir].items():
            if abs(a - mac_dinh[s]) > 1e-3:
                P.alpha[s] = a
        for s2, s in host.items():
            a = dam[ir].get(s, mac_dinh[s])
            if abs(a - mac_dinh[s2]) > 1e-3:
                P.alpha[s2] = a
        if nham[ir]:
            P.alpha["dau_nham"] = 1.0
        q, bat = kenh(goc, "la", tq)
        if KR[goc]["la"][ir][1] > 0.5:             # lá đang bay: chỗ và góc của lá thật lấy từ chính bộ xương này ở khung đang dựng
            q = float(q)
            W = sk.the_gioi(P)
            if goc not in neo_nem:                 # dáng ở khung lá rời cánh (nem): chỗ xuất phát
                P0 = khung.Pose()
                dat_xuong(P0, goc, RC.C_NEM)
                neo_nem[goc] = sk.the_gioi(P0)
            W0n = neo_nem[goc]
            ve_ = tq >= RC.C_VE
            if tq < truoc.get("t", -1.0):
                truoc.clear()
            truoc["t"] = tq
            for k, lb in enumerate(bay):
                dx, dy, vong, xo = lech[k]
                S0, rot0 = W0n[lb["xb"]][:2, 2], khung.goc_mat(W0n[lb["xb"]])
                Tg = far + np.array([dx, dy])
                E, g_e = W[lb["xb"]][:2, 2], khung.goc_mat(W[lb["xb"]])
                A_ = E if ve_ else S0
                d = Tg - A_
                nn = np.array([-d[1], d[0]]) / (np.hypot(*d) + 1e-6)
                Pd = A_ + q * d + nn * vong * math.sin(math.pi * q) * (0.6 if ve_ else 1.0)
                fly = q * far                      # fly_k chỉ mang phần quãng (game co quãng theo x của nó so với far)
                P.move(f"fly_{k}", float(fly[0]), float(fly[1]))
                P.move(f"la_{k}", float(Pd[0] - fly[0]), float(Pd[1] - fly[1]))
                huong = math.degrees(math.atan2(d[1], d[0])) + xo
                g_bay = (huong if not ve_ else huong + 180.0) - lb["truc"]      # mũi lá đi trước
                g_neo = g_e if ve_ else rot0
                f_ = min(1.0, q / 0.22)                                         # gần cánh thì xoay về góc của lá thật
                f_ = f_ * f_ * (3 - 2 * f_)
                g = g_neo + ((g_bay - g_neo + 180.0) % 360.0 - 180.0) * f_
                if k in truoc:                     # giữ góc liền mạch giữa các khung (không nhảy 360 độ)
                    g += 360.0 * round((truoc[k] - g) / 360.0)
                truoc[k] = g
                P.rot(f"la_{k}", float(g))
                P.alpha[f"bay_{k}"] = 1.0
                P.alpha[lb["slot"]] = 0.0
        return float(kenh(goc, "mo", tq))

    out = []
    for ten_, goc, lap in CLIPS:
        dur = CD[goc][0]
        ev = [tuple(e) for e in KR[goc]["su_kien"]]
        if ten_ == "die":
            def fn(t, P, goc=goc, dur=dur):
                dat_dang(P, goc, t, False)
                a = float(np.clip(1.0 - (t - dur) / (TAN - 0.1), 0.0, 1.0))
                for sl in sk.slots:
                    P.alpha[sl["name"]] = a * P.alpha.get(sl["name"], sl["alpha"])
            out.append(Clip(ten_, dur + TAN, fn, ev=ev))
        elif ten_ == "appear":
            def fn(t, P, goc=goc):
                mo = dat_dang(P, goc, t, False)
                if mo < 0.999:
                    for sl in sk.slots:
                        P.alpha[sl["name"]] = mo * P.alpha.get(sl["name"], sl["alpha"])
            out.append(Clip(ten_, dur, fn, ev=ev))
        else:
            out.append(Clip(ten_, dur, (lambda t, P, goc=goc, lap=lap: dat_dang(P, goc, t, lap) and None), loop=lap, ev=ev))
    return out, dat_dang


def main(a):
    sk, info = dung()
    clips, dat_dang = lam_clip(sk, info)
    if a and a[0] == "bo_cuc":                   # khung 0 idle trên nền trắng 1536 × 1024: hình bố cục cho concept (da đang có)
        c = [x for x in clips if x.ten == "idle"][0]
        P = hoat.nuong(sk, c)[0]
        ve = soi.Ve(sk)
        bx = ve.bao(P)
        sc = min(1240.0 / (bx[2] - bx[0]), 900.0 / (bx[3] - bx[1]))
        im = ve.ve(P, bx, sc, bg=(255, 255, 255), ss=2).convert("RGB")
        out = Image.new("RGB", (1536, 1024), (255, 255, 255))
        out.paste(im, ((1536 - im.width) // 2, (1024 - im.height) // 2))
        mau = os.path.join(HERE, "inbox", TEN, "mau")
        os.makedirs(mau, exist_ok=True)
        pth = os.path.join(mau, "bo_cuc.png")
        out.save(pth)
        json.dump({"sc": sc, "bx": [float(v) for v in bx], "o": [(1536 - im.width) // 2, (1024 - im.height) // 2]},
                  open(os.path.join(mau, "bo_cuc.json"), "w"))
        print(pth, f"{sc:.4f} px mỗi đơn vị rig; khung", [round(float(v)) for v in bx])
        return
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
        os.makedirs(RA, exist_ok=True)
        pth = os.path.join(RA, f"soi_{a[1]}.png")
        out.save(pth)
        print(pth, out.size)
        return
    frames = {c.ten: hoat.nuong(sk, c) for c in clips}
    for c in clips:
        if c.ten in VE_NGHI:
            frames[c.ten] = [P.copy() for P in frames[c.ten]]
            hoat.khop_cuoi(frames[c.ten], frames["idle"][0], 0.2)
    if a and a[0] == "nhe":                        # CL_NHE=1 (dạng lớn): ghi bản nhẹ cho rig dạng non gộp tiến hóa
        import pickle
        os.makedirs(RA, exist_ok=True)
        pickle.dump(dict(sk=sk, idle=frames["idle"], cao=info["cao"]), open(os.path.join(RA, "_nhe.pkl"), "wb"))
        print("bản nhẹ:", os.path.join(RA, "_nhe.pkl"))
        return
    Mx, noi = sk, {}
    if DANG == "non":
        # TIẾN HÓA nối liền: gộp bản nhẹ của dạng lớn (dựng ở tiến trình riêng vì cấu hình theo dạng đọc lúc nạp mô-đun)
        import pickle
        import subprocess
        from quai import tienhoa
        subprocess.run([sys.executable, "-I", os.path.abspath(__file__), "nhe"], env=dict(os.environ, CL_DANG="lon", CL_NHE="1", CL_RA=""),
                       check=True)
        B = pickle.load(open(os.path.join(HERE, "inbox", "chim_la_1", "rig", "_nhe.pkl"), "rb"))
        sk2, idle2, cao2 = B["sk"], B["idle"], B["cao"]
        ti = info["cao"] / cao2
        Mx = tienhoa.gop(sk, sk2)
        E_DUR, E_B0 = 3.0, 1.10

        def gong(t, P):                            # chim non: thu hai cánh ôm thân, co người, rung mạnh dần (đoạn đầu chiêu cuối của nó)
            ta = hoat.cv(t, [(0, 0.0), (0.35, 0.26), (1.35, 0.70), (E_DUR, 0.70)])
            dat_dang(P, "ca_skill", float(ta), False)
            r = hoat.rung(t, 0.45, 1.3, moi=1)
            P.move("move", 3.0 * r, 2.0 * r)

        def bung(t, P, fl):                        # chim lớn: hiện ra đang vỗ một nhịp idle chậm, vươn lên, ngẩng đầu kêu rồi về dáng nghỉ
            n = len(idle2) - 1
            x = min(1.0, max(0.0, (t - E_B0) / (E_DUR - E_B0))) * n
            i0 = min(int(x), n)
            i1 = min(i0 + 1, n)
            w = x - i0
            ten_ = set(idle2[i0].t) | set(idle2[i1].t)
            for b in ten_:
                v0, v1 = idle2[i0].t.get(b, khung.ZERO), idle2[i1].t.get(b, khung.ZERO)
                P.t["n_" + b] = [v0[q] * (1 - w) + v1[q] * w for q in range(5)]
            P.move("n_bone", 0.0, 60.0 * fl)
            P.rot("n_bone8", 12.0 * fl)
            P.rot("n_bone5", 3.0 * fl)

        ev = tienhoa.clip_tien_hoa(Mx, sk, sk2, idle2[0], tiB=ti, dur=E_DUR, fnA=gong, fnB=bung, gam=(1.45, 1.85, 2.25, 2.65), mem=[])
        # n_bone144 là NoScale: không nhận tỉ lệ của xương evo (dạng lớn co tiB trong rig gộp) → phần ngoài cánh gần lệch cỡ ~6%
        # (khung cuối lệch 46 px so với idle dạng lớn). Nhân bù đúng tỉ lệ của evo cho riêng xương này, sau bước hoà về idle.
        post0 = ev.post

        def post_ns(t, P):
            post0(t, P)
            P.scale("n_bone144", ti * hoat.cv(t, [(0, 0.86), (1.0, 0.86), (1.95, 1.0, "out"), (E_DUR, 1.0)]))

        ev.post = post_ns
        clips = clips + [ev]
        _, _, s_ev = tienhoa.lech_cuoi(Mx, hoat.nuong(Mx, ev), sk2, idle2[0], ti)
        noi["evolve"] = s_ev + f" (dạng lớn co {ti:.3f} trong rig gộp)"
        print("  evolve:", noi["evolve"])
    xuat.xuat_het(Mx, clips, RA, TEN, "Chim bảo hộ rừng cánh lá (chim_la), " + ("dạng 2: chim lớn" if DANG == "lon" else "dạng 1: chim non"),
                  frames=frames, dang=(2 if DANG == "lon" else 1), so_dang=2,
                  dung_yen=("cast", "skill"), far=("cast",), far_aim=("cast",), ma_goc=None, khop_idle=0, cao=info["cao"], noi_them=noi, impact=IMPACT,
                  tol={"rotate": 0.06, "translate": 0.15, "scale": 0.0015}, dich_mb=0.9, tran_mb=1.4)


if __name__ == "__main__":
    main(sys.argv[1:])
