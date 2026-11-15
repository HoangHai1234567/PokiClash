# -*- coding: utf-8 -*-
"""Viêm Đao DẠNG 1 (quỷ lửa con chibi vác đao; mã quy_dao_non, suất giap_long = tướng thứ 7 đảo Hỏa).

Người dùng 2026-11-14 (máy ổ D): "làm dạng 1 cho tướng thứ 7 đảo hỏa" → xem hai concept → "làm đi" (theo đề xuất B của Claude):
concept chốt inbox/quy_dao_non/tai_ve/L1_duyet.png (= L1_tron_hon.png).

Cùng bộ xương, cùng 9 clip với dạng 2 (quy_dao_rig.py, chế độ QD_NON=1). Khác dạng 2:
- ĐẦU là một quả cầu mặt nạ to (gần nửa chiều cao thân), hai SỪNG MẦM, BA búi lửa nhỏ sau đầu, KHÔNG râu lửa, giáp vai vòm KHÔNG gai,
  đao bè hơn. Thân, tay, chân, khố: dùng lại da dạng 2 (cùng loài, cùng màu; trên concept phần này gần như khuất sau đầu + giáp vai).
- Mảnh đổi dáng: đầu, đao = GPT vẽ lại "đúng chỗ, đúng cỡ" từ concept (tờ N_DAU, N_DAO); ba búi lửa = GPT vẽ rời từng búi (tờ N_LUA);
  giáp vai, hai sừng mầm = cắt thẳng từ concept (nằm trên cùng, không bị che).
- Chỗ đặt: MỘT phép đồng dạng concept → rig (hai mốc trên trục đao: tâm khâu tròn, mũi đao ↔ trục xương vũ khí của rig), mọi mảnh
  đặt theo nó; xương sừng, gốc ba chuỗi xương lửa dời tới đúng chỗ mảnh (mau/dang.json, quy_dao_rig đọc ở chế độ non).

    quy_dao_non.py prompt        ba file prompt gui_gpt/quy_dao_non/luot_2_manh_<DAU|DAO|LUA>.txt (+ HUONG_DAN_manh.md)
    quy_dao_non.py cat           cắt tờ đã gen + cắt concept + bóp thon tay xa → inbox/quy_dao_non/manh/*.png, dat_moi.json; mau/dang.json
    quy_dao_non.py so            dáng đứng rig chồng lên concept → inbox/quy_dao_non/so_concept.png
    quy_dao_non.py th            gộp clip evolve sang dạng 2 → inbox/quy_dao_non/rig/quy_dao_non_th.atomik + khung_evolve.png
  Rig: QD_NON=1 SXS=... py -3 -I quy_dao_rig.py → inbox/quy_dao_non/rig/
Xương, lưới, chuyển động gốc là của nhà phát hành game tham khảo: dùng nội bộ, không đăng công khai."""
import json
import os
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
BASE = os.path.join(HERE, "inbox", "quy_dao_non")
TAI = os.path.join(BASE, "tai_ve")
MAU = os.path.join(BASE, "mau")
MANH = os.path.join(BASE, "manh")
RIG = os.path.join(BASE, "rig")
GUI = os.path.join(HERE, "gui_gpt", "quy_dao_non")
CONCEPT = os.path.join(TAI, "L1_duyet.png")
W, H = 1536, 1024


def Wp(p):
    return os.path.normpath(p)


def ghi(p, lines):
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


# ---------------------------------------------------------------- prompt ba tờ mảnh
STYLE = ("LINE AND COLOUR: exactly the hand-drawn look of image 1: the same wobbly dark-brown ink pen outline (#2B2118), about 5 px thick "
         "around every piece and about 3 px for inner details; the same visible coloured-pencil / wax-crayon hatching inside every area; "
         "the same flat colours as image 1. FLAT COLOUR, NO LIGHT, NO SHADOW: every area one even colour, no shading, no darker "
         "underside, no cast shadow, no white highlights or shine spots (except the one tiny dot already in each eye), no metal "
         "reflections, no glow around fire or eyes, no gradients.")
BG = ("Plain pure-white background (#FFFFFF) everywhere else: no paper grain, no ground, no shadow, no text, no labels, no numbers, no "
      "frame, no white border or sticker outline around the pieces.")

TO = {
    "DAU": dict(
        vi="đầu quả cầu mặt nạ (không sừng), vẽ đủ phần bị giáp vai, sừng, bàn tay che; đúng chỗ, đúng cỡ",
        task=("TASK: redraw image 1 on the same 1536x1024 canvas with ONLY ONE PIECE left: the creature's big round HEAD (the black-iron "
              "demon mask ball with its low crest of three points on top, the heavy brow line and the two slanted yellow eyes). "
              "Everything else is removed and becomes pure white: no fire, no horns, no shoulder guard, no arms, no hand, no body, no "
              "legs, no weapon.\n\n"
              "KEEP IDENTICAL (if the new picture were laid over image 1, the head must coincide exactly): the head at the same "
              "position and the same size (it spans about x = 545 to x = 990, y = 350 to y = 795), its outline wherever it is visible "
              "in image 1, the crest points, the brow line, both eyes with their small light dots, the colour.\n\n"
              "DRAW THE HEAD COMPLETE (this is the point of the picture): in image 1 parts of the head are hidden. Draw them in, so the "
              "head is ONE closed round shape with a complete ink outline all the way around:\n"
              "- the LEFT side, hidden behind the round shoulder guard: continue the round outline of the ball down the left side "
              "(a smooth curve from about (545, 500) down to about (640, 760));\n"
              "- the TOP-LEFT, hidden behind the near horn bud: NO horn; the ball's outline simply continues round there;\n"
              "- the TOP-RIGHT where the small far horn bud was: NO horn; smooth round outline;\n"
              "- the LOWER-RIGHT, hidden behind the clawed hand: continue the round chin outline.\n"
              "The whole hidden area is the same flat black-iron colour with the same crayon hatching as the rest of the head. Do not "
              "add a mouth, teeth, ears, a neck or anything new.")),
    "DAO": dict(
        vi="cây đao trọn vẹn (không bàn tay, không bị đầu che); đúng chỗ, đúng cỡ, đúng góc",
        task=("TASK: redraw image 1 on the same 1536x1024 canvas with ONLY ONE PIECE left: the creature's WEAPON, the giant dao (a "
              "broad single-edged chopping sabre). Everything else is removed and becomes pure white: no creature, no fire, no hand, "
              "no head.\n\n"
              "KEEP IDENTICAL (if the new picture were laid over image 1, the weapon must coincide exactly): the weapon at the same "
              "position, the same size and the same angle: the ring pommel at the top (its hole centred at about (603, 68)), the "
              "dark-red wrapped handle running down-right, the small dark guard at about (820, 305), the broad blade running on "
              "down-right, the square notch in its back at about (1110, 680), the slanted clipped tip ending at about (1085, 990), "
              "the hot orange band along the cutting edge at the lower left. Same outline wherever it is visible in image 1, same "
              "colours.\n\n"
              "DRAW THE WEAPON COMPLETE (this is the point of the picture): in image 1 parts of it are hidden. Draw them in, so the "
              "weapon is ONE whole object with a complete ink outline all the way around:\n"
              "- the HANDLE where the fist grips it: no fist, no fingers; the wrapped handle simply continues straight from the ring "
              "pommel to the guard, with the same dark-red wrap bands;\n"
              "- the GUARD and the UPPER PART OF THE BLADE hidden behind the big head: the guard is a small plain dark block across the "
              "handle; below it the blade starts and gets steadily wider; its cutting edge (the long edge on the lower-left side) "
              "runs in one smooth line from the guard down to where it is visible again at about (820, 800), and the orange band "
              "runs along the whole cutting edge;\n"
              "- the part of the cutting edge hidden behind the clawed hand: no hand; the edge and its orange band continue smooth.\n"
              "The ring pommel keeps its round hole (white shows through it). No cross-guard, no second edge, no cracks, no runes, no "
              "flames on the blade.")),
    "LUA": dict(
        vi="ba búi lửa vẽ RỜI nhau, mỗi búi đủ cả gốc; cùng cỡ, cùng hướng như trên concept",
        task=("TASK: draw a PARTS SHEET on a 1536x1024 pure-white canvas with exactly THREE separate pieces: the THREE FLAME LOCKS of "
              "the fire hair of the creature in image 1, each drawn ALONE and COMPLETE. Nothing else: no head, no creature, no "
              "weapon.\n\n"
              "In image 1 the fire hair is three flame locks that grow from the back of the head and stream to the LEFT; they overlap "
              "each other and their roots are hidden behind the head. On the sheet draw them pulled apart, one under the other, with "
              "at least 40 px of white between them, NOT touching:\n"
              "- TOP ROW (y about 60 to 300): the TOP lock of image 1 (the short one that curls up to a tip at the upper left), about "
              "430 px long;\n"
              "- MIDDLE ROW (y about 360 to 640): the MIDDLE lock (the longest one), about 580 px long;\n"
              "- BOTTOM ROW (y about 700 to 980): the BOTTOM lock (the one whose tip is the leftmost point of the creature), about "
              "520 px long.\n"
              "EACH LOCK: the SAME shape, the same size, the same orientation and the same three nested flat colour zones as in "
              "image 1 (red-orange #E0441F outside, orange #F7902A, yellow #FFD45A inside): its pointed curling tip at the LEFT, its "
              "soft wavy upper and lower edges, and its ROOT at the RIGHT. Draw the root end that image 1 hides: the lock continues "
              "to the right about 110 px further than what is visible in image 1, getting a little narrower, and closes in a "
              "ROUNDED end. Every lock is ONE closed shape with a complete ink outline all the way around, a natural hand-drawn "
              "flame (soft curves, a few pointed tongues), not a saw-tooth zigzag. No sparks, no embers, no smoke.")),
}


def prompt():
    os.makedirs(GUI, exist_ok=True)
    os.makedirs(TAI, exist_ok=True)
    if not os.path.exists(CONCEPT):
        raise SystemExit("thiếu concept chốt: " + Wp(CONCEPT))
    gd = ["# Gói gửi GPT: mảnh của `quy_dao_non` (Viêm Đao dạng 1), lượt 2", "",
          "Làm 2026-11-14 (máy ổ D) sau khi concept B được chọn. Mỗi tờ một file prompt; ảnh mẫu duy nhất là concept chốt.", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|",
          f"| 1 | `{Wp(CONCEPT)}` | Concept dạng 1 đã chốt (1536 × 1024, nền trắng): quỷ lửa con đầu tròn to mặt nạ sắt đen, hai sừng mầm, "
          "ba búi lửa tạt sang trái, giáp vai vòm, đao lớn một lưỡi dựng chéo sau lưng |", ""]
    for k, d in TO.items():
        out = os.path.join(TAI, f"N_{k}.png")
        p = os.path.join(GUI, f"luot_2_manh_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(CONCEPT)}: the APPROVED picture of OUR creature, 1536x1024, white background: a small chibi fire demon "
             "facing right, with a big round black-iron mask head (two slanted yellow eyes, a low three-point crest, two short black "
             "horn buds), three flame locks of fire hair streaming to the left, a round shoulder guard, and a giant single-edged dao "
             "carried diagonally behind it (ring pommel at the top, blade down to the lower right). Take every shape, colour and the "
             "drawing style from it.",
             "", f"SAVE: save it as a PNG to {Wp(out)}",
             f"If a file with that name already exists, save as N_{k}_2.png, N_{k}_3.png ... in the same folder. Do not edit, move or "
             "delete any other file.", "",
             d["task"], "", STYLE, BG]
        ghi(p, t)
        gd += [f"## Tờ `{k}`: {d['vi']}", "",
               f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. GPT tự mở ảnh mẫu và lưu ảnh vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
               f"Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/quy_dao_non/luot_2_manh_{k}.txt --timeout 420`", ""]
        print(p)
    gd += ["## Kiểm", "",
           "- `DAU`: chỉ còn cái đầu, đúng chỗ cũ (đặt chồng lên concept thì trùng), tròn kín, KHÔNG sừng, đủ mào ba mũi + hai mắt vàng.",
           "- `DAO`: chỉ còn cây đao, đúng chỗ, đúng góc; cán liền từ khâu tròn tới chắn tay (không bàn tay), dải lưỡi cam chạy suốt lưỡi sắc.",
           "- `LUA`: đúng ba búi, rời nhau, mũi nhọn bên trái, gốc bo tròn bên phải, ba vùng màu phẳng, viền lửa mềm (không răng cưa).",
           "- Tô phẳng, không bóng, không quầng sáng; nền trắng.", "",
           "## GPT vẽ sai thì gửi thêm", "", "| Sai | Gửi thêm |", "|---|---|",
           "| Mảnh bị dời / đổi cỡ | `Keep the piece at exactly the same position, size and angle as in image 1: laid over image 1 it must coincide.` |",
           "| Còn sót bộ phận khác | `Only that one piece remains; everything else is pure white.` |",
           "| Ba búi lửa dính nhau | `The three flame locks must be separate, with at least 40 px of white between them.` |"]
    ghi(os.path.join(GUI, "HUONG_DAN_manh.md"), gd)


# ---------------------------------------------------------------- concept ↔ rig
# MỘT phép đồng dạng cho cả con (GPT bám hình bố cục nên concept trùng rig: hai bàn chân, giáp vai, bụng khớp trong ~15 đơn vị):
#   x_rig = K (x_px − X0),  y_rig = K (Y0 − y_px).  Mốc: đáy hai bàn chân y_px 990 ↔ y_rig −7; khung đao x_px 541 ↔ x_rig −37.
K, X0, Y0 = 1.01, 578.0, 983.0


def tg(p):
    """điểm concept (px) → thế giới rig."""
    return [K * (p[0] - X0), K * (Y0 - p[1])]


def M_cua(ox, oy, k=K, x0=X0, y0=Y0):
    """ma trận "M" của dat_moi.json cho ảnh cắt có góc trên trái ở (ox, oy) trên concept."""
    return [[k, 0.0, k * (ox - x0)], [0.0, -k, k * (y0 - oy)]]


def _rig():
    """dựng rig dạng non (QD_NON=1), trả (R, sk, info, clips, khung idle đã nướng + aura)."""
    import contextlib
    import io
    os.environ["QD_NON"] = "1"
    import quy_dao_rig as R
    from quai import hoat
    with contextlib.redirect_stdout(io.StringIO()):
        sk, info = R.dung()
        clips = R.lam_clip(sk, info)
    return R, sk, info, clips, hoat


def so(clip="idle", t=0.0, ra=None):
    """dáng của rig ở khung concept (1536 × 1024) đặt cạnh và chồng nửa trong lên concept → inbox/quy_dao_non/so_concept.png."""
    from quai import soi
    R, sk, info, clips, hoat = _rig()
    fr = hoat.nuong(sk, [c for c in clips if c.ten == clip][0])
    P = fr[min(len(fr) - 1, int(round(t * 30)))]
    ve = soi.Ve(sk)
    box = (K * (0 - X0), K * (Y0 - H), K * (W - X0), K * Y0)
    im = ve.ve(P, box, 1.0 / K, bg=(255, 255, 255), ss=2).convert("RGB").resize((W, H), Image.LANCZOS)
    C = Image.open(CONCEPT).convert("RGB")
    tron = Image.blend(C, im, 0.5)
    o = Image.new("RGB", (W * 3 // 2, H // 2 * 1 + H), (255, 255, 255))
    o.paste(tron, (0, 0))
    o.paste(im.resize((W // 2, H // 2), Image.LANCZOS), (W, 0))
    o.paste(C.resize((W // 2, H // 2), Image.LANCZOS), (W, H // 2))
    p = ra or os.path.join(BASE, "so_concept.png")
    o.crop((0, 0, W * 3 // 2, H)).save(p)
    im.save(os.path.join(BASE, "_rig_khung_concept.png"))
    print(p)


# ---------------------------------------------------------------- cắt mảnh
# đa giác khung (px concept) cho ba mảnh cắt THẲNG từ concept (nằm trên cùng, không bị che)
PAD_POLY = [(470, 478), (530, 488), (580, 530), (602, 588), (624, 604), (627, 640), (612, 668), (590, 700), (540, 742), (470, 768), (395, 774),
            (335, 765), (305, 735), (305, 690), (308, 640), (318, 590), (345, 540), (395, 498)]
SUNG_GAN_POLY = [(600, 338), (628, 348), (640, 400), (668, 450), (672, 500), (630, 528), (585, 530), (548, 515), (530, 470), (538, 420),
                 (565, 372)]
SUNG_XA_POLY = [(985, 403), (1006, 418), (1014, 460), (1008, 500), (992, 522), (962, 524), (948, 470), (952, 446), (972, 426)]
# gốc xương sừng (chỗ sừng mọc trên đầu), gốc + mũi từng búi lửa trên concept (px): quy_dao_rig dời gốc chuỗi xương tới đó
SUNG_GAN_GOC, SUNG_XA_GOC = (590, 492), (975, 492)
LUA = [  # (slot, chuỗi xương, gốc búi (khuất sau đầu), mũi búi) theo thứ tự vẽ sau → trước: búi trên, búi giữa, búi dưới
    ("toufa_07", ["toufa_07", "toufa_08", "toufa_09"], (770, 330), (432, 195)),
    ("toufa_03", ["toufa_03", "toufa_04", "toufa_05", "toufa_06"], (780, 400), (300, 318)),
    ("toufa_06", ["toufa_014", "toufa_015", "toufa_016"], (640, 500), (190, 440)),
]
LUA_TI = (0.90, 0.85, 0.9)                         # tỉ lệ từng búi so với tờ N_LUA (GPT vẽ búi mập hơn concept)
LUA_XOAY = (22.0, 10.0, 8.0)                       # tờ N_LUA vẽ búi nằm ngang; trên concept búi dốc xuống về phía gốc (độ, thuận kim)
LUA_DOI = ((-18, 10), (0, 0), (0, 0))                # dời từng búi (đơn vị rig)
AN = ["huzi", "toufa_01", "toufa_02", "jiajia_l"]     # râu lửa, hai búi bờm trên thân, giáp bắp tay xa (con non chưa có)
THON = {"xiaobi_l": 0.62, "dabi_l": 0.62}          # tay xa (vòng lên sau đầu nắm cán đao): thon lại, không thì lòi một cục to sau ba búi lửa nhỏ
CAO = 700.0
DAO_PHONG = 0.35                                  # giữ 35 % độ phóng phối cảnh của đao lúc chém (họ phóng tới × 1,5: con nhỏ thì đao thành gấp ba thân)
WALK_NGA = 0.25                                   # walk: giữ 25 % độ gập ngực của run_01 (đầu to tụt sát đất, tay gần che hết mặt)
TAY_GAN = 0.86                                    # tay gần ngắn, mập hơn dạng 2


def el(r):
    import cv2
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def _luu(rgb, m, ten, pad=4):
    """cắt khung quanh mặt nạ m, khử viền sáng, lưu manh/<ten>.png; trả (x, y, rộng, cao) của khung trên ảnh nguồn."""
    import cv2
    import quy_dao_da as DA
    ys, xs = np.nonzero(m)
    x0, y0, x1, y1 = max(0, xs.min() - pad), max(0, ys.min() - pad), min(m.shape[1], xs.max() + 1 + pad), min(m.shape[0], ys.max() + 1 + pad)
    mm = m[y0:y1, x0:x1].astype(np.uint8)
    c = DA.khu_vien(np.ascontiguousarray(rgb[y0:y1, x0:x1]).astype(np.uint8), mm)
    al = cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.8)
    vien = mm.astype(bool) & ~cv2.erode(mm, el(2)).astype(bool)
    sang = c.min(2).astype(np.float32)
    al = np.where(vien, np.minimum(al, np.clip((250.0 - sang) / 70.0, 0, 1)), al)
    os.makedirs(MANH, exist_ok=True)
    Image.fromarray(np.dstack([c, (np.clip(al, 0, 1) * 255).astype(np.uint8)]), "RGBA").save(os.path.join(MANH, ten + ".png"))
    return int(x0), int(y0), int(x1 - x0), int(y1 - y0)


def _moi_nhat(tien_to):
    fs = sorted([f for f in os.listdir(TAI) if f.startswith(tien_to) and f.endswith(".png")], key=lambda f: os.path.getmtime(os.path.join(TAI, f)))
    return os.path.join(TAI, fs[-1]) if fs else None


def _doc(p):
    return np.asarray(Image.open(p).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.uint8)


def _cum(A, min_dt=1500):
    """các cụm không phải nền trắng của một tờ (nền = trắng nối mép ảnh), lỗ trắng kín bên trong được lấp."""
    import cv2
    import quy_dao_da as DA
    fg = (~DA.nen(A.astype(np.int32))).astype(np.uint8)
    fg = cv2.morphologyEx(fg, cv2.MORPH_OPEN, el(1))
    n, lab, st, cen = cv2.connectedComponentsWithStats(fg, 8)
    out = []
    for i in range(1, n):
        if st[i, 4] < min_dt:
            continue
        m = (lab == i).astype(np.uint8)
        m = (cv2.dilate(m, el(10)).astype(bool) & fg.astype(bool)) | m.astype(bool)
        cs, _ = cv2.findContours(m.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        day = np.zeros(m.shape, np.uint8)
        cv2.drawContours(day, cs, -1, 1, -1)
        out.append((day.astype(bool), cen[i]))
    return out


def thon():
    """mảnh tay xa của dạng 2 (ảnh vùng × 2, cùng khung) bóp thon theo chiều NGANG xương (quanh đường giữa mảnh, trong hệ của xương
    mang nó): cùng lưới, cùng chỗ gắn, chỉ ảnh đổi → manh/<slot>.png của dạng non (quy_dao_rig ưu tiên thư mục manh của dạng non)."""
    import cv2
    import quy_dao as G
    AG = json.load(open(os.path.join(G.scan(), "att_goc.json"), encoding="utf-8"))
    WG = {b["name"]: np.array([[b["a"], b["b"], b["x"]], [b["c"], b["d"], b["y"]], [0, 0, 1.0]]) for b in AG["bones"]}
    G._C.pop("att", None)
    _, imgs_ho, _ = G.nap("att_goc.json")
    for slot, f in THON.items():
        a = next(x for x in AG["atts"] if x["slot"] == slot)
        uv_px, _ = G.luoi(a)
        xy = np.array(a["xy"], float).reshape(-1, 2)
        im = np.asarray(Image.open(os.path.join(HERE, "inbox", "quy_dao_1", "manh", a["region"] + ".png")).convert("RGBA"))
        k = im.shape[1] / imgs_ho[a["region"]].size[0]                      # ảnh mảnh = ảnh vùng × k
        src = np.float32(uv_px[:3] * k)
        loc = np.array([np.linalg.solve(WG[a["bone"]], np.array([q[0], q[1], 1.0]))[:2] for q in xy[:3]], np.float32)
        A_ = cv2.getAffineTransform(src, loc)                               # px ảnh → hệ xương
        A3 = np.vstack([A_, [0, 0, 1]])
        ys, xs = np.nonzero(im[..., 3] > 40)
        y0 = float((A3 @ np.stack([xs, ys, np.ones(len(xs))]))[1].mean())   # đường giữa mảnh (y trong hệ xương)
        S_ = np.array([[1, 0, 0], [0, 1 / f, y0 * (1 - 1 / f)], [0, 0, 1.0]])  # đích → nguồn trong hệ xương
        Minv = np.linalg.inv(A3) @ S_ @ A3                                  # px đích → px nguồn
        pm = im.astype(np.float32)
        pm[..., :3] *= pm[..., 3:4] / 255.0
        out = cv2.warpAffine(pm, Minv[:2], (im.shape[1], im.shape[0]), flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP,
                             borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
        al = np.clip(out[..., 3:4], 1e-3, 255)
        out[..., :3] = np.where(out[..., 3:4] > 0, out[..., :3] * 255.0 / al, 0)
        os.makedirs(MANH, exist_ok=True)
        Image.fromarray(np.clip(out + 0.5, 0, 255).astype(np.uint8), "RGBA").save(os.path.join(MANH, a["region"] + ".png"))
        print(f"  {slot}: thon còn {f} bề ngang (xương {a['bone']}, đường giữa y = {y0:.0f})")


def cat():
    import cv2
    sys.path.insert(0, os.path.join(HERE, "mo_xe"))
    from cat_concept import cat as cat_c
    C = _doc(CONCEPT)
    thon()
    cap, xuong = {}, {"dabi_r": {"s": TAY_GAN}}
    lab = cv2.cvtColor(C, cv2.COLOR_RGB2LAB)
    den = (lab[..., 0] < 30 * 255 / 100) & (np.abs(C[..., 0].astype(int) - C[..., 2].astype(int)) < 14)     # đen trung tính của sừng (mực thì nâu)

    # 1. giáp vai (trên cùng, không bị che): cắt thẳng
    _, m = cat_c(C, PAD_POLY, ti=0.7, vien=8)
    m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_OPEN, el(5)).astype(bool)          # bỏ mẩu nét mực của mảnh bên cạnh dính vào mép
    x, y, w, h = _luu(C, m, "jianjia")
    cap["jianjia"] = dict(anh="jianjia", M=M_cua(x, y), px=0.72, buoc=40.0, cung="dabi_r")
    print(f"  giáp vai  {w}×{h} ở ({x}, {y})  ← concept")
    # 2. sừng gần (trên cùng), sừng xa (gốc nấp sau đầu: kéo dài gốc xuống dưới trái 16 px bằng chính màu sừng)
    _, m = cat_c(C, SUNG_GAN_POLY, ti=0.6, them=den)
    x, y, w, h = _luu(C, m, "dajiao_r")
    cap["dajiao_r"] = dict(anh="dajiao_r", M=M_cua(x, y), px=0.72, buoc=40.0, cung="dajiao_r")
    xuong["dajiao_r"] = {"tg": tg(SUNG_GAN_GOC)}
    print(f"  sừng gần  {w}×{h} ở ({x}, {y})  ← concept")
    _, m = cat_c(C, SUNG_XA_POLY, ti=0.6, them=den)
    C2, m2 = C.copy(), m.copy()
    for k in range(1, 17):
        sh = np.zeros_like(m)
        sh[k:, :-k] = m[:-k, k:]                         # dời (−k, +k): xuống dưới, sang trái
        them = sh & ~m2
        C2[them] = (33, 32, 36)
        m2 |= sh
    x, y, w, h = _luu(C2, m2, "dajiao_l")
    cap["dajiao_l"] = dict(anh="dajiao_l", M=M_cua(x, y), px=0.72, buoc=40.0, cung="dajiao_l")
    xuong["dajiao_l"] = {"tg": tg(SUNG_XA_GOC)}
    print(f"  sừng xa   {w}×{h} ở ({x}, {y})  ← concept (gốc kéo dài 16 px)")

    # 3. đầu (tờ N_DAU, đúng chỗ đúng cỡ): cụm lớn nhất
    src = _moi_nhat("N_DAU")
    if src:
        A = _doc(src)
        cs = sorted(_cum(A), key=lambda c: -c[0].sum())
        m = cs[0][0]
        x, y, w, h = _luu(A, m, "lian_01")
        cap["lian_01"] = dict(anh="lian_01", M=M_cua(x, y), px=0.72, buoc=40.0, cung="lian_01")
        print(f"  đầu       {w}×{h} ở ({x}, {y})  ← {os.path.basename(src)}")
    else:
        print("  đầu: chưa gen N_DAU")

    # 4. đao (tờ N_DAO, đúng chỗ): đặt bằng HAI MỐC riêng: chỗ bàn tay xa nắm cán (tâm cán gần (750, 232) trên concept) ↔ gốc xương vũ
    # khí của rig (chỗ bàn tay), mũi đao ↔ mũi đao của rig. (Đao trên concept bè, cán lệch khỏi đường khâu → mũi nên không dùng hai đầu mút.)
    src = _moi_nhat("N_DAO")
    vet = None
    if src:
        A = _doc(src)
        cs = sorted(_cum(A), key=lambda c: -c[0].sum())
        m = cs[0][0]
        lo = m & (A.min(2) > 232)                                    # lỗ khâu tròn ở chuôi: giấy trắng kín
        n, ll, ss, _ = cv2.connectedComponentsWithStats(lo.astype(np.uint8), 4)
        for j in range(1, n):
            if ss[j, 4] > 120:
                m[ll == j] = False
        ys, xs = np.nonzero(m)
        Pm = np.stack([xs, ys], 1).astype(float)
        gan_tay = Pm[np.hypot(Pm[:, 0] - TAY_NAM[0], Pm[:, 1] - TAY_NAM[1]) < 42]
        z1 = gan_tay.mean(0)                                         # tâm cán chỗ bàn tay nắm
        c = Pm.mean(0)
        _, _, vt = np.linalg.svd(Pm - c, full_matrices=False)
        d = vt[0] if vt[0][1] > 0 else -vt[0]                        # trục dài, chiều đi xuống (về mũi)
        z2 = Pm[np.argmax((Pm - c) @ d)]                             # mũi đao (điểm xa nhất về phía mũi)
        x, y, w, h = _luu(A, m, "wuqi_02")
        import quy_dao_da as DA
        _, dao = DA.the_gioi_mau()
        import quy_dao as G
        AG = json.load(open(os.path.join(G.scan(), "att_goc.json"), encoding="utf-8"))
        WG = {b["name"]: np.array([[b["a"], b["b"], b["x"]], [b["c"], b["d"], b["y"]], [0, 0, 1.0]]) for b in AG["bones"]}
        w1 = WG["wuqi_03"][:2, 2]                                    # chỗ bàn tay nắm trên rig (dáng gốc)
        w2 = np.asarray(dao["mui"], float)
        za, zb = complex(z1[0], -z1[1]), complex(z2[0], -z2[1])
        a_ = (complex(*w2) - complex(*w1)) / (zb - za)
        b_ = complex(*w1) - a_ * za
        Mm = np.array([[a_.real, a_.imag, b_.real + 0.0], [a_.imag, -a_.real, b_.imag + 0.0]])
        Mm[:, 2] += Mm[:, :2] @ np.array([x, y], float)              # ảnh đã cắt: gốc ảnh ở (x, y)
        cap["wuqi_02"] = dict(anh="wuqi_02", M=Mm.tolist(), px=0.62, buoc=60.0, cung="wuqi_03")
        print(f"  đao       {w}×{h} ở ({x}, {y})  ← {os.path.basename(src)}; tay {z1.round()} → mũi {z2.round()}, tỉ lệ {abs(a_):.3f}, "
              f"xoay {np.degrees(np.angle(a_)):.1f}°")
        # điểm dọc LƯỠI SẮC cho vệt chém (u từ chuôi, v ngang, theo chiều dài đao của rig; lưỡi sắc ở phía v âm)
        Vd = np.array(next(a for a in AG["atts"] if a["slot"] == "wuqi_02")["xy"], float).reshape(-1, 2)
        chuoi_g, mui_g = (Vd[1] + Vd[2]) / 2, (Vd[0] + Vd[3]) / 2
        Ld = float(np.linalg.norm(mui_g - chuoi_g))
        ax = (mui_g - chuoi_g) / Ld
        song = np.array([-ax[1], ax[0]])
        cs_, _ = cv2.findContours(m.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        Pc = max(cs_, key=len).reshape(-1, 2).astype(float)
        Wc = (np.array([[a_.real, a_.imag], [a_.imag, -a_.real]]) @ Pc.T).T + np.array([b_.real, b_.imag])
        U, V_ = (Wc - chuoi_g) @ ax / Ld, (Wc - chuoi_g) @ song / Ld
        vet = []
        for u in (0.40, 0.58, 0.76, 0.90):
            vet.append([u, round(float(V_[np.abs(U - u) < 0.012].min()) + 0.006, 4)])
        k = int(np.argmax(U))                                        # mũi đao: điểm xa nhất (cuối lưỡi sắc)
        vet.append([round(float(U[k]) - 0.006, 4), round(float(V_[k]) + 0.004, 4)])
        print("  vệt chém (u, v):", vet)
    else:
        print("  đao: chưa gen N_DAO")

    # 5. ba búi lửa (tờ N_LUA: vẽ rời, hàng trên → dưới = búi trên, giữa, dưới): đặt bằng mũi búi (điểm trái nhất) ↔ mũi trên concept, cùng
    # hướng, tỉ lệ K × LUA_TI (chỉnh tay sau khi soi chồng lên concept)
    src = _moi_nhat("N_LUA")
    if src:
        A = _doc(src)
        cs = sorted(sorted(_cum(A, 4000), key=lambda c: -c[0].sum())[:3], key=lambda c: c[1][1])
        for (slot, chuoi, goc, mui), (m, _), ti, xoay, dch in zip(LUA, cs, LUA_TI, LUA_XOAY, LUA_DOI):
            ys, xs = np.nonzero(m)
            j = int(np.argmin(xs))
            tip = np.array([xs[j], ys[xs == xs[j]].mean()])                      # mũi búi: điểm trái nhất
            j2 = int(np.argmax(xs))
            duoi = np.array([xs[j2] - 55.0, ys[xs > xs[j2] - 60].mean()])        # gốc búi: lùi 55 px từ đầu bo tròn bên phải
            x, y, w, h = _luu(A, m, slot)
            k = K * ti
            c_, s_ = np.cos(np.radians(xoay)), np.sin(np.radians(xoay))          # xoay thuận kim trên màn hình quanh mũi búi
            wt = np.array(tg(mui)) + np.array(dch, float)
            A2 = np.array([[k * c_, -k * s_], [-k * s_, -k * c_]])
            Mm = np.column_stack([A2, wt - A2 @ (tip - np.array([x, y], float))])
            goc_w = (A2 @ (duoi - tip) + wt).tolist()
            cap[slot] = dict(anh=slot, M=Mm.tolist(), px=0.62, buoc=24.0, chuoi=chuoi)
            xuong[chuoi[0]] = {"lua": [goc_w, wt.tolist()]}
            print(f"  lửa {slot}  {w}×{h} ở ({x}, {y})  ← {os.path.basename(src)}; mũi {tip.round()} → {np.round(wt)}, gốc → {np.round(goc_w)}, "
                  f"tỉ lệ {k:.3f}, xoay {xoay}°")
    else:
        print("  lửa: chưa gen N_LUA")
    json.dump(cap, open(os.path.join(MANH, "dat_moi.json"), "w", encoding="utf-8"), indent=1)
    dang = {"an": AN, "cao": CAO, "dao_phong": DAO_PHONG, "walk_nga": WALK_NGA, "xuong": xuong}
    if vet:
        dang["vet_hang"] = vet
    os.makedirs(MAU, exist_ok=True)
    json.dump(dang, open(os.path.join(MAU, "dang.json"), "w", encoding="utf-8"), indent=1)
    print("→", os.path.join(MANH, "dat_moi.json"), "+", os.path.join(MAU, "dang.json"))


TAY_NAM = (750, 232)                               # tâm bàn tay xa trên concept (chỗ nắm cán đao)


# ---------------------------------------------------------------- tiến hóa
SIZE_A, SIZE_B = 0.8, 1.1                          # cỡ trong heroes.json: dạng 1 (đề xuất), dạng 2 (khối giap_long)


def th():
    """gộp dạng 2 (quy_dao_1 bản nhẹ) vào rig dạng 1 + clip `evolve` (mo_xe/atomik_dang.gop_tien_hoa, như golem_lua_non_th.py):
    dạng 1 gồng rung rồi mờ, dạng 2 hiện, lớn dần, dừng đúng khung 0 idle của nó. Slot ẩn sẵn của hai rig (bản nhân của slot di động,
    vệt chém: fade 1) giữ ẩn suốt clip."""
    sys.path.insert(0, os.path.join(HERE, "mo_xe"))
    import atomik_dang as A
    src_a = os.path.join(RIG, "quy_dao_non.atomik")
    src_b = os.path.join(HERE, "inbox", "quy_dao_1", "rig", "quy_dao_1.atomik")
    if not os.path.exists(src_b):                  # máy chưa dựng lại rig dạng 2: lấy bản đang ở trong game (chỉ đọc)
        src_b = os.path.normpath(os.path.join(HERE, "..", "..", "Assets", "03 Art", "Heroes", "Resources", "quy_dao_1", "quy_dao_1.atomik"))
    J, img, ver = A.load(src_a)
    JB, imgB, _ = A.load(src_b)
    an_A = {i for i, s in enumerate(J["slots"]) if s.get("fade", 0) >= 1}
    an_B = {i for i, s in enumerate(JB["slots"]) if s.get("fade", 0) >= 1}
    nA_s = len(J["slots"])
    hA, hB = J["game"]["height"], JB["game"]["height"]
    k_B = SIZE_B / SIZE_A * hA / hB
    img = A.gop_tien_hoa(J, img, JB, imgB, k_B, than_A=A.bi(J)["bone"])
    ev = J["anims"][-1]
    n = 0
    for x in ev["sa"]:
        if x["slot"] in an_A or (x["slot"] - nA_s) in an_B:
            x["keys"] = A.rot_keys([(0, 0), (ev["dur"], 0)])
            n += 1
    p = os.path.join(RIG, "quy_dao_non_th.atomik")
    kq = A.save(p, J, img, ver)
    print(f"{p}: {os.path.getsize(p) // 1024} KB; dạng 2 lấy từ {src_b}; trong rig gộp × {k_B:.3f}; {n} slot ẩn giữ ẩn trong evolve; {kq}")
    ci = A.clip(J, "evolve")
    ts = [0.0, 0.5, 0.9, 1.05, 1.2, 1.35, 1.5, 1.8, 2.2, 2.6, 3.0]
    Ps = [A.Pose(J).at(ci, t) for t in ts]
    bs = np.array([A.bounds(P) for P in Ps])
    box = (bs[:, 0].min() - 20, bs[:, 1].min() - 20, bs[:, 2].max() + 20, bs[:, 3].max() + 20)
    ims = [A.render(J, img, A.Pose(J).at(ci, t), box, 0.4, bg=(150, 150, 150)).convert("RGB") for t in ts]
    cot = 6
    out = Image.new("RGB", (cot * ims[0].width, ((len(ims) + cot - 1) // cot) * ims[0].height), (150, 150, 150))
    for i, im in enumerate(ims):
        out.paste(im, ((i % cot) * im.width, (i // cot) * im.height))
    out.save(os.path.join(RIG, "khung_evolve.png"))
    print(os.path.join(RIG, "khung_evolve.png"), out.size)
    # khung cuối evolve phải trùng khung 0 idle của dạng 2 (cùng tỉ lệ k_B)
    ib = A.clip(JB, "idle")
    Pb = A.Pose(JB).at(ib, 0.0)
    Pe = A.Pose(J).at(ci, ev["dur"])
    nb = len(J["bones"]) - len(JB["bones"])
    lech = 0.0
    for i in range(len(JB["bones"])):
        lech = max(lech, abs(Pe.w[nb + i][4] - Pb.w[i][4] * k_B), abs(Pe.w[nb + i][5] - Pb.w[i][5] * k_B))
    print(f"khung cuối evolve so khung 0 idle dạng 2: lệch gốc xương lớn nhất {lech:.3f} đơn vị")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "prompt":
        prompt()
    elif cmd == "th":
        th()
    elif cmd == "cat":
        cat()
    elif cmd == "so":
        so(*(sys.argv[2:3]), *([float(sys.argv[3])] if len(sys.argv) > 3 else []))
    else:
        print(__doc__)
