# Thời gian "phá đảo" (xong 350 ải) và chạm trần cấp theo nhóm, cho các bộ số chạy dài (90 ngày).
#   py -3 -I pha_dao.py B90 D_exp_doc E_boss_manh
# Người chưa xong trong kỳ: ước lượng ngày xong bằng tốc độ qua ải của 30 ngày cuối (ghi kèm dấu ~).
import os, sys, statistics as st
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tong_hop as T

sets = sys.argv[1:]
data = {s: T.load(s) for s in sets}
ROWS = [("chăm", "F0", None), ("chăm", "FA", "ít"), ("chăm", "FA", "nhiều"), ("chăm", "P1", None), ("chăm", "P2", None), ("chăm", "P3", None),
        ("vừa", "F0", None), ("vừa", "FA", "ít"), ("vừa", "FA", "nhiều"), ("vừa", "P1", None), ("vừa", "P2", None), ("vừa", "P3", None),
        ("ít", "F0", None), ("ít", "FA", "nhiều"), ("ít", "P2", None)]


def reach(p, key, val):
    for d, v in enumerate(p[key]):
        if v >= val:
            return d
    return None


def finish_est(p):
    D = len(p["cleared"]) - 1
    f = reach(p, "cleared", 350)
    if f is not None:
        return f, True
    rate = (p["cleared"][D] - p["cleared"][D - 30]) / 30.0
    return (D + (350 - p["cleared"][D]) / rate if rate > 0.05 else float("inf")), False


for cas in ("không ra đảo", "đảo thận trọng"):
    print(f"\n## {cas}\n")
    head = ["Mức chơi", "Nhóm", "Bộ số", "n", "Cấp N7 / N30 / N60 / N90", "Ải N30 / N60 / N90", "Xong 350 ải (ngày)", "Chạm cấp 200 (ngày)", "Thua / 30 ngày", "Gặp tường / 30 ngày",
            "Bi thu / ngày", "USD / 30 ngày", "QC xem / ngày"]
    rows = []
    for e, m, sub in ROWS:
        for s in sets:
            g = [p for p in data[s] if p["eng"] == e and p["m"] == m and p["cas"] == cas and (sub is None or sub in p["mon"])]
            if not g:
                continue
            D = len(g[0]["level"]) - 1
            fin = [finish_est(p) for p in g]
            done = sum(1 for f, ok in fin if ok)
            fm = st.median(f for f, ok in fin)
            ftxt = (f"{fm:.0f}" if done == len(g) else f"~{fm:.0f}" if fm != float("inf") else "không tới") + f" ({done}/{len(g)} xong)"
            cap = [reach(p, "level", 200) for p in g]
            ctxt = f"{st.median(c for c in cap if c is not None):.0f} ({sum(1 for c in cap if c is not None)}/{len(g)})" if any(c is not None for c in cap) else "chưa"
            days = lambda xs: " / ".join(T.f0(T.med(p[xs[0]][d] for p in g)) for d in xs[1] if d <= D)
            rows.append([e, m + (f" ({sub})" if sub else ""), s, len(g), days(("level", (7, 30, 60, 90))), days(("cleared", (30, 60, 90))), ftxt, ctxt,
                         T.f0(T.avg(p["count"].get("thua", 0) for p in g) * 30 / D), T.f0(T.avg(p["count"].get("tường (ải kế < 30%)", 0) for p in g) * 30 / D),
                         T.f0(T.avg(sum(v for k, v in T.income(p).items() if k != "máy bi trả lại") / T.days_of(p) for p in g)),
                         T.f1(T.avg(p["usdCum"][D] for p in g) * 30 / D), T.f1(T.avg(p["adsCum"][D] for p in g) / D)])
    print(T.table(head, rows))
