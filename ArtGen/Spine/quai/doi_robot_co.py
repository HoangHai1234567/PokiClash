# -*- coding: utf-8 -*-
"""Đổi HÌNH suất 7 đảo Kim (id `thiet_phu`, ải 40 "Mỏ Sắt Ngân") sang robot hủy diệt cổ đại (mã làm việc robot_co, rig monster_3613;
dạng 1 robot con thép mới → `robot_co_1`, dạng 2 robot cổ sắt gỉ → `robot_co_2`; ghi chú ArtGen/Spine/inbox/robot_co_ghichu.md).
Người dùng 2026-11-16: "ổn rồi, ghép vào game đi, làm thêm các fx cần thiết vì tôi chưa thấy tên lửa nào" (hiệu ứng: HatRobot.cs).

Giữ id tướng, id thẻ, chỉ số, hiệu ứng thẻ, SỐ DẠNG (2 → 2): bản lưu và golden không đổi. Đổi:
    tên     Thiết Phủ -> Thần Cơ; danh hiệu "Cỗ máy hủy diệt cổ đại"; dòng "Dòng Thần Cơ"
    dạng    [Heo Thiếc, Thiết Phủ] (thiet_phu_1, thiet_phu_2) -> [Thần Cơ Nhi (robot_co_1), Thần Cơ (robot_co_2)]
    thẻ     Rìu Bổ -> Thiên Cầu Giáng (hammer -> sun); Thiết Phủ Khai Sơn -> Hỏa Tiễn Liên Hoàn (crack -> flame);
            Thân Thiếc -> Giáp Thép Cổ (shield giữ)
Tên do Claude đặt (người dùng chưa đặt), người dùng có thể đổi. Không đè, không xoá thư mục Resources/thiet_phu_* cũ.

Sửa `Assets/02 Data/Json/heroes.json`, `cards.json` (nguồn). HeroDb.asset, CardDb.asset do menu Unity "PokiClash/Nhập dữ liệu" dựng lại, rồi
"PokiClash/Tướng/Gắn dạng .atomik vào prefab tướng". Chạy lại không đổi gì thêm.

    py -3 -I ArtGen/Spine/quai/doi_robot_co.py [--kiem]   heroes.json + cards.json
    py -3 -I ArtGen/Spine/quai/doi_robot_co.py th          gộp bản nhẹ dạng 2 + clip `evolve` vào rig dạng 1 → inbox/robot_co_non/rig/robot_co_non_th.atomik
    py -3 -I ArtGen/Spine/quai/doi_robot_co.py chep        chép rig (dạng 1 bản đã gộp tiến hoá) + chân dung vào Resources/robot_co_1/, robot_co_2/
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

D.ID = "thiet_phu"
TEN, TEN_NON = "Thần Cơ", "Thần Cơ Nhi"
CO_1, CO_2 = 0.92, 1.1
D.KHAC = [("name", "Thiết Phủ", TEN), ("title", "Người thiếc rìu bén", "Cỗ máy hủy diệt cổ đại"), ("line", "Dòng Thiết Phủ", "Dòng Thần Cơ")]
D.THE = {"thiet_phu_skill": ("Rìu Bổ", "Thiên Cầu Giáng", "hammer", "sun"),
         "thiet_phu_ult": ("Thiết Phủ Khai Sơn", "Hỏa Tiễn Liên Hoàn", "crack", "flame"),
         "thiet_phu_pas": ("Thân Thiếc", "Giáp Thép Cổ", "shield", "shield")}
INBOX = os.path.normpath(D.INBOX)
RIG1 = os.path.join(INBOX, "robot_co_non", "rig")
RIG2 = os.path.join(INBOX, "robot_co_1", "rig")
NHE = float(os.environ.get("RC_NHE") or 0.5)       # tỉ lệ atlas dạng 2 trong rig gộp


def th():
    """gộp dạng 2 (bản nhẹ) vào rig dạng 1 + clip `evolve` (như doi_quy_xich.th): dạng 1 gồng rung rồi mờ, dạng 2 hiện, lớn dần, dừng đúng
    khung 0 idle của nó. Slot ẩn sẵn của hai rig (nắp mắt tắt, bản nhân đôi theo thứ tự vẽ, ống rỗng...) giữ ẩn suốt clip."""
    sys.path.insert(0, os.path.join(SPINE, "mo_xe"))
    import atomik_dang as A
    J, img, ver = A.load(os.path.join(RIG1, "robot_co_non.atomik"))
    JB, imgB, _ = A.load(os.path.join(RIG2, "robot_co.atomik"))
    an_A = {i for i, s in enumerate(J["slots"]) if s.get("fade", 0) >= 1}
    an_B = {i for i, s in enumerate(JB["slots"]) if s.get("fade", 0) >= 1}
    nA_s = len(J["slots"])
    hA, hB = J["game"]["height"], JB["game"]["height"]
    k_B = CO_2 / CO_1 * hA / hB
    img = A.gop_tien_hoa(J, img, JB, imgB, k_B, than_A=A.bi(J)["bone3"], nhe=NHE)
    ev = J["anims"][-1]
    n = 0
    for x in ev["sa"]:
        if x["slot"] in an_A or (x["slot"] - nA_s) in an_B:
            x["keys"] = A.rot_keys([(0, 0), (ev["dur"], 0)])
            n += 1
    p = os.path.join(RIG1, "robot_co_non_th.atomik")
    kq = A.save(p, J, img, ver)
    print(f"{p}: {os.path.getsize(p) // 1024} KB; trong rig gộp dạng 2 × {k_B:.3f} (atlas × {NHE}); {n} slot ẩn giữ ẩn trong evolve; {kq}")
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
        D.chep("robot_co_1", RIG1, "robot_co_non_th.atomik")
        D.chep("robot_co_2", RIG2, "robot_co.atomik")
    else:
        D.heroes([(TEN_NON, "robot_co_1", CO_1), (TEN, "robot_co_2", CO_2)])
        D.cards()
