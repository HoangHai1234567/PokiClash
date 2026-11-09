# -*- coding: utf-8 -*-
"""Gen lần lượt nhiều file prompt của ArtGen/Spine qua gen.py (chung khoá Codex), bỏ qua file đã có ảnh ở chỗ lưu. Chạy tách
khỏi phiên Claude (Start-Process) để phiên có ngắt thì gen vẫn chạy tiếp. Ghi nhật ký inbox/chay_hoa.log.

    py -3 -I ArtGen/Spine/chay_hoa.py <file prompt> ...
"""
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, "inbox", "chay_hoa.log")


def log(msg):
    with open(LOG, "a", encoding="utf-8") as fh:
        fh.write(time.strftime("%H:%M:%S ") + msg + "\n")


def save_of(prompt):
    m = re.search(r"save it as a PNG to ([A-Za-z]:\\\S+\.png)", open(prompt, encoding="utf-8").read())
    return m.group(1) if m else None


def main(prompts):
    for p in prompts:
        p = os.path.abspath(p)
        s = save_of(p)
        if s and os.path.isfile(s):
            log(f"đã có, bỏ qua: {s}")
            continue
        log(f"gen: {p}")
        for attempt in range(3):
            r = subprocess.run([sys.executable, "-I", os.path.join(HERE, "gen.py"), p], capture_output=True, text=True,
                               encoding="utf-8", errors="replace")
            tail = " | ".join((r.stdout or "").strip().splitlines()[-3:])
            log(f"  xong (mã {r.returncode}): {tail}")
            if s and os.path.isfile(s):
                break
            if "usage limit" in (r.stdout + r.stderr).lower():
                log("  hết hạn mức Codex, chờ 10 phút")
                time.sleep(600)
    log("HẾT DANH SÁCH")


if __name__ == "__main__":
    main(sys.argv[1:])
