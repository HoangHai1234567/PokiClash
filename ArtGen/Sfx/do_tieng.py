# -*- coding: utf-8 -*-
"""Đo đặc trưng các tiếng ứng viên (ArtGen/Sfx/tran/nghe/am) để chọn khi không nghe được: độ dài có tiếng, độ trễ đầu, độ to (RMS dB),
độ trầm (tâm phổ Hz, tỉ lệ năng lượng < 250 Hz), thời điểm đỉnh, hướng cao độ (tâm phổ nửa sau / nửa đầu: > 1 là cao dần — tụ năng
lượng), đuôi (thời gian từ đỉnh tới khi tắt). In bảng CSV ra stdout.
    py -3 ArtGen/Sfx/do_tieng.py [thư_mục]
"""
import glob
import os
import sys

import numpy as np
import soundfile as sf

D = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "tran", "nghe", "am")


def feats(f):
    x, sr = sf.read(f, always_2d=True)
    x = x.mean(1)
    if len(x) < 64:
        return None
    a = np.abs(x)
    thr = max(1e-4, a.max() * 0.03)
    on = np.where(a > thr)[0]
    t0, t1 = on[0] / sr, on[-1] / sr
    hop = 512
    fr = [x[i:i + 2048] for i in range(0, max(1, len(x) - 2048), hop)]
    rms = np.array([np.sqrt(np.mean(c ** 2)) + 1e-9 for c in fr])
    cent, low = [], []
    freqs = np.fft.rfftfreq(2048, 1 / sr)
    for c in fr:
        s = np.abs(np.fft.rfft(c * np.hanning(len(c)), 2048))
        e = s.sum() + 1e-9
        cent.append((s * freqs).sum() / e)
        low.append(s[freqs < 250].sum() / e)
    cent, low = np.array(cent), np.array(low)
    loud = rms > rms.max() * 0.1
    pk = int(np.argmax(rms))
    half = len(cent) // 2
    c1 = cent[:half][loud[:half]].mean() if loud[:half].any() else 0
    c2 = cent[half:][loud[half:]].mean() if loud[half:].any() else 0
    tail = (np.where(loud)[0][-1] - pk) * hop / sr if loud.any() else 0
    return dict(dur=t1 - t0, delay=t0, db=20 * np.log10(np.sqrt(np.mean(x[on[0]:on[-1] + 1] ** 2)) + 1e-9),
                cent=cent[loud].mean() if loud.any() else 0, low=low[loud].mean() if loud.any() else 0,
                peak=pk * hop / sr, rise=(c2 / c1) if c1 else 0, tail=tail)


print("id,dur,delay,db,cent,low,peak,rise,tail")
for f in sorted(glob.glob(os.path.join(D, "*.*"))):
    try:
        r = feats(f)
    except Exception as e:
        print(os.path.basename(f), "ERR", e)
        continue
    if r:
        print(os.path.splitext(os.path.basename(f))[0] + "," + ",".join(f"{r[k]:.2f}" if k not in ("cent",) else f"{r[k]:.0f}"
                                                                       for k in ("dur", "delay", "db", "cent", "low", "peak", "rise", "tail")))
