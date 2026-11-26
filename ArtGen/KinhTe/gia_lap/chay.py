# Chạy 300 người chơi ảo cho một hoặc nhiều bộ số, tối đa N tiến trình cùng lúc (mặc định 6: giới hạn CPU người dùng dặn), chạy tiếp
# được (bỏ qua id đã có kết quả). Mỗi khúc 10 id liền nhau (một ô mức chơi × nhóm tiền × đảo), khúc nặng chạy trước.
#   py -3 -I chay.py <bộ số> [<bộ số> ...] [--n 6] [--ngay 30] [--lam-lai]
import os, sys, subprocess, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build

args = sys.argv[1:]
def opt(name, default):
    if name in args:
        i = args.index(name); v = args[i + 1]; del args[i:i + 2]; return v
    return default
N = min(6, int(opt("--n", "6")))
DAYS = opt("--ngay", "30")
NHOM = opt("--nhom", "")  # chỉ chạy các nhóm tiền này, ví dụ "0,1,3" (F0, FA, P2); rỗng: cả 5
nhom = {int(x) for x in NHOM.split(",") if x != ""}
redo = "--lam-lai" in args
if redo: args.remove("--lam-lai")
sets = args or ["goc"]
build.build()
jobs = []
for st in sets:
    res = os.path.join(build.OUT, "res", st)
    os.makedirs(res, exist_ok=True)
    if redo:
        for f in os.listdir(res): os.remove(os.path.join(res, f))
    chunks = [(a, a + 10) for a in range(0, 300, 10) if not nhom or (a // 20 % 5) in nhom]
    # nặng trước: nhóm tiền cao (m = id//20%5), có đảo
    chunks.sort(key=lambda c: (-(c[0] // 20 % 5), -(c[0] // 10 % 2), c[0]))
    for a, b in chunks:
        if all(os.path.exists(os.path.join(res, "p%03d.json" % i)) for i in range(a, b)): continue
        jobs.append((st, a, b))
print("khúc cần chạy:", len(jobs), "| tiến trình cùng lúc:", N)
run, t0 = [], time.time()
while jobs or run:
    run = [(p, j) for p, j in run if p.poll() is None]
    while jobs and len(run) < N:
        j = jobs.pop(0)
        log = open(os.path.join(build.OUT, "log_%s_%03d.txt" % (j[0], j[1])), "w", encoding="utf-8")
        p = subprocess.Popen([build.MONO, os.path.join(build.OUT, "sim.exe"), "pop", j[0], str(j[1]), str(j[2]), DAYS, "6"], cwd=build.OUT, stdout=log, stderr=log)
        run.append((p, j))
    time.sleep(1)
print("xong sau %.0f giây" % (time.time() - t0))
