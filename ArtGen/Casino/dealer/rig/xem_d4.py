# Ảnh động duyệt clip D4 của Lão Mực (GD_Claude/31 mục 4.3, lều Vòng Xoay). Như xem_d2.py nhưng khung nhìn rộng tới sát người chơi
# và bàn là bàn Vòng Xoay: chép project AtomSpine sang thư mục tạm, thêm mặt bàn nỉ có bảng cược + bánh xe vẽ tạm (chỉ để xem, không
# vào rig thật) với lớp vẽ thân, mặt, lưỡi trai < BÀN < tay, nịt, nơ, bi, bàn tay, đúng như trong game.
# Bố cục (clip_d4.py): rig tỉ lệ 0,7, mép bàn rig y 500; bảng cược rig x ±643, y 321..−357; bánh xe tâm rig (0, −714), vành ngoài
# bán kính 457, dẹt 0,6; mâm xoay 0,70; đường bi 0,875 ở độ cao 0,11; dấu + đỏ: chỗ tay trái bám mâm, cuối cú quất, chỗ bi vào đường.
# Ra: ../d4/<clip>.gif (30 khung/giây), <clip>_to.png (tờ 10 khung), và với --lon: ../d4/lon/<clip>_fNNN.png (khung lớn để soi).
# Chạy: py -3 -I xem_d4.py [clip ...] [--lon clip:giây,giây ...]
import json, math, os, shutil, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ATOM = os.path.abspath(os.path.join(HERE, "..", "atom"))
OUT = os.path.abspath(os.path.join(HERE, "..", "d4"))
TMP = os.path.join(os.environ.get("TEMP", "C:/Temp"), "lao_muc_xem_d4")
sys.path.insert(0, HERE)
from atom_cli import CLI, TSX, ATOMSPINE  # noqa: E402  (tìm AtomSpine, node theo máy đang chạy)

CLIPS = ["rl_invite", "rl_no_more", "rl_spin", "rl_watch", "rl_point"]
TABLE_Y = 500
FPS = 30
BOX = (-760, -1060, 760, 1420)      # khung nhìn (thế giới): rộng 1520, cao 2480 (màn 9:16 thấy rig x ±771)
GIF_W, GIF_H = 380, 620
BIG_W, BIG_H = 1140, 1860
WHEEL, WHEEL_R = (0.0, -714.0), 457.0
MARKS = [(140.0, -541.0), (-260.0, -603.0), (306.0, -520.0)]   # bám mâm, cuối cú quất, bi vào đường chạy
TW, TH = 1700, 1600                 # ảnh bàn: x −850..850, y 500..−1100


def atom(*args):
    r = subprocess.run(CLI + list(args) + ["-p", TMP], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print((r.stdout + r.stderr)[-800:])
        raise SystemExit("atom lỗi")
    return r.stdout


def px(x, y):
    return (x + TW / 2, TABLE_Y - y)


def ell(d, r, h, **kw):
    cx, cy = px(WHEEL[0], WHEEL[1] + WHEEL_R * 0.8 * h)
    d.ellipse([cx - WHEEL_R * r, cy - WHEEL_R * r * 0.6, cx + WHEEL_R * r, cy + WHEEL_R * r * 0.6], **kw)


def make_table():
    """Mặt bàn nỉ tím than tô phẳng, vân chì nhẹ, viền gỗ ở mép xa, bảng cược 6 x 6, bánh xe vẽ tạm."""
    rng = np.random.default_rng(3)
    felt = np.array([70, 52, 104], float)
    a = np.tile(felt, (TH, TW, 1))
    yy, xx = np.mgrid[0:TH, 0:TW]
    stroke = (np.sin((xx + yy * 1.7) * 0.9 + rng.normal(0, 1.2, (TH, TW))) > 0.86).astype(float)
    a = a * (1 - 0.10 * stroke[..., None]) + np.array([104, 84, 150]) * 0.10 * stroke[..., None]
    pil = Image.fromarray(np.dstack([a.clip(0, 255), np.full((TH, TW), 255.0)]).astype(np.uint8))
    d = ImageDraw.Draw(pil)
    d.rectangle([0, 0, TW, 26], fill=(122, 78, 44, 255))
    d.rectangle([0, 26, TW, 34], fill=(88, 54, 30, 255))
    d.rounded_rectangle([TW / 2 - 330, 40, TW / 2 + 330, 150], radius=10, outline=(122, 78, 44, 255), width=5)   # khay chip nhà cái
    x0, y0 = px(-643, 321)
    x1, y1 = px(643, -357)
    line = (232, 222, 190, 255)
    for i in range(7):
        xi = x0 + (x1 - x0) * i / 6
        yi = y0 + (y1 - y0) * i / 6
        d.line([(xi, y0), (xi, y1)], fill=line, width=3)
        d.line([(x0, yi), (x1, yi)], fill=line, width=3)
    ink = (59, 40, 30, 255)
    # thành ngoài (bề dày), vành gỗ, đường bi, mâm xoay, nón giữa
    ell(d, 1.0, -0.07, fill=(96, 60, 34, 255), outline=ink, width=4)
    ell(d, 1.0, 0.0, fill=(150, 98, 54, 255), outline=ink, width=4)
    ell(d, 0.93, 0.0, fill=(120, 76, 42, 255), outline=ink, width=3)
    ell(d, 0.70, 0.0, fill=(214, 190, 140, 255), outline=ink, width=4)
    ell(d, 0.44, 0.0, fill=(170, 120, 70, 255), outline=ink, width=3)
    ell(d, 0.10, 0.06, fill=(226, 180, 70, 255), outline=ink, width=3)
    for k in range(26):
        ang = math.radians(k * 360 / 26)
        p0 = px(WHEEL[0] + WHEEL_R * 0.44 * math.cos(ang), WHEEL[1] + WHEEL_R * 0.44 * 0.6 * math.sin(ang))
        p1 = px(WHEEL[0] + WHEEL_R * 0.70 * math.cos(ang), WHEEL[1] + WHEEL_R * 0.70 * 0.6 * math.sin(ang))
        d.line([p0, p1], fill=ink, width=2)
    ell(d, 0.875, 0.11, outline=(240, 230, 200, 255), width=2)     # đường bi chạy
    for mx, my in MARKS:
        cx, cy = px(mx, my)
        d.line([(cx - 14, cy), (cx + 14, cy)], fill=(230, 40, 40, 255), width=4)
        d.line([(cx, cy - 14), (cx, cy + 14)], fill=(230, 40, 40, 255), width=4)
    return pil


def setup_tmp():
    if os.path.isdir(TMP):
        shutil.rmtree(TMP)          # thư mục tạm của chính script này
    os.makedirs(TMP)
    shutil.copy(os.path.join(ATOM, "atomspine.json"), TMP)
    shutil.copytree(os.path.join(ATOM, "images"), os.path.join(TMP, "images"))
    make_table().save(os.path.join(TMP, "images", "xem_ban.png"))
    # canvas 1024 x 1536, gốc (512, 1460): toạ độ ảnh = (x + 512, 1460 − y)
    ops = [
        f"part.add xem_ban path=images/xem_ban.png at={512 - TW // 2},{1460 - TABLE_Y} canvas=1024,1536 origin=512,1460 bone=root",
        "slot.order xem_ban to=before:tay_trai",
    ]
    open(os.path.join(TMP, "xem.ops"), "w", encoding="utf-8").write("\n".join(ops) + "\n")
    atom("do", "-f", os.path.join(TMP, "xem.ops"))


def sheets(names, w, h, cols, fps=FPS):
    r = subprocess.run(TSX + [os.path.join(HERE, "khung.mts"), TMP, TMP, str(fps), ",".join(map(str, BOX)), str(w), str(h), str(cols),
                              ",".join(names)], capture_output=True, text=True, encoding="utf-8", errors="replace",
                       env=dict(os.environ, ATOMSPINE_DIR=ATOMSPINE))
    if r.returncode != 0:
        print((r.stdout + r.stderr)[-1500:])
        raise SystemExit("khung.mts lỗi")
    info = {}
    for ln in r.stdout.splitlines():
        p = ln.split()
        if len(p) == 3 and p[1].isdigit():
            info[p[0]] = (int(p[1]), float(p[2]))
    return info


def main():
    args = sys.argv[1:]
    big = []
    if "--lon" in args:
        i = args.index("--lon")
        big = args[i + 1:]
        args = args[:i]
    names = args or (CLIPS if not big else [])
    os.makedirs(OUT, exist_ok=True)
    setup_tmp()
    if names:
        cols = 12
        info = sheets(names, GIF_W, GIF_H, cols)
        loops = {a["name"]: a.get("loop", False) for a in json.load(open(os.path.join(TMP, "atomspine.json"), encoding="utf-8"))["anims"]}
        for c in names:
            n, dur = info[c]
            im = Image.open(os.path.join(TMP, f"{c}_sheet.png")).convert("RGB")
            frames = [im.crop(((k % cols) * GIF_W, (k // cols) * GIF_H, (k % cols + 1) * GIF_W, (k // cols + 1) * GIF_H)) for k in range(n)]
            seq = frames[:-1] if loops.get(c) else frames
            durs = [30 if k % 3 else 40 for k in range(len(seq))]
            if not loops.get(c):
                durs[-1] = 700      # clip một lần: nghỉ một nhịp trước khi lặp lại
            pal = seq[0].quantize(colors=96, method=Image.MEDIANCUT, dither=Image.NONE)
            q = [f.quantize(palette=pal, dither=Image.NONE) for f in seq]
            q[0].save(os.path.join(OUT, f"{c}.gif"), save_all=True, append_images=q[1:], duration=durs, loop=0, optimize=False)
            pick = [frames[int(round(k * (n - 1) / 9))] for k in range(10)]
            cw, chh = 266, 434
            to = Image.new("RGB", (cw * 10, chh), (255, 255, 255))
            for k, f in enumerate(pick):
                to.paste(f.resize((cw, chh), Image.LANCZOS), (k * cw, 0))
            to.save(os.path.join(OUT, f"{c}_to.png"))
            # tờ MỌI khung (để soi cú quất / cú búng từng khung)
            im.save(os.path.join(OUT, f"{c}_moi_khung.png"))
            print(c, n, "khung", dur, "s")
    if big:
        os.makedirs(os.path.join(OUT, "lon"), exist_ok=True)
        for item in big:
            c, ts = item.split(":")
            info = sheets([c], BIG_W, BIG_H, 10, fps=FPS)
            n, dur = info[c]
            im = Image.open(os.path.join(TMP, f"{c}_sheet.png")).convert("RGB")
            for t in ts.split(","):
                k = min(n - 1, int(round(float(t) * FPS)))
                f = im.crop(((k % 10) * BIG_W, (k // 10) * BIG_H, (k % 10 + 1) * BIG_W, (k // 10 + 1) * BIG_H))
                f.save(os.path.join(OUT, "lon", f"{c}_f{k:03d}.png"))
            print(c, "khung lớn", ts)


if __name__ == "__main__":
    main()
