# -*- coding: utf-8 -*-
"""Đo trên rig quỷ xích các điểm lớp hạt cần bám (HatXich.cs): theo từng khung 30 / giây của clip skill và cast.

- MOC: tâm lưỡi móc ở đầu xích dài (slot W_wuqi2 / W_wuqi2_sau, xương bone14b11) lúc QUAY xích; cờ hiện (rig chỉ hiện lúc quay).
- XICH: ba điểm giữa xích dài (gốc xương bone14b14, bone14b16, bone14b18) lúc quay.
- TAY: chỗ xích nối vào cán móc tay (vòng cuối cán, xương bone14b2 · MOC_TRUC[0]): gốc xích căng lúc ném / giữ / giật.
Đơn vị: phần của chiều cao KHAI cho game (`height` trong <tên>_game.json), x về phía trước (phía đối thủ), y lên, gốc = chân (root).
In ra mảng C# để dán vào HatXich.cs. Đổi clip hay tỉ lệ rig thì đo lại.

    QX_DANG=non py -3 -I ArtGen/Spine/quy_xich_do_hat.py      dạng 1 non (tiền tố Xq1)
    py -3 -I ArtGen/Spine/quy_xich_do_hat.py                  dạng 2 (tiền tố Xq2)
"""
import json
import os
import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import quy_xich_rig as R  # noqa: E402


def f3(v):
    return f"{v:.3f}f"


def main():
    sk0, _ = R.dung_tam()
    R.do_truc_moc(sk0)
    sk, info = R.dung()
    clips = {c.ten: c for c in R.lam_clip(sk, info)}
    g = json.load(open(os.path.join(R.RA, R.TEN + "_game.json"), encoding="utf-8"))
    cao = float(g["height"])
    tien = "Xq1" if R.NON else "Xq2"
    print(f"        // {R.TEN}: chiều cao khai {cao:.1f}; skill {clips['skill'].dur:.3f} s, trúng {clips['skill'].gio_trung():.3f}; "
          f"cast {clips['cast'].dur:.3f} s, trúng {clips['cast'].gio_trung():.3f}")
    vong = np.array([*R.MOC_TRUC[0], 1.0])
    for ten in ("skill", "cast"):
        fr = R.nuong(sk, clips[ten])
        M, MH, X, T = [], [], [], []
        for P in fr:
            W = sk.the_gioi(P)
            sl = "W_wuqi2_sau" if P.alpha.get("W_wuqi2_sau", 0) > 0.5 else "W_wuqi2"
            hien = P.alpha.get(sl, 0) > 0.5
            sp = list(sk.atts[sl].values())[0]
            loc = np.array([[r_[0][1], r_[0][2]] for r_ in sp["verts"]]).mean(0)
            b = sp["verts"][0][0][0]
            m = (W[b] @ np.array([*loc, 1.0]))[:2] / cao
            M.append(m)
            MH.append(1 if hien else 0)
            X.append(np.concatenate([W[bn][:2, 2] / cao for bn in ("bone14b14", "bone14b16", "bone14b18")]))
            T.append((W["bone14b2"] @ vong)[:2] / cao)
        M, X, T = np.array(M), np.array(X), np.array(T)
        k = "S" if ten == "skill" else "C"
        print(f"        static readonly float[] {tien}{k}MocX = {{ " + ", ".join(f3(v) for v in M[:, 0]) + " };")
        print(f"        static readonly float[] {tien}{k}MocY = {{ " + ", ".join(f3(v) for v in M[:, 1]) + " };")
        print(f"        static readonly byte[] {tien}{k}MocHien = {{ " + ", ".join(str(v) for v in MH) + " };")
        for j in range(3):
            print(f"        static readonly float[] {tien}{k}Xich{j}X = {{ " + ", ".join(f3(v) for v in X[:, 2 * j]) + " };")
            print(f"        static readonly float[] {tien}{k}Xich{j}Y = {{ " + ", ".join(f3(v) for v in X[:, 2 * j + 1]) + " };")
        print(f"        static readonly float[] {tien}{k}TayX = {{ " + ", ".join(f3(v) for v in T[:, 0]) + " };")
        print(f"        static readonly float[] {tien}{k}TayY = {{ " + ", ".join(f3(v) for v in T[:, 1]) + " };")
        on = [i for i, v in enumerate(MH) if v]
        print(f"        // {ten}: móc quay hiện khung {on[0] if on else '-'}–{on[-1] if on else '-'} ({len(on)} khung)", file=sys.stderr)


if __name__ == "__main__":
    main()
