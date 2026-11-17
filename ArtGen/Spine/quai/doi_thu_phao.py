# -*- coding: utf-8 -*-
"""Đổi HÌNH suất 9 đảo Kim (id `ung_thep`, ải 60 "Tổ Cánh Pha Lê") sang thú giáp pháo (mã làm việc thu_phao, rig monster_3629;
dạng 1 thú non mũ hiệp sĩ tròn → `thu_phao_1`, dạng 2 thú giáp bạc viền vàng mũ hiệp sĩ → `thu_phao_2`; ghi chú
ArtGen/Spine/inbox/thu_phao_ghichu.md). Người dùng 2026-11-17: "cho vao game di" (hiệu ứng: HatPhao.cs).

Giữ id tướng, id thẻ, chỉ số, hiệu ứng thẻ, SỐ DẠNG (2 → 2): bản lưu và golden không đổi. Đổi:
    tên     Ưng Thép -> Pháo Giáp; danh hiệu "Thú giáp pháo công thành"; dòng "Dòng Pháo Giáp"
    dạng    [Ưng Thép Con, Ưng Thép] (ung_thep_1, ung_thep_2) -> [Pháo Giáp Nhi (thu_phao_1), Pháo Giáp (thu_phao_2)]
    thẻ     Lông Pha Lê -> Pháo Tán Hỏa Tiễn (feather -> crack); Săn Trời -> Lôi Pháo Đại Cầu (wing -> bolt);
            Cánh Gió -> Giáp Hiệp Sĩ (wing -> helmet)
Tên do Claude đặt (người dùng chưa đặt), người dùng có thể đổi. Không đè, không xoá thư mục Resources/ung_thep_* cũ.

Sửa `Assets/02 Data/Json/heroes.json`, `cards.json` (nguồn). HeroDb.asset, CardDb.asset do menu Unity "PokiClash/Nhập dữ liệu" dựng lại, rồi
"PokiClash/Tướng/Gắn dạng .atomik vào prefab tướng". Chạy lại không đổi gì thêm.

    py -3 -I ArtGen/Spine/quai/doi_thu_phao.py [--kiem]   heroes.json + cards.json
    py -3 -I ArtGen/Spine/quai/doi_thu_phao.py th          gộp bản nhẹ dạng 2 + clip `evolve` vào rig dạng 1 → inbox/thu_phao_non/rig/thu_phao_non_th.atomik
    py -3 -I ArtGen/Spine/quai/doi_thu_phao.py chep        chép rig (dạng 1 bản đã gộp tiến hoá) + chân dung vào Resources/thu_phao_1/, thu_phao_2/
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

D.ID = "ung_thep"
TEN, TEN_NON = "Pháo Giáp", "Pháo Giáp Nhi"
CO_1, CO_2 = 0.92, 1.1
D.KHAC = [("name", "Ưng Thép", TEN), ("title", "Thợ săn trời cánh pha lê", "Thú giáp pháo công thành"), ("line", "Dòng Ưng Thép", "Dòng Pháo Giáp")]
D.THE = {"ung_thep_skill": ("Lông Pha Lê", "Pháo Tán Hỏa Tiễn", "feather", "crack"),
         "ung_thep_ult": ("Săn Trời", "Lôi Pháo Đại Cầu", "wing", "bolt"),
         "ung_thep_pas": ("Cánh Gió", "Giáp Hiệp Sĩ", "wing", "helmet")}
INBOX = os.path.normpath(D.INBOX)
RIG1 = os.path.join(INBOX, "thu_phao_non", "rig")
RIG2 = os.path.join(INBOX, "thu_phao_1", "rig")
NHE = float(os.environ.get("TP_NHE") or 0.5)       # tỉ lệ atlas dạng 2 trong rig gộp


def th():
    """gộp dạng 2 (bản nhẹ) vào rig dạng 1 + clip `evolve` (như doi_robot_co.th): dạng 1 gồng rung rồi mờ, dạng 2 hiện, lớn dần, dừng đúng
    khung 0 idle của nó. Slot ẩn sẵn của hai rig giữ ẩn suốt clip."""
    sys.path.insert(0, os.path.join(SPINE, "mo_xe"))
    import atomik_dang as A
    J, img, ver = A.load(os.path.join(RIG1, "thu_phao_non.atomik"))
    JB, imgB, _ = A.load(os.path.join(RIG2, "thu_phao.atomik"))
    an_A = {i for i, s in enumerate(J["slots"]) if s.get("fade", 0) >= 1}
    an_B = {i for i, s in enumerate(JB["slots"]) if s.get("fade", 0) >= 1}
    nA_s = len(J["slots"])
    hA, hB = J["game"]["height"], JB["game"]["height"]
    k_B = CO_2 / CO_1 * hA / hB
    img = A.gop_tien_hoa(J, img, JB, imgB, k_B, than_A=A.bi(J)["bone"], nhe=NHE)
    ev = J["anims"][-1]
    n = 0
    for x in ev["sa"]:
        if x["slot"] in an_A or (x["slot"] - nA_s) in an_B:
            x["keys"] = A.rot_keys([(0, 0), (ev["dur"], 0)])
            n += 1
    p = os.path.join(RIG1, "thu_phao_non_th.atomik")
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
        D.chep("thu_phao_1", RIG1, "thu_phao_non_th.atomik")
        D.chep("thu_phao_2", RIG2, "thu_phao.atomik")
    else:
        D.heroes([(TEN_NON, "thu_phao_1", CO_1), (TEN, "thu_phao_2", CO_2)])
        D.cards()
