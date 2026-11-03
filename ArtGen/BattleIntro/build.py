# Màn VS kiểu trang truyện tranh và dải tuyệt kỹ (Unity: BattleIntro, UltCutIn; người dùng chốt 2026-11-03): gói gửi GPT.
# - Lượt 1: nền khung truyện dùng chung (tia tập trung, một màu giấy và mực; game cắt thành hai khung chéo và tô đỏ, xanh theo phe).
# - Lượt 2: dấu "VS" (hình nổ và chữ, nền trắng, game cắt nền).
# - Mặt tướng: mỗi dòng tiến hóa một file, mỗi dạng một bước; ảnh mẫu là chân dung dạng đó trong game. Lính của ải chung một file.
#   Mặt quay sang trái người xem; game lật cho phe mình.
# Ghi: gui_gpt/ (file prompt, HUONG_DAN.md), refs/mat/<aola>.png (chân dung trong game phóng 2 lần trên nền trắng).
# GPT lưu ảnh vào tai_ve/ (vs_nen.png, vs_no.png, mat/<aola>.png).
# Chạy: py -3 -I ArtGen/BattleIntro/build.py
# Duyệt ảnh GPT đã lưu (mặc định ảnh mới nhất trong tai_ve), chép vào Unity rồi dựng lại gói:
#   py -3 -I ArtGen/BattleIntro/build.py --duyet nen [ảnh]
#   py -3 -I ArtGen/BattleIntro/build.py --duyet vs [ảnh]
#   py -3 -I ArtGen/BattleIntro/build.py --duyet mat <aola hoặc mã tướng> [ảnh]
# Ảnh vào Assets/03 Art/BattleIntro/Resources/: BattleIntro/vs_nen.png, BattleIntro/vs_no.png, HeroFaces/mat_<aola>.png (game nạp khi
# cần: BattleIntro.ArtBg, ArtVs, HeroArt.Face). Nền trắng nối với mép được cắt thành trong suốt (dấu VS, mặt).
import argparse
import json
import sys
from collections import deque
from pathlib import Path

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent  # ArtGen/BattleIntro
ART = HERE.parent
ROOT = ART.parent
PACK = HERE / "gui_gpt"
REFS = HERE / "refs"
INBOX = HERE / "tai_ve"
UNITY = ROOT / "Assets" / "03 Art" / "BattleIntro" / "Resources"
WORLD = ART / "Islands" / "refs" / "world_style.png"
CARDS = ART / "StyleRefs" / "R1_UI_Cards.png"
SHOT = REFS / "man_vs_hien_tai.png"  # ảnh chụp màn VS trong game (nền tia vẽ bằng code), chép từ vòng thử
HEROES_JSON = ROOT / "Assets" / "02 Data" / "Json" / "heroes.json"
PORTRAITS = ROOT / "Assets" / "03 Art" / "Heroes" / "Resources"

ELEM_VI = {"kim": "Kim", "moc": "Mộc", "thuy": "Thủy", "hoa": "Hỏa", "tho": "Thổ"}
ORDER = ["thuy", "kim", "moc", "hoa", "tho"]  # đảo Thủy (70 ải) đang chơi trước

HEAD = ("Read this whole file. Then open the reference images listed below from their full paths, draw {what} and save {how}. "
        "Do not reply with text only.")

# luật chung ArtGen/README.md (người dùng dặn 2026-11-03): UI và tướng không vẽ bóng
NO_SHADOWS = ("NO SHADOWS: no drop shadow, no hard offset shadow, no cast shadow, no shadow under the feet or on the ground or "
              "background. Shade only with colour-pencil hatching inside the shapes; the game adds shadows itself where needed.")

STYLE = ("STYLE (image 1): the hand-drawn storybook look of this game: slightly wobbly dark-brown ink outlines #2B2118, flat warm "
         "colours, light colour-pencil hatching for shading, cream paper feel. Drawn neatly by a professional illustrator, not "
         "scribbly. No glossy highlights, no gradients, no 3D render, no airbrush.")


def save_rule(p):
    return (f"save it as a PNG to {p} (create the folder if it is missing; if that file already exists, add _2, _3 … before "
            f".png). Do not change, move or delete any other file.")


def refs_block(refs):
    out = ["REFERENCE IMAGES (open each file from its full path):"]
    for i, (p, en, _) in enumerate(refs, 1):
        sz = Image.open(p).size if Path(p).exists() else None
        out.append(f"image {i} = {p}" + (f" ({sz[0]} x {sz[1]})" if sz else "") + f": {en}")
    return out


def write(path, lines):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------- dữ liệu tướng ----------

def lines_of_heroes():
    d = json.loads(HEROES_JSON.read_text(encoding="utf-8"))
    starters = d.get("starters", [])
    heroes = sorted(d["heroes"], key=lambda h: (h["id"] not in starters, ORDER.index(h["elem"]), d["heroes"].index(h)))
    out = []
    for h in heroes:
        forms = [(f["aola"], f["name"]) for f in h.get("forms", [])] or [(h["aola"], h["name"])]
        out.append({"id": h["id"], "name": h["name"], "elem": h["elem"], "forms": forms, "starter": h["id"] in starters})
    minions = d.get("minions", [])
    if minions:
        out.append({"id": "linh", "name": "Lính của ải", "elem": minions[0]["elem"], "starter": False,
                    "forms": [((m.get("forms") or [{"aola": m["aola"]}])[0]["aola"], m["name"]) for m in minions]})
    return out


def portrait_ref(aola):
    """chân dung trong game (384 x 480, nền trong) phóng 2 lần trên nền trắng -> refs/mat/<aola>.png"""
    src = PORTRAITS / aola / f"{aola}_portrait.png"
    dst = REFS / "mat" / f"{aola}.png"
    if not src.exists():
        return None
    if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
        im = Image.open(src).convert("RGBA")
        im = im.resize((im.width * 2, im.height * 2), Image.LANCZOS)
        bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
        bg.alpha_composite(im)
        dst.parent.mkdir(parents=True, exist_ok=True)
        bg.convert("RGB").save(dst)
    return dst


def face_out(aola):
    return UNITY / "HeroFaces" / f"mat_{aola}.png"


# ---------- lượt 1, 2 ----------

def refs_nen():
    r = [(WORLD, "style reference only: the game's hand-drawn world map (ink lines, colour-pencil hatching on cream paper)",
          "bản đồ thế giới của game (1024 × 1536): bốn đảo vẽ tay, viền mực nâu, tô sáp màu: chỉ để học nét")]
    if SHOT.exists():
        r.append((SHOT, "how the game uses the background: the versus screen with the game's placeholder lines inside the two "
                        "slanted comic panels (red enemy panel on top, blue player panel at the bottom)",
                  "ảnh chụp màn VS trong game hiện giờ: hai khung chéo đỏ, xanh, tia vẽ tạm bằng code, ô mặt tướng"))
    return r


def prompt_nen():
    refs = refs_nen()
    out = [HEAD.format(what="ONE image", how="it as described under SAVE"), ""] + refs_block(refs)
    out += ["", "SAVE: " + save_rule(INBOX / "vs_nen.png"), ""]
    use = ("Image 2 shows where it goes: the game currently draws plain placeholder lines there" if len(refs) > 1 else
           "The game currently draws plain placeholder lines there")
    out += [
        "WHAT THIS IS: the background texture inside the comic panels of the \"versus\" screen of a cute hand-drawn mobile game. "
        "The game crops this one square into two slanted comic panels (the enemy team on top, the player team at the bottom) "
        f"and tints it: red for the enemy panel, blue for the player panel. The heroes' face cards sit in the middle. {use}; "
        "your image replaces them.",
        "",
        "DRAW: a square 1024 x 1024 manga \"focus lines\" background: speed lines radiating from the centre out to all four edges, "
        "like the dramatic concentration lines behind a hero in a comic. Mostly thin lines with a few longer, bolder strokes; "
        "soft colour-pencil hatching between some lines and a sprinkle of halftone dots toward the corners.",
        "",
        "CENTRE: keep a calm round area about 560 px across in the middle as plain paper with at most a few very faint lines: the "
        "face cards cover it.",
        "",
        "DENSITY: the lines cover about a quarter of the area, so the panel stays light and the faces stand out.",
        "",
        "COLOURS: only cream paper #FBF4E2, warm grey #B9AA90 for most lines and hatching, and dark-brown ink #2B2118 for a few "
        "accent strokes. No other colour at all: the game tints the whole image.",
        "",
        "EDGES: the lines run off all four edges. No frame, no border, no panel edge, no white margin.",
        "",
        STYLE,
        "",
        "AVOID: characters, faces, text, letters, \"VS\", symbols, explosions, glow, colour, gradients, photo texture, 3D.",
    ]
    return refs, out


def refs_vs():
    return [(WORLD, "style reference only: the game's hand-drawn world map (ink lines, colour-pencil hatching on cream paper)",
             "bản đồ thế giới của game: chỉ để học nét"),
            (CARDS, "the game's hand-drawn interface: see the chunky rounded title lettering with ink outlines (\"Sổ thẻ\" on top)",
             "màn Sổ thẻ bản web (540 × 960): học kiểu chữ tiêu đề tròn, mập, viền mực")]


def prompt_vs():
    refs = refs_vs()
    out = [HEAD.format(what="ONE image", how="it as described under SAVE"), ""] + refs_block(refs)
    out += ["", "SAVE: " + save_rule(INBOX / "vs_no.png"), ""]
    out += [
        "WHAT THIS IS: the \"VS\" sign of the versus screen of a cute hand-drawn mobile game. The game stamps it in the middle of "
        "the slanted gap between the enemy panel (top, red) and the player panel (bottom, blue), about 430 px wide on a phone.",
        "",
        "DRAW, centred on a square 1024 x 1024 canvas with a plain pure white background:",
        "- a jagged comic explosion burst with 12 to 14 sharp, uneven points like hand-cut paper: yellow #F7C948, lighter in the "
        "middle, orange #F39A2D toward the tips, a thick dark-brown ink outline (about 14 px) and colour-pencil hatching;",
        "- on top of it the two letters \"V\" and \"S\", hand-lettered, chunky and rounded like the titles in image 2: red "
        "#E8553F, a thick ink outline (about 16 px), one short white highlight stroke on each letter; the \"S\" sits a little lower than the \"V\"; the whole word tilted about 8 degrees "
        "counter-clockwise.",
        "Spell exactly V then S. No other text.",
        "",
        "SIZE: the burst fills about 80% of the canvas width; nothing touches the edges.",
        "",
        STYLE,
        "",
        NO_SHADOWS,
        "",
        "AVOID: other letters or words, an exclamation mark, characters, lightning, glow, glossy shine, gradients, 3D bevel, a "
        "frame, any shadow, a coloured background.",
    ]
    return refs, out


# ---------- mặt tướng ----------

FACE_RULES = [
    "FOR EVERY STEP:",
    "- Draw the SAME creature as that step's reference image: same species, head shape, ears, horns, crest, hair, colours, "
    "markings, eye colour and head accessories (helmet, headband, hat...). Do not invent a new design and do not add anything.",
    "- Redraw it in the style of image 1 (see STYLE). Outline about 9 px thick on this canvas.",
    "- Close-up portrait: head and the top of the shoulders only; the bottom edge of the square cuts across the chest. The head "
    "fills about 80% of the canvas height; the top of the head (ears, horns, crest) stays inside the canvas with a small "
    "margin; the eyes at about the middle of the canvas height.",
    "- Three-quarter view turned towards the viewer's LEFT: the face and the eyes look to the left side of the image. If the "
    "reference looks to the right, mirror it.",
    "- Expression: determined and ready to fight: brows lowered, eyes focused, mouth closed in a confident grin or a firm line "
    "(fangs only if the design has them). Brave and cute; not angry, not scary, not goofy.",
    "- A square 1024 x 1024 canvas with a plain pure white background. No sticker border or white outline around the head, no "
    "shadow, no frame, no text, no effects; no hands or weapons in front of the face.",
]


def face_file(n, line):
    steps = [(aola, name, portrait_ref(aola)) for aola, name in line["forms"]]
    steps = [s for s in steps if s[2] is not None]
    refs = [(WORLD, "style reference only: the game's hand-drawn world map (ink lines, colour-pencil hatching on cream paper)",
             "bản đồ thế giới của game: chỉ để học nét")]
    for aola, name, ref in steps:
        refs.append((ref, f"the creature \"{name}\" as it looks in the game now (full body, white background)",
                     f"chân dung {name} trong game (768 × 960, nền trắng, cả con)"))
    many = len(steps) > 1
    what = "ONE image per reply" if many else "ONE image"
    how = "each one as its step says" if many else "it as its step says"
    out = [HEAD.format(what=what, how=how), ""] + refs_block(refs)
    out += ["", f"SAVE: every step's image goes into {INBOX / 'mat'} under the name that step gives. If that file already exists, "
                "add _2, _3 … before .png. Do not change, move or delete any other file.", ""]
    kind = ("the minions of the islands (each step is a different creature)" if line["id"] == "linh" else
            f"one creature, \"{line['name']}\", in each of its evolution forms (one step per form)")
    out += [f"WHAT THIS IS: face icons for a cute hand-drawn mobile game: {kind}. The game shows each face inside a small square "
            "comic frame on the versus screen before a battle, and big inside a wide slanted comic strip when the creature uses "
            "its ultimate move.", "", STYLE, "", NO_SHADOWS, ""]
    out += FACE_RULES + [""]
    if many:
        out += [f"ORDER: draw step 1 now, save it and stop. When I say \"next\", draw the next step, save it and stop, until step "
                f"{len(steps)}.", ""]
    for i, (aola, name, _) in enumerate(steps, 1):
        out += [f"=== STEP {i}: {name} ===",
                f"Reference: image {i + 1}." + (f" Same creature line as the other steps, so keep the family look; this form "
                                                 f"is stage {i} of {len(steps)}." if many and line["id"] != "linh" else ""),
                f"SAVE this step: {save_rule(INBOX / 'mat' / (aola + '.png'))}", ""]
    name = f"{n:02d}_{line['id']}.txt"
    write(PACK / "mat" / name, out)
    return PACK / "mat" / name, refs, steps


# ---------- duyệt ----------

def latest(pattern, base=INBOX):
    files = sorted(base.glob(pattern), key=lambda p: p.stat().st_mtime)
    return files[-1] if files else None


def cut_white(im, thr=238, soft=26):
    """nền trắng nối với mép -> trong suốt; mép nửa trong suốt tính từ độ trắng"""
    im = im.convert("RGBA")
    w, h = im.size
    px = im.load()
    lo = thr - soft
    seen = bytearray(w * h)
    q = deque()
    for x in range(w):
        q.append((x, 0))
        q.append((x, h - 1))
    for y in range(h):
        q.append((0, y))
        q.append((w - 1, y))
    while q:
        x, y = q.popleft()
        i = y * w + x
        if seen[i]:
            continue
        r, g, b, a = px[x, y]
        m = min(r, g, b)
        if m < lo:
            continue
        seen[i] = 1
        px[x, y] = (r, g, b, 0 if m >= thr else int(255 * (thr - m) / soft))
        if x > 0:
            q.append((x - 1, y))
        if x < w - 1:
            q.append((x + 1, y))
        if y > 0:
            q.append((x, y - 1))
        if y < h - 1:
            q.append((x, y + 1))
    return im


def approve(kind, key, src):
    if kind == "nen":
        src = Path(src) if src else latest("vs_nen*.png")
        dst = UNITY / "BattleIntro" / "vs_nen.png"
        im = Image.open(src).convert("RGB").resize((1024, 1024), Image.LANCZOS)
    elif kind == "vs":
        src = Path(src) if src else latest("vs_no*.png")
        dst = UNITY / "BattleIntro" / "vs_no.png"
        im = cut_white(Image.open(src))
        box = im.getchannel("A").getbbox()
        im = im.crop((max(0, box[0] - 8), max(0, box[1] - 8), min(im.width, box[2] + 8), min(im.height, box[3] + 8)))
    else:
        aola = key
        for line in lines_of_heroes():
            if line["id"] == key:
                aola = line["forms"][0][0]
        src = Path(src) if src else latest(f"{aola}*.png", INBOX / "mat")
        dst = face_out(aola)
        im = cut_white(Image.open(src)).resize((512, 512), Image.LANCZOS)
    if not src or not Path(src).exists():
        raise SystemExit(f"Không thấy ảnh để duyệt ({kind} {key or ''}).")
    dst.parent.mkdir(parents=True, exist_ok=True)
    im.save(dst)
    print(f"Duyệt {src} -> {dst} ({im.width} x {im.height}). Mở Unity (tự nhập ảnh), vào trận xem màn VS.")


# ---------- hướng dẫn ----------

def guide(nen, vs, faces):
    def ref_rows(refs):
        return [f"| {i} | `{p}` | {vi} |" for i, (p, _, vi) in enumerate(refs, 1)]

    def done(p):
        return "đã có trong game" if p.exists() else "chưa có"

    g = ["# Gói gửi GPT: màn VS truyện tranh và dải tuyệt kỹ", "",
         f"Sinh bằng `{HERE / 'build.py'}`, đừng sửa tay (chạy lại script sẽ ghi đè).", "",
         "Trong game (Unity):",
         "- màn VS đầu trận là một trang truyện tranh: khung trên là đội địch (đỏ), khung dưới là đội bạn (xanh), ngăn bằng khe "
         "chéo; mỗi tướng một ô mặt, có lực chiến cả đội, chữ VS nổ giữa khe;",
         "- khi ra tuyệt kỹ, khung đó cắt thành dải hình bình hành ngang sân, có mặt tướng ra chiêu và tên chiêu.", "",
         "Chưa có ảnh thì game vẽ tạm (tia bằng code, hình nổ của bộ giấy, chân dung cắt ngang thân). Có ảnh nào thì game tự dùng "
         "ảnh đó.", "",
         "**Mỗi lượt chỉ gửi GPT đường dẫn file prompt.** File ghi sẵn đường dẫn đầy đủ của từng ảnh mẫu (GPT tự mở) và chỗ GPT "
         f"lưu ảnh (`{INBOX}`). Xong một ảnh thì nhắn Claude \"duyệt nền\", \"duyệt vs\" hoặc \"duyệt mặt <mã tướng>\". Claude "
         "cắt nền và chép vào game; tự làm được bằng lệnh ở cuối file.", "",
         "## Lượt 1: nền khung truyện (dùng chung mọi trận, mọi phe)", "",
         f"File prompt: `{nen[0]}`. GPT lưu `{INBOX / 'vs_nen.png'}`. Trong game: {done(UNITY / 'BattleIntro' / 'vs_nen.png')}.", "",
         "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"] + ref_rows(nen[1]) + [
         "",
         "Soi: vuông 1024; tia tỏa từ giữa ra bốn mép; giữa trống một vòng tròn to; chỉ màu giấy kem, xám ấm, vài nét mực nâu "
         "(game tô đỏ hoặc xanh); không khung viền, không chữ, không nhân vật.", "",
         "## Lượt 2: dấu VS", "",
         f"File prompt: `{vs[0]}`. GPT lưu `{INBOX / 'vs_no.png'}`. Trong game: {done(UNITY / 'BattleIntro' / 'vs_no.png')}.", "",
         "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"] + ref_rows(vs[1]) + [
         "",
         "Soi: hình nổ vàng cam viền mực, chữ V S đỏ viền mực, đúng hai chữ; không bóng đổ (luật chung); nền trắng tinh; không chạm mép.", "",
         "## Mặt tướng (mỗi dòng tiến hóa một file, mỗi dạng một bước)", "",
         "Ảnh mẫu 1 của mọi file là bản đồ thế giới (học nét); ảnh mẫu 2 trở đi là chân dung từng dạng trong game, phóng "
         f"768 × 960 trên nền trắng (`{REFS / 'mat'}`). GPT lưu `{INBOX / 'mat'}\\<aola>.png`. Một file nhiều dạng: GPT vẽ bước 1 "
         "rồi dừng; gõ `next` để vẽ bước sau.", "",
         "Nên làm trước: tướng khởi đầu, tướng và lính đảo Thủy (đang chơi). Tướng sẽ vẽ lại hình (QUY_TRINH của Heroes) thì để "
         "sau khi có hình mới rồi chạy lại script (ảnh mẫu lấy theo chân dung trong game lúc đó).", "",
         "| File | Tướng | Hệ | Dạng (aola: trong game?) |", "|---|---|---|---|"]
    for path, line, steps in faces:
        forms = "; ".join(f"{name} (`{aola}`: {'có' if face_out(aola).exists() else 'chưa'})" for aola, name, _ in steps)
        tag = " (khởi đầu)" if line["starter"] else ""
        g.append(f"| `{path}` | {line['name']}{tag} | {ELEM_VI.get(line['elem'], line['elem'])} | {forms} |")
    g += ["",
          "Soi mặt: đúng con trong ảnh mẫu (màu, tai, sừng, mũ...); đầu và vai, mép dưới cắt ngang ngực; đầu chiếm gần hết chiều "
          "cao, đỉnh đầu không chạm mép; quay sang **trái**; mặt quả quyết, sẵn sàng đánh, không dữ; nét vẽ tay như bản đồ; nền "
          "trắng tinh, không viền trắng quanh đầu, không bóng đổ (luật chung: UI và tướng không vẽ bóng).", "",
          "## Sửa nhanh (gõ vào chat)", "",
          "| Lỗi | Gõ |", "|---|---|",
          "| Nền có màu | `Same image but only cream paper, warm grey and a little dark-brown ink: no other colour.` |",
          "| Nền rối, che mặt tướng | `Same image with fewer, thinner lines and a bigger plain area in the middle.` |",
          "| Nền có khung, viền | `Same image without any frame or border: the lines run off all four edges.` |",
          "| Chữ VS sai, thừa chữ | `Redraw it with exactly two letters, V then S, and nothing else written.` |",
          "| VS chạm mép | `Same sign a little smaller, centred, with white space all around.` |",
          "| Mặt khác con trong ảnh mẫu | `Keep exactly the creature of the reference image: same head shape, colours, ears and "
          "markings. Only change the pose to a close-up face.` |",
          "| Mặt quay phải | `Mirror it so the face looks to the viewer's left.` |",
          "| Lấy cả thân, đầu nhỏ | `Closer: only the head and the top of the shoulders, the head filling most of the square.` |",
          "| Mặt dữ quá hoặc ngố | `Same face, but brave and cute: brows a little lowered, a confident small grin.` |",
          "| Bóng loáng kiểu 3D | `Redraw it in the hand-drawn style of image 1: wobbly ink outline, flat colours, pencil "
          "hatching, no shine.` |",
          "| Có viền trắng, nền xám | `Same image on a plain pure white background, without a white outline around the head.` |",
          "| Có bóng đổ, bóng lệch, bóng in xuống nền | `Same image without any shadow: no drop shadow, no offset shadow, nothing on "
          "the background. Keep only the pencil hatching inside the shapes.` |",
          "",
          "## Lệnh (Claude chạy khi bạn nhắn duyệt)", "",
          "```",
          "py -3 -I ArtGen/BattleIntro/build.py --duyet nen",
          "py -3 -I ArtGen/BattleIntro/build.py --duyet vs",
          "py -3 -I ArtGen/BattleIntro/build.py --duyet mat <aola hoặc mã tướng>",
          "```",
          "Ảnh vào `Assets/03 Art/BattleIntro/Resources/`; mở lại Unity cho nó nhập, vào trận xem."]
    write(PACK / "HUONG_DAN.md", g)


def build():
    refs, lines = prompt_nen()
    write(PACK / "luot_1_nen.txt", lines)
    nen = (PACK / "luot_1_nen.txt", refs)
    refs, lines = prompt_vs()
    write(PACK / "luot_2_vs.txt", lines)
    vs = (PACK / "luot_2_vs.txt", refs)
    faces = []
    for n, line in enumerate(lines_of_heroes(), 1):
        path, _, steps = face_file(n, line)
        faces.append((path, line, steps))
    guide(nen, vs, faces)
    print(f"Gói: {PACK} (2 lượt nền và VS, {len(faces)} file mặt, {sum(len(f[2]) for f in faces)} dạng).")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--duyet", nargs="+", metavar="X", help="nen [ảnh] | vs [ảnh] | mat <aola hoặc mã tướng> [ảnh]")
    a = ap.parse_args()
    if a.duyet:
        kind = a.duyet[0]
        if kind == "mat":
            if len(a.duyet) < 2:
                raise SystemExit("--duyet mat <aola hoặc mã tướng> [ảnh]")
            approve(kind, a.duyet[1], a.duyet[2] if len(a.duyet) > 2 else None)
        elif kind in ("nen", "vs"):
            approve(kind, None, a.duyet[1] if len(a.duyet) > 1 else None)
        else:
            raise SystemExit("--duyet nen | vs | mat")
    build()


if __name__ == "__main__":
    main()
