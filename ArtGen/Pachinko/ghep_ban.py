# Ghép phần tĩnh của mặt máy bi (Assets/03 Art/Baked/Machine/may_tinh.png, 920 x 1360 = 2 lần khung máy 460 x 680) theo
# đúng hình học bàn trong code (Board.Build, Assets/01 Script/Core/Pachinko.cs), xuất ra refs/mat_may.json.
# Bàn chép bàn table_01 của máy bi tham khảo: khung vòm 26 điểm, 22 đinh, mái hai cánh, đáy V có ba núm, 4 vách, 5 ô, cốc dưới mái,
# làn phóng ngoài mép phải. Hình vẽ tay lấy từ tờ bộ phận GPT đã duyệt (tai_ve/bo_phan.png, 12 ô): đinh, cọc vách, thanh mái,
# núm, cốc. Phần ngoài vòm, viền vòm, làn phóng vẽ bằng script theo cùng nét (mực nâu sẫm, tô màu gạch chéo như ô đáy) để khớp
# toạ độ va chạm từng điểm. Nấm đỉnh, hai nấm lớn, bi là hình động trong game (không vẽ ở đây).
# Ghi thêm Assets/03 Art/Pachinko/pk_nam_dinh.png (nấm đỉnh, từ núm cam của tờ bộ phận).
#   py -3 -I ArtGen/Pachinko/ghep_ban.py            (ghép, ghi ảnh game)
#   py -3 -I ArtGen/Pachinko/ghep_ban.py --soi out.png  (thêm ảnh soi: va chạm vẽ đè lên ảnh ghép)
#   py -3 -I ArtGen/Pachinko/ghep_ban.py --ra thu.png   (ghi ảnh ghép ra chỗ khác, không đụng ảnh game)
# Đổi hình học trong Pachinko.cs thì xuất lại refs/mat_may.json (menu Unity "PokiClash/Prefab/Máy bi: xuất hình học mặt máy",
# Board.GeometryJson) rồi chạy lại script này; test PachinkoTests.MatMay_AnhGhepKhopHinhHoc báo khi file lệch code.
import importlib.util
import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

sys.stdout.reconfigure(encoding="utf-8")
sys.dont_write_bytecode = True  # nạp build.py không để lại __pycache__
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("pk_build", HERE / "build.py")
pk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pk)

GEOM = HERE / "refs" / "mat_may.json"
PARTS = HERE / "tai_ve" / "bo_phan.png"
OUT = pk.BOARD_PNG

INK = (43, 33, 24, 255)
SURROUND = (252, 116, 84)  # đỏ cam của thân máy (pk_than_may)
WOOD = (214, 140, 82)
LANE_BG = (251, 236, 205)
CHEVRON = (247, 201, 72)
SLOT_COLOR = dict(pk.SLOT_COLOR)


def ring_sprite(size=256, inner=0.8):
    """vòng mỏng cho vòng tiến độ của nấm lớn: nền trắng có gạch chéo nhạt (game tô màu), mực hai mép; trong suốt ở giữa"""
    ss = 4
    n = size * ss
    im = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = n / 2
    ro, ri, ink = c - 2 * ss, (c - 2 * ss) * inner, 3.2 * ss
    d.ellipse([c - ro, c - ro, c + ro, c + ro], fill=INK)
    d.ellipse([c - ro + ink, c - ro + ink, c + ro - ink, c + ro - ink], fill=(255, 255, 255, 255))
    d.ellipse([c - ri, c - ri, c + ri, c + ri], fill=INK)
    d.ellipse([c - ri + ink, c - ri + ink, c + ri - ink, c + ri - ink], fill=(0, 0, 0, 0))
    # gạch chéo nhạt trên nền trắng (chỉ trong dải)
    band = Image.new("L", (n, n), 0)
    bd = ImageDraw.Draw(band)
    bd.ellipse([c - ro + ink, c - ro + ink, c + ro - ink, c + ro - ink], fill=255)
    bd.ellipse([c - ri, c - ri, c + ri, c + ri], fill=0)
    lines = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lines)
    for t in range(-n, 2 * n, 9 * ss):
        ld.line([(t, n), (t + n, 0)], fill=(225, 220, 210, 255), width=2 * ss)
    clip = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    clip.paste(lines, (0, 0), band)
    im.alpha_composite(clip)
    return im.resize((size, size), Image.LANCZOS)


def plate_sprite(size=192):
    """đĩa kem viền mực lót sau hình quà giữa nấm lớn"""
    ss = 4
    n = size * ss
    im = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c, r, ink = n / 2, n / 2 - 2 * ss, 3.4 * ss
    d.ellipse([c - r, c - r, c + r, c + r], fill=INK)
    d.ellipse([c - r + ink, c - r + ink, c + r - ink, c + r - ink], fill=(255, 246, 224, 255))
    lines = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lines)
    for t in range(-n, 2 * n, 9 * ss):
        ld.line([(t, n), (t + n, 0)], fill=(246, 230, 200, 255), width=2 * ss)
    mask = Image.new("L", (n, n), 0)
    ImageDraw.Draw(mask).ellipse([c - r + ink, c - r + ink, c + r - ink, c + r - ink], fill=255)
    clip = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    clip.paste(lines, (0, 0), mask)
    im.alpha_composite(clip)
    return im.resize((size, size), Image.LANCZOS)


def main():
    g = json.loads(GEOM.read_text(encoding="utf-8"))
    BW, BH, U = int(g["bw"]), int(g["bh"]), g["u"]
    SS, OUTK = 2, 2
    K = SS * OUTK
    parts = pk.cut_cells(PARTS, 4, 3, split=True)
    peg, _bumper, bump, post, cup, roof, _floor, _cloud, _ball, shoulder, _rail, _plate = parts
    img = Image.new("RGBA", (BW * K, BH * K), (0, 0, 0, 0))

    def P(x, y):
        return (x * K, y * K)

    def put(spr, cx, cy, w, h=None, angle=0):
        h = h if h is not None else w * spr.height / spr.width
        im = spr.resize((max(1, round(w * K)), max(1, round(h * K))), Image.LANCZOS)
        if angle:
            im = im.rotate(-angle, resample=Image.BICUBIC, expand=True)
        img.alpha_composite(im, (round(cx * K - im.width / 2), round(cy * K - im.height / 2)))

    def plank(spr, x1, y1, x2, y2, thick, extra):
        length = math.hypot(x2 - x1, y2 - y1) + 2 * extra
        im = pk.three_slice(spr, length * K, thick * K)
        ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
        im = im.rotate(-ang, resample=Image.BICUBIC, expand=True)
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        img.alpha_composite(im, (round(cx * K - im.width / 2), round(cy * K - im.height / 2)))

    def hatch(size, rgb, step=5, width=2, base_a=89):
        """lớp tô màu nhạt kèm gạch chéo đậm (như ô đáy cũ)"""
        layer = Image.new("RGBA", size, rgb + (base_a,))
        d = ImageDraw.Draw(layer)
        span = size[0] + size[1]
        for t in range(-size[1], span, step * K):
            d.line([(t, size[1]), (t + size[1], 0)], fill=rgb + (255,), width=width * K)
        return layer

    def paste_masked(layer, mask):
        clipped = Image.new("RGBA", img.size, (0, 0, 0, 0))
        clipped.paste(layer, (0, 0), mask)
        img.alpha_composite(clipped)

    # khung vòm: nối các đoạn tường theo thứ tự thành đa giác
    walls = [s for s in g["segs"] if s[5] == "Wall"]
    poly = [(walls[0][0], walls[0][1])] + [(s[2], s[3]) for s in walls]
    inside = Image.new("L", img.size, 0)
    ImageDraw.Draw(inside).polygon([P(x, y) for x, y in poly], fill=255)
    outside = Image.eval(inside, lambda v: 255 - v)

    # 1. ngoài vòm: đỏ cam của thân máy, gạch chéo đậm hơn
    sur = Image.new("RGBA", img.size, SURROUND + (255,))
    d = ImageDraw.Draw(sur)
    for t in range(-img.height, img.width + img.height, 7 * K):
        d.line([(t, img.height), (t + img.height, 0)], fill=(236, 92, 64, 255), width=K)
    paste_masked(sur, outside)

    # 2. chấm trang trí trên mặt chơi (trong vòm)
    dots = Image.new("RGBA", img.size, (0, 0, 0, 0))
    dd = ImageDraw.Draw(dots)
    y = 60
    while y < BH - 120:
        x = 12 + ((y / 22) % 2) * 11
        while x < BW - 6:
            dd.ellipse([(x - 2.2) * K, (y - 2.2) * K, (x + 2.2) * K, (y + 2.2) * K], fill=(232, 85, 63, 31))
            x += 22
        y += 22
    paste_masked(dots, inside)

    # 3. ô đáy: tô theo loại ô, cắt theo khung
    for x0, y0, x1, y1, kind in g["slots"]:
        box = Image.new("L", img.size, 0)
        ImageDraw.Draw(box).rectangle([P(x0, y0), P(x1, BH)], fill=255)
        mask = Image.fromarray(__import__("numpy").minimum(__import__("numpy").array(box), __import__("numpy").array(inside)))
        paste_masked(hatch(img.size, SLOT_COLOR[kind]), mask)
    d = ImageDraw.Draw(img)
    slot_top = min(s[1] for s in g["slots"])
    d.line([P(0, slot_top), P(BW, slot_top)], fill=(43, 33, 24, 70), width=K)

    # 4. viền vòm: dải gỗ phía ngoài cạnh va chạm, mực hai mép
    T = 7
    band_ink = Image.new("L", img.size, 0)
    ImageDraw.Draw(band_ink).line([P(x, y) for x, y in poly], fill=255, width=round((2 * T + 3) * K), joint="curve")
    band = Image.new("L", img.size, 0)
    ImageDraw.Draw(band).line([P(x, y) for x, y in poly], fill=255, width=round(2 * T * K), joint="curve")
    np = __import__("numpy")
    o = np.array(outside)
    paste_masked(Image.new("RGBA", img.size, INK), Image.fromarray(np.minimum(np.array(band_ink), o)))
    wood = hatch(img.size, WOOD, step=4, width=1, base_a=255)
    paste_masked(wood, Image.fromarray(np.minimum(np.array(band), o)))
    ImageDraw.Draw(img).line([P(x, y) for x, y in poly], fill=INK, width=round(1.6 * K), joint="curve")

    # 5. làn phóng: rãnh kem viền mực, mũi tên vàng hướng lên dọc làn
    lane = g["lane"]
    lw = g["lane_half"]
    d = ImageDraw.Draw(img)
    pts = [P(x, y) for x, y in lane]
    d.line(pts, fill=INK, width=round((2 * lw + 3.2) * K), joint="curve")
    d.line(pts, fill=LANE_BG + (255,), width=round(2 * lw * K), joint="curve")
    for (x, y) in (lane[0], lane[-1]):
        pass
    # nắp tròn đầu làn dưới (bệ phóng)
    x0, y0 = lane[0]
    d.ellipse([P(x0 - lw - 1.6, y0 - 2), P(x0 + lw + 1.6, y0 + 2 * lw + 1.6)], fill=INK)
    d.ellipse([P(x0 - lw, y0 - 0.4), P(x0 + lw, y0 + 2 * lw)], fill=LANE_BG + (255,))
    # mũi tên trên đoạn dọc
    vx = lane[0][0]
    top = lane[1][1]
    yy = y0 - 18
    while yy > top + 14:
        cw, ch = lw * 0.62, lw * 0.5
        tri = [P(vx, yy - ch), P(vx + cw, yy + ch * 0.6), P(vx + cw * 0.45, yy + ch * 0.6), P(vx, yy - ch * 0.15),
               P(vx - cw * 0.45, yy + ch * 0.6), P(vx - cw, yy + ch * 0.6)]
        d.polygon(tri, fill=CHEVRON + (255,), outline=INK, width=round(0.9 * K))
        yy -= 24

    # 6. vách ô: cọc vẽ tay (núm tròn trên đầu, thân tới đáy máy)
    knob_h = post.width
    tops = [s for s in g["segs"] if s[5] == "Divider"]
    for x1, y1, x2, y2, r, _ in tops:
        wdt = 2 * r
        s = wdt / post.width
        top_img = post.crop((0, 0, post.width, knob_h))
        stick = post.crop((0, knob_h, post.width, post.height))
        ytop = y1 - r
        stick_len = BH - (ytop + knob_h * s) + 1
        put(stick, x1, ytop + knob_h * s + stick_len / 2 - 0.5, post.width * s * 0.9, stick_len)
        put(top_img, x1, ytop + knob_h * s / 2, wdt, knob_h * s)

    # 7. cốc dưới mái (cảm biến cốc thẻ), mái hai cánh, đáy V và núm
    for x0, y0, x1, y1, _ in g["cups"]:
        cw = (x1 - x0) * 0.86
        put(cup, (x0 + x1) / 2, y0 + (y1 - y0) * 0.6, cw, cw * cup.height / cup.width)
    for x1, y1, x2, y2, r, kind in g["segs"]:
        if kind in ("Roof", "Floor"):
            spr = roof if x2 > x1 else roof.transpose(Image.FLIP_LEFT_RIGHT)
            plank(spr, x1, y1, x2, y2, 2 * r, r)
    for x, y, r, kind in g["pegs"]:
        if kind == "Post":
            put(bump, x, y, 2 * r + 1.5)

    # 8. đinh
    for x, y, r, kind in g["pegs"]:
        if kind == "Peg":
            put(peg, x, y, 2 * r + 2)

    out = img.resize((BW * OUTK, BH * OUTK), Image.LANCZOS)
    dst = Path(sys.argv[sys.argv.index("--ra") + 1]) if "--ra" in sys.argv else OUT
    out.save(dst, optimize=True)
    print(f"  mặt máy tĩnh {dst} {out.width} x {out.height}, {dst.stat().st_size // 1024} KB")
    if dst == OUT:
        pk.save_game(pk.fit(pk.square(bump, 0.03), 128), "pk_nam_dinh")
        pk.save_game(ring_sprite(), "pk_vong_nam")
        pk.save_game(plate_sprite(), "pk_dia_nam")

    if "--soi" in sys.argv:
        dst = Path(sys.argv[sys.argv.index("--soi") + 1])
        soi = Image.new("RGBA", out.size, (251, 244, 226, 255))
        soi.alpha_composite(out)
        d = ImageDraw.Draw(soi)
        k = OUTK
        for x, y, r, kind in g["pegs"]:
            d.ellipse([(x - r) * k, (y - r) * k, (x + r) * k, (y + r) * k], outline=(0, 160, 255, 255), width=2)
        for x1, y1, x2, y2, r, kind in g["segs"]:
            d.line([x1 * k, y1 * k, x2 * k, y2 * k], fill=(0, 160, 255, 255), width=max(2, round(2 * r * k)) if r else 2)
        for x0, y0, x1, y1, _ in g["cups"] + g["slots"]:
            d.rectangle([x0 * k, y0 * k, x1 * k, y1 * k], outline=(0, 200, 90, 255), width=2)
        soi.save(dst)
        print(f"  ảnh soi {dst}")


if __name__ == "__main__":
    main()
