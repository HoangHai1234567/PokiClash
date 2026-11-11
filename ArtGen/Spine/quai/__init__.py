# -*- coding: utf-8 -*-
"""Thư viện rig dựng bằng mã cho lô quái đảo Thủy (2026-11-11). Xem README.md cùng thư mục.

Dùng từ script trong ArtGen/Spine (chạy `py -3 -I` không tự thêm thư mục script vào sys.path):

    import os, sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from quai import anh, luoi, trongso, khung, hoat, mieng, tienhoa, xuat, soi
"""
import os
import sys

SPINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # ArtGen/Spine (atomik.py, mo_xe/, lib/)
if SPINE not in sys.path:
    sys.path.insert(0, SPINE)
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
