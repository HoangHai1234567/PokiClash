# -*- coding: utf-8 -*-
"""Đổi HÌNH suất 8 đảo Kim (id `tam_kiem`, ải 50 "Thành Ba Kiếm", có boss) sang kỵ sĩ cổ đại bị nguyền (mã làm việc ky_nguyen, rig
monster_3642; ghi chú ArtGen/Spine/inbox/ky_nguyen_ghichu.md). Người dùng 2026-11-16: "ok cho vào game, làm thêm các fx hiệu ứng nữa rồi làm
dạng 1 của tướng này".

Giữ id tướng, id thẻ, chỉ số, hiệu ứng thẻ, số mảnh. SỐ DẠNG 3 → 2 (như các suất đã đổi hình) nên golden roster / sim phải tính lại trong Unity.
Đổi:
    tên     Tam Kiếm -> Vong Kỵ; danh hiệu "Kỵ sĩ cổ đại bị nguyền"; dòng "Dòng Vong Kỵ"
    dạng    [Kiếm Sĩ Nhí, Song Kiếm, Tam Kiếm Vương] (tam_kiem_1..3) -> hai dạng. Chưa có rig dạng 1: cả hai trỏ ky_nguyen_2 (cỡ 0,92 / 1,1).
            Có rig dạng 1 thì chạy `dang_1`: dạng 1 "Vong Kỵ Nhi" -> ky_nguyen_1 (bản đã gộp tiến hoá)
    thẻ     Song Kiếm -> Hồn Binh Cổ Chiến (sword -> ghost); Tam Kiếm Hợp Nhất -> Kiếm Hồn Phục Sinh (sword); Kiếm Tâm -> Bất Tử Nguyền
            (crown -> skull); thẻ boss Kiếm Phản -> Kiếm Nguyền Phản (sword)
Tên do Claude đặt tạm (người dùng chưa đặt), người dùng có thể đổi. Không đè, không xoá thư mục Resources/tam_kiem_* cũ.

    py -3 -I ArtGen/Spine/quai/doi_ky_nguyen.py [--kiem]   heroes.json + cards.json
    py -3 -I ArtGen/Spine/quai/doi_ky_nguyen.py th          gộp bản nhẹ dạng 2 + clip `evolve` vào rig dạng 1 → inbox/ky_nguyen_non/rig/ky_nguyen_non_th.atomik
    py -3 -I ArtGen/Spine/quai/doi_ky_nguyen.py chep        rig dạng 1 (bản gộp, nếu có) → Resources/ky_nguyen_1/; rig dạng 2 + chân dung + ảnh
                                                            hồn đồng đội (HatHon.cs) → Resources/ky_nguyen_2/
    py -3 -I ArtGen/Spine/quai/doi_ky_nguyen.py dang_1      dạng 1 -> ky_nguyen_1 (sau khi có Resources/ky_nguyen_1)
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

D.ID = "tam_kiem"
TEN, TEN_NON = "Vong Kỵ", "Vong Kỵ Nhi"
CO_1, CO_2 = 0.92, 1.1
D.KHAC = [("name", "Tam Kiếm", TEN), ("title", "Giáp vương ba kiếm", "Kỵ sĩ cổ đại bị nguyền"), ("line", "Dòng Tam Kiếm", "Dòng Vong Kỵ")]
D.THE = {"tam_kiem_skill": ("Song Kiếm", "Hồn Binh Cổ Chiến", "sword", "ghost"),
         "tam_kiem_ult": ("Tam Kiếm Hợp Nhất", "Kiếm Hồn Phục Sinh", "sword", "sword"),
         "tam_kiem_pas": ("Kiếm Tâm", "Bất Tử Nguyền", "crown", "skull"),
         "tam_kiem_boss": ("Kiếm Phản", "Kiếm Nguyền Phản", "sword", "sword")}
INBOX = os.path.normpath(D.INBOX)
RIG1 = os.path.join(INBOX, "ky_nguyen_non", "rig")          # dạng 1 Vong Kỵ Nhi (concept C, 2026-11-17)
RIG2 = os.path.join(INBOX, "ky_nguyen_1", "rig")
MANH2 = os.path.join(INBOX, "ky_nguyen_1", "manh")
XANH, NHAT, DAM, INK = (132, 205, 57), (211, 244, 149), (62, 142, 52), (43, 33, 24)


def anh_hon(ma):
    """ảnh HỒN ĐỒNG ĐỘI cho chiêu mana (HatHon.cs nạp Resources.Load<Sprite>("<ma>/<ma>_tt_hon")): hình bóng mũ vương miện của mình (manh/mu.png)
    tô phẳng xanh hồn, lõi xanh nhạt, khe mắt tối có hai mắt sáng, viền mực; tên có "_tt_" để AolaImport nhập thành sprite."""
    import cv2
    g = np.asarray(Image.open(os.path.join(MANH2, "mu.png")).convert("RGBA"))
    a = g[..., 3] > 110
    h, w = a.shape
    pad = 8
    m = np.zeros((h + 2 * pad, w + 2 * pad), np.uint8)
    m[pad:pad + h, pad:pad + w] = a
    el = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * 5 + 1, 2 * 5 + 1))
    trong = cv2.erode(m, el)
    lum = np.zeros(m.shape, np.uint8)
    lum[pad:pad + h, pad:pad + w] = (g[..., :3].astype(np.int32).mean(2) < 45) & a      # khe mắt + nét mực của mũ
    rgb = np.zeros(m.shape + (3,), np.uint8)
    rgb[...] = XANH
    # lõi xanh nhạt: vùng cách mép > 22 % bề ngang
    dist = cv2.distanceTransform(m, cv2.DIST_L2, 5)
    rgb[dist > 0.16 * w] = NHAT
    rgb[(lum > 0) & (trong > 0)] = (47, 107, 42)                                    # khe mắt, đường mũ: xanh thẫm
    rgb[(m > 0) & (trong == 0)] = INK                                               # viền mực
    # hai mắt: mảnh mắt của rig (manh/mat.png) đặt đúng chỗ trên mũ theo 4 góc thế giới của mũ / mắt (moi.json), tô xanh nhạt sáng
    import json
    moi = json.load(open(os.path.join(MANH2, "moi.json")))
    Vm, Ve = np.array(moi["mu"]["the_gioi"], float), np.array(moi["mat"]["the_gioi"], float)
    src = np.array([[0, 0], [w, 0], [w, h], [0, h]], float)
    Mm, *_ = np.linalg.lstsq(np.c_[Vm, np.ones(4)], src, rcond=None)                # thế giới → px ảnh mũ
    e = np.asarray(Image.open(os.path.join(MANH2, "mat.png")).convert("RGBA"))
    eh, ew = e.shape[:2]
    pe = np.c_[Ve, np.ones(4)] @ Mm + pad
    Mp = cv2.getPerspectiveTransform(np.float32([[0, 0], [ew, 0], [ew, eh], [0, eh]]), np.float32(pe))
    ea = cv2.warpPerspective(e[..., 3], Mp, (m.shape[1], m.shape[0])) > 110
    ex = cv2.warpPerspective(((e[..., 1].astype(int) - e[..., 0] > 40) & (e[..., 3] > 110)).astype(np.uint8) * 255, Mp,
                             (m.shape[1], m.shape[0])) > 110
    rgb[ea] = INK
    rgb[ex] = (236, 255, 190)
    al = (m > 0).astype(np.float32)
    al = cv2.GaussianBlur(al, (0, 0), 0.7)
    out = np.dstack([rgb, (np.clip(al * 1.2, 0, 1) * 255).astype(np.uint8)])
    d = os.path.join(D.RES, ma)
    os.makedirs(d, exist_ok=True)
    q = os.path.join(d, f"{ma}_tt_hon.png")
    Image.fromarray(out, "RGBA").save(q)
    print(f"  {os.path.relpath(q, D.ROOT)}: {out.shape[1]}×{out.shape[0]}")


def th():
    """gộp dạng 2 (bản nhẹ) vào rig dạng 1 + clip `evolve` (như doi_quy_xich.th): dạng 1 gồng rung rồi mờ, dạng 2 hiện, lớn dần, dừng đúng
    khung 0 idle của nó. Slot ẩn sẵn của hai rig (phần vá hồn của chiêu cuối...) giữ ẩn suốt clip. Mặt nạ cắt (khối masks) của dạng 2 không
    vào rig gộp (dạng 2 trong evolve không bao giờ bật mặt nạ); mặt nạ của dạng 1 giữ nguyên chỉ số slot."""
    sys.path.insert(0, os.path.join(SPINE, "mo_xe"))
    import atomik_dang as A
    J, img, ver = A.load(os.path.join(RIG1, "ky_nguyen_non.atomik"))
    JB, imgB, _ = A.load(os.path.join(RIG2, "ky_nguyen.atomik"))
    an_A = {i for i, s in enumerate(J["slots"]) if s.get("fade", 0) >= 1}
    an_B = {i for i, s in enumerate(JB["slots"]) if s.get("fade", 0) >= 1}
    nA_s = len(J["slots"])
    hA, hB = J["game"]["height"], JB["game"]["height"]
    k_B = CO_2 / CO_1 * hA / hB
    img = A.gop_tien_hoa(J, img, JB, imgB, k_B, than_A=A.bi(J)["bone2"])
    ev = J["anims"][-1]
    n = 0
    for x in ev["sa"]:
        if x["slot"] in an_A or (x["slot"] - nA_s) in an_B:
            x["keys"] = A.rot_keys([(0, 0), (ev["dur"], 0)])
            n += 1
    p = os.path.join(RIG1, "ky_nguyen_non_th.atomik")
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
        if os.path.exists(os.path.join(RIG1, "ky_nguyen_non_th.atomik")):      # dạng 1 riêng (bản đã gộp tiến hoá)
            D.chep("ky_nguyen_1", RIG1, "ky_nguyen_non_th.atomik")
        D.chep("ky_nguyen_2", RIG2, "ky_nguyen.atomik")
        anh_hon("ky_nguyen_2")
    elif a[:1] == ["dang_1"]:
        D.heroes([(TEN_NON, "ky_nguyen_1", CO_1), (TEN, "ky_nguyen_2", CO_2)])
    else:
        D.heroes([(TEN_NON, "ky_nguyen_2", CO_1), (TEN, "ky_nguyen_2", CO_2)])
        D.cards()
