# Ngày (trung vị) người chơi ảo tới từng mốc số ải đã qua, theo nhóm, để so các bộ số về "đi trước bao nhiêu ngày".
#   py -3 -I moc_ai.py <bộ số> [...]        (người không ra đảo; nhóm không có kết quả thì bỏ)
import os, sys, statistics as st
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tong_hop as T

sets = sys.argv[1:]
MARKS = [50, 100, 150, 200, 250, 300, 350]
data = {s: T.load(s) for s in sets}
p0 = next(iter(data.values()))[0]
key = "cleared" if "cleared" in p0 else next(k for k in p0 if isinstance(p0[k], list) and "clear" in k.lower())


def day_to(p, n):
    for i, v in enumerate(p[key]):
        if v >= n:
            return i
    return None


print("| Mức chơi | Nhóm | Bộ số | n | " + " | ".join("%d ải" % m for m in MARKS) + " | Cấp N30 | Thua / 30 ngày đầu |")
print("|---|---|---|---|" + "---|" * (len(MARKS) + 2))
for eng in T.ENG:
    for mon in ("F0", "FA", "P1", "P2", "P3"):
        for s in sets:
            ps = [p for p in data[s] if p.get("eng") == eng and p["m"] == mon and not p.get("casino") and p.get("brokenDay", -1) <= 0]
            if not ps:
                continue
            cells = []
            for m in MARKS:
                ds = [day_to(p, m) for p in ps]
                ok = [d for d in ds if d is not None]
                cells.append(("%d" % st.median(ok) if len(ok) * 2 > len(ds) else "chưa") + ("" if len(ok) == len(ds) else " (%d/%d)" % (len(ok), len(ds))))
            lv = st.median(p["level"][min(30, len(p["level"]) - 1)] for p in ps)
            print("| %s | %s | %s | %d | %s | %d | |" % (eng, mon, s, len(ps), " | ".join(cells), lv))
