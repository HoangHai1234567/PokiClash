"""Sửa nhẹ ảnh nhóm mảnh GPT vẽ (giữ ảnh gốc, lưu ảnh mới cạnh nó; bộ ghép lấy ảnh mới nhất của nhóm).

  py -3 -I tools/sua_manh.py doi  <ảnh.png> <dx> <dy>   dời cả ảnh (GPT vẽ lệch chỗ gốc khớp)  -> <tên>_doi_cho.png
  py -3 -I tools/sua_manh.py vien <ảnh.png> <px>        nới viền ngoài ra phía ngoài px điểm   -> <tên>_vien_day.png

Nới viền: tô mực (màu lấy từ mép nét) lên nền sát hình. "Nền" tính cả quầng sáng quanh nét của GPT (điểm có min kênh > 110
nối với mép ảnh) và tô sẫm mép ngoài 3 px của nét cũ, nếu không sẽ còn một vòng sáng mảnh giữa nét cũ và phần nới.
Khe hẹp hơn 2 × px giữa hai phần (mũi đinh ba...) sẽ bị lấp: soi lại sau khi chạy.
"""
import os
import sys

import cv2
import numpy as np
from PIL import Image


def doi(path, dx, dy):
    a = np.asarray(Image.open(path).convert("RGB"))
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    b = cv2.warpAffine(a, M, (a.shape[1], a.shape[0]), borderValue=(255, 255, 255))
    lost = (np.asarray(a).min(2) < 235).sum() - (b.min(2) < 235).sum()
    out = os.path.splitext(path)[0] + "_doi_cho.png"
    Image.fromarray(b).save(out, optimize=True)
    print(out, f"(mất {lost} điểm ra ngoài khung)" if lost > 50 else "")


def vien(path, r):
    a = np.asarray(Image.open(path).convert("RGB")).astype(np.float32)
    near = (a.min(2) > 110).astype(np.uint8)
    _, lab = cv2.connectedComponents(near, connectivity=4)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    ext = np.isin(lab, sorted(border))
    din = cv2.distanceTransform((~ext).astype(np.uint8), cv2.DIST_L2, 5)
    dout = cv2.distanceTransform(ext.astype(np.uint8), cv2.DIST_L2, 5)
    ink = np.median(a[(~ext) & (din < 4)], 0)
    out = a.copy()
    edge = (~ext) & (din <= 3)
    out[edge] = np.minimum(a[edge], ink)
    al = (np.clip(r + 0.5 - dout, 0, 1) * ext)[..., None]
    out = out * (1 - al) + ink * al
    p = os.path.splitext(path)[0] + "_vien_day.png"
    Image.fromarray(out.round().astype(np.uint8)).save(p, optimize=True)
    print(p, "mực", ink.round().astype(int).tolist())


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    cmd, path, *v = sys.argv[1:]
    if cmd == "doi":
        doi(path, int(v[0]), int(v[1]))
    elif cmd == "vien":
        vien(path, float(v[0]))
    else:
        sys.exit(__doc__)
