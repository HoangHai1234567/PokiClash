# Tách tuyết từ ảnh GPT vẽ lại (gen/<tờ>.png) rồi ghép lên ảnh gốc ở cỡ thật, cho màn Nhà và đảo Casino mùa Noel (người dùng
# 2026-11-27: "làm tuyết phủ lên đảo / cây cối / các building"). Cách tách như tach_tuyet.py của sảnh: mỗi ảnh trên tờ khớp ECC affine
# về ảnh gốc (đã thu đúng cỡ trên tờ, đặt trên nền xanh của tờ), lấy điểm tuyết (sáng, ít màu, ảnh gốc chỗ đó chưa trắng), dọn đốm, thêm
# viền mực nâu của chính đống tuyết; lớp tuyết phóng về cỡ ảnh gốc rồi phủ lên ảnh gốc. Mũ tuyết được nhô ra ngoài hình một chút (mái,
# lều) nhưng không ra khỏi khung ảnh; nền đảo không phủ tuyết lên nước (biển, hồ, suối, thác).
# Ra out/noel/<tên>.png (ảnh gốc + tuyết, đúng cỡ ảnh gốc; cây: ghép lại thành atlas home_trees.png đúng bố cục atlas gốc) và
# out/xem_<tờ>.jpg (tờ gốc | tờ ghép tuyết | ảnh GPT).
# py -3 -I tach_map.py [tờ ...]
import json, os, sys
import cv2
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
ART = os.path.join(PROJ, "Assets", "03 Art")
TO, GEN, OUT = (os.path.join(HERE, d) for d in ("to", "gen", "out"))
NOEL = os.path.join(OUT, "noel")
os.makedirs(NOEL, exist_ok=True)
sys.stdout.reconfigure(encoding="utf-8")
BG = np.array([62, 118, 168], np.uint8)
BASES = {"casino_dao", "home_base"}  # nền đảo: không nhô ra ngoài đất, không phủ nước


def snow_of(rgb):
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV).astype(np.float32)
    v, sat = hsv[..., 2] / 255, hsv[..., 1] / 255
    return (v > 0.78) & (sat < 0.20)


def white_of(rgb):
    """Chỗ ảnh gốc đã trắng sẵn (khói, khung cửa, bọt sóng): không tính là tuyết mới. Đá xám nhạt không tính (để nhận tuyết)."""
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV).astype(np.float32)
    return (hsv[..., 2] > 0.88 * 255) & (hsv[..., 1] < 0.12 * 255)


def water_of(rgb):
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    return (h >= 88) & (h <= 128) & (s > 80) & (v > 90)


def align(src_rgb, dst_rgb, mask):
    g1 = cv2.GaussianBlur(cv2.cvtColor(dst_rgb, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255, (5, 5), 0)
    g2 = cv2.GaussianBlur(cv2.cvtColor(src_rgb, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255, (5, 5), 0)
    # affine; vật mảnh (cọc dây) ECC affine không hội tụ thì thử chỉ dời
    for motion in (cv2.MOTION_AFFINE, cv2.MOTION_TRANSLATION):
        warp = np.eye(2, 3, dtype=np.float32)
        try:
            cc, warp = cv2.findTransformECC(g1, g2, warp, motion,
                                            (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6), mask, 5)
            return warp, cc
        except cv2.error:
            pass
    # ECC không hội tụ (mái phủ tuyết dày đổi quá nhiều điểm): dò dời ±12 px cho nét mực hai ảnh trùng nhiều nhất (nét viền không đổi)
    ink_r = (g1 < 0.35) & (mask > 0)
    ink_g = cv2.dilate((g2 < 0.35).astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
    best, bd = -1, (0, 0)
    for dy in range(-12, 13):
        for dx in range(-12, 13):
            sc = int((ink_r & np.roll(ink_g, (-dy, -dx), (0, 1))).sum())
            if sc > best:
                best, bd = sc, (dx, dy)
    print(f"   ECC không hội tụ, dò nét mực: dời {bd}, trùng {best / max(1, int(ink_r.sum())):.2f}")
    return np.array([[1, 0, bd[0]], [0, 1, bd[1]]], np.float32), best / max(1, int(ink_r.sum()))


def unpremul_resize(rgba, size):
    a = rgba[..., 3:4].astype(np.float32) / 255
    pre = np.concatenate([rgba[..., :3].astype(np.float32) * a, a * 255], -1)
    pre = cv2.resize(pre, size, interpolation=cv2.INTER_CUBIC)
    pre = np.clip(pre, 0, 255)
    al = pre[..., 3:4] / 255
    rgb = np.where(al > 1e-3, pre[..., :3] / np.maximum(al, 1e-3), 0)
    return np.concatenate([np.clip(rgb, 0, 255), pre[..., 3:4]], -1).astype(np.uint8)


def one(name, orig, dst, gpt, base):
    """orig: RGBA cỡ gốc; dst: khung trên tờ; gpt: ảnh GPT cả tờ. Trả (ảnh ghép cỡ gốc, phần trăm phủ)."""
    x, y, w, h = dst
    m = 0 if base else 18
    Hs, Ws = gpt.shape[:2]
    x0, y0, x1, y1 = max(0, x - m), max(0, y - m), min(Ws, x + w + m), min(Hs, y + h + m)
    rw, rh = x1 - x0, y1 - y0
    small = cv2.resize(orig, (w, h), interpolation=cv2.INTER_AREA)
    ref = np.zeros((rh, rw, 4), np.uint8)
    ref[..., :3] = BG
    ref[y - y0:y - y0 + h, x - x0:x - x0 + w] = small
    a = ref[..., 3:4].astype(np.float32) / 255
    a[...] = 0
    a[y - y0:y - y0 + h, x - x0:x - x0 + w, 0] = small[..., 3] / 255
    refrgb = (ref[..., :3] * a + BG * (1 - a)).astype(np.uint8)
    alpha_s = (a[..., 0] * 255).astype(np.uint8)
    reg = gpt[y0:y1, x0:x1].copy()
    emask = cv2.dilate((alpha_s > 100).astype(np.uint8), np.ones((9, 9), np.uint8))
    warp, cc = align(reg, refrgb, emask)
    al = cv2.warpAffine(reg, warp, (rw, rh), flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REPLICATE)
    if base:
        allowed = (alpha_s > 200) & ~water_of(refrgb)
    else:
        allowed = cv2.dilate((alpha_s > 100).astype(np.uint8), np.ones((9, 9), np.uint8)) > 0
    snow = snow_of(al) & ~white_of(refrgb) & allowed
    mk = snow.astype(np.uint8) * 255
    mk = cv2.morphologyEx(mk, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
    mk = cv2.morphologyEx(mk, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    mk[~allowed] = 0
    n, lab, st, _ = cv2.connectedComponentsWithStats(mk, 8)
    keep = np.zeros(n, bool)
    keep[1:] = st[1:, cv2.CC_STAT_AREA] >= 14
    mk = (keep[lab] * 255).astype(np.uint8)
    # viền cỏ sót: điểm cỏ xanh của ảnh gốc sát tuyết (trong 4 px) mà ảnh GPT ở đó sáng (tuyết, mép tuyết) thì cũng là tuyết; nét mực
    # (GPT tối) giữ nguyên. GPT vẽ lệch vài px quanh cây, mép đường nên viền cỏ mảnh lộ ra giữa tuyết và mép.
    hsv_r = cv2.cvtColor(refrgb, cv2.COLOR_RGB2HSV)
    hsv_g = cv2.cvtColor(al, cv2.COLOR_RGB2HSV)
    grass = (hsv_r[..., 0] >= 32) & (hsv_r[..., 0] <= 85) & (hsv_r[..., 1] > 60)
    light = (hsv_g[..., 2] > 160) & (hsv_g[..., 1] < 95)
    near = cv2.dilate(mk, np.ones((9, 9), np.uint8)) > 0
    mk[grass & light & near & allowed] = 255
    # viền mực của đống tuyết: điểm tối của ảnh GPT sát quanh tuyết (vòng 2–3 px)
    ring = cv2.dilate(mk, np.ones((5, 5), np.uint8)) & ~mk
    v = cv2.cvtColor(al, cv2.COLOR_RGB2HSV)[..., 2]
    ink = (ring > 0) & (v < 115) & allowed
    alpha = np.maximum(cv2.GaussianBlur(mk, (3, 3), 0), ink.astype(np.uint8) * 230)
    alpha[~allowed] = 0
    layer = np.dstack([al, alpha]).astype(np.uint8)
    # phần lớp tuyết trùng khung ảnh gốc, phóng về cỡ gốc
    crop = layer[y - y0:y - y0 + h, x - x0:x - x0 + w]
    H0, W0 = orig.shape[:2]
    big = unpremul_resize(crop, (W0, H0))
    out = Image.fromarray(orig)
    out.alpha_composite(Image.fromarray(big))
    out = np.array(out)
    land = max(1, int((small[..., 3] > 128).sum()))
    pct = 100 * int((crop[..., 3] > 128).sum()) / land
    return out, pct, cc


def run(sheet):
    meta = json.load(open(os.path.join(TO, sheet + ".json"), encoding="utf-8"))
    gpt = np.array(Image.open(os.path.join(GEN, sheet + ".png")).convert("RGB").resize((meta["W"], meta["H"]), Image.LANCZOS))
    base = sheet in BASES
    comp = Image.new("RGBA", (meta["W"], meta["H"]), tuple(BG) + (255,))
    results = {}
    for it in meta["items"]:
        im = Image.open(os.path.join(ART, it["src"])).convert("RGBA")
        cx, cy, cw, ch = it["crop"]
        orig = np.array(im.crop((cx, cy, cx + cw, cy + ch)))
        out, pct, cc = one(it["name"], orig, it["dst"], gpt, base)
        results[it["name"]] = (it, out)
        print(f"  {it['name']:22s} ECC {cc:.3f}  tuyết {pct:4.0f}%")
        x, y, w, h = it["dst"]
        comp.alpha_composite(Image.fromarray(out).resize((w, h), Image.LANCZOS), (x, y))
    # ghi ảnh ghép: ảnh rời theo tên; ảnh cắt từ atlas thì ghép lại atlas đúng bố cục
    atlases = {}
    for name, (it, out) in results.items():
        if it["crop"][0] == 0 and it["crop"][1] == 0 and Image.open(os.path.join(ART, it["src"])).size == (it["crop"][2], it["crop"][3]):
            Image.fromarray(out).save(os.path.join(NOEL, name + ".png"), optimize=True)
        else:
            atlases.setdefault(it["src"], []).append((it, out))
    for srcp, lst in atlases.items():
        src = Image.open(os.path.join(ART, srcp)).convert("RGBA")
        at = src.copy()
        for it, out in lst:
            cx, cy, cw, ch = it["crop"]
            at.paste(Image.fromarray(out), (cx, cy))
        nm = os.path.splitext(os.path.basename(srcp))[0]
        at.save(os.path.join(NOEL, nm + ".png"), optimize=True)
        print(f"  atlas {nm}: {len(lst)} ảnh")
    orig_sheet = Image.open(os.path.join(TO, sheet + ".png")).convert("RGB")
    W, H = meta["W"], meta["H"]
    view = Image.new("RGB", (W * 3 + 40, H), (40, 40, 40))
    view.paste(orig_sheet, (0, 0))
    view.paste(comp.convert("RGB"), (W + 20, 0))
    view.paste(Image.fromarray(gpt), (2 * W + 40, 0))
    view.thumbnail((3000, 3000))
    view.save(os.path.join(OUT, f"xem_{sheet}.jpg"), quality=85)
    comp.convert("RGB").save(os.path.join(OUT, f"ghep_{sheet}.jpg"), quality=90)


if __name__ == "__main__":
    sheets = sys.argv[1:] or [os.path.splitext(f)[0] for f in sorted(os.listdir(GEN)) if f.endswith(".png")]
    for s in sheets:
        print(s)
        run(s)
