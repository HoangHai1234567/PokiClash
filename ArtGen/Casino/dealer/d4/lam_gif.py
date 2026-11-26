# Ghép chuỗi khung lượt chụp Vòng Xoay có Lão Mực (Editor/CasinoRouletteTour.cs, Temp/PokiShots/casino_rl_dealer/f_*.jpg, 20 khung/giây)
# thành ảnh động d4/vong_xoay.webp (WebP động, rộng 384; GIF cùng độ dài nặng ~60 MB nên chỉ xuất khi thêm --gif, không vào git) và tờ
# khung d4/vong_xoay_to.jpg (mỗi giây một khung) để soi nhanh.
# Chạy: py -3 -I lam_gif.py [rộng] [--gif]
import glob, os, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
SHOTS = os.path.join(PROJ, "Temp", "PokiShots", "casino_rl_dealer")
args = [a for a in sys.argv[1:] if not a.startswith("--")]
W = int(args[0]) if args else 384
FPS = 20

files = sorted(glob.glob(os.path.join(SHOTS, "f_*.jpg")))
if not files:
    raise SystemExit("Chưa có khung: chạy lượt chụp (cờ Temp/casino_rl_dealer_tour.flag) trước.")
first = Image.open(files[0])
H = round(first.height * W / first.width)
frames = [Image.open(f).convert("RGB").resize((W, H), Image.LANCZOS) for f in files]
frames[0].save(os.path.join(HERE, "vong_xoay.webp"), save_all=True, append_images=frames[1:], duration=1000 // FPS, loop=0, quality=60,
               method=4)
if "--gif" in sys.argv:
    pal = frames[len(frames) // 3].quantize(colors=128, method=Image.MEDIANCUT, dither=Image.NONE)
    q = [f.quantize(palette=pal, dither=Image.NONE) for f in frames]
    q[0].save(os.path.join(HERE, "vong_xoay.gif"), save_all=True, append_images=q[1:], duration=1000 // FPS, loop=0, optimize=False)
# tờ khung: mỗi giây một khung, 8 cột
pick = frames[::FPS]
cols = 8
cw, ch = W // 2, H // 2
rows = (len(pick) + cols - 1) // cols
sheet = Image.new("RGB", (cols * cw, rows * ch), (30, 30, 30))
for k, f in enumerate(pick):
    sheet.paste(f.resize((cw, ch), Image.LANCZOS), ((k % cols) * cw, (k // cols) * ch))
sheet.save(os.path.join(HERE, "vong_xoay_to.jpg"), quality=85)
print(len(frames), "khung,", round(len(frames) / FPS, 1), "s ->", os.path.join(HERE, "vong_xoay.webp"))
