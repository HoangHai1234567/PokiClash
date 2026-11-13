# -*- coding: utf-8 -*-
"""Chạy nối nhau các tờ mảnh lượt 2 của moc_vuong qua Codex (gen.py giữ khoá: một lệnh Codex mỗi lúc), tờ nào về thì cắt ngay.

    py -3 -I ArtGen/Spine/moc_vuong_gen.py [Q3 Q7 ...] [--lai]      mặc định: mọi tờ chưa có ảnh; --lai: gen lại cả tờ đã có
Nhật ký: inbox/moc_vuong_1/gen_part.log
"""
import json
import os
import subprocess
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "inbox", "moc_vuong_1")
LOG = os.path.join(BASE, "gen_part.log")


def log(s):
    open(LOG, "a", encoding="utf-8").write(time.strftime("%H:%M:%S ") + s + "\n")
    print(s, flush=True)


def main(a):
    lai = "--lai" in a
    chon = [x for x in a if not x.startswith("--")]
    muc = json.load(open(os.path.join(BASE, "mau", "part_Q.json"), encoding="utf-8"))
    for to in (chon or list(muc)):
        co = [f for f in os.listdir(os.path.join(BASE, "tai_ve")) if f.startswith(f"N_{to}.") or f.startswith(f"N_{to}_")]
        if co and not lai:
            log(f"{to}: đã có {co[-1]}, bỏ qua")
            continue
        p = os.path.join(HERE, "gui_gpt", "moc_vuong_1", f"luot_2_part_{to}.txt")
        t0 = time.time()
        r = subprocess.run([sys.executable, "-I", os.path.join(HERE, "gen.py"), p], stdin=subprocess.DEVNULL, capture_output=True, text=True, encoding="utf-8", errors="replace")
        duoi = (r.stdout or "")[-300:].replace("\n", " | ")
        log(f"{to}: gen {time.time() - t0:.0f} s, mã {r.returncode}: {duoi}")
        if "usage limit" in (r.stdout or "").lower():
            log("HẾT HẠN MỨC Codex: dừng")
            return 2
        c = subprocess.run([sys.executable, "-I", os.path.join(HERE, "moc_vuong.py"), "cat_part", to], capture_output=True, text=True, encoding="utf-8", errors="replace")
        log("  " + (c.stdout or c.stderr or "")[-400:].strip().replace("\n", " | "))
    log("XONG")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
