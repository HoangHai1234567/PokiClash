# -*- coding: utf-8 -*-
"""Cắt bộ NƯỚC Blender từ vfx_blender/render/g_<script> thành frames/<tên> (cat_gen.save: hộp gộp, neo, manifest).
    py -3 -I cat_nuoc.py [tên ...]
"""
import glob
import json
import os
import sys

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cat_gen  # noqa: E402

R = os.path.normpath(os.path.join(HERE, "..", "vfx_blender", "render"))
SETS = {  # tên khung: (thư mục render, tiền tố ảnh, lặp)
    "cau_nuoc": ("g_cau_nuoc_bl", "cau_nuoc", True),
    "no_nuoc": ("g_no_nuoc_bl", "no_nuoc", False),
    "thuong_nuoc": ("g_thuong_nuoc_bl", "thuong_nuoc", True),
    "mach_phun": ("g_mach_phun_bl", "mach_phun", False),
    "song_nuoc": ("g_song_nuoc_bl", "song_nuoc", False),
    "song_cuon": ("g_song_cuon_bl", "song_cuon", False),   # sóng cuộn theo mẫu ABitOfGameDev (2026-11-24)
    "nuoc_tia": ("nuoc_tia1", "nuoc_tia", False),          # tia (nuoc_blender.py --phan tia), đuôi tan theo hai ngưỡng
    "nuoc_trung": ("nuoc_trung1", "nuoc_trung", False),    # va chạm ở đích (--phan trung)
    "toe_nuoc": ("g_toe_nuoc_bl", "toe_nuoc", False),      # cụm toé nhiều lớp (toe_nuoc_bl.py --phan toe), neo điểm trúng
    "vung_nuoc": ("g_vung_nuoc_bl", "vung_nuoc", False),   # vũng đọng trên đất (--phan vung), neo tâm vũng
    "cau_vo": ("g_cau_vo_bl", "cau_vo", False),            # cầu nước vỡ lấm tấm + cụm toé (--phan cau)
    # theo repo abitofgamedev/water_vfx, chất nước xanh của mình (vfx_blender/nuoc_repo_bl.py)
    # bộ v2 ("dựa theo shader của họ rồi tự build ... tất cả theo ý mình"): chất nước chung lam nhạt + bọt, khối cel, metaball
    "cau_nem": ("g_v2_cau", "cau_nem", True),
    "toe_dat": ("g_v2_toe", "toe_dat", False),
    "tia_ong": ("g_v2_ong", "tia_ong", False),
    "roi_nuoc": ("g_v2_roi", "roi_nuoc", False),
    "tia_nuoc2": ("g_v2_tia", "tia_nuoc2", False),
    "thuong_nuoc2": ("g_v2_thuong", "thuong_nuoc2", True),
    "mach_phun2": ("g_v2_phun", "mach_phun2", False),
    "toe_nuoc2": ("g_v2_than", "toe_nuoc2", False),
    "cau_vo2": ("g_v2_vo", "cau_vo2", False),
    "loc_nuoc": ("g_loc_nuoc", "loc_nuoc", False),
}
names = sys.argv[1:] or list(SETS)
for n in names:
    d, pre, loop = SETS[n]
    src = os.path.join(R, d)
    info = json.load(open(os.path.join(src, "info.json"), encoding="utf-8"))
    fr = [cv2.imread(f, cv2.IMREAD_UNCHANGED) for f in sorted(glob.glob(os.path.join(src, pre + "_*.png")))]
    al = np.max(np.stack([f[..., 3] for f in fr]), 0)
    edge = [(al[:, 0] > 8).any(), (al[:, -1] > 8).any(), (al[0] > 8).any(), (al[-1] > 8).any()]
    if any(edge):
        print(n, "CHAM MEP trai/phai/tren/duoi:", edge)
    cat_gen.save(n, fr, info["anchor"], loop=loop)
