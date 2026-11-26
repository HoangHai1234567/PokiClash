# Mở AtomSpine Studio cho rig máy quả (xem, sửa, ghi nhận xét ở Comment mode). Chạy: py -3 -I mo_studio.py
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from atom_cli import CLI
subprocess.run(CLI + ["studio", os.path.abspath(os.path.join(HERE, "..", "atom"))])
