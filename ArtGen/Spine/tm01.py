# -*- coding: utf-8 -*-
"""Rig dòng tm01 (Tí Tách → Sóng Thần), dựng bằng mã với thư viện quai (đặc tả ArtGen/Spine/quai/DAC_TA_LO_THUY.md mục 5).

    py -3 -I ArtGen/Spine/tm01.py cat 2            cắt tờ mảnh dạng 2 (M01, M02) vào inbox/tm01_2/manh/
    py -3 -I ArtGen/Spine/tm01.py cat 1            cắt tờ mảnh dạng 1 (M01) vào inbox/tm01_1/manh/
    py -3 -I ArtGen/Spine/tm01.py ghep 2|1         ảnh so ghép dáng đứng với concept
    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/tm01.py sil 2|1   dò bố trí theo bóng dáng concept (sil.json)
      (dạng 2 dò từ khop.json: chỗ đặt từng mảnh đã dò theo màu bằng tm01_khop.py ở bản trước; ghi '{}' vào sil.json để dò lại từ đó)
    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/tm01.py rig 2     dựng + xuất dạng 2
    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/tm01.py rig 1     dựng dạng 1 + tiến hóa gộp dạng 2
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import numpy as np  # noqa: E402

from quai import anh  # noqa: E402

INBOX = os.path.join(HERE, "inbox")


def dir_of(k, sub):
    return os.path.join(INBOX, f"tm01_{k}", sub)


# ---------------------------------------------------------------- cắt tờ
# mỗi tờ: (bước, ô) với ô = [(x0, y0, x1, y1, [tên...], khoá sắp)] theo pixel tờ 1536 x 1024; mảnh rơi vào ô theo tâm khung bao.
TO = {
    2: [("M01", [(0, 0, 600, 512, ["dau"], "x"), (600, 0, 980, 512, ["ham"], "x"), (980, 0, 1536, 512, ["mieng_long", "mi"], "x"),
                 (0, 512, 470, 1024, ["mao_a", "mao_b"], "y"), (470, 512, 900, 1024, ["dai_a", "dai_b"], "y"),
                 (900, 512, 1536, 1024, ["duoi"], "x")]),
        ("M02", [(0, 0, 410, 512, ["than"], "x"), (410, 0, 860, 512, ["tay"], "x"), (860, 0, 1180, 512, ["nam"], "x"),
                 (1180, 0, 1536, 512, ["xoe"], "x"), (0, 512, 400, 1024, ["chan"], "x"), (400, 512, 800, 1024, ["ban_chan"], "x"),
                 (800, 512, 1180, 1024, ["giap_vai"], "x"), (1180, 512, 1536, 1024, ["dai_dai"], "x")]),
        ("M03", [(0, 0, 480, 1024, ["chan2"], "x"), (480, 0, 1536, 1024, ["duoi2"], "x")])],
    1: [("M01", [(0, 0, 620, 1024, ["than"], "x"),
                 (620, 120, 1060, 330, ["m_het", "m_tron"], "x"), (620, 330, 1060, 480, ["m_mim", "m_nghien"], "x"),
                 (1060, 100, 1536, 300, ["nham_gan", "nham_xa"], "x"), (1060, 300, 1536, 500, ["ep_gan", "ep_xa"], "x"),
                 (620, 520, 1060, 720, ["tay"], "x"), (620, 720, 1060, 1024, ["ban_chan"], "x"),
                 (1060, 500, 1536, 720, ["duoi"], "x"), (1060, 720, 1536, 1024, ["dai_a", "dai_b"], "y")])],
}


def gan_o(to, o):
    out, thua = {}, []
    groups = {i: [] for i in range(len(o))}
    for m in to.manh:
        cx, cy = (m["x0"] + m["x1"]) / 2, (m["y0"] + m["y1"]) / 2
        hit = [i for i, (x0, y0, x1, y1, _, _) in enumerate(o) if x0 <= cx < x1 and y0 <= cy < y1]
        (groups[hit[0]] if hit else thua).append(m)
    for i, (x0, y0, x1, y1, names, key) in enumerate(o):
        ms = sorted(groups[i], key=lambda m: -m["dt"])[:len(names)]
        if len(ms) < len(names):
            print(f"  THIẾU mảnh ở ô {names}: có {len(ms)}")
        thua += sorted(groups[i], key=lambda m: -m["dt"])[len(names):]
        f = {"x": lambda m: m["x0"] + m["x1"], "y": lambda m: m["y0"] + m["y1"]}[key]
        for nm, m in zip(names, sorted(ms, key=f)):
            out[nm] = m
    if thua:
        print("  mảnh thừa: " + ", ".join(f"({m['x0']},{m['y0']}) {m['x1'] - m['x0']}x{m['y1'] - m['y0']} dt {m['dt']}" for m in thua))
    return out


def cat(k):
    tv, ra = dir_of(k, "tai_ve"), dir_of(k, "manh")
    names = []
    for buoc, o in TO[k]:
        p = anh.to_moi_nhat(tv, buoc)
        to = anh.doc_to(p, dien_tich_min=200 if k == 1 else 900, gop_px=14 if k == 1 else 30)
        ten = gan_o(to, o)
        anh.luu_manh(to, ten, ra)
        names += list(ten)
    print(anh.to_soi(ra, names))


if __name__ == "__main__":
    cmd, k = sys.argv[1], int(sys.argv[2])
    if cmd == "cat":
        cat(k)
    else:
        import tm01_rig
        tm01_rig.main(cmd, k)
