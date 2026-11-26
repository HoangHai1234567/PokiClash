# So các bộ số cạnh nhau theo nhóm người chơi (trung vị cấp, ải; trung bình bi thu / ngày, tường, thua, mảnh).
#   py -3 -I so_sanh.py goc A_khoa_ban_the B_de_xuat C_siet_them
import os, sys, statistics as st
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # py -I bỏ thư mục script khỏi đường tìm module
import tong_hop as T

sets = sys.argv[1:]
data = {s: T.load(s) for s in sets}
for s in sets:
    bad = [p["id"] for p in data[s] if p.get("timedOut")]
    br = [p for p in data[s] if p.get("brokenDay", -1) > 0]
    print(f"{s}: {len(data[s])} người, quá giờ {len(bad)}, vỡ kinh tế {len(br)}" + (f" (ngày vỡ trung vị {st.median(p['brokenDay'] for p in br)})" if br else ""))
print()
rows = []
head = ["Mức chơi", "Tiền", "Đảo", "Bộ số", "n", "Cấp N7", "N14", "N30", "Ải N14", "N30", "Bi thu / ngày", "trong đó đảo", "QC", "IAP", "Trận thua", "Gặp tường", "Mảnh 30 ngày", "Đá 30 ngày", "Tướng", "Tổng sao", "Lực chiến N30"]
for e in T.ENG:
    for m in T.MON:
        for c in T.CAS:
            for s in sets:
                g = [p for p in data[s] if p["eng"] == e and p["m"] == m and p["cas"] == c and p.get("brokenDay", -1) < 0]
                if not g:
                    if any(p["eng"] == e and p["m"] == m and p["cas"] == c for p in data[s]):
                        rows.append([e, m, c, s, 0] + ["vỡ"] * 16)
                    continue
                inc = [T.income(p) for p in g]
                D = len(g[0]["level"]) - 1
                tot = T.avg(sum(v for k, v in i.items() if k != "máy bi trả lại") / T.days_of(p) for i, p in zip(inc, g))
                cas = T.avg(i["đảo Casino (ròng)"] / T.days_of(p) for i, p in zip(inc, g))
                qc = T.avg(i["quảng cáo"] / T.days_of(p) for i, p in zip(inc, g))
                iap = T.avg(i["IAP"] / T.days_of(p) for i, p in zip(inc, g))
                rows.append([e, m, c, s, len(g)] + [T.f0(T.med(p["level"][d] for p in g)) for d in (7, 14, 30)] + [T.f0(T.med(p["cleared"][d] for p in g)) for d in (14, 30)]
                            + [T.f0(tot), T.f0(cas), T.f0(qc), T.f0(iap), T.f0(T.avg(p["count"].get("thua", 0) for p in g)), T.f0(T.avg(p["count"].get("tường (ải kế < 30%)", 0) for p in g)),
                               T.f0(T.avg(sum(p["shards"].values()) for p in g)), T.f0(T.avg(sum(p["evo"].values()) for p in g)),
                               T.f1(T.avg(len(p["heroes"]) for p in g)), T.f0(T.avg(sum(p["heroes"].values()) for p in g)), T.f0(T.avg(p["power"][D] for p in g) / 1000) + "k"])
print(T.table(head, rows))
