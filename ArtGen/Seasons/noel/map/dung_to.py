# Tờ ảnh mẫu gửi GPT vẽ lại có tuyết, cho màn Nhà và đảo Casino (người dùng 2026-11-27: "làm tuyết phủ lên đảo / cây cối / các
# building"). Mỗi tờ đúng cỡ ảnh GPT 2.6 1k 3:2 (1536 x 1024), nền xanh phẳng (tuyết trắng tách được khỏi nền); ảnh rời xếp kệ, giữ
# tỉ lệ thật giữa các ảnh trong cùng tờ, cách nhau đủ rộng cho mũ tuyết nhô lên trên mép.
# py -3 -I dung_to.py  -> to/<tờ>.png + to/<tờ>.json (mỗi ảnh: tên, nguồn, khung cắt ở ảnh nguồn, khung trên tờ, hệ số thu)
import json, os, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
ART = os.path.join(PROJ, "Assets", "03 Art")
OUT = os.path.join(HERE, "to")
os.makedirs(OUT, exist_ok=True)
sys.stdout.reconfigure(encoding="utf-8")

W, H = 1536, 1024
BG = (62, 118, 168, 255)
GAP, MARGIN = 34, 26  # px trên tờ: khe giữa ảnh (mũ tuyết nhô lên), lề tờ


def src(rel, name=None, crop=None):
    p = os.path.join(ART, rel)
    im = Image.open(p).convert("RGBA")
    if crop:
        x, y, w, h = crop
        im = im.crop((x, y, x + w, y + h))
    else:
        crop = (0, 0, im.width, im.height)
    return {"name": name or os.path.splitext(os.path.basename(rel))[0], "src": rel.replace("\\", "/"), "crop": list(crop), "im": im}


def pack(items, s):
    """Xếp kệ theo chiều cao giảm dần ở hệ số s; trả danh sách (item, x, y, w, h) hoặc None nếu không vừa."""
    order = sorted(items, key=lambda it: -it["im"].height)
    x, y, row_h, out = MARGIN, MARGIN, 0, []
    for it in order:
        w, h = round(it["im"].width * s), round(it["im"].height * s)
        if x + w > W - MARGIN:
            x, y, row_h = MARGIN, y + row_h + GAP, 0
        if x + w > W - MARGIN or y + h > H - MARGIN:
            return None
        out.append((it, x, y, w, h))
        x += w + GAP
        row_h = max(row_h, h)
    # dồn từng kệ ra giữa bề ngang cho đều lề
    return out


def best(items):
    lo, hi = 0.1, 1.0
    if pack(items, hi):
        return hi, pack(items, hi)
    for _ in range(30):
        mid = (lo + hi) / 2
        if pack(items, mid):
            lo = mid
        else:
            hi = mid
    return lo, pack(items, lo)


def save(name, items, single=False):
    sheet = Image.new("RGBA", (W, H), BG)
    meta = {"sheet": name, "W": W, "H": H, "items": []}
    if single:
        it = items[0]
        s = min(W / it["im"].width, H / it["im"].height)
        w, h = round(it["im"].width * s), round(it["im"].height * s)
        placed = [(it, (W - w) // 2, (H - h) // 2, w, h)]
    else:
        s, placed = best(items)
    for it, x, y, w, h in placed:
        sheet.alpha_composite(it["im"].resize((w, h), Image.LANCZOS), (x, y))
        meta["items"].append({"name": it["name"], "src": it["src"], "crop": it["crop"], "dst": [x, y, w, h], "scale": w / it["im"].width})
    sheet.convert("RGB").save(os.path.join(OUT, name + ".png"), optimize=True)
    json.dump(meta, open(os.path.join(OUT, name + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{name}: {len(placed)} ảnh, thu {s:.3f}")


def main():
    save("casino_dao", [src("Casino/casino_dao.png")], single=True)
    save("home_base", [src("Home/home_base.png")], single=True)
    ct = ["thap", "cho", "dua", "quan_tro", "ben_tau", "ben_cau", "hang", "bai_phai", "bai_trai", "bai_tren",
          "leu_blackjack", "leu_roulette", "leu_slot"]
    save("casino_ct", [src(f"Casino/casino_ct_{k}.png") for k in ct])
    b1 = ["main", "mine", "waterwheel", "kitchen", "forge"]
    b2 = ["storage", "sawmill", "orchard", "field", "pond", "hotspring", "well", "tree", "bench", "swing"]
    save("home_b1", [src(f"Home/home_b_{k}.png") for k in b1])
    save("home_b2", [src(f"Home/home_b_{k}.png") for k in b2])
    tj = json.load(open(os.path.join(ART, "Baked", "Home", "home_trees.json"), encoding="utf-8"))
    save("home_cay", [src("Baked/Home/home_trees.png", t["name"], (t["x"], t["y"], t["w"], t["h"])) for t in tj["items"]])
    save("home_kit", [src(f"Home/home_k_vach_{i}.png") for i in range(1, 5)] + [src(f"Home/home_k_bien_{i}.png") for i in range(1, 7)])


if __name__ == "__main__":
    main()
