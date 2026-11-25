# -*- coding: utf-8 -*-
"""Xuất bộ lửa Blender (frames/<tên>_bl, người dùng duyệt 2026-11-24: "thay các fx vừa làm vào game") vào Unity:
    Assets/03 Art/Fx/Hat/hat_fb_<tên game>_NN.png   (HatLua.Fb… tra bằng S("fb_<tên game>_NN"))

Tên game cũ (no, khoi, lua_lap, cau_lua, loc_lua) GHI ĐÈ ảnh cùng tên → giữ .meta / GUID, mảng hatSprites của prefab không đổi; khung dư
(26 khung nổ, 25 khói, 48 lốc) và tên mới (phun, kim_lua, duoi_lua) là ảnh mới → chạy menu "PokiClash/Prefab/Trận/Sàn đấu: hạt lửa (bộ Hỏa)"
và "Hộp chi tiết tướng: hạt lửa + nút Mana" để nạp. Ảnh cũ: git + ArtGen/Spine/vfx_gen/khung/<tên> (xuat_fb.py đã bỏ các tên này).
Thu nhỏ cho gần cỡ bộ cũ (~250 px; phun 512 ngang). In bảng FbDef (n, w, h, px, py) để dán vào HatFlip.cs.

    py -3 -I ArtGen/Spine/vfx_lua_toon/xuat_game.py [tên game ...]
"""
import json
import os
import sys

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
FR = os.path.join(HERE, "frames")
OUT = os.path.join(ROOT, "Assets", "03 Art", "Fx", "Hat")
# tên game: (bộ khung, cạnh dài tối đa (px), điểm neo (px trong khung gốc) hoặc None = neo của manifest)
MAP = {
    "cau_lua": ("cau_bl", 180, None),           # cầu tròn, neo tâm
    "lua_lap": ("lua_bl", 280, None),           # lửa cháy lặp, neo chân
    "no": ("no_bl", 300, (224, 335)),           # nổ tròn: neo ở ĐÁY quả nổ lúc to nhất (khung 9), tâm ngang 224
    "khoi": ("khoi_bl", 280, (175, 345)),       # cụm khói: neo ở đáy cụm lúc phồng đủ (chân)
    "loc_lua": ("loc_bl", 420, None),           # lốc một lượt 2 s, neo chân phễu
    "phun": ("phun_bl2", 512, None),            # phun lửa, neo miệng (mép trái)
    "kim_lua": ("kim_bl", 300, None),           # kim xoắn, mũi về +x
    "duoi_lua": ("duoi_bl", 240, None),         # hạt vệt đuôi cầu lửa (lửa đậm → khói), neo tâm cụm lúc sinh
    # cầu NĂNG LƯỢNG kiểu Energy Ball (vfx_blender/cau_nl_bl.py + cat_nl.py, người dùng chọn 2026-11-24), tên MỚI, lặp 36 khung, neo tâm:
    # 256 px (render --px 400): cầu to (Lộc Phong, Pháo Giáp) ở 180 px bị phóng ~1,9 lần, mờ trên máy
    "cau_moc": ("cau_nl_moc", 256, None),       # lục ngọc + gân chanh: CauLa (Gạc Đá, Lộc Phong), đầu nòng tia lá DaTiaMoc
    "cau_vang": ("cau_nl_vang", 256, None),     # cam vàng + gân kem: RbCau (Thần Cơ, Pháo Giáp), đầu nòng tia vàng DaTiaVang
    "cau_troi": ("cau_nl_troi", 256, None),     # cam đỏ + gân vàng: Mặt Trời của Thổ Tinh
}


def main():
    man = json.load(open(os.path.join(FR, "manifest.json"), encoding="utf-8"))
    names = sys.argv[1:] or list(MAP)
    tot = 0
    for g in names:
        src, mx, anc = MAP[g]
        m = man[src]
        w, h = m["w"], m["h"]
        ax, ay = anc or m["anchor"]
        s = min(1.0, mx / max(w, h))
        W, H = max(1, round(w * s)), max(1, round(h * s))
        for i in range(m["count"]):
            im = Image.open(os.path.join(FR, src, f"{src}_{i:02d}.png")).convert("RGBA")
            if s < 1:
                im = im.convert("RGBa").resize((W, H), Image.LANCZOS).convert("RGBA")   # nhân alpha trước khi thu: không viền tối
            dst = os.path.join(OUT, f"hat_fb_{g}_{i:02d}.png")
            im.save(dst, optimize=True)
            tot += os.path.getsize(dst)
        print(f'{{ "{g}", new FbDef({m["count"]}, {W}, {H}, {ax / w:.3f}f, {(h - ay) / h:.3f}f, {"true" if m["loop"] else "false"}) }},')
    print("tổng %.1f MB vào %s" % (tot / 1048576, OUT))


if __name__ == "__main__":
    main()
