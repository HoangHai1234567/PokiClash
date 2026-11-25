# -*- coding: utf-8 -*-
"""Xuất TIẾNG ĐÁNH NHAU đã chọn vào Unity: Assets/03 Art/Audio/Sfx/tran_<khoá>.ogg (mono, chuẩn độ to theo RMS phần có tiếng, đỉnh ≤ −1 dBFS,
cắt lặng, mờ đầu / cuối; vài tiếng TRỘN hai lớp). Người dùng 2026-11-24: "bạn tự chọn, nếu không hợp thì gen" — chọn bằng số đo
(ArtGen/Sfx/do_tieng.py) vì không nghe được; nguồn và giấy phép ở ArtGen/Sfx/tran/NGUON.md. Khoá dùng trong game: AudioImportMenu.Sfx,
SkillSfx.cs.
    py -3 ArtGen/Sfx/xuat_tieng_tran.py
"""
import os

import numpy as np
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
AM = os.path.join(HERE, "tran", "nghe", "am")
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "Assets", "03 Art", "Audio", "Sfx"))
SR = 44100

# khoá: ([(mã ứng viên, độ to lớp dB, lệch s)], RMS đích dB, cắt dài tối đa s, mờ vào s, mờ ra s)
CHON = {
    "hit": ([("huc_02", 0, 0)], -15, 0.4, 0, 0.05),                          # đòn trúng thường: đấm nặng (thay tiếng tổng hợp)
    "hitCrit": ([("huc_01", 0, 0), ("huc_06", -2, 0)], -13, 0.45, 0, 0.06),   # chí mạng: đấm + thịch trầm
    "ult": ([("gen_08", 0, 0)], -15, 1.6, 1.1, 0.25),                         # vào chiêu cuối: tụ năng lượng lớn dần (gen)
    "fx_tu": ([("gen_07", 0, 0)], -17, 1.0, 0.7, 0.15),                       # tụ chiêu mana (gen, cao dần)
    "fx_nha_tia": ([("gen_11", 0, 0)], -15, 0.6, 0, 0.1),                     # nhả tia / bắn đạn năng lượng (gen)
    "fx_no": ([("no_02", 0, 0)], -14, 1.3, 0, 0.3),                           # nổ
    "fx_no_nho": ([("no_01", 0, 0)], -16, 0.7, 0, 0.2),                       # nổ nhỏ, trúng lửa
    "fx_no_lon": ([("no_02", 0, 0), ("no_06", -1, 0)], -12, 1.6, 0, 0.4),      # nổ lớn: nổ + ầm trầm
    "fx_chem": ([("chem_04", 0, 0)], -15, 0.35, 0, 0.05),                     # chém
    "fx_chem2": ([("chem_10", 0, 0)], -15, 0.4, 0, 0.05),                     # chém trúng (dao cắt)
    "fx_kim": ([("kim_01", 0, 0)], -15, 0.4, 0, 0.08),                        # va kim loại
    "fx_huc": ([("huc_01", 0, 0), ("huc_08", -4, 0)], -14, 0.4, 0, 0.05),      # húc / nện của chiêu
    "fx_lua_bay": ([("lua_08", 0, 0)], -17, 1.1, 0, 0.25),                    # cầu lửa bay, lửa bùng
    "fx_phun_lua": ([("lua_09", 0, 0)], -16, 1.5, 0.05, 0.4),                 # phun lửa
    "fx_nuoc": ([("nuoc_09", 0, 0)], -16, 0.6, 0, 0.12),                      # nước toé
    "fx_nuoc_lon": ([("nuoc_04", 0, 0), ("nuoc_09", -3, 0)], -15, 1.1, 0, 0.3),  # nước toé lớn
    "fx_bong": ([("nuoc_10", 0, 0)], -18, 0.45, 0, 0.08),                     # bóng nước / cầu nước bật ra
    "fx_tia_nuoc": ([("gen_05", 0, 0)], -16, 1.5, 0.05, 0.4),                 # tia nước phun (gen)
    "fx_song": ([("gen_03", 0, 0)], -15, 2.4, 0.05, 0.5),                     # sóng đổ ụp (gen)
    "fx_loc": ([("gen_01", 0, 0)], -15, 1.9, 0.1, 0.5),                       # gió lốc (gen)
    "fx_gam": ([("gen_09", 0, 0)], -14, 1.7, 0, 0.4),                         # gầm lớn (gen)
    "fx_da": ([("da_06", 0, 0), ("da_03", -3, 0.03)], -15, 0.6, 0, 0.15),      # đá nện + đá vụn
    "fx_phep": ([("phep_01", 0, 0)], -17, 0.5, 0, 0.1),                       # phép / hồi / buff của chiêu
}


def load(mid):
    for ext in (".ogg", ".wav", ".mp3"):
        f = os.path.join(AM, mid + ext)
        if os.path.exists(f):
            x, sr = sf.read(f, always_2d=True)
            x = x.mean(1)
            if sr != SR:
                idx = np.arange(0, len(x) - 1, sr / SR)
                x = np.interp(idx, np.arange(len(x)), x)
            return x
    raise SystemExit("thiếu " + mid)


def trim(x):
    a = np.abs(x)
    on = np.where(a > a.max() * 0.02)[0]
    return x[max(0, on[0] - 64): on[-1] + 1] if len(on) else x


os.makedirs(OUT, exist_ok=True)
for key, (layers, rms_db, dmax, fin, fout) in CHON.items():
    mix = np.zeros(int(SR * (dmax + 0.5)))
    for mid, gain_db, off in layers:
        x = trim(load(mid))
        x = x / (np.sqrt(np.mean(x ** 2)) + 1e-9) * 10 ** (gain_db / 20)
        o = int(off * SR)
        n = min(len(x), len(mix) - o)
        mix[o:o + n] += x[:n]
    mix = trim(mix)[: int(SR * dmax)]
    if fin > 0:
        k = min(len(mix), int(fin * SR))
        mix[:k] *= np.linspace(0.15, 1, k) ** 1.5           # lớn dần (tiếng tụ)
    k = min(len(mix), int(fout * SR))
    if k > 0:
        mix[-k:] *= np.linspace(1, 0, k)
    mix = mix / (np.sqrt(np.mean(mix ** 2)) + 1e-9) * 10 ** (rms_db / 20)
    pk = np.abs(mix).max()
    if pk > 0.89:
        # đỉnh nhọn chạm trần → nén mềm (tanh) tăng dần tới khi đủ độ to đích, đỉnh ≤ −1 dBFS
        target = 10 ** ((rms_db - 1) / 20)
        base = mix / pk
        for drive in (1, 1.5, 2, 3, 4, 6, 8):
            y = np.tanh(drive * base) / np.tanh(drive) * 0.89
            if np.sqrt(np.mean(y ** 2)) >= target:
                break
        mix = y
    dst = os.path.join(OUT, f"tran_{key}.ogg")
    sf.write(dst, mix.astype(np.float32), SR, format="OGG", subtype="VORBIS")
    print(f"{key:12s} {len(mix) / SR:4.2f}s rms {20 * np.log10(np.sqrt(np.mean(mix ** 2)) + 1e-9):6.1f} dB  -> tran_{key}.ogg")
