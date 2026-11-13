# -*- coding: utf-8 -*-
"""Chờ Codex có hạn mức lại (báo mở 18:30 ngày 2026-11-13) rồi gen hai concept chibi dạng 1 của Hỏa Quy qua chay_hoa.py (tự thử lại khi còn
báo hết hạn mức). Chạy tách khỏi phiên Claude:  Start-Process py -ArgumentList '-3 -I ArtGen/Spine/inbox/rua_lua_non/cho_gen.py'
Nhật ký: ArtGen/Spine/inbox/rua_lua_non/cho_gen.log và ArtGen/Spine/inbox/chay_hoa.log."""
import datetime
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SPINE = os.path.normpath(os.path.join(HERE, "..", ".."))
LOG = os.path.join(HERE, "cho_gen.log")
PROMPTS = [os.path.join(SPINE, "gui_gpt", "rua_lua_non", f"luot_1_concept_{k}.txt") for k in ("theo_e", "tron_hon")]
OUT = [os.path.join(HERE, "tai_ve", f"L1_{k}.png") for k in ("theo_e", "tron_hon")]


def log(s):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(time.strftime("%H:%M:%S ") + s + "\n")


dich = datetime.datetime.now().replace(hour=18, minute=32, second=0, microsecond=0)
cho = (dich - datetime.datetime.now()).total_seconds()
log(f"chờ {int(max(0, cho))} s tới 18:32")
if cho > 0:
    time.sleep(cho)
for lan in range(6):                      # mỗi lượt chay_hoa tự thử 3 lần cách 10 phút; lặp tới khi đủ hai ảnh
    con = [p for p, o in zip(PROMPTS, OUT) if not os.path.exists(o)]
    if not con:
        break
    log(f"lượt {lan + 1}: gen {len(con)} file")
    subprocess.run([sys.executable, "-I", os.path.join(SPINE, "chay_hoa.py")] + con)
log("xong: " + ", ".join(os.path.basename(o) + (" có" if os.path.exists(o) else " CHƯA") for o in OUT))
