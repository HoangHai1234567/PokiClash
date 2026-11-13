# -*- coding: utf-8 -*-
"""DẠNG 1 (non) của dòng quỷ lửa bắn cung, trên CÙNG rig với dạng 2 (cung_lua_rig.py, CL_DANG=non): đổi tỉ lệ ở rig rồi chuyển da.

    py -3 -I ArtGen/Spine/cung_lua_non.py concept     # dựng hình bố cục từ rig (da dạng lớn) + file prompt concept dạng non
    py -3 -I ArtGen/Spine/cung_lua_non.py da          # mảnh dạng non: chép mảnh dạng lớn, sửa bốn mảnh bằng mã, dựng tờ S + prompt sừng cụt
    py -3 -I ArtGen/Spine/cung_lua_non.py cat         # cắt to_01 (vòm mũ sừng cụt) từ tờ S đã gen

Trình tự (skill pokiclash-spine-rig, mục "DẠNG KHÁC trên CÙNG rig gốc"): tỉ lệ trước (TI_LE trong cung_lua_rig.py) → bố cục → concept →
người dùng duyệt → tờ chuyển da (các part ĐÃ XONG của dạng lớn xếp đúng ô, GPT chỉ đổi chi tiết) → cắt → rig → xuất cung_lua_1.
Đường dẫn tính từ chỗ đặt file này (hai máy khác ổ).
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "inbox", "cung_lua_1")
NON = os.path.join(BASE, "non")
MAU = os.path.join(NON, "mau")
TAI = os.path.join(NON, "tai_ve")
GUI = os.path.join(HERE, "gui_gpt", "cung_lua_1")
STYLE = os.path.join(HERE, "inbox", "kiem_si_1", "tai_ve", "L1_duyet.png")

FLAT = ("FLAT COLOUR, NO LIGHTING: every area is filled with ONE even colour; the coloured-pencil / wax-crayon strokes are only a texture, "
        "they do not make light or dark. No light and dark patches, no cast shadow, no shadow under the feet, no white highlights, no gloss, "
        "no glow halo, no gradient. The visor slits and the flame are flat yellow / orange shapes with an ink outline, they do NOT glow.")
LINE = ("Hand-drawn on paper with an ink pen: a slightly wobbly dark-brown outline (#2B2118, about 7 px on this canvas) around every shape, "
        "thinner ink lines (about 4 px) for the inner lines; neat, not scribbly, not a glossy digital render.")


def concept():
    os.makedirs(MAU, exist_ok=True)
    os.makedirs(TAI, exist_ok=True)
    bo_cuc = os.path.join(MAU, "bo_cuc.png")
    env = dict(os.environ, CL_DANG="non")
    subprocess.run([sys.executable, "-I", os.path.join(HERE, "cung_lua_rig.py"), "bo_cuc", bo_cuc, "2.2"], env=env, check=True)
    from PIL import Image
    w, h = Image.open(bo_cuc).size
    ra = os.path.join(TAI, "C1.png")
    p = f"""IMAGES (attached in this order; open each from its path):
image 1 = {bo_cuc}: the LAYOUT, {w}x{h}, white background: a 2D animation puppet standing in its rest pose, facing right: a small armoured archer with a big round helmet (three tall yellow visor slits), two long dark horns on top of the helmet, a flame as helmet plume sweeping to the left behind the head, a quiver with three arrow ends behind its back, a round shoulder plate, a short body on two short legs, and a big dark bow held low in front of it (the bow points to the lower right, its orange string runs behind the body). This picture gives the POSE, the PROPORTIONS and the PLACE AND SIZE of every body part. It shows the GROWN-UP form of the character; you will draw its YOUNG form on the same puppet.
image 2 = {STYLE}: an approved hero of the same project, 1536x1024: the hand-drawn ink and crayon drawing style to match. Do NOT copy its design.

SAVE: save it as a PNG to {ra}
If a file with that name already exists, save as C1_2.png, C1_3.png ... in the same folder. Do not edit, move or delete any other file.

TASK: draw ONE character concept: the YOUNG FIRST FORM of the fire-demon archer of image 1, standing in exactly the pose of image 1, on a plain white background. It will be cut into the same puppet parts as image 1, so every body part must stay where it is in image 1, at the same size and the same angle: the helmet, the body, both arms, both legs, the quiver, the bow and its string. Same canvas proportions as image 1 (portrait), the whole character inside the canvas with a white margin.

THE DESIGN (the young form: a little ember imp squire who has not caught fire yet; clearly the same creature as image 1, but simpler and younger; determined, ready to fight, cute but not a cheerful mascot and not scary):
1. HELMET: the same big round charred helmet with the same three tall visor slits, flat yellow (#FFD254), at the same place. Plain, no rim decoration.
2. HORNS: instead of the two long horns of image 1, two SHORT horn stubs (about one quarter of that length), thick, blunt, slightly curved, dark charred (#342A2C), at the same two places on top of the helmet.
3. PLUME: the flame behind the helmet stays at the place and size shown in image 1 (it is already small), drawn as ONE simple small flame of two flat colours: orange (#F88C28) outside, yellow (#FFD254) inside. No extra sparks.
4. ARMOUR: the same plates as image 1 (shoulder plate, chest, belt, skirt plates, arm and leg plates) but PLAIN: charred brown (#644A44) plates over a darker charred under-suit (#342A2C), with NO cracks of fire anywhere (the cracks of fire of image 1 appear only in the grown-up form). The shoulder plate is a plain round plate.
5. BOW: the same bow at the same place, same size, same angle, as plain dark charred wood (#342A2C) with NO line of fire on it; keep its two limbs and the pointed fins at the ends, simple. The string stays a thin orange line (#F88C28) at the same place.
6. QUIVER and the three arrow ends, the big arrowhead hanging below the belt: as in image 1, arrow ends and arrowhead gold (#E8B24A).
Few details: do not add anything that is not listed (no emblem, no extra spikes, no extra flames, no scarf, no face: the helmet is closed, only the three slits).

STYLE (see image 2): {LINE}
{FLAT}
Colours only from this list: charred brown #644A44, darker charred black #342A2C, yellow #FFD254, orange #F88C28, gold #E8B24A, ink #2B2118.

Plain pure-white background (#FFFFFF): no ground, no shadow, no paper grain outside the character, no white sticker border around the character, no text, no frame.
"""
    os.makedirs(GUI, exist_ok=True)
    f = os.path.join(GUI, "non_luot_1_concept.txt")
    open(f, "w", encoding="utf-8").write(p)
    print(f)
    hd = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read() if os.path.exists(hd) else ""
    dau = "\n## Dạng 1 (non), lượt 1: concept"
    cu = cu.split(dau)[0].rstrip("\n") + "\n"
    cu += f"""{dau} (2026-11-13)

Người dùng: "gen tiếp dạng 1 của tướng này". Dạng 1 làm trên CÙNG rig với dạng 2 (đổi tỉ lệ ở rig: đầu × 1,17, chùm lửa × 0,7), rồi chuyển da.

**Chỉ gửi GPT đường dẫn:** `{f}`. Ảnh lưu vào `{ra}` (trùng tên thì `C1_2.png`, `C1_3.png`...).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `{bo_cuc}` | Hình bố cục dựng từ rig ({w} × {h}, nền trắng): con rối đứng dáng nghỉ quay phải, tỉ lệ dạng 1 (đầu to hơn, chùm lửa nhỏ hơn), còn mang da dạng 2 (hai sừng dài, giáp nứt lửa, cung có vân lửa). Cho dáng, tỉ lệ, chỗ và cỡ từng bộ phận. |
| 2 | `{STYLE}` | Một tướng đã duyệt của game (1536 × 1024): chỉ lấy nét vẽ tay mực + chì sáp. |

Kiểm: đúng dáng và chỗ từng bộ phận như ảnh 1; hai sừng CỤT (chừng một phần tư), chùm lửa nhỏ hai màu, giáp trơn KHÔNG nứt lửa, cung trơn không vân lửa; mũ kín ba khe vàng; tô phẳng, không bóng, không quầng sáng; nền trắng, không viền sticker.

Câu sửa nhanh: "horns shorter and blunter", "remove the cracks of fire", "keep every part exactly where it is in image 1", "flat colour, no glow".

Duyệt xong Claude mới dựng lượt chuyển da (tờ part của dạng 2 xếp đúng ô, GPT chỉ đổi chi tiết).
"""
    open(hd, "w", encoding="utf-8").write(cu)
    print(hd)


# ---------------------------------------------------------------- CHUYỂN DA (người dùng duyệt concept C1, 2026-11-13: "dạng 1 ổn, làm đi")
# Dạng 1 khác dạng 2 ở NĂM mảnh; các mảnh còn lại dùng nguyên ảnh dạng 2 (không cho GPT vẽ lại: khỏi lệch khớp nối đã khít):
#   xiong (ngực), zuoxiaobi (găng lớn), gongjian_01 (cung): BỎ vết nứt / vân lửa bằng mã (lấp bằng vân chì của chính mảng đó);
#   tofa (chùm lửa): ba màu → hai màu (đỏ cam → cam, cam → vàng) bằng mã;
#   to_01 (vòm mũ + sừng): gen lại riêng (tờ S), hai sừng dài → hai mẩu sừng cụt.
MANH2 = os.path.join(BASE, "manh")
MANH1 = os.path.join(NON, "manh")
S_HOP, S_Z = (528, 88, 480, 849), 4.4          # ô của to_01 trên tờ S 1536 × 1024 (ảnh vùng + phần nới sừng, phóng 4,4)


def _lua(a):
    """điểm màu lửa (cam, vàng) trên mảnh giáp / cung."""
    r, g, b = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int)
    return (a[..., 3] > 40) & (r > 170) & (g > 80) & (r - b > 85)


def bo_lua(ten):
    """xoá vết lửa: mỗi điểm lửa (nới 4 px) lấy điểm cùng mảng ở cách đó một khoảng dời (thử nhiều hướng, lấy hướng lấp được nhiều nhất,
    lặp tới hết) → giữ vân chì sáp, không nhoè như inpaint."""
    import cv2
    import numpy as np
    from PIL import Image
    a = np.asarray(Image.open(os.path.join(MANH2, ten + ".png")).convert("RGBA")).copy()
    el = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
    m = cv2.dilate(_lua(a).astype(np.uint8), el).astype(bool) & (a[..., 3] > 0)
    con = m.copy()
    vanh = cv2.dilate(m.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31))).astype(bool) & ~m & (a[..., 3] > 250)
    sang = a[..., :3].max(2)
    mau = np.median(a[vanh & (sang > np.percentile(sang[vanh], 35))][:, :3], axis=0)          # màu tô của mảng quanh vết (bỏ mực)
    ok = (a[..., 3] > 250) & ~m & (np.abs(a[..., :3].astype(int) - mau).max(2) < 34)          # điểm cho: cùng màu tô, không mực
    H, W = m.shape
    out = a.copy()
    dois = [(int(round(d * np.cos(g))), int(round(d * np.sin(g)))) for d in (14, 20, 28, 38, 50, 64) for g in np.linspace(0, 2 * np.pi, 24, endpoint=False)]
    for _ in range(40):
        if not con.any():
            break
        ys, xs = np.nonzero(con)
        tot, best = -1, None
        for dx, dy in dois:
            y2, x2 = ys + dy, xs + dx
            v = (y2 >= 0) & (y2 < H) & (x2 >= 0) & (x2 < W)
            v[v] = ok[y2[v], x2[v]]
            if v.sum() > tot:
                tot, best = int(v.sum()), (dx, dy, v)
        if tot <= 0:
            break
        dx, dy, v = best
        out[ys[v], xs[v], :3] = a[ys[v] + dy, xs[v] + dx, :3]
        con[ys[v], xs[v]] = False
    if con.any():
        out[con, :3] = mau.astype(np.uint8)
    w = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 1.2)[..., None]                        # mép vùng lấp: hoà 1,2 px
    out[..., :3] = (a[..., :3] * (1 - w) + out[..., :3] * w).astype(np.uint8)
    Image.fromarray(out, "RGBA").save(os.path.join(MANH1, ten + ".png"))
    print(f"  {ten:12s} bỏ lửa: {int(m.sum())} điểm, còn sót {int(con.sum())}")


def lua_hai_mau():
    """chùm lửa: đỏ cam → cam, cam → vàng (giữ vân: nhân theo tỉ lệ màu chuẩn), vàng giữ."""
    import numpy as np
    from PIL import Image
    a = np.asarray(Image.open(os.path.join(MANH2, "tofa.png")).convert("RGBA")).copy()
    rgb = a[..., :3].astype(np.float32)
    mx, mn = rgb.max(2), rgb.min(2)
    d = np.maximum(mx - mn, 1e-3)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    hue = np.where(mx == r, (g - b) / d * 60.0, np.where(mx == g, 120.0 + (b - r) / d * 60.0, 240.0 + (r - g) / d * 60.0))
    lua = (a[..., 3] > 0) & (mx > 150) & (mx - mn > 60)
    CAM, VANG = np.array([248, 140, 40.0]), np.array([255, 210, 84.0])
    do = lua & (hue < 20.5)
    cam = lua & (hue >= 20.5) & (hue < 37.0)
    for vung, sang in ((do, CAM), (cam, VANG)):
        if vung.any():
            med = np.median(rgb[vung], axis=0)
            rgb[vung] = np.clip(rgb[vung] / np.maximum(med, 1.0) * sang, 0, 255)
    a[..., :3] = rgb.astype(np.uint8)
    Image.fromarray(a, "RGBA").save(os.path.join(MANH1, "tofa.png"))
    print(f"  tofa         hai màu: đỏ→cam {int(do.sum())} điểm, cam→vàng {int(cam.sum())} điểm")


def da():
    """mảnh dạng 1 = mảnh dạng 2 + bốn mảnh sửa bằng mã; dựng tờ S + prompt cho to_01 (sừng cụt)."""
    import json
    import shutil
    import numpy as np
    from PIL import Image
    os.makedirs(MANH1, exist_ok=True)
    for f in sorted(os.listdir(MANH2)):
        if f.startswith("_") or not (f.endswith(".png") or f.endswith(".json")):
            continue
        if f == "to_01.png" and os.path.exists(os.path.join(MANH1, "_to_01_da_cat")):
            continue                                   # to_01 của dạng 1 đã cắt từ tờ S: không chép đè
        shutil.copyfile(os.path.join(MANH2, f), os.path.join(MANH1, f))
    for t in ("xiong", "zuoxiaobi", "gongjian_01"):
        bo_lua(t)
    lua_hai_mau()
    # ---- tờ S: vòm mũ + hai sừng của dạng 2, phóng to, đúng ô
    g = Image.open(os.path.join(MANH2, "to_01.png")).convert("RGBA")
    x, y, cw, ch = S_HOP
    T = Image.new("RGB", (1536, 1024), "white")
    gz = g.resize((cw, ch), Image.LANCZOS)
    T.paste(gz, (x, y), gz)
    mau = os.path.join(MAU, "goc_S.png")
    T.save(mau)
    noi = json.load(open(os.path.join(BASE, "mau", "goc_A.json"), encoding="utf-8"))["to_01"]["noi"]
    json.dump({"to_01": {"hop": list(S_HOP), "z": S_Z, "noi": noi}}, open(os.path.join(MAU, "goc_S.json"), "w"), indent=1)
    al = np.asarray(gz)[..., 3] > 100
    hang = np.nonzero(al.any(1))[0]
    y_dinh = y + int(hang[0])                          # đỉnh sừng dài
    y_vom = y + int(round(noi * S_Z))                  # chỗ sừng gặp vòm (mép trên ảnh vùng gốc)
    y_cut = int(round(y_vom - 0.30 * (y_vom - y_dinh)))
    ra = os.path.join(TAI, "D_S.png")
    c1 = os.path.join(TAI, "C1.png")
    p = f"""IMAGES (attached in this order; open each from its path):
image 1 = {mau}: ONE PUPPET PART drawn alone and big, 1536x1024, white background: the round back dome of a helmet (the dark rounded shape in the lower part, from about y = {y_vom} to y = {y + ch}, with a small knob on its top) and TWO LONG CURVED HORNS rising from the top of the dome (their tips reach about y = {y_dinh}). Dark charred black, hand-drawn brown ink outline, crayon hatching. This is the piece of the GROWN-UP form; it gives the exact place, size and outline of the dome and the two places where the horns grow.
image 2 = {c1}: the APPROVED picture of the YOUNG form of the character (portrait, white background): a little armoured archer whose big helmet has two SHORT BLUNT HORN STUBS instead of long horns. Look only at how short and blunt its two horn stubs are. Do NOT copy its pose or anything else.

SAVE: save it as a PNG to {ra}
If a file with that name already exists, save as D_S_2.png, D_S_3.png ... in the same folder. Do not edit, move or delete any other file.

TASK: redraw image 1 as the same piece for the YOUNG form: the SAME dome and two SHORT HORN STUBS.
1. THE DOME (everything below about y = {y_vom}): keep it exactly as in image 1: the same outline, the same size, the same place on the canvas (if your picture were laid over image 1 the dome must coincide), the same small knob, the same darker charred black (#342A2C), the same ink outline.
2. THE HORNS: replace each long horn with a SHORT, THICK, BLUNT horn stub. Each stub grows from the same place on the dome as the long horn of image 1 and has the same width at its base; it is only about one quarter as long: its rounded tip is at about y = {y_cut} (nothing above y = {y_cut - 25}). It leans and curves slightly the same way as the base of the long horn. Smooth, rounded tip, ONE thin ring groove near its base. Same darker charred black (#342A2C).
3. ONE CLOSED SHAPE: dome and the two stubs together, with the dark-brown ink outline (#2B2118, the same thickness as in image 1, about 14 px on this canvas) running all the way round.

STYLE: hand-drawn on paper with an ink pen, slightly wobbly outline; the area filled with ONE even colour with visible coloured-pencil / wax-crayon hatching as in image 1. {FLAT}

Plain pure-white background (#FFFFFF), no paper grain outside the piece, no labels, no frame, nothing added.
"""
    f = os.path.join(GUI, "non_luot_2_sung.txt")
    open(f, "w", encoding="utf-8").write(p)
    print(f)
    hd = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read()
    dau = "\n## Dạng 1 (non), lượt 2: vòm mũ sừng cụt"
    cu = cu.split(dau)[0].rstrip("\n") + "\n"
    cu += f"""{dau} (2026-11-13)

Người dùng duyệt concept C1 ("dạng 1 ổn, làm đi"). Dạng 1 khác dạng 2 ở năm mảnh: ngực, găng lớn, cung (bỏ vết lửa) và chùm lửa (hai màu) sửa bằng mã (`py -3 -I ArtGen/Spine/cung_lua_non.py da`); chỉ vòm mũ + sừng phải gen lại.

**Chỉ gửi GPT đường dẫn:** `{f}`. Ảnh lưu vào `{ra}` (trùng tên thì `D_S_2.png`, `D_S_3.png`...).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `{mau}` | Một mảnh phóng to trên nền trắng (1536 × 1024): vòm sau mũ màu than sẫm (nửa dưới, có núm nhỏ) và hai sừng dài cong mọc từ đỉnh vòm, viền mực nâu. Mảnh của dạng 2. |
| 2 | `{c1}` | Concept dạng 1 đã duyệt (ảnh dọc, nền trắng): chỉ xem hai mẩu sừng cụt trên mũ. |

Kiểm: vòm trùng khít vòm ảnh 1 (cùng chỗ, cùng cỡ); hai mẩu sừng cụt, tù, mọc đúng chỗ gốc sừng cũ, đỉnh khoảng y = {y_cut}; một hình kín viền mực; tô phẳng.

Câu sửa nhanh: "the dome must stay exactly where it is in image 1", "horn stubs shorter and blunter", "flat colour, no highlights".

Cắt: `py -3 -I ArtGen/Spine/cung_lua_non.py cat` → `inbox/cung_lua_1/non/manh/to_01.png`.
"""
    open(hd, "w", encoding="utf-8").write(cu)
    print(hd)


def cat():
    """cắt to_01 từ tờ S bằng đúng bộ cắt của dạng 2 (cung_lua_da.cat), trỏ thư mục sang dạng non."""
    sys.path.insert(0, HERE)
    import cung_lua as G
    import cung_lua_da as D
    G.MAU, G.TAI = MAU, TAI
    D.MANH = MANH1
    D.TO = {"S": [[("to_01", S_Z)]]}
    giu = {f: open(os.path.join(MANH1, f), "rb").read() for f in ("gongjian_02.png",) if os.path.exists(os.path.join(MANH1, f))}
    D.cat()
    for f, d in giu.items():
        open(os.path.join(MANH1, f), "wb").write(d)
    open(os.path.join(MANH1, "_to_01_da_cat"), "w", encoding="utf-8").write("to_01.png cắt từ tờ S (D_S*.png)\n")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    {"concept": concept, "da": da, "cat": cat}[sys.argv[1]]()
