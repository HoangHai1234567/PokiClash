# -*- coding: utf-8 -*-
"""Cỡ tướng trên sân (2026-11-19, người dùng: "các con đầu tiên có vài con to quá, các final boss lại bé tí; càng về sau càng to,
pháp sư có thể nhỏ đi một chút").

Cỡ trên sân = Height (150 phía địch, 176 phía mình) x size của dạng x 1,18 nếu boss; rig tự co theo chiều cao dáng đứng, nên con thấp
bè trông to, con cao gầy hay có lửa / khói quanh người trông khác hẳn dù cùng size. Vì vậy size tính từ HÌNH THẬT:

  1. Unity, đang Play: menu "PokiClash/Thử/Cỡ tướng: đo và chụp hàng tướng từng đảo (đang Play)" (Editor/HeroSizeTour.cs) chụp
     Temp/PokiShots/co_tuong/<đảo>.png + co_tuong.csv (10 tướng theo ải ra mắt, mỗi dạng một hàng; sau đó là lính của đảo).
  2. py -3 -I ArtGen/CoTuong/co_tuong.py do     -> ra/co_do.json: mỗi hình đếm điểm ảnh: cao, rộng, V = căn diện tích (điểm sân)
  3. py -3 -I ArtGen/CoTuong/co_tuong.py tinh   -> ra/co_moi.json + ra/so_sanh_1.jpg, so_sanh_2.jpg (TRƯỚC / SAU từng đảo)
  4. py -3 -I ArtGen/CoTuong/co_tuong.py ghi    -> ghi size vào Assets/02 Data/Json/heroes.json (chỉ sửa dòng "size"), cộng
     chinh_tay.json (số chỉnh bằng mắt, đè lên số tính). Rồi Unity: menu PokiClash/Nhập dữ liệu.

Độ to M = V^0.6 x cao^0.4 (chỉ diện tích thì con cao gầy bị phóng quá tay, chỉ chiều cao thì con bè quá to). Dạng cuối ở ải ra mắt
theo bậc DICH (ải 1, 5, 10, 15, 20, 30, 40, 50, 60, 70; đã gồm hệ số boss của ải); dạng nhỏ hơn theo TI_LE; pháp sư nhân PHAP_SU.
Trần chiều cao phía địch HCAP (chân địch ở y 236 trên sân 464, phía trên còn khoảng trời tới dải HUD). Lính: bậc 1 (gặp ải 2–34) và
bậc 2 (ải 37–68) theo DICH_LINH, nhỏ hơn tướng đi cùng.
"""
import csv
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
SHOTS = os.path.join(ROOT, "Temp", "PokiShots", "co_tuong")
RA = os.path.join(HERE, "ra")
HEROES = os.path.join(ROOT, "Assets", "02 Data", "Json", "heroes.json")

SLOT = {1: 0, 5: 1, 10: 2, 15: 3, 20: 4, 30: 5, 40: 6, 50: 7, 60: 8, 70: 9}
DICH = [132, 138, 144, 150, 162, 170, 178, 186, 196, 222]
TI_LE = {1: [1.0], 2: [0.78, 1.0], 3: [0.72, 0.86, 1.0]}
PHAP_SU = {"hong_lien": 0.92, "giong_bao": 0.92}  # Viêm Sư (pháp sư gọi cầu lửa), Giông Bão (kỳ giông áo pháp sư)
DICH_LINH = {1: 100, 2: 128}
HCAP = 255
PPU, GAP, ROWH, ROWGAP = 180.0, 0.25, 1.75, 0.35  # như HeroSizeTour.cs
ZONES = ["Thuy", "Hoa", "Kim", "Moc", "Tho"]
ZN = {"Thuy": "Đảo Thủy", "Hoa": "Đảo Hỏa", "Kim": "Đảo Kim", "Moc": "Đảo Mộc", "Tho": "Đảo Thổ"}


def doc_csv():
    return list(csv.DictReader(open(os.path.join(SHOTS, "co_tuong.csv"), encoding="utf-8-sig")))


def o_hinh(rows, z, mask, W, H):
    """(dòng csv, x0, y0, x1, y1 vùng ô, chân y) cho từng hình của đảo z"""
    zr = [r for r in rows if r["zone"] == z]
    cols = sorted(set(float(r["cx"]) for r in zr))
    for r in zr:
        cx = float(r["cx"])
        i = cols.index(cx)
        x0 = 0 if i == 0 else (cols[i - 1] + cx) / 2
        x1 = 1 if i == len(cols) - 1 else (cols[i + 1] + cx) / 2
        foot = GAP + int(r["row"]) * (ROWH + ROWGAP) + ROWH * 0.92
        yield r, i, int(x0 * W), int(max(0, foot - 2.0) * PPU), int(x1 * W), int(min(H, (foot + 0.15) * PPU)), int(foot * PPU)


def lenh_do():
    import numpy as np
    from PIL import Image
    rows = doc_csv()
    res = []
    for z in ZONES:
        im = np.asarray(Image.open(os.path.join(SHOTS, z.lower() + ".png")).convert("RGB")).astype(int)
        H, W, _ = im.shape
        mask = np.abs(im - im[2, 2]).sum(axis=2) > 24
        for r, i, x0, y0, x1, y1, fy in o_hinh(rows, z, mask, W, H):
            ys, xs = np.nonzero(mask[y0:y1, x0:x1])
            if len(ys) == 0:
                continue
            k = 150.0 / PPU
            res.append(dict(zone=z, stage=int(r["stage"]), kind=r["kind"], hero=r["hero"], name=r["name"], form=int(r["form"]),
                            formName=r["formName"], size=float(r["size"]), mul=float(r["mul"]),
                            h=round((fy - (ys.min() + y0)) * k), w=round((xs.max() - xs.min()) * k), v=round((len(ys) * k * k) ** 0.5)))
    os.makedirs(RA, exist_ok=True)
    json.dump(res, open(os.path.join(RA, "co_do.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    for x in res:
        print(f"{x['zone']:5} ải{x['stage']:2} {x['formName'][:18]:18} size {x['size']:.2f}x{x['mul']:.2f}  cao {x['h']:3} rộng {x['w']:3} V {x['v']:3}")


def lenh_tinh():
    m = json.load(open(os.path.join(RA, "co_do.json"), encoding="utf-8"))
    tay = json.load(open(os.path.join(HERE, "chinh_tay.json"), encoding="utf-8"))
    by = {}
    for x in m:
        by.setdefault((x["zone"], x["hero"]), []).append(x)
    new = {}
    for (z, h), fs in by.items():
        fs.sort(key=lambda x: x["form"])
        n = len(fs)
        for x in fs:
            M = x["v"] ** 0.6 * x["h"] ** 0.4
            if x["kind"] == "minion":
                t = DICH_LINH[2 if h.endswith("2") else 1]
            else:
                t = DICH[SLOT[fs[0]["stage"]]] * TI_LE[n][x["form"]] * PHAP_SU.get(h, 1)
            k = t / M
            if x["h"] * k > HCAP:
                k = HCAP / x["h"]
            ns = round(x["size"] * k, 2)
            if abs(ns - x["size"]) <= (0.04 if x["kind"] != "minion" else 0.02):  # đã đúng cỡ (sai số đo): giữ số cũ, khỏi xê dịch lặt vặt mỗi lần đo lại
                ns = x["size"]
            if h in tay:
                ns = tay[h][x["form"]]
            x.update(M=M, ns=ns, k=ns / x["size"])
            new.setdefault(h, [None] * n)[x["form"]] = ns
    json.dump(new, open(os.path.join(RA, "co_moi.json"), "w", encoding="utf-8"), indent=0)
    for x in m:
        print(f"{x['zone']:5} ải{x['stage']:2} {x['formName'][:18]:18} size {x['size']:.2f} -> {x['ns']:.2f}   M {x['M']:4.0f} -> "
              f"{x['M'] * x['k']:4.0f}   cao {x['h']:3} -> {x['h'] * x['k']:4.0f}")
    so_sanh(m)


def so_sanh(m):
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
    rows = doc_csv()
    F = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 20)
    FS = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 17)
    FT = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 30)
    SC = 0.55
    key = {(x["zone"], x["hero"], x["form"]): x for x in m}

    def sheet(z, after):
        im = Image.open(os.path.join(SHOTS, z.lower() + ".png")).convert("RGB")
        a = np.asarray(im).astype(int)
        H, W, _ = a.shape
        mask = np.abs(a - a[2, 2]).sum(axis=2) > 24
        items = []
        for r, i, x0, y0, x1, y1, fy in o_hinh(rows, z, mask, W, H):
            x = key.get((z, r["hero"], int(r["form"])))
            ys, xs = np.nonzero(mask[y0:y1, x0:x1])
            if x is None or len(ys) == 0:
                continue
            bx0, bx1, by0 = xs.min() + x0, xs.max() + x0 + 1, ys.min() + y0
            items.append((x, im.crop((bx0, by0, bx1, fy + 4)), Image.fromarray((mask[by0:fy + 4, bx0:bx1] * 255).astype(np.uint8)), i))
        ncol = max(i for *_, i in items) + 1
        nrow = max(x["form"] for x, *_ in items) + 1
        cw = [0] * ncol
        for x, c, mk, i in items:
            cw[i] = max(cw[i], int(c.width * (x["k"] if after else 1) * SC) + 16)
        rowh = int(275 * SC * PPU / 150) + 70
        can = Image.new("RGB", (sum(cw) + 20, nrow * rowh + 46), (238, 232, 219))
        dr = ImageDraw.Draw(can)
        dr.text((10, 6), ZN[z] + (" — SAU" if after else " — TRƯỚC"), font=FT, fill=(150, 40, 30) if after else (60, 40, 30))
        xs0 = [10]
        for w in cw[:-1]:
            xs0.append(xs0[-1] + w)
        for x, c, mk, i in items:
            k = (x["k"] if after else 1) * SC
            cc = c.resize((max(1, int(c.width * k)), max(1, int(c.height * k))), Image.LANCZOS)
            footy = 46 + x["form"] * rowh + rowh - 8
            can.paste(cc, (xs0[i] + (cw[i] - cc.width) // 2, footy - cc.height), mk.resize(cc.size, Image.LANCZOS))
            dr.line((xs0[i] + 4, footy, xs0[i] + cw[i] - 4, footy), fill=(200, 190, 170), width=1)
            sz = x["ns"] if after else x["size"]
            ty = footy - rowh + 4
            tag = "lính" if x["kind"] == "minion" else f"ải {x['stage']}"
            for t, f, col in ((x["formName"][:16], F, (40, 30, 20)), (f"{tag} · size {sz:.2f}", FS, (90, 60, 40)),
                              (f"cao {x['h'] * (x['k'] if after else 1):.0f}", FS, (150, 40, 30))):
                w = dr.textlength(t, font=f)
                dr.text((xs0[i] + (cw[i] - w) / 2, ty), t, font=f, fill=col)
                ty += 20
        return can

    blocks = []
    for z in ZONES:
        blocks += [sheet(z, False), sheet(z, True)]
    mw = max(b.width for b in blocks)
    for name, sel in (("so_sanh_1.jpg", blocks[:6]), ("so_sanh_2.jpg", blocks[6:])):
        big = Image.new("RGB", (mw, sum(b.height for b in sel)), (238, 232, 219))
        y = 0
        for b in sel:
            big.paste(b, (0, y))
            y += b.height
        big.save(os.path.join(RA, name), quality=86)
        print(os.path.join(RA, name), big.size)


def lenh_ghi():
    new = json.load(open(os.path.join(RA, "co_moi.json"), encoding="utf-8"))
    for h, v in json.load(open(os.path.join(HERE, "chinh_tay.json"), encoding="utf-8")).items():
        new[h] = v
    raw = open(HEROES, "rb").read().decode("utf-8")
    nl = "\r\n" if "\r\n" in raw else "\n"
    lines = raw.split(nl)
    cur, k = None, 0
    for i, ln in enumerate(lines):
        mm = re.match(r'^   "id": "([^"]+)",$', ln)
        if mm:
            cur, k = mm.group(1), 0
            continue
        if cur in new:
            mm = re.match(r'^(\s*"size": )([0-9.]+)(,?)$', ln)
            if mm:
                vals = new[cur]
                if k <= len(vals):
                    lines[i] = f"{mm.group(1)}{(vals[0] if k == 0 else vals[k - 1]):g}{mm.group(3)}"
                k += 1
    open(HEROES, "wb").write(nl.join(lines).encode("utf-8"))
    d = json.load(open(HEROES, encoding="utf-8"))
    allh = {h["id"]: h for h in d["heroes"] + d["minions"]}
    for h, v in new.items():
        got = [f["size"] for f in allh[h]["forms"]]
        assert got == v and allh[h]["size"] == v[0], (h, got, v)
    print("đã ghi", len(new), "tướng / lính vào", HEROES)


if __name__ == "__main__":
    {"do": lenh_do, "tinh": lenh_tinh, "ghi": lenh_ghi}[sys.argv[1]]()
