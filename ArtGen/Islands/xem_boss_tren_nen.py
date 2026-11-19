# Tờ xem môi trường hợp boss (người dùng 2026-11-19: "các môi trường bạn làm phải phù hợp với kiểu boss"): đặt chân dung boss
# (dạng đầu) lên đúng bệ của nó trên ảnh nền đảo vùng đất, ghi số ải. Ra land_<đảo>/m1/xem_boss.png.
# Chạy: py -3 -I xem_boss_tren_nen.py [đảo ...]
import importlib.util
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
RES = os.path.join(ROOT, "Assets", "03 Art", "Heroes", "Resources")
DATA = os.path.join(ROOT, "Assets", "02 Data", "Json")
SC = 2


def bosses(zone):
    st = json.load(open(os.path.join(DATA, "stages.json"), encoding="utf-8"))["stages"]
    H = {h["id"]: h for h in json.load(open(os.path.join(DATA, "heroes.json"), encoding="utf-8"))["heroes"]}
    out = {}
    for s in st:
        if s["zone"] == zone and s.get("tag") == "hero":
            h = H.get(s["enemies"][0]["hero"], {})
            f = [x.get("aola") for x in h.get("forms", [])]
            out[s["idx"]] = (f[0] if f else h.get("aola"), h.get("name", ""))
    return out


def main(isl):
    zone = isl.split("_")[1]
    m0 = os.path.join(HERE, isl, "m0")
    spec = importlib.util.spec_from_file_location("dt_" + zone, os.path.join(m0, "diem_tho.py"))
    dt = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dt)
    src = open(os.path.join(m0, "do_duong.py"), encoding="utf-8").read()
    nen = src.split('SRC = "')[1].split('"')[0]
    im = Image.open(os.path.join(m0, nen)).convert("RGBA")
    im = im.resize((im.width * SC, im.height * SC), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 26)
    b = bosses(zone)
    for st, (cx, cy), s, side in dt.HABS:
        aola, name = b.get(st, (None, ""))
        p = os.path.join(RES, str(aola), f"{aola}_portrait.png")
        rx, ry = getattr(dt, "RING_OF", {}).get(st, dt.RING[s])
        if os.path.exists(p):
            por = Image.open(p).convert("RGBA")
            hgt = int((160 if s >= 4 else 130) * SC)
            por = por.resize((int(por.width * hgt / por.height), hgt), Image.LANCZOS)
            bb = por.getbbox() or (0, 0, por.width, por.height)
            foot = bb[3]
            im.alpha_composite(por, (int(cx * SC - por.width / 2), int(cy * SC + ry * SC * 0.35 - foot)))
        d.text((cx * SC, (cy + ry) * SC + 6), f"{st} {name}", fill=(40, 20, 10), font=f, anchor="mt", stroke_width=4,
               stroke_fill=(255, 255, 255))
    out = os.path.join(HERE, isl, "m1")
    os.makedirs(out, exist_ok=True)
    im.convert("RGB").save(os.path.join(out, "xem_boss.png"), quality=90)
    print(isl, os.path.join(out, "xem_boss.png"))


if __name__ == "__main__":
    for isl in (sys.argv[1:] or ["land_moc", "land_hoa", "land_kim", "land_tho"]):
        main(isl)
