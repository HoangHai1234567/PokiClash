# -*- coding: utf-8 -*-
"""Gói GPT vẽ RIÊNG dạng 1 của Hỏa Quy (rùa non CHIBI; mã làm việc rua_lua_non, suất nguu_quyen đảo Hỏa).

Người dùng (2026-11-13): xem bản dựng lại từ mảnh dạng 2 (A, B, C) → "tôi muốn chi bi hơn, nhỏ hơn nữa" → xem D, E → "E cũng được nhưng sẽ phải
gen lại bằng gpt cho chi bi hơn". Bản E (rua_lua_non.py hướng chibi_1: đầu to, sừng mầm, một ngọn lửa) đang ở trong game làm dạng 1 tạm.
Codex hết hạn mức tới 18:30 nên gói này dựng sẵn, gen sau. Hai hướng là ĐỀ XUẤT của Claude:
  theo_e    giữ đúng bố cục bản E (chỗ đặt từng bộ phận trùng rig), vẽ lại cho ra nét chibi: khối tròn mập, mắt to hơn, ít chi tiết
  tron_hon  chibi mạnh hơn: mai tròn ngắn như hòn cuội, bốn chân lùn hẳn, đầu gần nửa chiều cao

    py -3 -I ArtGen/Spine/build_rua_lua_non.py           dựng hình bố cục E (inbox/rua_lua_non/mau/bo_cuc_e.png) + hai file prompt
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/rua_lua_non/luot_1_concept_<hướng>.txt
"""
import contextlib
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
PK = os.path.join(HERE, "gui_gpt", "rua_lua_non")
BASE = os.path.join(HERE, "inbox", "rua_lua_non")
MAU = os.path.join(BASE, "mau")
TAI = os.path.join(BASE, "tai_ve")
DANG2 = os.path.join(HERE, "inbox", "rua_lua_1", "tai_ve", "L1_duyet.png")
BO_CUC = os.path.join(MAU, "bo_cuc_e.png")
W, H = 1536, 1024


def Wp(p):
    return os.path.normpath(p)


def bo_cuc():
    """dáng đứng của bản E (dựng từ rig) đặt giữa khung 1536 × 1024 nền trắng; trả khung bao hình (px)."""
    from PIL import Image
    import numpy as np
    os.environ["RL_NON"] = "chibi_1"
    import rua_lua_rig as R
    from quai import hoat, soi
    with contextlib.redirect_stdout(io.StringIO()):
        sk, info = R.dung()
        clips = R.lam_clip(sk, info)
    fr = hoat.nuong(sk, [c for c in clips if c.ten == "idle"][0])
    ve = soi.Ve(sk)
    Bx = soi._union([ve.bao(fr[0])], 0.02)
    ti = min((W - 360) / (Bx[2] - Bx[0]), (H - 260) / (Bx[3] - Bx[1]))
    im = ve.ve(fr[0], Bx, ti, bg=(255, 255, 255), ss=2).convert("RGB")
    o = Image.new("RGB", (W, H), (255, 255, 255))
    x0, y0 = (W - im.width) // 2, H - 90 - im.height
    o.paste(im, (x0, y0))
    os.makedirs(MAU, exist_ok=True)
    o.save(BO_CUC)
    a = np.asarray(o).min(2) < 240
    ys, xs = np.nonzero(a)
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


CHUNG = (
    "CREATURE: the BABY (first-stage) form of the fire tortoise golem of image 2, for a monster-collecting game: the same living rock "
    "tortoise built from separate stone blocks, with a skull-like stone face mask and fire on its shell, but YOUNG and SMALL, drawn "
    "CHIBI.\n\n"
    "CHIBI PROPORTIONS (the whole point of this picture): a VERY BIG head, {dau} of the whole figure's height; a short, round, plump "
    "body; very short stubby legs; everything rounder, simpler and chunkier than image 2. It is still a fighter: the brow of the mask "
    "comes down over the eye, a determined, plucky look. NOT a smiling mascot, NOT a real turtle, NOT a robot.\n\n"
    "WHAT IT KEEPS FROM IMAGE 2 (same species, same colours, same materials): slate blue-grey stone shell and legs, a lighter "
    "blue-grey belly plate, dark navy-charcoal stone columns, warm ivory face mask and jaw, pale ivory horns and tail spikes, small "
    "hot-orange crystals on the two front legs, yellow fire eye in a dark socket, red-orange / orange / yellow flat flame, dark-brown "
    "wobbly ink outline, visible crayon hatching, completely flat colouring.\n\n"
    "WHAT IS DIFFERENT (it is a baby):\n"
    "- HORNS: only two short blunt HORN BUDS (the near one a short thick curved nub on the side of the head, about one third of the "
    "head's height; the far one a tiny nub peeking out behind the mask). Whole, not broken.\n"
    "- FIRE: only ONE small flame, on the top of the shell. No other flames.\n"
    "- STONE COLUMNS: one small cluster of three short stubby columns on the near side of the shell. No far column.\n"
    "- EYE: a little bigger than in image 2, still slanted and fierce, one eye only (the other is hidden).\n"
    "- TAIL: a short stubby tail with two small spikes. CRYSTALS: one or two small ones on each front leg.\n\n"
    "SAME BUILD AND VIEW AS IMAGE 2: four legs, seen from its left side in a slight three-quarter view, FACING THE VIEWER'S RIGHT, "
    "head low at the front right, muzzle pointing down-right, the separate lower jaw block under the mask with the zigzag tooth edge "
    "between them, mouth closed, all four feet flat on the same ground level.")

D = {
    "theo_e": dict(
        ten="theo bố cục bản E: chỗ đặt từng bộ phận giữ như hình bố cục, vẽ lại nét chibi (khối tròn mập, mắt to hơn)",
        dau="about 45 %",
        rieng=("FOLLOW THE LAYOUT GUIDE (image 1) CLOSELY for where every part sits and how big it is: the shell, the column cluster, "
               "the single flame, the big head with its mask, jaw and horn buds, the four legs, the tail. Image 1 is a rough "
               "computer paste-up made by shrinking and enlarging parts of the adult: redraw it as ONE properly designed chibi "
               "creature: make every block rounder and plumper, simplify the shell to three or four big slabs, make the legs "
               "short rounded stumps, keep the head as big as in the guide.")),
    "tron_hon": dict(
        ten="chibi mạnh hơn: mai tròn ngắn như hòn cuội, bốn chân lùn hẳn, đầu gần nửa chiều cao",
        dau="almost half (about 50 %)",
        rieng=("Use the LAYOUT GUIDE (image 1) only for the general arrangement and the view. Push the chibi look further than the "
               "guide: the shell is a SHORT ROUND dome like a river pebble (the body is clearly shorter than in the guide, about "
               "as long as it is tall), the four legs are very short round stumps, the head is even bigger and rounder, the tail "
               "is tiny. Simplify the shell to three big slabs.")),
}

POSE = ("ANIMATION-READY (very important: the picture will be cut into separate pieces and animated with a 2D skeleton): calm, clean "
        "resting pose. Draw every piece as a clear, simple, closed shape with its own complete ink outline, so the pieces can be "
        "separated: the shell, the column cluster, the flame, the face mask, the jaw, each horn bud, each thigh block, each lower "
        "leg block, the tail, the belly plate. Every leg is clearly attached to the body (no white background between a leg and "
        "the body). No sparks, no embers, no smoke, no glow, no ground, no shadow, no props, no second character.")
LINE = ("LINE AND COLOUR: exactly the hand-drawn look of image 2: dark-brown ink pen (#2B2118), outline about 5 px thick around every "
        "big piece and about 3 px for small details; coloured-pencil and wax-crayon hatching visible inside every area. FLAT COLOUR, "
        "NO LIGHT, NO SHADOW: every area one even colour, no shading, no highlights except one tiny dot in the eye, no glow around "
        "the fire, no gradients.")
BG = ("Plain pure-white background (#FFFFFF), no paper grain outside the drawing, no white border or sticker outline around the "
      "figure, no text, no labels, no frame.")


def ghi(p, lines):
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def main():
    x0, y0, x1, y1 = bo_cuc()
    os.makedirs(PK, exist_ok=True)
    os.makedirs(TAI, exist_ok=True)
    gd = ["# Gói gửi GPT: `rua_lua_non` (Hỏa Quy dạng 1, rùa non chibi; suất `nguu_quyen` đảo Hỏa)", "",
          "Làm 2026-11-13. Người dùng: \"E cũng được nhưng sẽ phải gen lại bằng gpt cho chi bi hơn\". Hai hướng là đề xuất của Claude, chờ "
          "người dùng chọn. Ghi chú: `ArtGen/Spine/inbox/rua_lua_ghichu.md` mục 8, 9.", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|",
          f"| 1 | `{Wp(BO_CUC)}` | Hình bố cục bản E dựng từ rig (1536 × 1024, nền trắng): rùa non đầu to, sừng mầm, một ngọn lửa, ghép từ "
          "mảnh dạng 2 co giãn. Lấy chỗ đặt, cỡ từng bộ phận |",
          f"| 2 | `{Wp(DANG2)}` | Concept dạng 2 đã duyệt (1536 × 1024, nền trắng): rùa golem lửa đá bazan xám lam, mặt sọ ngà, hai sừng, "
          "bảy ngọn lửa. Lấy loài, màu, chất liệu, nét vẽ |", ""]
    for kieu, d in D.items():
        out = os.path.join(TAI, f"L1_{kieu}.png")
        p = os.path.join(PK, f"luot_1_concept_{kieu}.txt")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(BO_CUC)}: LAYOUT GUIDE, 1536x1024, white background: a rough computer paste-up of the baby creature in its "
             "resting stance (a small tortoise golem with a very big head, two short horn buds, one small flame on its shell), made "
             "from resized parts of the adult. Use it for the arrangement and sizes, not for its drawing quality.",
             f"image 2 = {Wp(DANG2)}: the APPROVED ADULT form of this creature, 1536x1024, white background: take the species, every "
             "colour, the materials and EXACTLY the hand-drawn line and colouring style from it.",
             "", f"SAVE: save it as a PNG to {Wp(out)}",
             f"If a file with that name already exists, save as L1_{kieu}_2.png, L1_{kieu}_3.png ... in the same folder. Do not edit, "
             "move or delete any other file.", "",
             "TASK: draw ONE creature as ONE picture, in a clean animation-ready resting pose.", "",
             CHUNG.format(dau=d["dau"]), "", d["rieng"], "",
             f"CANVAS AND FRAMING: landscape 1536x1024. The figure stands in the middle, about as big as in the guide (in image 1 it "
             f"spans about x = {x0} to x = {x1}, y = {y0} to y = {y1}); everything visible, nothing cut by the edges.", "",
             POSE, "", LINE, BG]
        ghi(p, t)
        gd += [f"## Hướng `{kieu}`: {d['ten']}", "",
               f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. GPT tự mở ảnh mẫu và lưu ảnh vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", ""]
        print(p)
    gd += ["## Kiểm", "", "- Chibi thật: đầu gần nửa chiều cao, thân ngắn tròn, chân lùn; vẫn mặt \"chiến\" (mày đè xuống mắt), không cười.",
           "- Cùng loài với dạng 2: đá xám lam, mặt sọ ngà một mắt vàng, hàm rời mép răng cưa, pha lê cam ở chân trước.",
           "- Chỉ hai mầm sừng ngắn (lành lặn), MỘT ngọn lửa trên mai, một cụm ba cột đá lùn.",
           "- Nhìn sang phải, bốn chân chạm đất, chân nào cũng dính thân; từng khối có viền kín.",
           "- Tô phẳng, không bóng, không quầng sáng; nền trắng.", "",
           "## GPT vẽ sai thì gửi thêm", "", "| Sai | Gửi thêm |", "|---|---|",
           "| Chưa đủ chibi | `Make it more chibi: the head must be about half of the whole height, the body shorter and rounder, the legs shorter.` |",
           "| Mặt cười / hiền | `Not cute-smiling: the brow comes down over the eye, a determined fierce look, mouth closed.` |",
           "| Sừng dài / nhiều lửa | `Only two short horn buds and only ONE small flame on the shell.` |"]
    ghi(os.path.join(PK, "HUONG_DAN.md"), gd)


if __name__ == "__main__":
    main()
