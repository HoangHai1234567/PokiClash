# -*- coding: utf-8 -*-
"""Tiếng khán giả cho scene Hầm đấu (người dùng 2026-11-26: "cần thì gen thêm tiếng hò reo vào đấu trường ngầm, lấy luôn nhạc khi combat
cho phần này"; App/Scenes/Casino/UndergroundScene.cs). Gen bằng Magnific (ElevenLabs SFX), 110 credit, vào tai_ve/:
- reo_1.mp3, reo_2.mp3 (3 s, 2 bản, 30 credit): "A small rowdy crowd of about thirty people suddenly cheering, whooping and whistling for
  two seconds inside a stone cellar fighting pit, a few fists banging on wooden rails, then quickly dying down. Close, punchy, slightly
  cartoonish, short room echo. No music, no announcer, no words."
- on_1.mp3, on_2.mp3 (8 s, lặp liền, 2 bản, 80 credit): "Continuous background murmur of a small excited crowd in an underground stone
  cellar fighting pit: low overlapping chatter, occasional chuckle and shuffle, even level throughout, no single voice standing out, no
  clear words, no shouting, no cheering peaks. Short room echo. No music."
Máy ổ C chưa có thư viện đọc mp3 (soundfile) nên CHƯA đo độ to, chưa chọn bản bằng số đo: chép nguyên file. Hai bản reo dùng làm hai
biến thể phát xen kẽ (khoá "pitCheer1", "pitCheer2"); tiếng ồn nền lấy bản 1 (khoá "pitCrowd", phát lặp bằng App.Audio.Loop); muốn đổi
sang bản 2 thì sửa ON bên dưới rồi chạy lại. Khoá khai ở Editor/AudioImportMenu.cs, nạp bằng menu "PokiClash/Âm thanh/Nạp nhạc và tiếng".
    py -3 -I ArtGen/Sfx/ham_dau/dua_vao_unity.py
"""
import os, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "..", "Assets", "03 Art", "Audio", "Sfx"))
ON = "on_1.mp3"
for src, dst in (("reo_1.mp3", "ham_reo_1.mp3"), ("reo_2.mp3", "ham_reo_2.mp3"), (ON, "ham_on_loop.mp3")):
    shutil.copyfile(os.path.join(HERE, "tai_ve", src), os.path.join(OUT, dst))
    print("chep", src, "->", os.path.join(OUT, dst))
