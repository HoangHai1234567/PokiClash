# -*- coding: utf-8 -*-
"""Đổi HÌNH suất 3 đảo Kim (id `bo_ngua`, ải 10 "Rừng Lưỡi Liềm") sang tinh linh quặng sắt (mã làm việc quang_sat; cả hai dạng trên rig
monster_3371: dạng 1 → `quang_sat_1`, dạng 2 → `quang_sat_2`; ghi chú ArtGen/Spine/inbox/quang_sat_ghichu.md). Người dùng 2026-11-16: dòng 2 dạng,
"bạn cho vào game chưa" → chọn "Làm luôn, Claude đặt tên tạm".

Giữ id tướng, id thẻ, chỉ số, hiệu ứng thẻ (không đổi bản lưu). SỐ DẠNG 3 → 2 nên golden roster, sim phải tính lại trong Unity. Đổi:
    tên     Bọ Ngựa Liềm Thép -> Thiết Khoáng; danh hiệu "Tinh linh quặng sắt chui đất"; dòng "Dòng Thiết Khoáng"
    dạng    [Bọ Ngựa Con, Bọ Ngựa Lưỡi Bén, Bọ Ngựa Liềm Thép] (bo_ngua_1, bo_ngua_2, goc_685)
            -> [Thiết Khoáng Nhi (quang_sat_1, cỡ 0,92), Thiết Khoáng (quang_sat_2, cỡ 1,0)]
    thẻ     Song Liềm -> Song Quyền Quặng (sword -> fist2: thẻ đánh 2 nhát = hai tay quặng bay); Liềm Thép Xé Gió -> Độn Thổ Húc (wind -> crack);
            Mắt Rình Mồi -> Mắt Dò Mạch (eye, tăng chí mạng: mắt dò mạch quặng)
Tên do Claude đặt tạm, người dùng có thể đổi. Không đè, không xoá thư mục Resources/bo_ngua_* cũ.

Sửa `Assets/02 Data/Json/heroes.json`, `cards.json` (nguồn). HeroDb.asset, CardDb.asset do menu Unity "PokiClash/Nhập dữ liệu" dựng lại, rồi
"PokiClash/Tướng/Gắn dạng .atomik vào prefab tướng", rồi các menu golden. Chạy lại không đổi gì thêm.

    py -3 -I ArtGen/Spine/quai/doi_quang_sat.py [--kiem]   heroes.json + cards.json
    py -3 -I ArtGen/Spine/quai/doi_quang_sat.py th          gộp dạng 2 + clip `evolve` vào rig dạng 1 → inbox/quang_sat_1/rig/quang_sat_1_th.atomik
    py -3 -I ArtGen/Spine/quai/doi_quang_sat.py chep        chép rig (dạng 1 bản đã gộp tiến hoá) + chân dung vào Resources/quang_sat_1/, quang_sat_2/
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

D.ID = "bo_ngua"
TEN, TEN_NON = "Thiết Khoáng", "Thiết Khoáng Nhi"
CO_1, CO_2 = 0.92, 1.0
D.KHAC = [("name", "Bọ Ngựa Liềm Thép", TEN), ("title", "Song liềm kiếm khách", "Tinh linh quặng sắt chui đất"),
          ("line", "Dòng Bọ Ngựa Liềm Thép", "Dòng Thiết Khoáng")]
D.THE = {"bo_ngua_skill": ("Song Liềm", "Song Quyền Quặng", "sword", "fist2"),
         "bo_ngua_ult": ("Liềm Thép Xé Gió", "Độn Thổ Húc", "wind", "crack"),
         "bo_ngua_pas": ("Mắt Rình Mồi", "Mắt Dò Mạch", "eye", "eye")}
INBOX = os.path.normpath(D.INBOX)
RIG1 = os.path.join(INBOX, "quang_sat_1", "rig")
RIG2 = os.path.join(INBOX, "quang_sat_2", "rig")


def th():
    """gộp dạng 2 vào rig dạng 1 + clip `evolve` (như doi_tinh_sat.py th): dạng 1 gồng rung rồi mờ, dạng 2 hiện, lớn dần, dừng đúng khung 0
    idle của nó. Slot ẩn sẵn của hai rig (hố, gò, mặt nạ, tay bay, bản sao tay của die) giữ ẩn suốt clip."""
    sys.path.insert(0, os.path.join(SPINE, "mo_xe"))
    import atomik_dang as A
    J, img, ver = A.load(os.path.join(RIG1, "quang_sat_1.atomik"))
    JB, imgB, _ = A.load(os.path.join(RIG2, "quang_sat_2.atomik"))
    an_A = {i for i, s in enumerate(J["slots"]) if s.get("fade", 0) >= 1}
    an_B = {i for i, s in enumerate(JB["slots"]) if s.get("fade", 0) >= 1}
    nA_s = len(J["slots"])
    hA, hB = J["game"]["height"], JB["game"]["height"]
    k_B = CO_2 / CO_1 * hA / hB
    img = A.gop_tien_hoa(J, img, JB, imgB, k_B, than_A=A.bi(J)["tam"])
    ev = J["anims"][-1]
    n = 0
    for x in ev["sa"]:
        if x["slot"] in an_A or (x["slot"] - nA_s) in an_B:
            x["keys"] = A.rot_keys([(0, 0), (ev["dur"], 0)])
            n += 1
    p = os.path.join(RIG1, "quang_sat_1_th.atomik")
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


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if a[:1] == ["th"]:
        th()
    elif a[:1] == ["chep"]:
        D.chep("quang_sat_1", RIG1, "quang_sat_1_th.atomik")
        D.chep("quang_sat_2", RIG2, "quang_sat_2.atomik")
    else:
        D.heroes([(TEN_NON, "quang_sat_1", CO_1), (TEN, "quang_sat_2", CO_2)])
        D.cards()
