# -*- coding: utf-8 -*-
"""Đổi HÌNH suất 5 đảo Kim (id `khien_bac`, ải 20 "Gác Chuông Đồng") sang quỷ xích (mã làm việc quy_xich, rig monster_3408; dạng 1 non
→ `quy_xich_1`, dạng 2 giáp kín → `quy_xich_2`; ghi chú ArtGen/Spine/inbox/quy_xich_ghichu.md). Người dùng 2026-11-16: dòng 2 dạng,
"ổn rồi, cho vào game".

Giữ id tướng, id thẻ, chỉ số, hiệu ứng thẻ, SỐ DẠNG (2 → 2): bản lưu và golden không đổi. Đổi:
    tên     Khiên Bạc -> Quỷ Xích; danh hiệu "Quỷ béo móc xích lửa"; dòng "Dòng Quỷ Xích"
    dạng    [Khiên Sắt Tí Hon, Vệ Sĩ Khiên Bạc] (khien_bac_1, khien_bac_2) -> [Quỷ Xích Nhi (quy_xich_1), Quỷ Xích (quy_xich_2)]
    thẻ     Khiên Đập -> Ném Móc Xích (shield -> claw); Thành Lũy Bạc -> Xích Lửa Thiêu (helmet -> flame); Khiên Phản -> Bụng Thép (mirror -> fist)
Tên do Claude đặt (người dùng chưa đặt), người dùng có thể đổi. Không đè, không xoá thư mục Resources/khien_bac_* cũ.

Sửa `Assets/02 Data/Json/heroes.json`, `cards.json` (nguồn). HeroDb.asset, CardDb.asset do menu Unity "PokiClash/Nhập dữ liệu" dựng lại, rồi
"PokiClash/Tướng/Gắn dạng .atomik vào prefab tướng". Chạy lại không đổi gì thêm.

    py -3 -I ArtGen/Spine/quai/doi_quy_xich.py [--kiem]   heroes.json + cards.json
    py -3 -I ArtGen/Spine/quai/doi_quy_xich.py th          gộp bản nhẹ dạng 2 + clip `evolve` vào rig dạng 1 → inbox/quy_xich_non/rig/quy_xich_non_th.atomik
    py -3 -I ArtGen/Spine/quai/doi_quy_xich.py chep        chép rig (dạng 1 bản đã gộp tiến hoá) + chân dung + ảnh mắt xích (vòng trói, HatXich.cs)
                                                           vào Resources/quy_xich_1/, Resources/quy_xich_2/
"""
import os
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
SPINE = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, SPINE)
import doi_phap_lua as D  # noqa: E402  (dùng lại khoi_tuong, dat_dang, heroes, cards, chep)

D.ID = "khien_bac"
TEN, TEN_NON = "Quỷ Xích", "Quỷ Xích Nhi"
CO_1, CO_2 = 0.92, 1.1
D.KHAC = [("name", "Khiên Bạc", TEN), ("title", "Vệ sĩ khiên bạc", "Quỷ béo móc xích lửa"), ("line", "Dòng Khiên Bạc", "Dòng Quỷ Xích")]
D.THE = {"khien_bac_skill": ("Khiên Đập", "Ném Móc Xích", "shield", "claw"),
         "khien_bac_ult": ("Thành Lũy Bạc", "Xích Lửa Thiêu", "helmet", "flame"),
         "khien_bac_pas": ("Khiên Phản", "Bụng Thép", "mirror", "fist")}
INBOX = os.path.normpath(D.INBOX)
RIG1 = os.path.join(INBOX, "quy_xich_non", "rig")
RIG2 = os.path.join(INBOX, "quy_xich_1", "rig")


def th():
    """gộp dạng 2 (bản nhẹ) vào rig dạng 1 + clip `evolve` (như doi_tinh_sat.th): dạng 1 gồng rung rồi mờ, dạng 2 hiện, lớn dần, dừng đúng
    khung 0 idle của nó. Slot ẩn sẵn của hai rig (xích dài, móc thứ hai, xích bay, bản _sau) giữ ẩn suốt clip."""
    sys.path.insert(0, os.path.join(SPINE, "mo_xe"))
    import atomik_dang as A
    J, img, ver = A.load(os.path.join(RIG1, "quy_xich_non.atomik"))
    JB, imgB, _ = A.load(os.path.join(RIG2, "quy_xich.atomik"))
    an_A = {i for i, s in enumerate(J["slots"]) if s.get("fade", 0) >= 1}
    an_B = {i for i, s in enumerate(JB["slots"]) if s.get("fade", 0) >= 1}
    nA_s = len(J["slots"])
    hA, hB = J["game"]["height"], JB["game"]["height"]
    k_B = CO_2 / CO_1 * hA / hB
    img = A.gop_tien_hoa(J, img, JB, imgB, k_B, than_A=A.bi(J)["bone3"])
    ev = J["anims"][-1]
    n = 0
    for x in ev["sa"]:
        if x["slot"] in an_A or (x["slot"] - nA_s) in an_B:
            x["keys"] = A.rot_keys([(0, 0), (ev["dur"], 0)])
            n += 1
    p = os.path.join(RIG1, "quy_xich_non_th.atomik")
    kq = A.save(p, J, img, ver)
    print(f"{p}: {os.path.getsize(p) // 1024} KB; trong rig gộp dạng 2 × {k_B:.3f}; {n} slot ẩn giữ ẩn trong evolve; {kq}")
    ci = A.clip(J, "evolve")
    ts = [0.0, 0.5, 0.9, 1.05, 1.2, 1.35, 1.5, 1.8, 2.2, 2.6, 3.0]
    Ps = [A.Pose(J).at(ci, t) for t in ts]
    bs = np.array([A.bounds(P) for P in Ps])
    box = (bs[:, 0].min() - 20, bs[:, 1].min() - 20, bs[:, 2].max() + 20, bs[:, 3].max() + 20)
    ims = [A.render(J, img, A.Pose(J).at(ci, t), box, 0.3, bg=(150, 150, 150)).convert("RGB") for t in ts]
    cot = 6
    out = Image.new("RGB", (cot * ims[0].width, ((len(ims) + cot - 1) // cot) * ims[0].height), (150, 150, 150))
    for i, im in enumerate(ims):
        out.paste(im, ((i % cot) * im.width, (i // cot) * im.height))
    out.save(os.path.join(RIG1, "khung_evolve.png"))
    print(os.path.join(RIG1, "khung_evolve.png"), out.size)
    ib = A.clip(JB, "idle")
    Pb = A.Pose(JB).at(ib, 0.0)
    Pe = A.Pose(J).at(ci, ev["dur"])
    nb = len(J["bones"]) - len(JB["bones"])
    lech = 0.0
    for i in range(len(JB["bones"])):
        lech = max(lech, abs(Pe.w[nb + i][4] - Pb.w[i][4] * k_B), abs(Pe.w[nb + i][5] - Pb.w[i][5] * k_B))
    print(f"khung cuối evolve so khung 0 idle dạng 2: lệch gốc xương lớn nhất {lech:.3f} đơn vị")


# ảnh mắt xích cho VÒNG TRÓI của chiêu cuối (HatXich.cs nạp Resources.Load<Sprite>("quy_xich_2/quy_xich_2_xich_<vùng>")): đúng ảnh trong atlas rig
XICH = ["W_suolian1", "W_suolian2"]


def anh_xich(ma, rig, ten_rig):
    """chép hai ảnh mắt xích của mình (manh/W_suolian1.png nghiêng, W_suolian2.png thẳng, 1 px / đơn vị rig) làm sprite cho vòng trói.
    (Cắt từ atlas thì vùng xoay 90° và dính mảnh bên cạnh.)"""
    import shutil
    d = os.path.join(D.RES, ma)
    os.makedirs(d, exist_ok=True)
    for v in XICH:
        p = os.path.join(INBOX, "quy_xich_1", "manh", v + ".png")
        q = os.path.join(d, f"{ma}_tt_xich_{v[-1]}.png")       # "_tt_": AolaImport nhập thành sprite (Resources.Load<Sprite>)
        shutil.copyfile(p, q)
        print(f"  {os.path.relpath(q, D.ROOT)}: {Image.open(q).size}")


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if a[:1] == ["th"]:
        th()
    elif a[:1] == ["chep"]:
        D.chep("quy_xich_1", RIG1, "quy_xich_non_th.atomik")
        D.chep("quy_xich_2", RIG2, "quy_xich.atomik")
        anh_xich("quy_xich_2", RIG2, "quy_xich")
    else:
        D.heroes([(TEN_NON, "quy_xich_1", CO_1), (TEN, "quy_xich_2", CO_2)])
        D.cards()
