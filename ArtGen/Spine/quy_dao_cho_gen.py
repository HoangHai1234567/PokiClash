# -*- coding: utf-8 -*-
"""Chờ Codex có lại hạn mức rồi gen (chạy tách khỏi phiên Claude bằng Start-Process). Codex báo 2026-11-13 16:05: "try again at 6:30 PM".

    py -3 -I ArtGen/Spine/quy_dao_cho_gen.py <HH:MM bắt đầu thử> <file prompt> [<file prompt> ...]

Mỗi file: bỏ qua nếu ảnh ở mục SAVE đã có; gen qua gen.py (chung khoá Codex); hết hạn mức thì chờ 10 phút thử lại (tối đa 18 lần).
Nhật ký: inbox/quy_dao_cho_gen.log."""
import datetime
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, "inbox", "quy_dao_cho_gen.log")


def log(msg):
    with open(LOG, "a", encoding="utf-8") as fh:
        fh.write(time.strftime("%H:%M:%S ") + msg + "\n")


def save_of(prompt):
    m = re.search(r"save it as a PNG to ([A-Za-z]:\\\S+\.png)", open(prompt, encoding="utf-8").read())
    return m.group(1) if m else None


def main(a):
    hh, mm = [int(x) for x in a[0].split(":")]
    dich = datetime.datetime.now().replace(hour=hh, minute=mm, second=0, microsecond=0)
    log(f"chờ tới {a[0]} rồi gen: {', '.join(os.path.basename(p) for p in a[1:])}")
    while datetime.datetime.now() < dich:
        time.sleep(30)
    for p in a[1:]:
        p = os.path.abspath(p)
        s = save_of(p)
        for lan in range(18):
            if s and os.path.isfile(s):
                log(f"đã có: {s}")
                break
            r = subprocess.run([sys.executable, "-I", os.path.join(HERE, "gen.py"), p], capture_output=True, text=True,
                               encoding="utf-8", errors="replace")
            log(f"  lần {lan + 1} (mã {r.returncode}): " + " | ".join((r.stdout or "").strip().splitlines()[-3:]))
            if s and os.path.isfile(s):
                break
            time.sleep(600 if "usage limit" in (r.stdout + r.stderr).lower() else 60)
    log("HẾT")


if __name__ == "__main__":
    main(sys.argv[1:])
