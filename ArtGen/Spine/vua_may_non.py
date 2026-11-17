# -*- coding: utf-8 -*-
"""Vua robot non: DẠNG 1 của vua robot (dạng 2 = inbox/vua_may_1: vua giáp vàng bốn cánh lông trắng, hào quang nguyệt quế, quyền trượng
Mặt Trời + ba hành tinh), trên CÙNG rig monster_3637 (cùng xương, lưới, clip, chân ống lồng, cánh).

Người dùng 2026-11-17: "làm dạng 1 cho tướng thứ 10 đảo kim". Máy C (rig dựng lại từ bản quét lại `D:\\Ripper\\SwordxStaff\\scan\\monster_3637`).
Tỉ lệ đổi THẲNG trên .atomik dạng 2 (`mo_xe/atomik_dang.scale_bones`, như dạng non Giác Mộc / Thanh Long): đầu × 1,4 (vương miện, mặt, râu
theo), bốn cánh × 0,55, hào quang × 0,55, ba hành tinh × 0,75; thân, tay, chân, quyền trượng giữ (chân là IK đã nướng: đổi khối hông là hở).

    vua_may_non.py soi         soi tỉ lệ ở các clip gắt (da dạng 2) → inbox/vua_may_non/mau/_soi_ti_le.png
    vua_may_non.py khung       bố cục (mau/bo_cuc.png, chụp bằng runtime Spine thật) → mau/bo_cuc_khung.png 1536 × 1024 (+ .json)
    vua_may_non.py concept     ba file prompt concept → gui_gpt/vua_may_non/luot_1_concept_<A|B|C>.txt + HUONG_DAN.md
    (người dùng chọn A → tai_ve/L1_duyet.png; mảnh: vua_may_non_manh.py)
    VM_DANG=non vua_may_rig.py dựng rig da dạng 1 ở tỉ lệ dạng 2 → inbox/vua_may_non/rig/lon/
    vua_may_non.py rig         đổi tỉ lệ xương → inbox/vua_may_non/rig/vua_may_non.atomik (+ game.height mới) + trang xem rig/xem.html
    vua_may_non.py soi_rig     khung 0 idle cạnh concept A (rig/_so_concept.png, _so_dau.png) + tờ khung từng clip (rig/khung_<clip>.png)
"""
import json
import os
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "mo_xe"))
sys.path.insert(0, HERE)
BASE = os.path.join(HERE, "inbox", "vua_may_non")
MAU = os.path.join(BASE, "mau")
TAI = os.path.join(BASE, "tai_ve")
GUI = os.path.join(HERE, "gui_gpt", "vua_may_non")
RIG2 = os.path.join(HERE, "inbox", "vua_may_1", "rig", "vua_may.atomik")
DANG2 = os.path.join(HERE, "inbox", "vua_may_1", "tai_ve", "L1_duyet.png")
TI_LE = os.path.join(MAU, "ti_le.json")
KHUNG = (-1250.0, -80.0, 1250.0, 1680.0)          # khung nhìn bố cục (đơn vị rig), dùng chung cho dạng 2 và dạng 1 khi so
W, H = 1536, 1024
MUC = "#2E2012"


def Wp(p):
    return os.path.normpath(p)


def ghi(p, lines):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def soi():
    """da dạng 2 ở tỉ lệ dạng 1, các khung gắt của từng clip (vẽ bằng bộ vẽ Python chép AtomikPose)."""
    import atomik_dang as A
    J, img, _ = A.load(RIG2)
    A.scale_bones(J, json.load(open(TI_LE, encoding="utf-8")))
    hang = [("idle", [0.0, 0.9, 1.8]), ("walk", [0.0, 0.45, 0.9]), ("appear", [0.5, 1.0, 1.6]), ("attack", [0.3, 0.45, 0.8]),
            ("cast", [0.6, 1.0, 1.2]), ("skill", [0.5, 1.2, 2.0]), ("skill", [2.45, 2.9, 3.3]), ("hit", [0.1, 0.25, 0.4]),
            ("die", [0.4, 0.9, 1.4])]
    Ps = []
    for c, ts in hang:
        ci = A.clip(J, c)
        Ps += [(c, t, A.Pose(J).at(ci, t)) for t in ts]
    bs = np.array([A.bounds(P) for _, _, P in Ps])
    box = (bs[:, 0].min() - 20, bs[:, 1].min() - 20, bs[:, 2].max() + 20, bs[:, 3].max() + 20)
    sc = 0.16
    ims = [A.render(J, img, P, box, sc, bg=(150, 150, 150)).convert("RGB") for _, _, P in Ps]
    cot = 6
    w, h = ims[0].size
    o = Image.new("RGB", (cot * w, ((len(ims) + cot - 1) // cot) * h), (150, 150, 150))
    from PIL import ImageDraw
    d = ImageDraw.Draw(o)
    for i, (im, (c, t, _)) in enumerate(zip(ims, Ps)):
        o.paste(im, ((i % cot) * w, (i // cot) * h))
        d.text(((i % cot) * w + 8, (i // cot) * h + 6), f"{c} {t:.2f}", fill=(255, 255, 255))
    p = os.path.join(MAU, "_soi_ti_le.png")
    o.save(p)
    print(p, o.size)


def khung():
    im = Image.open(os.path.join(MAU, "bo_cuc.png")).convert("RGB")
    k = min(980.0 / im.height, 1480.0 / im.width)
    im2 = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    can = Image.new("RGB", (W, H), (255, 255, 255))
    ox, oy = (W - im2.width) // 2, (H - im2.height) // 2
    can.paste(im2, (ox, oy))
    p = os.path.join(MAU, "bo_cuc_khung.png")
    can.save(p)
    json.dump(dict(k=k, ox=ox, oy=oy, khung=KHUNG, w_bo_cuc=im.width, h_bo_cuc=im.height), open(p[:-4] + ".json", "w"), indent=1)
    print(p, f"k {k:.3f}, lệch {ox},{oy}")


GIU = ("KEEP (they make it the same family line as image 2): a stocky ROBOT KING character in three-quarter view facing RIGHT, "
       "standing on two short armoured robot legs with big boots; plate armour on chest, shoulders and big round forearms; dark "
       "three-fingered hands; the NEAR hand (left in the picture) holds a tall thin SCEPTRE planted upright down to the ground, topped by a "
       "small tower head carrying a small SUN with rays; three small PLANETS float beside the sun (a blue-green EARTH, a small "
       "rust-red MARS, a small grey MERCURY); the FAR hand (right) is a fist in front of the chest; a short red CAPE over the near shoulder "
       "and a blue SASH over the far shoulder; FOUR feathered WINGS float behind the back (two upper, two lower) and a round HALO ring "
       "floats behind the head. Every part in the same place and at the same size as in image 1.")

HUONG = {
    "A": ("hoàng tử robot (Claude đề xuất)",
          "cùng màu dạng 2 (vàng hoàng kim + bạc, áo choàng đỏ, dải lam) nhưng NON: mặt robot trẻ KHÔNG RÂU (tấm mặt bạc tròn, hai mắt "
          "vàng tròn to, mũi tròn nhỏ), vương miện THẤP ba chóp nhỏ (vương miện hoàng tử), giáp ít tấm, viền ít; bốn cánh nhỏ lông trắng "
          "ngọn vàng (lông non ngắn tròn), hào quang chỉ là một vòng vàng mảnh có ít hạt",
          ["COLOURS: the same family colours as image 2: flat gold #F2B935 armour with silver-grey #A9AEB8 plates, red #C8322B cape with a "
           "cream fur edge, blue #2F6FD0 sash, dark #4A4A55 hands.",
           "HEAD: a NEW SHAPE, not the old bearded king of image 2: a YOUNG robot PRINCE face with NO BEARD and NO MOUSTACHE: a smooth "
           "rounded silver face plate, TWO BIG ROUND golden-yellow eyes #F8C44C with dark pupils and one small white dot each, small "
           "determined brows, a small round nose, a short straight mouth line. On top a LOW PRINCE CROWN: a plain gold band with THREE small "
           "rounded points and one small red jewel (much lower and simpler than the castle crown of image 2). Same size and place as the "
           "head of image 1.",
           "ARMOUR: LIGHTER and SIMPLER than image 2: fewer plates, thin gold rims, no engraved patterns, at most one small gear emblem.",
           "WINGS: the four small wings of image 1 with SHORT ROUNDED young feathers, white with pale-gold tips, fewer feathers (one layer "
           "plus small coverts), a small gold joint at each wing root.",
           "HALO: only a THIN plain gold ring with five small pearls (no laurel leaves).",
           "SCEPTRE: the same tall sceptre with the small sun and the three small planets."]),
    "B": ("tiểu vương đồng thau",
          "giáp ĐỒNG THAU + thép xám (chưa thành vàng), mặt robot trẻ không râu chỉ một bộ ria nhỏ bạc, mắt lam; vương miện đồng thau "
          "chóp tròn; cánh lông xám bạc ngọn đồng (cánh máy non); hào quang bánh răng đồng mảnh",
          ["COLOURS: flat BRASS #D9A848 armour (darker brass #B0863A on side faces) with steel-grey #8F96A3 plates, a dark red #A12C28 cape "
           "with a cream edge, a teal #2F8F9A sash, dark #4A4A55 hands.",
           "HEAD: a NEW SHAPE, not the bearded king of image 2: a YOUNG robot face, NO BEARD, only a tiny curled silver moustache: a "
           "rounded steel face plate with TWO BIG ROUND light-blue eyes #7FD3F0 (dark pupils, one white dot each), small determined brows. "
           "On top a small BRASS crown with four ROUND KNOBS. Same size and place as the head of image 1.",
           "ARMOUR: simple brass plates with a few round rivets, no engraved patterns.",
           "WINGS: the four small wings of image 1 as young MECHANICAL wings: thin brass wing arms with short rounded steel-grey feathers "
           "tipped with brass.",
           "HALO: a THIN brass GEAR RING (a ring with small teeth), no leaves.",
           "SCEPTRE: the same tall sceptre (brass head) with the small sun and the three small planets."]),
    "C": ("hoàng tử bạc men lam",
          "giáp BẠC sáng + men LAM + viền vàng mảnh; mặt robot trẻ không râu, mắt vàng; vương miện vòng bạc một ngọc lam; áo choàng lam "
          "đậm; cánh lông trắng ngọn lam nhạt; hào quang vòng sao nhỏ",
          ["COLOURS: flat bright SILVER #C9CDD6 armour with ENAMEL BLUE #3E78C8 panels and thin gold #E2B44A rims, a deep blue #24408F cape "
           "with a cream edge, a gold sash, dark #4A4A55 hands.",
           "HEAD: a NEW SHAPE, not the bearded king of image 2: a YOUNG robot PRINCE face, NO BEARD, NO MOUSTACHE: a smooth rounded silver "
           "face plate, TWO BIG ROUND golden-yellow eyes #F8C44C (dark pupils, one white dot each), small determined brows, a small nose. "
           "On top a slim SILVER CIRCLET crown with one blue jewel in front and two small upward points. Same size and place as the head "
           "of image 1.",
           "ARMOUR: simple silver plates with blue enamel panels and thin gold rims, no engraved patterns.",
           "WINGS: the four small wings of image 1 with short rounded white feathers tipped with pale blue #A9CBEF.",
           "HALO: a THIN gold ring with five small five-pointed stars on it.",
           "SCEPTRE: the same tall sceptre (silver and gold) with the small sun and the three small planets."]),
}

STYLE = (f"DRAWING STYLE: exactly the hand-drawn style of image 2: a wobbly dark-brown ink outline ({MUC}, about 7 px) round every piece, "
         "thin ink lines for the few inner lines, every area ONE flat colour with visible coloured-pencil / wax-crayon hatching. No shading, "
         "no highlights, no white shine streaks, no gradients, no glow, no shadows. VERY SIMPLE DESIGN, FEW DETAILS: fewer details than "
         "image 2, nothing beyond what is listed.")


def concept():
    bc = os.path.join(MAU, "bo_cuc_khung.png")
    R = [(bc, "the POSE AND PROPORTION GUIDE, 1536x1024, white background: OUR robot king redrawn by computer at the proportions of its "
              "YOUNG first form (a much bigger head, four much smaller wings, a smaller halo, smaller planets), still wearing the look of "
              "its final form (small seams between pieces are only computer artefacts). It gives the exact POSE, the PROPORTIONS and the "
              "PLACE and SIZE of every part: head, crown, chest, shoulder plates, both arms and hands, sceptre, sun, planets, cape, sash, "
              "hip block, both legs and boots, four wings, halo. Keep them. Change the head, the materials and the details as described.",
          "Hình bố cục dạng 1 (1536 × 1024, nền trắng): rig dạng 2 đổi tỉ lệ (đầu × 1,4, bốn cánh × 0,55, hào quang × 0,55, hành tinh × 0,75), "
          "da tạm dạng 2. Giữ dáng, tỉ lệ, chỗ và cỡ từng bộ phận"),
         (DANG2, "the APPROVED FINAL FORM of the same character (an old robot king in gold armour with a castle crown, a white beard, four "
                 "big white-and-gold feathered wings, a laurel halo, a sceptre with the sun and three planets), 1536x1024, white "
                 "background. It gives the hand-drawn style. The young form must look clearly YOUNGER, CUTER and LESS GRAND (a prince, not "
                 "yet a king), but of the same family line.",
          "Concept dạng 2 đã duyệt (vua già vàng, râu trắng, bốn cánh lông, hào quang nguyệt quế): lấy nét vẽ và nét chung của dòng; "
          "dạng 1 trẻ hơn, gọn hơn")]
    hd = ["# Gói GPT: vua robot non, dạng 1 (vua_may_non), tướng 10 / boss đảo Kim", "",
          "## Lượt 1: concept dạng 1, ba hướng (2026-11-17)", "",
          "Dạng đã làm (vua già vàng, râu trắng, bốn cánh lông, hào quang nguyệt quế) là dạng 2. Dạng 1 trên cùng rig: tỉ lệ đã đổi ở rig "
          "(đầu × 1,4, bốn cánh × 0,55, hào quang × 0,55, ba hành tinh × 0,75; thân, tay, chân, quyền trượng giữ). Ba hướng đều là HOÀNG TỬ "
          "robot (chưa thành vua): bỏ râu, vương miện thấp, giáp ít chi tiết; giữ đủ quyền trượng Mặt Trời + ba hành tinh, bốn cánh nhỏ, "
          "vòng hào quang mảnh (clip đòn và chiêu dùng các mảnh đó).", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    hd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
    hd += [""]
    for k, (vi, vi2, doi) in HUONG.items():
        out = os.path.join(TAI, f"L1_{k}.png")
        p = os.path.join(GUI, f"luot_1_concept_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {e}" for i, (r, e, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
              f"If a file with that name already exists, save as L1_{k}_2.png, L1_{k}_3.png ... in the same folder. Do not edit, move or "
              "delete any other file.", "",
              "TASK: draw the YOUNG FIRST FORM of our robot king (a young robot PRINCE) as ONE picture: the SAME pose and proportions as "
              "image 1, every part in the same place and at the same size (if the new picture were laid over image 1, the head, crown, "
              "chest, arms, hands, sceptre, sun, planets, cape, hip block, legs, boots, the four wings and the halo must coincide), but "
              "with the new head, colours and details described below, in the drawing style of image 2.", "",
              GIU, "",
              "CHANGE:"] + [f"- {d}" for d in doi] + ["",
              STYLE, "",
              "Mood: a young robot prince, small but proud and ready to fight (a game boss's first form), determined eyes; cute but not a "
              "mascot, not scary. Both boots stand on the ground; the sceptre stands upright.", "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow; the character at the same place "
              "and size as in image 1. No sparkles, no glow, no light rays, no speed lines, no labels, no frame."]
        ghi(p, t)
        hd += [f"- **Hướng {k}** ({vi}: {vi2}): chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…)."]
        print(p)
    hd += ["", "Bản được chọn chép thành `L1_duyet.png` cùng thư mục.", "",
           "Kiểm: đúng dáng, tỉ lệ, chỗ và cỡ từng bộ phận như ảnh 1 (đầu to, bốn cánh nhỏ, hào quang nhỏ, quyền trượng dựng tới đất); KHÔNG "
           "râu; vương miện thấp; vẫn nhận ra cùng dòng với ảnh 2; tô phẳng, không bóng; nền trắng tinh.", "",
           "Câu sửa nhanh: \"same pose and size as image 1\"; \"no beard, young prince face\"; \"flat colours only, no shading, no glow\"."]
    ghi(os.path.join(GUI, "HUONG_DAN.md"), hd)


RIG_LON = os.path.join(BASE, "rig", "lon", "vua_may_non.atomik")       # VM_DANG=non vua_may_rig.py: da dạng 1, tỉ lệ dạng 2
RA = os.path.join(BASE, "rig")
CANH = ("cw_", "canh_", "hao_quang", "fx_", "sau_")


def _cao(J):
    import atomik_dang as A
    P = A.Pose(J).at(None, 0.0)
    ys = [V[:, 1].max() for s, a, V, al in P.items() if not J["slots"][s]["name"].startswith(CANH)]
    return float(max(ys))


def rig():
    """rig_lon (tỉ lệ dạng 2) → đổi tỉ lệ xương → rig/vua_may_non.atomik (+ game.height mới), trang xem, tờ soi."""
    import subprocess
    import atomik_dang as A
    J, img, ver = A.load(RIG_LON)
    h0 = J["game"]["height"]
    A.scale_bones(J, json.load(open(TI_LE, encoding="utf-8")))
    J["game"]["height"] = round(_cao(J), 2)
    os.makedirs(RA, exist_ok=True)
    p = os.path.join(RA, "vua_may_non.atomik")
    kq = A.save(p, J, img, ver)
    print(f"{p}: {os.path.getsize(p) // 1024} KB; game.height {h0:.0f} → {J['game']['height']:.0f}; {kq}")
    # chân dung vuông 512, nền trong suốt (như quai/soi.chan_dung): khung 0 idle, ôm cả con
    P = A.Pose(J).at(A.clip(J, "idle"), 0.0)
    b = A.bounds(P)
    side = max(b[2] - b[0], b[3] - b[1]) * 1.12
    cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
    im = A.render(J, img, P, (cx - side / 2, cy - side / 2, cx + side / 2, cy + side / 2), 1024 / side, bg=None)
    im.resize((512, 512), Image.LANCZOS).save(os.path.join(RA, "chan_dung.png"))
    print(os.path.join(RA, "chan_dung.png"))
    repo = os.path.normpath(os.path.join(HERE, "..", ".."))
    subprocess.run([sys.executable, "-I", os.path.join(HERE, "mo_xe", "atomik_xem.py"), repo, RA, p,
                    "Vua robot non dạng 1 (vua_may_non): tướng 10 đảo Kim"], check=True)


def soi_rig():
    """(1) khung 0 idle của rig dạng 1 đặt cạnh concept A (cùng phép căn của vua_may_non_manh); (2) tờ khung các clip."""
    import atomik_dang as A
    import vua_may_non_manh as VM
    J, img, _ = A.load(os.path.join(RA, "vua_may_non.atomik"))
    c2w, w2c, upc = VM.phep_can()
    x0, y1 = c2w([[0, 0]])[0]
    x1, y0 = c2w([[W, H]])[0]
    P = A.Pose(J).at(A.clip(J, "idle"), 0.0)
    im = A.render(J, img, P, (x0, y0, x1, y1), 1.0 / upc, bg=(255, 255, 255)).convert("RGB").resize((W, H))
    con = Image.open(VM.CON).convert("RGB").resize((W, H))
    o = Image.new("RGB", (W * 2 + 20, H), (255, 255, 255))
    o.paste(con, (0, 0))
    o.paste(im, (W + 20, 0))
    o = o.resize((o.width // 2, o.height // 2), Image.LANCZOS)
    o.save(os.path.join(RA, "_so_concept.png"))
    print(os.path.join(RA, "_so_concept.png"))
    # cận đầu, cánh, hào quang
    can = (480, 180, 1180, 700)
    a_ = con.crop(can)
    b_ = im.crop(can)
    o2 = Image.new("RGB", (a_.width * 2 + 10, a_.height), (255, 255, 255))
    o2.paste(a_, (0, 0))
    o2.paste(b_, (a_.width + 10, 0))
    o2.save(os.path.join(RA, "_so_dau.png"))
    hang = [("idle", [0.0, 0.67, 1.33, 2.0]), ("walk", [0.0, 0.33, 0.67, 1.0]), ("appear", [0.3, 0.6, 1.0, 1.4, 1.7, 2.1]),
            ("attack", [0.15, 0.35, 0.45, 0.55, 0.8, 1.1]), ("cast", [0.4, 0.8, 1.0, 1.1, 1.24, 1.8]),
            ("skill", [0.4, 1.0, 1.5, 2.0, 2.45, 2.9, 3.2, 3.55]), ("hit", [0.1, 0.25, 0.4]), ("die", [0.3, 0.6, 0.9, 1.2])]
    for c, ts in hang:
        ci = A.clip(J, c)
        Ps = [A.Pose(J).at(ci, t) for t in ts]
        bs = np.array([A.bounds(Q) for Q in Ps])
        box = (bs[:, 0].min() - 20, bs[:, 1].min() - 20, bs[:, 2].max() + 20, bs[:, 3].max() + 20)
        sc = min(0.32, 700.0 / max(1.0, box[3] - box[1]))
        ims = [A.render(J, img, Q, box, sc, bg=(150, 150, 150)).convert("RGB") for Q in Ps]
        cot = min(6, len(ims))
        w, h = ims[0].size
        sh = Image.new("RGB", (cot * w, ((len(ims) + cot - 1) // cot) * h), (150, 150, 150))
        for i, q in enumerate(ims):
            sh.paste(q, ((i % cot) * w, (i // cot) * h))
        pth = os.path.join(RA, f"khung_{c}.png")
        sh.save(pth)
        print(pth, sh.size)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "soi":
        soi()
    elif cmd == "khung":
        khung()
    elif cmd == "concept":
        concept()
    elif cmd == "rig":
        rig()
    elif cmd == "soi_rig":
        soi_rig()
    else:
        print(__doc__)
