# -*- coding: utf-8 -*-
"""Tiếng bút chì cho màn mở khoá tướng (người dùng 2026-11-24: "gen thêm tiếng bút chì"; màn bút chì vẽ tướng lên trang sổ,
App/Shop/HeroUnlockView.cs). Gen bằng Magnific (ElevenLabs SFX, 4 s, lặp liền, 2 bản; lời: "fast pencil sketching on paper,
graphite pencil scribbling and hatching quickly on a notebook page, close mic, dry, no music") vào tai_ve/. Chọn bản 2 theo số đo
(độ to đều hơn: RMS từng 0,1 s quanh −30 dB, một chỗ lặng 0,1 s như nhấc bút; bản 1 có quãng nhỏ hẳn 0,5 s).
Xuất: mono, nâng tới đỉnh −1 dBFS, ogg → Assets/03 Art/Audio/Sfx/ui_but_chi.ogg (khoá "pencil" ở AudioImportMenu.Sfx, phát lặp bằng
App.Audio.Loop trong lúc vẽ).
    py -3 -I ArtGen/Sfx/but_chi/xuat.py
"""
import os

import numpy as np
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "tai_ve", "but_chi_2.mp3")
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "..", "Assets", "03 Art", "Audio", "Sfx", "ui_but_chi.ogg"))

x, sr = sf.read(SRC, always_2d=True)
m = x.mean(1)
gain = 10 ** (-1 / 20) / max(1e-6, np.abs(m).max())
m = (m * gain).astype(np.float32)
sf.write(OUT, m, sr, format="OGG", subtype="VORBIS")
rms = 20 * np.log10(np.sqrt(np.mean(m ** 2)))
print("ghi", OUT, "dài %.2f s, nâng %.1f dB, RMS %.1f dB" % (len(m) / sr, 20 * np.log10(gain), rms))
