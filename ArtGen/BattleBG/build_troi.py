# Nền trận vẽ dư trời cho máy dài (người dùng 2026-11-04: máy dài hơn 9:16 thì vùng sân cao thêm, phần trên chỉ có màu trời trơn).
# Vùng sân cao 928 ở 9:16, thêm 300 ở 2960 x 1440, 480 ở 20:9, 600 ở 21:9. Mỗi nền đảo Thủy đã duyệt (build_thuy.py) cho GPT vẽ
# nối lên trên (outpainting): khung 1024 x 1536, 880 px dưới là khung sân cũ, 656 px trên để trắng cho GPT vẽ tiếp.
# Duyệt: khớp ảnh GPT với nền cũ (tỉ lệ, dịch), 928 dòng dưới giữ nguyên ảnh cũ, phần trên lấy của GPT, nối theo đường ít lệch nhất
# trong dải 96 dòng ngay trên mép cũ (cắt kiểu ghép vân), mờ mép 4 px. Ra 1080 x 1528 (600 trên + khung 928), lưu troi/<mã>.png
# và ảnh soi troi/soi_<mã>.png (vạch chỗ máy 9:16, 2960 x 1440, 20:9, 21:9 bắt đầu thấy, đường nối).
# Đưa vào game: build_thuy.py --xuat (nền nào có troi/<mã>.png thì xuất bản cao; StageView.FitBg neo đáy ảnh vào đáy khung).
# Ghi: gui_gpt/troi/ (<nn>_<mã>.txt, khung_<mã>.png, HUONG_DAN.md); GPT lưu ảnh vào troi/tai_ve/.
# Chạy: py -3 -I ArtGen/BattleBG/build_troi.py
# Duyệt: py -3 -I ArtGen/BattleBG/build_troi.py --duyet <mã> [ảnh] (mặc định ảnh mới nhất troi/tai_ve/<mã>*.png); dựng lại gói
# (boss dạng 2, 3 cần dạng 1 đã duyệt).
import argparse
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent  # ArtGen/BattleBG
sys.path.insert(0, str(HERE))

import numpy as np  # noqa: E402
from PIL import Image, ImageDraw, ImageFilter  # noqa: E402

import build_thuy as bt  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
PACK = HERE / "gui_gpt" / "troi"
WORK = HERE / "troi"  # <mã>.png: bản cao đã ghép; soi_<mã>.png
INBOX = WORK / "tai_ve"

CW, CH = 1024, 1536  # khung GPT
OH = round(CW * bt.FH / bt.FW)  # 880: khung sân cũ thu về bề ngang 1024
TOP = CH - OH  # 656: phần GPT vẽ
EXTRA = 600  # phần trời thêm của bản cuối (đủ tới 21:9)
FULL = bt.FH + EXTRA  # 1528
BAND = 96  # dải tìm đường nối, ngay trên mép cũ (theo bản cuối 1080)
FEATHER = 4
SHOWS = [(0, "9:16"), (300, "2960x1440"), (480, "20:9"), (600, "21:9")]  # phần dôi của vùng sân theo máy

# Thứ tự lượt, câu tả phần trên cho GPT (TOP) và cho người dùng
ORDER = ["c01", "c02", "c03", "c04", "c05", "c06", "c07", "c08", "c09", "m20", "m30", "m40", "m50", "m60",
         "b70a", "b70b", "b70c"]
DAY = ("the same bright pale-blue sky, hatched with the same diagonal pencil strokes, becoming only a little deeper blue towards "
       "the very top")
UP = {
    "c01": (f"{DAY}. Complete the cloud cut by the old top-left corner and add two or three more small fluffy cream clouds with "
            f"thin ink outlines, spread out. The palm leaves at the far left edge may reach a little higher.",
            "trời xanh nhạt, hoàn chỉnh đám mây bị cắt ở góc trên trái, thêm 2, 3 đám mây nhỏ"),
    "c02": (f"{DAY}. Complete the cloud cut by the old top-left corner and add two or three more small fluffy cream clouds.",
            "trời xanh nhạt, hoàn chỉnh mây góc trên trái, thêm vài đám mây nhỏ"),
    "c03": (f"{DAY}. Complete the cloud cut by the old top-left corner and add two or three more small fluffy cream clouds.",
            "trời xanh nhạt, hoàn chỉnh mây góc trên trái, thêm vài đám mây nhỏ"),
    "c04": (f"{DAY}. Complete the cloud cut by the old top-left corner and add two or three more small fluffy cream clouds.",
            "trời xanh nhạt, hoàn chỉnh mây góc trên trái, thêm vài đám mây nhỏ"),
    "c05": (f"{DAY}. The striped lighthouse at the far left is already complete (its red cone roof is inside the old picture): "
            f"keep it, only sky above it. Complete the cloud cut by the old top edge and add two or three small fluffy cream "
            f"clouds.", "trời xanh nhạt; hải đăng bên trái đã đủ mái, phía trên chỉ là trời; vài đám mây nhỏ"),
    "c06": (f"{DAY}. The cliff and the waterfall at the far left are already complete (their grassy top is inside the old "
            f"picture; the water comes from the left edge): keep them, only sky above them. Complete the cloud cut by the old "
            f"top edge at the upper left and add two or three small fluffy cream clouds.",
            "trời xanh nhạt; vách và thác bên trái đã đủ đỉnh, phía trên chỉ là trời; hoàn chỉnh mây bị cắt ở mép trên, thêm vài "
            "đám mây"),
    "c07": (f"{DAY}. Complete the cloud cut by the old top-left corner and add two or three more small fluffy cream clouds.",
            "trời xanh nhạt, hoàn chỉnh mây góc trên trái, thêm vài đám mây nhỏ"),
    "c08": (f"{DAY}. Complete the cloud cut by the old top-left corner and add two or three more small fluffy cream clouds.",
            "trời xanh nhạt, hoàn chỉnh mây góc trên trái, thêm vài đám mây nhỏ"),
    "c09": (f"{DAY}. The turtle-shell temple at the far left is already complete: keep it, only sky above it. Complete the "
            f"cloud cut by the old top-left corner and add two or three small fluffy cream clouds.",
            "trời xanh nhạt; đền mai rùa bên trái đã đủ, phía trên chỉ là trời; vài đám mây nhỏ"),
    "m20": ("The red cone roof of the striped lighthouse at the far left is cut by the old top edge: complete the roof up to "
            "its pointed tip with a small ball on it, the tip about 60 px above the old edge, the same width and slope. Around "
            "it the dramatic sunset storm sky continues upward: the same heavy violet and slate-blue clouds with warm pink-orange "
            "rims, the sky becoming deeper violet-blue towards the very top. No light beam (the game animates it).",
            "mái nón đỏ của hải đăng bên trái bị cắt ở mép cũ: vẽ nốt tới chóp; trời hoàng hôn bão tiếp lên, mây tím xám viền "
            "hồng cam, lên cao tím xanh đậm dần; không vẽ tia đèn"),
    # 2026-11-05: hai bản đầu vẽ lặp mảng rêu và vách ngay trên mép cũ (gãy ngang qua vách và hai thác): dặn rõ chỗ nối
    "m30": ("The big mossy grey cliff and its two waterfalls pour from above the old top edge: continue the cliff and both "
            "waterfalls upward, the same width and place, to the cliff top (a mossy edge with ferns, round bushes and a palm "
            "tree) where the water spills over, about y 200-320 of your image; above the cliff and on the right the cool fresh "
            "morning sky continues upward (soft silver-blue, a few soft white clouds), a little deeper blue towards the very top. "
            "THE JOIN AT y 656 IS THE HARD PART: look at the first rows of image 1 and continue exactly those shapes upward. The two "
            "waterfall streams keep their exact left and right edges and their white streaks run straight up across the join; the "
            "rock outlines and cracks that touch the old top edge carry on upward from the same points. The big moss patch with "
            "hanging vines just below the old top edge is NOT repeated: right above the join the cliff is plain grey rock with a "
            "few cracks and small tufts, then the mossy cliff top. Never copy or mirror any strip of the old picture above it.",
            "vách đá rêu và hai dòng thác chảy từ trên mép cũ: vẽ tiếp lên tới đỉnh vách (rêu, dương xỉ, bụi, cây cọ) chỗ nước "
            "đổ xuống; trên đó và bên phải là trời sáng sớm xanh bạc, vài đám mây"),
    "m40": ("The magical twilight sky continues upward: the same violet-blue sky, becoming deeper indigo towards the very top, "
            "a few more tiny stars and two or three small soft lilac clouds. The thin crescent moon stays where it is (no second "
            "moon). The giant clam at the left is already complete.",
            "trời chạng vạng tím xanh tiếp lên, cao lên chàm đậm dần, thêm sao nhỏ, vài đám mây tím nhạt; giữ trăng khuyết, "
            "không thêm trăng"),
    "m50": ("The calm night sky continues upward: the same deep blue with many small stars, becoming a little darker towards "
            "the very top, two or three small dark-blue clouds with pale silver rims. Complete the full moon at the upper left if "
            "the old top edge touches it; no second moon.",
            "trời đêm xanh đậm nhiều sao tiếp lên, cao lên tối dần, vài đám mây nhỏ viền bạc; trăng tròn giữ nguyên, không thêm "
            "trăng"),
    "m60": ("The turtle-shell temple at the far left is cut by the old top edge: complete its dome (the mossy green turtle-shell "
            "roof with its hexagon plates, vines hanging), the dome top about 120 px above the old edge. The palm leaves at the "
            "top-right corner continue a little. Around them the mysterious dusk sky continues upward: teal below, violet above, "
            "a few soft violet clouds, deeper violet towards the very top.",
            "đền mai rùa bên trái bị cắt ở mép cũ: vẽ nốt mái vòm mai rùa phủ rêu, dây leo; lá cọ góc trên phải vươn thêm; trời "
            "chạng vạng xanh ngọc lên tím, vài đám mây tím"),
    "b70a": ("The broken carved stone pillar at the far left edge rises above the old top edge: continue it upward and end it "
             "in a broken, jagged top about 160 px above the old edge, a little seaweed hanging. Around it the deep blue stormy "
             "dusk continues upward: the same heavy slate-blue storm clouds, becoming darker and heavier towards the very top. "
             "No lightning, no rain, no trident.",
             "cột đá chạm sóng bên trái nhô lên trên mép cũ: vẽ tiếp lên, đỉnh gãy lởm chởm; trời bão chạng vạng xanh đậm tiếp lên, "
             "mây xám xanh dày dần; không sét, mưa, đinh ba"),
    "b70b": ("Extend it exactly like image 2 (phase 1 of this arena, already extended and approved): the same pillar top, the "
             "same cloud shapes in the same places, only in this image's darker, stormier weather and light. No lightning, no "
             "rain, no trident.",
             "nối lên y như bản dạng 1 đã duyệt (ảnh 2): cùng đỉnh cột, cùng chỗ mây, chỉ theo trời bão tối hơn của ảnh này"),
    "b70c": ("Extend it exactly like image 2 (phase 1 of this arena, already extended and approved): the same pillar top, the "
             "same cloud shapes in the same places, only in this image's darkest purple-black storm. No lightning, no rain, no "
             "trident.",
             "nối lên y như bản dạng 1 đã duyệt (ảnh 2): cùng đỉnh cột, cùng chỗ mây, chỉ theo trời bão đêm tím đen của ảnh này"),
}


def done(i):
    return WORK / f"{i}.png"


def needs(i):
    return ["b70a"] if i in ("b70b", "b70c") else []


def ready(i):
    return all(done(n).exists() for n in needs(i))


def canvas(i):
    """khung gửi GPT: khung sân cũ thu về 1024 x 880 ở dưới, phần trên trắng"""
    im = Image.new("RGB", (CW, CH), "white")
    im.paste(bt.frame_of(i).resize((CW, OH), Image.LANCZOS), (0, TOP))
    return im


def ref_list(i):
    """[(đường dẫn, câu cho GPT, câu cho người dùng)]"""
    out = [(PACK / f"khung_{i}.png",
            f"the picture to extend: its bottom part (y {TOP}-{CH}) is a finished hand-drawn battle background of this game, its "
            f"top part (y 0-{TOP}) is empty white canvas for you to paint",
            f"khung nối trời ({CW} × {CH}): {OH} px dưới là nền trận {bt.BY_ID[i]['vi']} cũ, {TOP} px trên để trắng")]
    if i in ("b70b", "b70c"):
        out.append((done("b70a"), "phase 1 of this same boss arena, already extended upward and approved: extend yours the "
                                  "same way",
                    f"nền boss dạng 1 đã nối trời và duyệt ({bt.FW} × {FULL}): nối y như vậy"))
    return out


def prompt(i):
    a = bt.BY_ID[i]
    place = a.get("place") or bt.BY_ID[a["base"]]["place"]
    refs = ref_list(i)
    lines = bt.head(refs)
    lines += ["", f"SAVE: save the finished image as a {CW} x {CH} PNG to", str(INBOX / f"{i}.png"),
              f"Create the folder if it is missing. If that file already exists, save it as {i}_2.png, {i}_3.png … in the same "
              f"folder instead. Do not change, move or delete any other file."]
    lines += ["",
              f"WHAT THIS IS: the battle background of {place} on the Water island of a vertical mobile monster-battle game. On "
              f"tall phones the battle area is taller than this painting, so the game needs more of the scene ABOVE it: more sky, "
              f"and the tops of the tall things that the old top edge cuts.",
              "",
              f"TASK: extend the painting upward (outpainting). Draw one {CW} x {CH} image:",
              f"- y {TOP}-{CH} (the bottom part): keep image 1 exactly as it is: the same drawing, every shape in the same place "
              f"and size, the same colours. Do not redraw, move, crop, zoom or restyle it.",
              f"- y 0-{TOP} (the empty white top): continue the scene upward so the old top edge disappears; nobody should be able "
              f"to tell where the old picture ended. Fill it completely, edge to edge: no white, no margin, no frame.",
              "",
              f"UP THERE: {UP[i][0]}",
              "",
              "KEEP IT CALM: this part is only seen on tall phones, above the fighters and their name panels. Mostly sky in this "
              "scene's light, plus the continuation of whatever the old top edge cuts. No new landmark, no big bright object, no "
              "busy pattern, nothing that pulls the eye away from the fighters below.",
              "",
              "RENDERING: exactly the rendering of the bottom part: the same wobbly dark-brown ink outlines (thin on far things), "
              "the same coloured-pencil hatching (same direction, same density), the same cream paper grain, the same colours and "
              "light. Not 3D, not glossy, no smooth digital gradient.",
              "",
              f"Do not draw: {bt.PLAIN}; a second sun or moon; a light beam, rain or lightning (the game animates them).",
              "",
              f"Remember: save the image to {INBOX / (i + '.png')}"]
    return "\n".join(lines) + "\n"


# Gộp một file (người dùng 2026-11-04: c02–c09 làm một thể): nền thường cùng trời ban ngày, mỗi bước một ảnh, lưu riêng
GROUP = ["c02", "c03", "c04", "c05", "c06", "c07", "c08", "c09"]
GROUP_FILE = "gop_c02_c09.txt"


def group_todo():
    return [i for i in GROUP if bt.approved(i).exists() and not done(i).exists()]


def group_prompt(ids):
    n = len(ids)
    lines = [f"Read this whole file. It has {n} steps and each step is ONE separate image. Do the steps in order: for each step "
             f"open its reference image from its full path, draw the image, save it as that step says, then go straight on to "
             f"the next step. Do not reply with text only and do not stop until all {n} images are saved.", "",
             "REFERENCE IMAGES (open each file from its full path):"]
    for k, i in enumerate(ids, 1):
        lines.append(f"image {k} = {PACK / f'khung_{i}.png'} ({CW} x {CH}): step {k}, the picture to extend: its bottom part "
                     f"(y {TOP}-{CH}) is a finished hand-drawn battle background of this game, its top part (y 0-{TOP}) is "
                     f"empty white canvas for you to paint")
    lines += ["", f"SAVE: one {CW} x {CH} PNG per step:"]
    lines += [f"step {k}: {INBOX / (i + '.png')}" for k, i in enumerate(ids, 1)]
    lines += ["Create the folder if it is missing. If a file already exists, save it as <name>_2.png, <name>_3.png … in the "
              "same folder instead. Do not change, move or delete any other file.",
              "",
              "WHAT THIS IS: battle backgrounds of the Water island of a vertical mobile monster-battle game. On tall phones the "
              "battle area is taller than these paintings, so the game needs more of each scene ABOVE it: more sky, and the "
              "tops of the things that the old top edge cuts.",
              "",
              f"TASK (every step): extend the step's picture upward (outpainting). Draw one {CW} x {CH} image:",
              f"- y {TOP}-{CH} (the bottom part): keep the step's reference image exactly as it is: the same drawing, every "
              f"shape in the same place and size, the same colours. Do not redraw, move, crop, zoom or restyle it.",
              f"- y 0-{TOP} (the empty white top): continue the scene upward so the old top edge disappears; nobody should be "
              f"able to tell where the old picture ended. Fill it completely, edge to edge: no white, no margin, no frame.",
              "",
              "KEEP IT CALM: this part is only seen on tall phones, above the fighters and their name panels. Mostly sky, plus "
              "the continuation of whatever the old top edge cuts. No new landmark, no big bright object, no busy pattern. "
              "Give each step its own cloud shapes and places (they are different stages), not a copy of the previous step.",
              "",
              "RENDERING: exactly the rendering of the bottom part: the same wobbly dark-brown ink outlines (thin on far "
              "things), the same coloured-pencil hatching (same direction, same density), the same cream paper grain, the same "
              "colours and light. Not 3D, not glossy, no smooth digital gradient.",
              "",
              f"Do not draw: {bt.PLAIN}; a second sun or moon; a light beam, rain or lightning.",
              "",
              "STEPS:"]
    for k, i in enumerate(ids, 1):
        lines += ["", f"Step {k} (image {k}, {bt.BY_ID[i]['place']}): {UP[i][0]}", f"Save to {INBOX / (i + '.png')}"]
    lines += ["", f"Remember: {n} images, one per step, each saved to its own path above."]
    return "\n".join(lines) + "\n"


def guide():
    rows = []
    for n, i in enumerate(ORDER, 1):
        a = bt.BY_ID[i]
        name = f"{n:02d}_{i}.txt"
        if ready(i):
            refs = "; ".join(f"{k + 1} `{p}`: {vi}" for k, (p, _, vi) in enumerate(ref_list(i)))
            file = f"`{PACK / name}`"
        else:
            refs = "chưa có: cần " + ", ".join(f"`{x}`" for x in needs(i) if not done(x).exists()) + " đã duyệt"
            file = "chưa dựng"
        rows.append(f"| {n}. {a['vi']} (ải {a['stages']}): {UP[i][1]} | {file} | {refs} | `{INBOX / (i + '.png')}` |")
    ok = [i for i in ORDER if done(i).exists()]
    todo = [i for i in ORDER if i not in ok]
    group = group_todo()
    group_line = (f"- **Bước tiếp:** gửi GPT file gộp `{PACK / GROUP_FILE}` (c02–c09 một thể, {len(group)} ảnh: "
                  f"{', '.join(group)}; mỗi bước một ảnh, lưu riêng), rồi nhắn Claude \"duyệt troi c02–c09\". Sau đó m20–m60, "
                  f"b70a (file lẻ), cuối cùng b70b, b70c (dựng sau khi b70a duyệt)." if group else
                  "- **Bước tiếp:** các file lẻ còn lại trong bảng dưới (m20–m60, b70a; b70b, b70c dựng sau khi b70a duyệt).")
    return f"""# Gói gửi GPT: nối trời nền trận đảo Thủy (`troi`)

Sinh bằng `{HERE / 'build_troi.py'}`, đừng sửa tay (chạy lại script sẽ ghi đè).

## Tiến độ (script tự ghi lúc dựng gói)

- **Đã ghép, đã vào game:** {', '.join(ok) or 'chưa có'}. Code game (`StageView.FitBg`) đã thử trong Play ở 1080 × 2400 và 1080 × 1920 (2026-11-04).
- **Còn:** {', '.join(todo) or 'hết'}. Làm bằng GPT (người dùng chốt 2026-11-04: gen lại từng nền, không mượn trời c01 cho nền khác).
{group_line}
- **Đổi máy:** file prompt ghi đường dẫn tuyệt đối của máy dựng gói. Sang máy khác thì chạy lại `py -3 -I ArtGen/BattleBG/build_troi.py` trước khi gửi GPT.
- **Duyệt:** `py -3 -I ArtGen/BattleBG/build_troi.py --duyet <mã>` (ghép, ảnh soi `troi/soi_<mã>.png`), soi mép cũ phóng to; rồi `py -3 -I ArtGen/BattleBG/build_thuy.py --xuat` và Play thử "Đánh thử ải …" ở khung 1080 × 2400.

**Vì sao:** máy dài hơn 9:16 thì vùng sân trận cao hơn khung nền 1080 × 928 (máy 2960 × 1440 thêm 300, 20:9 thêm 480, 21:9 thêm 600), phần trên chỉ có màu trời trơn. Mỗi nền cũ cho GPT vẽ nối lên trên; game neo đáy ảnh vào đáy khung, máy dài thấy thêm trời, máy 9:16 cắt bớt (không đổi gì).

**Khung gửi GPT** (`khung_<mã>.png`, 1024 × 1536): 880 px dưới là nền trận cũ, 656 px trên để trắng. GPT vẽ lại cả khung; Claude chỉ lấy phần trên của GPT, phần dưới vẫn là ảnh cũ (khớp tỉ lệ, chỗ rồi nối theo đường ít lệch nhất), nên phần dưới GPT có lệch chút cũng không sao.

**Mỗi lượt chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn ảnh mẫu (GPT tự mở) và chỗ GPT lưu ảnh. GPT lưu xong thì nhắn Claude "duyệt troi <mã>" (vd `duyệt troi c01`); Claude ghép, soi rồi đưa vào game. Boss dạng 2, 3 (`b70b`, `b70c`) cần dạng 1 (`b70a`) đã duyệt, Claude dựng file prompt sau.

| Lượt | File prompt gửi GPT | Ảnh mẫu GPT mở (theo thứ tự) | GPT lưu ảnh vào |
|---|---|---|---|
{chr(10).join(rows)}

Bản ghép Claude lưu ở `{WORK}\\<mã>.png` (1080 × 1528: 600 trời thêm + khung 928), kèm ảnh soi `soi_<mã>.png`: bên trái ảnh sạch, bên phải có vạch chỗ từng loại máy bắt đầu thấy (9:16, 2960 × 1440, 20:9, 21:9) và đường nối (đỏ).

## Soi trước khi nhắn Claude

- Phần trên kín màu, không còn trắng, không viền, không khung.
- Không thấy mép cũ: trời liền màu, nét chì cùng hướng; vật bị mép cũ cắt (hải đăng, vách thác, đền, cột đá) được vẽ tiếp đúng chỗ, đúng bề ngang.
- Phần trên êm: chủ yếu là trời, không thêm địa danh, vật to sáng, sinh vật, chữ.
- Không vẽ tia đèn, mưa, sét, đinh ba (game tự cho chạy).
- Phần dưới giống ảnh cũ (cùng bố cục); lệch nhẹ không sao.

## Sửa nhanh (gõ vào chat)

| Lỗi | Gõ |
|---|---|
| Còn trắng hoặc có viền | `Same image, but fill the whole top part edge to edge: no white area, no margin, no frame.` |
| Thấy rõ mép cũ | `Same image, but make the sky continue seamlessly across the old top edge: same colours and same pencil hatching, no line or colour change there.` |
| Vật bị cắt không được vẽ tiếp | `Same image, but continue the [lighthouse / cliff and waterfall / temple dome / stone pillar] upward from the old top edge, same width and place.` |
| Phần trên rối, có vật mới to | `Same image, but keep the new top part calm: mostly sky with a few small clouds, no new landmark or big bright object.` |
| Vẽ lại lệch phần dưới | `Keep the bottom part exactly like image 1, same layout, same size and place; only paint the top part.` |
| Có tia đèn, mưa, sét | `Same image without the [light beam / rain / lightning]; the game adds them.` |
| Có chữ, số, sinh vật | `Same image without any text, numbers, creatures or people.` |
"""


def build():
    PACK.mkdir(parents=True, exist_ok=True)
    INBOX.mkdir(parents=True, exist_ok=True)
    for f in PACK.glob("*.txt"):
        f.unlink()
    built = []
    for n, i in enumerate(ORDER, 1):
        if not bt.approved(i).exists():
            print(f"  ! chưa có nền đã duyệt {bt.approved(i)}")
            continue
        canvas(i).save(PACK / f"khung_{i}.png")
        if not ready(i):
            continue
        name = f"{n:02d}_{i}.txt"
        (PACK / name).write_text(prompt(i), encoding="utf-8")
        built.append(name)
    if group_todo():
        (PACK / GROUP_FILE).write_text(group_prompt(group_todo()), encoding="utf-8")
        built.append(GROUP_FILE)
    (PACK / "HUONG_DAN.md").write_text(guide(), encoding="utf-8")
    print(f"Gói {PACK}: {len(built)} file prompt; {len(ORDER) - len(built)} lượt chờ ảnh duyệt")


# ---------- ghép ----------

def detail(im, r):
    """nét chi tiết (lọc dải): bỏ dải chuyển màu của trời, chỉ còn viền, mây, nét chì"""
    g = im.convert("L")
    return (np.asarray(g.filter(ImageFilter.GaussianBlur(r)), dtype=np.float32)
            - np.asarray(g.filter(ImageFilter.GaussianBlur(r * 6)), dtype=np.float32))


def warp(im, s, tx, ty, cx, cy, size=None, y0=0):
    """ảnh khớp với khung: điểm (x, y) của khung lấy từ (s(x-cx)+cx+tx, s(y-cy)+cy+ty) của ảnh GPT; size, y0: chỉ lấy dải
    dòng y0.. của khung"""
    return im.transform(size or im.size, Image.AFFINE, (s, 0, cx - s * cx + tx, 0, s, cy - s * cy + ty + s * y0),
                        Image.BICUBIC, fillcolor=(0, 0, 0))


def ncc(a, b):
    a = a - a.mean()
    b = b - b.mean()
    return float((a * b).sum() / (np.sqrt((a * a).sum() * (b * b).sum()) + 1e-6))


def align(gpt, ref, rows=400, keep=6):
    """tìm tỉ lệ, dịch khớp phần dưới ảnh GPT vào khung: so nét chi tiết của dải rows dòng ngay dưới mép cũ (nơi đường nối đi
    qua). Thô ở 1/4 cỡ (lưới tỉ lệ 0.94..1.06, dịch ±40 px), giữ keep chỗ tốt nhất cách xa nhau (ở 1/4 cỡ chỗ sai có khi điểm
    cao hơn chỗ đúng), mỗi chỗ leo dốc ở cỡ thật; trả (điểm, tỉ lệ, dịch x, dịch y) tốt nhất ở cỡ thật"""
    cx, cy = CW / 2, TOP
    k = 4
    small_g = gpt.resize((CW // k, CH // k), Image.BOX)
    band = (CW // k, rows // k)
    small_r = detail(ref.resize((CW // k, CH // k), Image.BOX).crop((0, TOP // k, CW // k, (TOP + rows) // k)), 1)
    coarse = []
    for s in np.arange(0.94, 1.0601, 0.01):
        for tx in range(-40, 41, 4):
            for ty in range(-40, 41, 4):
                w = detail(warp(small_g, s, tx / k, ty / k, cx / k, cy / k, band, TOP // k), 1)
                coarse.append((ncc(w, small_r), round(float(s), 3), tx, ty))
    coarse.sort(reverse=True)
    starts = []
    for c in coarse:
        if all(abs(c[1] - o[1]) > 0.015 or abs(c[2] - o[2]) > 8 or abs(c[3] - o[3]) > 8 for o in starts):
            starts.append(c)
        if len(starts) == keep:
            break
    big_r = detail(ref.crop((0, TOP, CW, TOP + rows)), 2)
    seen = {}

    def score(p):
        if p not in seen:
            seen[p] = ncc(detail(warp(gpt, p[0], p[1], p[2], cx, cy, (CW, rows), TOP), 2), big_r)
        return seen[p]

    best = (-2, 1, 0, 0)
    for _, s, tx, ty in starts:
        p = (s, tx, ty)
        for ds, dt in ((0.01, 4), (0.004, 2), (0.002, 1)):
            moved = True
            while moved:
                moved = False
                for q in ((p[0] + ds, p[1], p[2]), (p[0] - ds, p[1], p[2]), (p[0], p[1] + dt, p[2]), (p[0], p[1] - dt, p[2]),
                          (p[0], p[1], p[2] + dt), (p[0], p[1], p[2] - dt)):
                    q = (round(q[0], 3), q[1], q[2])
                    if score(q) > score(p):
                        p, moved = q, True
        if score(p) > best[0]:
            best = (score(p), *p)
    return best


def seam(cost):
    """đường nối ngang ít lệch nhất trong dải (mỗi cột một dòng, cột kề lệch tối đa 1 dòng)"""
    h, w = cost.shape
    acc = cost.copy()
    back = np.zeros((h, w), dtype=np.int8)
    for x in range(1, w):
        prev = acc[:, x - 1]
        up = np.r_[np.inf, prev[:-1]]
        down = np.r_[prev[1:], np.inf]
        stack = np.vstack([up, prev, down])
        arg = stack.argmin(axis=0)
        acc[:, x] += stack[arg, np.arange(h)]
        back[:, x] = arg - 1
    path = np.zeros(w, dtype=int)
    path[-1] = int(acc[:, -1].argmin())
    for x in range(w - 1, 0, -1):
        path[x - 1] = path[x] + back[path[x], x]
    return path


def compose(i, src):
    with Image.open(src) as im:
        gpt = im.convert("RGB")
    if gpt.size != (CW, CH):
        print(f"  ! {Path(src).name} cỡ {gpt.size}, cần {CW} x {CH}: thu về")
        gpt = gpt.resize((CW, CH), Image.LANCZOS)
    v, s, tx, ty = align(gpt, canvas(i))
    print(f"  khớp: tương quan {v:.3f}, tỉ lệ {s:.3f}, dịch ({tx}, {ty}) px")
    if v < 0.3:
        print("  ! khớp kém: phần dưới GPT vẽ khác ảnh cũ nhiều, soi kỹ đường nối")
    cx, cy = CW / 2, TOP
    # GPT vẽ to hơn hay lệch thì mép ảnh khớp hụt vài px: kéo dài mép ảnh GPT (PAD px) trước khi biến đổi
    pad = 64
    padded = Image.fromarray(np.pad(np.asarray(gpt), ((pad, pad), (pad, pad), (0, 0)), mode="edge"))
    al = warp(padded, s, tx + pad, ty + pad, cx, cy, (CW, CH))
    hole = np.asarray(warp(Image.new("RGB", gpt.size, "white"), s, tx, ty, cx, cy).convert("L")) < 128
    sc = bt.FW / CW
    seam_y = round(TOP * sc)  # 692: mép cũ trên bản 1080 x 1620
    tall = al.resize((bt.FW, round(CH * sc)), Image.LANCZOS)
    cut = seam_y - EXTRA  # bỏ phần trên cùng thừa
    kept = hole[round(cut / sc):TOP]  # phần GPT giữ lại (theo khung 1024)
    side = max(kept.sum(axis=1).max(initial=0), kept[:, CW // 3:2 * CW // 3].sum(axis=0).max(initial=0))  # rộng hụt hai bên, cao hụt trên
    if side > 12:
        print(f"  ! ảnh GPT lệch nhiều: {side} px ở mép bản ghép là mép ảnh GPT kéo dài, soi kỹ hai bên")
    t = np.asarray(tall, dtype=np.float32)
    return stitch(t[cut:seam_y + BAND], np.asarray(bt.frame_of(i), dtype=np.float32))


def stitch(top, o):
    """top: lớp trời mới, dòng 0..EXTRA+BAND của bản cuối (dải BAND dưới cùng chồng lên khung cũ); o: khung cũ 1080 x 928.
    Nối theo đường ít lệch nhất trong dải chồng, mờ mép FEATHER, khử vạch ở mép cũ; trả (ảnh, đường nối)"""
    band_t = top[EXTRA:EXTRA + BAND]
    band_o = o[:BAND]
    cost = np.abs(np.asarray(Image.fromarray(band_t.astype(np.uint8)).filter(ImageFilter.GaussianBlur(2)), dtype=np.float32)
                  - np.asarray(Image.fromarray(band_o.astype(np.uint8)).filter(ImageFilter.GaussianBlur(2)), dtype=np.float32)
                  ).sum(axis=2)
    cost += np.arange(BAND, dtype=np.float32)[:, None] * 0.3  # lệch ngang nhau thì giữ ảnh cũ nhiều hơn
    cost[:FEATHER + 2] = cost[-(FEATHER + 2):] = 1e6
    path = seam(cost)
    rows = np.arange(BAND)[:, None]
    m = (rows < path[None, :]).astype(np.float32)  # 1: lấy lớp trời mới
    m = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(FEATHER / 2)),
                   dtype=np.float32)[..., None] / 255
    out = np.empty((FULL, bt.FW, 3), dtype=np.float32)
    out[:EXTRA] = top[:EXTRA]
    out[EXTRA:EXTRA + BAND] = band_t * m + band_o * (1 - m)
    out[EXTRA + BAND:] = o[BAND:]
    unline(out)
    res = Image.fromarray(np.clip(out + 0.5, 0, 255).astype(np.uint8))
    return res, path


def unline(out, rise=80):
    """GPT giữ nguyên phần dưới thì ảnh GPT có mép riêng ngay ở mép cũ (dòng EXTRA): phần vẽ thêm lệch độ sáng 1, 2 mức, nét chì
    đứt ngang thành một vạch mờ. Bù độ sáng phần trên cho khớp ảnh cũ (một mức chung cả hàng, trung vị, nhạt dần lên trên trong
    rise dòng), rồi làm mềm ±3 dòng quanh mép. GPT vẽ lại cả ảnh thì mức bù gần 0, không hại."""
    e = EXTRA
    off = np.clip(np.median(out[e:e + 6] - out[e - 6:e][::-1], axis=(0, 1)), -8, 8)
    out[e - rise:e] += off[None, None] * ((np.arange(rise) + 1) / rise)[:, None, None]
    band = out[e - 6:e + 6].copy()
    k = (0.1, 0.2, 0.4, 0.2, 0.1)
    soft = sum(k[i] * np.roll(band, i - 2, axis=0) for i in range(5))
    w = np.array([0, 0, 0.3, 0.6, 0.9, 1, 1, 0.9, 0.6, 0.3, 0, 0], dtype=np.float32)[:, None, None]
    # né nét mực (viền mây, vật vắt qua mép): làm mềm nét ngang thì nét nhạt đi một khúc
    ink = Image.fromarray(((band.mean(axis=2) < 150) * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(7))
    w = w * (1 - np.asarray(ink.filter(ImageFilter.GaussianBlur(1.5)), dtype=np.float32)[..., None] / 255)
    out[e - 6:e + 6] = band * (1 - w) + soft * w


def soi(im, path):
    """trái ảnh sạch; phải vạch chỗ từng loại máy bắt đầu thấy và đường nối"""
    marked = im.copy()
    d = ImageDraw.Draw(marked)
    for extra, label in SHOWS:
        y = EXTRA - extra
        d.line([(0, y), (bt.FW, y)], fill=(255, 0, 255), width=4)
        d.rectangle((8, y + 6, 8 + 9 * len(label) + 12, y + 30), fill=(255, 0, 255))
        d.text((14, y + 10), label, fill="white")
    d.line([(x, EXTRA + int(p)) for x, p in enumerate(path)], fill=(255, 0, 0), width=2)
    out = Image.new("RGB", (bt.FW * 2 + 20, FULL), "white")
    out.paste(im, (0, 0))
    out.paste(marked, (bt.FW + 20, 0))
    return out


def approve(i, src):
    if i not in ORDER:
        sys.exit(f"không có mã {i}; các mã: {', '.join(ORDER)}")
    if src is None:
        found = sorted(INBOX.glob(f"{i}*.png"), key=lambda p: p.stat().st_mtime)
        found = [p for p in found if p.stem == i or p.stem.startswith(i + "_")]
        if not found:
            sys.exit(f"chưa có ảnh {INBOX / (i + '.png')}")
        src = found[-1]
    print(f"Ghép {i}: {src}")
    im, path = compose(i, src)
    WORK.mkdir(parents=True, exist_ok=True)
    im.save(done(i))
    soi(im, path).save(WORK / f"soi_{i}.png")
    print(f"  -> {done(i)} ({im.width} x {im.height}), ảnh soi {WORK / f'soi_{i}.png'}")
    print("  đưa vào game: py -3 -I ArtGen/BattleBG/build_thuy.py --xuat")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--duyet", nargs="+", metavar=("MA", "ANH"), help="ghép ảnh GPT của lượt <mã> (mặc định ảnh mới nhất)")
    args = ap.parse_args()
    if args.duyet:
        approve(args.duyet[0], args.duyet[1] if len(args.duyet) > 1 else None)
    build()
