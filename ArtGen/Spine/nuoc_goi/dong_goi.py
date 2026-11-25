# -*- coding: utf-8 -*-
"""ĐÓNG GÓI FLIPBOOK NƯỚC từ hai gói mẫu (người dùng 2026-11-25: "làm lại vfx nước của game theo asset này ... dùng thẳng nhưng nên thay đổi
đi chút, xem cả 2 package") thành atlas "giá trị + alpha" cho shader PokiClash/UIWaterFx (chế độ 6 flipbook, 7 ống tia):
  - mỗi khung: độ sáng (luminance) chuẩn hoá theo cả flipbook (2 % → 0, 98 % → 1) + alpha; shader tô lại bằng dải màu cel lam nhạt / bọt
    trắng của game + vân chì vẽ tay (đây là phần "thay đổi": màu, dải, nét chì của mình; dáng + nhịp giữ của gói);
  - một ô atlas chứa HAI flipbook: cặp 0 ở RG (giá trị, alpha), cặp 1 ở BA;
  - texture lặp nuoc_vet.png: R vân nước sắc (tia), G lưới vân nước toon, B nhiễu tan, A vệt đuôi.
Ra: Assets/03 Art/Fx/Nuoc/nuoc_fb.png (2048²), nuoc_vet.png (512²), Assets/01 Script/Game/Battle/NuocFbBang.cs (bảng UV, SINH TỰ ĐỘNG),
ArtGen/Spine/nuoc_goi/manifest.json, NGUON.md (danh sách nguồn → để thay trước khi phát hành nếu cần).
    py -3 -I dong_goi.py
"""
import json
import math
import os

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
RUB = os.path.join(PROJ, "Assets", "SrRubfish_VFX_02", "Textures")
NAMU = os.path.join(PROJ, "Assets", "NamuFX")
OUT_TEX = os.path.join(PROJ, "Assets", "03 Art", "Fx", "Nuoc")
OUT_CS = os.path.join(PROJ, "Assets", "01 Script", "Game", "Battle", "NuocFbBang.cs")
ATLAS = 2048

W = "Flipbooks/Water/"
S = "Shared/"
# (mã trong game, file nguồn (Rubfish), cột, hàng, cỡ ô w×h trong atlas, ghi chú dùng cho gì)
FB = [
    ("Xoan", W + "FX_TX_TwirlingWater_2x8_01.png", 2, 8, 256, 64, "vệt xoắn cuộn quanh thân tia / mũ đầu tia (Water Laser LaserNoise03/05)"),
    ("NuocNgang", W + "FX_TX_LateralWater_01_3x4.png", 3, 4, 128, 128, "lá nước xoay ở đầu tia (Laser LaserNoise06)"),
    ("VongNuoc", W + "FX_TX_TiledWater_3x4_01_SoftRender.png", 3, 4, 256, 128, "vòng nước nở quanh thân tia / gốc (Laser WaterAOE)"),
    ("Toe", W + "FX_TX_NormalSplash_4x4_01.png", 4, 4, 128, 128, "toé thường (Laser Splashes)"),
    ("ToeNgangA", W + "FX_TX_LateralSplash_2x5_03.png", 2, 5, 192, 108, "toé ngang có hướng (Laser Impact WaterDirectionalImpact)"),
    ("ToeNgangB", W + "FX_TX_LateralSplash_2x5_04.png", 2, 5, 192, 102, "toé ngang có hướng 2"),
    ("TruotDat", W + "FX_TX_LateralWaterSlide_4x4_01.png", 4, 4, 160, 87, "vệt nước loang trượt trên đất (Laser LateralWater_Lingering)"),
    ("ChamDat", W + "FX_TX_WaterDots_4x4_01.png", 4, 4, 128, 128, "vòng gợn chấm trên đất (GroundDots)"),
    ("MuaA", W + "FX_TX_RainSplash_02.png", 4, 4, 128, 64, "toé hạt mưa trên đất (WaterGround_01)"),
    ("MuaB", W + "FX_TX_RainSplash_03.png", 3, 3, 128, 64, "toé hạt mưa 2 (WaterGround_03)"),
    ("MuaC", W + "FX_TX_RainSplash_01.png", 4, 3, 96, 96, "toé hạt mưa 3 (WaterGround_04)"),
    ("MuaD", W + "FX_TX_RainSplash_04.png", 4, 3, 96, 96, "toé hạt mưa 4 (WaterGround_02)"),
    ("Giot", S + "FX_TX_FlipbookDots_02.png", 2, 2, 64, 64, "giọt bắn kéo dài (Dots / DotsDirectional)"),
    ("BongNho", S + "fx_tx_bubbles_2x2_01.png", 2, 2, 64, 64, "bong bóng trong lòng tia (DotsDirectionalInside)"),
    ("GaiTrung", S + "FX_TX_ImpactShapes_Sharp_01.png", 2, 2, 128, 128, "gai sắc chỗ trúng (Impact LightImpact / ImpactSpikes)"),
    ("ChopHuong", S + "FX_TX_DirectionalImpact_02.png", 1, 1, 128, 128, "chớp trúng có hướng (Impact Impact)"),
    ("ChopTron", S + "FX_TX_Animeimpact_Circular_01.png", 1, 1, 128, 128, "chớp trúng tròn (Impact CenterImpact)"),
    ("ToeGiua", W + "FX_TX_SimpleCenterSplash_4x4_01.png", 4, 4, 128, 128, "toé bung giữa (SimpleSplash)"),
    ("ToeDon", W + "FX_TX_WaterSimpleSplash_4x4_01.png", 4, 4, 128, 128, "toé đơn (SimpleWaterImpact)"),
    ("ToeTrung", W + "FX_TX_SimpleImpactWater_4x4_01.png", 4, 4, 128, 128, "toé trúng đạn (Water_Impact_01)"),
    ("ToeVa", W + "FX_TX_ImpactSplash_4x4_01.png", 4, 4, 128, 128, "toé va (ImpactGround)"),
    ("CotDung", W + "FX_TX_VerticalSplash_4x4_02.png", 4, 4, 80, 128, "cột nước dựng (mạch phun / ImpactGround)"),
    ("ToeDat", W + "FX_TX_GroundWaterSplash_4x4_01.png", 4, 4, 160, 80, "toé trên đất (Water_ImpactGround)"),
    ("CauVong", W + "FX_TX_WaterLoop_01.png", 5, 5, 112, 112, "khối nước cuộn vòng (Orb / StrongProjectile)"),
    ("BongVo", W + "FX_TX_BubbleExplode_3x3_01.png", 3, 3, 112, 112, "bong bóng vỡ (Bubble)"),
    ("BongDon", W + "FX_TX_SmpleBubble_4x4_01.png", 4, 4, 80, 80, "bong bóng đơn"),
    ("Chem", W + "FX_TX_MainSlash_4x4_01.png", 4, 4, 256, 64, "lưỡi chém nước (WaveAttack / Slash)"),
    ("SongTruot", W + "FX_TX_LateralSplashSlides_4x6_02.png", 4, 6, 128, 74, "sóng trượt ngang (WaveAttack Projectile)"),
    ("Roi", W + "FX_TX_WaterWhip_4x4_02.png", 4, 4, 112, 112, "roi nước (Whip)"),
    ("GonMua", W + "FX_TX_WaterRipples_4x3_01.png", 4, 3, 112, 112, "vòng gợn mưa (RainExample)"),
    ("XoayO", W + "FX_TX_TwirlTiled_4x5_01.png", 4, 5, 160, 96, "lốc xoáy ô lặp (Buff / whirl)"),
    ("BotKhoi", W + "FX_TX_FoamSmoke_4x4_01.png", 4, 4, 96, 96, "khói bọt (FoamImpact)"),
    ("ChemVong", W + "FX_TX_CicularSlash_4x4_01.png", 4, 4, 112, 112, "chém vòng tròn (SlashBasic / whirl)"),
    ("ToeNgangC", W + "FX_TX_WaterLateralImpact_4x3_01.png", 4, 3, 112, 112, "toé ngang 3 (StrongProjectile Impact)"),
    ("ToeNho", W + "FX_TX_MiniSplash_2x6_01.png", 2, 6, 128, 57, "toé nhỏ"),
    ("ToeGiuaNho", W + "FX_TX_SmallSplashCenter_01_6x8.png", 6, 8, 80, 60, "toé nhỏ bung giữa (Projectile)"),
    ("NuocRoi", W + "FX_TX_FallingWater_4x3_01.png", 4, 3, 64, 128, "nước rơi (FallingWater)"),
    ("ToeDatLon", W + "FX_TX_GroundSplash_5x5_01.png", 5, 5, 112, 83, "toé đất lớn (Grenade Explosion)"),
    ("BotRieng", W + "FX_TX_FoamIndividual_4x4_01.png", 4, 4, 80, 80, "bọt rời (Waterfall foam)"),
    ("VetSang", W + "FX_TX_HighlightSlash_2x5_01.png", 2, 5, 192, 29, "vệt sáng lưỡi chém (Slash highlight)"),
]
# texture lặp: (kênh, nguồn, cách lấy)
VET = [
    ("R", os.path.join(RUB, S + "FX_TX_WaterNoise_Sharp.png"), "lum"),       # vân nước sắc: thân tia (LaserNoise, ComplexGradient trôi)
    ("G", os.path.join(NAMU, "StylizedWaterEffects", "Textures", "Tex_Water_01.tga"), "R"),  # lưới vân nước toon (NamuFX SH_Water_Base)
    ("B", os.path.join(RUB, S + "FX_TX_FlamesNoise_01.png"), "lum"),        # nhiễu tan (dissolve)
    ("A", os.path.join(RUB, S + "FX_TX_WaterTrail_01.png"), "a"),           # vệt đuôi (trail)
]


def frames_of(path, cols, rows):
    im = Image.open(path).convert("RGBA")
    a = np.asarray(im).astype(np.float32) / 255
    H, Wd = a.shape[:2]
    fw, fh = Wd / cols, H / rows
    out = []
    for r in range(rows):
        for c in range(cols):
            x0, y0 = round(c * fw), round(r * fh)
            fr = a[y0:round(y0 + fh), x0:round(x0 + fw)]
            if a[..., 3].mean() > 0.9:  # texture alpha đặc (hình nằm trong kênh màu trên nền đen: chớp, gai trúng) → alpha = kênh sáng nhất
                fr = fr.copy()
                fr[..., 3] = np.clip(fr[..., :3].max(axis=2) * 1.4 - 0.08, 0, 1)
            if fr[..., 3].sum() < 4:  # khung rỗng ở cuối tờ
                continue
            out.append(fr)
    return out, fw / fh


def to_va(frames):
    """giá trị (độ sáng chuẩn hoá theo cả flipbook) + alpha, khử viền tối khi thu nhỏ (nhân / chia alpha)."""
    lum = [0.30 * f[..., 0] + 0.59 * f[..., 1] + 0.11 * f[..., 2] for f in frames]
    allv = np.concatenate([l[f[..., 3] > 0.25] for l, f in zip(lum, frames)])
    lo, hi = (np.percentile(allv, 2), np.percentile(allv, 98)) if allv.size else (0, 1)
    hi = max(hi, lo + 0.05)
    return [(np.clip((l - lo) / (hi - lo), 0, 1), f[..., 3]) for l, f in zip(lum, frames)]


def resize_va(v, a, w, h):
    va = Image.fromarray((v * a * 255).astype(np.uint8)).resize((w, h), Image.LANCZOS)
    aa = Image.fromarray((a * 255).astype(np.uint8)).resize((w, h), Image.LANCZOS)
    va, aa = np.asarray(va).astype(np.float32), np.asarray(aa).astype(np.float32)
    v2 = np.where(aa > 2, va / np.maximum(aa, 1) * 255, 0)
    return np.clip(v2, 0, 255).astype(np.uint8), aa.astype(np.uint8)


# ---- xếp khối (kệ) vào 2 lớp (cặp kênh) của atlas 2048²
items = []
for code, rel, cols, rows, cw, ch, note in FB:
    src = os.path.join(RUB, rel)
    frs, asp = frames_of(src, cols, rows)
    n = len(frs)
    cols2 = cols
    rows2 = math.ceil(n / cols2)
    items.append(dict(code=code, src=rel, note=note, frames=frs, n=n, cols=cols2, rows=rows2, cw=cw, ch=ch, aspect=asp,
                      bw=cols2 * cw, bh=rows2 * ch))
order = sorted(items, key=lambda it: -it["bh"])
layers = [np.zeros((ATLAS, ATLAS, 2), np.uint8), np.zeros((ATLAS, ATLAS, 2), np.uint8)]
state = [[0, 0, 0], [0, 0, 0]]  # x, y, shelf h
for it in order:
    best = None
    for L in range(2):  # thử cả hai lớp, chọn chỗ thấp hơn
        x, y, sh = state[L]
        if x + it["bw"] > ATLAS:
            x, y, sh = 0, y + sh, 0
        if y + it["bh"] <= ATLAS and (best is None or y < best[2]):
            best = (L, x, y, sh)
    assert best, f"atlas full: {it['code']}"
    L, x, y, sh = best
    it.update(layer=L, bx=x, by=y)
    state[L] = [x + it["bw"], y, max(sh, it["bh"])]
    vas = to_va(it["frames"])
    for i, (v, a) in enumerate(vas):
        c, r = i % it["cols"], i // it["cols"]
        v2, a2 = resize_va(v, a, it["cw"], it["ch"])
        x0, y0 = it["bx"] + c * it["cw"], it["by"] + r * it["ch"]
        layers[it["layer"]][y0:y0 + it["ch"], x0:x0 + it["cw"], 0] = v2
        layers[it["layer"]][y0:y0 + it["ch"], x0:x0 + it["cw"], 1] = a2
    del it["frames"]
    print(f"{it['code']:12s} {it['n']:3d} fr  L{it['layer']} @ ({it['bx']},{it['by']}) {it['bw']}x{it['bh']}")
atlas = np.concatenate([layers[0], layers[1]], axis=2)
os.makedirs(OUT_TEX, exist_ok=True)
Image.fromarray(atlas, "RGBA").save(os.path.join(OUT_TEX, "nuoc_fb.png"), optimize=True)
for L in range(2):
    print(f"L{L}: used y = {state[L][1] + state[L][2]} / {ATLAS}")

# ---- texture lặp
vet = np.zeros((512, 512, 4), np.uint8)
for k, (ch, path, how) in enumerate(VET):
    im = Image.open(path).convert("RGBA").resize((512, 512), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32)
    if how == "lum":
        v = 0.30 * a[..., 0] + 0.59 * a[..., 1] + 0.11 * a[..., 2]
    elif how == "a":
        v = a[..., 3]
    else:
        v = a[..., "RGBA".index(how)]
    vet[..., k] = np.clip(v, 0, 255).astype(np.uint8)
Image.fromarray(vet, "RGBA").save(os.path.join(OUT_TEX, "nuoc_vet.png"), optimize=True)

# ---- manifest + bảng C#
man = []
for it in items:
    man.append({k: it[k] for k in ("code", "src", "note", "n", "cols", "rows", "cw", "ch", "aspect", "layer", "bx", "by")})
json.dump(man, open(os.path.join(HERE, "manifest.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
lines = []
for i, it in enumerate(items):
    u0 = it["bx"] / ATLAS
    v1 = 1 - it["by"] / ATLAS  # mép trên của khối (v của Unity tính từ đáy)
    lines.append(f"            new NFbDef({u0:.6f}f, {v1:.6f}f, {it['cw'] / ATLAS:.6f}f, {it['ch'] / ATLAS:.6f}f, {it['cols']}, {it['n']}, {it['layer']}, "
                 f"{it['aspect']:.4f}f), // {i} {it['code']}: {it['note']}")
enum = ", ".join(it["code"] for it in items)
cs = f"""// SINH TỰ ĐỘNG bởi ArtGen/Spine/nuoc_goi/dong_goi.py — đừng sửa tay (chạy lại script).
// Bảng UV các flipbook nước trong atlas Assets/03 Art/Fx/Nuoc/nuoc_fb.png (2048², cặp 0 = RG (giá trị, alpha), cặp 1 = BA).
// Nguồn từng flipbook: ArtGen/Spine/nuoc_goi/NGUON.md (gói SrRubfish Water VFX 02, người dùng 2026-11-25 cho dùng, có biến đổi).
namespace PokiClash
{{
    public enum NFb {{ {enum} }}

    public readonly struct NFbDef
    {{
        public readonly float u0, vTop, cu, cv, aspect;
        public readonly int cols, frames, pair;

        public NFbDef(float u0, float vTop, float cu, float cv, int cols, int frames, int pair, float aspect)
        {{
            this.u0 = u0;
            this.vTop = vTop;
            this.cu = cu;
            this.cv = cv;
            this.cols = cols;
            this.frames = frames;
            this.pair = pair;
            this.aspect = aspect;
        }}

        // góc dưới trái (uv) của khung i (ô hàng r tính từ trên xuống)
        public UnityEngine.Vector2 Min(int i)
        {{
            int c = i % cols, r = i / cols;
            return new UnityEngine.Vector2(u0 + c * cu, vTop - (r + 1) * cv);
        }}
    }}

    public static class NuocFbBang
    {{
        public static readonly NFbDef[] Defs =
        {{
{chr(10).join(lines)}
        }};

        public static NFbDef Get(NFb f) => Defs[(int)f];
    }}
}}
"""
open(OUT_CS, "w", encoding="utf-8").write(cs)

src_lines = "\n".join(f"| `{it['code']}` | `{it['src']}` | {it['n']} | {it['note']} |" for it in items)
open(os.path.join(HERE, "NGUON.md"), "w", encoding="utf-8").write(
    "# Nguồn texture của bộ nước (atlas nuoc_fb.png, nuoc_vet.png)\n\n"
    "Người dùng 2026-11-25 cho dùng thẳng texture của hai gói mẫu, có biến đổi (độ sáng → dải màu cel của game + vân chì). Gói "
    "SrRubfish \"Water - Assets for VFX 02\" tải qua Baidu Netdisk, chưa rõ đã mua trên Asset Store: nếu chưa, phải thay các flipbook "
    "dưới đây bằng bản tự làm trước khi phát hành (chạy lại dong_goi.py với nguồn mới, giữ mã).\n\n"
    "| Mã | Nguồn (Assets/SrRubfish_VFX_02/Textures/) | Khung | Dùng cho |\n|---|---|---|---|\n" + src_lines +
    "\n\nTexture lặp `nuoc_vet.png`: R `Shared/FX_TX_WaterNoise_Sharp.png` (Rubfish), G kênh R của `Tex_Water_01.tga` (NamuFX), "
    "B `Shared/FX_TX_FlamesNoise_01.png` (Rubfish), A alpha của `Shared/FX_TX_WaterTrail_01.png` (Rubfish).\n")
print("ok", len(items), "flipbook")
