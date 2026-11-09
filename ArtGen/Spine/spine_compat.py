# -*- coding: utf-8 -*-
"""Hai hàm thay cho repo spine-animation-ai (giấy phép PolyForm Noncommercial) khi máy không có repo đó, viết lại 2026-11-07:

- _convert_timeline(kind, frames): khoá kiểu bộ rig (curve chuẩn hoá [cx1, cy1, cx2, cy2] trong 0..1 gắn với khoá KẾT THÚC
  đoạn, rotate ghi "angle") -> JSON Spine 4.2 (curve bezier tuyệt đối theo (thời gian, giá trị) gắn với khoá BẮT ĐẦU đoạn, mỗi
  thuộc tính 4 số; rotate ghi "value"). "stepped" giữ nguyên. Sửa tại chỗ.
- pack(ims, padding=2): xếp ảnh theo hàng (cao trước), trả (rộng, cao, {tên: (x, y, w, h)}); cạnh atlas làm tròn lên bội 8 để
  nén khối (ASTC, DXT) không phải độn.
"""
import math

PROPS = {"rotate": ["value"], "alpha": ["value"], "translate": ["x", "y"], "scale": ["x", "y"], "shear": ["x", "y"]}


def _convert_timeline(kind, frames):
    props = PROPS.get(kind, ["value"])
    base = 1.0 if kind == "scale" else 0.0
    if kind == "rotate":
        for f in frames:
            if "angle" in f:
                f["value"] = f.pop("angle")
    ends = [f.pop("curve", None) for f in frames]
    for i in range(len(frames) - 1):
        a, b, c = frames[i], frames[i + 1], ends[i + 1]
        if c is None:
            continue  # thẳng (mặc định của Spine)
        if c == "stepped":
            a["curve"] = "stepped"
            continue
        t0, t1 = a.get("time", 0.0), b.get("time", 0.0)
        out = []
        for p in props:
            v0, v1 = a.get(p, base), b.get(p, base)
            out += [t0 + c[0] * (t1 - t0), v0 + c[1] * (v1 - v0), t0 + c[2] * (t1 - t0), v0 + c[3] * (v1 - v0)]
        a["curve"] = [round(float(x), 5) for x in out]
    return frames


def pack(ims, padding=2):
    items = sorted(ims.items(), key=lambda kv: (-kv[1].height, -kv[1].width))
    area = sum((im.width + padding) * (im.height + padding) for _, im in items)
    widest = max(im.width for _, im in items) + 2 * padding
    W = max(widest, int(math.sqrt(area * 1.15)))
    W = (W + 7) // 8 * 8
    place, x, y, row = {}, padding, padding, 0
    for name, im in items:
        if x + im.width + padding > W:
            x, y, row = padding, y + row + padding, 0
        place[name] = (x, y, im.width, im.height)
        x += im.width + padding
        row = max(row, im.height)
    H = (y + row + padding + 7) // 8 * 8
    return W, H, place
