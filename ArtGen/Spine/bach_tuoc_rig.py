# -*- coding: utf-8 -*-
"""Bạch tuộc quái vật dạng 2 (bach_tuoc_2): hình của mình chạy trên ĐÚNG rig của con gốc monster_3616. Ghi chú: inbox/bach_tuoc_ghichu.md.

- XƯƠNG: đủ mọi xương của họ (trừ shadow và ba mục tiêu IK đã nướng), đúng cha – con, đúng biến đổi riêng ở dáng gốc, đơn vị × KG.
  Con gốc nhìn PHẢI (mắt hướng về phía ba xúc tu ngắn) như game cần: KHÔNG lật (xương `lat` giữ tỉ lệ 1, để sau này cần thì đổi).
- MẶT giữ cách dựng của con gốc (người dùng 2026-11-12: "chỉ thấy 1 bên mắt, không có mồm"): nhìn nghiêng, một mắt, không mồm.
- BỎ của con gốc (người dùng 2026-11-12: "không nhất thiết phải có phần tàu ở trên, có thể bỏ"): mũ (mảnh tàu), mặt trong của nó,
  san hô, xích. THÊM của mình: mào ba gai thịt (ô cứng bám da đầu ngay chỗ gốc gai, vẽ sau đầu).
- MẢNH: mỗi slot dùng NGUYÊN lưới của họ (đỉnh, tam giác, uv, trọng số) với ảnh của mình vẽ đúng khung part (bach_tuoc.anh_part:
  bản Codex vẽ ở manh/part, chưa có thì da tạm tô phẳng bằng mã). Mắt: ba hình (mở, lim dim, nhắm) là ba slot bật bằng độ đậm.
- CHUYỂN ĐỘNG: mẫu 30 khung/giây của runtime Spine (biến đổi riêng ĐÃ áp IK, đường cong): clip của họ (scan/sample_dk.json) và clip
  riêng của mình dựng ở tầng điều khiển (bach_tuoc_clip.py → scan/sample_moi.json).
- THÊM CỦA MÌNH: hố đất hai lớp + mặt nạ cắt cho appear; bạch tuộc con trên xương fly* cho chiêu cuối (game dời far / fly* tới đối
  thủ); xương `mieng` (chỗ phụt bóng mực; bóng mực là VFX).
Xương, lưới và chuyển động là của nhà phát hành game gốc; hình là của mình. Dùng nội bộ, không đăng công khai.

    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/bach_tuoc_rig.py        → inbox/bach_tuoc_2/rig/ (xem.html, khung_*.png)
    py -3 -I ArtGen/Spine/bach_tuoc_rig.py soi <clip> <giây,giây,...> [tỉ lệ]                 → rig/soi_<clip>.png (khung lớn nền xám)
"""
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "mo_xe"))
from quai import anh, luoi, trongso, khung, hoat, xuat, soi  # noqa: E402
from quai.khung import Dat  # noqa: E402
from quai.hoat import Clip  # noqa: E402
import bach_tuoc as BT  # noqa: E402
import bach_tuoc_clip as BC  # noqa: E402

TEN = f"bach_tuoc_{BT.K}"
RA = os.path.join(BT.BASE, "rig")
KG = 0.44                    # đơn vị rig con gốc → đơn vị rig của mình
PXU = 0.64                   # pixel ảnh atlas cho mỗi đơn vị rig con gốc (atlas của họ: 0,5)
# BẢN NHẸ (BT_NHE=1): dạng 2 gộp vào file dạng 1 cho clip evolve (chỉ hiện ~1,3 giây cuối): ảnh nhỏ, không hố, không tay chống, không
# bạch tuộc con
NHE = os.environ.get("BT_NHE") == "1"
if NHE:
    PXU = 0.36
# appear TRỒI LÊN TỪ HỐ (hố đất hai lớp, mặt nạ cắt, hai tay chống) chỉ dạng 2 có. Dạng 1: người dùng 2026-11-12 "dạng 1 appear làm nó
# nhảy vào là được" → nhảy từ ngoài vào (clip viết ở rig), rig dạng 1 không mang hố, mặt nạ, tay chống
CO_HO = BT.K == 2 and not NHE
BO_TEN = ("shadow", "CJ1", "CJ2", "CJ3")
SLOT = {"P_shou6_2": "xt6_ngon", "P_shou6_1": "xt6_goc", "P_tou": "dau", "P_yanjing1": "mat", "P_shou5_1": "ngon_3", "P_shou4_1": "ngon_2",
        "P_shou3_1": "ngon_1", "P_shou1_3": "xt1_khoi", "P_shou1_2": "xt1_goc", "P_shou2_2": "xt2_goc", "P_shou1_1": "xt1_ngon",
        "P_shou2_1": "xt2_ngon"}
MAT = {"P_yanjing1": "mat", "P_yanjing2": "mat_lim", "P_yanjing 3": "mat_nham"}
# xương của họ chỉ phục vụ phần đã bỏ (mũ bone32, san hô bone33–38 + bone47, xích bone48 + bone39–46): không đưa vào rig
BO_XUONG = tuple(["bone32", "bone33", "bone34", "bone35", "bone36", "bone37", "bone38", "bone47", "bone48"] + [f"bone{i}" for i in range(39, 47)])
# DẠNG 1 (con non, BT_DANG=1): cùng xương, lưới, clip; chỉ đổi TỈ LỆ DÁNG GỐC của vài xương (xương con thừa hưởng) và da. Đầu to: phóng
# bone5 (giữa vòm đầu; bone6, xương mắt, da đỉnh đầu theo nó) và bone76 (da má phải); xúc tu ngắn, mảnh hơn: thu xương gốc từng xúc tu.
# CAO_KHAI: chiều cao khai cho game = chiều cao đo × hệ số này (game co tướng theo chiều cao khai: khai lớn hơn thì vẽ nhỏ lại).
# SO_CON: số bạch tuộc con của chiêu cuối (người dùng 2026-11-12: "dạng 2 gọi nhiều bạch tuộc mini hơn (6 con)"; dạng 1 gọi 3)
TI_LE, CAO_KHAI, SO_CON = {}, 1.0, 6
MAT_TI = 1.35                # con mắt phóng quanh tâm chừng này lần so với part của họ (concept đã duyệt: mắt to, gần kín vành hốc mắt)
if BT.K == 1:
    TI_LE = {"bone5": 1.13, "bone76": 1.13, "bone12": 0.84, "bone77": 0.84, "bone7": 0.84, "bone27": 0.84, "bone18": 0.9, "bone21": 0.9,
             "bone24": 0.9}
    CAO_KHAI, SO_CON = 1.2, 3
    MAT_TI = 1.62
LAT_X = 1.0                  # 2026-11-12: bản đầu để −1 vì đoán sai hướng mặt con gốc; người dùng: "mắt hướng cùng với bên xúc tu ngắn"
CAT_TI = 12.0                # mặt nạ cắt lúc không dùng còn phóng to chừng này lần (vách hai bên ra xa, không cắt gì)
CLIPS = [("appear", "bt_appear", False), ("idle", "idle_01", True), ("walk", "bt_walk", True), ("attack", "bt_attack", False),
         ("cast", "bt_cast", False), ("skill", "bt_skill", False), ("hit", "hit_01", False), ("die", "die_01", False)]
# giảm biên độ xoay của vài xương ở clip của họ: {clip nguồn: {xương: hệ số}}. idle_01: ngọn xúc tu to phía sau (xúc tu 1) duỗi – cuộn
# 45–86 độ, lưới thưa của ngọn tự gập thành mép răng cưa; con gốc che chỗ đó bằng mép mũ tàu, của mình (đã bỏ mũ) lộ ra như bị rách
GIAM = {"idle_01": {"bone14": 0.5, "bone15": 0.5, "bone16": 0.5, "bone17": 0.5}}
# HAI TAY CHỐNG của appear: (tên, xương gốc xúc tu của thân mà tay mọc ra cạnh đó, đỉnh vươn lên, chỗ ngọn bám đất, phía −1 trái / +1 phải,
# trễ). Toạ độ theo đơn vị con gốc; miệng hố là elip tâm (0, 18) bán trục 693 × 161. Chỗ bám nằm NGOÀI miệng hố và cao hơn tâm hố (đất
# phía dưới tâm thuộc lớp vành trước, vẽ đè lên thân). Bạch tuộc có 8 tay, rig lộ 6: hai tay này là hai tay khuất, xong việc thu vào sau thân.
VOI = [("vt", "bone12", (-430.0, 640.0), (-900.0, 14.0), -1.0, 0.00), ("vp", "bone27", (455.0, 610.0), (870.0, 22.0), 1.0, 0.05)]
# thu tay vào sau đầu: {tay: (chỗ gốc tay trượt tới, chỗ ngọn dừng)} tính từ gốc xương thân bone3 (đơn vị rig). Cả hai điểm nằm
# trong hình bóng vòm đầu (so với bone3: x −269..127, y −5..285) nên cuối đoạn thu cả tay khuất sau đầu; gốc trượt sang phía bên kia
# đầu để tay TRƯỢT vào (giữ chiều dài) chứ không co ngắn lại
VOI_TRONG = {"vt": ((45.0, 105.0), (-105.0, 165.0)), "vp": ((-150.0, 112.0), (15.0, 172.0))}
VOI_DAY = 1.8                # bề dày tay phóng thêm chừng này lần so với ảnh (ảnh vẽ thon dài; tay phải mập cỡ xúc tu của thân)
VOI_DOT, VOI_DAI, VOI_PX = 10, 470.0, 1.1          # số đốt, chiều dài tự nhiên (đơn vị rig), pixel atlas mỗi đơn vị
QUAY_AN = {"bt_appear": 0.1}     # appear: cả thân ẩn (độ đậm 0) tới 0,2 s
TAN = 0.45                   # die: giữ dáng cuối rồi mờ dần chừng này giây
# hố đất của appear (đơn vị rig của mình): miệng hố rộng HO_RONG, tâm ở (0, HO_Y); ảnh hố vào atlas HO_PX pixel mỗi đơn vị rig
HO_RONG, HO_Y, HO_PX = 610.0, 8.0, 0.85
CAT_SAU = 3000.0             # mặt nạ cắt lúc không dùng nằm sâu chừng này dưới đất (không cắt gì)
# bạch tuộc con của chiêu cuối: (x xuất phát, y, cỡ) quanh thân, phía trước là +x; FAR = chỗ đối thủ ở dáng gốc (game dời tới chỗ thật)
FAR = (640.0, 150.0)
CON = [(235.0, -46.0, 1.0), (-250.0, -40.0, 0.9), (330.0, 6.0, 0.86), (-335.0, 10.0, 0.8), (160.0, 20.0, 0.78),
       (-130.0, -66.0, 0.94)]       # ba con phía trước, ba con phía sau / dưới thân (dạng 1 chỉ dùng ba con đầu)
CON_CAO = 88.0               # chiều cao bạch tuộc con (đơn vị rig)
BO, NHAY, TRUNG0 = 0.52, 0.24, 0.0      # thời gian bò, nhảy; (TRUNG0 tính trong lam_clip)


def anh_con():
    """ảnh bạch tuộc con: bản Codex vẽ (manh/bt_con.png) nếu có, không thì hình tạm vẽ bằng mã."""
    p = os.path.join(BT.MANH, "bt_con.png")
    if os.path.exists(p):
        return Image.open(p).convert("RGBA"), False
    S = 4
    im = Image.new("RGBA", (120 * S, 110 * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    ink, da, bung = BT.INK + (255,), BT.PAL["da"] + (255,), BT.PAL["bung"] + (255,)
    for i, x in enumerate((14, 36, 58, 80)):
        d.ellipse([x * S, 66 * S, (x + 28) * S, 104 * S], fill=bung if i % 2 else da, outline=ink, width=3 * S)
    d.ellipse([12 * S, 6 * S, 108 * S, 88 * S], fill=da, outline=ink, width=3 * S)
    d.ellipse([66 * S, 40 * S, 88 * S, 64 * S], fill=BT.PAL["mat"] + (255,), outline=ink, width=2 * S)
    d.rectangle([70 * S, 50 * S, 84 * S, 55 * S], fill=ink)
    return im.resize((120, 110), Image.LANCZOS), True


def anh_voi():
    """ảnh xúc tu dài (manh/voi.png: duỗi thẳng nằm ngang, gốc trái, trục giữa ảnh); chưa có thì hình tạm vẽ bằng mã."""
    p = os.path.join(BT.MANH, "voi.png")
    if os.path.exists(p):
        return Image.open(p).convert("RGBA"), False
    S = 2
    im = Image.new("RGBA", (1100 * S, 190 * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.polygon([(4 * S, 6 * S), (1070 * S, 78 * S), (1094 * S, 95 * S), (1070 * S, 112 * S), (4 * S, 184 * S)], fill=BT.PAL["da"] + (255,),
              outline=BT.INK + (255,))
    d.polygon([(4 * S, 130 * S), (1070 * S, 100 * S), (1070 * S, 112 * S), (4 * S, 184 * S)], fill=BT.PAL["bung"] + (255,), outline=BT.INK + (255,))
    return im.resize((1100, 190), Image.LANCZOS), True


def dung():
    scan = BT.scan()
    D = json.load(open(os.path.join(scan, "att_goc.json"), encoding="utf-8"))
    I = json.load(open(os.path.join(scan, "info.json"), encoding="utf-8"))
    IB = I["bones"]
    ten = [b["name"] for b in IB]
    assert ten == [b["name"] for b in D["bones"]]

    sk = khung.Sk(TEN)
    sk.xuong("root")
    sk.xuong("move", "root")                     # game đo độ dời thân trên xương này
    sk.xuong("lat", "move", sx=LAT_X)            # con gốc đã nhìn phải: không lật
    for b in IB:
        if b["name"] == "root" or b["name"] in BO_TEN or b["name"] in BO_XUONG:
            continue
        cha = ten[b["parent"]]
        k_ = TI_LE.get(b["name"], 1.0)
        sk.xuong(b["name"], "lat" if cha == "root" else cha, b["x"] * KG, b["y"] * KG, goc=b["rot"], dai=b["len"] * KG, sx=b["sx"] * k_,
                 sy=b["sy"] * k_)
    # ma trận thế giới dáng gốc ĐÃ ÁP RÀNG BUỘC của họ (IK, đường cong), trong hệ CHƯA lật: điểm gắn lưới tính theo đây
    Wc = {b["name"]: np.array([[b["a"], b["b"], b["x"] * KG], [b["c"], b["d"], b["y"] * KG], [0.0, 0.0, 1.0]]) for b in D["bones"]}
    LAT = np.array([LAT_X, 1.0])

    # hố đất, lớp sau: vẽ đầu tiên
    hj = json.load(open(os.path.join(BT.MANH, "ho.json"), encoding="utf-8"))
    hs = HO_RONG / (2 * hj["a"])                 # đơn vị rig mỗi pixel ảnh hố
    sk.xuong("ho", "root", 0.0, HO_Y)
    sk.xuong("cat_x", "root", 0.0, HO_Y - CAT_SAU, sx=CAT_TI, sy=CAT_TI)

    def anh_ho(t):
        g = Image.open(os.path.join(BT.MANH, t + ".png")).convert("RGBA")
        bb = g.getbbox()
        g = g.crop(bb).convert("RGBa")
        k = hs * HO_PX
        g = anh.loang_mau(g.resize((max(2, round(g.width * k)), max(2, round(g.height * k))), Image.LANCZOS).convert("RGBA"))
        sk.anh(t, g)
        # góc trên trái của khung đã cắt → thế giới
        x = (bb[0] - hj["cx"]) * hs
        y = HO_Y - (bb[1] - hj["cy"]) * hs
        return Dat(x, y, neo=(0.0, 0.0), ti=1.0 / HO_PX)

    if CO_HO:
        d_sau = anh_ho("ho_sau")
        sk.slot("ho_sau", "ho", "ho_sau", an=True)
        sk.manh("ho_sau", "ho_sau", d_sau)
        sk.slot("cat", "cat_x")                  # mặt nạ cắt: đặt hình ở cuối (cần biết slot cuối của thân)

    # hai tay chống của appear: dải lưới VOI_DOT đốt, vẽ SAU thân (ngay trên lớp sau của hố), trong vùng mặt nạ cắt; ẩn mặc định
    voi_tam, tong = False, [0, 0]
    if CO_HO:
        gv, voi_tam = anh_voi()
        kv = VOI_DAI * VOI_PX / gv.width
        sk.anh("voi", anh.loang_mau(gv.convert("RGBa").resize((round(gv.width * kv), max(2, round(gv.height * kv))), Image.LANCZOS).convert("RGBA")))
        iv = sk.images["voi"]
        Lv = luoi.luoi_dai(iv, VOI_DOT, ten="voi", buoc=13.0, in_tk=False)
        for ten_, goc_x, _, _, phia, _ in VOI:
            r0 = sk.W0[goc_x][:2, 2]
            # tay bên trái lật dọc ảnh: mặt dưới (kem) phải nằm phía TRONG vòm khi tay chống xuống đất
            dv = Dat(float(r0[0]), float(r0[1]), ti=(1.0 / VOI_PX, (-VOI_DAY if phia < 0 else VOI_DAY) / VOI_PX), neo=(0.0, 0.5))
            names = sk.chuoi(ten_, "bone3", dv.ra(Lv.khop(VOI_DOT), iv.width, iv.height))
            sk.slot(ten_, names[0], "voi", an=True)
            sk.luoi_gan(ten_, "voi", Lv, trongso.chuoi(Lv.s, Lv.truc[1][-1] / VOI_DOT, names), dat=dv)
        tong = [2 * Lv.n, 2 * len(Lv.tris)]

    by = {a["att"]: a for a in D["atts"]}
    tam = []
    than = []

    def gan(slot, hinh, an=False, V=None, anh_co=None):
        """slot dùng nguyên lưới của họ (att `hinh`). V: toạ độ thế giới khác (mắt xa); anh_co: dùng lại ảnh đã có trong atlas."""
        a = by[hinh]
        if anh_co is None:
            g, la_tam = BT.anh_part(hinh)
            if la_tam:
                tam.append(hinh)
            g = g.convert("RGBa").resize((max(2, round(g.width / BT.Z * 2 * PXU)), max(2, round(g.height / BT.Z * 2 * PXU))), Image.LANCZOS).convert("RGBA")
            sk.anh(slot, anh.loang_mau(g))
        ta = anh_co or slot
        im = sk.images[ta]
        L = luoi.Luoi(np.array(a["uv"], float).reshape(-1, 2) * np.array([im.width, im.height]), np.array(a["tris"]).reshape(-1, 3),
                      a["hull"], a["hull"], im.width, im.height, ten=slot)
        V = (np.array(a["xy"], float).reshape(-1, 2) if V is None else np.asarray(V, float)) * KG
        sk.slot(slot, "move", ta, an=an)
        sk.luoi_gan(slot, ta, L, trongso.cung(L.n, "move"), the_gioi=V * LAT)
        rows = []
        for p, ws in zip(V, a["w"]):
            row = [(ten[k], *[float(v) for v in (np.linalg.inv(Wc[ten[k]]) @ np.array([p[0], p[1], 1.0]))[:2]], float(w)) for k, w in ws if w > 0.002]
            tot = sum(r[3] for r in row) or 1.0
            rows.append([(n, x, y, w / tot) for n, x, y, w in row])
        sk.atts[slot][ta]["verts"] = rows
        tong[0] += L.n
        tong[1] += len(L.tris)
        than.append(slot)

    def gan_gai(g):
        """một gai của mào: ô cứng 4 đỉnh; mọi đỉnh bám da đầu theo trọng số của da NGAY CHỖ GỐC GAI (đi theo da, không trượt)."""
        t = g[0]
        pm = os.path.join(BT.MANH, "part", t + ".png")
        im_, m_, V, uv = BT.o_gai(t)
        if os.path.exists(pm):
            gim = Image.open(pm).convert("RGBA").resize((m_.shape[1], m_.shape[0]), Image.LANCZOS)
        else:
            gim = Image.fromarray(np.dstack([im_, m_.astype(np.uint8) * 255]), "RGBA")
            tam.append(t)
        gim = gim.convert("RGBa").resize((max(2, round(gim.width / BT.Z * 2 * PXU)), max(2, round(gim.height / BT.Z * 2 * PXU))), Image.LANCZOS).convert("RGBA")
        sk.anh(t, anh.loang_mau(gim))
        im = sk.images[t]
        L = luoi.Luoi(np.array([[0, 0], [im.width, 0], [im.width, im.height], [0, im.height]], float), np.array([[0, 1, 2], [0, 2, 3]]), 4, 4,
                      im.width, im.height, ten=t)
        Vr = V * KG
        ws = {ten[k]: w for k, w in BT.trong_so_da("P_tou", g[1]).items() if w > 0.01 and ten[k] in sk.bi}
        tot = sum(ws.values())
        sk.slot(t, "move", t)
        sk.luoi_gan(t, t, L, trongso.cung(4, "move"), the_gioi=Vr * LAT)
        sk.atts[t][t]["verts"] = [[(n, *[float(v) for v in (np.linalg.inv(Wc[n]) @ np.array([p_[0], p_[1], 1.0]))[:2]], w / tot) for n, w in ws.items()]
                                  for p_ in Vr]
        tong[0] += 4
        tong[1] += 2
        than.append(t)

    for a in sorted([x for x in D["atts"] if x["cur"] and not BT.BO(x["att"])], key=lambda x: x["order"]):
        if a["att"] == "P_tou":
            for g in BT.GAI:                     # mào gai: vẽ SAU đầu
                gan_gai(g)
        if a["att"] == "P_yanjing1":
            Vm = np.array(a["xy"], float).reshape(-1, 2)
            to_ = lambda h: (lambda q: q.mean(0) + (q - q.mean(0)) * MAT_TI)(np.array(by[h]["xy"], float).reshape(-1, 2))      # noqa: E731
            gan("mat", "P_yanjing1", V=Vm.mean(0) + (Vm - Vm.mean(0)) * MAT_TI)
            gan("mat_lim", "P_yanjing2", an=True, V=to_("P_yanjing2"))
            gan("mat_nham", "P_yanjing 3", an=True, V=to_("P_yanjing 3"))
        else:
            gan(SLOT[a["att"]], a["att"])
        if a["att"] == "P_yanjing1":
            if BT.MAT_XA:                        # mắt xa (bản 2 lượt đầu; đã bỏ: con gốc nhìn nghiêng, chỉ lộ một mắt)
                Vx = BT.mat_xa(a)
                gan("mat2", "P_yanjing1", V=Vx, anh_co="mat")
                gan("mat2_lim", "P_yanjing2", an=True, V=Vx, anh_co="mat_lim")
                gan("mat2_nham", "P_yanjing 3", an=True, V=Vx, anh_co="mat_nham")
    print(f"{len(sk.bones)} xương, {len(than)} slot thân, {tong[0]} đỉnh, {tong[1]} tam giác" + (f"; DA TẠM {len(tam)} part" if tam else ""))

    # mặt nạ cắt của appear: giữ phần TRÊN mặt đất + lòng hố. Đa giác phải LỒI: đáy là đoạn giữa của nửa dưới elip miệng hố (|x| ≤ 0,6 a),
    # hai bên đi tiếp theo tiếp tuyến ra xa (mặt đất quanh hố vẫn thấy được: ngọn vòi úp xuống mép hố), rồi vách dựng đứng.
    # Hình gốc đúng cỡ nằm trong hệ xương cat_x; dáng gốc của xương đó nằm sâu CAT_SAU và phóng CAT_TI lần (không cắt gì); appear thu về.
    a_, b_ = hj["a"] * hs, hj["b"] * hs
    th0 = math.acos(0.6)
    cung_ = [(a_ * math.cos(th), b_ * math.sin(th)) for th in np.linspace(math.pi + th0, 2 * math.pi - th0, 11)]
    doc = (b_ / a_) * (0.6 / 0.8)
    XW, CAO = 1400.0, 3000.0
    yl = cung_[-1][1] + doc * (XW - cung_[-1][0])
    da_giac = [(-XW, CAO), (-XW, yl)] + cung_ + [(XW, yl), (XW, CAO)]
    if CO_HO:
        sk.cat("cat", than[-1], [(x * CAT_TI, HO_Y - CAT_SAU + y * CAT_TI) for x, y in da_giac])
        # hố đất, lớp trước: trên thân
        d_tr = anh_ho("ho_truoc")
        sk.slot("ho_truoc", "ho", "ho_truoc", an=True)
        sk.manh("ho_truoc", "ho_truoc", d_tr)

    # xương miệng (chỗ phụt bóng mực): dưới mắt, phía trước mặt; theo hệ xương thân bone3 ở dáng gốc của họ
    eye = np.array(by["P_yanjing1"]["xy"], float).reshape(-1, 2).mean(0) * KG
    # con gốc không có mồm: bóng mực phụt ra từ dưới mép trước của đầu, sau xúc tu trước (chỗ phễu của bạch tuộc thật, khuất)
    lp = np.linalg.solve(Wc["bone3"], np.array([330.0 * KG, 250.0 * KG, 1.0]))
    sk.xuong("mieng", "bone3", float(lp[0]), float(lp[1]))

    # bạch tuộc con: xương far (chỗ đối thủ) và fly_c<i> (game dời theo quãng), mỗi con một xương con c<i> (nhún, xoay, nảy)
    sk.xuong("far", "root", FAR[0], FAR[1])
    gc, con_tam = anh_con()
    kc = CON_CAO * 1.2 / gc.height               # đơn vị rig mỗi pixel ảnh con → vào atlas 1,2 px mỗi đơn vị
    gc = anh.loang_mau(gc.convert("RGBa").resize((max(2, round(gc.width * kc * 1.2)), max(2, round(gc.height * kc * 1.2))), Image.LANCZOS).convert("RGBA"))
    sk.anh("con", gc)
    for i, (x, y, s) in enumerate([] if NHE else CON[:SO_CON]):
        sk.xuong(f"fly_c{i}", "root", x, y)
        sk.xuong(f"c{i}", f"fly_c{i}", 0.0, 0.0)
        sk.slot(f"con{i}", f"c{i}", "con", an=True)
        sk.manh(f"con{i}", "con", Dat(x, y, neo=(0.5, 1.0), ti=s / 1.2))
    for e, m in (("trung", "khung đòn trúng"), ("phun", "phụt bóng mực (VFX)"), ("trieu_hoi", "một bạch tuộc con hiện ra"),
                 ("lenh", "hai vòi bổ xuống: bạch tuộc con xông lên"), ("ho_mo", "hố đất mở"), ("bam_dat", "ngọn các xúc tu đập xuống đất quanh miệng hố"), ("keo_len", "bắt đầu kéo thân lên"),
                 ("cham_dat", "thân rơi về chỗ")):
        sk.su_kien(e, m)
    if voi_tam:
        tam.append("voi")
    return sk, dict(scan=scan, IB=IB, ten=ten, slots=[s["name"] for s in I["slots"]], than=than, tam=tam, con_tam=con_tam)


def chuyen_dong(sk, info):
    """{clip: (dài giây, {xương: mảng (số khung, 5) = xoay độ, dời x, y (đơn vị rig của mình), tỉ lệ x, y nhân}, tên hình mắt từng
    khung)}: lệch của biến đổi RIÊNG đã áp (runtime Spine) so với dáng gốc."""
    S = json.load(open(os.path.join(info["scan"], "sample_dk.json"), encoding="utf-8"))
    S.update(json.load(open(os.path.join(info["scan"], "sample_moi.json"), encoding="utf-8")))
    IB, ten = info["IB"], info["ten"]
    ids = [i for i, n in enumerate(ten) if n in sk.bi and n != "root"]
    im = info["slots"].index("P_yanjing1")
    out = {}
    for clip, v in S.items():
        fr = v["frames"]
        res = {}
        for i in ids:
            b0 = IB[i]
            A = np.array([[F["l"][i][2] - b0["rot"], (F["l"][i][0] - b0["x"]) * KG, (F["l"][i][1] - b0["y"]) * KG,
                           F["l"][i][3] / (b0["sx"] or 1.0), F["l"][i][4] / (b0["sy"] or 1.0)] for F in fr])
            A[:, 0] = np.degrees(np.unwrap(np.radians(A[:, 0])))
            A[:, 0] -= 360.0 * round(A[0, 0] / 360.0)
            # xương đi hết một vòng rồi về dáng nghỉ theo ngả khác (xúc tu của appear vung qua đầu): góc nối liền kết thúc lệch ±360 so
            # với 0, bước hoà cuối clip về idle sẽ quay nó thêm một vòng (xúc tu văng xuống đất trong 0,2 s cuối). Trả lại bội 360 đó
            # bằng một bước nhảy ở lúc cả con còn ẩn (QUAY_AN: giây), hoặc báo để sửa clip
            kq = round(A[-1, 0] / 360.0)
            if kq:
                if clip in QUAY_AN:
                    A[int(QUAY_AN[clip] * 30):, 0] -= 360.0 * kq
                else:
                    print(f'  CHÚ Ý: {clip}/{ten[i]} kết thúc lệch {kq} vòng so với dáng nghỉ')
            if np.abs(A[:, :3]).max() > 1e-3 or np.abs(A[:, 3:] - 1).max() > 1e-4:
                res[ten[i]] = A
        out[clip] = (float(v["dur"]), res, [F["n"][im] or "P_yanjing1" for F in fr])
    return out


def lam_clip(sk, info):
    CD = chuyen_dong(sk, info)
    than = info["than"]

    def dat_dang(P, goc, tau, lap):
        dur, R, mat = CD[goc]
        n = len(mat)
        x = (tau % dur if lap else min(max(tau, 0.0), dur)) * 30.0
        i0 = min(int(x), n - 1)
        i1 = min(i0 + 1, n - 1)
        w = x - i0
        giam = GIAM.get(goc, {})
        for b, A in R.items():
            v = A[i0] * (1 - w) + A[i1] * w
            if b in giam:
                v = v.copy()
                v[0] *= giam[b]
            if abs(v[0]) > 1e-4:
                P.rot(b, float(v[0]))
            if abs(v[1]) > 1e-4 or abs(v[2]) > 1e-4:
                P.move(b, float(v[1]), float(v[2]))
            if abs(v[3] - 1) > 1e-5 or abs(v[4] - 1) > 1e-5:
                P.scale(b, float(v[3]), float(v[4]))
        for h, sl in MAT.items():
            P.alpha[sl] = 1.0 if mat[i0] == h else 0.0
            if BT.MAT_XA:
                P.alpha[sl.replace("mat", "mat2", 1)] = P.alpha[sl]

    em, cung, ra = BC.em, BC.cung, BC.ra

    truoc_goc = {}

    def tay_chong(t, P):
        """hai tay chống của appear: mỗi tay là một dải lưới chạy dọc đường cong bậc ba từ gốc tay (theo thân) tới ngọn. Ngọn: vươn lên
        khỏi hố → ngoe nguẩy → lấy đà → VUNG ĐẬP xuống chỗ bám → BÁM YÊN (đoạn ngọn nằm bẹt trên đất, chĩa ra ngoài) trong lúc thân
        được đẩy lên → thân đáp xong thì nhấc ngọn, cả tay TRƯỢT vào sau đầu (gốc tay trượt sang bên kia đầu, ngọn khuất sau cùng). Chiều dài đường cong đổi thì dải giãn / co đều (dời xương con dọc trục cha); lúc thân
        đã lên cao, tay không bị dồn ngắn lại mà vồng cao lên như khuỷu chống."""
        if t <= 1e-9:
            truoc_goc.clear()
        W = sk.the_gioi(P)
        a_cha = math.degrees(math.atan2(W["bone3"][1, 0], W["bone3"][0, 0]))
        B3, M3 = W["bone3"][:2, 2], W["bone3"][:2, :2]
        for ten_, _, A, G, phia, tre in VOI:
            names = [f"{ten_}{i}" for i in range(VOI_DOT)]
            het = BC.P_THU_HET + tre
            P.alpha[ten_] = (1.0 if t >= BC.P_VOI - 0.06 else 0.0) * (1.0 - em((t - het + 0.05) / 0.05))
            P0 = W[names[0]][:2, 2].copy()
            A_, G_ = np.array(A) * KG, np.array(G) * KG
            # THU TAY: u3 nhấc ngọn khỏi đất (cong lên, vào trong); u4 cả tay trượt vào sau đầu (gốc tay trượt sang bên kia đầu)
            u3 = em((t - BC.P_THU - tre) / 0.22)
            u4 = em((t - BC.P_THU - 0.14 - tre) / (het - BC.P_THU - 0.14 - tre))
            R1, T1 = B3 + np.array(VOI_TRONG[ten_][0]), B3 + np.array(VOI_TRONG[ten_][1])
            if u4 > 0:
                P0m = P0 + (R1 - P0) * u4
                dl_ = np.linalg.solve(M3, P0m - P0)
                P.move(names[0], float(dl_[0]), float(dl_[1]))
                P0 = P0m
            S0 = np.array([A_[0] * 0.55, -140.0 * KG])                              # ngọn lúc còn trong lòng hố
            len_ = ra((t - BC.P_VOI - tre) / 0.42, 2.0)
            ph = 2 * math.pi * 2.1 * t + 40.0 * tre
            lac = cung(t, BC.P_VOI + 0.2, 0.6, BC.P_VUNG, BC.P_VUNG + 0.06)
            Aw = A_ + np.array([34.0 * math.sin(ph), 22.0 * math.sin(1.7 * ph + 1.0)]) * KG * lac
            Aw = Aw + np.array([-phia * 80.0, 55.0]) * KG * cung(t, BC.P_VUNG - 0.16, BC.P_VUNG - 0.02, BC.P_VUNG, BC.P_VUNG + 0.08)   # lấy đà
            T = S0 + (Aw - S0) * len_
            u2 = BC.vao((t - BC.P_VUNG - 0.3 * tre) / (BC.P_BAM - BC.P_VUNG), 2.4)   # vung đập xuống: chậm rồi nhanh
            if u2 > 0:
                T = Aw + (G_ - Aw) * u2 + np.array([phia * 90.0, 150.0]) * KG * math.sin(math.pi * u2) * (1 - u2)
            if u3 > 0:
                T = T + np.array([-phia * 85.0, 190.0]) * KG * u3
            if u4 > 0:
                T = T + (T1 - T) * u4
            g_ = em(u2)
            v = T - P0
            n_ = np.array([-v[1], v[0]]) / max(1e-6, float(np.hypot(*v))) * phia      # pháp tuyến chĩa ra NGOÀI
            song = 85.0 * KG * math.sin(ph * 1.2) * lac                              # lượn chữ S lúc ngoe nguẩy
            K1k = P0 + v * 0.33 - n_ * (30.0 * KG + song)
            K2k = P0 + v * 0.66 - n_ * (18.0 * KG - song)
            ra_ngoai = np.array([phia * 78.0 * KG, 0.0]) * (1.0 - u3)                # đoạn ngọn nằm bẹt, chĩa ra ngoài (nhấc lên thì hết bẹt)
            K1c, K2c = P0 + v * 0.33 + np.array([0.0, 26.0]), P0 + v * 0.66 + np.array([0.0, 26.0])   # lúc đã vào sau đầu: cung thoải

            def duong(cao):
                K1b = np.array([P0[0] + (T[0] - P0[0]) * 0.42, max(P0[1], T[1]) + cao + 0.5 * max(0.0, T[1] - P0[1])])
                K2b = T + np.array([-phia * 95.0 * KG, 0.62 * cao]) * (1.0 - 0.6 * u3)
                K1, K2, E = K1k + (K1b - K1k) * g_, K2k + (K2b - K2k) * g_, T + ra_ngoai * g_
                K1, K2 = K1 + (K1c - K1) * u4, K2 + (K2c - K2) * u4
                tt = np.linspace(0, 1, 140)[:, None]
                C = (1 - tt) ** 3 * P0 + 3 * (1 - tt) ** 2 * tt * K1 + 3 * (1 - tt) * tt ** 2 * K2 + tt ** 3 * E
                return C, np.r_[0, np.cumsum(np.hypot(*np.diff(C, axis=0).T))]

            cao = 150.0
            C, dl = duong(cao)
            if g_ > 0.5 and u4 < 0.6:                 # đã bám / đang nhấc: tay ngắn hơn 0,92 chiều dài tự nhiên thì vồng cao thêm cho đủ dài
                lo, hi = cao, 520.0
                for _ in range(10):
                    mid = 0.5 * (lo + hi)
                    if duong(mid)[1][-1] < 0.92 * VOI_DAI:
                        lo = mid
                    else:
                        hi = mid
                if duong(cao)[1][-1] < 0.92 * VOI_DAI:
                    C2, dl2 = duong(hi)
                    k_ = 1.0 - em((u4 - 0.2) / 0.4)   # vào sau đầu thì thôi vồng, để tay nằm gọn
                    C = C + (C2 - C) * k_
                    dl = np.r_[0, np.cumsum(np.hypot(*np.diff(C, axis=0).T))]
            f = np.linspace(0, dl[-1], VOI_DOT + 1)
            J = np.stack([np.interp(f, dl, C[:, 0]), np.interp(f, dl, C[:, 1])], 1)
            prev = a_cha
            for i, nm in enumerate(names):
                d = J[i + 1] - J[i]
                th = math.degrees(math.atan2(d[1], d[0]))
                b = sk.bones[sk.bi[nm]]
                dr = th - prev - b["rot"]
                g0 = truoc_goc.get(nm, 0.0)
                dr = g0 + ((dr - g0 + 180.0) % 360.0 - 180.0)          # liền với khung trước (không nhảy 360)
                truoc_goc[nm] = dr
                P.rot(nm, dr)
                if i + 1 < VOI_DOT:
                    c = sk.bones[sk.bi[names[i + 1]]]
                    P.move(names[i + 1], float(np.hypot(*d)) - c["x"], -c["y"])
                prev = th

    def appear(t, P):
        dat_dang(P, "bt_appear", t, False)
        tay_chong(t, P)
        # thân ẩn hẳn tới khi vòi sắp thò lên (khung đầu trống); mặt nạ cắt bật từ đầu tới lúc thân vọt lên cao nhất
        if t < BC.P_VOI - 0.08:
            for sl in than:
                P.alpha[sl] = 0.0
        if t < BC.P_LEN - 0.02:
            P.move("cat_x", 0.0, CAT_SAU)
            P.scale("cat_x", 1.0 / CAT_TI)
        # hố: đùn lên 0 → 0,28 (nảy quá đà), rung lúc vòi bổ xuống và lúc thân vọt lên, sụp + mờ khi thân đã ra
        mo = ra(t / 0.26, 2.6)
        nay = 1.0 + 0.16 * math.exp(-t * 9.0) * math.sin(t * 26.0) if t < 0.6 else 1.0
        sup = em((t - BC.P_LEN) / 0.34)
        sx = (0.25 + 0.75 * mo) * (1.0 - 0.12 * sup)
        sy = (0.05 + 0.95 * mo) * nay * (1.0 - 0.75 * sup)
        r = 5.0 * cung(t, BC.P_BAM - 0.01, BC.P_BAM + 0.03, BC.P_BAM + 0.08, BC.P_BAM + 0.22) + 2.5 * cung(t, BC.P_KEO, BC.P_KEO + 0.06, BC.P_LEN - 0.1, BC.P_LEN)
        P.scale("ho", sx, sy)
        P.move("ho", r * math.sin(t * 71.0), r * 0.6 * math.sin(t * 93.0 + 1.0))
        a = min(1.0, t / 0.08) * (1.0 - em((t - BC.P_LEN - 0.08) / 0.28))
        P.alpha["ho_sau"] = a
        P.alpha["ho_truoc"] = a

    # chiêu cuối: bạch tuộc con. Hiện (bật khỏi đất) ở S_GOI[i], nhấp nhổm chờ, sau lệnh S_LENH thì bò (nhích từng nhịp) tới sát
    # đối thủ rồi nhảy bổ vào (xương fly_c<i> đi từ chỗ xuất phát tới far; game co quãng theo chỗ đối thủ thật)
    # mốc từng con hiện ra: rải đều từ 0,58 tới 1,58 (trước lệnh S_LENH), ít con thì thưa hơn
    goi = [round(0.58 + (1.0 if SO_CON > 4 else 0.6) * i / max(1, SO_CON - 1), 3) for i in range(SO_CON)]
    xuat_phat = [BC.S_LENH + 0.05 + 0.07 * i for i in range(SO_CON)]
    trung = [x + BO + NHAY for x in xuat_phat]

    def skill(t, P):
        dat_dang(P, "bt_skill", t, False)
        for i, (x0, y0, s) in enumerate(CON[:SO_CON]):
            sl, fb, cb = f"con{i}", f"fly_c{i}", f"c{i}"
            if t < goi[i] or t > trung[i] + 0.16:
                P.alpha[sl] = 0.0
                continue
            u = t - goi[i]
            P.alpha[sl] = min(1.0, u / 0.05) * (1.0 - em((t - trung[i]) / 0.14))
            hien = ra(u / 0.22, 2.4) * (1.0 + 0.35 * math.exp(-u * 10.0) * math.sin(u * 30.0))
            sx = sy = hien
            dy = 26.0 * math.sin(math.pi * min(1.0, u / 0.26)) * (1.0 if u < 0.26 else 0.0)        # bật khỏi đất
            xa, cao, goc = 0.0, 0.0, 0.0
            if t < xuat_phat[i]:
                k = math.sin(2 * math.pi * 2.6 * u + i)                                           # nhấp nhổm chờ lệnh
                sx *= 1.0 + 0.06 * k
                sy *= 1.0 - 0.06 * k
            elif t < xuat_phat[i] + BO:
                v = (t - xuat_phat[i]) / BO                                                        # bò: ba nhịp nhích
                nh = v * 3.0
                j, f = int(min(2.999, nh)), min(2.999, nh) % 1.0
                xa = 0.86 * (j + em(min(1.0, f / 0.6))) / 3.0
                k = math.sin(math.pi * f)
                sx *= 1.0 + 0.26 * k
                sy *= 1.0 - 0.2 * k
                cao = 5.0 * k
            else:
                v = min(1.0, (t - xuat_phat[i] - BO) / NHAY)                                       # nhảy bổ vào người đối thủ
                xa = 0.86 + 0.14 * v
                cao = (FAR[1] - y0) * v + 90.0 * math.sin(math.pi * v) * (1.0 - 0.45 * v)
                goc = -40.0 * math.sin(math.pi * min(1.0, v * 1.15))
                sx *= 1.0 + 0.22 * math.sin(math.pi * v)
                sy *= 1.0 - 0.12 * math.sin(math.pi * v)
                if t > trung[i]:
                    b = (t - trung[i]) / 0.14
                    sx *= 1.0 + 0.5 * b
                    sy *= 1.0 - 0.45 * b
            P.move(fb, (FAR[0] - x0) * xa, 0.0)
            P.move(cb, 0.0, dy + cao)
            P.rot(cb, goc)
            P.scale(cb, sx, sy)

    def attack(t, P):
        dat_dang(P, "bt_attack", t, False)
        # trượt nhẹ cả thân tới lúc đấm (game đo cú lao trên xương move)
        P.move("move", 46.0 * LAT_X * cung(t, BC.A_DA - 0.02, BC.A_TRUNG, BC.A_GIU, 0.9), 0.0)

    # APPEAR của dạng không có hố (dạng 1): NHẢY VÀO từ phía sau (bên trái), một cú nhảy vòng cung, đáp xuống bẹp người rồi nảy nhẹ một
    # nhịp và nhún tắt dần. Dời trên xương move (game đo cú lao ở đó); khung đầu trống (hiện dần 0,12 s). Khung sticker rộng ~3,4 lần
    # chiều cao nên chỉ dời tối đa ~0,8 chiều cao. Xúc tu bay tạt về sau lúc ở trên không, đáp thì văng tới rồi đung đưa tắt dần.
    N_DAT, N_NAY, N_DUR = 0.46, 0.80, 1.25
    HN = soi.chieu_cao(soi.Ve(sk), hoat.nuong(sk, Clip("_", 0.1, lambda t, P: dat_dang(P, "idle_01", 0.0, False)))[0])

    def nhay_vao(t, P):
        dat_dang(P, "idle_01", 0.0, False)
        a = float(np.clip(t / 0.12, 0.0, 1.0))
        for sl in than:
            if sk.slots[sk.si[sl]]["alpha"] > 0 or sl == "mat":
                P.alpha[sl] = a * P.alpha.get(sl, 1.0)
        if t < N_DAT:                                   # cú nhảy chính: vào từ −0,8 H, đỉnh cao 0,5 H
            u = t / N_DAT
            x = -0.8 * HN * (1.0 - u) ** 1.15
            y = 0.5 * HN * 4.0 * u * (1.0 - u) + 0.12 * HN * (1.0 - u)
            sx, sy, tat = 0.94, 1.08, 1.0               # đang bay: người hơi thuôn dài, xúc tu tạt về sau
        elif t < N_NAY:                                 # đáp: bẹp → nảy nhẹ một nhịp
            u = (t - N_DAT) / (N_NAY - N_DAT)
            x = 0.0
            y = 0.07 * HN * math.sin(math.pi * max(0.0, (u - 0.28) / 0.72)) if u > 0.28 else 0.0
            bep = math.exp(-u * 5.0)
            sx, sy, tat = 1.0 + 0.2 * bep, 1.0 - 0.22 * bep, -0.9 * math.exp(-u * 3.0)
        else:                                           # nhún tắt dần về dáng nghỉ
            r = t - N_NAY
            x, y = 0.0, 0.0
            k = math.exp(-r * 8.0) * math.cos(r * 22.0)
            sx, sy, tat = 1.0 + 0.07 * k, 1.0 - 0.08 * k, 0.35 * math.exp(-r * 6.0) * math.sin(r * 16.0)
        P.move("move", x, y)
        P.scale("move", sx, sy)
        P.rot("bone3", -7.0 * (1.0 if t < N_DAT else 0.0) * math.sin(math.pi * min(1.0, t / N_DAT)))      # chúi tới lúc bay
        for j, ch in enumerate(BC.NGON):                # xúc tu rủ xuống: xoay âm = ngọn tạt về phía sau (−x)
            for q, b in enumerate(ch):
                P.rot(b, -(9.0 + 6.0 * q) * tat)
        for ch in (BC.T1[2:], BC.T2[2:], BC.T6[2:]):
            for q, b in enumerate(ch):
                P.rot(b, -(6.0 + 4.0 * q) * tat)
        nham = N_DAT - 0.02 < t < N_DAT + 0.12          # chớp mắt lúc đáp
        P.alpha["mat"], P.alpha["mat_nham"], P.alpha["mat_lim"] = (0.0 if nham else a), (1.0 if nham else 0.0), 0.0

    ev = BC.SU_KIEN
    ev_skill = ([(g, "trieu_hoi", str(i)) for i, g in enumerate(goi)] + [e for e in ev["bt_skill"] if e[1] != "trieu_hoi"]
                + [(round(x, 3), "trung", str(i)) for i, x in enumerate(trung)])
    out = []
    for ten_, goc, lap in CLIPS:
        dur = CD[goc][0]
        if ten_ == "die":
            def fn(t, P, goc=goc, dur=dur):
                dat_dang(P, goc, t, False)
                a = float(np.clip(1.0 - (t - dur) / (TAN - 0.1), 0.0, 1.0))
                for sl in than:
                    if sk.slots[sk.si[sl]]["alpha"] > 0 or sl.startswith("mat"):
                        P.alpha[sl] = a * P.alpha.get(sl, 1.0)
            out.append(Clip(ten_, dur + TAN, fn))
        elif ten_ == "appear" and CO_HO:
            out.append(Clip(ten_, dur, appear, ev=ev[goc]))
        elif ten_ == "appear":
            out.append(Clip(ten_, N_DUR, nhay_vao, ev=[(N_DAT, "cham_dat", "")]))
        elif ten_ == "skill":
            out.append(Clip(ten_, max(dur, trung[-1] + 0.25), skill, ev=ev_skill, trung=trung[0]))
        elif ten_ == "attack":
            out.append(Clip(ten_, dur, attack, ev=ev[goc]))
        else:
            out.append(Clip(ten_, dur, (lambda t, P, goc=goc, lap=lap: dat_dang(P, goc, t, lap)), loop=lap, ev=ev.get(goc, [])))
    return out


def tien_hoa(skA, clipsA):
    """clip `evolve` của dạng 1: gộp bản NHẸ của dạng 2 vào rig dạng 1 (quai/tienhoa.py: xương dạng 2 mang tiền tố n_, slot ẩn mặc
    định). Bản nhẹ dựng ở tiến trình con (BT_DANG=2 BT_NHE=1: cấu hình dạng đọc lúc nạp module) rồi nạp lại bằng pickle. Con non
    gồng: thu người, đầu phồng dần, rung; đổi dạng ~1,2 s; dạng 2 hiện ra lớn dần, phồng đầu gầm rồi hoà về đúng khung 0 idle của nó."""
    import pickle
    import subprocess
    from quai import tienhoa
    f = os.path.join(RA, "_dang2_nhe.pkl")
    subprocess.check_call([sys.executable, "-I", os.path.abspath(__file__), "nhe", f], env=dict(os.environ, BT_DANG="2", BT_NHE="1"))
    skB, frB0, hB = pickle.load(open(f, "rb"))
    os.remove(f)
    idleA = [c for c in clipsA if c.ten == "idle"][0]
    hA = soi.chieu_cao(soi.Ve(skA), hoat.nuong(skA, idleA)[0]) * CAO_KHAI      # chiều cao KHAI của dạng 1 (game co theo đó)
    M = tienhoa.gop(skA, skB)

    def gong(t, P):
        idleA.fn(0.0, P)
        g = hoat.cv(t, [(0, 0), (0.3, -0.3), (0.6, 1, "out"), (1.3, 1.15)])
        r = hoat.rung(t, 0.45, 1.35, moi=1)
        gp = max(g, 0.0)
        P.move("bone3", 0.0, -9.0 * gp)
        P.rot("bone3", 3.0 * g + 0.7 * r)
        P.scale("bone5", 1.0 + 0.07 * gp, 1.0 + 0.10 * gp)
        for b in ("bone18", "bone21", "bone24", "bone14", "bone9", "bone29"):
            P.rot(b, 8.0 * gp + 1.5 * r)

    def gam(t, P, fl):
        r = hoat.rung(t, 2.0, 2.4, moi=1)
        P.rot("n_bone3", -4.0 * fl + 0.8 * r * fl)
        P.scale("n_bone5", 1.0 + 0.08 * fl, 1.0 + 0.10 * fl)
        for b in ("n_bone14", "n_bone29"):
            P.rot(b, 14.0 * fl)

    ev = tienhoa.clip_tien_hoa(M, skA, skB, frB0, tiB=hA / hB, fnA=gong, fnB=gam, mem=[])
    print(f"  evolve: gộp dạng 2 bản nhẹ (ảnh {0.36}); cao khai dạng 1 {hA:.0f}, dạng 2 {hB:.0f} → dạng 2 phóng {hA / hB:.3f} trong rig gộp")
    return M, clipsA + [ev]


def main(a):
    sk, info = dung()
    clips = lam_clip(sk, info)
    if a and a[0] == "nhe":                    # bản nhẹ của dạng này cho clip evolve của dạng trước → pickle (sk, khung 0 idle, chiều cao)
        import pickle
        fr0 = hoat.nuong(sk, [c for c in clips if c.ten == "idle"][0])[0]
        pickle.dump((sk, fr0, soi.chieu_cao(soi.Ve(sk), fr0)), open(a[1], "wb"))
        return
    if BT.K == 1 and not (a and a[0] == "bo_cuc"):
        sk, clips = tien_hoa(sk, clips)
    if a and a[0] == "bo_cuc":                 # hình bố cục 1536x1024 nền trắng (khung 0 idle của rig dạng này) cho prompt concept → a[1]
        fr = hoat.nuong(sk, [x for x in clips if x.ten == "idle"][0])
        ve = soi.Ve(sk)
        Bx = soi._union([ve.bao(fr[0])], 0.03)
        sc = min(1536 * 0.62 / (Bx[2] - Bx[0]), 1024 * 0.74 / (Bx[3] - Bx[1]))
        im = ve.ve(fr[0], Bx, sc, bg=(255, 255, 255), ss=2).convert("RGB")
        out = Image.new("RGB", (1536, 1024), (255, 255, 255))
        out.paste(im, ((1536 - im.width) // 2, (1024 - im.height) // 2))
        os.makedirs(os.path.dirname(a[1]), exist_ok=True)
        out.save(a[1])
        print(a[1], im.size)
        return
    if a and a[0] == "soi":                    # soi <clip> <giây,giây,...> [tỉ lệ]: khung lớn nền xám → rig/soi_<clip>.png
        c = [x for x in clips if x.ten == a[1]][0]
        fr = hoat.nuong(sk, c)
        ts = [float(x) for x in a[2].split(",")]
        ve = soi.Ve(sk)
        Ps = [fr[min(len(fr) - 1, int(round(t * 30)))] for t in ts]
        Bx = soi._union([ve.bao(P) for P in Ps], 0.04)
        sc = float(a[3]) if len(a) > 3 else 1.0
        ims = [ve.ve(P, Bx, sc, bg=(150, 150, 150), ss=2).convert("RGB") for P in Ps]
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
    cao = None
    if CAO_KHAI != 1.0:                        # con non vẽ nhỏ hơn trên sân: khai chiều cao lớn hơn chiều cao đo ở khung 0 idle
        fr0 = hoat.nuong(sk, [c for c in clips if c.ten == "idle"][0])[0]
        cao = soi.chieu_cao(soi.Ve(sk), fr0, ()) * CAO_KHAI
    xuat.xuat_het(sk, clips, RA, TEN, f"Bạch tuộc quái vật (bach_tuoc) dạng {BT.K}" + (" — DA TẠM" if info["tam"] else ""), dang=BT.K, so_dang=2,
                  dung_yen=("cast", "skill"), far=("skill",), ma_goc=None, tol={"rotate": 0.05, "translate": 0.12, "scale": 0.001},
                  khop_idle=0.2, dich_mb=0.45, tran_mb=0.5, cao=cao)

if __name__ == "__main__":
    main(sys.argv[1:])
