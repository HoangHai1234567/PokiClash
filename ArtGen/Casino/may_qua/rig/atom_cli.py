# Tìm lệnh AtomSpine (atom.mjs, tsx) và node trên máy đang chạy; không ghi cứng ổ đĩa (hai máy khác ổ).
# Thứ tự: biến môi trường ATOMSPINE_DIR, thư mục AtomSpine cạnh project (…/PokiWar/../AtomSpine), D:/AtomSpine.
# node: biến NODE, node trong PATH, Node bản portable ở %LOCALAPPDATA%/Programs/nodejs.
import os, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))


def _atomspine_dir():
    cands = [os.environ.get("ATOMSPINE_DIR", ""), os.path.join(os.path.dirname(PROJECT), "AtomSpine"), "D:/AtomSpine"]
    for c in cands:
        if c and os.path.isfile(os.path.join(c, "packages", "cli", "dist", "atom.mjs")):
            return os.path.abspath(c)
    raise SystemExit("Không thấy AtomSpine đã build (packages/cli/dist/atom.mjs). Đặt ATOMSPINE_DIR hoặc build AtomSpine cạnh project.")


def _node():
    n = os.environ.get("NODE") or shutil.which("node")
    if n:
        return n
    p = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "nodejs", "node.exe")
    if os.path.isfile(p):
        return p
    raise SystemExit("Không thấy node. Cài Node 20+ hoặc đặt biến NODE.")


ATOMSPINE = _atomspine_dir()
NODE = _node()
CLI = [NODE, os.path.join(ATOMSPINE, "packages", "cli", "dist", "atom.mjs")]
TSX = [NODE, os.path.join(ATOMSPINE, "node_modules", "tsx", "dist", "cli.mjs")]
