# -*- coding: utf-8 -*-
"""Gen một file prompt của ArtGen/Spine qua Codex, giữ chung khoá với các lô tướng (chỉ một lệnh Codex mỗi lúc).

    py -3 -I ArtGen/Spine/gen.py <file prompt> [--note "..."] [--timeout 1800]
"""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
HEROES = os.path.normpath(os.path.join(HERE, "..", "Heroes"))
GEN = os.path.join(HEROES, "tools", "gen_codex.py")


def main(argv):
    import msvcrt
    fh = open(os.path.join(HEROES, "inbox", ".codex.lock"), "a+")
    while True:
        try:
            fh.seek(0)
            msvcrt.locking(fh.fileno(), msvcrt.LK_NBLCK, 1)
            break
        except OSError:
            print("đợi khoá Codex...", flush=True)
            time.sleep(10)
    try:
        return subprocess.run([sys.executable, "-I", GEN] + argv).returncode
    finally:
        fh.seek(0)
        msvcrt.locking(fh.fileno(), msvcrt.LK_UNLCK, 1)
        fh.close()


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main(sys.argv[1:]))
