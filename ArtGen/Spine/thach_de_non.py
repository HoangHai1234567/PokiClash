# -*- coding: utf-8 -*-
"""Tiểu Thổ Tinh (mã làm việc thach_de_non): DẠNG 1 của tướng 10 đảo Thổ (ải 70, final boss, id `giap_nham`; dạng 2 = Thổ Tinh
`thach_de`, rig monster_3802, ghi chú inbox/thach_de_ghichu.md). Người dùng 2026-11-18: "ok cho vào game đi rồi gen dạng 1 của nó".
Làm như Thiên Thạch Thú Non (tinh_hach_non.py): CÙNG rig, đổi tỉ lệ thành con non ngay trên rig dạng 2, dựng bố cục, concept vẽ trên bố
cục đó (Claude đề xuất hai hướng), người dùng duyệt, rồi mới làm mảnh + rig. Rig, lưới, chuyển động gốc là của nhà phát hành game tham
khảo: chỉ dùng nội bộ, không đăng công khai.

    thach_de_non.py bocuc      mau/so_ti_le.jpg (gốc, A, B, C), mau/ti_le.json, mau/bo_cuc.png (1536x1024), mau/bo_cuc_khung.json
    thach_de_non.py concept    gui_gpt/thach_de_non/luot_1_concept_<k>.txt + HUONG_DAN.md
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

CODE = "thach_de_non"
SRC = os.path.join(HERE, "inbox", "thach_de_1", "rig", "thach_de_1.atomik")
BASE = os.path.join(HERE, "inbox", CODE)
MAU = os.path.join(BASE, "mau")
TAI = os.path.join(BASE, "tai_ve")
GUI = os.path.join(HERE, "gui_gpt", CODE)
DUYET2 = os.path.join(HERE, "inbox", "thach_de_1", "tai_ve", "L1_duyet.png")
W, H = 1536, 1024

# ---------------------------------------------------------------- tỉ lệ (thử trên dáng idle khung 0)
# bone5 lõi (kéo theo hành tinh, đầu, hai tay, vỏ vai, gai lưng); bone6 cổ → đầu (+ hàm, nanh); gai_i lưỡi trăng lưng (đế ở vành);
# dao_j vệ tinh; bone10 / bone18 khối tay (cẳng + nắm đấm); `bone` hông → hai chân. Hạ cả con (xy dy) cho chân chạm đất như dạng 2.
GAI = {f"gai_{i}": 0.6 for i in range(10)}
TI_LE_THU = {
    "A": {"bone5": 0.80, "bone6": 1.55, **GAI, **{f"dao_{j}": 0.75 for j in range(6)}, "bone": 0.88},
    "B": {"bone5": 0.74, "bone6": 1.72, **{k: 0.52 for k in GAI}, **{f"dao_{j}": 0.7 for j in range(6)}, "bone10": 1.06, "bone18": 1.06,
          "bone": 0.84},
    "C": {"bone5": 0.70, "bone6": 1.85, **{k: 0.5 for k in GAI}, **{f"dao_{j}": 0.7 for j in range(6)}, "bone10": 1.1, "bone18": 1.1,
          "bone": 0.8},
}
CHON = "B"
# con non: SÁU lưỡi trăng (ẩn 4 lưỡi xen kẽ), BA vệ tinh
AN_SLOT = ("P_R_beiji09", "P_R_beiji07", "P_R_beiji04", "P_R_beiji02", "ve_3_", "ve_4_", "ve_5_", "ve_0_b", "ve_1_b", "ve_2_b",
           "ho_", "dat_cat")    # hố, vệ tinh nửa sau: chỗ của clip aura (bố cục chụp không có aura)
PAD = 1.18


def nap():
    J, img, _ = A.load(SRC)
    return J, img


def ap_ti_le(J0, ti):
    """nhân tỉ lệ + dời xy cho điểm thấp nhất (idle khung 0) trùng dạng 2."""
    y_goc = A.bounds(A.Pose(J0).at(A.clip(J0, "idle"), 0.0))[1]
    J = copy.deepcopy(J0)
    A.scale_bones(J, ti)
    y0 = A.bounds(A.Pose(J).at(A.clip(J, "idle"), 0.0))[1]
    ti2 = dict(ti)
    ti2["xy"] = {"s": 1.0, "dy": round(y_goc - y0, 1)}
    J = copy.deepcopy(J0)
    A.scale_bones(J, ti2)
    return J, ti2


def chon_slot(J, P):
    return {s for s, _, _, _ in P.items() if not J["slots"][s]["name"].startswith(AN_SLOT)}


def bocuc():
    os.makedirs(MAU, exist_ok=True)
    J0, img = nap()
    BOX, SC = (-700, -200, 700, 1100), 0.3
    tiles = []
    for k in ["goc"] + list(TI_LE_THU):
        J = J0 if k == "goc" else ap_ti_le(J0, TI_LE_THU[k])[0]
        P = A.Pose(J).at(A.clip(J, "idle"), 0.0)
        only = None if k == "goc" else chon_slot(J, P)
        im = A.render(J, img, P, BOX, SC, bg=(255, 255, 255), only=only).convert("RGB")
        ImageDraw.Draw(im).text((10, 10), k + (" (chọn)" if k == CHON else ""), fill=(200, 0, 0))
        tiles.append(im)
    S = Image.new("RGB", (sum(t.width for t in tiles), tiles[0].height), "white")
    for i, t in enumerate(tiles):
        S.paste(t, (i * t.width, 0))
    S.save(os.path.join(MAU, "so_ti_le.jpg"), quality=88)
    J, ti = ap_ti_le(J0, TI_LE_THU[CHON])
    json.dump(ti, open(os.path.join(MAU, "ti_le.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    P = A.Pose(J).at(A.clip(J, "idle"), 0.0)
    only = chon_slot(J, P)
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
        nm = J["slots"][s]["name"].split("@")[0]
        b = [int(q[:, 0].min()), int(q[:, 1].min()), int(q[:, 0].max()), int(q[:, 1].max())]
        if nm in hop["slot"]:
            o = hop["slot"][nm]
            b = [min(o[0], b[0]), min(o[1], b[1]), max(o[2], b[2]), max(o[3], b[3])]
        hop["slot"][nm] = b
    json.dump(hop, open(os.path.join(MAU, "bo_cuc_khung.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("ti_le", CHON, "dy", ti["xy"]["dy"], "| khung rig", hop["khung_rig"], "|", hop["px_moi_don_vi"], "px / đơn vị")
    for k in ("P_shenti01", "P_tou1", "P_R_xiaobi06", "P_L_xiaobi05", "P_R_shitou09", "P_L_shitou07", "P_kua03"):
        if k in hop["slot"]:
            print(f"  {k:14s} {hop['slot'][k]}")


# ---------------------------------------------------------------- concept lượt 1: hai hướng
R1 = (os.path.join(MAU, "bo_cuc.png"),
      "the PROPORTION GUIDE, 1536x1024, white background: our adult hero re-proportioned as its YOUNG form on the same skeleton (a much "
      "bigger head, a smaller planet body, smaller fists and shoulder shells, short back blades: only six of them, three small moons), "
      "still wearing the adult's skin. Keep its pose, its facing, its size and place on the canvas and where every part is; redraw the "
      "surface as the young form described below",
      "Bố cục dạng non: rig Thổ Tinh đổi tỉ lệ (thân trên 0,74, đầu net ~1,27, nắm đấm nhỏ, sáu lưỡi trăng ngắn, ba vệ tinh), còn mang da "
      "dạng 2, nền trắng 1536×1024, con nhìn sang phải. Giữ dáng, chỗ, cỡ từng bộ phận")
R2 = (DUYET2,
      "the APPROVED ADULT form of the same hero, 1536x1024, white background: the young form must clearly be the SAME creature at a "
      "younger age: a banded stone planet body, moon-rock fists with knuckle stones, crescent shells and blades of grey-lilac moon rock "
      "with round craters, a horned beast mask with amber eyes and cream tusks, small moons orbiting; the same pen line, crayon hatching "
      "and flat colouring. Do NOT copy its adult proportions (image 1 gives the proportions)",
      "Concept dạng 2 (Thổ Tinh, B2Y) đã duyệt: lõi hành tinh đá kẻ dải, nắm đấm mặt trăng, vỏ vai và lưỡi trăng đá trăng có hố, mặt nạ thú "
      "sừng trăng mắt hổ phách nanh kem, vệ tinh bay quanh. Lấy chất liệu, màu, nét bút, vân sáp; không lấy tỉ lệ người lớn")


def plan(h):
    s = h["slot"]
    f = lambda k: f"x {s[k][0]}-{s[k][2]}, y {s[k][1]}-{s[k][3]}"  # noqa: E731
    xs = [v[0] for v in s.values()] + [v[2] for v in s.values()]
    ys = [v[1] for v in s.values()] + [v[3] for v in s.values()]
    lung = [v for k, v in s.items() if k.startswith("P_R_beiji")]
    lx0, ly0 = min(v[0] for v in lung), min(v[1] for v in lung)
    lx1, ly1 = max(v[2] for v in lung), max(v[3] for v in lung)
    return (
        "BODY PLAN (from image 1, positions on the 1536x1024 canvas; keep it exactly, it is animated with the same skeleton): a young "
        f"stone-planet creature floating its fists low, FACING RIGHT (three-quarter view), filling about x {min(xs)}-{max(xs)}, "
        f"y {min(ys)}-{max(ys)}. "
        f"(1) PLANET BODY: one round ball in the middle ({f('P_shenti01')}). "
        f"(2) HEAD: BIG for the body, on the front-right of the planet ({f('P_tou1')}), facing right. "
        f"(3) BIG FIST on the LEFT, low, in front ({f('P_R_xiaobi06')}) with its knuckle stones under it; its crescent forearm chunk and the "
        f"big crescent SHOULDER SHELL above it on the upper left ({f('P_R_shitou09')}). "
        f"(4) SMALL FIST on the RIGHT, low ({f('P_L_xiaobi05')}), with its shoulder shell above it ({f('P_L_shitou07')}). "
        f"(5) SHORT LEGS under the planet ({f('P_kua03')} is the hip). "
        f"(6) BACK: SIX short blades standing on the top rim of the planet, inside x {lx0}-{lx1}, y {ly0}-{ly1}. "
        "(7) THREE small moons floating close around the planet. "
        "Same size and same place on the canvas as image 1; every part keeps about the same size and outline as in image 1; the "
        "floating rock pieces (fists, shells, blades) float close to the planet like in image 1.")


CHUNG = [
    "HEAD: the horned beast mask of image 2 made YOUNGER: rounder and bigger for the body, the two crescent horns SHORT and stubby (they "
    "still meet into a small upward crescent moon), BIG round amber eyes #F6C443 (a round dark pupil, ONE small white dot each) under a "
    "heavy FROWNING brow: a determined, ready-to-fight little face (fierce-cute, not sad, not silly); a small snarling mouth with two "
    "SMALL cream tusks #F4EAD2 (milk tusks, much smaller than image 2).",
    "FISTS: two moon-rock fists like image 2 but rounder and smaller: grey-lilac #CFC8D6 (side faces #9D95AB) with two or three round "
    "craters #B3ABC0, THREE chunky knuckle stones under each.",
    "SHOULDER SHELLS: smaller, rounder crescent shells of the same moon rock, only a few craters.",
    "MOONS: THREE small round moons of the same moon rock (one or two craters each), 50-90 px, floating close around the planet.",
    "NO moss, no plants, no cracks that glow, no carvings, no runes, no extra spots or pebbles, no glow.",
]

HUONG = {
    "A": ("hành tinh non",
          "lõi hành tinh nhỏ, chỉ bốn dải rộng (kem, vàng đất, đỏ gạch) và MỘT hố tròn lớn; sáu lưỡi trăng ngắn mập như nụ; đầu to, sừng "
          "trăng ngắn, mắt to cau mày, nanh sữa",
          ["PLANET BODY: a smaller young stone planet with only FOUR wide flat horizontal bands with gently wavy edges (cream #EAD7AE, "
           "ochre #D9A441, terracotta #B5532F, cream again) and ONE big round shallow crater #8A5636 on it (the adult has seven bands).",
           "BACK: SIX short stubby crescent BUDS of moon rock standing on the top rim of the planet (each about half the height of the "
           "adult's blades, tips curving to the right, one small crater each): baby blades."]),
    "B": ("trăng non nứt vỏ",
          "lõi hành tinh còn bọc trong VỎ ĐÁ TRĂNG nứt như vỏ trứng (nửa trên vỏ xám tím có hố, khe nứt răng cưa ngang lộ dải hành tinh "
          "bên trong); trên lưng là sáu mảnh vỏ vỡ dựng đứng thay cho lưỡi trăng; lớn lên vỏ vỡ hết thành hành tinh có lưỡi trăng",
          ["PLANET BODY: the young planet is still wrapped in a cracked SHELL of grey-lilac moon rock #CFC8D6 (side faces #9D95AB) with a "
           "few round craters #B3ABC0, like a cracking egg: the shell covers the top half and the sides, split by ONE jagged zig-zag crack "
           "running across the middle through which the banded planet inside shows (bands cream #EAD7AE, ochre #D9A441, terracotta "
           "#B5532F); the lower part of the planet is already bare and banded.",
           "BACK: instead of crescent blades, SIX broken SHELL SHARDS standing up along the top rim (jagged edges, curving slightly to "
           "the right, the same moon rock): the adult's crescent blades will grow from them."]),
}

DETAIL = ("DETAIL: about as much detail as image 2 or less: big simple masses, each a flat colour, at most one or two inner lines per "
          "piece; only the details listed under DESIGN.")
MOOD = ("MOOD: the YOUNG form (first evolution stage) of a fierce stone-planet titan that grows into image 2: chunky, a big head, small "
        "fists, a determined frown, ready to fight; likeable, NOT a mascot, not babyish-silly, not horror.")
STYLE = ("DRAWING STYLE (very important): hand-drawn on paper exactly like image 2: a wobbly dark-brown INK outline (#2B2118, about "
         "7 px) running all the way round every piece on its silhouette, thinner ink lines (about 4 px) for the few inner lines, and "
         "every area filled with ONE flat colour with visible coloured-pencil / wax-crayon hatching (the hatching is only texture, it "
         "never makes light or dark areas). FLAT COLOUR ONLY: no shading, no light and dark planes, no highlights, no white shine "
         "streaks, no gloss, no gradients, no glow, no rim light; only one small white dot in each eye. NO SHADOWS: no drop shadow, no "
         "cast shadow, no shadow under the body or on the ground. No white sticker border round the character.")


def task():
    return ("TASK: redraw image 1 as the YOUNG FORM (first evolution stage) of the hero in image 2. Keep image 1's pose, facing, size, "
            "place on the canvas and the outline of every part (it is animated with the same skeleton); give it the surface, materials "
            "and colours of image 2 made younger, as described below.")


def concept():
    h = json.load(open(os.path.join(MAU, "bo_cuc_khung.json"), encoding="utf-8"))
    R = [R1, R2]
    hd = ["# Gói gen: Tiểu Thổ Tinh (`thach_de_non`), dạng 1 tướng 10 đảo Thổ (ải 70, id `giap_nham`)", "",
          "Rig: `monster_3802` (game tham khảo) đổi tỉ lệ. Ảnh mẫu 1 mang lưới / da dựng từ rig đó: chỉ dùng trong máy, không đăng công khai.",
          "", "## Lượt 1: concept dạng 1, hai hướng (2026-11-18)", "",
          "Người dùng: \"ok cho vào game đi rồi gen dạng 1 của nó\". Dựng trên cùng rig (như Thiên Thạch Thú Non), Claude đề xuất hai hướng. "
          "Ảnh 1 là bố cục dạng non (tỉ lệ đã đổi trên rig, còn mang da dạng 2); ảnh 2 là concept dạng 2 đã duyệt để giữ nhận diện.", "",
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
        os.makedirs(GUI, exist_ok=True)
        tho5.ghi(p, t)
        hd += [f"- **Hướng {k}** ({vi}: {vi2}): file prompt `{tho5.Wp(p)}`; ảnh lưu vào `{tho5.Wp(out)}` (trùng tên thì `_2`, `_3`…)."]
        print(p)
    hd += ["", "Claude tự gen: `py -3 -I ArtGen/Spine/gen.py <file prompt>` (Codex). Bản được chọn chép thành `L1_duyet.png` cùng thư mục.", "",
           "Kiểm: đúng dáng, chỗ, cỡ từng bộ phận như ảnh 1 (hành tinh giữa, đầu to phía trước bên phải, nắm đấm to thấp bên trái, nắm "
           "đấm nhỏ bên phải, vỏ vai trên mỗi nắm đấm, sáu lưỡi / mảnh trên lưng, ba vệ tinh); rõ là cùng loài với ảnh 2; mắt to, mặt quả "
           "quyết; nét bút mực rung, vân sáp, tô phẳng, không bóng, không quầng sáng, chỉ một chấm sáng trong mỗi mắt; nền trắng tinh; "
           "không viền sticker.",
           "", "Câu sửa nhanh: \"too many details: simplify\"; \"remove the shading / highlights / glow, flat colour only\"; \"keep every part "
           "at the same place and size as image 1\"; \"make the head rounder and the eyes bigger, keep the determined frown\"."]
    tho5.ghi(os.path.join(GUI, "HUONG_DAN.md"), hd)


# ================================================================ mảnh (người dùng chọn B 2026-11-18: "làm B" → tai_ve/L1_duyet.png)
# Concept B cùng bảng màu dạng 2 → nắm đấm, cẳng tay, vỏ vai, chân, hông, vệ tinh, bàn tay xoè DÙNG LẠI mảnh dạng 2 (rig co theo ti_le.json).
# Gen lại chỗ khác hẳn: đầu non (tách hàm như dạng 2), lõi hành tinh bọc vỏ nứt, sáu mảnh vỏ vỡ trên lưng. Mảnh mới vẽ CÙNG CỠ mảnh dạng 2
# tương ứng (ảnh mẫu) để đặt đúng chỗ mảnh cũ trong hệ xương dạng 2, rồi co / phóng theo xương như mảnh dùng lại.
DUYET = os.path.join(TAI, "L1_duyet.png")
MANH2 = os.path.join(HERE, "inbox", "thach_de_1", "manh")
MANH = os.path.join(BASE, "manh")
DAU_M = ("IMAGES (attached in this order; open each from its path):\n"
         "image 1 = {duyet}: our approved character concept, the YOUNG form (1536x1024, white background): a young stone-planet "
         "creature: a banded planet body still wrapped in a cracked moon-rock shell like a cracking egg, six broken shell shards standing "
         "on its back, a big horned head with big amber eyes and small milk tusks, moon-rock fists, crescent shoulder shells, three small "
         "moons. Match EXACTLY its design and drawing style: wobbly dark-brown ink outline (#2B2118, about 7 px), flat colours with "
         "visible coloured-pencil / wax-crayon hatching, one darker tone on side faces, no shading, no highlights, no gradients, no "
         "glow, no shadows.")
CHUNG_M = ("TASK: draw a PARTS SHEET for animating the character of image 1: the pieces listed below, as SEPARATE objects on a pure-white "
           "background. Rules: every piece is COMPLETE (the whole object, including what is hidden behind other things in image 1), has "
           "a closed ink outline all the way round, and uses the same line weight, colours and hatching as image 1. Pieces must NOT touch "
           "or overlap: leave at least 40 px of white between any two pieces. Draw ONLY the listed pieces, each exactly once, at the "
           "place given (x, y in pixels on the 1536x1024 sheet, x from the left, y from the top). No text, no labels, no numbers, no "
           "arrows, no frame, no ground line, no cast shadows, no sparkles.")
PAL_M = ("PALETTE (flat): planet bands cream #EAD7AE / ochre #D9A441 / terracotta #B5532F; moon rock #CFC8D6, its side faces #9D95AB, "
         "its craters #B3ABC0; horn tips #9A5A44; tusks #F4EAD2; eyes amber #F6C443; inside of the mouth maroon #4A2228, tongue "
         "#A8505A; ink #2B2118.")
TO_N = {
    "N1": dict(
        vi="đầu non trọn (ngậm), đầu non bỏ hàm (hàng nanh trên), hàm dưới kèm lòng miệng, hai nanh sữa rời",
        refs=[(os.path.join(MANH2, "dau.png"), "the ADULT head piece of the same hero (407x455 px, transparent background), shown at its "
               "real size: draw the young head pieces at THIS SIZE (about 407 px wide) and in the same three-quarter view facing right")],
        ds=["YOUNG HEAD, centre about (240, 270): the head of image 1 COMPLETE with its closed snarling mouth and two small milk tusks, "
            "exactly its design (short stubby crescent horns meeting into a small upward crescent, big round amber eyes under a heavy "
            "frowning brow), three-quarter view facing right, about 407 px wide (the size of image 2). Nothing else attached to it.",
            "YOUNG UPPER HEAD, centre about (740, 270): the same young head WITHOUT its lower jaw and WITHOUT the two milk tusks: horns, "
            "brow, eyes, nose, cheeks (everything ABOVE the mouth line) at exactly the same size and shape as the YOUNG HEAD piece. Its "
            "bottom edge is the upper lip with a row of short pointed cream upper fangs. Closed ink outline all round, also under the fangs.",
            "YOUNG LOWER JAW, centre about (1230, 260), about 230 px wide and 230 px tall: the lower jaw of the young head for an OPENING "
            "MOUTH: at the bottom the small chin and lower lip in moon rock; along its top a row of small blunt cream lower teeth; ABOVE "
            "the teeth the INSIDE of the mouth: one dark maroon area with a rounded red-brown tongue, rising about 120 px above the teeth "
            "with a smooth dome top. NO tusks on this piece.",
            "TWO MILK TUSKS, centres about (520, 800) and (660, 800): the two small curved cream tusks of the young head, each drawn ALONE "
            "as its own closed shape: about 55 x 85 px and 45 x 72 px; wide base at the bottom, tip at the top curving outward."]),
    "N2": dict(
        vi="lõi hành tinh bọc vỏ nứt (đĩa trọn, không gì che), sáu mảnh vỏ vỡ dựng đứng",
        refs=[(os.path.join(MANH2, "hanh_tinh.png"), "the ADULT planet body piece of the same hero (630x653 px, transparent background), "
               "shown at its real size: draw the young planet body as a disc of THIS SIZE (about 630 px across)"),
              (os.path.join(MANH2, "luoi_1.png"), "one ADULT back blade of the same hero (228x389 px): the young shell shards stand on the "
               "planet rim in the same way (wide base at the bottom, tip at the top), but are BROKEN SHELL pieces, not blades")],
        ds=["YOUNG PLANET BODY, centre about (360, 512): ONE perfect circle about 630 px across (the size of image 2): the body of image 1 "
            "COMPLETE with nothing in front of it (no head, no fists, no shells, no moons, no shards): the top part covered by the cracked "
            "grey-lilac moon-rock SHELL with five or six flat round craters; ONE jagged zig-zag crack edge crosses the whole disc from "
            "left to right a little above the middle, like an eggshell broken open; BELOW it the banded stone planet: four flat wavy "
            "horizontal bands (cream, ochre, terracotta, terracotta) running from edge to edge. No shards on it.",
            "SIX SHELL SHARDS in a 3 x 2 block inside x 780-1500 (row 1 y 80-470, row 2 y 560-960): six separate broken pieces of the "
            "same cracked moon-rock shell, each STANDING UPRIGHT: a wide flat base at the bottom, a jagged broken tip at the top leaning "
            "a little to the RIGHT, one or two small craters, the darker side face along one edge. Heights about 330, 300, 270, 240, 210 "
            "and 185 px (row 1: the three tallest), widths about half the height, each a slightly different jagged outline."]),
}
TEN_N = {"N1": ["non_dau", "non_dau_tren", "non_ham", "non_nanh_1", "non_nanh_2"],
         "N2": ["non_hanh_tinh", "non_vo_1", "non_vo_2", "non_vo_3", "non_vo_4", "non_vo_5", "non_vo_6"]}
HANG_N = {"N1": [540], "N2": None}


def manh():
    hd = open(os.path.join(GUI, "HUONG_DAN.md"), encoding="utf-8").read().rstrip("\n").split("\n")
    td = "## Lượt 2: hai tờ mảnh dạng 1 (2026-11-18)"
    if td in hd:
        hd = hd[:hd.index(td) - 1]
    hd += ["", td, "", "Người dùng chọn B (\"làm B\") → `L1_duyet.png`. Nắm đấm, vỏ vai, chân, vệ tinh, bàn tay xoè dùng lại mảnh dạng 2; "
           "gen lại đầu non (tách hàm), lõi bọc vỏ, sáu mảnh vỏ, vẽ cùng cỡ mảnh dạng 2 tương ứng.", ""]
    for k, t in TO_N.items():
        out = os.path.join(TAI, f"M_{k}.png")
        p = os.path.join(GUI, f"luot_2_manh_{k}.txt")
        lines = DAU_M.format(duyet=tho5.Wp(DUYET)).split("\n")
        lines += [f"image {i} = {tho5.Wp(r)}: {e}" for i, (r, e) in enumerate(t["refs"], 2)]
        lines += ["", f"SAVE: save it as a PNG to {tho5.Wp(out)}",
                  f"If a file with that name already exists, save as M_{k}_2.png, M_{k}_3.png ... in the same folder. Do not edit, move or "
                  "delete any other file.", "", CHUNG_M, "", "PIECES:"] + [f"- {d}" for d in t["ds"]] + ["", PAL_M, "",
                  "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF)."]
        tho5.ghi(p, lines)
        hd += [f"- **Tờ {k}**: {t['vi']}. File prompt `{tho5.Wp(p)}`; ảnh lưu `{tho5.Wp(out)}`. Ảnh mẫu: 1 = concept B, "
               + ", ".join(f"{i} = `{tho5.Wp(r)}`" for i, (r, _) in enumerate(t["refs"], 2)) + f". Kiểm: đủ {len(TEN_N[k])} mảnh rời, viền kín."]
        print(p)
    tho5.ghi(os.path.join(GUI, "HUONG_DAN.md"), hd)


def cat(ks):
    from quai import anh
    os.makedirs(MANH, exist_ok=True)
    for k in ks:
        c = sorted((f for f in os.listdir(TAI) if f == f"M_{k}.png" or (f.startswith(f"M_{k}_") and f.endswith(".png"))),
                   key=lambda f: os.path.getmtime(os.path.join(TAI, f)))
        p = os.path.join(TAI, c[-1])
        to = anh.doc_to(p, dien_tich_min=500, gop_px=14)
        ms = to.manh
        if k == "N2":
            lon = max(ms, key=lambda m: m["dt"])
            nho = sorted([m for m in ms if m is not lon], key=lambda m: -m["dt"])
            thu = [lon] + nho
        else:
            thu = sorted(ms, key=lambda m: (sum((m["y0"] + m["y1"]) / 2 > r for r in HANG_N[k]), m["x0"]))
        print(f"tờ {k} ({os.path.basename(p)}): {len(ms)} mảnh, cần {len(TEN_N[k])}")
        for m in thu:
            print("   ", m["x0"], m["y0"], m["x1"] - m["x0"], m["y1"] - m["y0"], m["dt"])
        if len(ms) != len(TEN_N[k]):
            raise SystemExit(f"tờ {k}: sai số mảnh, xem lại ảnh")
        anh.luu_manh(to, dict(zip(TEN_N[k], thu)), MANH)
    anh.to_soi(MANH, sorted(f[:-4] for f in os.listdir(MANH) if f.endswith(".png") and not f.startswith("_")))


CO1, CO2 = 0.92, 1.1


def th():
    """gộp dạng 2 (bản nhẹ, rig đang chạy trong game) vào rig dạng non + clip evolve (như tinh_hach_non.th) → rig/thach_de_non_th.atomik,
    rig/khung_evolve.png. Slot ẩn sẵn của hai rig giữ ẩn suốt clip."""
    import numpy as np
    rig = os.path.join(BASE, "rig")
    J, img, ver = A.load(os.path.join(rig, "thach_de_non.atomik"))
    JB, imgB, _ = A.load(SRC)
    an_A = {i for i, s in enumerate(J["slots"]) if s.get("fade", 0) >= 1}
    # dạng 2 trong rig gộp không chạy aura: hố hành tinh (đứng chồng giữa lõi) và vệ tinh nửa sau (trùng nửa trước) giữ ẩn
    an_B = {i for i, s in enumerate(JB["slots"]) if s.get("fade", 0) >= 1 or s["name"].startswith("ho_")
            or (s["name"].startswith("ve_") and s["name"].endswith("_b"))}
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
    p = os.path.join(rig, "thach_de_non_th.atomik")
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
    a = sys.argv[1:]
    if not a:
        print(__doc__)
    elif a[0] == "th":
        th()
    elif a[0] == "bocuc":
        bocuc()
    elif a[0] == "concept":
        concept()
    elif a[0] == "manh":
        manh()
    elif a[0] == "cat":
        cat(a[1:] or list(TO_N))
