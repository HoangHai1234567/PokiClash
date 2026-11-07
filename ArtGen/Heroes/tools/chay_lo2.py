"""Chạy trọn từng dạng boss lô 2 đảo Thủy (2026-11-07 đêm, người dùng ủy quyền làm một mạch):
chờ concept -> duyệt (chép concept_duyet.png) -> build.py -> gen nhóm bằng Codex (mỗi lệnh tối đa 6 bước, gen lại bước thiếu) ->
anim_lo2.py -> ghep_nhom.py (tự chạy anim_moi) -> so_sanh_reskin.py. Ghi tiến độ vào ArtGen/Heroes/inbox/chay_lo2.log.

    py -3 -I ArtGen/Heroes/tools/chay_lo2.py <mã> [<mã> ...]
"""
import json
import os
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
HEROES = os.path.normpath(os.path.join(HERE, ".."))
AOLA = next(p for p in ("D:/Aola-20261029T161238Z-1-001/Aola/AolaRipper/AolaRipper", "E:/ProjectAtomik/aola") if os.path.isdir(p))
PY = sys.executable
LOG = os.path.join(HEROES, "inbox", "chay_lo2.log")
SHOTS = os.path.join(os.environ.get("TEMP", HERE), "aola_work")
sys.stdout.reconfigure(encoding="utf-8")


def log(msg):
    line = time.strftime("%H:%M:%S ") + msg
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def run(args, timeout=3000):
    p = subprocess.run([PY, "-I"] + args, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def form(code):
    forms = json.load(open(os.path.join(HEROES, "forms_thuy_lo2.json"), encoding="utf-8"))
    return next(f for f in forms if f["code"] == code)


def have(code, step):
    d = os.path.join(HEROES, "inbox", code, "tai_ve")
    return any(x.lower().startswith(step.lower()) and x.lower().endswith(".png") for x in os.listdir(d)) if os.path.isdir(d) else False


def one(code):
    f = form(code)
    tai = os.path.join(HEROES, "inbox", code, "tai_ve")
    duyet = os.path.join(HEROES, "inbox", code, "concept_duyet.png")
    # 1. concept (dạng sau cần concept dạng 1 đã duyệt; concept của dạng này do chuỗi gen concept vẽ)
    t0 = time.time()
    while not os.path.exists(duyet):
        if have(code, "concept"):
            src = max((os.path.join(tai, x) for x in os.listdir(tai) if x.startswith("concept")), key=os.path.getmtime)
            shutil.copy2(src, duyet)
            log(f"{code}: duyệt concept {os.path.basename(src)}")
            break
        if time.time() - t0 > 3600:
            log(f"{code}: chờ concept quá 1 giờ, bỏ qua")
            return
        time.sleep(20)
    # 2. prompt lượt 2 và gen nhóm
    run([os.path.join(HEROES, "build.py"), code])
    p2 = os.path.join(HEROES, "gui_gpt", code, "luot_2_nhom_manh.txt")
    steps = [g[0] for g in f["groups"]]
    attempt, waited = 0, 0
    while attempt < 3:
        todo = [s for s in steps if not have(code, s)]
        if not todo:
            break
        limited = False
        for i in range(0, len(todo), 6):
            part = todo[i:i + 6]
            rc, out = run([os.path.join(HERE, "gen_codex.py"), p2, "--steps", ",".join(part), "--timeout", "2400"], timeout=2700)
            log(f"{code}: gen {','.join(part)} -> {out.strip().splitlines()[-1] if out.strip() else rc}")
            if "usage limit" in out:  # hết hạn mức gói ChatGPT: chờ rồi thử lại, không tính là một lần hỏng
                limited = True
                break
        if limited:
            if waited > 4 * 3600:
                log(f"{code}: hết hạn mức quá 4 giờ, dừng")
                return
            log(f"{code}: hết hạn mức Codex, chờ 10 phút")
            time.sleep(600)
            waited += 600
            continue
        attempt += 1
    miss = [s for s in steps if not have(code, s)]
    if miss:  # không ghép dở: nhóm thiếu sẽ để lọt hình gốc aola
        log(f"{code}: còn thiếu nhóm {miss}, chưa ghép")
        return
    # 3. animation, ghép, so sánh
    run([os.path.join(HERE, "anim_lo2.py"), code])
    rc, out = run([os.path.join(AOLA, "tools", "ghep_nhom.py"), os.path.join(AOLA, "reskin", f"thuy_{f['aola']}")], timeout=900)
    keep = [l for l in out.splitlines() if "IoU" in l or "1_4:" in l or "1_6:" in l or "Error" in l or "Traceback" in l]
    log(f"{code}: ghép rc={rc}\n  " + "\n  ".join(keep))
    os.makedirs(SHOTS, exist_ok=True)
    run([os.path.join(AOLA, "tools", "so_sanh_reskin.py"), f"thuy_{f['aola']}", f"goc_{f['aola']}",
         os.path.join(SHOTS, f"ss_{f['aola']}.png"), "6", "--cell", "140"], timeout=900)
    log(f"{code}: xong (so sánh: {os.path.join(SHOTS, 'ss_' + str(f['aola']) + '.png')})")


if __name__ == "__main__":
    for c in sys.argv[1:]:
        try:
            one(c)
        except Exception as e:  # noqa: BLE001
            log(f"{c}: LỖI {e}")
