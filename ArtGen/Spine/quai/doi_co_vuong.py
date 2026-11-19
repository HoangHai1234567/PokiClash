# -*- coding: utf-8 -*-
"""Đổi suất 6 đảo Mộc (id `gio_loc`, ải 30 "Thung Lũng Lá") sang dòng CỔ VƯƠNG: tượng vua cổ rễ quấn cầm cột đá (người dùng 2026-11-17:
"ok ổn cho vào game đi"). Thay hẳn Linh Điểu (chim_la). Ghi chú: ArtGen/Spine/inbox/tuong_cot_ghichu.md.

ĐÃ THAY 2026-11-19: Cổ Vương là tướng 6 đảo THỔ (ghép nhầm vào gio_loc); nay ở suất hat_de, Linh Điểu trả về gio_loc. Dùng
quai/doi_suat6_tho.py, đừng chạy lại script này (nó đè Cổ Vương lên gio_loc lần nữa).

Giữ id tướng, id thẻ, chỉ số, hiệu ứng thẻ, tên thư mục dạng (gio_loc_1, gio_loc_2: prefab không phải đổi); đổi tên hiển thị, biểu tượng
thẻ, cỡ, hình:

    tướng   Linh Điểu -> Cổ Vương; danh hiệu "Tượng vua cổ cầm trụ"; dòng "Dòng Cổ Vương"
    dạng    Cổ Vương Nhi (gio_loc_1 = tuong_cot_non_th.atomik, rig monster_3273, có clip evolve) / Cổ Vương (gio_loc_2 = tuong_cot_1.atomik,
            rig monster_3608)
    thẻ     Lông Lá Găm -> Rễ Trói Đất (seed); Thiên Thạch Giáng -> Thần Trụ Giáng Thế (rock); Cánh Lá Nhẹ -> Thân Đá Rời (shield, né
            đòn: các khối đá lơ lửng dạt ra); bị động boss Gió Cuốn -> Rễ Hút Linh Lực (leaf)
Tên do Claude đặt (người dùng: "tên bạn tự đặt"), người dùng có thể đổi.

    py -3 -I ArtGen/Spine/quai/doi_co_vuong.py [--kiem]     heroes.json, cards.json
    py -3 -I ArtGen/Spine/quai/doi_co_vuong.py th            gộp bản nhẹ dạng 2 vào rig dạng 1 + clip evolve → tuong_cot_non_th.atomik
    py -3 -I ArtGen/Spine/quai/doi_co_vuong.py chep          chép .atomik + chân dung vào Resources/gio_loc_1, gio_loc_2
"""
import os
import shutil
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
SPINE = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, SPINE)
import doi_phap_lua as D  # noqa: E402

INBOX = os.path.normpath(D.INBOX)
ID = "gio_loc"
CO1, CO2 = 0.88, 1.1
DANG = [("Cổ Vương Nhi", "gio_loc_1", CO1), ("Cổ Vương", "gio_loc_2", CO2)]
RIG = {"gio_loc_1": ("tuong_cot_non", "tuong_cot_non_th.atomik"), "gio_loc_2": ("tuong_cot_1", "tuong_cot_1.atomik")}
KHAC = [("name", "Linh Điểu", "Cổ Vương"), ("title", "Chim thần giữ rừng", "Tượng vua cổ cầm trụ"), ("line", "Dòng Linh Điểu", "Dòng Cổ Vương")]
THE = {"gio_loc_skill": ("Lông Lá Găm", "Rễ Trói Đất", "leaf", "seed"),
       "gio_loc_ult": ("Thiên Thạch Giáng", "Thần Trụ Giáng Thế", "rock", "rock"),
       "gio_loc_pas": ("Cánh Lá Nhẹ", "Thân Đá Rời", "wing", "shield"),
       "gio_loc_boss": ("Gió Cuốn", "Rễ Hút Linh Lực", "wind", "leaf")}


THU_MUC = {"tuong_cot_non": "tuong_cot_non_1", "tuong_cot_1": "tuong_cot_1"}


def rig(ma):
    return os.path.join(INBOX, THU_MUC[ma], "rig")


def th():
    """như doi_tho5_dang2.th: gộp dạng 2 (bản nhẹ) vào rig dạng 1 + clip evolve; slot ẩn sẵn của hai rig giữ ẩn suốt clip."""
    sys.path.insert(0, os.path.join(SPINE, "mo_xe"))
    import atomik_dang as A
    ma1, ma2 = "tuong_cot_non", "tuong_cot_1"
    J, img, ver = A.load(os.path.join(rig(ma1), f"{ma1}.atomik"))
    JB, imgB, _ = A.load(os.path.join(rig(ma2), f"{ma2}.atomik"))
    an_A = {i for i, s in enumerate(J["slots"]) if s.get("fade", 0) >= 1}
    an_B = {i for i, s in enumerate(JB["slots"]) if s.get("fade", 0) >= 1}
    nA_s = len(J["slots"])
    hA, hB = J["game"]["height"], JB["game"]["height"]
    k_B = CO2 / CO1 * hA / hB
    bi = A.bi(J)
    than = bi.get("bone2", bi.get("xy"))
    img = A.gop_tien_hoa(J, img, JB, imgB, k_B, than_A=than)
    ev = J["anims"][-1]
    n = 0
    for x in ev["sa"]:
        if x["slot"] in an_A or (x["slot"] - nA_s) in an_B:
            x["keys"] = A.rot_keys([(0, 0), (ev["dur"], 0)])
            n += 1
    p = os.path.join(rig(ma1), f"{ma1}_th.atomik")
    kq = A.save(p, J, img, ver)
    print(f"{p}: {os.path.getsize(p) // 1024} KB; dạng 2 × {k_B:.3f}; xương rung {J['bones'][than]['name']}; {n} slot ẩn giữ ẩn; {kq}")
    ci = A.clip(J, "evolve")
    ts = [0.0, 0.5, 0.9, 1.05, 1.2, 1.35, 1.5, 1.8, 2.2, 2.6, 3.0]
    Ps = [A.Pose(J).at(ci, t) for t in ts]
    bs = np.array([A.bounds(P) for P in Ps])
    box = (bs[:, 0].min() - 20, bs[:, 1].min() - 20, bs[:, 2].max() + 20, bs[:, 3].max() + 20)
    sc = 300.0 / max(1.0, box[3] - box[1])
    ims = [A.render(J, img, A.Pose(J).at(ci, t), box, sc, bg=(150, 150, 150)).convert("RGB") for t in ts]
    cot = 6
    out = Image.new("RGB", (cot * ims[0].width, ((len(ims) + cot - 1) // cot) * ims[0].height), (150, 150, 150))
    for i, im in enumerate(ims):
        out.paste(im, ((i % cot) * im.width, (i // cot) * im.height))
    q = os.path.join(rig(ma1), "khung_evolve.png")
    out.save(q)
    print(q, out.size)


def chep():
    for dich, (ma, ten) in RIG.items():
        d = os.path.join(D.RES, dich)
        os.makedirs(d, exist_ok=True)
        for nguon, ra in ((ten, f"{dich}.atomik"), ("chan_dung.png", f"{dich}_portrait.png")):
            p, q = os.path.join(rig(ma), nguon), os.path.join(d, ra)
            giong = os.path.exists(q) and open(p, "rb").read() == open(q, "rb").read()
            if not giong and not D.KIEM:
                shutil.copyfile(p, q)
            print(f"  {os.path.relpath(q, D.ROOT)}: {'giữ' if giong else 'chép'} ({os.path.getsize(p) // 1024} KB)")


def du_lieu():
    D.ID = ID
    D.KHAC = KHAC
    D.THE = THE
    D.heroes(DANG)
    D.cards()


if __name__ == "__main__":
    D.KIEM = "--kiem" in sys.argv
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if a[:1] == ["th"]:
        th()
    elif a[:1] == ["chep"]:
        chep()
    else:
        du_lieu()
