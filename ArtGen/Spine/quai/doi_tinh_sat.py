# -*- coding: utf-8 -*-
"""Đổi HÌNH suất 1 đảo Kim (id `bo_cap`, ải 1 "Cảng Sắt") sang tinh linh tinh thể sắt (mã làm việc tinh_sat; dạng 1 rig monster_3346 →
`tinh_sat_1`, dạng 2 rig monster_3347 → `tinh_sat_2`; ghi chú ArtGen/Spine/inbox/tinh_sat_ghichu.md). Người dùng 2026-11-16: dòng 2 dạng,
"ổn rồi, cho vào game đi".

Giữ id tướng, id thẻ, chỉ số, hiệu ứng thẻ (không đổi bản lưu). SỐ DẠNG 3 → 2 nên golden roster, sim phải tính lại trong Unity. Đổi:
    tên     Bọ Cạp Đồng -> Thiết Tinh; danh hiệu "Tinh linh tinh thể sắt"; dòng "Dòng Thiết Tinh"
    dạng    [Bọ Cạp Pha Lê, Bọ Cạp Đá Lục, Bọ Cạp Đồng] (bo_cap_1, bo_cap_2, goc_678) -> [Thiết Tinh Nhi (tinh_sat_1), Thiết Tinh (tinh_sat_2)]
    thẻ     Đuôi Pha Lê -> Mưa Tinh Thể (fang -> rock); Kim Châm Cát Đỏ -> Thiết Tinh Dập (crack -> hammer); Vỏ Cát -> Giáp Tinh Thể (shield)
Tên do Claude đặt (người dùng chưa đặt), người dùng có thể đổi. Không đè, không xoá thư mục Resources/bo_cap_* cũ.

Sửa `Assets/02 Data/Json/heroes.json`, `cards.json` (nguồn). HeroDb.asset, CardDb.asset do menu Unity "PokiClash/Nhập dữ liệu" dựng lại, rồi
"PokiClash/Tướng/Gắn dạng .atomik vào prefab tướng", rồi các menu golden. Chạy lại không đổi gì thêm.

    py -3 -I ArtGen/Spine/quai/doi_tinh_sat.py [--kiem]   heroes.json + cards.json
    py -3 -I ArtGen/Spine/quai/doi_tinh_sat.py th          gộp bản nhẹ dạng 2 + clip `evolve` vào rig dạng 1 → inbox/tinh_sat_1/rig/tinh_sat_1_th.atomik
    py -3 -I ArtGen/Spine/quai/doi_tinh_sat.py chep        chép rig (dạng 1 bản đã gộp tiến hoá) + chân dung + ảnh tinh thể bay (HatSat.cs) vào
                                                           Resources/tinh_sat_1/, Resources/tinh_sat_2/
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

D.ID = "bo_cap"
TEN, TEN_NON = "Thiết Tinh", "Thiết Tinh Nhi"
CO_1, CO_2 = 0.88, 1.0
D.KHAC = [("name", "Bọ Cạp Đồng", TEN), ("title", "Đuôi pha lê cát đỏ", "Tinh linh tinh thể sắt"), ("line", "Dòng Bọ Cạp Đồng", "Dòng Thiết Tinh")]
D.THE = {"bo_cap_skill": ("Đuôi Pha Lê", "Mưa Tinh Thể", "fang", "rock"),
         "bo_cap_ult": ("Kim Châm Cát Đỏ", "Thiết Tinh Dập", "crack", "hammer"),
         "bo_cap_pas": ("Vỏ Cát", "Giáp Tinh Thể", "shield", "shield")}
INBOX = os.path.normpath(D.INBOX)
RIG1 = os.path.join(INBOX, "tinh_sat_1", "rig")
RIG2 = os.path.join(INBOX, "tinh_sat_2", "rig")


def th():
    """gộp dạng 2 (bản nhẹ) vào rig dạng 1 + clip `evolve` (như dat_nung_non.py th): dạng 1 gồng rung rồi mờ, dạng 2 hiện, lớn dần, dừng đúng
    khung 0 idle của nó. Slot ẩn sẵn của hai rig (bàn chân rời, tinh thể nhân bản) giữ ẩn suốt clip."""
    sys.path.insert(0, os.path.join(SPINE, "mo_xe"))
    import atomik_dang as A
    src_a = os.path.join(RIG1, "tinh_sat_1.atomik")
    src_b = os.path.join(RIG2, "tinh_sat_2.atomik")
    J, img, ver = A.load(src_a)
    JB, imgB, _ = A.load(src_b)
    an_A = {i for i, s in enumerate(J["slots"]) if s.get("fade", 0) >= 1}
    an_B = {i for i, s in enumerate(JB["slots"]) if s.get("fade", 0) >= 1}
    nA_s = len(J["slots"])
    hA, hB = J["game"]["height"], JB["game"]["height"]
    k_B = CO_2 / CO_1 * hA / hB
    img = A.gop_tien_hoa(J, img, JB, imgB, k_B, than_A=A.bi(J)["all2"])
    ev = J["anims"][-1]
    n = 0
    for x in ev["sa"]:
        if x["slot"] in an_A or (x["slot"] - nA_s) in an_B:
            x["keys"] = A.rot_keys([(0, 0), (ev["dur"], 0)])
            n += 1
    p = os.path.join(RIG1, "tinh_sat_1_th.atomik")
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


# ảnh tinh thể bay của chiêu mana (HatSat.cs nạp bằng Resources.Load<Sprite>("<dạng>/<dạng>_tt_<vùng>"); AolaImport nhập thành sprite): đúng ảnh mảnh trong atlas rig
TT_1 = ["bin1", "bin2", "bin3", "bin6", "bin7", "bin8", "bin9", "tail3"]
TT_2 = ["P_bc_01", "P_bc_02", "P_bc_03", "P_bc_04", "P_bc_05"]


def anh_tt(ma, rig, vung):
    sys.path.insert(0, os.path.join(SPINE, "mo_xe"))
    import atomik_dang as A
    J, img, _ = A.load(os.path.join(rig, ma + ".atomik"))
    d = os.path.join(D.RES, ma)
    os.makedirs(d, exist_ok=True)
    ten_att = [a.get("name") for a in J["atts"]]
    for v in vung:
        ai = ten_att.index(v)
        uv = np.array(J["atts"][ai]["uvs"], float).reshape(-1, 2)
        H2, W2 = img.shape[:2]
        x0, x1 = uv[:, 0].min() * W2, uv[:, 0].max() * W2
        y0, y1 = (1 - uv[:, 1].max()) * H2, (1 - uv[:, 1].min()) * H2
        im = Image.fromarray(img[int(round(y0)):int(round(y1)), int(round(x0)):int(round(x1))], "RGBA")
        q = os.path.join(d, f"{ma}_tt_{v}.png")
        im.save(q)
        print(f"  {os.path.relpath(q, D.ROOT)}: {im.size}")


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if a[:1] == ["th"]:
        th()
    elif a[:1] == ["chep"]:
        D.chep("tinh_sat_1", RIG1, "tinh_sat_1_th.atomik")
        D.chep("tinh_sat_2", RIG2, "tinh_sat_2.atomik")
        anh_tt("tinh_sat_1", RIG1, TT_1)
        anh_tt("tinh_sat_2", RIG2, TT_2)
    else:
        D.heroes([(TEN_NON, "tinh_sat_1", CO_1), (TEN, "tinh_sat_2", CO_2)])
        D.cards()
