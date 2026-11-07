"""Chạy lô đảo Mộc theo pha (2026-11-07). Ghi tiến độ vào ArtGen/Heroes/inbox/chay_moc.log.

    py -3 -I ArtGen/Heroes/tools/chay_moc.py concept <mã> ...   gen concept dạng nào chưa có (dạng sau cần concept_duyet dạng 1)
    py -3 -I ArtGen/Heroes/tools/chay_moc.py nhom <mã> ...      gen các nhóm mảnh còn thiếu (cần concept_duyet.png)
    py -3 -I ArtGen/Heroes/tools/chay_moc.py ghep <mã> ...      ghép, animation (anim_moc.py + anim_moi.py), trang so sánh
    py -3 -I ArtGen/Heroes/tools/chay_moc.py fx <gói>           gen các bước còn thiếu của một gói hiệu ứng (build_fx.py)
    py -3 -I ArtGen/Heroes/tools/chay_moc.py tron <mã> ...      nhom rồi ghep từng dạng

Codex chạy từng lệnh một (gen_codex.py). Hết hạn mức gói ChatGPT ("usage limit") thì chờ 10 phút rồi thử lại, tối đa 6 giờ.
Duyệt concept là việc của Claude/người dùng (chép concept_duyet.png), script không tự duyệt.
"""
import json
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
HEROES = os.path.normpath(os.path.join(HERE, ".."))
AOLA = next(p for p in ("E:/ProjectAtomik/aola", "D:/Aola-20261029T161238Z-1-001/Aola/AolaRipper/AolaRipper")
            if os.path.isdir(p))
PY = sys.executable
LOG = os.path.join(HEROES, "inbox", "chay_moc.log")
SHOTS = os.path.join(HEROES, "inbox", "moc_so_sanh")
sys.stdout.reconfigure(encoding="utf-8")


def log(msg):
    line = time.strftime("%m-%d %H:%M:%S ") + msg
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def run(args, timeout=3000):
    try:
        p = subprocess.run([PY, "-I"] + args, capture_output=True, text=True, encoding="utf-8", errors="replace",
                           timeout=timeout)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except subprocess.TimeoutExpired:
        return "timeout", ""


def form(code):
    return json.load(open(os.path.join(HEROES, "forms_moc", code + ".json"), encoding="utf-8"))


def have(code, step):
    d = os.path.join(HEROES, "inbox", code, "tai_ve")
    return os.path.isdir(d) and any(re.match(re.escape(step) + r"(_\d+)?\.png$", x, re.I) for x in os.listdir(d))


class CodexLock:
    """khoá file: nhiều lô chay_moc chạy cùng lúc thì Codex vẫn chỉ chạy một lệnh mỗi lúc"""

    def __enter__(self):
        import msvcrt
        self.fh = open(os.path.join(HEROES, "inbox", ".codex.lock"), "a+")
        while True:
            try:
                self.fh.seek(0)
                msvcrt.locking(self.fh.fileno(), msvcrt.LK_NBLCK, 1)
                return self
            except OSError:
                time.sleep(5)

    def __exit__(self, *a):
        import msvcrt
        self.fh.seek(0)
        msvcrt.locking(self.fh.fileno(), msvcrt.LK_UNLCK, 1)
        self.fh.close()


def codex(prompt, steps=None, note=None, timeout=2400):
    with CodexLock():
        return _codex(prompt, steps, note, timeout)


def _codex(prompt, steps=None, note=None, timeout=2400):
    """một lệnh gen_codex; hết hạn mức thì chờ rồi thử lại. Trả về dòng cuối kết quả."""
    waited = 0
    while True:
        args = [os.path.join(HERE, "gen_codex.py"), prompt, "--timeout", str(timeout)]
        if steps:
            args += ["--steps", ",".join(steps)]
        if note:
            args += ["--note", note]
        rc, out = run(args, timeout=timeout + 300)
        if "usage limit" in out.lower() or "rate limit" in out.lower():
            if waited >= 6 * 3600:
                log("hết hạn mức Codex quá 6 giờ, dừng")
                raise SystemExit(2)
            log("hết hạn mức Codex, chờ 10 phút")
            time.sleep(600)
            waited += 600
            continue
        lines = [l for l in out.strip().splitlines() if l.strip()]
        return rc, lines


def concept(code):
    f = form(code)
    duyet = os.path.join(HEROES, "inbox", code, "concept_duyet.png")
    if os.path.exists(duyet) or have(code, "concept"):
        log(f"{code}: đã có concept")
        return True
    if f.get("prev"):
        pc = f["prev"][0][0]
        if not os.path.exists(os.path.join(HEROES, "inbox", pc, "concept_duyet.png")):
            log(f"{code}: chờ concept_duyet của {pc}")
            return False
    run([os.path.join(HEROES, "build.py"), code])
    p1 = os.path.join(HEROES, "gui_gpt", code, "luot_1_concept.txt")
    for attempt in range(2):
        rc, lines = codex(p1, timeout=1500)
        log(f"{code}: concept -> {' | '.join(lines[-2:])}")
        if have(code, "concept"):
            return True
    return False


def nhom(code):
    f = form(code)
    if not os.path.exists(os.path.join(HEROES, "inbox", code, "concept_duyet.png")):
        log(f"{code}: chưa có concept_duyet, bỏ qua nhóm")
        return False
    run([os.path.join(HEROES, "build.py"), code])
    p2 = os.path.join(HEROES, "gui_gpt", code, "luot_2_nhom_manh.txt")
    steps = [g[0] for g in f["groups"]]
    for attempt in range(3):
        todo = [s for s in steps if not have(code, s)]
        if not todo:
            break
        for i in range(0, len(todo), 6):
            part = todo[i:i + 6]
            rc, lines = codex(p2, steps=part)
            got = [s for s in part if have(code, s)]
            log(f"{code}: gen {','.join(part)} -> có {','.join(got) or 'không'} ({lines[0] if lines else rc})")
    miss = [s for s in steps if not have(code, s)]
    if miss:
        log(f"{code}: còn thiếu nhóm {miss}")
        return False
    return True


def ghep(code):
    f = form(code)
    pid = f["aola"]
    rdir = os.path.join(AOLA, "reskin", f"moc_{pid}")
    rc, out = run([os.path.join(AOLA, "tools", "ghep_nhom.py"), rdir], timeout=1200)
    keep = [l for l in out.splitlines() if "IoU" in l or "Error" in l or "Traceback" in l or "lỗi" in l.lower() or "thiếu" in l]
    log(f"{code}: ghép rc={rc}\n    " + "\n    ".join(keep[-12:]) + ("\n    " + out[-600:] if rc else ""))
    if rc:
        return False
    rc, out = run([os.path.join(HERE, "anim_moc.py"), code, "--run"], timeout=1200)
    keep = [l for l in out.splitlines() if "khung" in l or "chiêu" in l or "Traceback" in l or "Error" in l]
    log(f"{code}: animation rc={rc}\n    " + "\n    ".join(keep[-10:]))
    rc3, out3 = run([os.path.join(AOLA, "tools", "portrait_png.py"), rdir], timeout=600)
    if rc3:
        log(f"{code}: chân dung lỗi\n    {out3[-400:]}")
    os.makedirs(SHOTS, exist_ok=True)
    shot = os.path.join(SHOTS, f"{code}.png")
    rc2, out2 = run([os.path.join(AOLA, "tools", "so_sanh_reskin.py"), f"moc_{pid}", f"goc_{pid}", shot, "6"], timeout=900)
    log(f"{code}: so sánh rc={rc2} {shot}" + ("\n    " + out2[-400:] if rc2 else ""))
    return rc == 0


def fx(pack):
    run([os.path.join(HEROES, "build_fx.py"), pack])
    p = os.path.join(HEROES, "gui_gpt", pack, "luot_1_hieu_ung.txt")
    steps = re.findall(r"^=== STEP (FX\d+)", open(p, encoding="utf-8").read(), re.M)
    for attempt in range(3):
        todo = [s for s in steps if not have(pack, s)]
        if not todo:
            break
        for i in range(0, len(todo), 6):
            part = todo[i:i + 6]
            rc, lines = codex(p, steps=part)
            log(f"{pack}: gen {','.join(part)} -> có {','.join(s for s in part if have(pack, s)) or 'không'}")
    miss = [s for s in steps if not have(pack, s)]
    log(f"{pack}: " + (f"còn thiếu {miss}" if miss else "đủ ảnh"))


if __name__ == "__main__":
    phase, codes = sys.argv[1], sys.argv[2:]
    for c in codes:
        try:
            if phase == "concept":
                concept(c)
            elif phase == "nhom":
                nhom(c)
            elif phase == "ghep":
                ghep(c)
            elif phase == "fx":
                fx(c)
            elif phase == "tron":
                if nhom(c):
                    ghep(c)
        except SystemExit:
            raise
        except Exception as e:  # noqa: BLE001
            log(f"{c}: LỖI {type(e).__name__}: {e}")
