# Tách lớp công trình đảo Casino (gen "đúng chỗ đúng cỡ" trên nền trắng) thành từng ảnh rời, và ghép thử lên đảo trống.
# py -3 -I tach_cong_trinh.py [hậu tố, mặc định 1k]
#   vào:  dao_trong_<h>.png, cong_trinh_<h>.png (cùng cỡ)
#   ra:   cat/<id>.png (cắt sát, trong suốt), cong_trinh.json (khung theo ảnh đảo: x0, y0, x1, y1 px gốc trên trái; đáy để xếp lớp),
#         ghep_thu_<h>.png (đảo + công trình) để soi
# Nền: điểm gần trắng (cả ba kênh > NGUONG) nối với mép ảnh (loang từ mép), nên chỗ trắng bên trong (buồm, tường kem) có viền mực bao
# quanh thì giữ. Mỗi cụm điểm còn lại gán cho công trình có khung (KHUNG, toạ độ bản 1k) chứa tâm cụm.
import sys, os, json
from collections import deque
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
H = sys.argv[1] if len(sys.argv) > 1 else "1k"
NGUONG = 238
# khung công trình trên bản 1k (1536 x 1024): id → (x0, y0, x1, y1)
KHUNG = {
    "thap": (630, 60, 925, 600),
    "hang": (325, 135, 500, 335),
    "cho": (60, 285, 365, 675),
    "dua": (990, 85, 1400, 376),
    "quan_tro": (1080, 500, 1445, 790),
    "ben_cau": (360, 610, 590, 810),
    "ben_tau": (370, 765, 1040, 995),
    "bai_tren": (540, 115, 705, 222),
    "bai_phai": (1250, 377, 1415, 495),
    "bai_trai": (210, 655, 362, 785),
}


def main():
    base = Image.open(os.path.join(HERE, f"dao_trong_{H}.png")).convert("RGBA")
    lay = Image.open(os.path.join(HERE, f"cong_trinh_{H}.png")).convert("RGBA")
    if lay.size != base.size:
        lay = lay.resize(base.size, Image.LANCZOS)
    W, Hh = lay.size
    k = W / 1536.0
    alpha = lay.getchannel("A")
    ap = alpha.load()
    if alpha.getextrema()[0] < 20:
        # ảnh đã có nền trong suốt (GPT trả RGBA): nền là alpha thấp
        bg = [[ap[x, y] < 100 for y in range(Hh)] for x in range(W)]
        mask = alpha
    else:
        px = lay.load()
        white = [[min(px[x, y][:3]) > NGUONG for y in range(Hh)] for x in range(W)]
        bg = [[False] * Hh for _ in range(W)]
        q = deque()
        for x in range(W):
            for y in (0, Hh - 1):
                if white[x][y] and not bg[x][y]:
                    bg[x][y] = True
                    q.append((x, y))
        for y in range(Hh):
            for x in (0, W - 1):
                if white[x][y] and not bg[x][y]:
                    bg[x][y] = True
                    q.append((x, y))
        while q:
            x, y = q.popleft()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < W and 0 <= ny < Hh and white[nx][ny] and not bg[nx][ny]:
                    bg[nx][ny] = True
                    q.append((nx, ny))
        mask = Image.new("L", (W, Hh), 0)
        mp = mask.load()
        for x in range(W):
            for y in range(Hh):
                if not bg[x][y]:
                    mp[x, y] = 255
        mask = mask.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(0.7))
    # cụm điểm (trên mặt nạ nhị phân) → công trình
    lab = [[-1] * Hh for _ in range(W)]
    comps = []
    for x0 in range(W):
        for y0 in range(Hh):
            if bg[x0][y0] or lab[x0][y0] >= 0:
                continue
            cid = len(comps)
            pts = []
            q = deque([(x0, y0)])
            lab[x0][y0] = cid
            while q:
                x, y = q.popleft()
                pts.append((x, y))
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < Hh and not bg[nx][ny] and lab[nx][ny] < 0:
                        lab[nx][ny] = cid
                        q.append((nx, ny))
            comps.append(pts)
    owner = {}
    for cid, pts in enumerate(comps):
        if len(pts) < 12:
            continue
        cx = sum(p[0] for p in pts) / len(pts) / k
        cy = sum(p[1] for p in pts) / len(pts) / k
        best = None
        for bid, (a, b, c, d) in KHUNG.items():
            if a <= cx <= c and b <= cy <= d:
                best = bid
                break
        if best is None:
            # gần khung nào nhất
            best = min(KHUNG, key=lambda i: max(0, KHUNG[i][0] - cx, cx - KHUNG[i][2]) + max(0, KHUNG[i][1] - cy, cy - KHUNG[i][3]))
        owner[cid] = best
    os.makedirs(os.path.join(HERE, "cat"), exist_ok=True)
    meta = {"w": W, "h": Hh, "items": {}}
    ghep = base.copy()
    order = []
    for bid in KHUNG:
        m = Image.new("L", (W, Hh), 0)
        mm = m.load()
        any_px = False
        for cid, o in owner.items():
            if o != bid:
                continue
            for (x, y) in comps[cid]:
                mm[x, y] = 255
                any_px = True
        if not any_px:
            print("THIEU", bid)
            continue
        m = m.filter(ImageFilter.MaxFilter(5))  # gồm cả mép mềm quanh cụm
        a = Image.composite(mask, Image.new("L", (W, Hh), 0), m)
        img = lay.copy()
        img.putalpha(a)
        box = a.getbbox()
        cut = img.crop(box)
        cut.save(os.path.join(HERE, "cat", bid + ".png"))
        meta["items"][bid] = {"x0": box[0], "y0": box[1], "x1": box[2], "y1": box[3]}
        order.append((box[3], bid, cut, box))
    for _, bid, cut, box in sorted(order):
        ghep.alpha_composite(cut, (box[0], box[1]))
    ghep.save(os.path.join(HERE, f"ghep_thu_{H}.png"))
    with open(os.path.join(HERE, "cong_trinh.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    print("xong", len(meta["items"]), "cong trinh", W, Hh)


if __name__ == "__main__":
    main()
