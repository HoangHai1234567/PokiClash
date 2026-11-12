# -*- coding: utf-8 -*-
"""Rồng vây NON (dạng 1 trong game; concept duyệt 2026-11-12 "ổn rồi": inbox/rong_vay_non/tai_ve/L1_duyet.png).
Cùng rig, cùng lưới, cùng clip với dạng 2 (`rong_vay_1`); chỉ đổi tỉ lệ dáng gốc (rong_vay_rig.py, RV_DANG=non) và DA.
Da làm bằng cách CHUYỂN DA: tờ hướng dẫn = chính ảnh part ĐÃ XONG của dạng 2 (đúng khung, đã xoá vạch nối, đã vá) xếp theo ô;
Codex vẽ lại từng part theo thiết kế rồng non, giữ nguyên hình bóng; mã lấy lại ĐỘ ĐẬM (alpha) và CHỖ KHÔNG CÓ MỰC của dạng 2 nên
mọi bước dọn chỗ nối, vá mép đã làm cho dạng 2 được thừa hưởng, không phải chạy lại.

    rong_vay_non.py to            tờ hướng dẫn G1..G6 + prompt gui_gpt/rong_vay_non/luot_2_part_G<k>.txt
    rong_vay_non.py cat [G1 ..]   cắt tờ tai_ve/N_G<k>.png → inbox/rong_vay_non/manh/{part,part_va,part_noi}/<slot>.png
    rong_vay_non.py xong          chép các part không vẽ lại (sừng, mỏ), mắt nhắm đổi màu, tờ so → sẵn sàng cho rig
Rig: RV_DANG=non py -3 -I ArtGen/Spine/rong_vay_rig.py (qua quai/khoa.py nang)."""
import json
import os
import shutil
import sys

import cv2
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
LON = os.path.join(HERE, "inbox", "rong_vay_1")
NON = os.path.join(HERE, "inbox", "rong_vay_non")
PK = os.path.join(HERE, "gui_gpt", "rong_vay_non")
MAU, TAI, MANH = os.path.join(NON, "mau"), os.path.join(NON, "tai_ve"), os.path.join(NON, "manh")
W, H = 1536, 1024
WP = os.path.normpath
# tờ → [(slot, loại)]; ô của từng slot lấy lại từ tờ của dạng 2 (TO_GOC). Không vẽ lại: sừng, mỏ (giữ đen than), vây đã bỏ (BO_VAY).
TO = {"G1": [("P_chibangR08", "song"), ("P_weiba", "vay"), ("P_shenti06", "than"), ("P_chibangL05", "song"), ("P_yuqi02", "vay")],
      "G2": [("P_chibangR06", "mang"), ("P_shenti04", "than")],
      "G3": [("P_chibangL06", "mang"), ("P_yuqi10", "vay")],
      "G4": [("P_shenti03", "than_so"), ("P_yuqi15", "vay"), ("P_shenti02", "than"), ("P_shenti05", "than")],
      "G5": [("P_yuqi14", "vay"), ("P_shenti01", "than"), ("P_yuqi05", "vay")],
      "G6": [("P_yuqi01", "vay"), ("P_yuqi07", "vay"), ("P_yuqi09", "vay"), ("P_tou", "dau"), ("P_erduo", "mao")]}
TO_GOC = {"G1": "P1", "G2": "Q2", "G3": "Q3", "G4": "Q4", "G5": "Q5", "G6": "Q6"}
GIU = ["P_yuqi03", "P_yuqi04", "P_zuiba01", "P_zuiba02"]          # chép nguyên của dạng 2
EN = {
    "than": "a stretch of the serpent BODY: the back becomes periwinkle blue (#6C86DC); the band of cream belly plates (#F3E6C4) "
            "stays exactly where it is, with its thin ink lines between the plates.",
    "than_so": "a stretch of the serpent BODY: the back becomes periwinkle blue (#6C86DC); the small cream belly patch stays. The "
               "adult wears three scallop shells on the top edge of this part: the juvenile has NONE. Leave the shell area "
               "pure WHITE (cut away) and close the back with a smooth ink outline just below where the shells were.",
    "mang": "a WING MEMBRANE: the web becomes pale aqua (#9CD3D6); the rays stay in the same places, dark blue (#3B4CA8); the round "
            "cream spots stay in the same places.",
    "song": "a WING SPAR (the bony leading edge of a wing): dark blue (#3B4CA8), plain.",
    "vay": "a FIN: the web becomes pale aqua (#9CD3D6); its rays stay in the same places, dark blue (#3B4CA8).",
    "dau": "the HEAD (without beak, horns or fins), exactly as the juvenile's head in image 1: periwinkle blue (#6C86DC); ONE big "
           "round amber eye (#F2A21E) with a dark slit pupil and one small white dot, centred where the adult's eye is but "
           "clearly bigger and rounder; a short straight dark brow line above it. Everything else plain periwinkle.",
    "mao": "the small pointed BROW CREST on top of the head: plain dark blue (#3B4CA8).",
}
VI = {"than": "khúc thân", "than_so": "khúc thân có vỏ sò (dạng 1 bỏ vỏ sò)", "mang": "màng cánh", "song": "sống cánh", "vay": "vây",
      "dau": "đầu", "mao": "mào"}


def xong2(slot):
    """ảnh part ĐÃ XONG của dạng 2 (rig đang dùng): bản vá > bản xoá vạch nối > bản cắt."""
    for d in ("part_va", "part_noi", "part"):
        p = os.path.join(LON, "manh", d, slot + ".png")
        if os.path.exists(p):
            return p, d
    raise SystemExit("thiếu part dạng 2: " + slot)


def o(to):
    K = json.load(open(os.path.join(LON, "mau", f"part_{TO_GOC[to]}.json"), encoding="utf-8"))
    out = {}
    for slot, _ in TO[to]:
        v = K[slot]
        out[slot] = (v[0], v[1], v[2], v[3], 2) if isinstance(v, list) else (v["x"], v["y"], v["w"], v["h"], v["z"])
    return out


def lam_to():
    os.makedirs(MAU, exist_ok=True)
    os.makedirs(PK, exist_ok=True)
    os.makedirs(TAI, exist_ok=True)
    duyet = os.path.join(TAI, "L1_duyet.png")
    rows = []
    for to, ds in TO.items():
        im = Image.new("RGB", (W, H), (255, 255, 255))
        O = o(to)
        for slot, _ in ds:
            x, y, w, h, z = O[slot]
            g = Image.open(xong2(slot)[0]).convert("RGBA").convert("RGBa").resize((w, h), Image.LANCZOS).convert("RGBA")
            im.paste(g, (x, y), g)
        gp = os.path.join(MAU, f"part_{to}.png")
        im.save(gp)
        out = os.path.join(TAI, f"N_{to}.png")
        p = os.path.join(PK, f"luot_2_part_{to}.txt")
        n = len(ds)
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {WP(duyet)}: the APPROVED picture of the JUVENILE form of a winged sea-serpent dragon, 1536x1024, white "
             "background. Use it for the juvenile's colours and face, the wobbly dark-brown ink line and the crayon texture.",
             f"image 2 = {WP(gp)}: PART SHEET of the ADULT form's skin, 1536x1024, white background: {n} separate cut-out parts of "
             "the creature's animation rig. The outline, size, orientation and place of every part are fixed by the rig. The "
             "colours are the ADULT's (deep indigo body, grey-teal fins).",
             "", f"SAVE: save it as a PNG to {WP(out)}",
             f"If a file with that name already exists, save as N_{to}_2.png, N_{to}_3.png ... in the same folder. Do not edit, "
             "move or delete any other file.", "",
             f"TASK: redraw image 2 as the same sheet of {n} parts wearing the JUVENILE's skin (the colours of image 1).", "",
             "RULES:",
             "- EVERY PART KEEPS ITS SILHOUETTE EXACTLY: the same outline, size, orientation and position on the canvas as in "
             "image 2. Do not rotate, mirror, move, resize, round off or simplify any shape. If the result were laid over image "
             "2, every part would cover its shape exactly.",
             "- Keep every line and pattern where image 2 has it (plate lines, rays, spots); only the COLOURS change as listed "
             "below, plus the changes written for a part.",
             "- Ink outline (dark brown #2B2118, the same thickness as in image 2) wherever image 2 has one. Where an edge of a "
             "part has NO ink outline in image 2 (a cut end that tucks under a neighbour), keep it WITHOUT outline: the colours "
             "simply run to that edge.",
             "- FLAT COLOUR, NO LIGHT, NO SHADOW: every area one even colour with loose crayon hatching as texture; no shading, "
             "no highlights, no gloss, no gradients.",
             f"- Exactly these {n} parts, pure-white background between them, nothing else: no text, no labels, no frame.", "",
             f"THE {n} PARTS (the place is the centre of the part's box on the 1536x1024 canvas):"]
        for i, (slot, loai) in enumerate(ds, 1):
            x, y, w, h, z = O[slot]
            t.append(f"{i}. at about x = {x + w / 2:.0f}, y = {y + h / 2:.0f} (about {w} px wide, {h} px tall): " + EN[loai])
        open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
        rows.append((to, p, gp, out, ", ".join(f"`{s}` ({VI[l]})" for s, l in ds)))
        print(WP(p))
    hd = os.path.join(PK, "HUONG_DAN.md")
    s = open(hd, encoding="utf-8").read() if os.path.exists(hd) else ""
    s = s.split("\n## Lượt 2")[0].rstrip("\n")
    s += ("\n\n## Lượt 2: da rồng non cho từng part (concept đã duyệt 2026-11-12: `tai_ve/L1_duyet.png`)\n\n"
          "Ảnh 1 của mọi tờ: concept rồng non đã duyệt (1536 × 1024, nền trắng). Ảnh 2: tờ part của DẠNG 2 đã xong (mỗi part nằm "
          "đúng ô, đúng khung ảnh vùng của rig; thân chàm, vây lam xám), dựng bằng `py -3 -I ArtGen/Spine/rong_vay_non.py to`. GPT "
          "vẽ lại đúng tờ đó với màu rồng non, giữ nguyên hình bóng. Cắt: `py -3 -I ArtGen/Spine/rong_vay_non.py cat G<k>` (lấy "
          "lại độ đậm và chỗ không có mực của dạng 2). Sừng, mỏ không vẽ lại (giữ đen than; sừng thu thành nụ ở rig).\n\n"
          "| Tờ | File prompt | Tờ hướng dẫn (ảnh 2) | Lưu vào | Part |\n|---|---|---|---|---|\n")
    s += "\n".join(f"| {a} | `{WP(b)}` | `{WP(c)}` | `{WP(d)}` | {e} |" for a, b, c, d, e in rows)
    s += ("\n\nKiểm mỗi tờ: đủ số part, đúng chỗ, hình bóng không đổi; thân lam nhạt, bụng kem; vây và màng lam ngọc nhạt, tia lam "
          "đậm; khúc lưng không còn vỏ sò; đầu mắt to tròn. Sai thì chạy lại với `--note \"<câu sửa>\"`.\n")
    open(hd, "w", encoding="utf-8", newline="\n").write(s)


def _gan(src, mask):
    """màu của điểm `mask` gần nhất cho mọi điểm."""
    _, lb = cv2.distanceTransformWithLabels((~mask).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
    tra = np.zeros((int(lb.max()) + 1, 3), np.uint8)
    tra[lb[mask]] = src[mask]
    return tra[lb]


def chuyen(cell, f2, z):
    """cell: RGB ô GPT vẽ (w, h theo ô); f2: RGBA ảnh đã xong của dạng 2 cỡ ô. Trả RGBA cỡ ô."""
    e = lambda r: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))  # noqa: E731
    s_ = max(1, z // 2)
    rgb = cell.copy()
    trang = rgb.min(axis=2) > 236
    nc, lab, st, _ = cv2.connectedComponentsWithStats(trang.astype(np.uint8), connectivity=4)
    for i in range(1, nc):                      # trắng nhỏ khép kín (chấm sáng mắt) là hình, không phải giấy
        if st[i, cv2.CC_STAT_AREA] < 160 * s_ * s_:
            x, y, w, h = st[i, :4]
            if x > 0 and y > 0 and x + w < trang.shape[1] and y + h < trang.shape[0]:
                trang[lab == i] = False
    ve = ~trang
    A2 = f2[..., 3].astype(np.float32) / 255.0
    gan = cv2.dilate(ve.astype(np.uint8), e(4 * s_)).astype(bool)
    alpha = A2 * gan
    muc1 = ve & (rgb.max(axis=2) < 105)
    muc2 = (A2 > 0.5) & (f2[..., :3].max(axis=2) < 105)
    muc2d = cv2.dilate(muc2.astype(np.uint8), e(3 * s_)).astype(bool)
    dac = A2 > 0.5
    vanh = (A2 > 0.02) & ~cv2.erode(dac.astype(np.uint8), e(5 * s_)).astype(bool)
    bo = vanh & muc1 & ~muc2d                                   # mực của mình ở mép mà dạng 2 đã xoá (chỗ nối, chỗ vá)
    nc, lab, st, _ = cv2.connectedComponentsWithStats((muc1 & ~bo).astype(np.uint8), connectivity=8)
    gb = cv2.dilate(bo.astype(np.uint8), e(3 * s_)).astype(bool)
    for i in range(1, nc):                                      # mẩu mực vụn còn sót cạnh đó
        if st[i, cv2.CC_STAT_AREA] < 110 * s_ * s_ and (gb & (lab == i)).any():
            bo |= lab == i
    bo = cv2.dilate(bo.astype(np.uint8), e(1)).astype(bool)
    tot = ve & ~cv2.dilate(muc1.astype(np.uint8), e(2 * s_)).astype(bool) & (rgb.min(axis=2) < 222)
    if tot.any():
        lap = cv2.medianBlur(_gan(rgb, tot), 5)
        can = (bo | ((alpha > 0.02) & ~ve)) | (ve & (rgb.min(axis=2) > 222) & vanh)
        rgb[can] = lap[can]
    # GPT tô mỗi tờ một sắc hơi khác (khúc thân này nhạt hơn khúc kia → lộ mảng khi ghép): kéo trung vị từng lớp màu về màu chuẩn
    f = rgb.astype(np.float32)
    R_, G_, B_ = f[..., 0], f[..., 1], f[..., 2]
    lop = {"cham_nhat": ((B_ > 170) & (R_ > 75) & (R_ < 155) & (B_ - R_ > 60) & (B_ - G_ > 40), (108, 134, 220)),
           "lam_ngoc": ((G_ > 170) & (B_ > 170) & (R_ > 105) & (R_ < 205) & (G_ - R_ > 25) & (B_ - G_ < 40), (156, 211, 214)),
           "tia": ((B_ > 120) & (B_ < 205) & (R_ < 85) & (B_ - R_ > 70), (59, 76, 168)),
           "kem": ((R_ > 222) & (G_ > 205) & (B_ > 160) & (B_ < 228) & (R_ - B_ > 18), (247, 232, 200))}
    for ten_, (m, dich) in lop.items():
        m = m & ve
        if m.sum() > 200:
            f[m] += np.array(dich, np.float32) - np.median(f[m], axis=0)
    rgb = np.clip(f, 0, 255).astype(np.uint8)
    return np.dstack([rgb, np.clip(alpha * 255, 0, 255).astype(np.uint8)])


def cat(tos):
    from quai import anh
    for to in tos:
        path = anh.to_moi_nhat(TAI, f"N_{to}")
        if not path:
            print(to, "chưa có ảnh")
            continue
        im = np.asarray(Image.open(path).convert("RGB").resize((W, H), Image.LANCZOS))
        for slot, (x, y, w, h, z) in o(to).items():
            cell = im[y:y + h, x:x + w]
            dich = [(slot, *xong2(slot))]
            if slot == "P_shenti06":                              # ảnh khúc đuôi dùng lại cho slot P_shenti07 (bản xoá vạch nối riêng)
                dich.append(("P_shenti07", *xong2("P_shenti07")))
            for ten, p2, d in dich:
                f2 = np.asarray(Image.open(p2).convert("RGBA").convert("RGBa").resize((w, h), Image.LANCZOS).convert("RGBA"))
                out = Image.fromarray(chuyen(cell, f2, z), "RGBA")
                if z != 2:
                    out = out.convert("RGBa").resize((w * 2 // z, h * 2 // z), Image.LANCZOS).convert("RGBA")
                dd = "part" if (d == "part_noi" and ten != "P_shenti07") else d
                os.makedirs(os.path.join(MANH, dd), exist_ok=True)
                out.save(os.path.join(MANH, dd, ten + ".png"))
                if dd == "part_va":                       # rig chỉ xét bản vá khi part/<slot>.png cũng có
                    os.makedirs(os.path.join(MANH, "part"), exist_ok=True)
                    out.save(os.path.join(MANH, "part", ten + ".png"))
                a1 = np.asarray(out)[..., 3] > 127
                a2 = np.asarray(Image.open(p2).convert("RGBA").resize(out.size))[..., 3] > 127
                print(f"  {to} {ten}: → {dd}/, phủ {100 * (a1 & a2).sum() / max(1, a2.sum()):.1f}% hình của dạng 2")


def xong():
    os.makedirs(os.path.join(MANH, "part"), exist_ok=True)
    for slot in GIU:
        shutil.copyfile(xong2(slot)[0], os.path.join(MANH, "part", slot + ".png"))
    # mắt nhắm: mảnh của dạng 2 (mí chàm) đổi sang lam nhạt của dạng 1; sống cánh cũ chỉ để rig lấy màu dải cạnh
    hsv_d = np.array([108, 134, 220], np.float32)
    for f in ("mat_nham.png",):
        src = os.path.join(LON, "manh_rig", f) if os.path.exists(os.path.join(LON, "manh_rig", f)) else os.path.join(LON, "manh", f)
        a = np.asarray(Image.open(src).convert("RGBA")).copy()
        rgb = a[..., :3].astype(np.float32)
        cham = (a[..., 3] > 0) & (rgb[..., 2] > 120) & (rgb[..., 2] > rgb[..., 0] * 1.6)
        if cham.any():
            med = np.median(rgb[cham], axis=0)
            rgb[cham] = np.clip(rgb[cham] - med + hsv_d, 0, 255)
            a[..., :3] = rgb.astype(np.uint8)
        Image.fromarray(a, "RGBA").save(os.path.join(MANH, f))
    g = os.path.join(MANH, "part", "P_chibangR08.png")
    if os.path.exists(g):
        shutil.copyfile(g, os.path.join(MANH, "canh_g_song.png"))
    thieu = [s for ds in TO.values() for s, _ in ds if not any(os.path.exists(os.path.join(MANH, d, s + ".png")) for d in ("part", "part_va"))]
    print("đã chép", GIU, "+ mat_nham; còn thiếu:", thieu or "không")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] == "to":
        lam_to()
    elif a[0] == "cat":
        cat(a[1:] or list(TO))
    elif a[0] == "xong":
        xong()
