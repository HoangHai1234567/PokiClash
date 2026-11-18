# -*- coding: utf-8 -*-
"""Thiên Thạch Thú Non (mã làm việc tinh_hach_non): DẠNG 1 của tướng 9 đảo Thổ (ải 60, id `cu_phu`; dạng 2 = thú thiên thạch
`tinh_hach`, rig monster_3806, ghi chú inbox/tho9_ghichu.md). Người dùng 2026-11-18 (máy D): "làm dạng 1 cho tướng thứ 9 đảo thổ";
chọn "cùng rig 3806" (đổi tỉ lệ ngay trên rig, như Bùn Ngoạm Nhi / Giác Mộc Non) và "Claude tự nghĩ 2 hướng" concept.
Rig, lưới, chuyển động gốc là của nhà phát hành game tham khảo: chỉ dùng nội bộ, không đăng công khai.

Quy trình (skill pokiclash-spine-rig, "DẠNG KHÁC trên CÙNG rig gốc"): tỉ lệ trước (mau/ti_le.json; bố cục chụp bằng da dạng 2 qua
mo_xe/atomik_dang.py, không Chrome), concept vẽ trên bố cục đó, người dùng duyệt, rồi mới làm mảnh + rig.

    tinh_hach_non.py bocuc      mau/ti_le.json, mau/bo_cuc.png (1536x1024), mau/so_ti_le.jpg (gốc, A, B, C), mau/bo_cuc_khung.json
    tinh_hach_non.py concept    gui_gpt/tinh_hach_non/luot_1_concept_<k>.txt + HUONG_DAN.md
    (người dùng chọn A 2026-11-18 → tai_ve/L1_duyet.png)
    tinh_hach_non.py can        căn concept A lên bố cục (co k + dời, IoU thân) → mau/can.json, tờ chồng viền mau/_can.jpg
    tinh_hach_non.py manh       file prompt hai tờ mảnh "đúng chỗ, đúng cỡ" → gui_gpt/tinh_hach_non/luot_2_<N>.txt + HUONG_DAN_luot_2.md
    tinh_hach_non.py cat        cắt tai_ve/M_<N>.png + ba thiên thạch thẳng từ concept → manh/<tên>.png, manh/dat.json (hộp px concept A)
Rig: TH_DANG=non py -3 -I tinh_hach_rig.py (cùng script dạng 2; xương nhân ti_le.json, mảnh mới đặt theo concept A qua tf()).
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
import tho5  # noqa: E402

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


# ================================================================ mảnh (người dùng chọn A 2026-11-18 → tai_ve/L1_duyet.png)
# Đo 2026-11-18: da concept A (84, 62, 67) trùng da mảnh dạng 2 (80–90, 62–68, 67–74) → thân, hai tay, móng, lòng miệng, quả cầu của dạng 2
# DÙNG LẠI (rig co theo ti_le.json, như bố cục). Chỉ gen lại chỗ khác hẳn: đầu (tròn, mắt to, diềm năm nụ, hai nanh trên), hàm dưới (ba răng
# sữa), ba mầm tinh thể + hai nụ trên lưng, đuôi một lưỡi. Ba thiên thạch đứng riêng trên concept (viền kín) nên cắt thẳng, khỏi gen.
DUYET = os.path.join(TAI, "L1_duyet.png")
MANH = os.path.join(BASE, "manh")


def _mat_na(p, giu_lon=True):
    import cv2
    import numpy as np
    a = np.asarray(Image.open(p).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
    m = (a.min(2) < 225).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    if giu_lon:
        n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
        m = (lab == 1 + int(np.argmax(st[1:, 4]))).astype(np.uint8)
    ff = m.copy()
    cv2.floodFill(ff, np.zeros((H + 2, W + 2), np.uint8), (0, 0), 2)
    m[ff == 0] = 1
    return m


def can():
    """px concept A → px bố cục: p_b = k · p + (tx, ty); IoU chấm trên phần thân (y > 340 bố cục: lưng / diềm khác nhau có chủ đích),
    concept chỉ lấy khối lớn nhất (bỏ ba thiên thạch)."""
    import cv2
    import numpy as np
    g, c = _mat_na(os.path.join(MAU, "bo_cuc.png")), _mat_na(DUYET)
    ys, xs = np.nonzero(g)
    ys2, xs2 = np.nonzero(c)
    S = 2
    gs = cv2.resize(g, (W // S, H // S), interpolation=cv2.INTER_AREA) > 0
    than = np.zeros_like(gs)
    than[340 // S:, :] = True
    best = None
    for k in np.arange(0.92, 1.06, 0.005):
        for dy in range(-40, 41, 2):
            for dx in range(-40, 41, 2):
                tx = (xs.min() + xs.max()) / 2 - k * (xs2.min() + xs2.max()) / 2 + dx
                ty = ys.max() - k * ys2.max() + dy
                w = cv2.warpAffine(c, np.float32([[k / S, 0, tx / S], [0, k / S, ty / S]]), (W // S, H // S)) > 0
                iou = ((w & gs) & than).sum() / max(1, ((w | gs) & than).sum())
                if best is None or iou > best[0]:
                    best = (float(iou), float(k), float(tx), float(ty))
    iou, k, tx, ty = best
    w = cv2.warpAffine(c, np.float32([[k, 0, tx], [0, k, ty]]), (W, H)) > 0
    ca = float((w & (g > 0)).sum() / (w | (g > 0)).sum())
    json.dump(dict(k=round(k, 4), tx=round(tx, 2), ty=round(ty, 2), iou_than=round(iou, 4), iou=round(ca, 4)),
              open(os.path.join(MAU, "can.json"), "w"), indent=1)
    im = Image.open(DUYET).convert("RGB").resize((W, H)).transform((W, H), Image.AFFINE, (1 / k, 0, -tx / k, 0, 1 / k, -ty / k),
                                                                     Image.BICUBIC, fillcolor=(255, 255, 255))
    arr = np.asarray(im).copy()
    ed = cv2.dilate((cv2.Canny((g * 255).astype(np.uint8), 50, 150) > 0).astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
    arr[ed] = (230, 0, 0)
    Image.fromarray(arr).save(os.path.join(MAU, "_can.jpg"), quality=88)
    print(f"căn: k {k:.3f}, dời ({tx:.1f}, {ty:.1f}); IoU thân {iou:.3f}, cả con {ca:.3f}")


def tf():
    """px concept A ↔ toạ độ rig dạng 1 (rig dạng 2 đã nhân ti_le.json, khung 0 idle): px → bố cục (mau/can.json) → rig (canvas_map của
    bố cục). Trả (px concept mỗi đơn vị rig, to_rig, to_px)."""
    import numpy as np
    c = json.load(open(os.path.join(MAU, "can.json")))
    hop = json.load(open(os.path.join(MAU, "bo_cuc_khung.json"), encoding="utf-8"))
    k, tx, ty = c["k"], c["tx"], c["ty"]
    b_rig, b_px, z = A.canvas_map(tuple(hop["khung_rig"]), W, H, pad=PAD)
    to_rig = lambda P: b_rig(np.asarray(P, float) * k + np.array([tx, ty]))  # noqa: E731
    to_px = lambda V: (b_px(V) - np.array([tx, ty])) / k  # noqa: E731
    return k / z, to_rig, to_px


ANH1_A = ("the APPROVED picture of our character, 1536x1024, white background: a YOUNG black obsidian METEOR BEAST crouching and leaning "
          "to the right, with two flat amber vein cracks on its flank; on its back three short crystal sprouts (amber, a tall turquoise "
          "one, amber) and two tiny turquoise nubs; a BIG rounded head at the upper right with a crest of five amber crystal nubs, a "
          "frowning brow, a big round amber eye, a blunt snout, two cream upper fangs and a slightly open mouth (dark-red inside, three "
          "small cream lower teeth); a thick near arm on the left with three cream claws on the ground, a far arm reaching forward under "
          "the head with two claws; a short tail at the lower left ending in one turquoise crystal blade; three small floating meteor "
          "rocks with amber and turquoise crystals. Hand-drawn: wobbly dark-brown ink line, crayon hatching, flat colours.")
NHOM = {
    "N1": [("dau", "the HEAD: the big rounded head at the upper right, from its back (the big rounded rock plates over the neck, left edge "
            "at about x 800 between y 340 and y 600) to the blunt snout (right edge at about x 1335, y 450-600), with the crest of FIVE amber "
            "crystal nubs along its top and back (at about (920, 295), (1000, 205), (1115, 190), (1225, 245) and (1300, 335)), the heavy "
            "frowning brow, the big round amber eye at about (1170, 480), the nostril, and the TWO cream UPPER FANGS hanging from the upper "
            "jaw at about (1100-1140, 555-610) and (1195-1230, 590-630)",
            "WITHOUT the lower jaw, the lower teeth and the dark-red inside of the mouth: the upper jaw ends along the line of the two upper "
            "fangs (outlined in ink); complete the underside of the head behind the mouth, and its lower back over the neck (hidden in "
            "image 1), as a rounded black stone edge reaching down to about y 640; NO back crystals (the amber and turquoise sprouts LEFT of "
            "x 870 are NOT part of the head), NO body, NO arms, NO claws"),
           ("duoi", "the TAIL at the lower left: the short thick black tail that comes out from behind the near hand and goes to the lower "
            "left (visible from about x 240 to x 390, y 760-880), ending in ONE flat turquoise crystal blade at its tip (about x 180-300, "
            "y 785-860)",
            "complete its root, hidden behind the near hand and the body, as the same black tail continuing to the right up to about "
            "(560, 800) and ending there in a thick rounded end; NO claws, NO hand, NO arm")],
    "N2": [("ham", "the LOWER JAW: the black lower jaw under the open mouth (from its back end at about x 840 to its front tip at about "
            "x 1110; its lower edge at about y 700), with its THREE small rounded cream LOWER TEETH standing along its upper edge (at about "
            "(980-1015, 615-650), (1025-1060, 625-665) and (1065-1110, 640-690))",
            "WITHOUT the dark-red inside of the mouth (the upper edge of the jaw with its teeth is the top of this part), WITHOUT the far "
            "arm and its claws below it, WITHOUT the head and the upper fangs; complete its back end, hidden under the cheek, as a rounded "
            "hinge"),
           ("rung", "the CRYSTAL SPROUTS on the back: the THREE short crystal prisms growing out of the top of the back (an amber one at "
            "about x 545-640, y 240-345; the tall turquoise one at about x 645-765, y 175-315; an amber one at about x 780-860, y 230-335) "
            "and the TWO tiny turquoise nubs further left along the spine (at about x 500-550, y 330-370 and x 445-480, y 377-410)",
            "draw every crystal complete and exactly as in image 1; their lower ends, hidden behind the back in image 1, continue STRAIGHT "
            "DOWN as the same crystals for about 50 px more and end there (they will be hidden behind the body); NO body, NO head, NO amber "
            "nubs of the head crest (the ones right of x 885), NO flat base line, NO ground")],
}
TAM = {"dau": (1080, 400), "duoi": (330, 830), "ham": (980, 655), "rung": (660, 290)}
STYLE_M = ("Same wobbly dark-brown ink line (about 7 px), same colours, same crayon hatching, same completely flat colouring as image 1 "
           "(no shading, no highlights, no glow, no shadows).")


def _Q():
    """trỏ các hàm cắt dùng chung của quy_nui_manh sang thư mục dạng non."""
    import types
    import quy_nui_manh as Q
    Q.G = types.SimpleNamespace(TAI=TAI, MAU=MAU, BASE=BASE)
    Q.CONCEPT, Q.MANH, Q.GUI = DUYET, MANH, GUI
    return Q


def manh():
    hd = ["# Gói gen: Thiên Thạch Thú Non (`tinh_hach_non`), lượt 2: mảnh", "",
          f"Concept duyệt: `{tho5.Wp(DUYET)}` (hướng A \"mầm tinh thể\", người dùng chọn 2026-11-18). Thân, hai tay, móng, lòng miệng, "
          "quả cầu dùng lại mảnh dạng 2 (màu đo ra trùng). Hai tờ dưới gen lại chỗ khác hẳn, mỗi tờ hai mảnh không chồng nhau, đúng chỗ, "
          "đúng cỡ như concept (Magnific GPT 2.6, 1k high, 95 credit / tờ). Ba thiên thạch cắt thẳng từ concept.", "",
          "Ảnh mẫu duy nhất (ảnh 1) cho cả hai tờ: concept duyệt (1536 × 1024, nền trắng): thú thiên thạch non đá vỏ chai đen quay phải, "
          "đầu to tròn có diềm năm nụ hổ phách, mắt hổ phách tròn, ba mầm tinh thể trên lưng, đuôi một lưỡi ngọc lam, ba thiên thạch nhỏ bay.",
          "", "| Tờ | File prompt | Lưu vào |", "|---|---|---|"]
    for nh, ds in NHOM.items():
        out = os.path.join(TAI, f"M_{nh}.png")
        p = os.path.join(GUI, f"luot_2_{nh}.txt")
        t = ["IMAGES (attached in this order; open each from its path):", f"image 1 = {tho5.Wp(DUYET)}: {ANH1_A}", "",
             f"SAVE: save it as a PNG to {tho5.Wp(out)}",
             f"If a file with that name already exists, save as M_{nh}_2.png, M_{nh}_3.png ... in the same folder. Do not edit, move or "
             "delete any other file.", "",
             "TASK: redraw image 1 with ONLY the parts listed under KEEP, each in exactly the SAME POSITION and at exactly the SAME SIZE as in "
             "image 1 (if the new picture were laid over image 1, every kept part must coincide with image 1). REMOVE everything else (leave "
             "pure white there). COMPLETE each kept part into ONE CLOSED SHAPE with the dark-brown ink outline running all the way around it: "
             "where a part is hidden behind another part in image 1, draw the hidden portion as it would continue, in the same style, colours "
             "and flat crayon colouring. " + STYLE_M + " Do not move, resize, rotate or redesign anything. Keep a clear white gap between "
             "the kept parts.", "", "KEEP:"]
        t += [f"{i}. {mt}: {kh}." for i, (_, mt, kh) in enumerate(ds, 1)]
        t += ["", "CANVAS: landscape 1536x1024, plain pure-white background (#FFFFFF), no labels, no shadows, no sparkles, no glow."]
        tho5.ghi(p, t)
        vi = {"N1": "đầu (diềm năm nụ, mắt, hai nanh trên; bỏ hàm dưới, lòng miệng) + đuôi một lưỡi ngọc lam",
              "N2": "hàm dưới (ba răng sữa) + ba mầm tinh thể và hai nụ trên lưng"}[nh]
        hd.append(f"| {nh}: {vi} | `{tho5.Wp(p)}` | `{tho5.Wp(out)}` |")
        print(p)
    hd += ["", "Kiểm: mảnh trùng chỗ, cỡ với concept (đặt chồng thì khớp), viền mực kín, phần khuất vẽ tiếp; đầu không có hàm dưới, lòng "
           "miệng; mầm tinh thể kéo dài xuống thêm ~50 px; nền trắng tinh. Câu sửa nhanh: \"keep it at the same place and size as image 1\"; "
           "\"remove the lower jaw and the red inside of the mouth\"; \"flat colour only, no shading\"."]
    tho5.ghi(os.path.join(GUI, "HUONG_DAN_luot_2.md"), hd)


BONG2 = os.path.join(HERE, "inbox", "tinh_hach_1", "manh", "bong.png")
BONG_NEN = os.path.join(MAU, "bong2_nen.png")            # quả cầu dạng 2 (839x931) giữa nền trắng 1536x1024


def manh_bong():
    """quả cầu chiêu cuối (cuộn người) của dạng 2 mang mặt người lớn, rừng tinh thể dày, đuôi ba lưỡi → vẽ lại cho con non."""
    g = Image.open(BONG2).convert("RGBA")
    nen = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    nen.alpha_composite(g, ((W - g.width) // 2, (H - g.height) // 2))
    nen.convert("RGB").save(BONG_NEN)
    out = os.path.join(TAI, "M_bong.png")
    p = os.path.join(GUI, "luot_2_bong.txt")
    t = ["IMAGES (attached in this order; open each from its path):",
         f"image 1 = {tho5.Wp(BONG_NEN)}: the ADULT form of our hero CURLED UP INTO A SPIKY BALL, alone in the middle of a 1536x1024 white "
         "canvas: a round black obsidian rock body with two amber vein cracks, the adult head tucked in on the right (narrow amber eye, a "
         "row of fangs), the tail with three turquoise blades wrapped across the bottom, and MANY long turquoise and amber crystal spikes "
         "all around it",
         f"image 2 = {tho5.Wp(DUYET)}: {ANH1_A} This is the YOUNG form; its ball must look like it.", "",
         f"SAVE: save it as a PNG to {tho5.Wp(out)}",
         "If a file with that name already exists, save as M_bong_2.png, M_bong_3.png ... in the same folder. Do not edit, move or delete "
         "any other file.", "",
         "TASK: redraw image 1 as the YOUNG form's ball. Keep the same ROUND curled-up body (same round outline of the body itself, same "
         "size, same place in the middle of the canvas), still a fierce spiky meteor ball. Change ONLY:",
         "1. HEAD: the young head of image 2 tucked in on the right of the ball: its BIG round amber eye (dark pupil, ONE small white dot) "
         "under a frowning brow, a blunt snout, two small cream upper fangs, and its crest of FIVE small amber crystal nubs along the top "
         "of the head.",
         "2. SPIKES: replace the adult's many long crystal spikes by about TEN SHORT stubby crystal prisms sticking out evenly all around "
         "the ball (about half the length of image 1's, simple six-sided prisms with a pointed tip), turquoise #3FC1AE and amber #F2A93B "
         "alternating, plus image 2's tall turquoise back sprout on the top.",
         "3. TAIL: the short tail of image 2 wrapped across the bottom of the ball, ending in ONE flat turquoise crystal blade.",
         "4. BODY: the same black obsidian hide as image 2 (#3B3340, turned-away faces #2A2430) with only TWO thin amber vein cracks.",
         "", STYLE_M.replace("image 1", "image 2") + " No other changes, no new details, no glow, no motion lines.",
         "", "CANVAS: landscape 1536x1024, plain pure-white background (#FFFFFF), the ball where it is in image 1, no labels, no shadows, "
         "no sparkles."]
    tho5.ghi(p, t)
    hd = os.path.join(GUI, "HUONG_DAN_luot_2.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Quả cầu")[0].rstrip("\n")
    tho5.ghi(hd, (cu + "\n\n## Quả cầu chiêu cuối\n\n"
                  f"- File prompt `{tho5.Wp(p)}`; ảnh mẫu 1 = quả cầu dạng 2 (mặt người lớn, rừng tinh thể dày, đuôi ba lưỡi) giữa nền trắng "
                  f"`{tho5.Wp(BONG_NEN)}`; ảnh 2 = concept duyệt; lưu vào `{tho5.Wp(out)}`.\n- Kiểm: vẫn tròn đúng cỡ, chỗ; mặt con non (mắt "
                  "tròn to, diềm năm nụ), khoảng mười gai tinh thể ngắn, đuôi một lưỡi; tô phẳng.").split("\n"))
    print(p)


def cat():
    import numpy as np
    Q = _Q()
    DATJ = Q.nap_dat()
    src = Q.moi_nhat("M_bong")                            # quả cầu: khối lớn nhất của tờ
    if src:
        Am, lab, cum = Q._cum(src)
        lon = max(cum, key=lambda c: c[1])
        ids = [c[0] for c in cum if c[0] == lon[0] or np.hypot(c[2][0] - lon[2][0], c[2][1] - lon[2][1]) < 480]
        b = Q.luu_manh(Am, np.isin(lab, ids), "bong", DATJ, os.path.basename(src))
        print(f"  bong     hộp {b}, {len(ids)} cụm")
    for nh, ds in NHOM.items():
        src = Q.moi_nhat(f"M_{nh}")
        if not src:
            print(f"{nh}: chưa gen")
            continue
        Am, lab, cum = Q._cum(src)
        slots = [s for s, _, _ in ds]
        gan = {s: [] for s in slots}
        for i, a, c, _ in cum:
            best = min(slots, key=lambda s: np.hypot(c[0] - TAM[s][0], c[1] - TAM[s][1]))
            if np.hypot(c[0] - TAM[best][0], c[1] - TAM[best][1]) < 330 or a > 20000:
                gan[best].append(i)
            else:
                print(f"  bỏ cụm ở ({c[0]:.0f}, {c[1]:.0f}), {a} px")
        print(f"{nh} ({os.path.basename(src)}): {len(cum)} cụm")
        for s, ids in gan.items():
            if not ids:
                print(f"  {s:8s} KHÔNG THẤY MẢNH")
                continue
            b = Q.luu_manh(Am, np.isin(lab, ids), s, DATJ, os.path.basename(src))
            print(f"  {s:8s} hộp {b}, {len(ids)} cụm")
    # ba thiên thạch: cụm rời (không dính thân) trên concept, xếp trái → phải
    Am, lab, cum = Q._cum(DUYET)
    lon = max(cum, key=lambda c: c[1])
    tt = sorted([c for c in cum if c[0] != lon[0] and 3000 < c[1] < 40000], key=lambda c: c[2][0])
    for j, c in enumerate(tt, 1):
        b = Q.luu_manh(Am, lab == c[0], f"cum{j}", DATJ, "L1_duyet.png (cắt thẳng)")
        print(f"  cum{j}     hộp {b}, {c[1]} px")
    Q.ghi_dat(DATJ)


CO1, CO2 = 0.92, 1.10                                     # forms[].size trong heroes.json (dạng 1, dạng 2)


def th():
    """gộp dạng 2 (bản nhẹ, file đang chạy trong game) vào rig dạng non + clip evolve (như doi_tho5_dang2.th) → rig/tinh_hach_non_th.atomik,
    rig/khung_evolve.png. Slot ẩn sẵn của hai rig (bản sao thiên thạch, quả cầu, vệt bay) giữ ẩn suốt clip."""
    import numpy as np
    rig = os.path.join(BASE, "rig")
    J, img, ver = A.load(os.path.join(rig, "tinh_hach_non.atomik"))
    JB, imgB, _ = A.load(SRC)
    an_A = {i for i, s in enumerate(J["slots"]) if s.get("fade", 0) >= 1}
    an_B = {i for i, s in enumerate(JB["slots"]) if s.get("fade", 0) >= 1}
    nA_s = len(J["slots"])
    hA, hB = J["game"]["height"], JB["game"]["height"]
    k_B = CO2 / CO1 * hA / hB
    img = A.gop_tien_hoa(J, img, JB, imgB, k_B, than_A=A.bi(J)["all"])
    ev = J["anims"][-1]
    n = 0
    for x in ev["sa"]:
        if x["slot"] in an_A or (x["slot"] - nA_s) in an_B:
            x["keys"] = A.rot_keys([(0, 0), (ev["dur"], 0)])
            n += 1
    p = os.path.join(rig, "tinh_hach_non_th.atomik")
    kq = A.save(p, J, img, ver)
    print(f"{p}: {os.path.getsize(p) // 1024} KB; dạng 2 × {k_B:.3f} (cao {hA:.0f} / {hB:.0f}); {n} slot ẩn giữ ẩn; {kq}")
    ci = A.clip(J, "evolve")
    ts = [0.0, 0.5, 0.9, 1.05, 1.2, 1.35, 1.5, 1.8, 2.2, 2.6, 3.0]
    Ps = [A.Pose(J).at(ci, t) for t in ts]
    bs = np.array([A.bounds(P) for P in Ps])
    box = (bs[:, 0].min() - 20, bs[:, 1].min() - 20, bs[:, 2].max() + 20, bs[:, 3].max() + 20)
    sc = 300.0 / max(1.0, box[3] - box[1])
    ims = [A.render(J, img, P, box, sc, bg=(150, 150, 150)).convert("RGB") for P in Ps]
    for t, im in zip(ts, ims):
        ImageDraw.Draw(im).text((6, 4), f"evolve {t:.2f}", fill=(255, 255, 255))
    cot = 6
    out = Image.new("RGB", (cot * ims[0].width, ((len(ims) + cot - 1) // cot) * ims[0].height), (150, 150, 150))
    for i, im in enumerate(ims):
        out.paste(im, ((i % cot) * im.width, (i // cot) * im.height))
    q = os.path.join(rig, "khung_evolve.png")
    out.save(q)
    print(q, out.size)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "bocuc":
        bocuc()
    elif cmd == "concept":
        concept()
    elif cmd == "can":
        can()
    elif cmd == "manh":
        manh()
    elif cmd == "manh_bong":
        manh_bong()
    elif cmd == "th":
        th()
    elif cmd == "cat":
        cat()
    else:
        print(__doc__)
