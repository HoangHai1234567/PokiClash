# Bản 2k của đảo Casino (GD_Claude/29_DaoCasino.md, C8): py -3 -I xu_ly_2k.py
# 1. cong_trinh_2k.png: ảnh phóng Magnific (nền trắng, classic 2k) + kênh trong suốt lấy từ cong_trinh_1k.png phóng cùng cỡ; điểm gần trắng ở
#    mép trong suốt thì bỏ hẳn (khỏi viền trắng).
# 2. tach_cong_trinh.py 2k: cắt từng công trình (cat/<id>.png, cong_trinh.json theo px bản 2k).
# 3. Ba lều sự kiện (leu_1k.png, gen rời): mỗi cụm một lều, thu cho rộng bằng 1,25 lần bãi cọc (bai_*) và đặt chân lều vào giữa bãi.
#    Lều thay cọc bãi khi sự kiện mở. Ghép thử: ghep_thu_2k.png (không lều), ghep_thu_2k_leu.png (có lều).
# 4. Chép vào Assets/03 Art/Casino: casino_dao.png, casino_ct_<id>.png, casino_art.json.
import os, sys, json, shutil
from collections import deque
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ART = os.path.join(r"C:\Atomik\PokiWar", "Assets", "03 Art", "Casino")
# lều → bãi (bãi trên: Đêm Bài; bãi phải: Vòng Xoay; bãi trái dưới: Máy Quả)
LEU = {"blackjack": "bai_tren", "roulette": "bai_phai", "slot": "bai_trai"}


def make_layer():
    rgb = Image.open(os.path.join(HERE, "cong_trinh_2k_nen_trang.jpg")).convert("RGB")
    a1 = Image.open(os.path.join(HERE, "cong_trinh_1k.png")).getchannel("A").resize(rgb.size, Image.LANCZOS)
    px, ap = rgb.load(), a1.load()
    W, H = rgb.size
    for x in range(W):
        for y in range(H):
            if ap[x, y] < 250 and min(px[x, y]) > 232:
                ap[x, y] = 0
    out = rgb.convert("RGBA")
    out.putalpha(a1)
    out.save(os.path.join(HERE, "cong_trinh_2k.png"))
    Image.open(os.path.join(HERE, "dao_trong_2k.jpg")).convert("RGB").save(os.path.join(HERE, "dao_trong_2k.png"))


def components(alpha, thr=100, min_px=400):
    W, H = alpha.size
    ap = alpha.load()
    seen = [[False] * H for _ in range(W)]
    comps = []
    for x0 in range(W):
        for y0 in range(H):
            if seen[x0][y0] or ap[x0, y0] < thr:
                continue
            q = deque([(x0, y0)])
            seen[x0][y0] = True
            pts = []
            while q:
                x, y = q.popleft()
                pts.append((x, y))
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H and not seen[nx][ny] and ap[nx, ny] >= thr:
                        seen[nx][ny] = True
                        q.append((nx, ny))
            if len(pts) >= min_px:
                comps.append(pts)
    return comps


def tents(meta):
    im = Image.open(os.path.join(HERE, "leu_1k.png")).convert("RGBA")
    comps = components(im.getchannel("A"))
    comps.sort(key=lambda p: -len(p))
    comps = comps[:3]
    boxes = []
    for pts in comps:
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        boxes.append((min(xs), min(ys), max(xs) + 1, max(ys) + 1))
    # trên cùng: bài; phải nhất: vòng xoay; còn lại: máy quả
    top = min(boxes, key=lambda b: b[1])
    right = max((b for b in boxes if b != top), key=lambda b: b[0])
    left = next(b for b in boxes if b not in (top, right))
    pick = {"blackjack": top, "roulette": right, "slot": left}
    for booth, box in pick.items():
        pad = meta["items"][LEU[booth]]
        pw = pad["x1"] - pad["x0"]
        cut = im.crop(box)
        # bỏ phần trong suốt mờ quanh (cờ) ngoài cụm: cắt theo khung cụm là đủ
        tw = int(pw * 1.25)
        th = int(cut.height * tw / cut.width)
        cut = cut.resize((tw, th), Image.LANCZOS)
        cx = (pad["x0"] + pad["x1"]) / 2
        bottom = pad["y1"] - (pad["y1"] - pad["y0"]) * 0.12
        x0 = int(cx - tw / 2)
        y0 = int(bottom - th)
        name = "leu_" + booth
        cut.save(os.path.join(HERE, "cat", name + ".png"))
        meta["items"][name] = {"x0": x0, "y0": y0, "x1": x0 + tw, "y1": y0 + th}


def compose(meta, with_tents):
    base = Image.open(os.path.join(HERE, "dao_trong_2k.png")).convert("RGBA")
    items = []
    for bid, b in meta["items"].items():
        is_tent = bid.startswith("leu_")
        is_pad = bid in LEU.values()
        if is_tent and not with_tents:
            continue
        if is_pad and with_tents:
            continue
        items.append((b["y1"], bid, b))
    for _, bid, b in sorted(items):
        img = Image.open(os.path.join(HERE, "cat", bid + ".png")).convert("RGBA")
        base.alpha_composite(img, (b["x0"], b["y0"]))
    return base


def main():
    make_layer()
    import tach_cong_trinh
    sys.argv = ["", "2k"]
    tach_cong_trinh.H = "2k"
    tach_cong_trinh.main()
    meta = json.load(open(os.path.join(HERE, "cong_trinh.json"), encoding="utf-8"))
    tents(meta)
    json.dump(meta, open(os.path.join(HERE, "cong_trinh.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    compose(meta, False).convert("RGB").save(os.path.join(HERE, "ghep_thu_2k.png"))
    compose(meta, True).convert("RGB").save(os.path.join(HERE, "ghep_thu_2k_leu.png"))
    os.makedirs(ART, exist_ok=True)
    shutil.copy2(os.path.join(HERE, "dao_trong_2k.png"), os.path.join(ART, "casino_dao.png"))
    for bid in meta["items"]:
        shutil.copy2(os.path.join(HERE, "cat", bid + ".png"), os.path.join(ART, "casino_ct_" + bid + ".png"))
    json.dump(meta, open(os.path.join(ART, "casino_art.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("da chep", len(meta["items"]), "anh vao", ART)


if __name__ == "__main__":
    main()
