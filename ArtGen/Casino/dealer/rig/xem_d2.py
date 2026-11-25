# Ảnh động duyệt clip D2 của Lão Mực (GD_Claude/31, bản 2). Chép project AtomSpine sang thư mục tạm, thêm mặt bàn nỉ + chồng chip
# (chỉ để xem, không vào rig thật) với lớp vẽ: thân, mặt, lưỡi trai < BÀN, chip < tay, nịt, nơ, bàn tay — đúng như trong game (tay vươn
# ra trước bàn). Khung nhìn CỐ ĐỊNH như camera game (khung.mts gọi thẳng lõi AtomSpine), 30 khung/giây (bản 1 chỉ 15 nên tự nó đã giật).
# Ra: ../d2/<clip>.gif (30 khung/giây), <clip>_to.png (tờ 10 khung), và với --lon: ../d2/lon/<clip>_fNN.png (khung lớn để soi).
# Chạy: py -3 -I xem_d2.py [clip ...] [--lon clip:giây,giây ...]
import os, shutil, subprocess, sys, json
import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ATOM = os.path.abspath(os.path.join(HERE, "..", "atom"))
OUT = os.path.abspath(os.path.join(HERE, "..", "d2"))
TMP = os.path.join(os.environ.get("TEMP", "C:/Temp"), "lao_muc_xem")
CLI = ["node", "D:/AtomSpine/packages/cli/dist/atom.mjs"]
TSX = ["node", "D:/AtomSpine/node_modules/tsx/dist/cli.mjs"]
CLIPS = ["idle", "greet", "talk", "bet_watch", "take", "pay", "react_win_small", "react_win_big", "react_lose", "react_push",
         "grumpy", "sulk"]
TABLE_Y = 500   # thế giới, trùng dong_co.TABLE_Y
CHIP = (0, 120)  # ô cược của người chơi, trùng hoat_anh.CHIP
FPS = 30
BOX = (-480, -60, 480, 1500)      # khung nhìn (thế giới): rộng 960, cao 1560
GIF_W, GIF_H = 384, 624


def atom(*args):
    r = subprocess.run(CLI + list(args) + ["-p", TMP], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print((r.stdout + r.stderr)[-800:])
        raise SystemExit("atom lỗi")
    return r.stdout


def make_table():
    """Mặt bàn nỉ xanh tô phẳng, vân chì nhẹ, viền gỗ ở mép xa."""
    w, h = 1500, 600
    rng = np.random.default_rng(3)
    felt = np.array([47, 107, 74], float)
    a = np.tile(felt, (h, w, 1))
    yy, xx = np.mgrid[0:h, 0:w]
    stroke = (np.sin((xx + yy * 1.7) * 0.9 + rng.normal(0, 1.2, (h, w))) > 0.86).astype(float)
    a = a * (1 - 0.10 * stroke[..., None]) + np.array([70, 140, 98]) * 0.10 * stroke[..., None]
    img = np.dstack([a.clip(0, 255), np.full((h, w), 255.0)]).astype(np.uint8)
    pil = Image.fromarray(img)
    d = ImageDraw.Draw(pil)
    d.rectangle([0, 0, w, 26], fill=(122, 78, 44, 255))
    d.rectangle([0, 26, w, 34], fill=(88, 54, 30, 255))
    d.ellipse([w / 2 - 95, TABLE_Y - CHIP[1] - 42, w / 2 + 95, TABLE_Y - CHIP[1] + 42], outline=(232, 222, 190, 255), width=4)  # ô cược
    d.rounded_rectangle([w / 2 - 150, 44, w / 2 + 150, 100], radius=10, outline=(122, 78, 44, 255), width=5)   # khay chip nhà cái
    return pil


def make_chips():
    w, h = 130, 96
    pil = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(pil)
    cols = [(200, 64, 47), (58, 123, 200), (227, 178, 60), (200, 64, 47)]
    for i, c in enumerate(cols):
        y = h - 26 - i * 13
        d.ellipse([10, y, w - 10, y + 24], fill=c + (255,), outline=(60, 40, 30, 255), width=2)
        d.ellipse([36, y + 6, w - 36, y + 16], outline=(250, 245, 230, 255), width=2)
    return pil


def setup_tmp():
    if os.path.isdir(TMP):
        shutil.rmtree(TMP)          # thư mục tạm của chính script này
    os.makedirs(TMP)
    shutil.copy(os.path.join(ATOM, "atomspine.json"), TMP)
    shutil.copytree(os.path.join(ATOM, "images"), os.path.join(TMP, "images"))
    make_table().save(os.path.join(TMP, "images", "xem_ban.png"))
    make_chips().save(os.path.join(TMP, "images", "xem_chip.png"))
    # canvas 1024 x 1536, gốc (512, 1460): toạ độ ảnh = (x + 512, 1460 − y)
    ops = [
        f"part.add xem_ban path=images/xem_ban.png at={512 - 750},{1460 - TABLE_Y} canvas=1024,1536 origin=512,1460 bone=root",
        "slot.order xem_ban to=before:tay_trai",
        "bone.add xem_chip_b parent=root x=0 y=0",
        f"part.add xem_chip path=images/xem_chip.png at={512 - 65},{1460 - CHIP[1] - 60} canvas=1024,1536 origin=512,1460 bone=xem_chip_b",
        "slot.order xem_chip to=before:tay_trai",
        # chồng chip chỉ để xem: bị vơ về khay trong take, được đẩy từ khay tới ô cược trong pay (trong game do code lái)
        "key take xem_chip_b.translate 0:0,0 0.9:0,0:ease 1.32:0,326",
        "key take xem_chip.alpha 0:1 1.3:1 1.36:0 2.5:0",
        "key pay xem_chip_b.translate 0:44,322 0.62:44,322:ease 0.88:36,186 0.96:36,186:ease 1.164:32,104 1.218:32,104:ease 1.3:29,50:easeOut 1.42:27,20 2.5:27,20",
    ]
    open(os.path.join(TMP, "xem.ops"), "w", encoding="utf-8").write("\n".join(ops) + "\n")
    atom("do", "-f", os.path.join(TMP, "xem.ops"))


def sheets(names, w, h, cols, fps=FPS):
    r = subprocess.run(TSX + [os.path.join(HERE, "khung.mts"), TMP, TMP, str(fps), ",".join(map(str, BOX)), str(w), str(h), str(cols),
                              ",".join(names)], capture_output=True, text=True, encoding="utf-8", errors="replace")
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
            # GIF: mỗi khung 30 ms + 40 ms xen kẽ (trình duyệt làm tròn về 10 ms; trung bình 33,3 ms = 30 khung/giây)
            durs = [30 if k % 3 else 40 for k in range(len(seq))]
            if not loops.get(c):
                durs[-1] = 700      # clip một lần: nghỉ một nhịp trước khi lặp lại
            pal = seq[0].quantize(colors=96, method=Image.MEDIANCUT, dither=Image.NONE)
            q = [f.quantize(palette=pal, dither=Image.NONE) for f in seq]
            q[0].save(os.path.join(OUT, f"{c}.gif"), save_all=True, append_images=q[1:], duration=durs, loop=0, optimize=False)
            pick = [frames[int(round(k * (n - 1) / 9))] for k in range(10)]
            cw, chh = 230, 374
            to = Image.new("RGB", (cw * 10, chh), (255, 255, 255))
            for k, f in enumerate(pick):
                to.paste(f.resize((cw, chh), Image.LANCZOS), (k * cw, 0))
            to.save(os.path.join(OUT, f"{c}_to.png"))
            print(c, n, "khung", dur, "s")
    if big:
        # khung lớn để soi: clip:giây,giây -> render từng khung 896 x 1120 (đi qua atom render của bản tạm thì bị co; dùng khung.mts 1 fps giả)
        os.makedirs(os.path.join(OUT, "lon"), exist_ok=True)
        for item in big:
            c, ts = item.split(":")
            info = sheets([c], 896, 1456, 10, fps=FPS)
            n, dur = info[c]
            im = Image.open(os.path.join(TMP, f"{c}_sheet.png")).convert("RGB")
            for t in ts.split(","):
                k = min(n - 1, int(round(float(t) * FPS)))
                f = im.crop(((k % 10) * 896, (k // 10) * 1456, (k % 10 + 1) * 896, (k // 10 + 1) * 1456))
                f.save(os.path.join(OUT, "lon", f"{c}_f{k:03d}.png"))
            print(c, "khung lớn", ts)


if __name__ == "__main__":
    main()
