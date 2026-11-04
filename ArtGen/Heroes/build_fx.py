# Sinh gói gửi GPT cho hiệu ứng clip CHIÊU của một dòng tướng: ArtGen/Heroes/gui_gpt/<mã>_fx/ (người dùng 2026-11-03: làm lại
# hiệu ứng chiêu của 3 dạng Giọt Sương cho đẹp, hoành tráng hơn, thay quầng sáng aola).
# Một lượt, một file prompt (tiếng Anh) + HUONG_DAN.md (tiếng Việt), theo quy ước của build.py: file mở đầu bằng danh sách ảnh mẫu
# kèm đường dẫn đầy đủ (GPT tự mở), mục SAVE, mỗi bước một ảnh; GPT tự lưu vào inbox/<mã>_fx/tai_ve/<bước>.png.
# Hiệu ứng là hình vẽ tay rời trên nền trắng (game cắt nền), Claude ghép vào clip CHIÊU bằng aola tools/anim_moi.py (khoá "fx").
# Chạy: py -3 -I ArtGen/Heroes/build_fx.py
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/") + "/"
WORLD_STYLE = os.path.normpath(ROOT + "../Islands/refs/world_style.png").replace("\\", "/")


def W(p):
    return p.replace("/", "\\")


# Luật tướng (người dùng 2026-11-04, cả hiệu ứng): vẽ tay trên giấy bằng bút mực, tô chì màu và sáp màu; không bóng, không ánh
# sáng: mỗi vùng một màu đều, không mảng sáng tối, không điểm sáng, không quầng sáng (thay luật 2026-11-03: bóng chì gạch chéo).
FLAT_FIX = ("Flat colour only: every area one even colour coloured with pencil and wax crayon strokes; no shading, no shadows, "
            "no white highlights or shine, no glow, no gradients.")
LINE = ("RENDERING: the hand-drawn look of image 1 (the game's map): drawn by hand on paper with a dark-brown ink pen (#2B2118), "
        "an outline about {n} px thick on this 1024 canvas, the same weight on every edge, slightly wobbly like a real pen; every "
        "area coloured with coloured pencils and wax crayons, the strokes visible as loose diagonal hatching (strokes thinner "
        "than the outline). Colours of water from images 2-4 (clear sky blue, light blue, deep blue, white foam); gold only where "
        "the step says.\n"
        "FLAT COLOUR, NO LIGHT, NO SHADOW: every area one even colour, the strokes are texture only. No shading, no darker side, "
        "no shadows of any kind (no drop shadow, no cast shadow, nothing on the background), no white highlights or shine "
        "spots, no gloss, no glow or halo, no gradients, no 3D render. White appears only as a flat colour where the step says "
        "(foam, a sparkle), never as a light reflection.\n"
        "CANVAS: a square 1024 x 1024 image, plain pure white background (the game cuts the white away, so keep a clear white "
        "margin all round and do not let the effect touch the edges), the effect centred and filling about 75% of the canvas. "
        "Only this effect: no creature, no hand, no weapon, no ground, no text, no frame, no white sticker border.")

LINES = [
    {"code": "giot_suong_fx", "hero": "Giọt Sương", "elem": "thuy",
     "forms": ["giot_suong_1", "giot_suong_2", "giot_suong_3"],
     "steps": [
         ("FX09", "tia_nuoc", "tia nước bắn thẳng", 16,
          "A straight jet of water shot to the RIGHT, seen from the side: a long horizontal beam of rushing water, about five times longer than tall; a big round splashing head with white foam at the RIGHT end, the body slightly wavy with streaks of light and deep blue, tapering to thin wisps and a few droplets at the LEFT end. The mana attack of the water knight: the game stretches it from the hero to the enemy and scales it by evolution stage.",
          "tia nước bắn ngang sang phải, dài khoảng gấp năm lần chiều cao: đầu tia tròn bắn bọt trắng ở bên phải, thân hơi gợn có vệt xanh nhạt và xanh đậm, đuôi thon thành sợi mảnh và vài giọt ở bên trái"),
         ("FX02", "song_luoi_liem", "sóng nước lưỡi liềm", 16,
          "A crescent-shaped slash wave made of water, seen from the side, flying to the RIGHT: a thick curved front edge on the right, two thin pointed horns trailing to the upper left and lower left, white foam along the front edge, a few droplets flung off behind it. Like a sword slash turned into a rushing water wave.",
          "sóng hình lưỡi liềm bay sang phải: mép trước dày cong ở bên phải, hai sừng nhọn kéo về trên trái và dưới trái, bọt trắng dọc mép trước, vài giọt bắn phía sau"),
         ("FX03", "no_nuoc", "nước nổ tung", 16,
          "A big round splash burst of water seen from the front: eight to ten pointed water spikes and drops bursting outward from the centre in a ring, white foam in the middle, small droplets flying out between the spikes. The impact of a water attack.",
          "vụ nổ nước tròn nhìn thẳng: 8-10 mũi nước nhọn và giọt bắn ra quanh tâm, giữa là bọt trắng, giọt nhỏ bay ra giữa các mũi"),
         ("FX01", "xoay_nuoc", "vòng nước xoáy", 14,
          "A ring of swirling water seen from the front: three curling streams of water chasing each other around an EMPTY centre (the centre stays plain white and open), each stream thick at its head and thin at its tail, a few droplets flung off the ends. A small whirlpool ring that will spin around the hero.",
          "vòng nước xoáy nhìn thẳng: ba dòng nước cuộn đuổi nhau quanh tâm rỗng (giữa để trắng), đầu dòng dày đuôi mảnh, vài giọt văng ra"),
         ("FX04", "giot_nuoc", "chùm giọt nước", 12,
          "A loose cluster of five separate water droplets of different sizes, each a clean teardrop of flat light blue with a thin deeper-blue rim, all falling down and to the lower left, with small gaps between them.",
          "năm giọt nước rời to nhỏ khác nhau, mỗi giọt hình giọt lệ xanh nhạt tô phẳng, viền xanh đậm mảnh, cùng rơi xuống chéo trái"),
         ("FX05", "lap_lanh", "tia lấp lánh", 12,
          "One big four-pointed sparkle star, white with a light-blue rim and a tiny gold centre, plus two small four-pointed sparkles beside it.",
          "một ngôi sao lấp lánh bốn cánh lớn, trắng viền xanh nhạt, tâm vàng nhỏ, cạnh là hai sao nhỏ"),
         ("FX06", "bong_bong", "bong bóng", 14,
          "One big round water bubble: a very pale blue inside coloured flat with light crayon strokes, a thin rim of deeper blue, and a small curl of white foam stuck to its lower edge. Hand-drawn, flat, not glossy, no shine spot.",
          "một bong bóng nước tròn lớn: lòng xanh rất nhạt tô phẳng bằng nét sáp nhẹ, viền xanh đậm mảnh, một cụm bọt trắng nhỏ bám ở mép dưới; không vệt sáng"),
         ("FX07", "song_than", "sóng thần cuộn", 18,
          "A big curling wave of water seen from the side, rolling to the RIGHT: it rises from a flat base on the left, climbs and curls over at the top right into a hollow curl, a white foam crest and spray flying from the lip; deep blue body, lighter blue inside the curl. Grand and powerful but cartoon-clean.",
          "sóng lớn nhìn ngang cuộn sang phải: dâng từ chân phẳng bên trái, cuộn lại ở trên phải thành vòm rỗng, mào bọt trắng và bụi nước ở mép sóng"),
         ("FX08", "vong_song_dat", "vòng sóng loang mặt đất", 14,
          "A flat oval ripple ring of water on the ground, seen from a low side angle: an ellipse about three times wider than tall made of splashing water, small splashes rising along its rim, an EMPTY centre (plain white).",
          "vòng sóng nước loang trên mặt đất nhìn chếch thấp: hình bầu dục rộng gấp ba chiều cao, viền có tia nước nhỏ bắn lên, giữa rỗng trắng"),
     ]},
]


def build(f):
    code = f["code"]
    pk = ROOT + f"gui_gpt/{code}/"
    save = ROOT + f"inbox/{code}/tai_ve/"
    os.makedirs(pk, exist_ok=True)
    os.makedirs(save, exist_ok=True)
    refs = [(WORLD_STYLE, "the game's approved hand-drawn map: copy its RENDERING (ink outlines, coloured-pencil hatching), ignore its content",
             "Ảnh mốc nét vẽ đã duyệt (1024 × 1536, nền đặc): bản đồ sảnh vẽ tay, viền mực nâu hơi rung, tô chì màu gạch chéo. Lấy nét vẽ, không lấy nội dung")]
    for i, fc in enumerate(f["forms"], 1):
        refs.append((ROOT + f"inbox/{fc}/concept_duyet.png", f"approved concept of stage {i} of this hero: take only its water COLOURS and drawing style, do not draw the creature",
                     f"Concept đã duyệt dạng {i} ({fc}, nền trắng): chỉ lấy màu nước và nét vẽ, không vẽ con"))
    missing = [W(p) for p, _, _ in refs if not os.path.exists(p)]
    if missing:
        raise SystemExit("thiếu ảnh mẫu: " + ", ".join(missing))
    steps = f["steps"]
    order = [s[0] for s in steps]
    p1 = pk + "luot_1_hieu_ung.txt"
    t = ["Read this whole file. Then open the reference images listed below from their full paths, draw ONE image per reply "
         "and save each one as its step says. Do not reply with text only.", "",
         "REFERENCE IMAGES (open each file from its full path):"]
    t += [f"image {i} = {W(p)}: {en}" for i, (p, en, _) in enumerate(refs, 1)]
    t += ["", "WHAT THIS IS: special-attack effects for a 2D creature game with a hand-drawn storybook look. Each step is ONE "
          "separate effect sprite (water magic for a water knight and its dragon form). The game animates them (moves, spins, "
          "scales, fades), so draw each effect alone, still, centred on white.", "",
          f"SAVE: every step's image goes into {W(save)} under the step's name (for example {order[0]}.png). If that file "
          "already exists, add _2, _3 … before .png. Do not change, move or delete any other file.", "",
          f"ORDER: draw step {order[0]} now, save it and stop. When I say \"next\", draw step {order[1]}, save it and stop: I "
          f"will check both. When I say \"continue\", draw the remaining steps one per reply, each after I say \"next\", in this "
          f"order: {', '.join(order[2:])}.", ""]
    for sc, name, _, n, prompt, _ in steps:
        t += [f"=== STEP {sc} ({name.replace('_', ' ')}) ===", prompt, "", LINE.format(n=n),
              f"SAVE this step: save it as a PNG to {W(save + sc + '.png')} (create the folder if it is missing; if that file "
              f"already exists, save it as {sc}_2.png, {sc}_3.png … in the same folder instead). Do not change, move or delete "
              "any other file.", ""]
    open(p1, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")

    g = [f"# Gói gửi GPT: hiệu ứng chiêu {f['hero']} (`{code}`)", "",
         "Hiệu ứng vẽ tay cho clip CHIÊU của cả ba dạng (thay quầng sáng gốc của aola), người dùng dặn 2026-11-03: đẹp và hoành "
         f"tráng hơn. Mỗi hiệu ứng là một hình rời trên nền trắng; Claude ghép vào clip CHIÊU (aola `tools/anim_moi.py`). Quy trình: "
         f"`{W(ROOT + 'QUY_TRINH.md')}`.", "",
         f"**Chỉ gửi GPT đường dẫn file prompt:** `{W(p1)}` (chat mới). GPT tự mở ảnh mẫu và tự lưu ảnh vào `{W(save)}`.", "",
         f"1. GPT vẽ {order[0]}. Gõ `next`: GPT vẽ {order[1]}. Nhắn Claude \"soi thử {code}\".",
         f"2. Claude bảo ổn thì gõ `continue`, rồi `next` sau mỗi ảnh: {', '.join(order[2:])}.",
         f"3. Đủ ảnh thì nhắn Claude \"ghép {code}\".", "",
         "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    g += [f"| {i} | `{W(p)}` | {vi} |" for i, (p, _, vi) in enumerate(refs, 1)]
    g += ["", "Kiểm từng ảnh trước khi lưu (vẽ tay trên giấy, viền mực nâu, tô chì sáp phẳng; không mảng sáng tối, không điểm sáng, "
          "không bóng loáng, không quầng sáng, không bóng đổ; nền trắng, không chạm mép ảnh, không có con, không chữ):", ""]
    g += [f"- **{sc}** {vi_name} (viền khoảng {n} px): {vi}" for sc, _, vi_name, n, _, vi in steps]
    g += ["", "## GPT vẽ sai thì gửi thêm (cùng chat)", "", "| Sai | Gửi thêm |", "|---|---|",
          "| Không giống vẽ tay trên giấy | `Draw it by hand on paper: dark-brown ink-pen outlines, every area coloured with coloured pencils and wax crayons, the strokes visible as loose diagonal hatching.` |",
          f"| Quầng sáng, điểm sáng, mảng sáng tối, bóng loáng | `{FLAT_FIX}` |",
          "| Chạm mép ảnh, nền không trắng | `Keep the whole effect inside the canvas with a clear white margin; plain pure white background.` |",
          "| Có con, tay, vũ khí | `Only the effect itself, nothing else.` |",
          f"| Có bóng đổ, bóng in xuống nền | `{FLAT_FIX}` |", "",
          f"Gói này sinh từ `{W(ROOT + 'build_fx.py')}`; sửa prompt ở đó rồi chạy lại.", ""]
    open(pk + "HUONG_DAN.md", "w", encoding="utf-8", newline="").write("\n".join(g))
    return W(p1)


# ảnh dùng chung trên sân đấu (StageView.Beam: tia và hiệu ứng lúc phóng, lúc trúng): bước GPT → tên file, khoét lõi trắng (hình vòng),
# cạnh dài tối đa (điểm ảnh): theo cỡ hiện lớn nhất trên sân (đơn vị canvas, sân x2): tia kéo dài tới khoảng 800, nổ nước và vòng sóng
# tới khoảng 500 (boss), giọt và lấp lánh dưới 150 nên 192 là đủ nét
STAGE_FX = [("FX09", "tia_nuoc", False, 512), ("FX03", "no_nuoc", False, 512), ("FX04", "giot_nuoc", False, 192),
            ("FX05", "lap_lanh", False, 192), ("FX08", "vong_song", True, 512)]


def export_stage(code="giot_suong_fx"):
    """--xuat: các ảnh dùng chung trên sân đấu vào Assets/03 Art/Fx/ (menu PokiClash/Prefab/Sàn đấu: tia nước của chiêu bắn)"""
    for step, name, hollow, side in STAGE_FX:
        export_beam(code, step, name, hollow, side)


def export_beam(code="giot_suong_fx", step="FX09", out_name="tia_nuoc", hollow=False, side=512):
    """ảnh GPT mới nhất của bước vào Assets/03 Art/Fx/<out_name>.png: cắt nền trắng nối mép (hollow: cả mảng trắng lớn nhất bên
    trong), cắt sát, thu về cạnh dài tối đa side điểm ảnh, lưu PNG nén kỹ; chưa có ảnh tia thì vẽ tạm một tia đơn giản để thử"""
    import glob
    import numpy as np
    from PIL import Image, ImageDraw
    out = os.path.normpath(ROOT + f"../../Assets/03 Art/Fx/{out_name}.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    src = sorted(glob.glob(ROOT + f"inbox/{code}/tai_ve/{step}*.png"), key=os.path.getmtime, reverse=True)
    if src:
        import cv2
        rgb = np.asarray(Image.open(src[0]).convert("RGB")).astype(np.float32)
        mn = rgb.min(2)
        near = (mn > 215).astype(np.uint8)
        n, lab, st, _ = cv2.connectedComponentsWithStats(near, connectivity=4)
        border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
        bg = np.isin(lab, sorted(border))
        if hollow:
            inner = [i for i in range(1, n) if i not in border]
            if inner:
                bg |= lab == max(inner, key=lambda i: st[i, cv2.CC_STAT_AREA])
        alpha = np.where(bg, 0, 255).astype(np.uint8)
        alpha = cv2.GaussianBlur(alpha, (3, 3), 0)
        im = Image.fromarray(np.dstack([rgb.astype(np.uint8), alpha]), "RGBA")
        im = im.crop(im.getbbox())
        if max(im.size) > side:
            k = side / max(im.size)
            im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
        note = os.path.basename(src[0])
    elif step != "FX09":
        print(f"{step}: chưa có ảnh GPT, bỏ qua")
        return
    else:
        im = Image.new("RGBA", (640, 128), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        ink, blue, light, white = (43, 33, 24, 255), (60, 140, 230, 255), (150, 210, 250, 255), (255, 255, 255, 255)
        d.polygon([(4, 64), (420, 22), (560, 14), (560, 114), (420, 106)], fill=ink)
        d.polygon([(14, 64), (420, 30), (556, 22), (556, 106), (420, 98)], fill=blue)
        d.polygon([(40, 64), (430, 46), (550, 44), (550, 70), (430, 68)], fill=light)
        d.ellipse((500, 6, 636, 122), fill=ink)
        d.ellipse((508, 14, 628, 114), fill=light)
        d.ellipse((540, 34, 600, 76), fill=white)
        note = "hình tạm (chưa có ảnh GPT)"
    im.save(out, optimize=True)
    print(f"{W(out)}: {note} {im.size[0]}x{im.size[1]}, {os.path.getsize(out) // 1024} KB")


if __name__ == "__main__":
    if "--xuat" in sys.argv:
        export_stage()
    else:
        for f in LINES:
            print(build(f))
