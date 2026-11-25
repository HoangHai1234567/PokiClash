# Ảnh động duyệt clip D2 của Lão Mực (GD_Claude/31). Chép project AtomSpine sang thư mục tạm, thêm một mặt bàn nỉ + hai chồng chip
# (chỉ để xem, không vào rig thật) với lớp vẽ: thân, mặt, lưỡi trai < BÀN < tay, bàn tay — đúng như trong game (tay vươn ra trước
# bàn). Mỗi clip một `atom sheet` một hàng (15 khung/giây), cắt thành khung, ghép GIF; thêm tờ 8 khung.
# Ra: ../dealer/d2/<clip>.gif, <clip>_to.png
# Chạy: py -3 -I xem_d2.py [clip ...]
import os, shutil, subprocess, sys, json
import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ATOM = os.path.abspath(os.path.join(HERE, "..", "atom"))
OUT = os.path.abspath(os.path.join(HERE, "..", "d2"))
TMP = os.path.join(os.environ.get("TEMP", "C:/Temp"), "lao_muc_xem")
CLI = ["node", "D:/AtomSpine/packages/cli/dist/atom.mjs"]
CLIPS = ["idle", "greet", "talk", "bet_watch", "take", "pay", "react_win_small", "react_win_big", "react_lose", "react_push",
         "grumpy", "sulk"]
TABLE_Y = 420  # thế giới


def atom(*args):
    r = subprocess.run(CLI + list(args) + ["-p", TMP], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print((r.stdout + r.stderr)[-800:])
        raise SystemExit("atom lỗi")
    return r.stdout


def make_table():
    """Mặt bàn nỉ xanh tô phẳng, vân chì nhẹ, viền gỗ ở mép xa (rộng 1500, cao 640 px thế giới)."""
    w, h = 1500, 640
    rng = np.random.default_rng(3)
    img = np.zeros((h, w, 4), np.uint8)
    felt = np.array([47, 107, 74], float)
    a = np.tile(felt, (h, w, 1))
    # vân chì chéo
    yy, xx = np.mgrid[0:h, 0:w]
    stroke = (np.sin((xx + yy * 1.7) * 0.9 + rng.normal(0, 1.2, (h, w))) > 0.86).astype(float)
    a = a * (1 - 0.10 * stroke[..., None]) + np.array([70, 140, 98]) * 0.10 * stroke[..., None]
    img[..., :3] = a.clip(0, 255)
    img[..., 3] = 255
    pil = Image.fromarray(img)
    d = ImageDraw.Draw(pil)
    d.rectangle([0, 0, w, 26], fill=(122, 78, 44, 255))      # viền gỗ mép xa
    d.rectangle([0, 26, w, 34], fill=(88, 54, 30, 255))
    d.ellipse([w / 2 - 70, 330, w / 2 + 70, 390], outline=(232, 222, 190, 255), width=4)  # ô cược của người chơi
    return pil


def make_chips():
    w, h = 120, 90
    pil = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(pil)
    cols = [(200, 64, 47), (58, 123, 200), (227, 178, 60), (200, 64, 47)]
    for i, c in enumerate(cols):
        y = h - 24 - i * 12
        d.ellipse([10, y, w - 10, y + 22], fill=c + (255,), outline=(60, 40, 30, 255), width=2)
        d.ellipse([34, y + 5, w - 34, y + 15], outline=(250, 245, 230, 255), width=2)
    return pil


def setup_tmp():
    if os.path.isdir(TMP):
        shutil.rmtree(TMP)
    os.makedirs(TMP)
    shutil.copy(os.path.join(ATOM, "atomspine.json"), TMP)
    shutil.copytree(os.path.join(ATOM, "images"), os.path.join(TMP, "images"))
    make_table().save(os.path.join(TMP, "images", "xem_ban.png"))
    make_chips().save(os.path.join(TMP, "images", "xem_chip.png"))
    # canvas 1024 x 1536, gốc (512, 1460): toạ độ ảnh = (x + 512, 1460 − y)
    ops = [
        f"part.add xem_ban path=images/xem_ban.png at={512 - 750},{1460 - TABLE_Y} canvas=1024,1536 origin=512,1460 bone=root",
        "slot.order xem_ban to=before:tay_trai",
        f"part.add xem_chip_t path=images/xem_chip.png at={512 - 150 - 60},{1460 - 250 - 45} canvas=1024,1536 origin=512,1460 bone=root",
        f"part.add xem_chip_p path=images/xem_chip.png at={512 + 150 - 60},{1460 - 250 - 45} canvas=1024,1536 origin=512,1460 bone=root",
        "slot.order xem_chip_t to=before:tay_trai",
        "slot.order xem_chip_p to=before:tay_trai",
    ]
    open(os.path.join(TMP, "xem.ops"), "w", encoding="utf-8").write("\n".join(ops) + "\n")
    atom("do", "-f", os.path.join(TMP, "xem.ops"))


def durs():
    j = json.load(open(os.path.join(TMP, "atomspine.json"), encoding="utf-8"))
    out = {}
    for a in j.get("anims", j.get("animations", [])):
        if isinstance(a, dict):
            out[a.get("name")] = a.get("dur") or a.get("duration")
    return out


def main():
    names = sys.argv[1:] or CLIPS
    os.makedirs(OUT, exist_ok=True)
    setup_tmp()
    D = durs()
    cell = 300
    for c in names:
        dur = D.get(c) or 1.5
        n = max(8, int(round(dur * 15)))
        sheet = os.path.join(TMP, f"{c}_sheet.png")
        atom("sheet", "--anim", c, "--frames", str(n), "--cols", str(n), "--cell", str(cell), "--bg", "EFE5D2FF", "-o", sheet)
        im = Image.open(sheet).convert("RGB")
        frames = [im.crop((i * cell, 0, (i + 1) * cell, cell)) for i in range(n)]
        frames[0].save(os.path.join(OUT, f"{c}.gif"), save_all=True, append_images=frames[1:], duration=int(1000 / 15), loop=0)
        pick = [frames[int(round(k * (n - 1) / 7))] for k in range(8)]
        to = Image.new("RGB", (cell * 8, cell), (255, 255, 255))
        for k, f in enumerate(pick):
            to.paste(f, (k * cell, 0))
        to.save(os.path.join(OUT, f"{c}_to.png"))
        print(c, n, "khung")


if __name__ == "__main__":
    main()
