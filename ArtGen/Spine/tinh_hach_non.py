# -*- coding: utf-8 -*-
"""Thiên Thạch Thú Non (mã làm việc tinh_hach_non): DẠNG 1 của tướng 9 đảo Thổ (ải 60, id `cu_phu`; dạng 2 = thú thiên thạch
`tinh_hach`, rig monster_3806, ghi chú inbox/tho9_ghichu.md). Người dùng 2026-11-18 (máy D): "làm dạng 1 cho tướng thứ 9 đảo thổ";
chọn "cùng rig 3806" (đổi tỉ lệ ngay trên rig, như Bùn Ngoạm Nhi / Giác Mộc Non) và "Claude tự nghĩ 2 hướng" concept.
Rig, lưới, chuyển động gốc là của nhà phát hành game tham khảo: chỉ dùng nội bộ, không đăng công khai.

Quy trình (skill pokiclash-spine-rig, "DẠNG KHÁC trên CÙNG rig gốc"): tỉ lệ trước (mau/ti_le.json; bố cục chụp bằng da dạng 2 qua
mo_xe/atomik_dang.py, không Chrome), concept vẽ trên bố cục đó, người dùng duyệt, rồi mới làm mảnh + rig.

    tinh_hach_non.py bocuc      mau/ti_le.json, mau/bo_cuc.png (1536x1024), mau/so_ti_le.jpg (gốc, A, B, C), mau/bo_cuc_khung.json
    tinh_hach_non.py concept    gui_gpt/tinh_hach_non/luot_1_concept_<k>.txt + HUONG_DAN.md
"""
import copy
import json
import os
import sys

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "mo_xe"))
import atomik_dang as A  # noqa: E402

CODE = "tinh_hach_non"
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
SRC = os.path.join(ROOT, "Assets", "03 Art", "Heroes", "Resources", "tinh_hach_1", "tinh_hach_1.atomik")
BASE = os.path.join(HERE, "inbox", CODE)
MAU = os.path.join(BASE, "mau")
TAI = os.path.join(BASE, "tai_ve")
GUI = os.path.join(HERE, "gui_gpt", CODE)
DUYET2 = os.path.join(HERE, "inbox", "tinh_hach_1", "tai_ve", "L1_duyet.png")     # concept dạng 2 đã duyệt (D2)
W, H = 1536, 1024

# ---------------------------------------------------------------- tỉ lệ (thử A, B, C trên dáng idle khung 0; soi dáng gắt: không rách)
# all6 đầu (kéo theo hàm all10, lòng miệng); all10 hàm (đặt sau đầu: hàm thật = all6 × all10); all7 khúc thân sau; all4 sống lưng
# (kéo cổ + đầu + rừng sau); dabi_r / dabi_l tay gần / xa; duoi0 đuôi; tt_sau / tt_truoc rừng tinh thể; tt_nam_g tinh thể vắt vai;
# dao_* (+ bóng mờ dao_g1/g2_*) năm thiên thạch bay. Hạ cả con (all3 dy) cho điểm thấp nhất chạm đất như dạng 2.
MET = {f"dao_{i}": 0.6 for i in range(5)}
MET.update({f"dao_g{g}_{i}": 0.6 for i in range(5) for g in (1, 2)})
TI_LE_THU = {
    "A": {"all6": 1.35, "all10": 0.72, "all7": 0.85, "dabi_r": 0.85, "dabi_l": 0.85, "duoi0": 0.65, "tt_sau": 0.55, "tt_truoc": 0.55,
          "tt_nam_g": 0.6, **MET},
    "B": {"all6": 1.5, "all10": 0.65, "all7": 0.8, "all4": 0.9, "dabi_r": 0.8, "dabi_l": 0.8, "duoi0": 0.6, "tt_sau": 0.5,
          "tt_truoc": 0.5, "tt_nam_g": 0.55, **MET},
    "C": {"all6": 1.5, "all10": 0.62, "all7": 0.8, "all4": 0.9, "dabi_r": 0.88, "dabi_l": 0.88, "duoi0": 0.6, "tt_sau": 0.6,
          "tt_truoc": 0.6, "tt_nam_g": 0.6, **MET},
}
CHON = "B"
AN = ("cum", "bay_", "bong")      # bố cục không vẽ thiên thạch bay / quả cầu (concept tự vẽ ba thiên thạch nhỏ theo lời)
PAD = 1.24                        # lề quanh con trên bố cục: chừa chỗ trắng cho ba thiên thạch bay


def nap():
    J, img, _ = A.load(SRC)
    return J, img


def ap_ti_le(J0, ti):
    """nhân tỉ lệ + hạ all3 cho điểm thấp nhất (idle khung 0) trùng dạng 2."""
    y_goc = A.bounds(A.Pose(J0).at(A.clip(J0, "idle"), 0.0))[1]
    J = copy.deepcopy(J0)
    A.scale_bones(J, ti)
    y0 = A.bounds(A.Pose(J).at(A.clip(J, "idle"), 0.0))[1]
    ti2 = dict(ti)
    ti2["all3"] = {"s": 1.0, "dy": round(y_goc - y0, 1)}
    J = copy.deepcopy(J0)
    A.scale_bones(J, ti2)
    return J, ti2


def chi_than(J, P):
    return {s for s, _, _, _ in P.items() if not J["slots"][s]["name"].startswith(AN)}


def bocuc():
    os.makedirs(MAU, exist_ok=True)
    J0, img = nap()
    # tờ so tỉ lệ
    BOX, SC = (-1400, 150, 1250, 2100), 0.28
    tiles = []
    for k in ["goc"] + list(TI_LE_THU):
        J = J0 if k == "goc" else ap_ti_le(J0, TI_LE_THU[k])[0]
        P = A.Pose(J).at(A.clip(J, "idle"), 0.0)
        im = A.render(J, img, P, BOX, SC, bg=(255, 255, 255)).convert("RGB")
        ImageDraw.Draw(im).text((10, 10), k + (" (chọn)" if k == CHON else ""), fill=(200, 0, 0))
        tiles.append(im)
    S = Image.new("RGB", (sum(t.width for t in tiles), tiles[0].height), "white")
    for i, t in enumerate(tiles):
        S.paste(t, (i * t.width, 0))
    S.save(os.path.join(MAU, "so_ti_le.jpg"), quality=88)
    # bố cục của bản chọn
    J, ti = ap_ti_le(J0, TI_LE_THU[CHON])
    json.dump(ti, open(os.path.join(MAU, "ti_le.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    P = A.Pose(J).at(A.clip(J, "idle"), 0.0)
    only = chi_than(J, P)
    xs, ys = [], []
    for s, _, V, _ in P.items():
        if s in only:
            xs += [V[:, 0].min(), V[:, 0].max()]
            ys += [V[:, 1].min(), V[:, 1].max()]
    khung = (float(min(xs)), float(min(ys)), float(max(xs)), float(max(ys)))
    to_rig, to_px, z = A.canvas_map(khung, W, H, pad=PAD)
    cx, cy = (khung[0] + khung[2]) / 2, (khung[1] + khung[3]) / 2
    box = (cx - W * z / 2, cy - H * z / 2, cx + W * z / 2, cy + H * z / 2)
    im = A.render(J, img, P, box, 1 / z, bg=(255, 255, 255), only=only).convert("RGB").resize((W, H), Image.LANCZOS)
    im.save(os.path.join(MAU, "bo_cuc.png"))
    hop = {"khung_rig": [round(v, 1) for v in khung], "px_moi_don_vi": round(1 / z, 4), "slot": {}}
    for s, _, V, _ in P.items():
        if s not in only:
            continue
        q = to_px(V)
        hop["slot"][J["slots"][s]["name"]] = [int(q[:, 0].min()), int(q[:, 1].min()), int(q[:, 0].max()), int(q[:, 1].max())]
    json.dump(hop, open(os.path.join(MAU, "bo_cuc_khung.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("ti_le", CHON, "dy", ti["all3"]["dy"], "| khung rig", hop["khung_rig"], "|", hop["px_moi_don_vi"], "px / đơn vị")
    for k, v in hop["slot"].items():
        print(f"  {k:12s} x {v[0]}-{v[2]}, y {v[1]}-{v[3]}")


# ---------------------------------------------------------------- concept lượt 1 (hai hướng, Magnific GPT 2.6 1k high, 95 credit / ảnh)
R1 = (os.path.join(MAU, "bo_cuc.png"),
      "the PROPORTION GUIDE, 1536x1024, white background: our adult hero re-proportioned as its YOUNG form on the same skeleton (a much "
      "bigger head, a smaller jaw, shorter arms, a short tail, the back crystals cut down), still wearing the adult's skin. Keep its pose, "
      "its facing, its size and place on the canvas and where every part is; redraw the surface as the young form described below",
      "Bố cục dạng non: rig thú thiên thạch đổi tỉ lệ (đầu to 1,5 lần, hàm nhỏ, tay ngắn, đuôi ngắn, rừng tinh thể thu nhỏ), còn mang da "
      "dạng 2, nền trắng 1536×1024, con nhìn sang phải, không có thiên thạch bay. Giữ dáng, chỗ, cỡ từng bộ phận")
R2 = (DUYET2,
      "the APPROVED ADULT form of the same hero, 1536x1024, white background: the young form must clearly be the SAME creature at a "
      "younger age: the same black obsidian hide with amber vein cracks, the same teal and amber crystals, the same pen line, crayon "
      "hatching and flat colouring. Do NOT copy its adult proportions or its huge crystal forest (image 1 gives the proportions)",
      "Concept dạng 2 (Thiên Thạch Thú, hướng D2) đã duyệt: da đá vỏ chai đen mạch hổ phách, rừng trụ tinh thể ngọc lam + hổ phách "
      "trên lưng, năm cụm tinh thể bay. Lấy chất liệu, màu, nét bút, vân sáp; không lấy tỉ lệ người lớn")

# chỗ ba thiên thạch bay trên bố cục (px): chỗ trắng quanh con (con chiếm x 148-1387, y 100-923)
THIEN_THACH = [(250, 330), (1460, 210), (1310, 830)]


def plan(h):
    s = h["slot"]
    f = lambda k: f"x {s[k][0]}-{s[k][2]}, y {s[k][1]}-{s[k][3]}"  # noqa: E731
    xs = [v[0] for v in s.values()] + [v[2] for v in s.values()]
    ys = [v[1] for v in s.values()] + [v[3] for v in s.values()]
    return (
        "BODY PLAN (from image 1, positions on the 1536x1024 canvas; keep it exactly, it is animated with the same skeleton): a young "
        f"meteor beast crouching low and leaning forward, FACING RIGHT, filling about x {min(xs)}-{max(xs)}, y {min(ys)}-{max(ys)}. "
        f"(1) HEAD: BIG for the body, at the upper right ({f('dau')}); one eye visible (three-quarter view to the right) at about "
        "(1200, 475); the blunt snout points right. "
        f"(2) JAW: the lower jaw hangs a little open under the snout ({f('ham')}); the inside of the mouth at {f('long_mieng')}. "
        f"(3) BODY: a rounded hunched body from behind the head down to the left ({f('than')}), the top of the back at about y 260. "
        f"(4) NEAR ARM on the LEFT, in front: a short thick arm from the shoulder down to the ground ({f('tay_gan')}), its clawed hand "
        "resting on the ground at the lower left (x 345-550, y 775-900). "
        f"(5) FAR ARM on the RIGHT, behind: a short arm reaching forward under the head ({f('tay_xa')}), its claws at x 950-1125, "
        "y 695-825. "
        f"(6) TAIL: a short tail lying to the lower LEFT ({f('duoi')}). "
        f"(7) BACK: whatever grows on the back stays inside {f('rung')} (much smaller than the adult's crystal forest). "
        "Same size and same place on the canvas as image 1; every part keeps about the same size and outline as in image 1; every "
        "limb and the head stay joined to the body (no white gaps).")


CHUNG = [
    "HIDE: the same black obsidian rock hide as image 2, a touch softer and warmer for a youngster: #3B3340 on the faces turned to the "
    "viewer, #2A2430 on the faces turned away; big smooth rounded rock plates with few inner lines; only TWO short, thin flat amber "
    "vein cracks #EFA330 on the flank (the adult has bigger ones).",
    "HEAD: a BIG ROUNDED head with a short blunt snout; ONE big round eye (amber-yellow iris #F6C443, a round dark pupil, ONE small "
    "white dot) under a heavy FROWNING brow plate: a determined, ready-to-fight little face (fierce-cute, not sad, not silly). The "
    "mouth a little open: inside terracotta red #A2412E, two small upper fangs and a few small rounded cream teeth #EDE0C2, fewer and "
    "smaller than image 2.",
    "HEAD CREST: a short fan of FIVE small rounded amber crystal nubs #F2A93B (side faces #D98A22) along the top of the head, about "
    "half the height of the crest in image 1.",
    "ARMS: short chunky rock arms; each hand with THREE short blunt cream claws #EDE0C2.",
    "METEORS: THREE small floating METEOR ROCKS in the white space around it, centred at about "
    + ", ".join(f"({x}, {y})" for x, y in THIEN_THACH)
    + ", each 80-120 px wide and NOT touching the body or each other: a rounded chunk of the same black rock with one small amber "
    "crystal and one small teal crystal sprouting from it (the adult has five bigger crystal clusters).",
    "NO moss, no plants, no extra cracks, carvings, runes, spots or pebbles, no glow.",
]

HUONG = {
    "A": ("mầm tinh thể",
          "lưng chỉ nhú BA mầm tinh thể ngắn mập (ngọc lam cao nhất ở giữa, hai mầm hổ phách thấp hai bên) + hai nụ nhỏ dọc sống "
          "lưng; đuôi kết bằng MỘT lưỡi tinh thể ngọc lam nhỏ (dạng 2 là cả rừng tinh thể, đuôi ba lưỡi)",
          ["BACK: instead of the adult's crystal forest, only THREE short stubby crystal SPROUTS growing from the top of the back: a teal "
           "one #3FC1AE (side faces #2A9A8B) in the middle, the tallest (about 150 px), and a shorter amber one #F2A93B (side faces "
           "#D98A22) on each side of it; plus two tiny teal nubs along the spine towards the tail. Each crystal is a simple hexagonal "
           "prism with a pointed tip, growing straight out of the rock.",
           "TAIL: a short tapering rock tail ending in ONE small teal crystal blade (the adult has three)."]),
    "B": ("vỏ thiên thạch",
          "lưng đội một VỎ THIÊN THẠCH tròn nứt (đá xám nâu rỗ ba bốn hố nhỏ, như mai rùa / vỏ trứng), nứt một đường răng cưa trên "
          "đỉnh, lộ ba chóp tinh thể ngọc lam (lớn lên vỏ vỡ thành rừng tinh thể); đuôi kết bằng một nụ tinh thể ngọc lam khép",
          ["BACK: the top of the back is covered by a rounded cracked METEORITE SHELL like a turtle shell or a broken egg: rough "
           "grey-brown rock #6B5E58 (side faces #4E433F) with three or four shallow round crater pits, split open along its top by ONE "
           "jagged zig-zag crack through which three small teal crystal tips #3FC1AE peek out (the adult's crystal forest will burst out "
           "of it later). The shell sits on the back inside the back area given in the body plan.",
           "TAIL: a short tapering rock tail ending in a small CLOSED teal crystal bud #3FC1AE."]),
}

DETAIL = ("DETAIL: about as much detail as image 2 or less: big simple masses, each a flat colour, at most one or two inner lines per "
          "piece; only the details listed under DESIGN.")
MOOD = ("MOOD: the YOUNG form (first evolution stage) of a fierce meteor beast that grows into image 2: chunky, a big head, short limbs, "
        "a determined frown, ready to fight; likeable, NOT a mascot, not babyish-silly, not horror.")
STYLE = ("DRAWING STYLE (very important): hand-drawn on paper exactly like image 2: a wobbly dark-brown INK outline (#2B2118, about "
         "7 px) running all the way round every piece on its silhouette, thinner ink lines (about 4 px) for the few inner lines, and "
         "every area filled with ONE flat colour with visible coloured-pencil / wax-crayon hatching (the hatching is only texture, it "
         "never makes light or dark areas). FLAT COLOUR ONLY: no shading, no light and dark planes, no highlights, no white shine "
         "streaks, no gloss, no gradients, no glow, no rim light; only one small white dot in the eye. NO SHADOWS: no drop shadow, no "
         "cast shadow, no shadow under the body or on the ground. No white sticker border round the character.")


def task():
    return ("TASK: redraw image 1 as the YOUNG FORM (first evolution stage) of the hero in image 2. Keep image 1's pose, facing, size, "
            "place on the canvas and the outline of every part (it is animated with the same skeleton); give it the surface, materials "
            "and colours of image 2 made younger, as described below.")


def concept():
    import tho5
    h = json.load(open(os.path.join(MAU, "bo_cuc_khung.json"), encoding="utf-8"))
    R = [R1, R2]
    hd = ["# Gói gen: Thiên Thạch Thú Non (`tinh_hach_non`), dạng 1 tướng 9 đảo Thổ (ải 60, id `cu_phu`)", "",
          "Rig: `monster_3806` (game tham khảo) đổi tỉ lệ. Ảnh mẫu 1 mang lưới / da dựng từ rig đó: chỉ dùng trong máy, không đăng công khai.",
          "", "## Lượt 1: concept dạng 1, hai hướng (2026-11-18, Magnific GPT 2.6, 1k high, 95 credit / ảnh)", "",
          "Người dùng: \"làm dạng 1 cho tướng thứ 9 đảo thổ\", chọn dựng trên cùng rig 3806 và để Claude tự nghĩ hai hướng. Ảnh 1 là bố cục "
          "dạng non (tỉ lệ đã đổi trên rig, còn mang da dạng 2); ảnh 2 là concept dạng 2 đã duyệt để giữ nhận diện.", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    hd += [f"| {i} | `{tho5.Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
    hd += [""]
    for k, (vi, vi2, rieng) in HUONG.items():
        out = os.path.join(TAI, f"L1_{k}.png")
        p = os.path.join(GUI, f"luot_1_concept_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {tho5.Wp(r)}: {e}" for i, (r, e, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {tho5.Wp(out)}",
              f"If a file with that name already exists, save as L1_{k}_2.png, L1_{k}_3.png ... in the same folder. Do not edit, move or "
              "delete any other file.",
              "", task(), "", plan(h), "", "DESIGN:"] + [f"- {d}" for d in rieng + CHUNG] + ["", DETAIL, "", STYLE, "", MOOD, "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line; the character at the same place and size "
              "as in image 1. No sparkles, no glints, no aura round the character, no smoke, no speed lines, no labels, no frame."]
        tho5.ghi(p, t)
        hd += [f"- **Hướng {k}** ({vi}: {vi2}): file prompt `{tho5.Wp(p)}`; ảnh lưu vào `{tho5.Wp(out)}` (trùng tên thì `_2`, `_3`…)."]
        print(p)
    hd += ["", "Claude tự gen: `py -3 -I ArtGen/Spine/gen_magnific.py <file prompt>` (hoặc gọi thẳng công cụ Magnific trong phiên). "
           "Bản được chọn chép thành `L1_duyet.png` cùng thư mục.", "",
           "Kiểm: đúng dáng, chỗ, cỡ từng bộ phận như ảnh 1 (đầu to bên phải, hàm hé, thân gù, tay gần bên trái chống đất, tay xa vươn dưới "
           "đầu, đuôi ngắn bên trái); rõ là cùng loài với ảnh 2 (da đá đen mạch hổ phách, tinh thể ngọc lam + hổ phách); một mắt, mặt "
           "quả quyết; đủ ba thiên thạch nhỏ bay không chạm thân; nét bút mực rung, vân sáp, tô phẳng, không bóng, không quầng sáng, chỉ một "
           "chấm sáng trong mắt; nền trắng tinh; không viền sticker.",
           "", "Câu sửa nhanh: \"too many details: simplify\"; \"remove the shading / highlights / glow, flat colour only\"; \"keep every part "
           "at the same place and size as image 1\"; \"make the head rounder and the eye bigger, keep the determined frown\"."]
    tho5.ghi(os.path.join(GUI, "HUONG_DAN.md"), hd)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "bocuc":
        bocuc()
    elif cmd == "concept":
        concept()
    else:
        print(__doc__)
