# Ghép các mảnh đã tách lại theo geo.json, đặt cạnh L1 để soi (soi/ghep_thu.png). Chạy: py -3 -I ghep_thu.py [mắt] [miệng]
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
ATOM = os.path.join(HERE, "..", "atom")
geo = json.load(open(os.path.join(ATOM, "geo.json"), encoding="utf-8"))
P = geo["parts"]
def im(n): return Image.open(os.path.join(ATOM, "images", n + ".png")).convert("RGBA")
def place(cv, n, left=None, top=None):
    i = im(n); cv.alpha_composite(i, (int(P[n]["left"] if left is None else left), int(P[n]["top"] if top is None else top)))
def ghep(mat, mieng, bg=(150, 150, 150, 255), den=None):
    cv = Image.new("RGBA", (1024, 1536), bg)
    for n in ("can", "lo_xo", "sao", "chan_t", "chan_p", "giay_t", "giay_p", "than"): place(cv, n)
    if den: place(cv, den + "_d"); place(cv, den + "_h")
    m = im(f"mieng_{mieng:02d}")
    place(cv, f"mieng_{mieng:02d}", geo["mieng"]["cx"] - m.width / 2, geo["mieng"]["top"])
    e = im(f"mat_{mat:02d}")
    place(cv, f"mat_{mat:02d}", geo["mat"]["cx"] - e.width / 2, geo["mat"]["cy"] - e.height / 2)
    place(cv, "may_t"); place(cv, "may_p")
    return cv
if __name__ == "__main__":
    a = ghep(1, 1)
    l1 = Image.open(os.path.join(HERE, "L1_goc.png")).convert("RGBA")
    sheet = Image.new("RGBA", (1024 * 4, 1536), (150, 150, 150, 255))
    sheet.paste(l1, (0, 0)); sheet.paste(a, (1024, 0)); sheet.paste(ghep(3, 3, den="den_a"), (2048, 0)); sheet.paste(ghep(7, 5, den="den_b"), (3072, 0))
    sheet.convert("RGB").resize((2048, 768)).save(os.path.join(HERE, "soi", "ghep_thu.png"))
    a.crop((200, 300, 824, 1250)).save(os.path.join(HERE, "soi", "ghep_can.png"))
