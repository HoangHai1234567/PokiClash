# -*- coding: utf-8 -*-
"""Trang nghe thử TIẾNG ĐÁNH NHAU (người dùng 2026-11-24: "tìm sound cho các skill đánh nhau trong game (nổ, tụ tia năng lượng, chém,
húc,...)"). Nguồn: các gói CC0 đã tải ở ArtGen/Sfx/tran (Kenney Sci-Fi / Digital / RPG Audio, OpenGameArt: kiếm, gậy lửa, fireball,
quái vật, nước, phép, sci-fi, 80 RPG SFX) + ArtGen/Sfx/kenney/impact-sounds. Chép ứng viên vào <thư_mục_ra>/am/<mã>.<đuôi> (WAV nặng: cắt
khoảng lặng, mono 32 kHz 16 bit), ghi <thư_mục_ra>/nghe_tran.html (nghe, tick chọn, chép danh sách) và nguon.json (mã → tệp gốc + gói).
    py -3 -I ArtGen/Sfx/make_nghe_tran.py <thư_mục_ra>
"""
import glob
import json
import os
import shutil
import sys
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(HERE, "tran")
K = os.path.join(HERE, "kenney")
OUT = sys.argv[1]
AM = os.path.join(OUT, "am")
os.makedirs(AM, exist_ok=True)


def find(root, stem):
    hits = [f for f in glob.glob(os.path.join(root, "**", "*"), recursive=True)
            if os.path.splitext(os.path.basename(f))[0] == stem and f.lower().endswith((".ogg", ".wav", ".mp3"))]
    if not hits:
        raise SystemExit(f"thiếu {root} / {stem}")
    return hits[0]


def wav_small(src, dst, sr_out=32000):
    """WAV bất kỳ (16/24/32 bit, stereo) → mono 16 bit sr_out, cắt lặng đầu / cuối, mờ 60 ms cuối."""
    w = wave.open(src)
    n, sr, ch, sw = w.getnframes(), w.getframerate(), w.getnchannels(), w.getsampwidth()
    raw = w.readframes(n)
    w.close()
    if sw == 3:
        a = np.frombuffer(raw, np.uint8).reshape(-1, 3)
        v = a[:, 0].astype(np.int32) | (a[:, 1].astype(np.int32) << 8) | (a[:, 2].astype(np.int32) << 16)
        v = np.where(v >= 1 << 23, v - (1 << 24), v) / float(1 << 23)
    elif sw == 2:
        v = np.frombuffer(raw, np.int16) / 32768.0
    else:
        v = np.frombuffer(raw, np.int32) / 2.0 ** 31
    v = v.reshape(-1, ch).mean(1)
    on = np.where(np.abs(v) > 0.01)[0]
    if len(on):
        v = v[max(0, on[0] - int(0.01 * sr)): min(len(v), on[-1] + int(0.15 * sr))]
    idx = np.arange(0, len(v) - 1, sr / sr_out)
    v = np.interp(idx, np.arange(len(v)), v)
    f = min(len(v), int(0.06 * sr_out))
    v[-f:] *= np.linspace(1, 0, f)
    o = wave.open(dst, "wb")
    o.setnchannels(1)
    o.setsampwidth(2)
    o.setframerate(sr_out)
    o.writeframes((np.clip(v, -1, 1) * 32767).astype(np.int16).tobytes())
    o.close()


# nhóm: (mã nhóm, tên, ghi chú dùng trong game, [(gói, thư mục gốc, [tên tệp không đuôi])])
G = [
    ("no", "Nổ", "Quả nổ lửa lớn (no), cầu lửa / thiên thạch chạm đất, nổ trúng.",
     [("Kenney Sci-Fi", "kenney_sci-fi-sounds", [f"explosionCrunch_00{i}" for i in range(5)] + ["lowFrequency_explosion_000", "lowFrequency_explosion_001"]),
      ("OGA Fireball", "oga_fireball", ["fireball_01"])]),
    ("tu", "Tụ năng lượng", "Lấy đà chiêu: cầu đang tụ, tụ tia ở miệng / trượng, gồng chiêu cuối.",
     [("Kenney Digital", "kenney_digital-audio", ["phaserUp1", "phaserUp3", "phaserUp5", "phaserUp7", "powerUp2", "powerUp4", "powerUp8", "powerUp11"]),
      ("Kenney Sci-Fi", "kenney_sci-fi-sounds", ["forceField_000", "forceField_002", "forceField_004"]),
      ("OGA Magic Spell", "oga_phep", ["magical_1_0", "magical_3", "magical_5"])]),
    ("tia", "Bắn tia năng lượng", "Nhả tia (tia lửa / nước / vàng / lá), đạn năng lượng, kim bay.",
     [("Kenney Sci-Fi", "kenney_sci-fi-sounds", ["laserLarge_000", "laserLarge_002", "laserLarge_004", "laserRetro_001", "laserRetro_003"]),
      ("Kenney Digital", "kenney_digital-audio", ["laser3", "laser6", "zap1", "zapTwoTone"])]),
    ("chem", "Chém", "Đao / kiếm / vuốt / đuôi quất chém, lướt chém.",
     [("OGA 20 Sword", "oga_kiem", [f"sword.{i}" for i in (1, 2, 4, 6, 8, 10)]),
      ("OGA 80 RPG", "oga_rpg", ["blade_01", "blade_02", "blade_03"]),
      ("Kenney RPG", "kenney_rpg-audio", ["knifeSlice", "knifeSlice2", "chop"])]),
    ("kim", "Va chạm kim loại", "Đao chạm giáp, chặn đòn, khiên, tướng hệ Kim.",
     [("OGA Sword Clash", "oga_kiem_cham", [f"sword_clash.{i}" for i in (1, 3, 5, 7, 9)]),
      ("OGA 80 RPG", "oga_rpg", ["metal_01", "metal_02", "metal_03"]),
      ("Kenney Sci-Fi", "kenney_sci-fi-sounds", ["impactMetal_000", "impactMetal_002"])]),
    ("huc", "Húc / đấm / quật", "Lao tới húc, đấm, nện, đuôi quật, nhảy đè (đòn thường).",
     [("Kenney Impact", K + "/impact-sounds", ["impactPunch_heavy_000", "impactPunch_heavy_002", "impactPunch_heavy_004", "impactPunch_medium_001",
                                                "impactSoft_heavy_000", "impactSoft_heavy_003", "impactPlate_heavy_001", "impactWood_heavy_002"])]),
    ("lua", "Lửa", "Phun lửa, cầu lửa bay, lửa bùng / cháy, kim lửa.",
     [("OGA 80 RPG", "oga_rpg", [f"spell_fire_0{i}" for i in range(1, 8)]),
      ("OGA Fire Staff", "oga_lua_gay", ["LEGIT_FIR_Fire_Staff 1-Audio", "LEGIT_FIR_Fire_Staff 10-Audio", "LEGIT_FIR_Fire_Staff 12-Audio",
                                         "LEGIT_FIR_Fire_Staff 13-Audio"]),
      ("Kenney Sci-Fi", "kenney_sci-fi-sounds", ["thrusterFire_001", "thrusterFire_003"])]),
    ("nuoc", "Nước", "Nước toé, cầu nước vỡ, tia nước (vòng lặp), bong bóng, bóng mực.",
     [("OGA 40 Water", "oga_nuoc", [f"splash_{i:02d}" for i in (1, 3, 5, 7, 9, 11, 13, 15)] + ["bubble_01", "bubble_03", "loop_water_01", "slime_03",
                                                                                              "slime_07"])]),
    ("gam", "Gầm", "Tướng thú gầm (sóng âm), boss xuất hiện, chiêu cuối.",
     [("OGA 80 Creature", "oga_quai", ["roar_01", "roar_02", "roar_03", "monster_01", "monster_03", "monster_05", "monster_07", "howl"]),
      ("OGA 80 RPG", "oga_rpg", ["creature_roar_01", "creature_roar_02", "creature_roar_03"])]),
    ("da", "Đá / đất", "Gai đất trồi, đá văng, đất nứt, nện xuống đất (hệ Thổ).",
     [("OGA 80 RPG", "oga_rpg", ["stones_01", "stones_02", "stones_03", "stones_04", "item_stone_01"]),
      ("Kenney Impact", K + "/impact-sounds", ["impactMining_000", "impactMining_003", "impactWood_heavy_000"])]),
    ("phep", "Phép / buff", "Hồi máu, tăng sức, khiên, chiêu phép chung.",
     [("OGA 80 RPG", "oga_rpg", ["spell_01", "spell_02"]),
      ("OGA Magic Spell", "oga_phep", ["magical_2", "magical_4", "magical_6_0", "magical_7_0"])]),
    ("dau", "Trúng đòn (kêu đau)", "Tướng bị đánh trúng, gục.",
     [("OGA 80 Creature", "oga_quai", ["hurt_01", "hurt_02", "hurt_03", "hurt_04", "grunt_01", "grunt_03"]),
      ("OGA 80 RPG", "oga_rpg", ["creature_hurt_01", "creature_hurt_02", "creature_die_01"])]),
    ("khac", "Năng lượng khác (gói 60 Sci-Fi)", "Tiếng điện tử lạ để thử cho tia, đạn, khiên, dịch chuyển.",
     [("OGA 60 Sci-Fi", "oga_scifi", ["sfx_01a", "sfx_03a", "sfx_05a", "sfx_07a", "sfx_09a", "sfx_11a", "sfx_13a", "sfx_15a", "sfx_17a", "sfx_19a"])]),
    # gen thêm bằng Magnific (ElevenLabs SFX, 2026-11-24, người dùng: "cần thì gen"): những loại không có trong gói CC0
    ("gen", "Gen thêm (Magnific)", "Không có trong gói miễn phí nên gen: gió / lốc xoáy (gen_01–02), sóng lớn đổ ụp (gen_03–04), tia nước phun dài, lặp liền (gen_05–06); đợt 2: tụ năng lượng (gen_07–08), gầm lớn (gen_09–10), nhả tia (gen_11–12).",
     [("Magnific SFX", "gen_1124", ["gio_loc_1", "gio_loc_2", "song_do_1", "song_do_2", "tia_nuoc_loop_1", "tia_nuoc_loop_2", "tu_nang_luong_1", "tu_nang_luong_2", "gam_lon_1", "gam_lon_2", "nha_tia_1", "nha_tia_2"])]),
]

groups, src_map = [], {}
for code, name, note, packs in G:
    items = []
    n = 0
    for pack, root, stems in packs:
        rdir = root if os.path.isabs(root) else os.path.join(T, root)
        for st in stems:
            n += 1
            f = find(rdir, st)
            ext = os.path.splitext(f)[1].lower()
            mid = f"{code}_{n:02d}"
            if ext == ".wav" and os.path.getsize(f) > 150_000:
                wav_small(f, os.path.join(AM, mid + ".wav"))
                ext = ".wav"
            else:
                shutil.copyfile(f, os.path.join(AM, mid + ext))
            items.append(dict(id=mid, file="am/" + mid + ext, pack=pack, name=st))
            src_map[mid] = dict(src=os.path.relpath(f, HERE).replace("\\", "/"), pack=pack)
    groups.append(dict(code=code, name=name, note=note, items=items))

tpl = open(os.path.join(HERE, "nghe_tran_tpl.html"), encoding="utf-8").read()
open(os.path.join(OUT, "nghe_tran.html"), "w", encoding="utf-8").write(tpl.replace("/*NHOM*/[]", json.dumps(groups, ensure_ascii=False)))
json.dump(src_map, open(os.path.join(OUT, "nguon.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
tot = sum(os.path.getsize(os.path.join(AM, x)) for x in os.listdir(AM))
print("ok", sum(len(g["items"]) for g in groups), "files", f"{tot / 1048576:.1f} MB")
