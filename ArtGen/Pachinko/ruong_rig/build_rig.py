# Rig rương máy bi bằng AtomSpine (GD_Claude/23_MayBi_TraiNghiem.md giai đoạn 1). Một bộ lệnh chung cho ba bậc gỗ, bạc, vàng.
# Hình lấy từ Assets/03 Art/Pachinko: pk_ruong_<bậc>_than (thân, miệng lộ lòng kem), _nap (nắp), _mo_sach (rương mở sạch); quầng
# ấm trong lòng rương và tia lọt khe vẽ bằng script (máy bi được phép quầng mềm từ 2026-11-10); lấp lánh dùng fx_sparkle.
# Clip: cho (đứng thở), nhac (nhắc mở: nhún, lắc, nắp hé hai lần có sáng và tia lọt khe, sập lại; lặp), gong (gồng trước khi mở,
# code co giãn tốc theo bậc), bat (nắp bật, sự kiện "open" ở khung đổi sang rương mở sạch), mo (mở rồi, lòng sáng phập phồng).
# Ra: ruong_rig/<bậc>/ (dự án AtomSpine, tờ soi .atomspine/soi_<clip>.png), Assets/03 Art/Pachinko/Rig/ruong_<bậc>.bytes
# (đuôi .bytes để Unity nhập thành TextAsset; gói AtomSpine nạp bằng AtomikFile.Load, xem UNITY.md "Runtime loading").
# Chạy: py -3 -I ArtGen/Pachinko/ruong_rig/build_rig.py [go bac vang]
import math
import os
import shutil
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ART = os.path.join(ROOT, "Assets", "03 Art", "Pachinko")
OUT = os.path.join(ART, "Rig")
ATOM = os.environ.get("ATOM_CLI", r"D:\AtomSpine\packages\cli\dist\atom.mjs")
CANVAS = 320
# màu quầng trong lòng rương theo bậc (RRGGBB) và số tia
TIERS = {
    "go": dict(glow="FFC15A", ray="FFD98A", rays=3),
    "bac": dict(glow="FFF0B8", ray="FFF4C8", rays=4),
    "vang": dict(glow="FFD84A", ray="FFE36A", rays=5),
}
SPAN_CLOSED, SPAN_OPEN = 150, 70  # độ xoè quạt tia: lúc hé (lọt khe, toả sang hai bên) và lúc đã mở (gom lên trên)


def atom(proj, *args):
    r = subprocess.run(["node", ATOM, *args], cwd=proj, capture_output=True, text=True, encoding="utf-8")
    out = (r.stdout + r.stderr).strip()
    if r.returncode != 0:
        raise SystemExit("atom %s lỗi:\n%s" % (" ".join(args), out))
    return out


def soft_glow(path, w=300, h=130):
    """Quầng ấm mềm: elip trắng, alpha giảm dần ra mép (màu do slot tô)."""
    y, x = np.mgrid[0:h, 0:w]
    d = np.sqrt(((x - w / 2) / (w / 2)) ** 2 + ((y - h / 2) / (h / 2)) ** 2)
    a = np.clip(1 - d, 0, 1) ** 1.6
    img = np.zeros((h, w, 4), np.uint8)
    img[..., :3] = 255
    img[..., 3] = (a * 255).astype(np.uint8)
    Image.fromarray(img).save(path)


def ray(path, w=190, h=46):
    """Tia sáng: nêm thuôn từ gốc (trái, hẹp) ra ngọn (phải, rộng), lõi đặc, ngọn mờ dần; trắng để slot tô màu."""
    K = 4
    im = Image.new("L", (w * K, h * K), 0)
    d = ImageDraw.Draw(im)
    d.polygon([(0, h * K / 2 - 2 * K), (w * K, 2 * K), (w * K, h * K - 2 * K), (0, h * K / 2 + 2 * K)], fill=255)
    a = np.asarray(im.resize((w, h), Image.LANCZOS).filter(ImageFilter.GaussianBlur(1.2))).astype(float) / 255
    fade = np.clip(1.15 - np.linspace(0, 1, w) ** 1.4, 0, 1)[None, :]
    img = np.zeros((h, w, 4), np.uint8)
    img[..., :3] = 255
    img[..., 3] = (a * fade * 235).astype(np.uint8)
    Image.fromarray(img).save(path)


def build(tier):
    cfg = TIERS[tier]
    proj = os.path.join(HERE, tier)
    if not os.path.exists(os.path.join(proj, "atomspine.json")):
        atom(HERE, "init", tier, "--name", "ruong_" + tier)
    imgs = os.path.join(proj, "images")
    os.makedirs(imgs, exist_ok=True)
    for src, dst in (("_than", "than"), ("_nap", "nap"), ("_mo_sach", "mo")):
        shutil.copyfile(os.path.join(ART, "pk_ruong_%s%s.png" % (tier, src)), os.path.join(imgs, dst + ".png"))
    shutil.copyfile(os.path.join(ART, "fx_sparkle.png"), os.path.join(imgs, "lap.png"))
    soft_glow(os.path.join(imgs, "glow.png"))
    ray(os.path.join(imgs, "tia.png"))
    sh = Image.open(os.path.join(ART, "pk_ruong_%s.png" % tier)).height   # rương đóng: mép dưới nắp ở sh - cao nắp
    lid_h = Image.open(os.path.join(imgs, "nap.png")).height
    body_h = Image.open(os.path.join(imgs, "than.png")).height
    open_h = Image.open(os.path.join(imgs, "mo.png")).height
    lip = sh - lid_h                    # mép dưới nắp (px từ đất)
    gy = lip + 8                        # gốc quầng và tia: đường khe giữa nắp và thân
    n = cfg["rays"]
    off = [(i - (n - 1) / 2) / max(1, (n - 1) / 2) for i in range(n)] if n > 1 else [0.0]  # -1 .. 1
    fan = [90 + o * SPAN_CLOSED / 2 for o in off]
    fan_open = [o * (SPAN_OPEN - SPAN_CLOSED) / 2 for o in off]  # xoay thêm khi đã mở

    ops = [
        "project.set name=ruong_%s fps=30 ppu=100" % tier,
        "bone.add chest parent=root x=0 y=0",
        "bone.add nap parent=chest x=0 y=%d" % lip,
        "bone.add glow parent=chest x=0 y=%d" % gy,
        "part.add than at=0,%d canvas=%d,%d bone=chest" % (CANVAS - body_h, CANVAS, CANVAS),
        "image.add glow path=images/glow.png",
        "slot.add glow bone=glow att=glow color=%sFF at=front" % cfg["glow"],
        "image.add tia path=images/tia.png",
    ]
    for i, a in enumerate(fan):
        ops += ["bone.add tia%d parent=glow x=0 y=6 rot=%.1f" % (i + 1, a),
                "slot.add tia%d bone=tia%d color=%sFF at=front" % (i + 1, i + 1, cfg["ray"]),
                "att.region tia%d tia image=tia x=95 y=0" % (i + 1)]
    ops += [
        "part.add nap at=0,%d canvas=%d,%d bone=nap" % (CANVAS - sh, CANVAS, CANVAS),
        # dải sáng dọc khe, vẽ trên nắp: quầng elip dẹt
        "bone.add khe parent=chest x=0 y=%d" % (lip + 4),
        "slot.add khe bone=khe color=%sFF at=front" % cfg["glow"],
        "att.region khe khe image=glow sx=1.05 sy=0.32",
        "part.add mo at=0,%d canvas=%d,%d bone=chest" % (CANVAS - open_h, CANVAS, CANVAS),
        "image.add lap path=images/lap.png",
    ]
    ops += ["slot.order tia%d to=before:mo" % (i + 1) for i in range(n)]  # tia trên nắp, dưới rương mở
    for i, (lx, ly) in enumerate([(-60, 0), (8, 14), (64, 4)]):
        ops += ["bone.add lap%d parent=glow x=%d y=%d" % (i + 1, lx, ly),
                "slot.add lap%d bone=lap%d at=front" % (i + 1, i + 1),
                "att.region lap%d lap image=lap sx=0.42 sy=0.42" % (i + 1)]
    # mặc định: quầng, tia, lấp lánh, rương mở không có hình (ẩn bằng hình rỗng, không bằng alpha: khoá alpha trong clip bị nhân
    # với alpha của màu slot, để alpha mặc định 0 thì clip không hiện được)
    ops += ["slot.set glow att=-", "slot.set khe att=-", "slot.set mo att=-"]
    ops += ["slot.set tia%d att=-" % (i + 1) for i in range(n)]
    ops += ["slot.set lap%d att=-" % (i + 1) for i in range(3)]
    open_glow_dy = int(open_h * 0.72) - gy  # lòng rương mở cao hơn miệng thân

    T = ["tia%d" % (i + 1) for i in range(n)]
    L = ["lap%d" % (i + 1) for i in range(3)]
    # lúc đóng: quầng dưới nắp (chỉ lộ ở khe), tia và dải khe trên nắp (lọt khe toả ra); lúc mở: rương mở là một ảnh liền nên
    # quầng, tia vẽ đè lên lòng rương
    closed_order = ["than", "glow", "nap", "khe"] + T + ["mo"] + L
    open_order = ["than", "nap", "khe", "mo", "glow"] + T + L

    def lights_on(anim, t=0, slit=True):
        k = ["key %s glow.attachment %g:glow" % (anim, t)] + ["key %s %s.attachment %g:tia" % (anim, x, t) for x in T]
        return k + (["key %s khe.attachment %g:khe" % (anim, t)] if slit else [])

    def fan_open_keys(anim, t0, t1=None):
        """Xoay tia gom lên khi đã mở (từ t0, hoặc chạy từ t0 tới t1)."""
        out = []
        for x, d in zip(T, fan_open):
            out.append("key %s %s.rotate %s" % (anim, x, ("%g:0:easeOut %g:%.1f" % (t0, t1, d)) if t1 is not None else ("%g:%.1f" % (t0, d))))
        return out

    def rays_alpha(anim, pts):
        return ["key %s %s.alpha %s" % (anim, t, " ".join(pts)) for t in T]

    def rays_scale(anim, pts):
        return ["key %s %s.scale %s" % (anim, t, " ".join(pts)) for t in T]

    # --- cho: đứng thở (2,4 giây) ---
    ops += ["anim.add cho dur=2.4 loop=true",
            "key cho chest.scale 0:1,1:ease 1.2:1.012,0.988:ease 2.4:1,1",
            "key cho nap.translate 0:0,0:ease 1.2:0,1.5:ease 2.4:0,0"]

    # --- nhac: nhắc mở (3,2 giây, lặp): nhún, lắc, nắp hé nhỏ rồi hé to có sáng và tia lọt khe, sập lại ---
    A = "nhac"
    ops += [f"anim.add {A} dur=3.2 loop=true",
            f"key {A} chest.scale 0:1,1 0.12:1.06,0.92:easeOut 0.26:0.95,1.07:easeOut 0.42:1,1:ease 1.7:1,1 1.76:1.05,0.94:easeOut 1.9:1,1:ease 3.2:1,1",
            f"key {A} chest.translate 0:0,0 0.26:0,0:easeOut 0.37:0,14:easeIn 0.48:0,0 3.2:0,0",
            f"key {A} chest.rotate 0:0 0.48:0:ease 0.58:-5:ease 0.7:4:ease 0.82:-2:ease 0.92:0 3.2:0",
            f"key {A} nap.translate 0:0,0 0.95:0,0:easeOut 1.05:0,9:easeIn 1.18:0,0 1.3:0,0:easeOut 1.43:0,17 1.62:0,16:easeIn 1.7:0,0 3.2:0,0",
            f"key {A} nap.rotate 0:0 0.95:0:easeOut 1.05:-3:easeIn 1.18:0 1.3:0:easeOut 1.43:4 1.62:3:easeIn 1.7:0 3.2:0",
            f"key {A} glow.alpha 0:0 0.95:0:easeOut 1.05:0.75 1.18:0.12 1.3:0.12:easeOut 1.43:1 1.62:0.9:easeIn 1.72:0 3.2:0",
            f"key {A} khe.alpha 0:0 0.95:0:easeOut 1.05:0.6 1.18:0 1.3:0:easeOut 1.43:0.9 1.62:0.75:easeIn 1.72:0 3.2:0",
            f"key {A} khe.translate 0:0,0 0.95:0,0:easeOut 1.05:0,4 1.18:0,0 1.3:0,0:easeOut 1.43:0,8 1.7:0,0 3.2:0,0"]
    ops += lights_on(A)
    ops += rays_alpha(A, ["0:0", "0.95:0:easeOut", "1.05:0.7", "1.18:0", "1.3:0:easeOut", "1.43:1", "1.62:0.85:easeIn", "1.72:0", "3.2:0"])
    ops += rays_scale(A, ["0:0.4,0.6", "0.95:0.4,0.6:easeOut", "1.05:0.9,0.9", "1.18:0.4,0.6", "1.3:0.4,0.6:easeOut", "1.43:1.15,1", "1.62:1.1,1:easeIn", "1.72:0.4,0.6", "3.2:0.4,0.6"])
    for i, l in enumerate(L):
        t0 = 1.42 + i * 0.06
        dx = (-26, 4, 30)[i]
        ops += [f"key {A} {l}.attachment 0:- {t0:.2f}:lap {t0 + 0.5:.2f}:-",
                f"key {A} {l}.translate 0:0,0 {t0:.2f}:0,0:easeOut {t0 + 0.5:.2f}:{dx},64 3.2:0,0",
                f"key {A} {l}.scale 0:0.4,0.4 {t0:.2f}:0.4,0.4:easeOut {t0 + 0.18:.2f}:1,1:easeIn {t0 + 0.5:.2f}:0.3,0.3 3.2:0.4,0.4",
                f"key {A} {l}.rotate 0:0 {t0:.2f}:0 {t0 + 0.5:.2f}:90 3.2:0"]

    # --- gong: gồng (0,6 giây): lắc mạnh dần, nén, nắp lạch cạch cao dần, sáng tăng ---
    A = "gong"
    rot = " ".join("%.2f:%d" % (k * 0.05, (1 if k % 2 else -1) * (2 + k // 2)) for k in range(1, 12))
    lid = " ".join("%.2f:0,%d" % (k * 0.05, (4 + k) if k % 2 else 0) for k in range(1, 12))
    ops += [f"anim.add {A} dur=0.6",
            f"key {A} chest.rotate 0:0 {rot} 0.6:0",
            f"key {A} chest.scale 0:1,1:easeIn 0.6:1.06,0.9",
            f"key {A} nap.translate 0:0,0 {lid} 0.6:0,14",
            f"key {A} glow.alpha 0:0.15:easeIn 0.6:1",
            f"key {A} khe.alpha 0:0.2:easeIn 0.6:1",
            f"key {A} khe.translate 0:0,0 0.6:0,7"]
    ops += lights_on(A)
    ops += rays_alpha(A, ["0:0.2:easeIn", "0.6:1"])
    ops += rays_scale(A, ["0:0.5,0.6:easeIn", "0.6:1.2,1"])

    # --- bat: nắp bật (0,45 giây), "open" ở 0,07: đổi sang rương mở sạch, bóp giãn như màn mở cũ ---
    A = "bat"
    ops += [f"anim.add {A} dur=0.45",
            f"key {A} nap.translate 0:0,14:easeOut 0.06:0,44",
            f"key {A} nap.rotate 0:0:easeOut 0.06:-22",
            f"key {A} than.attachment 0:than 0.07:-",
            f"key {A} nap.attachment 0:nap 0.07:-",
            f"key {A} mo.attachment 0:- 0.07:mo",
            f"key {A} chest.scale 0:1.06,0.9 0.07:1.25,0.8:easeOut 0.17:0.9,1.15:ease 0.3:1,1",
            f"key {A} glow.translate 0:0,0 0.07:0,{open_glow_dy}",
            f"key {A} glow.alpha 0:1 0.45:0.85",
            f"key.order {A} t=0 order={','.join(closed_order)}",
            f"key.order {A} t=0.07 order={','.join(open_order)}",
            f"key {A} khe.alpha 0:1 0.07:0",
            f"event {A} 0.07 open"]
    ops += lights_on(A)
    ops += fan_open_keys(A, 0.07, 0.2)
    ops += rays_alpha(A, ["0:1", "0.2:1:ease", "0.45:0.55"])
    ops += rays_scale(A, ["0:1.2,1:easeOut", "0.12:1.5,1.1:ease", "0.45:1.1,1"])

    # --- mo: đã mở (1,6 giây, lặp): lòng sáng phập phồng, tia xoay nhẹ ---
    A = "mo"
    ops += [f"anim.add {A} dur=1.6 loop=true",
            f"key {A} than.attachment 0:-",
            f"key {A} nap.attachment 0:-",
            f"key {A} mo.attachment 0:mo",
            f"key {A} glow.translate 0:0,{open_glow_dy}",
            f"key {A} glow.alpha 0:0.65:ease 0.8:0.95:ease 1.6:0.65",
            f"key {A} glow.rotate 0:-4:ease 0.8:4:ease 1.6:-4",
            f"key.order {A} t=0 order={','.join(open_order)}"]
    ops += lights_on(A, slit=False)
    ops += fan_open_keys(A, 0)
    ops += rays_alpha(A, ["0:0.4:ease", "0.8:0.6:ease", "1.6:0.4"])
    ops += rays_scale(A, ["0:1,1:ease", "0.8:1.12,1:ease", "1.6:1,1"])

    with open(os.path.join(proj, "rig.ops"), "w", encoding="utf-8") as f:
        f.write("\n".join(ops) + "\n")
    # dựng lại từ đầu mỗi lần: dự án mới
    fresh = os.path.join(HERE, "_tmp_" + tier)
    if os.path.exists(fresh):
        shutil.rmtree(fresh)
    atom(HERE, "init", "_tmp_" + tier, "--name", "ruong_" + tier)
    shutil.copytree(imgs, os.path.join(fresh, "images"), dirs_exist_ok=True)
    shutil.copyfile(os.path.join(proj, "rig.ops"), os.path.join(fresh, "rig.ops"))
    print(tier, atom(fresh, "do", "-f", "rig.ops").splitlines()[-1])
    for anim, frames in (("nhac", 12), ("gong", 6), ("bat", 6), ("mo", 4)):
        atom(fresh, "sheet", "--anim", anim, "--frames", str(frames), "--labels", "-o", ".atomspine/soi_%s.png" % anim)
    print(atom(fresh, "lint").splitlines()[-1] if atom(fresh, "lint") else "lint ok")
    atom(fresh, "export", "atomik", "--atlas-cap", "240")  # rương hiện tối đa khoảng 260 px: atlas nhỏ, nạp lúc chạy không nén
    # thay dự án chính bằng bản vừa dựng
    shutil.rmtree(proj)
    shutil.move(fresh, proj)
    exp = os.path.join(proj, "export", "ruong_%s.atomik" % tier)
    os.makedirs(OUT, exist_ok=True)
    shutil.copyfile(exp, os.path.join(OUT, "ruong_%s.bytes" % tier))
    print(tier, "xuất", os.path.getsize(exp), "byte →", os.path.join(OUT, "ruong_%s.bytes" % tier))


if __name__ == "__main__":
    for t in (sys.argv[1:] or list(TIERS)):
        build(t)
