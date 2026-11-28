# -*- coding: utf-8 -*-
"""Xuất TIẾNG CHIÊU RIÊNG (2026-11-28) vào Unity: Assets/03 Art/Audio/Sfx/tran_<khoá>.ogg, cùng chuẩn với xuat_tieng_tran.py (mono,
chuẩn độ to theo RMS, đỉnh ≤ −1 dBFS, nén mềm tanh, cắt lặng, mờ đầu / cuối). Người dùng 2026-11-28: "quét kĩ lại phần combat và chiêu
của từng tướng chưa có sound ... tiếng hét, lốc, cầu lửa, va chạm, tiếng nước bắn, tiếng đất, tiếng tia laser từ mặt trời đâm xuống,
thiên thạch va chạm, tiếng nổ ... thiếu thì tìm trên mạng nguồn free, mạng không có thì gen bằng magnific".
Nguồn (CC0) và tiếng gen ở ArtGen/Sfx/tran/NGUON.md. Chọn bằng số đo (do_tieng.py, đường bao từng 0,1 s) vì không nghe được.
Khoá dùng trong game: AudioImportMenu.Sfx, SkillSfx.cs.
    py -3 ArtGen/Sfx/xuat_tieng_chieu.py
"""
import os

import numpy as np
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(HERE, "tran")
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "Assets", "03 Art", "Audio", "Sfx"))
SR = 44100

KS = "kenney_sci-fi-sounds/Audio/"
KI = "../kenney/impact-sounds/Audio/"   # Kenney Impact Sounds tải đợt UI 11-22 (ArtGen/Sfx/kenney)
G = "gen_1128/"

# khoá: ([(tệp so với ArtGen/Sfx/tran, độ to lớp dB, lệch s, cắt từ s, cắt tới s)], RMS đích dB, dài tối đa s, mờ vào s, mờ ra s)
CHON = {
    # sét: tiếng nổ chát của bản thu mưa giông (giây 22,44) + ì ầm trầm
    "fx_set": ([("oga_set/rain-thunder.ogg", 0, 0, 22.42, 24.6), ("oga_sfx100b/sfx100v2_thunder_01.ogg", -5, 0.05, 0, 0)], -13, 2.0, 0, 0.8),
    # mưa trút (đoạn của vòng mưa)
    "fx_mua": ([("oga_nuoc/loop_rain.ogg", 0, 0, 0, 2.2)], -19, 1.8, 0.3, 0.6),
    # động đất / sóng đất / gò chạy ngầm: rung đất + thịch trầm đầu
    "fx_dong_dat": ([("oga_dongdat/shake.flac", 0, 0, 1.0, 3.2), (KS + "lowFrequency_explosion_000.ogg", -4, 0, 0, 0)], -15, 1.8, 0.04, 0.7),
    # đá vỡ / gai đá trồi / dăm đá: thịch trầm + đá nứt + đá lăn
    "fx_da_vo": ([("oga_vo_roi/bfh1_hit_02.ogg", 0, 0, 0, 0), ("oga_vo_roi/bfh1_rock_breaking_02.ogg", -1, 0.01, 0, 0),
                  ("oga_vo_roi/bfh1_rock_falling_01.ogg", -4, 0.06, 0, 0)], -15, 0.8, 0, 0.2),
    # tảng đá lớn nện / cột giáng: nổ trầm + nổ giòn + đá vỡ + đá lăn
    "fx_da_lon": ([(KS + "lowFrequency_explosion_000.ogg", 0, 0, 0, 0), (KS + "explosionCrunch_000.ogg", -3, 0, 0, 0),
                   ("oga_vo_roi/bfh1_rock_breaking_02.ogg", -3, 0.03, 0, 0), ("oga_vo_roi/bfh1_rock_falling_01.ogg", -5, 0.1, 0, 0)],
                  -13, 1.1, 0, 0.35),
    # thiên thạch rơi: tiếng rít đi xuống 1,0 s (gen bản 2, phần trước cú nện) — phát 1,0 s trước lúc trúng
    "fx_thien_thach_roi": ([(G + "thien_thach_2.mp3", 0, 0, 0, 1.0)], -17, 1.0, 0.25, 0.08),
    # thiên thạch nện (gen bản 1, từ cú nện giây 0,98) + ầm trầm
    "fx_thien_thach": ([(G + "thien_thach_1.mp3", 0, 0, 0.97, 2.5), (KS + "lowFrequency_explosion_000.ogg", -4, 0, 0, 0)], -12, 1.4, 0, 0.45),
    # tia Mặt Trời giáng xuống (gen bản 2: tia rít 0,85 s rồi nện) — phát 0,85 s trước lúc trúng
    "fx_tia_troi": ([(G + "tia_troi_2.mp3", 0, 0, 0, 1.45)], -12, 1.45, 0.05, 0.3),
    # nổ nấm / nổ cực lớn: nổ rất trầm + nổ giòn
    "fx_no_nam": ([("oga_dien/deathboom.wav", 0, 0, 0.42, 3.0), (KS + "explosionCrunch_001.ogg", -2, 0, 0, 0)], -11, 2.0, 0, 0.7),
    # cưa máy rú rồi ghì vào kim loại (gen)
    "fx_cua": ([(G + "cua_2.mp3", 0, 0, 0, 0)], -15, 1.3, 0.03, 0.35),
    # giật dây máy nổ ba lần rồi nổ máy (gen)
    "fx_may_no": ([(G + "may_no_1.mp3", 0, 0, 0, 0)], -15, 2.7, 0, 0.3),
    # tên lửa phóng (luồng lửa đẩy, Kenney)
    "fx_ten_lua": ([(KS + "thrusterFire_001.ogg", 0, 0, 0, 1.1)], -17, 1.0, 0.05, 0.45),
    # pháo nổ đầu nòng: nổ giòn ngắn + thịch trầm
    "fx_phao": ([(KS + "explosionCrunch_000.ogg", 0, 0, 0, 0), (KS + "lowFrequency_explosion_001.ogg", -2, 0, 0, 0)], -14, 0.6, 0, 0.25),
    # xích loảng xoảng
    "fx_xich": ([("oga_rpg/chain_01.ogg", 0, 0, 0, 0), ("oga_rpg/chain_03.ogg", -3, 0.12, 0, 0)], -16, 0.7, 0, 0.15),
    # hồn lướt (gen)
    "fx_hon": ([(G + "hon_2.mp3", 0, 0, 0, 0)], -16, 0.8, 0.03, 0.25),
    # đớp / ngoạm: tiếng cắn + thịch
    "fx_dop": ([("oga_quai/eat_02.ogg", 0, 0, 0, 0), ("oga_quat/PCM/thwack-03.wav", -4, 0, 0, 0)], -15, 0.35, 0, 0.08),
    # pha lê / tinh thể vỡ
    "fx_pha_le": ([(KI + "impactGlass_heavy_000.ogg", 0, 0, 0, 0), ("oga_vo_roi/bfh1_glass_breaking_06.ogg", -3, 0.02, 0, 0)], -16, 0.75, 0, 0.2),
    # lá bay xào xạc
    "fx_la": ([("oga_la/rustle/rustle02.flac", 0, 0, 0, 0), ("oga_sfx100b/sfx100v2_air_02.ogg", -6, 0, 0, 0)], -18, 0.9, 0.03, 0.3),
    # roi / dây gai quất (gen) + tiếng chát giòn
    "fx_roi": ([(G + "roi_2.mp3", 0, 0, 0, 0), ("oga_quat/PCM/thwack-01.wav", -3, 0.02, 0, 0)], -14, 0.4, 0, 0.1),
    # giật điện: chạm điện + tia lách tách
    "fx_dien": ([("oga_dien/hit.wav", 0, 0, 0, 0), ("oga_dien/snaploop.wav", -4, 0.02, 0, 0.9)], -16, 0.9, 0, 0.3),
    # dung nham trào (gen)
    "fx_nham": ([(G + "nham_1.mp3", 0, 0, 0, 0)], -14, 1.05, 0, 0.3),
    # sóng xung kích / sóng âm (gen)
    "fx_song_am": ([(G + "song_am_1.mp3", 0, 0, 0, 0)], -13, 1.4, 0, 0.45),
    # gió xé / quạt cánh (gen 11-24 bản 2, ngắn hơn fx_loc)
    "fx_gio": ([("gen_1124/gio_loc_2.mp3", 0, 0, 0, 0)], -16, 1.1, 0.06, 0.45),
    # tan biến / dịch chuyển
    "fx_bien_mat": ([("oga_dien/teleport_1.wav", 0, 0, 0, 0), ("oga_sfx100b/sfx100v2_air_03.ogg", -4, 0, 0, 0)], -17, 0.6, 0, 0.2),
    # gầm thú (hổ, sói, thú đá)
    "fx_gam_thu": ([("oga_rpg/creature_roar_01.ogg", 0, 0, 0, 0), ("oga_quai/roar_02.ogg", -3, 0.02, 0, 0)], -14, 0.7, 0, 0.2),
    # hét xung trận (gầm gừ ngắn)
    "fx_het": ([("oga_quai/troll_02.ogg", 0, 0, 0, 0), ("oga_quai/monster_03.ogg", -3, 0.03, 0, 0)], -15, 0.5, 0, 0.12),
    # bùn bẹp
    "fx_bun": ([("oga_nuoc/slime_04.ogg", 0, 0, 0, 0), ("oga_nuoc/slime_03.ogg", -3, 0.05, 0, 0), ("oga_vo_roi/bfh1_hit_06.ogg", -6, 0, 0, 0)],
               -16, 0.5, 0, 0.12),
    # nuốt ực
    "fx_nuot": ([("oga_quai/burp_01.ogg", 0, 0, 0, 0)], -16, 0.45, 0, 0.1),
    # búa sắt nện: kim loại nặng + thịch trầm
    "fx_bua": ([(KI + "impactMetal_heavy_000.ogg", 0, 0, 0, 0), (KS + "lowFrequency_explosion_001.ogg", -6, 0, 0, 0)], -14, 0.6, 0, 0.18),
}


def path(rel):
    return os.path.normpath(os.path.join(T, rel))


def load(rel, a, b):
    x, sr = sf.read(path(rel), always_2d=True)
    x = x.mean(1)
    if b > a:
        x = x[int(a * sr): int(b * sr)]
    if sr != SR:
        idx = np.arange(0, len(x) - 1, sr / SR)
        x = np.interp(idx, np.arange(len(x)), x)
    return x


def trim(x, head=True):
    a = np.abs(x)
    on = np.where(a > a.max() * 0.02)[0]
    if not len(on):
        return x
    return x[(max(0, on[0] - 64) if head else 0): on[-1] + 1]


os.makedirs(OUT, exist_ok=True)
for key, (layers, rms_db, dmax, fin, fout) in CHON.items():
    mix = np.zeros(int(SR * (dmax + 0.5)))
    for rel, gain_db, off, a, b in layers:
        x = trim(load(rel, a, b), head=(b <= a))   # đoạn cắt chủ ý (b > a) giữ nguyên đầu đoạn
        x = x / (np.sqrt(np.mean(x ** 2)) + 1e-9) * 10 ** (gain_db / 20)
        o = int(off * SR)
        n = min(len(x), len(mix) - o)
        mix[o:o + n] += x[:n]
    mix = trim(mix)[: int(SR * dmax)]
    if fin > 0:
        k = min(len(mix), int(fin * SR))
        mix[:k] *= np.linspace(0.15, 1, k) ** 1.5
    k = min(len(mix), int(fout * SR))
    if k > 0:
        mix[-k:] *= np.linspace(1, 0, k)
    mix = mix / (np.sqrt(np.mean(mix ** 2)) + 1e-9) * 10 ** (rms_db / 20)
    pk = np.abs(mix).max()
    if pk > 0.89:
        target = 10 ** ((rms_db - 1) / 20)
        base = mix / pk
        for drive in (1, 1.5, 2, 3, 4, 6, 8):
            y = np.tanh(drive * base) / np.tanh(drive) * 0.89
            if np.sqrt(np.mean(y ** 2)) >= target:
                break
        mix = y
    dst = os.path.join(OUT, f"tran_{key}.ogg")
    sf.write(dst, mix.astype(np.float32), SR, format="OGG", subtype="VORBIS")
    print(f"{key:20s} {len(mix) / SR:4.2f}s rms {20 * np.log10(np.sqrt(np.mean(mix ** 2)) + 1e-9):6.1f} dB  -> tran_{key}.ogg")
