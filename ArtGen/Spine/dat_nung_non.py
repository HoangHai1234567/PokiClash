# -*- coding: utf-8 -*-
"""Viêm Dũng DẠNG 1 (Viêm Dũng Nhi, chibi; mã dat_nung_non, suất huyen_viem = tướng thứ 8 đảo Hỏa).

Người dùng 2026-11-14: "Ổn, cho vào game đi rồi làm dạng 1 của tướng này" → xem hai concept → chọn A (mặt nạ thú non):
inbox/dat_nung_non/tai_ve/L1_duyet.png (= L1_theo_bo_cuc.png).

Cùng bộ xương, cùng lưới, cùng 8 clip với dạng 2 (dat_nung_rig.py, chế độ DN_NON=1). Khác dạng 2:
- tỉ lệ dáng gốc (TI_NON trong dat_nung_rig.py): đầu 1,5; lõi 1,2; vành cổ, giáp vai, phiến bên, phiến lưng, kiếm thu nhỏ; bớt bốn phiến lưng;
- mảnh vẽ riêng theo concept (đầu, hai vành cổ, hai giáp vai, kiếm): dat_nung_da.py non_to_minh / non_cat_moi → inbox/dat_nung_non/manh_part2;
  mảnh khác dùng da dạng 2.

    dat_nung_da.py non            hai prompt concept (gui_gpt/dat_nung_non/luot_1_concept_*.txt)
    dat_nung_da.py non_to_minh    tờ hướng dẫn + prompt mảnh (luot_2_manh_<G|K|W>.txt)
    dat_nung_da.py non_cat_moi    cắt tờ đã gen → inbox/dat_nung_non/manh_part2
    DN_NON=1 py -3 -I dat_nung_rig.py            rig dạng 1 → inbox/dat_nung_non/rig/
    dat_nung_non.py th            gộp clip evolve sang dạng 2 → inbox/dat_nung_non/rig/dat_nung_non_th.atomik + khung_evolve.png
Xương, lưới, chuyển động gốc là của nhà phát hành game tham khảo: dùng nội bộ, không đăng công khai."""
import os
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
RIG = os.path.join(HERE, "inbox", "dat_nung_non", "rig")
SIZE_A, SIZE_B = 0.85, 0.95                        # cỡ trong heroes.json: dạng 1, dạng 2 (quai/doi_dat_nung.py CO_NON, CO_LON)


def th():
    """gộp dạng 2 (bản nhẹ) vào rig dạng 1 + clip `evolve` (mo_xe/atomik_dang.gop_tien_hoa, như quy_dao_non.py th): dạng 1 gồng rung rồi mờ,
    dạng 2 hiện, lớn dần, dừng đúng khung 0 idle của nó. Slot ẩn sẵn của hai rig (mảnh rời, hình tắt, kiếm bay, bản nhân của slot di động)
    giữ ẩn suốt clip."""
    sys.path.insert(0, os.path.join(HERE, "mo_xe"))
    import atomik_dang as A
    src_a = os.path.join(RIG, "dat_nung_non.atomik")
    src_b = os.path.join(HERE, "inbox", "dat_nung_1", "rig_moi", "dat_nung_1.atomik")
    if not os.path.exists(src_b):                  # máy chưa dựng lại rig dạng 2: lấy bản đang ở trong game (chỉ đọc)
        src_b = os.path.normpath(os.path.join(HERE, "..", "..", "Assets", "03 Art", "Heroes", "Resources", "dat_nung_1", "dat_nung_1.atomik"))
    J, img, ver = A.load(src_a)
    JB, imgB, _ = A.load(src_b)
    an_A = {i for i, s in enumerate(J["slots"]) if s.get("fade", 0) >= 1}
    an_B = {i for i, s in enumerate(JB["slots"]) if s.get("fade", 0) >= 1}
    nA_s = len(J["slots"])
    hA, hB = J["game"]["height"], JB["game"]["height"]
    k_B = SIZE_B / SIZE_A * hA / hB
    img = A.gop_tien_hoa(J, img, JB, imgB, k_B, than_A=A.bi(J)["shenti1"])
    ev = J["anims"][-1]
    n = 0
    for x in ev["sa"]:
        if x["slot"] in an_A or (x["slot"] - nA_s) in an_B:
            x["keys"] = A.rot_keys([(0, 0), (ev["dur"], 0)])
            n += 1
    p = os.path.join(RIG, "dat_nung_non_th.atomik")
    kq = A.save(p, J, img, ver)
    print(f"{p}: {os.path.getsize(p) // 1024} KB; dạng 2 lấy từ {src_b}; trong rig gộp × {k_B:.3f}; {n} slot ẩn giữ ẩn trong evolve; {kq}")
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
    out.save(os.path.join(RIG, "khung_evolve.png"))
    print(os.path.join(RIG, "khung_evolve.png"), out.size)
    # khung cuối evolve phải trùng khung 0 idle của dạng 2 (cùng tỉ lệ k_B)
    ib = A.clip(JB, "idle")
    Pb = A.Pose(JB).at(ib, 0.0)
    Pe = A.Pose(J).at(ci, ev["dur"])
    nb = len(J["bones"]) - len(JB["bones"])
    lech = 0.0
    for i in range(len(JB["bones"])):
        lech = max(lech, abs(Pe.w[nb + i][4] - Pb.w[i][4] * k_B), abs(Pe.w[nb + i][5] - Pb.w[i][5] * k_B))
    print(f"khung cuối evolve so khung 0 idle dạng 2: lệch gốc xương lớn nhất {lech:.3f} đơn vị")


if __name__ == "__main__":
    if sys.argv[1:2] == ["th"]:
        th()
    else:
        print(__doc__)
