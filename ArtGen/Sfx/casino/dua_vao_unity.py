# -*- coding: utf-8 -*-
"""Tiếng riêng cho đảo Casino (người dùng chọn làm âm thanh D8 / B5 ngày 2026-11-27; GD_Claude/29, 31, 32). Gen bằng Magnific (ElevenLabs
SFX), 5 credit mỗi giây mỗi bản, tổng 175 credit, 25 bản trong tai_ve/ (đo bằng soundfile: dài, đỉnh, RMS):
- rl_tick_1..3 (1 s): "Single small ivory roulette ball clicking once against a thin metal fret on a spinning wooden roulette wheel..."
- rl_roi_1..2 (2 s): "Roulette ball dropping into a wooden pocket: two quick bounces between metal dividers, then settling..."
- sl_tick_1..2 (1 s): "One single mechanical ratchet click of an old slot machine reel turning..." (không dùng: đuôi dài 0,8 s, phát dồn sẽ chồng)
- sl_dung_1..3 (1 s): "Heavy mechanical slot machine reel stopping hard: one solid metal clunk with a brief spring rattle..."
- sl_can_1..2 (2 s): "Pulling the big metal lever of an old slot machine: ratchet clicks as it goes down, then a springy release thunk..."
- dua_huc_1..3 (1 s): "Cartoon bonk: two small creatures bump heads while running, a hollow wooden bonk followed by a brief comic dizzy twinkle..."
- dua_vot_1..2 (1 s): "Cartoon sudden speed burst: a quick rising whoosh with a little zip..."
- cau_guong_1..2 (2 s): "Fishing reel being cranked fast by hand: rapid ratchet clicking with a light line whir..."
- muc_noi_1..4 (1 s): "A sly old cartoon squid gentleman mumbling playful gibberish in a low raspy voice, a short sneaky chuckle at the end..."
- muc_boing_1..2 (1 s): "Comedic cartoon jaw-drop boing: a springy rubber boing like 1930s animation when a character is shocked..."
Chọn theo số đo (chưa nghe): bản to, gọn, ít đuôi. Muốn đổi bản thì sửa CHON rồi chạy lại, xong chạy menu
"PokiClash/Âm thanh/Nạp nhạc và tiếng" trong Unity (khoá khai ở Editor/AudioImportMenu.cs). Trang nghe thử: nghe_thu.html.
    py -3 -I ArtGen/Sfx/casino/dua_vao_unity.py
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "..", "Assets", "03 Art", "Audio", "Sfx"))
CHON = {
    "casino_rl_tick.mp3": "rl_tick_2.mp3",
    "casino_rl_roi.mp3": "rl_roi_2.mp3",
    "casino_sl_can.mp3": "sl_can_1.mp3",
    "casino_sl_dung_1.mp3": "sl_dung_1.mp3",
    "casino_sl_dung_2.mp3": "sl_dung_2.mp3",
    "casino_sl_dung_3.mp3": "sl_dung_3.mp3",
    "casino_dua_huc_1.mp3": "dua_huc_1.mp3",
    "casino_dua_huc_2.mp3": "dua_huc_3.mp3",
    "casino_dua_vot.mp3": "dua_vot_2.mp3",
    "casino_cau_guong.mp3": "cau_guong_2.mp3",
    "casino_muc_noi_1.mp3": "muc_noi_2.mp3",
    "casino_muc_noi_2.mp3": "muc_noi_3.mp3",
    "casino_muc_noi_3.mp3": "muc_noi_4.mp3",
    "casino_muc_boing.mp3": "muc_boing_1.mp3",
}
for dst, src in CHON.items():
    shutil.copyfile(os.path.join(HERE, "tai_ve", src), os.path.join(OUT, dst))
    print("chep", src, "->", dst)
