# -*- coding: utf-8 -*-
"""Đổi HÌNH suất 10 đảo Kim (id `kim_nghe`, ải 70 "Tháp Thiên Chung", boss cuối) sang vua robot (mã làm việc vua_may, rig monster_3637;
dạng 1 hoàng tử robot → `vua_may_1` (rig inbox/vua_may_non/rig), dạng 2 vua robot bốn cánh → `vua_may_2` (rig inbox/vua_may_1/rig); ghi chú
ArtGen/Spine/inbox/vua_may_ghichu.md). Người dùng 2026-11-17: "cho vào game đi" (hiệu ứng: HatVua.cs).

Giữ id tướng, id thẻ, chỉ số, hiệu ứng thẻ, bị động boss, SỐ DẠNG (2 → 2): bản lưu và golden không đổi. Đổi:
    tên     Kim Nghê -> Nhật Vương; danh hiệu "Vua robot quyền trượng Mặt Trời"; dòng "Dòng Nhật Vương"
    dạng    [Nghê Con, Kim Nghê] (kim_nghe_1, kim_nghe_2) -> [Nhật Hoàng Tử (vua_may_1), Nhật Vương (vua_may_2)], cỡ giữ 0,92 / 1,1
    thẻ     Nghê Hống -> Tam Tinh Quang Pháo (fang -> sun); Kim Nghê Lam Hỏa -> Nhật Thực Thiên Giáng (flame -> moon);
            Thần Thú Hộ Giáp -> Hào Quang Hộ Thể (helmet -> crown); bị động boss Kim Thân Bất Hoại giữ
Tên do Claude đặt (người dùng chưa đặt), người dùng có thể đổi.

Vụ nổ trong rig (fx_no, fx_no0..2: ảnh Mặt Trời phóng to) TẮT khi vào game: lớp hạt HatVua.cs làm nổ.

    py -3 -I ArtGen/Spine/quai/doi_vua_may.py [--kiem]   heroes.json + cards.json
    py -3 -I ArtGen/Spine/quai/doi_vua_may.py th          tắt nổ ảnh + gộp bản nhẹ dạng 2 + clip `evolve` vào rig dạng 1 → inbox/vua_may_non/rig/vua_may_non_th.atomik;
                                                          dạng 2 tắt nổ ảnh → inbox/vua_may_1/rig/vua_may_tran.atomik
    py -3 -I ArtGen/Spine/quai/doi_vua_may.py chep        chép hai rig + chân dung vào Resources/vua_may_1/, vua_may_2/
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

D.ID = "kim_nghe"
TEN, TEN_NON = "Nhật Vương", "Nhật Hoàng Tử"
CO_1, CO_2 = 0.92, 1.1
D.KHAC = [("name", "Kim Nghê", TEN), ("title", "Thần thú giáp lửa lam", "Vua robot quyền trượng Mặt Trời"), ("line", "Dòng Kim Nghê", "Dòng Nhật Vương")]
D.THE = {"kim_nghe_skill": ("Nghê Hống", "Tam Tinh Quang Pháo", "fang", "sun"),
         "kim_nghe_ult": ("Kim Nghê Lam Hỏa", "Nhật Thực Thiên Giáng", "flame", "moon"),
         "kim_nghe_pas": ("Thần Thú Hộ Giáp", "Hào Quang Hộ Thể", "helmet", "crown")}
INBOX = os.path.normpath(D.INBOX)
RIG1 = os.path.join(INBOX, "vua_may_non", "rig")
RIG2 = os.path.join(INBOX, "vua_may_1", "rig")
NHE = float(os.environ.get("VM_NHE") or 0.5)       # tỉ lệ atlas dạng 2 trong rig gộp
NO_ANH = ("fx_no", "fx_no0", "fx_no1", "fx_no2")   # vụ nổ trong rig: ảnh Mặt Trời phóng to (HatVua.cs làm nổ thật)


def an_no(J, tien=""):
    """mọi khoá độ đậm của các slot nổ ảnh → 0 suốt clip; trả số timeline đã tắt."""
    sys.path.insert(0, os.path.join(SPINE, "mo_xe"))
    import atomik_dang as A
    si = {s["name"]: i for i, s in enumerate(J["slots"])}
    ids = {si[tien + n] for n in NO_ANH if tien + n in si}
    n = 0
    for an in J["anims"]:
        for x in an.get("sa") or []:
            if x["slot"] in ids:
                x["keys"] = A.rot_keys([(0, 0), (an["dur"], 0)])
                n += 1
    for i in ids:
        J["slots"][i]["fade"] = 1.0
    return n


def th():
    """dạng 2 tắt nổ ảnh → vua_may_tran.atomik; gộp dạng 2 (bản nhẹ) vào rig dạng 1 + clip `evolve` (như doi_thu_phao.th)."""
    sys.path.insert(0, os.path.join(SPINE, "mo_xe"))
    import atomik_dang as A
    JB, imgB, verB = A.load(os.path.join(RIG2, "vua_may.atomik"))
    n2 = an_no(JB)
    p2 = os.path.join(RIG2, "vua_may_tran.atomik")
    A.save(p2, JB, imgB, verB)
    print(f"{p2}: {os.path.getsize(p2) // 1024} KB; tắt {n2} timeline nổ ảnh")
    J, img, ver = A.load(os.path.join(RIG1, "vua_may_non.atomik"))
    n1 = an_no(J)
    an_A = {i for i, s in enumerate(J["slots"]) if s.get("fade", 0) >= 1}
    an_B = {i for i, s in enumerate(JB["slots"]) if s.get("fade", 0) >= 1}
    nA_s = len(J["slots"])
    hA, hB = J["game"]["height"], JB["game"]["height"]
    k_B = CO_2 / CO_1 * hA / hB
    img = A.gop_tien_hoa(J, img, JB, imgB, k_B, than_A=A.bi(J)["xiabanshen_02"], nhe=NHE)
    ev = J["anims"][-1]
    n = 0
    for x in ev["sa"]:
        if x["slot"] in an_A or (x["slot"] - nA_s) in an_B:
            x["keys"] = A.rot_keys([(0, 0), (ev["dur"], 0)])
            n += 1
    p = os.path.join(RIG1, "vua_may_non_th.atomik")
    kq = A.save(p, J, img, ver)
    print(f"{p}: {os.path.getsize(p) // 1024} KB; tắt {n1} timeline nổ ảnh; trong rig gộp dạng 2 × {k_B:.3f} (atlas × {NHE}); {n} slot ẩn giữ ẩn "
          f"trong evolve; {kq}")
    ci = A.clip(J, "evolve")
    ts = [0.0, 0.5, 0.9, 1.05, 1.2, 1.35, 1.5, 1.8, 2.2, 2.6, 3.0]
    Ps = [A.Pose(J).at(ci, t) for t in ts]
    bs = np.array([A.bounds(P) for P in Ps])
    box = (bs[:, 0].min() - 20, bs[:, 1].min() - 20, bs[:, 2].max() + 20, bs[:, 3].max() + 20)
    ims = [A.render(J, img, A.Pose(J).at(ci, t), box, 0.2, bg=(150, 150, 150)).convert("RGB") for t in ts]
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
        D.chep("vua_may_1", RIG1, "vua_may_non_th.atomik")
        D.chep("vua_may_2", RIG2, "vua_may_tran.atomik")
    else:
        D.heroes([(TEN_NON, "vua_may_1", CO_1), (TEN, "vua_may_2", CO_2)])
        D.cards()
