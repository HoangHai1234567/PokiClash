# -*- coding: utf-8 -*-
"""Đưa DẠNG 2 (và dạng non của Sa Long) của các tướng Thổ vào game (2026-11-17). Mỗi suất thành dòng 2 dạng trên HAI rig khác nhau:
    thach_nhan  Thạch Giáp Nhi (cong_da_1, rig 3378)        → Thạch Giáp (cong_da_2, rig 3528)
    lung_vuong  Sa Tích Nhi    (than_lan_cat_1, rig 3257)   → Sa Tích    (than_lan_cat_2, rig 3530)
    cao_da      Tê Thiềm Nhi   (thu_da_1, rig 3525)         → Tê Thiềm   (thu_da_2, rig 3526)
    ho_khoan    Sa Long Nhi    (rong_cat_non, rig 3529)     → Sa Long    (rong_cat_1, rig 3424: bản đã có trong game)
Ghi chú: ArtGen/Spine/inbox/tho5_ghichu.md, inbox/<mã>_ghichu.md. Giữ id tướng, id thẻ, chỉ số (doi_tho5.py đã đổi tên, thẻ).

Clip tiến hoá như doi_tinh_sat.th(): gộp bản nhẹ dạng 2 vào rig dạng 1 + clip `evolve` (dạng 1 gồng rung rồi mờ, dạng 2 hiện, lớn dần, dừng
đúng khung 0 idle dạng 2) → inbox/<dạng 1>/rig/<dạng 1>_th.atomik + khung_evolve.png. Resources/<dạng 1>/ dùng bản _th.

    py -3 -I ArtGen/Spine/quai/doi_tho5_dang2.py [--kiem]        forms 2 dạng trong heroes.json (mọi suất trong TUONG2)
    py -3 -I ArtGen/Spine/quai/doi_tho5_dang2.py th [id|all]     gộp clip tiến hoá
    py -3 -I ArtGen/Spine/quai/doi_tho5_dang2.py chep [id|all]   chép rig + chân dung vào Resources/<mã>/
    py -3 -I ArtGen/Spine/quai/doi_tho5_dang2.py lam <id>        th + chep một suất (vd sau khi agent rig sửa lại dạng 2: `lam thach_nhan`)
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
import doi_phap_lua as D  # noqa: E402

INBOX = os.path.normpath(D.INBOX)
# id: (mã dạng 1, mã dạng 2, tên, cỡ dạng 1, cỡ dạng 2). Tên dạng 1 = tên + " Nhi".
TUONG2 = {
    "thach_nhan": ("cong_da_1", "cong_da_2", "Thạch Giáp", 0.88, 1.0),
    "lung_vuong": ("than_lan_cat_1", "than_lan_cat_2", "Sa Tích", 0.9, 1.04),
    "cao_da": ("thu_da_1", "thu_da_2", "Tê Thiềm", 0.92, 1.08),
    "ho_khoan": ("rong_cat_non", "rong_cat_1", "Sa Long", 0.85, 1.1),
}


def rig(ma):
    return os.path.join(INBOX, ma, "rig")


def th(hid):
    """gộp dạng 2 (bản nhẹ) vào rig dạng 1 + clip evolve; slot ẩn sẵn của hai rig giữ ẩn suốt clip."""
    sys.path.insert(0, os.path.join(SPINE, "mo_xe"))
    import atomik_dang as A
    ma1, ma2, ten, co1, co2 = TUONG2[hid]
    J, img, ver = A.load(os.path.join(rig(ma1), f"{ma1}.atomik"))
    JB, imgB, _ = A.load(os.path.join(rig(ma2), f"{ma2}.atomik"))
    an_A = {i for i, s in enumerate(J["slots"]) if s.get("fade", 0) >= 1}
    an_B = {i for i, s in enumerate(JB["slots"]) if s.get("fade", 0) >= 1}
    nA_s = len(J["slots"])
    hA, hB = J["game"]["height"], JB["game"]["height"]
    k_B = co2 / co1 * hA / hB
    bi = A.bi(J)
    than = next((i for i, b in enumerate(J["bones"]) if b["parent"] == bi.get("tam")), bi.get("all", bi.get("bone")))
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


def heroes():
    for hid, (ma1, ma2, ten, co1, co2) in TUONG2.items():
        D.ID = hid
        D.KHAC = []
        D.heroes([(f"{ten} Nhi", ma1, co1), (ten, ma2, co2)])


def chep(hid):
    ma1, ma2, ten, co1, co2 = TUONG2[hid]
    th1 = os.path.join(rig(ma1), f"{ma1}_th.atomik")
    if not os.path.exists(th1):
        raise SystemExit(f"chưa có {th1}: chạy `th {hid}` trước")
    D.chep(ma1, rig(ma1), f"{ma1}_th.atomik")
    D.chep(ma2, rig(ma2), f"{ma2}.atomik")


if __name__ == "__main__":
    D.KIEM = "--kiem" in sys.argv
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    ids = list(TUONG2) if len(a) < 2 or a[1] == "all" else [a[1]]
    if a[:1] == ["th"]:
        for h in ids:
            th(h)
    elif a[:1] == ["chep"]:
        for h in ids:
            chep(h)
    elif a[:1] == ["lam"]:
        th(a[1])
        chep(a[1])
    else:
        heroes()
