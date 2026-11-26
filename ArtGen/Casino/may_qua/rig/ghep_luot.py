# Ghép các ảnh động clip (../xem/<clip>.gif, do xem.py dựng) thành một lượt quay trọn để xem nhịp nối clip:
#   ../xem/luot_truot.gif, luot_trung.gif, luot_jackpot.gif. Chỗ nối là cắt thẳng (trong game runtime hoà 0,12 s).
# Chạy: py -3 -I ghep_luot.py
import os, sys
from PIL import Image, ImageSequence
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, "..", "xem"))
LOOP = {"idle", "spin", "tease"}
cache = {}

def fr(c):
    if c not in cache:
        f = [x.convert("RGB").resize((224, 376), Image.LANCZOS) for x in ImageSequence.Iterator(Image.open(os.path.join(OUT, c + ".gif")))]
        cache[c] = f if c in LOOP else f[:-12]      # clip một lần: bỏ 12 khung giữ cuối
    return cache[c]

def seq(*items):
    out = []
    for it in items:
        c, n = (it, 1) if isinstance(it, str) else it
        f = fr(c)
        out += (f * n) if isinstance(n, int) else f[:int(len(f) * n)]
    return out

FLOWS = {
    "luot_truot": [("idle", 0.25), "pull", ("spin", 2), "stop_1", "spin", "stop_2", "spin", "stop_3", "lose", ("idle", 0.25)],
    "luot_trung": [("idle", 0.25), "pull", ("spin", 2), "stop_1", "spin", "stop_2", "spin", "stop_3", "win", ("idle", 0.25)],
    "luot_jackpot": [("idle", 0.25), "pull", ("spin", 2), "stop_1", "spin", "stop_2", ("tease", 3), "stop_3", "jackpot", ("idle", 0.25)],
}
for name, items in FLOWS.items():
    f = seq(*items)
    pal = f[len(f) // 2].quantize(128, method=Image.Quantize.MEDIANCUT)
    q = [x.quantize(palette=pal, dither=Image.Dither.NONE) for x in f]
    q[0].save(os.path.join(OUT, name + ".gif"), save_all=True, append_images=q[1:], duration=33, loop=0, disposal=1)
    print(name, len(f), "khung", round(len(f) / 30, 1), "giây")
