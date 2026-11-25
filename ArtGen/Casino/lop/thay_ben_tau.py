# Thay ảnh bến tàu (ben_tau) bằng bản không có thuyền (ben_tau_trong_1k.png, gen đúng chỗ đúng cỡ): con tàu của game (ShipLook, chuyến
# tàu qua mây sảnh ↔ đảo) cập vào bến này. Cắt cụm điểm trong khung bến (bản 1k), phóng theo tỉ lệ bản 2k (LANCZOS), ghi đè
# cat/ben_tau.png, sửa khung trong cong_trinh.json, chép vào Assets/03 Art/Casino. Công trình khác không đụng tới.
import os, sys, json, shutil
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from xu_ly_2k import components, compose, ART

KHUNG = (370, 765, 1040, 1000)  # bến tàu trên bản 1k


def main():
    im = Image.open(os.path.join(HERE, "ben_tau_trong_1k.png")).convert("RGBA")
    a = im.getchannel("A")
    comps = components(a, thr=60, min_px=30)
    keep = Image.new("L", im.size, 0)
    kp = keep.load()
    for pts in comps:
        cx = sum(p[0] for p in pts) / len(pts)
        cy = sum(p[1] for p in pts) / len(pts)
        if KHUNG[0] <= cx <= KHUNG[2] and KHUNG[1] <= cy <= KHUNG[3]:
            for x, y in pts:
                kp[x, y] = 255
    from PIL import ImageFilter
    keep = keep.filter(ImageFilter.MaxFilter(5))
    alpha = Image.composite(a, Image.new("L", im.size, 0), keep)
    im.putalpha(alpha)
    box = alpha.getbbox()
    cut = im.crop(box)
    meta = json.load(open(os.path.join(HERE, "cong_trinh.json"), encoding="utf-8"))
    sx, sy = meta["w"] / 1536.0, meta["h"] / 1024.0
    x0, y0 = round(box[0] * sx), round(box[1] * sy)
    w2, h2 = round(cut.width * sx), round(cut.height * sy)
    cut = cut.resize((w2, h2), Image.LANCZOS)
    cut.save(os.path.join(HERE, "cat", "ben_tau.png"))
    meta["items"]["ben_tau"] = {"x0": x0, "y0": y0, "x1": x0 + w2, "y1": y0 + h2}
    json.dump(meta, open(os.path.join(HERE, "cong_trinh.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    compose(meta, False).convert("RGB").save(os.path.join(HERE, "ghep_thu_2k.png"))
    compose(meta, True).convert("RGB").save(os.path.join(HERE, "ghep_thu_2k_leu.png"))
    shutil.copy2(os.path.join(HERE, "cat", "ben_tau.png"), os.path.join(ART, "casino_ct_ben_tau.png"))
    json.dump(meta, open(os.path.join(ART, "casino_art.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("ben_tau", meta["items"]["ben_tau"])


if __name__ == "__main__":
    main()
