"""Đọc và vẽ một dạng tướng aola ĐÃ NHẬP vào project (Assets/03 Art/Heroes/Resources/<dạng>/), không cần thư mục ghép của
AolaRipper (lô Thủy 2026-11-07 ghép ở máy ổ D, máy E không có).

- <dạng>_anim.bytes: anim.json gzip (fps, clips, idle_parts, cast, lunge, far_center, anim_moi: root, parent, pivot);
- <dạng>.asset: sizes (cỡ gốc mỗi hình, ma trận tính theo cỡ này), uvs (chỗ trong atlas, gốc dưới trái), shadow;
- <dạng>_atlas.png: mọi hình đã thu nhỏ.

    from aola_form import Form
    f = Form("thuy_1831")            # bản đang có trong project
    f = Form("thuy_1831", rev="4d7557b")  # bản ở một commit (gốc để dựng lại, chạy lại không cộng dồn)
    img = f.render(f.clips["1_4"]["frames"][18])
"""
import gzip
import io
import json
import os
import re
import subprocess

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
RES = "Assets/03 Art/Heroes/Resources"


def _read(rel, rev=None):
    if rev is None:
        return open(os.path.join(PROJECT, rel), "rb").read()
    return subprocess.run(["git", "-C", PROJECT, "show", f"{rev}:{rel}"], capture_output=True, check=True).stdout


def parse_asset(text):
    sizes = [(float(a), float(b)) for a, b in re.findall(r"^  - \{x: ([\d.]+), y: ([\d.]+)\}", text, re.M)]
    uvs = []
    for m in re.finditer(r"serializedVersion: 2\s+x: ([-\d.eE]+)\s+y: ([-\d.eE]+)\s+width: ([-\d.eE]+)\s+height: ([-\d.eE]+)", text):
        uvs.append(tuple(float(v) for v in m.groups()))
    sh = re.search(r"^  shadow: (-?\d+)", text, re.M)
    return sizes, uvs, int(sh.group(1)) if sh else -1


class Form:
    def __init__(self, form, rev=None):
        self.form = form
        base = f"{RES}/{form}/{form}"
        self.anim = json.loads(gzip.decompress(_read(base + "_anim.bytes", rev)))
        self.asset_text = _read(base + ".asset", rev).decode("utf-8")
        self.sizes, self.uvs, self.shadow = parse_asset(self.asset_text)
        self.atlas = Image.open(io.BytesIO(_read(base + "_atlas.png", rev))).convert("RGBA")
        assert len(self.sizes) == len(self.uvs), (form, len(self.sizes), len(self.uvs))
        self._spr = {}

    @property
    def clips(self):
        return self.anim["clips"]

    def sprite(self, i):
        """hình i ở cỡ gốc (sizes), cắt từ atlas rồi phóng lại"""
        if i not in self._spr:
            W, H = self.atlas.size
            x, y, w, h = self.uvs[i]
            box = (round(x * W), round((1 - y - h) * H), round((x + w) * W), round((1 - y) * H))
            im = self.atlas.crop(box)
            sw, sh = self.sizes[i]
            sw, sh = max(1, round(sw)), max(1, round(sh))
            if im.size != (sw, sh):
                im = im.resize((sw, sh), Image.BICUBIC)
            self._spr[i] = im
        return self._spr[i]

    def bbox(self, row):
        s, a, b, c, d, tx, ty = row[:7]
        w, h = self.sizes[s]
        xs = [a * x + c * y + tx for x, y in ((0, 0), (w, 0), (0, h), (w, h))]
        ys = [b * x + d * y + ty for x, y in ((0, 0), (w, 0), (0, h), (w, h))]
        return min(xs), min(ys), max(xs), max(ys)

    def render(self, rows, view=None, scale=2.0, bg=(255, 255, 255, 255), far=None):
        """vẽ một khung; view (x0, y0, x1, y1) toạ độ clip; far: (dx, dy) cộng vào hình ở xa (thử kéo về đối thủ)"""
        if view is None:
            bs = [self.bbox(r) for r in rows]
            view = (min(b[0] for b in bs) - 10, min(b[1] for b in bs) - 10, max(b[2] for b in bs) + 10, max(b[3] for b in bs) + 10)
        x0, y0, x1, y1 = view
        W, H = max(1, int((x1 - x0) * scale)), max(1, int((y1 - y0) * scale))
        out = Image.new("RGBA", (W, H), bg)
        for r in rows:
            s, a, b, c, d, tx, ty = r[:7]
            alpha = r[7] if len(r) > 7 else 1
            if alpha <= 0.01:
                continue
            im = self.sprite(s)
            # điểm ảnh đích (X, Y) = scale * (M · p + t - v0) → nghịch đảo cho Image.transform
            A, B, C, D = a * scale, b * scale, c * scale, d * scale
            TX, TY = (tx - x0) * scale, (ty - y0) * scale
            det = A * D - B * C
            if abs(det) < 1e-9:
                continue
            ia, ib, ic, id_ = D / det, -C / det, -B / det, A / det
            coeffs = (ia, ib, -(ia * TX + ib * TY), ic, id_, -(ic * TX + id_ * TY))
            layer = im.transform((W, H), Image.AFFINE, coeffs, resample=Image.BILINEAR)
            if alpha < 1:
                al = layer.getchannel("A").point(lambda v: int(v * alpha))
                layer.putalpha(al)
            out.alpha_composite(layer)
        return out
