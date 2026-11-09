# -*- coding: utf-8 -*-
"""Dựng rig Rồng Giọt từ mảnh đã khớp (rong_giot.py place): xương, hiệu ứng nước (ảnh FX sẵn có của dòng Giọt Sương),
6 animation (idle, hit, attack, cast, skill, evolve), xuất Spine 4.2 + atlas, tờ khung và GIF để soi, thông tin trận
(khung trúng, chỗ bắn tia), rồi .atomik và chân dung vào Assets/03 Art/Heroes/Resources/rong_giot/.

Gọi qua: <venv>/Scripts/python -I ArtGen/Spine/rong_giot.py build
Toạ độ rig: pixel, y lên, gốc ở giữa hai chân trên mặt đất; con nhìn sang phải (+x là phía trước).
"""
import copy
import json
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import atomik
import rig
from rong_giot import BASE, CODE, SPEC
from spine_compat import _convert_timeline, pack

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.normpath(os.path.join(HERE, "..", ".."))
FX_DIR = os.path.join(PROJECT, "ArtGen", "Heroes", "inbox", "giot_suong_fx", "tai_ve")
OUT_RES = os.path.join(PROJECT, "Assets", "03 Art", "Heroes", "Resources", CODE)
RIG = os.path.join(BASE, "rig")

H = 340.0       # chiều cao dáng đứng trong rig: sticker vẽ tối đa ~301 điểm (RenderTexture 1024 cho 3,4 lần chiều cao)
FPS = 25
E, EO, EI, L = rig.E, rig.EO, rig.EI, None

# vẽ từ sau ra trước: tay phải (người xem) nằm sau thân để vai không lộ cục tròn; nắm tay và kiếm trước thân
DRAW = ["tail", "wing_l", "wing_r", "thigh_l", "foot_l", "thigh_r", "foot_r", "arm_r", "torso", "arm_l", "fist_l",
        "crest", "ear_l", "ear_r", "head", "sword", "fist_r"]

# ảnh hiệu ứng: (tệp, cạnh dài khi lưu vào atlas, cạnh dài khi hiện ở cỡ 1)
FX = {
    "FX01": ("FX01.png", 160, 0.95 * H),   # lốc nước vòng tròn
    "FX02": ("FX02.png", 124, 0.6 * H),    # sóng lưỡi liềm (vệt chém)
    "FX03": ("FX03.png", 116, 0.5 * H),    # nổ nước
    "FX04": ("FX04.png", 80, 0.32 * H),    # giọt nước
    "FX05": ("FX05.png", 60, 0.2 * H),     # lấp lánh
    "FX06": ("FX06.png", 128, 0.9 * H),    # bong bóng (tô phẳng, phóng to không lộ)
    "FX07": ("FX07.png", 150, 0.85 * H),   # sóng thần
    "FX08": ("FX08.png", 160, 0.95 * H),   # vòng sóng mặt đất
}


# ---------------------------------------------------------------- ảnh
def fx_image(name):
    f, keep, _ = FX[name]
    rgb = np.array(Image.open(os.path.join(FX_DIR, f)).convert("RGB"))
    m = rig.fg_mask(rgb)
    rgba = rig.to_rgba(rgb, m)
    ys, xs = np.where(m > 0)
    rgba = rgba[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    im = Image.fromarray(rgba)
    s = keep / max(im.size)
    return im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)


def shadow_image():
    w, h = 220, 44
    im = Image.new("L", (w * 4, h * 4), 0)
    ImageDraw.Draw(im).ellipse([4, 4, w * 4 - 4, h * 4 - 4], fill=255)
    a = np.array(im.resize((w, h), Image.LANCZOS)).astype(np.float32) / 255 * 0.32
    rgba = np.zeros((h, w, 4), np.uint8)
    rgba[:, :, :3] = (40, 48, 64)
    rgba[:, :, 3] = (a * 255).astype(np.uint8)
    return Image.fromarray(rgba)


# ---------------------------------------------------------------- khoá
def tl(keys):
    return rig.tl(keys)


def tl2(keys):
    return rig.tl2(keys)


def al(keys):
    """độ đậm slot: (t, a, curve) như tl; curve gắn với đoạn kết thúc ở khoá đó."""
    out = []
    for k in keys:
        f = {"time": k[0], "value": k[1]}
        c = k[2] if len(k) > 2 else L
        if c:
            f["curve"] = c
        out.append(f)
    return out


def wave(amp, phase, dur, n=16, base=0.0):
    """dao động vòng lặp khép kín (khoá đầu = khoá cuối), thẳng giữa các khoá dày."""
    return [(round(dur * i / n, 4), round(base + amp * math.sin(2 * math.pi * (i / n - phase)), 3), L) for i in range(n + 1)]


def show(slot_keys):
    """[(t, tên hình hoặc None)] -> khoá đổi hình của slot."""
    return [{"time": t, "name": n} for t, n in slot_keys]


# ---------------------------------------------------------------- dựng
def build():
    P = rig.paths(CODE)
    pl = json.load(open(os.path.join(RIG, "placed.json")))
    W1, H1 = pl["ref_size"]
    parts = pl["parts"]
    pimg = {n: np.array(Image.open(os.path.join(RIG, "placed", n + ".png"))) for n in parts}
    mask = {n: rig.placed_mask(parts[n], pimg[n], W1, H1) for n in parts}

    # mặt đất, gốc, tỉ lệ (ảnh L1 -> rig)
    ground = max(parts[n]["y0"] + parts[n]["h"] for n in ("foot_l", "foot_r")) - 6
    feet_x = (parts["foot_l"]["cx"] + parts["foot_r"]["cx"]) / 2
    top = min(int(np.where(mask[n].any(1))[0].min()) for n in ("crest", "head"))
    k = H / (ground - top)

    def S(p):
        return ((p[0] - feet_x) * k, (ground - p[1]) * k)

    J = rig.joint
    hip_l, hip_r = J(mask["thigh_l"], mask["torso"]), J(mask["thigh_r"], mask["torso"])
    hip = ((hip_l[0] + hip_r[0]) / 2, (hip_l[1] + hip_r[1]) / 2)
    neck = J(mask["head"], mask["torso"])
    core = ((hip[0] + neck[0]) / 2, (hip[1] + neck[1]) / 2)
    world = {
        "root": (feet_x, ground), "shadow": (feet_x, ground), "move": (feet_x, ground), "core": core, "hip": hip,
        "body": hip, "chest": hip, "head": neck, "crest": J(mask["crest"], mask["head"]), "ear_l": J(mask["ear_l"], mask["head"]),
        "ear_r": J(mask["ear_r"], mask["head"]), "wing_l": J(mask["wing_l"], mask["torso"]),
        "wing_r": J(mask["wing_r"], mask["torso"]), "arm_l": J(mask["arm_l"], mask["torso"]),
        "fist_l": J(mask["fist_l"], mask["arm_l"]), "arm_r": J(mask["arm_r"], mask["torso"]),
        "fist_r": J(mask["fist_r"], mask["arm_r"]), "sword": J(mask["sword"], mask["fist_r"]),
        "tail": J(mask["tail"], mask["torso"]), "thigh_l": hip_l, "foot_l": J(mask["foot_l"], mask["thigh_l"]),
        "thigh_r": hip_r, "foot_r": J(mask["foot_r"], mask["thigh_r"]),
    }
    # mũi kiếm: điểm của mảnh kiếm xa chỗ nắm nhất
    ys, xs = np.where(mask["sword"] > 0)
    g = world["sword"]
    i = int(np.argmax((xs - g[0]) ** 2 + (ys - g[1]) ** 2))
    tip = (float(xs[i]), float(ys[i]))

    # (xương, cha, noScale). Không dùng noScale: tiến hóa thu nhỏ cả con qua core, noScale sẽ giữ đầu, tay nguyên cỡ. Thở phồng,
    # dẹp giãn làm trên xương chest chỉ mang mảnh thân, nên đầu, tay không méo.
    bone_def = [
        ("move", "root", False), ("shadow", "move", False), ("core", "move", False), ("hip", "core", False),
        ("body", "hip", False), ("chest", "body", False), ("head", "body", False), ("crest", "head", False),
        ("ear_l", "head", False), ("ear_r", "head", False), ("wing_l", "body", False), ("wing_r", "body", False),
        ("tail", "body", False), ("arm_l", "body", False), ("fist_l", "arm_l", False), ("arm_r", "body", False),
        ("fist_r", "arm_r", False), ("sword", "fist_r", False), ("thigh_l", "hip", False), ("foot_l", "thigh_l", False),
        ("thigh_r", "hip", False), ("foot_r", "thigh_r", False),
    ]
    rigxy = {b: S(p) for b, p in world.items()}
    tip_xy = S(tip)
    # xương hiệu ứng: (tên, cha, x, y) theo rig (thế giới ở dáng gốc)
    cx0, cy0 = rigxy["core"]
    fx_bones = [  # hiệu ứng là con của move (đi theo cú lao), không theo core (core bị xoay, thu nhỏ)
        ("fx_slash", "move", 0.42 * H, 0.42 * H), ("fx_splash", "move", 0.62 * H, 0.42 * H),
        ("fx_wave", "move", 0.72 * H, 0.0), ("fx_ring", "move", cx0, cy0),
        ("fx_bubble", "move", cx0, cy0 + 0.05 * H), ("fx_tip", "sword", tip_xy[0], tip_xy[1]),
        ("fx_spark1", "move", cx0 - 0.32 * H, cy0 + 0.25 * H), ("fx_spark2", "move", cx0 + 0.36 * H, cy0 + 0.05 * H),
        ("fx_spark3", "move", cx0 - 0.12 * H, cy0 - 0.3 * H),
        ("fx_ground", "root", 0.0, 0.02 * H), ("fx_drop", "core", cx0 + 0.3 * H, cy0 + 0.02 * H),
    ]
    for name, parent, x, y in fx_bones:
        rigxy[name] = (x, y)
    bones = [{"name": "root"}]
    for name, parent, ns in bone_def + [(n, p, False) for n, p, _, _ in fx_bones]:
        bx, by = rigxy[name]
        px, py = rigxy[parent] if parent != "root" else (0.0, 0.0)
        b = {"name": name, "parent": parent, "x": round(bx - px, 2), "y": round(by - py, 2), "length": 18}
        if ns:
            b["inherit"] = "noScale"
        bones.append(b)

    # ảnh mảnh ở tỉ lệ rig
    imgs, skin, slots = {}, {}, []
    bone_of = {n: n for n in DRAW}
    bone_of["torso"] = "chest"
    for ex in SPEC["swap"]["head"]:
        bone_of[ex] = "head"
    for n in DRAW + SPEC["swap"]["head"]:
        t = parts[n]
        im = Image.fromarray(pimg[n])
        imgs[n] = im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)
    fx_imgs = {n: fx_image(n) for n in FX}
    imgs.update(fx_imgs)
    imgs["shadow"] = shadow_image()

    def region_piece(n):
        t = parts[n]
        cx, cy = S((t["x0"] + t["w"] / 2, t["y0"] + t["h"] / 2))
        bx, by = rigxy[bone_of[n]]
        return {"x": round(cx - bx, 2), "y": round(cy - by, 2), "width": imgs[n].width, "height": imgs[n].height}

    def region_fx(fx, scale=1.0):
        _, _, size = FX[fx]
        im = fx_imgs[fx]
        s = size * scale / max(im.size)
        return {"path": fx, "x": 0, "y": 0, "width": round(im.width * s, 1), "height": round(im.height * s, 1)}

    slot_list = [("shadow", "shadow", "shadow", {"shadow": {"x": 0, "y": 0, "width": 220 * H / 400, "height": 44 * H / 400}}),
                 ("fx_ground", "fx_ground", None, {"ground": region_fx("FX08")}),
                 ("fx_ring_back", "fx_ring", None, {"ring_back": region_fx("FX01")})]
    for n in DRAW:
        atts = {n: region_piece(n)}
        if n == "head":
            for ex in SPEC["swap"]["head"]:
                atts[ex] = region_piece(ex)
        slot_list.append((n, bone_of[n], n, atts))
    slot_list += [
        ("fx_ring_front", "fx_ring", None, {"ring_front": region_fx("FX01")}),
        ("fx_bubble", "fx_bubble", None, {"bubble": region_fx("FX06")}),
        ("fx_tip", "fx_tip", None, {"tip_bubble": region_fx("FX06", 0.22)}),
        ("fx_drop", "fx_drop", None, {"drops": region_fx("FX04")}),
        ("fx_wave", "fx_wave", None, {"wave": region_fx("FX07")}),
        ("fx_slash", "fx_slash", None, {"slash": region_fx("FX02")}),
        ("fx_splash", "fx_splash", None, {"splash": region_fx("FX03")}),
        ("fx_spark1", "fx_spark1", None, {"spark": region_fx("FX05")}),
        ("fx_spark2", "fx_spark2", None, {"spark": region_fx("FX05", 0.8)}),
        ("fx_spark3", "fx_spark3", None, {"spark": region_fx("FX05", 0.65)}),
    ]
    for name, bone, att, atts in slot_list:
        s = {"name": name, "bone": bone}
        if att:
            s["attachment"] = att
        slots.append(s)
        skin[name] = atts

    anims = make_anims(rigxy)
    raw = copy.deepcopy(anims)
    for a in anims.values():
        for tls_ in a.get("bones", {}).values():
            for kind, frames in tls_.items():
                _convert_timeline(kind, frames)
        for st in a.get("slots", {}).values():
            if "alpha" in st:
                _convert_timeline("alpha", st["alpha"])
    xs_ = [b[0] for b in rigxy.values()]
    skel = {"skeleton": {"hash": CODE, "spine": "4.2.0", "x": round(-0.7 * H), "y": round(-0.1 * H), "width": round(2.3 * H),
                         "height": round(1.7 * H), "images": "./images/", "fps": FPS},
            "bones": bones, "slots": slots, "skins": [{"name": "default", "attachments": skin}], "animations": anims}
    os.makedirs(RIG, exist_ok=True)
    json.dump(skel, open(os.path.join(RIG, CODE + ".json"), "w"), indent=1)
    aw, ah, place_ = pack(imgs, padding=2)
    atlas = Image.new("RGBA", (aw, ah), (0, 0, 0, 0))
    lines = [f"{CODE}.png", f"size: {aw},{ah}", "format: RGBA8888", "filter: Linear,Linear", "repeat: none"]
    for n, (x, y, w, h) in place_.items():
        atlas.paste(imgs[n], (x, y))
        lines += [n, "  rotate: false", f"  xy: {x}, {y}", f"  size: {w}, {h}", f"  orig: {w}, {h}", "  offset: 0, 0",
                  "  index: -1"]
    atlas.save(os.path.join(RIG, CODE + ".png"))
    open(os.path.join(RIG, CODE + ".atlas"), "w").write("\n".join(lines) + "\n")
    print(f"{len(bones)} xương, {len(slots)} slot, atlas {aw}x{ah}, animation: {', '.join(anims)}")

    # soi: xương, tờ khung, GIF
    dbg = Image.open(P["ref"]).convert("RGB")
    d = ImageDraw.Draw(dbg)
    for name, parent, _ in bone_def:
        if name in world and parent in world:
            (x, y), (px, py) = world[name], world[parent]
            d.line([px, py, x, y], fill=(255, 0, 160), width=3)
            d.ellipse([x - 7, y - 7, x + 7, y + 7], outline=(255, 0, 160), width=3)
            d.text((x + 9, y - 6), name, fill=(120, 0, 80))
    d.ellipse([tip[0] - 8, tip[1] - 8, tip[0] + 8, tip[1] + 8], outline=(0, 160, 255), width=3)
    dbg.save(os.path.join(RIG, "xuong.png"))
    pix = {n: np.array(im) for n, im in imgs.items()}
    render_sheet(skel, raw, pix)

    # thông tin trận và .atomik
    game = game_info(skel, raw)
    json.dump(game, open(os.path.join(RIG, CODE + "_game.json"), "w"), indent=1, ensure_ascii=False)
    print("trận:", json.dumps(game, ensure_ascii=False))
    os.makedirs(OUT_RES, exist_ok=True)
    atomik.convert(os.path.join(RIG, CODE + ".json"), os.path.join(RIG, CODE + ".atlas"),
                   os.path.join(OUT_RES, CODE + ".atomik"), CODE, game)
    portrait(parts, pimg, ground, feet_x, top)


# ---------------------------------------------------------------- tư thế (soi, thông tin trận)
def pose(skel, anim, t):
    world = {}
    tls = anim.get("bones", {})
    for b in skel["bones"]:
        x, y, r, sx, sy = b.get("x", 0), b.get("y", 0), 0.0, 1.0, 1.0
        tl_ = tls.get(b["name"], {})
        if "translate" in tl_:
            dx, dy = rig.sample(tl_["translate"], t, ("x", "y"))
            x, y = x + dx, y + dy
        if "rotate" in tl_:
            r += rig.sample(tl_["rotate"], t, ("angle",))[0]
        if "scale" in tl_:
            fx, fy = rig.sample(tl_["scale"], t, ("x", "y"))
            sx, sy = sx * fx, sy * fy
        c, s = math.cos(math.radians(r)), math.sin(math.radians(r))
        M = np.array([[c * sx, -s * sy, x], [s * sx, c * sy, y], [0, 0, 1]])
        if "parent" not in b:
            world[b["name"]] = M
        else:
            Pm = world[b["parent"]]
            if b.get("inherit") == "noScale":
                Pm = Pm.copy()
                Pm[:2, 0] /= max(1e-9, np.linalg.norm(Pm[:2, 0]))
                Pm[:2, 1] /= max(1e-9, np.linalg.norm(Pm[:2, 1]))
            world[b["name"]] = Pm @ M
    shown, alpha = {}, {}
    for sl in skel["slots"]:
        name = sl.get("attachment")
        st = anim.get("slots", {}).get(sl["name"], {})
        for kk in st.get("attachment", []):
            if kk["time"] <= t + 1e-6:
                name = kk["name"]
        shown[sl["name"]] = name
        alpha[sl["name"]] = float(np.clip(rig.sample(st["alpha"], t, ("value",))[0], 0, 1)) if "alpha" in st else 1.0
    return world, shown, alpha


def draw(skel, anim, t, pix, k, box):
    Wb, Hb, ox, oy = box
    canvas = np.full((Hb, Wb, 3), (250, 246, 236), np.float32)
    world, shown, alpha = pose(skel, anim, t)
    atts = skel["skins"][0]["attachments"]
    to_px = np.array([[k, 0, ox], [0, -k, oy], [0, 0, 1]])
    for sl in skel["slots"]:
        an = shown[sl["name"]]
        if not an or alpha[sl["name"]] <= 0.003:
            continue
        a = atts[sl["name"]][an]
        im = pix[a.get("path", an)]
        h, w = im.shape[:2]
        sx, sy = a["width"] / w, a["height"] / h
        A = np.array([[sx, 0, a["x"] - a["width"] / 2], [0, -sy, a["y"] + a["height"] / 2], [0, 0, 1]])
        M = (to_px @ world[sl["bone"]] @ A)[:2]
        wp = rig.cv2.warpAffine(im, M, (Wb, Hb), flags=rig.cv2.INTER_LINEAR, borderMode=rig.cv2.BORDER_CONSTANT,
                                borderValue=(0, 0, 0, 0)).astype(np.float32)
        al_ = wp[:, :, 3:4] / 255.0 * alpha[sl["name"]]
        canvas = canvas * (1 - al_) + wp[:, :, :3] * al_
    return canvas.astype(np.uint8)


def render_sheet(skel, raw, pix, fh=260, n=9):
    k = fh / (1.75 * H)
    Wb = int(2.4 * H * k)
    box = (Wb, fh, int(0.65 * H * k), int(fh - 0.1 * H * k))
    rows = []
    font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 13)
    for name, anim in raw.items():
        dur = anim_dur(anim)
        fr = [draw(skel, anim, dur * i / (n - 1), pix, k, box) for i in range(n)]
        row = Image.fromarray(np.concatenate(fr, 1))
        dd = ImageDraw.Draw(row)
        dd.text((6, 4), f"{name} ({dur:.2f}s)", fill=(43, 33, 24), font=font)
        for i in range(n):
            dd.text((i * Wb + Wb - 40, fh - 16), f"{dur * i / (n - 1):.2f}", fill=(120, 100, 80), font=font)
        rows.append(np.array(row))
        g = [Image.fromarray(draw(skel, anim, t, pix, k, box)) for t in np.arange(0, dur + 1e-6, 1 / 20)]
        g[0].save(os.path.join(RIG, f"anim_{name}.gif"), save_all=True, append_images=g[1:], duration=50, loop=0)
    Image.fromarray(np.concatenate(rows, 0)).save(os.path.join(RIG, "khung.png"))
    print("soi:", os.path.join(RIG, "khung.png"))


def anim_dur(anim):
    ts = [f["time"] for tl_ in anim.get("bones", {}).values() for fr in tl_.values() for f in fr]
    ts += [f["time"] for st in anim.get("slots", {}).values() for fr in st.values() for f in fr]
    return max(ts)


def game_info(skel, raw):
    world, shown, _ = pose(skel, raw["idle"], 0)
    atts = skel["skins"][0]["attachments"]
    topy = 0.0
    for sl in skel["slots"]:
        an = shown[sl["name"]]
        if not an or sl["name"].startswith("fx_") or sl["name"] == "shadow":
            continue
        a = atts[sl["name"]][an]
        M = world[sl["bone"]]
        for cx in (-0.5, 0.5):
            for cy in (-0.5, 0.5):
                p = M @ np.array([a["x"] + cx * a["width"], a["y"] + cy * a["height"], 1])
                topy = max(topy, p[1])
    w2, _, _ = pose(skel, raw["cast"], HIT["cast"])
    tip = w2["fx_tip"][:2, 2]
    return {"fps": FPS, "height": round(float(topy), 2), "hitClips": list(HIT), "hitTimes": [HIT[c] for c in HIT],
            "lunge": ["skill"], "stay": [], "muzzle": [round(float(tip[0]), 2), round(float(tip[1]), 2)], "beam": 0.8,
            "beamStyle": "", "move": "move", "shadow": "shadow"}


def portrait(parts, pimg, ground, feet_x, top):
    """chân dung khung 4:5 như HeroArt (chân cách đáy 6%), lưu vuông 512 (kéo giãn như AolaImport), không bóng (luật UI)."""
    hh = ground - top
    fh_ = hh / 0.86
    fw = fh_ * 0.8
    W, Hh = int(round(fw)), int(round(fh_))
    canvas = np.zeros((Hh, W, 4), np.float32)
    x0 = feet_x - fw / 2
    y0 = ground - (1 - 0.06) * fh_
    for n in DRAW:
        t = parts[n]
        im = pimg[n].astype(np.float32)
        ox, oy = int(round(t["x0"] - x0)), int(round(t["y0"] - y0))
        h, w = im.shape[:2]
        ax0, ay0, ax1, ay1 = max(0, ox), max(0, oy), min(W, ox + w), min(Hh, oy + h)
        if ax1 <= ax0 or ay1 <= ay0:
            continue
        sub = im[ay0 - oy:ay1 - oy, ax0 - ox:ax1 - ox]
        a = sub[:, :, 3:4] / 255.0
        dst = canvas[ay0:ay1, ax0:ax1]
        out_a = a + dst[:, :, 3:4] * (1 - a)
        rgb = (sub[:, :, :3] * a + dst[:, :, :3] * dst[:, :, 3:4] * (1 - a)) / np.maximum(out_a, 1e-6)
        dst[:, :, :3], dst[:, :, 3:4] = rgb, out_a
    im = Image.fromarray(np.clip(np.dstack([canvas[:, :, :3], canvas[:, :, 3:4] * 255]), 0, 255).astype(np.uint8))
    p = os.path.join(OUT_RES, CODE + "_portrait.png")
    im.resize((512, 512), Image.LANCZOS).save(p)
    im.save(os.path.join(RIG, "chan_dung_4x5.png"))
    print("chân dung:", p)


# ---------------------------------------------------------------- animation
HIT = {"attack": 0.44, "cast": 0.5, "skill": 1.04}


def make_anims(xy):
    A = {}
    D = 1.6  # idle
    A["idle"] = {"bones": {
        "body": {"translate": tl2([(0, 0, 0), (0.8, 0, -4), (D, 0, 0)])},
        "chest": {"scale": tl2([(0, 1, 1), (0.8, 1.02, 0.975), (D, 1, 1)])},
        "head": {"rotate": tl(wave(1.6, 0.1, D))},
        "crest": {"rotate": tl(wave(6, 0.25, D))},
        "ear_l": {"rotate": tl(wave(5, 0.15, D))}, "ear_r": {"rotate": tl(wave(-5, 0.15, D))},
        "wing_l": {"rotate": tl(wave(-7, 0.05, D, base=-2))}, "wing_r": {"rotate": tl(wave(7, 0.05, D, base=2))},
        "tail": {"rotate": tl(wave(5, 0.3, D))},
        "arm_l": {"rotate": tl(wave(-3, 0.12, D))}, "arm_r": {"rotate": tl(wave(2.5, 0.12, D))},
        "sword": {"rotate": tl(wave(-2, 0.2, D))},
        "move": {"translate": tl2([(0, 0, 0), (D, 0, 0)])},
    }, "slots": {"head": {"attachment": show([(0, "head"), (1.1, "head_blink"), (1.22, "head")])}}}

    D = 0.5  # trúng đòn: bật lùi
    A["hit"] = {"bones": {
        "move": {"translate": tl2([(0, 0, 0), (0.07, -24, 0, EO), (0.2, -28, 0), (D, 0, 0)])},
        "core": {"rotate": tl([(0, 0), (0.07, 11, EO), (0.2, 7), (D, 0)])},
        "head": {"rotate": tl([(0, 0), (0.07, 6, EO), (0.25, 3), (D, 0)])},
        "arm_l": {"rotate": tl([(0, 0), (0.08, -28, EO), (D, 0)])},
        "arm_r": {"rotate": tl([(0, 0), (0.08, 22, EO), (D, 0)])},
        "ear_l": {"rotate": tl([(0, 0), (0.08, -16, EO), (D, 0)])}, "ear_r": {"rotate": tl([(0, 0), (0.08, 16, EO), (D, 0)])},
        "wing_l": {"rotate": tl([(0, 0), (0.08, -14, EO), (D, 0)])}, "wing_r": {"rotate": tl([(0, 0), (0.08, 14, EO), (D, 0)])},
        "crest": {"rotate": tl([(0, 0), (0.1, 12, EO), (0.3, -5), (D, 0)])},
        "tail": {"rotate": tl([(0, 0), (0.1, 10, EO), (D, 0)])},
    }, "slots": {
        "head": {"attachment": show([(0, "head"), (0.02, "head_blink"), (0.32, "head")])},
        "fx_drop": {"attachment": show([(0, None), (0.02, "drops"), (0.42, None)]),
                    "alpha": al([(0, 1), (0.14, 1), (0.42, 0, E)])},
    }}
    # giọt nước bắn ra từ chỗ trúng (trước ngực), bay lên phía trước
    A["hit"]["bones"]["fx_drop"] = {"translate": tl2([(0, 0, 0), (0.02, 0, 0), (0.42, 34, 26, EO)]),
                                    "scale": tl2([(0, 0.6, 0.6), (0.02, 0.6, 0.6), (0.42, 1.15, 1.15, EO)])}

    D = 0.9  # đánh thường: lấy đà, lao tới chém, về (trận kéo cú lao về đối thủ, đỉnh lao ~ khung trúng)
    h = HIT["attack"]
    A["attack"] = {"bones": {
        "move": {"translate": tl2([(0, 0, 0), (0.2, -14, 0), (h, 0.68 * H, 0, EI), (0.52, 0.66 * H, 0), (D, 0, 0, E)])},
        "core": {"rotate": tl([(0, 0), (0.2, 9), (h - 0.06, -10, EI), (h + 0.06, -14, EO), (0.62, -4), (D, 0)])},
        "chest": {"scale": tl2([(0, 1, 1), (0.18, 1.06, 0.92), (h - 0.08, 0.96, 1.05), (0.6, 1, 1), (D, 1, 1)])},
        # lấy đà: giơ kiếm lên phía trước bên phải đầu (không vắt qua mặt), rồi bổ chéo xuống
        "arm_r": {"rotate": tl([(0, 0), (0.22, 92, E), (h - 0.06, 100), (h + 0.02, -22, EO), (0.62, -12), (D, 0)])},
        "sword": {"rotate": tl([(0, 0), (0.22, 30), (h - 0.06, 38), (h + 0.02, -10, EO), (D, 0)])},
        "arm_l": {"rotate": tl([(0, 0), (0.22, 18), (h, -30, EO), (0.62, -12), (D, 0)])},
        "thigh_l": {"rotate": tl([(0, 0), (0.2, 6), (h, -22, EI), (0.62, -8), (D, 0)])},
        "thigh_r": {"rotate": tl([(0, 0), (0.2, -6), (h, 18, EI), (0.62, 6), (D, 0)])},
        "head": {"rotate": tl([(0, 0), (0.2, 6), (h, -6, EO), (D, 0)])},
        "ear_l": {"rotate": tl([(0, 0), (h, 18, EI), (0.7, -6), (D, 0)])}, "ear_r": {"rotate": tl([(0, 0), (h, -18, EI), (0.7, 6), (D, 0)])},
        "wing_l": {"rotate": tl([(0, 0), (0.2, -18), (h, 14, EI), (D, 0)])}, "wing_r": {"rotate": tl([(0, 0), (0.2, 18), (h, -14, EI), (D, 0)])},
        "tail": {"rotate": tl([(0, 0), (0.2, -10), (h, 16, EI), (0.7, -4), (D, 0)])},
        "crest": {"rotate": tl([(0, 0), (h, 16, EI), (0.7, -8), (D, 0)])},
        "fx_slash": {"scale": tl2([(0, 0.7, 0.7), (h - 0.04, 0.7, 0.7), (h + 0.18, 1.2, 1.2, EO), (D, 1.2, 1.2)])},
        "fx_splash": {"scale": tl2([(0, 0.4, 0.4), (h, 0.4, 0.4), (h + 0.22, 1.25, 1.25, EO), (D, 1.25, 1.25)])},
    }, "slots": {
        "head": {"attachment": show([(0, "head"), (0.24, "head_shout"), (0.66, "head")])},
        "fx_slash": {"attachment": show([(0, None), (h - 0.04, "slash"), (h + 0.24, None)]),
                     "alpha": al([(0, 1), (h + 0.06, 1), (h + 0.24, 0, E)])},
        "fx_splash": {"attachment": show([(0, None), (h, "splash"), (h + 0.3, None)]),
                      "alpha": al([(0, 1), (h + 0.08, 1), (h + 0.3, 0, E)])},
    }}

    D = 0.9  # chiêu mana: giơ kiếm tụ nước ở mũi, đâm tới; trận bắn tia từ mũi kiếm ở khung trúng
    h = HIT["cast"]
    A["cast"] = {"bones": {
        "move": {"translate": tl2([(0, 0, 0), (0.3, -8, 0), (h, 22, 0, EI), (0.7, 18, 0), (D, 0, 0)])},
        "core": {"rotate": tl([(0, 0), (0.3, 6), (h, -8, EI), (0.7, -6), (D, 0)])},
        "arm_r": {"rotate": tl([(0, 0), (0.3, 120, E), (h - 0.04, 112), (h, 52, EO), (0.72, 50), (D, 0)])},
        "sword": {"rotate": tl([(0, 0), (0.3, 20), (h, -6, EO), (0.72, -6), (D, 0)])},
        "arm_l": {"rotate": tl([(0, 0), (0.3, 14), (h, -24, EO), (D, 0)])},
        "head": {"rotate": tl([(0, 0), (0.3, 5), (h, -4), (D, 0)])},
        "wing_l": {"rotate": tl(wave(-9, 0, D))}, "wing_r": {"rotate": tl(wave(9, 0, D))},
        "tail": {"rotate": tl([(0, 0), (0.3, -8), (h, 10, EI), (D, 0)])},
        "crest": {"rotate": tl([(0, 0), (0.3, -6), (h, 12, EI), (D, 0)])},
        "fx_tip": {"scale": tl2([(0, 0.2, 0.2), (0.12, 0.3, 0.3), (h - 0.02, 1.15, 1.15, E), (h + 0.08, 1.6, 1.6, EO), (D, 1.6, 1.6)]),
                   "rotate": tl([(0, 0), (D, -160, L)])},
    }, "slots": {
        "head": {"attachment": show([(0, "head"), (h - 0.06, "head_shout"), (0.76, "head")])},
        "fx_tip": {"attachment": show([(0, None), (0.12, "tip_bubble"), (h + 0.1, None)]),
                   "alpha": al([(0, 0), (0.12, 0.2), (0.3, 0.95, E), (h, 0.95), (h + 0.1, 0, E)])},
    }}

    D = 1.7  # chiêu cuối: tụ lốc nước, nhảy lộn tới, bổ kiếm xuống kèm sóng thần (trận kéo cú lao, đỉnh = lúc bổ)
    h = HIT["skill"]
    cy = xy["core"][1]
    A["skill"] = {"bones": {
        "move": {"translate": tl2([(0, 0, 0), (0.32, -10, -6), (0.62, 0.42 * H, 0.55 * H, EO), (0.86, 0.8 * H, 0.32 * H),
                                   (h, 0.98 * H, 0, EI), (1.2, 0.95 * H, 0), (1.45, 0.3 * H, 0.12 * H, E), (D, 0, 0, E)])},
        "core": {"rotate": tl([(0, 0), (0.32, 8), (0.4, 0), (0.9, -360, E), (h, -372), (1.2, -366), (D, -360, E)])},
        "chest": {"scale": tl2([(0, 1, 1), (0.3, 1.08, 0.9), (0.42, 0.94, 1.08), (h - 0.06, 1, 1), (h + 0.04, 1.08, 0.9, EO),
                                (1.25, 1, 1), (D, 1, 1)])},
        "arm_r": {"rotate": tl([(0, 0), (0.3, 30), (0.6, 70), (h - 0.1, 165, E), (h, -25, EO), (1.25, -15), (D, 0)])},
        "sword": {"rotate": tl([(0, 0), (h - 0.1, 20), (h, -15, EO), (D, 0)])},
        "arm_l": {"rotate": tl([(0, 0), (0.3, -20), (0.6, 40), (h, -40, EO), (1.3, -10), (D, 0)])},
        "thigh_l": {"rotate": tl([(0, 0), (0.3, 8), (0.6, 35), (h - 0.08, 10), (h, -15, EO), (1.3, 0), (D, 0)])},
        "thigh_r": {"rotate": tl([(0, 0), (0.3, -8), (0.6, 40), (h - 0.08, 14), (h, 18, EO), (1.3, 0), (D, 0)])},
        "head": {"rotate": tl([(0, 0), (0.3, 6), (h, -8, EO), (D, 0)])},
        "wing_l": {"rotate": tl([(0, 0), (0.3, -20), (0.5, 18), (0.65, -20), (0.8, 18), (h, -10), (D, 0)])},
        "wing_r": {"rotate": tl([(0, 0), (0.3, 20), (0.5, -18), (0.65, 20), (0.8, -18), (h, 10), (D, 0)])},
        "tail": {"rotate": tl([(0, 0), (0.3, -12), (0.7, 20), (h, -14, EO), (1.3, 6), (D, 0)])},
        "ear_l": {"rotate": tl([(0, 0), (0.5, 20), (h, -12), (D, 0)])}, "ear_r": {"rotate": tl([(0, 0), (0.5, -20), (h, 12), (D, 0)])},
        "crest": {"rotate": tl([(0, 0), (0.5, 18), (h, -14), (1.3, 6), (D, 0)])},
        "shadow": {"scale": tl2([(0, 1, 1), (0.62, 0.62, 0.62, EO), (0.86, 0.8, 0.8), (h, 1, 1, EI), (1.45, 0.92, 0.92), (D, 1, 1)])},
        "fx_ring": {"rotate": tl([(0, 0), (0.6, -540, L)]), "scale": tl2([(0, 0.5, 0.5), (0.3, 1.05, 1.05, EO), (0.6, 1.25, 1.25)])},
        "fx_slash": {"translate": tl2([(0, 0.1 * H, -0.05 * H), (D, 0.1 * H, -0.05 * H)]),
                     "rotate": tl([(0, -35), (D, -35)]),
                     "scale": tl2([(0, 1, 1), (h - 0.04, 1, 1), (h + 0.18, 1.7, 1.7, EO), (D, 1.7, 1.7)])},
        "fx_wave": {"scale": tl2([(0, 0.4, 0.2), (h, 0.4, 0.2), (h + 0.2, 1.15, 1.15, EO), (h + 0.45, 1.25, 1.3), (D, 1.25, 1.3)])},
        "fx_splash": {"translate": tl2([(0, 0.15 * H, -0.3 * H), (D, 0.15 * H, -0.3 * H)]),
                      "scale": tl2([(0, 0.5, 0.5), (h, 0.5, 0.5), (h + 0.25, 1.6, 1.6, EO), (D, 1.6, 1.6)])},
    }, "slots": {
        "head": {"attachment": show([(0, "head"), (0.25, "head_shout"), (1.3, "head")])},
        "fx_ring_back": {"attachment": show([(0, "ring_back"), (0.62, None)]), "alpha": al([(0, 0), (0.25, 0.85, E), (0.45, 0.85), (0.6, 0, E)])},
        "fx_ring_front": {"attachment": show([(0, "ring_front"), (0.62, None)]), "alpha": al([(0, 0), (0.25, 0.55, E), (0.45, 0.55), (0.6, 0, E)])},
        "fx_slash": {"attachment": show([(0, None), (h - 0.04, "slash"), (h + 0.26, None)]),
                     "alpha": al([(0, 1), (h + 0.08, 1), (h + 0.26, 0, E)])},
        "fx_wave": {"attachment": show([(0, None), (h - 0.02, "wave"), (h + 0.62, None)]),
                    "alpha": al([(0, 1), (h + 0.35, 1), (h + 0.62, 0, E)])},
        "fx_splash": {"attachment": show([(0, None), (h, "splash"), (h + 0.36, None)]),
                      "alpha": al([(0, 1), (h + 0.12, 1), (h + 0.36, 0, E)])},
        "fx_ground": {"attachment": show([(0, None), (h, "ground"), (h + 0.5, None)]),
                      "alpha": al([(0, 1), (h + 0.2, 1), (h + 0.5, 0, E)])},
    }}
    # bóng là con của move (theo cú lao) nhưng nằm trên mặt đất: dời ngược độ cao của move
    A["skill"]["bones"]["shadow"]["translate"] = tl2([(0, 0, 0), (0.32, 0, 6), (0.62, 0, -0.55 * H, EO), (0.86, 0, -0.32 * H),
                                                      (h, 0, 0, EI), (1.2, 0, 0), (1.45, 0, -0.12 * H, E), (D, 0, 0, E)])
    A["skill"]["bones"]["fx_ground"] = {"translate": tl2([(0, 0.98 * H, 0), (D, 0.98 * H, 0)]),
                                        "scale": tl2([(0, 0.5, 0.5), (h, 0.5, 0.5), (h + 0.4, 1.3, 1.3, EO), (D, 1.3, 1.3)])}

    D = 2.4  # tiến hóa: vòng sóng dưới chân, lốc nước, xoay người bay lên, bọc bong bóng, thu nhỏ, bóng vỡ tung lấp lánh
    sp = {"fx_spark1": (-0.55, 0.45), "fx_spark2": (0.6, 0.2), "fx_spark3": (-0.25, -0.55)}
    ev = {"bones": {
        "move": {"translate": tl2([(0, 0, 0), (0.3, 0, -6), (1.4, 0, 0.22 * H, E), (D, 0, 0.22 * H)])},
        "core": {"scale": tl2([(0, 1, 1), (0.4, 1, 1), (0.65, -1, 1, E), (0.9, 1, 1, E), (1.1, -1, 1, E), (1.3, 1, 1, E),
                               (1.75, 0.16, 0.16, EI), (1.82, 0.01, 0.01), (D, 0.01, 0.01)])},
        "head": {"rotate": tl([(0, 0), (0.3, 4), (1.4, -4), (D, 0)])},
        "arm_l": {"rotate": tl([(0, 0), (0.4, -40), (1.4, -50), (D, -50)])},
        "arm_r": {"rotate": tl([(0, 0), (0.4, 95), (1.4, 110), (D, 110)])},
        "wing_l": {"rotate": tl(wave(-16, 0, D, n=24))}, "wing_r": {"rotate": tl(wave(16, 0, D, n=24))},
        "ear_l": {"rotate": tl([(0, 0), (0.6, 18), (D, 18)])}, "ear_r": {"rotate": tl([(0, 0), (0.6, -18), (D, -18)])},
        "tail": {"rotate": tl(wave(12, 0.2, D, n=24))},
        "crest": {"rotate": tl(wave(10, 0.3, D, n=24))},
        "shadow": {"scale": tl2([(0, 1, 1), (1.4, 0.6, 0.6, E), (1.8, 0.2, 0.2), (D, 0.2, 0.2)]),
                   "translate": tl2([(0, 0, 0), (0.3, 0, 6), (1.4, 0, -0.22 * H, E), (D, 0, -0.22 * H)])},
        "fx_ground": {"scale": tl2([(0, 0.4, 0.4), (0.5, 1.2, 1.2, EO), (1.4, 1.35, 1.35), (D, 1.35, 1.35)])},
        "fx_ring": {"rotate": tl([(0, 0), (1.8, -900, L), (D, -900)]),
                    "scale": tl2([(0, 0.4, 0.4), (0.6, 1.0, 1.0, EO), (1.4, 1.1, 1.1), (1.75, 0.5, 0.5, EI), (D, 0.5, 0.5)])},
        "fx_bubble": {"scale": tl2([(0, 0.3, 0.3), (0.8, 0.3, 0.3), (1.3, 1.08, 1.08, EO), (1.62, 0.96, 0.96), (1.74, 1.1, 1.1),
                                    (1.9, 1.55, 1.55, EO), (D, 1.55, 1.55)]),
                      "translate": tl2([(0, 0, 0), (D, 0, 0)])},
        # nổ ở tâm con (fx_splash gốc ở (0,62H; 0,42H) so với move, move đã bay lên cùng)
        "fx_splash": {"translate": tl2([(0, xy["core"][0] - 0.62 * H, xy["core"][1] - 0.42 * H),
                                        (D, xy["core"][0] - 0.62 * H, xy["core"][1] - 0.42 * H)]),
                      "scale": tl2([(0, 0.5, 0.5), (1.75, 0.5, 0.5), (2.15, 2.0, 2.0, EO), (D, 2.0, 2.0)])},
    }, "slots": {
        "head": {"attachment": show([(0, "head"), (0.35, "head_blink"), (1.0, "head_shout"), (1.6, "head_blink")])},
        "shadow": {"alpha": al([(0, 1), (1.8, 0.4), (D, 0, E)])},
        "fx_ground": {"attachment": show([(0, "ground"), (D, "ground")]), "alpha": al([(0, 0), (0.35, 1, E), (1.5, 0.9), (2.0, 0, E), (D, 0)])},
        "fx_ring_back": {"attachment": show([(0, None), (0.2, "ring_back"), (1.85, None)]),
                         "alpha": al([(0, 0), (0.2, 0), (0.6, 0.9, E), (1.5, 0.9), (1.8, 0, E)])},
        "fx_ring_front": {"attachment": show([(0, None), (0.2, "ring_front"), (1.85, None)]),
                          "alpha": al([(0, 0), (0.2, 0), (0.6, 0.5, E), (1.5, 0.5), (1.8, 0, E)])},
        "fx_bubble": {"attachment": show([(0, None), (0.8, "bubble"), (1.95, None)]),
                      "alpha": al([(0, 0), (0.8, 0), (1.3, 0.62, E), (1.74, 0.7), (1.92, 0, EO)])},
        "fx_splash": {"attachment": show([(0, None), (1.75, "splash"), (D, "splash")]),
                      "alpha": al([(0, 1), (1.95, 1), (D, 0, E)])},
    }}
    for name, (dx, dy) in sp.items():
        # lúc bóng vỡ lấp lánh bắn ra tới tâm con + (dx, dy) lần chiều cao (move đã mang độ bay lên)
        tx = xy["core"][0] + dx * H - xy[name][0]
        ty = xy["core"][1] + dy * H - xy[name][1]
        ev["bones"][name] = {
            "translate": tl2([(0, 0, 0), (1.75, 0, 0), (2.3, tx, ty, EO), (D, tx, ty)]),
            "scale": tl2([(0, 0.3, 0.3), (0.5, 1, 1, EO), (0.8, 0.6, 0.6), (1.1, 1, 1), (1.4, 0.6, 0.6), (1.75, 0.8, 0.8),
                          (1.95, 1.4, 1.4, EO), (D, 0.5, 0.5)]),
            "rotate": tl([(0, 0), (D, 180, L)])}
        ev["slots"][name] = {"attachment": show([(0, None), (0.3, "spark"), (D, "spark")]),
                             "alpha": al([(0, 0), (0.3, 0), (0.5, 1, E), (1.95, 1), (D, 0, E)])}
    A["evolve"] = ev
    return A
