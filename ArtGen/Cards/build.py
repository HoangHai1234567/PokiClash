# -*- coding: utf-8 -*-
"""Gói gửi GPT vẽ TRANH THẺ CHUNG (GD_Claude/36_TranhThe.md): mỗi lượt một tấm 1536 x 1024, lưới 3 x 3 ô tranh 16:10 (464 x 290),
mỗi ô là tranh của một thẻ chung theo thứ tự khối pool trong cards.json. Cảnh từng thẻ ở canh_the_chung.json.

    py -3 -I ArtGen/Cards/build.py

Sinh vào ArtGen/Cards/gui_gpt/: bo_cuc_<k>.png (lưới đánh số), luot_01.txt..., HUONG_DAN.md. GPT lưu ảnh vào ArtGen/Cards/tai_ve/.
Lượt 1 chốt nét. Lượt 2 trở đi lấy tấm lượt 1 đã duyệt làm ảnh mẫu nên chỉ dựng khi DUYET trỏ tới ảnh có thật.
Đường dẫn tính từ chỗ đặt script (hai máy khác ổ đĩa).
"""
import json
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.normpath(os.path.join(HERE, ".."))
OUT = os.path.join(HERE, "gui_gpt")
SAVE_DIR = os.path.join(HERE, "tai_ve")

REF_WORLD = os.path.join(ART, "Islands", "refs", "world_style.png")
REF_FLAT = os.path.join(ART, "Spine", "inbox", "dat_nung_1", "tai_ve", "L3_1.png")
# tấm lượt 1 đã duyệt (làm ảnh mẫu nét cho các lượt sau); đổi tên file ở đây khi duyệt bản _2, _3...
# luot_01.png (bản đầu, nhiều chân thú) bị người dùng chê 2026-11-27: "giảm bớt hình động vật, nhìn là hiểu chức năng" → gen lại thành _2
DUYET = os.path.join(SAVE_DIR, "luot_01_2.png")

W, H = 1536, 1024
PW, PH = 464, 290  # ô tranh 16:10; trên thẻ hiện khoảng 280 x 175
PER = 9

NO_SHADOWS = ("NO SHADOWS: no drop shadow, no hard offset shadow, no cast shadow, no shadow under the feet or on the ground or background.\n"
              "Shade only with colour-pencil hatching inside the shapes; the game adds shadows itself where needed.")


def o_tranh(k):
    """k ô (k <= 9) trong khung W x H: 3 cột, số hàng vừa đủ, căn giữa theo chiều dọc. Trả list (x0, y0, x1, y1)."""
    rows = math.ceil(k / 3)
    ch = H / 3
    top = (H - rows * ch) / 2
    boxes = []
    for i in range(k):
        r, c = divmod(i, 3)
        x0 = round(c * (W / 3) + (W / 3 - PW) / 2)
        y0 = round(top + r * ch + (ch - PH) / 2)
        boxes.append((x0, y0, x0 + PW, y0 + PH))
    return boxes


def ve_bo_cuc(k, path):
    im = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(im)
    try:
        font = ImageFont.truetype("arial.ttf", 120)
    except OSError:
        font = ImageFont.load_default()
    for i, (x0, y0, x1, y1) in enumerate(o_tranh(k), 1):
        d.rectangle((x0, y0, x1, y1), fill=(236, 236, 236), outline=(150, 150, 150), width=4)
        d.text(((x0 + x1) / 2, (y0 + y1) / 2), str(i), fill=(175, 175, 175), font=font, anchor="mm")
    im.save(path)


def anh_mau(k, voi_duyet):
    bo = os.path.join(OUT, f"bo_cuc_{k}.png")
    ds = [
        (REF_WORLD, "1024 x 1536", "the game's approved hand-drawn map: copy its RENDERING only (wobbly dark-brown ink outlines, coloured-pencil "
                                   "hatching on cream paper, chunky cute doodles of objects such as the flames, rocks, bell and shells); ignore its content and layout"),
        (REF_FLAT, "1536 x 1024", "an approved creature of the same game: copy how its shapes are FILLED (each area one flat colour with a soft "
                                  "crayon grain, no light and dark modelling) and its ink outline weight; ignore the creature itself"),
        (bo, "1536 x 1024", f"the layout of the image you draw now: {k} numbered picture rectangles; follow it exactly"),
    ]
    if voi_duyet:
        ds.append((DUYET, "1536 x 1024", "the approved first sheet of this same card set: match its rendering, outline weight, colours, "
                                         "background treatment and borders EXACTLY so every card looks drawn by the same hand; ignore its subjects"))
    return ds


def prompt(n, cards, voi_duyet):
    k = len(cards)
    save = os.path.join(SAVE_DIR, f"luot_{n:02d}.png")
    ref = anh_mau(k, voi_duyet)
    L = ["Read this whole file. Then open the reference images listed below from their full paths, draw ONE image and save it as described "
         "under SAVE. Do not reply with text only.", "",
         "REFERENCE IMAGES (open each file from its full path):"]
    for i, (p, size, what) in enumerate(ref, 1):
        L.append(f"image {i} = {p} ({size}): {what}")
    stem = os.path.splitext(os.path.basename(save))[0]
    L += ["",
          "SAVE: save the finished image as a 1536 x 1024 PNG to",
          save,
          f"Create the folder if it is missing. If that file already exists, save it as {stem}_2.png, {stem}_3.png … in the same folder instead. "
          "Do not change, move or delete any other file.", "",
          f"WHAT THIS IS: {k} small card illustrations for the cards of a vertical mobile monster-battle card game (sheet {n}). Each picture "
          "sits in the art window of one card, above the card's name and rules text, and is shown only about 280 x 175 px on a phone, so it "
          "must read instantly at that small size.", "",
          f"LAYOUT: a 1536 x 1024 image on a plain pure white (#FFFFFF) background. {k} picture rectangles exactly where image 3 shows them, "
          f"each {PW} x {PH} px (16:10, landscape), with plain white gutters between them. Each picture fills its whole rectangle edge to edge "
          "and has a thin wobbly dark-brown ink border (about 4 px). Nothing crosses a rectangle's border or touches the white gutters. "
          "Picture 1 is the top-left rectangle, then left to right, row by row. Do not draw the numbers, the grey guide fill or any text.", "",
          "THE MOST IMPORTANT RULE: a player who glances at a picture must understand, or at least guess, what the card DOES "
          "(attack, heal, shield, gain mana, weaken the enemy...). Show the EFFECT, not a creature. Build every picture from the shared "
          "visual language below so the same idea always looks the same on every card.", "",
          "VISUAL LANGUAGE (use exactly these looks every time):",
          "- health = a red heart; healing = a green plus sign; a health bar = a short horizontal red bar in an ink frame (empty part cream);",
          "- mana = a blue water drop; rage = an orange flame;",
          "- attack = a steel sword; defense = a blue kite shield; a shield barrier = a light-blue bubble dome;",
          "- more / increase = a chunky green up-arrow; less / decrease = a chunky red down-arrow;",
          "- lasts several turns = a small hourglass; stun = yellow stars circling a head; poison = green bubbles and a small green skull-shaped bubble;",
          "- another card in hand = a small blank playing card (cream face, ink border, may carry one small symbol);",
          "- THE ENEMY = always the same cute straw training dummy: round burlap-sack head with two stitched dot eyes and a stitched frown, "
          "straw tufts at the neck and arms, standing on a wooden post. Anything done TO the enemy (hit, burned, poisoned, stunned, armour "
          "broken, mana stolen) is drawn ON this dummy. When the card only helps yourself, do not draw the dummy.", "",
          "EVERY PICTURE:",
          "- one big, clear idea in the middle, filling about 60-70% of the rectangle: chunky simple shapes with bold silhouettes, the effect "
          "symbols big enough to read at 280 x 175 px; a little action (motion lines, sparks, puffs, small flying pieces); nothing tiny or fussy.",
          "- background: cream paper (#FBF4E2) with one loose oval patch of light coloured-pencil hatching behind the subject, in a pale "
          "colour that contrasts with the subject; nothing else in the background, no scenery, no ground line unless the subject needs it.",
          "- NO animals and NO animal body parts (no paws, fur, claws, beast faces, legs, tails) unless the description names them; no people.",
          "- cute but fierce, like a kid's adventure notebook drawn by a professional illustrator.", "",
          "RENDERING: bold dark-brown ink outlines (#2B2118), about 6 px, slightly wobbly like a real pen, thinner (3 px) on small inner "
          "details. Fill every area with ONE flat colour with a soft colour-pencil and crayon grain, as in image 2; the grain is texture "
          "only, never light and dark modelling.",
          NO_SHADOWS,
          "No glow, no halo, no soft light, no gradient, no white shine spots, no glossy or 3D look. Energy (flames, lightning, magic, rays) "
          "is drawn as flat solid shapes with ink outlines.",
          "PALETTE: ink #2B2118, paper #FBF4E2, red #E8553F, orange #F39A2D, yellow #F7C948, green #6CBF4F, teal #3FB8A9, blue #4A90D9, "
          "purple #9A6AD6, pink #F07FA6, straw beige #D9B48A, stone grey #9A9A92.",
          "No text, no letters, no numbers, no runes, no readable symbols anywhere.", "",
          f"THE {k} PICTURES (number = rectangle in image 3; the card's name and what it does in the game, then what to draw):"]
    for i, c in enumerate(cards, 1):
        L.append(f'{i}. "{c["en"]}" ({c["does"]}): {c["draw"]}.')
    L += ["", f"Remember: save the image to {save}"]
    return "\n".join(L) + "\n"


def huong_dan(luot_da_dung, tong):
    L = ["# Tranh thẻ chung: gói gửi GPT", "",
         "Kế hoạch: `GD_Claude/36_TranhThe.md`. Sinh lại gói: `py -3 -I ArtGen/Cards/build.py`.", "",
         "## Cách gửi", "",
         "Mỗi lượt chỉ gửi GPT **đường dẫn một file prompt**. GPT tự mở ảnh mẫu và tự lưu ảnh vào `ArtGen/Cards/tai_ve/`.", "",
         "| Lượt | File prompt | Thẻ | Lưu vào |", "|---|---|---|---|"]
    for n, cards, path in luot_da_dung:
        ten = ", ".join(c["vi"] for c in cards)
        L.append(f"| {n} | `{path}` | {ten} | `tai_ve/luot_{n:02d}.png` |")
    if len(luot_da_dung) < tong:
        L += ["", f"Lượt 2–{tong} chưa dựng: chúng lấy tấm lượt 1 đã duyệt làm ảnh mẫu (`tai_ve/luot_01.png`). "
                  "Duyệt lượt 1 xong chạy lại `build.py` là có đủ file."]
    L += ["", "## Ảnh mẫu trông thế nào", "",
          "- `ArtGen/Islands/refs/world_style.png` (1024 × 1536): bản đồ 5 vùng hệ vẽ tay, viền nâu rung, gạch chì màu trên giấy kem. Chỉ lấy cách vẽ.",
          "- `ArtGen/Spine/inbox/dat_nung_1/tai_ve/L3_1.png` (1536 × 1024, nền trắng): concept tướng đất nung cầm kiếm, tô phẳng chì sáp. Chỉ lấy cách tô.",
          "- `ArtGen/Cards/gui_gpt/bo_cuc_<k>.png` (1536 × 1024, nền trắng): k ô xám 464 × 290 đánh số 1…k, chỗ đặt từng tranh.",
          "- Từ lượt 2: `ArtGen/Cards/tai_ve/luot_01.png`, tấm lượt 1 đã duyệt, để giữ nét đồng đều.", "",
          "## Cách kiểm", "",
          "- Đủ số ô, đúng chỗ, mỗi ô một tranh có viền mực, khe trắng giữa các ô, không hình nào lấn ra khe.",
          "- Tranh đúng thứ tự thẻ (ô 1 = thẻ đầu tiên trong bảng trên).",
          "- **Nhìn là đoán được thẻ làm gì** (người dùng dặn 2026-11-27): tim = máu, dấu cộng xanh = hồi, giọt xanh = mana, lửa cam = nộ, "
          "kiếm = công, khiên xanh = thủ, bong bóng xanh nhạt = khiên chắn, mũi tên xanh lên = tăng, mũi tên đỏ xuống = giảm, đồng hồ cát = nhiều lượt, "
          "sao quanh đầu = choáng, bọt xanh lá + đầu lâu = độc; địch luôn là hình nộm rơm.",
          "- Gần như không có thú: không chân, lông, móng, mặt thú (trừ khi cảnh ghi rõ, như cặp nanh của Cắn Xé).",
          "- Nhìn thu nhỏ còn đọc được: ý chính to, rõ.",
          "- Không chữ, không số; không bóng đổ, không quầng sáng, không bóng loáng; tô phẳng.", "",
          "## Câu sửa nhanh (gửi GPT kèm file prompt)", "",
          "- Lệch ô: `Same pictures, but put each one exactly inside its rectangle from image 3, with white gutters between them.`",
          "- Bóng, sáng: `Same pictures, but flat colours only: no shading, no glow, no shine spots, no drop shadows.`",
          "- Nhỏ, rối: `Same pictures, but make each main subject bigger and simpler, readable at 280 x 175 px.`",
          "- Có chữ: `Same pictures, with no text, letters or numbers anywhere.`", ""]
    return "\n".join(L)


def main():
    os.makedirs(OUT, exist_ok=True)
    data = json.load(open(os.path.join(HERE, "canh_the_chung.json"), encoding="utf-8"))["cards"]
    cards_json = os.path.normpath(os.path.join(ART, "..", "Assets", "02 Data", "Json", "cards.json"))
    pool = json.load(open(cards_json, encoding="utf-8"))["pool"]
    vi = {c["id"]: c["name"] for c in pool}
    ids = [c["id"] for c in pool]
    assert [c["id"] for c in data] == ids, "canh_the_chung.json lệch thứ tự hoặc thiếu thẻ so với cards.json"
    for c in data:
        c["vi"] = vi[c["id"]]
    tong = math.ceil(len(data) / PER)
    duyet = os.path.exists(DUYET)
    da_dung = []
    for n in range(1, tong + 1):
        cards = data[(n - 1) * PER: n * PER]
        if n > 1 and not duyet:
            # file lượt sau dựng từ lần trước (theo tấm lượt 1 cũ) thì ghi đè thành giấy báo, tránh gửi nhầm
            cu = os.path.join(OUT, f"luot_{n:02d}.txt")
            if os.path.exists(cu):
                open(cu, "w", encoding="utf-8").write(f"NOT READY - do not send. Lượt {n} chờ duyệt lượt 1 ({os.path.basename(DUYET)}), "
                                                      "rồi chạy lại ArtGen/Cards/build.py.\n")
            continue
        k = len(cards)
        bo = os.path.join(OUT, f"bo_cuc_{k}.png")
        if not os.path.exists(bo):
            ve_bo_cuc(k, bo)
        path = os.path.join(OUT, f"luot_{n:02d}.txt")
        open(path, "w", encoding="utf-8").write(prompt(n, cards, n > 1))
        da_dung.append((n, cards, path))
    open(os.path.join(OUT, "HUONG_DAN.md"), "w", encoding="utf-8").write(huong_dan(da_dung, tong))
    for n, cards, path in da_dung:
        print(f"lượt {n}: {len(cards)} thẻ → {path}")
    if not duyet:
        print(f"chưa có {DUYET}: chỉ dựng lượt 1")


if __name__ == "__main__":
    main()
