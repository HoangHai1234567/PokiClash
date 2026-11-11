# -*- coding: utf-8 -*-
"""Khoá chạy chung cho lô quái đảo Thủy (2026-11-11): giới hạn số việc nặng chạy cùng lúc trên cả máy.

Máy này từng sập cứng 5 lần khi Chrome ngầm vẽ (tải AVX), nên:
  chrome : 1 suất  (mo_xe/chay.py, trang xem Spine chạy ngầm, mọi thứ mở Chrome/Edge headless)
  nang   : 2 suất  (nướng animation, dựng lưới, xuất atlas: việc Python chạy lâu, nhiều numpy)

    py -3 -I ArtGen/Spine/quai/khoa.py chrome -- py -3 -I ArtGen/Spine/mo_xe/chay.py info <thư mục> <tên> <ra.json>
    py -3 -I ArtGen/Spine/quai/khoa.py nang   -- py -3 -I ArtGen/Spine/tm01.py rig 1

Chờ tới khi có suất (in "đợi khoá ..." mỗi 15 s), hạ ưu tiên tiến trình xuống BelowNormal (con cháu thừa hưởng) rồi chạy lệnh,
trả mã thoát của lệnh. Gen ảnh Codex KHÔNG đi qua đây: gen.py đã có khoá riêng (một lệnh Codex mỗi lúc).
"""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.join(HERE, ".khoa")
SLOTS = {"chrome": 1, "nang": 2}


def below_normal():
    try:
        import ctypes
        k = ctypes.windll.kernel32
        k.SetPriorityClass(k.GetCurrentProcess(), 0x4000)  # BELOW_NORMAL_PRIORITY_CLASS
    except Exception:
        pass


def acquire(kind):
    import msvcrt
    os.makedirs(DIR, exist_ok=True)
    n = SLOTS[kind]
    waited = 0
    while True:
        for i in range(n):
            fh = open(os.path.join(DIR, f"{kind}_{i}.lock"), "a+")
            try:
                fh.seek(0)
                msvcrt.locking(fh.fileno(), msvcrt.LK_NBLCK, 1)
                return fh
            except OSError:
                fh.close()
        if waited % 15 == 0:
            print(f"đợi khoá {kind} ({waited} s)...", flush=True)
        time.sleep(5)
        waited += 5


def main(argv):
    if len(argv) < 3 or argv[0] not in SLOTS or argv[1] != "--":
        print(__doc__)
        return 2
    sys.stdout.reconfigure(encoding="utf-8")
    fh = acquire(argv[0])
    below_normal()
    try:
        return subprocess.call(argv[2:])
    finally:
        try:
            import msvcrt
            fh.seek(0)
            msvcrt.locking(fh.fileno(), msvcrt.LK_UNLCK, 1)
        except OSError:
            pass
        fh.close()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
