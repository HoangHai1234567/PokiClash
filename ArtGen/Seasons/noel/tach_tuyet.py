# Tách lớp tuyết phủ đảo sảnh mùa Noel (người dùng 2026-11-27).
# Mỗi đảo: ảnh gốc Assets/03 Art/Islands/sanh_dao_<hệ>.png (đã đệm thêm nền biển cho đúng tỉ lệ khung GPT, số đệm ở gen/pad_meta.json)
# và ảnh GPT 2.6 vẽ lại có tuyết (gen/tuyet_<hệ>.png). Script: đổi cỡ, cắt bỏ phần đệm, khớp ảnh GPT về ảnh gốc (ECC affine trên ảnh
# xám), lấy điểm "tuyết" (sáng, ít màu, ảnh gốc ở đó chưa trắng), dọn đốm, thêm viền mực nâu của chính đống tuyết, ra lớp RGBA cùng cỡ ảnh
# gốc. Lớp này đặt chồng lên ảnh đảo trong game (HubSeason), không đổi ảnh đảo gốc.
# py -3 -I tach_tuyet.py [hệ ...]   -> out/tuyet_<hệ>.png (lớp tuyết), out/xem_<hệ>.jpg (gốc | gốc + tuyết | ảnh GPT đã khớp)
import json, os, sys
import cv2
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ISL = os.path.join(PROJ, "Assets", "03 Art", "Islands")
GEN = os.path.join(HERE, "gen")
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
sys.stdout.reconfigure(encoding="utf-8")


def align(src_rgb, dst_rgb, mask):
    """Khớp src về dst: ECC affine trên ảnh xám thu nhỏ, trả ma trận cho cỡ thật."""
    s = 0.5
    g1 = cv2.cvtColor(dst_rgb, cv2.COLOR_RGB2GRAY)
    g2 = cv2.cvtColor(src_rgb, cv2.COLOR_RGB2GRAY)
    g1s = cv2.resize(g1, None, fx=s, fy=s, interpolation=cv2.INTER_AREA).astype(np.float32) / 255
    g2s = cv2.resize(g2, None, fx=s, fy=s, interpolation=cv2.INTER_AREA).astype(np.float32) / 255
    ms = cv2.resize(mask, (g1s.shape[1], g1s.shape[0]), interpolation=cv2.INTER_NEAREST)
    # làm mờ nhẹ cho ECC hội tụ trên nét chì
    g1s = cv2.GaussianBlur(g1s, (5, 5), 0)
    g2s = cv2.GaussianBlur(g2s, (5, 5), 0)
    warp = np.eye(2, 3, dtype=np.float32)
    try:
        cc, warp = cv2.findTransformECC(g1s, g2s, warp, cv2.MOTION_AFFINE,
                                        (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6), ms, 5)
    except cv2.error as e:
        print("  ECC lỗi, giữ nguyên:", e)
        cc = 0
    warp[:, 2] /= s
    return warp, cc


def snow_of(rgb):
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV).astype(np.float32)
    v, sat = hsv[..., 2] / 255, hsv[..., 1] / 255
    return (v > 0.80) & (sat < 0.20)


def run(k, meta):
    m = meta[k]
    o = np.array(Image.open(os.path.join(ISL, f"sanh_dao_{k}.png")).convert("RGBA"))
    h, w = o.shape[:2]
    g = Image.open(os.path.join(GEN, f"tuyet_{k}.png")).convert("RGB").resize((m["W"], m["H"]), Image.LANCZOS)
    s = np.array(g)[m["y"]:m["y"] + h, m["x"]:m["x"] + w]
    orgb = o[..., :3].copy()
    land = (o[..., 3] > 128).astype(np.uint8)
    warp, cc = align(s, orgb, land)
    sa = cv2.warpAffine(s, warp, (w, h), flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REPLICATE)
    print(f"{k}: ECC {cc:.3f}, dời ({warp[0, 2]:.1f}, {warp[1, 2]:.1f}) px, co ({warp[0, 0]:.3f}, {warp[1, 1]:.3f})")

    snow = snow_of(sa) & ~snow_of(orgb) & (o[..., 3] > 200)
    mk = snow.astype(np.uint8) * 255
    mk = cv2.morphologyEx(mk, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mk = cv2.morphologyEx(mk, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(mk, 8)
    keep = np.zeros(n, bool)
    keep[1:] = st[1:, cv2.CC_STAT_AREA] >= 40
    mk = (keep[lab] * 255).astype(np.uint8)
    # viền mực của đống tuyết: điểm tối của ảnh GPT sát ngay dưới / quanh tuyết (vòng 3 px)
    ring = cv2.dilate(mk, np.ones((5, 5), np.uint8)) & ~mk
    hsv = cv2.cvtColor(sa, cv2.COLOR_RGB2HSV)
    ink = (ring > 0) & (hsv[..., 2] < 110) & (o[..., 3] > 200)
    alpha = np.maximum(cv2.GaussianBlur(mk, (3, 3), 0), ink.astype(np.uint8) * 230)
    alpha = np.minimum(alpha, o[..., 3])
    layer = np.dstack([sa, alpha]).astype(np.uint8)
    Image.fromarray(layer).save(os.path.join(OUT, f"tuyet_{k}.png"), optimize=True)

    comp = Image.fromarray(o).copy()
    comp.alpha_composite(Image.fromarray(layer))
    bg = (62, 118, 168, 255)
    tiles = []
    for im in (Image.fromarray(o), comp, Image.fromarray(np.dstack([sa, o[..., 3]]).astype(np.uint8))):
        t = Image.new("RGBA", im.size, bg)
        t.alpha_composite(im)
        tiles.append(t.convert("RGB"))
    sheet = Image.new("RGB", (w * 3 + 40, h), (40, 40, 40))
    for i, t in enumerate(tiles):
        sheet.paste(t, (i * (w + 20), 0))
    sheet.thumbnail((2400, 2400))
    sheet.save(os.path.join(OUT, f"xem_{k}.jpg"), quality=85)
    print(f"   tuyết phủ {100 * (alpha > 128).sum() / max(1, land.sum()):.0f}% đất")


if __name__ == "__main__":
    meta = json.load(open(os.path.join(GEN, "pad_meta.json")))
    for k in (sys.argv[1:] or ["thuy", "moc", "hoa", "tho", "casino"]):
        run(k, meta)
