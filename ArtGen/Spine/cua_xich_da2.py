# -*- coding: utf-8 -*-
"""Tinh linh đuôi máy cưa DẠNG 2 (cua_xich_2, suất phi_thuong đảo Kim): concept trên CÙNG rig với dạng 1 (monster_3374).

Người dùng 2026-11-16 (sau khi dạng 1 vào game): "làm dạng 2 của tướng này". Dạng 2 dùng cùng xương, lưới, clip; tỉ lệ đổi ở rig
(cua_xich_rig.py CX_DANG=2: thân 1,12, đầu 0,82, gốc đuôi 1,12, tay 0,9). Hình bố cục dựng bằng da dạng 1 (`mau/bo_cuc.png`) làm ảnh mẫu 1 để
concept bám đúng cái rig dựng ra được (skill pokiclash-spine-rig, "DẠNG KHÁC trên CÙNG rig gốc": tỉ lệ trước, concept sau).

    CX_DANG=2 py -3 -I ArtGen/Spine/cua_xich_rig.py bo_cuc ArtGen/Spine/inbox/cua_xich_2/mau/bo_cuc.png
    py -3 -I ArtGen/Spine/cua_xich_rig.py bo_cuc ArtGen/Spine/inbox/cua_xich_2/mau/bo_cuc_d1.png
    py -3 -I ArtGen/Spine/cua_xich_da2.py concept    gói gui_gpt/cua_xich_2/luot_1_concept_<A|B|C>.txt + HUONG_DAN.md
"""
import os
import sys

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1536, 1024
BASE2 = os.path.join(HERE, "inbox", "cua_xich_2")
MAU2 = os.path.join(BASE2, "mau")
TAI2 = os.path.join(BASE2, "tai_ve")
GUI2 = os.path.join(HERE, "gui_gpt", "cua_xich_2")
D3 = os.path.join(HERE, "inbox", "cua_xich_1", "tai_ve", "L1_duyet.png")
MUC = "#2B2118"


def Wp(p):
    return os.path.normpath(p)


def ghi(p, lines):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def khung(ten_vao, ten_ra, cao=900.0):
    """ảnh bố cục đặt giữa khung 1536 × 1024 nền trắng (cùng tỉ lệ px / đơn vị cho dạng 1 và dạng 2: cao theo dạng 1)."""
    im = Image.open(os.path.join(MAU2, ten_vao)).convert("RGB")
    ref = Image.open(os.path.join(MAU2, "bo_cuc_d1.png"))
    k = cao / ref.height
    im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    can = Image.new("RGB", (W, H), (255, 255, 255))
    can.paste(im, ((W - im.width) // 2, (H - im.height) // 2 + 20))
    p = os.path.join(MAU2, ten_ra)
    can.save(p)
    return p


# ba hướng tiến hóa (Claude đề xuất, chờ người dùng chọn). Luật dạng cuối (skill mục 0a): màu chủ đạo ĐẬM hơn, đổi chi tiết đặc trưng, đổi dáng
# mảnh nhận diện; vẫn nhận ra cùng dòng; ít chi tiết như con gốc (memory concept-it-chi-tiet: không tự thêm vết nứt, huy hiệu, gai lẻ).
HUONG = {
    "A": ("quặng gỉ dữ", "mai sắt đen viền gỉ, quặng to thêm thành chùm 5 cột đầu gỉ đỏ, sừng dài cong hơn, mõm hai nanh, đĩa cưa răng to viền gỉ",
          ["SHELL: the three armour bands become darker blackened iron #45464B, each band edge with a thin rust-orange #C2592A rim line.",
           "HORNS (both, the near one and the far one behind the ore): longer and more curved, sweeping forward like hooks, dark iron on top and "
           "rust-red #A8432A underneath.",
           "IRON ORE: a bigger cluster of FIVE hexagonal ore columns standing in the middle of the head between the two horns (the middle one "
           "the tallest), dark iron grey faces with deep rust-red #B1452C tops.",
           "FACE: the same pale face but a little greyer #C9C0B7; the snout with TWO small white fangs; the cheek marks become three short "
           "slanted rust-red slashes.",
           "TAIL SAW: the housing plate blackened iron with one rust-orange stripe along its edge; the disc dark iron with its EIGHT square "
           "teeth bigger and pale steel #D9D9D9, a rust-orange ring around the hub.",
           "BODY, LEGS, PAW: blackened iron #45464B; the claws ivory. The pull ring brass, the cord rust-brown."]),
    "B": ("thép nung", "thép súng sẫm, mép các đốt mai như răng cưa, quặng thành thỏi sắt nung đầu cam đỏ, đĩa cưa thép sáng răng nhọn vuông",
          ["SHELL: the three armour bands dark gunmetal #3E4249; the back edge of each band becomes a row of short blunt SAW TEETH (like the "
           "edge of a saw blade), all leaning backward.",
           "HORNS (both): thicker, dark gunmetal with a hot orange-red #D2502A underside.",
           "IRON ORE: the ore columns become fewer and BIGGER: three thick iron INGOT-like columns in the middle of the head, gunmetal faces "
           "with flat red-hot orange #E0662B tops (flat colour, no glow).",
           "FACE: pale grey #CFC6BD; a heavier brow; the snout with one bigger fang; the cheek marks two thick orange slashes.",
           "TAIL SAW: the housing plate gunmetal with an orange-red hub ring; the disc bright steel #C9CDD3 with EIGHT square teeth, each "
           "tooth tipped orange-red.",
           "BODY, LEGS, PAW: dark gunmetal #3E4249, claws ivory; the pull ring brass, the cord dark red-brown."]),
    # lần 2: người dùng "tôi thích B hơn nhưng nhìn chưa đủ khác biệt, phải to hơn và chiến hơn" → rig to hơn (thân 1,22, đuôi cưa 1,3,
    # chân 1,25, đầu 0,8; bố cục mới) + B đẩy mạnh: sừng thú húc to chĩa tới, gờ mày khấc chữ V, hai nanh to, thỏi quặng cao to, răng cưa sắc ở
    # mép mai, thân có hai đốt giáp răng cưa như mai, vuốt dài
    "B2": ("thép nung, to và chiến", "như B nhưng sừng thú húc to chĩa tới, mày khấc chữ V, hai nanh to, thỏi quặng cao to, mép mai răng cưa "
           "sắc, thân hai đốt giáp răng cưa, vuốt dài",
           ["SHELL: the three armour bands dark gunmetal #3A3D44; the back edge of each band is a row of SHARP saw teeth (all leaning "
            "backward, clearly bigger than small bumps); the FRONT band is a very heavy scowling BROW with a deep V-shaped notch right "
            "above the eye, cutting across the top half of the eye so the eye looks narrowed and furious.",
            "HORNS (both, the near one and the far one behind the ore): MUCH BIGGER and thicker, curving forward and up like the horns of a "
            "charging bull, sharp tips, dark gunmetal on top and hot orange-red #D2502A underneath.",
            "IRON ORE: three BIG tall iron INGOT-like columns standing in the middle of the head (clearly taller and thicker than in "
            "image 1), gunmetal faces #4A4E56 with flat red-hot orange #E0662B tops (flat colour, no glow).",
            "FACE: pale grey #C8BFB6; a short heavy snout baring TWO big white fangs; the slit pupil thin; the cheek marks two thick "
            "orange-red slashes.",
            "BODY: dark gunmetal #3A3D44 covered by TWO overlapping armour bands like the head shell (each band edge a row of sharp saw "
            "teeth), inside the same round body outline; the pull ring brass, the cord dark red-brown, the hole low on the belly as before.",
            "PAW: dark gunmetal with THREE long hooked ivory claws.",
            "LEGS: dark gunmetal, the near thigh dome with saw-tooth ridges instead of soft ribs (same outline).",
            "TAIL SAW: the housing plate dark gunmetal with an orange-red ring round the hub and one orange-red stripe along its edge; the "
            "disc bright steel #C9CDD3 with EIGHT square teeth, each tooth tipped orange-red."]),
    "C": ("thép lam bạc", "mai thép lam sẫm viền bạc, quặng tinh thể sắt lam đầu bạc, sừng bạc, đĩa cưa bạc thân lam",
          ["SHELL: the three armour bands deep blue steel #3F4A60 with a thin silver #C8CED8 rim line on each band edge.",
           "HORNS (both): longer, curved forward, silver #C8CED8 on top and deep blue steel underneath.",
           "IRON ORE: four tall hexagonal iron-ore columns in the middle of the head, blue-grey steel faces #5B6780 with silver-white "
           "#E3E7EE tops.",
           "FACE: pale cool grey #D3D2D0; the snout with one fang; the cheek marks two short slanted deep-blue slashes.",
           "TAIL SAW: the housing plate deep blue steel with a silver hub ring; the disc deep blue steel with EIGHT silver square teeth.",
           "BODY, LEGS, PAW: deep blue steel #3F4A60, claws silver-white; the pull ring silver, the cord dark blue-grey."]),
}


def concept():
    bc2 = khung("bo_cuc.png", "bo_cuc_khung.png")
    bc1 = khung("bo_cuc_d1.png", "bo_cuc_d1_khung.png")
    R = [(bc2, "the LAYOUT of the new form, 1536x1024, white background: OUR first-form iron beast re-proportioned for its evolved form "
               "(smaller head, bigger body, bigger tail saw), in its idle pose, facing right: a three-band slate armour shell over the head "
               "with a hooked horn on each side (the far horn behind the ore), iron ore columns standing in the middle of the head, a pale "
               "face with a short snout and a fang, one amber slit-pupil eye cut across its top half by the shell, ONE small paw holding a "
               "pull ring with a short cord going into the belly, short legs, and on the left a tail with an oblong saw housing and a disc "
               "with eight square teeth. Keep its POSE, its PROPORTIONS and the PLACE and SIZE of every piece.",
          "Bố cục dạng 2 (1536 × 1024, nền trắng): dạng 1 trong game dựng lại trên rig với đầu nhỏ hơn, thân to hơn, đuôi cưa to hơn"),
         (bc1, "the FIRST FORM of this character as it is now in the game, 1536x1024, white background: its identity to keep (shell bands, "
               "two hooked horns, ore columns in the middle of the head, snout with fang, slit eye, pull-ring cord, saw tail).",
          "Dạng 1 như đang chạy trong game (hình rig): nhận diện dòng"),
         (D3, "the APPROVED concept drawing of the first form, 1536x1024, white background: take ONLY the hand-drawn look from it (wobbly "
              "brown ink line, crayon hatching, flat colour). Its ore position and its second paw are outdated: follow image 1 for those.",
          "Concept D3 đã duyệt của dạng 1: chỉ lấy nét vẽ")]
    hd = ["# Gói GPT: tinh linh đuôi máy cưa DẠNG 2 (cua_xich_2), tướng 4 đảo Kim (suất phi_thuong)", "",
          "Người dùng 2026-11-16, sau khi dạng 1 vào game: \"làm dạng 2 của tướng này\". Dạng 2 dùng CÙNG rig, cùng clip; tỉ lệ đổi ở rig (thân "
          "1,12, đầu 0,82, đuôi 1,12, tay 0,9); hình bố cục dựng bằng da dạng 1 làm ảnh mẫu 1. Ảnh con gốc không đính.", "",
          "## Lượt 1: concept dạng 2, ba hướng (Claude đề xuất, chờ người dùng chọn)", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    hd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
    hd += [""]
    chi = sys.argv[2:] or list(HUONG)
    for k, (vi, vi2, doi) in HUONG.items():
        out = os.path.join(TAI2, f"L1_{k}.png")
        p = os.path.join(GUI2, f"luot_1_concept_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {e}" for i, (r, e, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
              f"If a file with that name already exists, save as L1_{k}_2.png, L1_{k}_3.png ... in the same folder. Do not edit, move or "
              "delete any other file.", "",
              "TASK: draw the EVOLVED SECOND FORM of our iron beast (image 2 is its first form): an older, " +
              ("much BIGGER, heavier and far FIERCER battle-hardened " if k == "B2" else "stronger, fiercer ") + "wild iron beast of the "
              "same line" + (", clearly different from the first form at a glance" if k == "B2" else "") + ". ONE picture in EXACTLY the pose, proportions and layout of image 1: every piece in the same place "
              "and at the same size (head shell bands, both horns, ore cluster, face and snout, eye, the one paw with the pull ring and "
              "cord, body, legs, tail housing, saw disc), with the same overlaps, so that it fits the same animation puppet. Only ONE paw "
              "shows (as in image 1), only ONE eye. Keep the identity: three overlapping armour bands over the head, the front band a "
              "heavy brow cutting across the top half of the eye, a hooked horn on each side, iron ore in the middle of the head, short "
              "snout with fang, pull ring on the belly, oblong saw housing with a hub, round disc with square teeth. Change ONLY what is "
              "listed:", ""]
        t += [f"- {d}" for d in doi]
        t += ["",
              f"DRAWING STYLE (very important): hand-drawn on paper like images 2 and 3: a wobbly dark-brown ink outline ({MUC}, about 7 px) "
              "round every piece, thinner ink lines for the few inner structural edges, every area ONE flat colour with visible "
              "coloured-pencil / wax-crayon hatching. No shading, no highlights, no white shine streaks, no gradients, no glow, no "
              "shadows, no gloss, no sparkles. SIMPLE DESIGN like the first form: no extra rivets, bolts, cables, cracks, scratches, "
              "badges, runes or extra spikes beyond what is listed.", "",
              "Mood: a tough, fierce, determined wild iron beast ready to fight (a game hero), not a cute mascot, not scary. Both legs, the "
              "paw and the tail base stay attached to the body exactly as in image 1.", "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow; the character at the same "
              "place and size as in image 1. No sparkles, no dust, no speed lines, no labels, no frame."]
        if k in chi:                                   # chỉ ghi file prompt của hướng được chọn (giữ nguyên file cũ của hướng khác)
            ghi(p, t)
            print(p)
        hd += [f"- **Hướng {k}** ({vi}: {vi2}): chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…)."]
    hd += ["", "Bản được chọn chép thành `L1_duyet.png` cùng thư mục.", "",
           "Kiểm: đúng dáng, đúng tỉ lệ, đúng chỗ và cỡ từng mảnh như ảnh 1 (chồng lên phải trùng, trừ phần đổi dáng: sừng, quặng, mép mai); "
           "vẫn nhận ra cùng dòng với dạng 1; màu đậm hơn dạng 1; một tay, một mắt; đĩa cưa răng vuông; tô phẳng, không bóng; nền trắng tinh.",
           "", "Câu sửa nhanh: \"keep every piece at the same place and size as in image 1\"; \"only one paw, only one eye\"; "
           "\"flat colour only, no shading\"."]
    ghi(os.path.join(GUI2, "HUONG_DAN.md"), hd)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "concept":
        concept()
    else:
        print(__doc__)
