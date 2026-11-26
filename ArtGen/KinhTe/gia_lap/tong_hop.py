# Gom kết quả 300 người chơi ảo của một bộ số thành bảng (markdown) để đọc và chép vào GD_Claude/33.
#   py -3 -I tong_hop.py <bộ số> [<bộ số> ...]   -> out/tong_hop_<bộ số>.md (in ra màn hình luôn)
import os, sys, json, glob, statistics as st
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ENG = ["chăm", "vừa", "ít"]
MON = ["F0", "FA", "P1", "P2", "P3"]
CAS = ["không ra đảo", "đảo thận trọng", "đảo máu me"]
# trọng số dân số (giả định, theo số ngành ở GD_Claude/26 mục 2.2): mức chơi, nhóm tiền
W_ENG = {"chăm": 0.15, "vừa": 0.35, "ít": 0.50}
W_MON = {"F0": 0.35, "FA": 0.55, "P1": 0.07, "P2": 0.025, "P3": 0.005}


def load(name):
    ps = []
    for f in sorted(glob.glob(os.path.join(HERE, "out", "res", name, "p*.json"))):
        with open(f, encoding="utf-8") as fh:
            p = json.load(fh)
        p["m"] = p["mon"][:2]
        ps.append(p)
    return ps


def med(xs):
    xs = [x for x in xs if x is not None]
    return st.median(xs) if xs else float("nan")


def avg(xs):
    xs = list(xs)
    return sum(xs) / len(xs) if xs else 0.0


def f0(v):
    return "–" if v != v else f"{v:,.0f}".replace(",", ".")


def f1(v):
    return "–" if v != v else f"{v:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")


def table(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "|".join("---" for _ in head) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(x) for x in r) + " |")
    return "\n".join(out)


def group(ps, **kw):
    r = ps
    for k, v in kw.items():
        if v is None:
            continue
        r = [p for p in r if (p[k] in v if isinstance(v, (list, tuple, set)) else p[k] == v)]
    return r


def src_sum(p, key, pred):
    return sum(v for k, v in p[key].items() if pred(k))


def days_of(p):
    return p["stoppedDay"] if p.get("stoppedDay", -1) > 0 else len(p["level"]) - 1


CASINO_IN = lambda k: k.startswith("đảo:")
PACH = lambda k: k.startswith("máy bi")


def income(p):
    """bi thu ròng ngoài máy bi: mọi nguồn trừ phần máy bi trả lại; đảo tính ròng (trả − cược − lệ phí − mua chợ)"""
    d = defaultdict(float)
    for k, v in p["ballsIn"].items():
        if PACH(k):
            d["máy bi trả lại"] += v
        elif CASINO_IN(k):
            d["đảo Casino (ròng)"] += v
        elif k.startswith("qc:"):
            d["quảng cáo"] += v
        elif k.startswith("iap:"):
            d["IAP"] += v
        elif k.startswith("ải"):
            d["ải"] += v
        elif k in ("cây bi", "Nhà (ruộng)"):
            d["cây bi + Nhà"] += v
        else:
            d["quà free (ngày, quỹ, chuỗi, rương mốc, AFK)"] += v
    for k, v in p["ballsOut"].items():
        if CASINO_IN(k):
            d["đảo Casino (ròng)"] -= v
    return d


def report(name):
    ps = load(name)
    if not ps:
        return "chưa có kết quả cho " + name
    D = len(ps[0]["level"]) - 1
    o = [f"# Bộ số `{name}`: {len(ps)} người chơi ảo, {D} ngày\n"]

    # 0. vỡ kinh tế
    broken = [p for p in ps if p.get("brokenDay", -1) > 0]
    if broken:
        o.append(f"**Vỡ kinh tế (bi vượt 1 triệu): {len(broken)} / {len(ps)} người**, trong đó {len([p for p in broken if p['m'] in ('F0', 'FA')])} người không trả tiền.")
        rows = []
        for e in ENG:
            for c in CAS[1:]:
                g = group(ps, eng=e, cas=c)
                b = [p["brokenDay"] for p in g if p.get("brokenDay", -1) > 0]
                rows.append([e, c, f"{len(b)} / {len(g)}", f0(med(b)) if b else "–", (f"{min(b)}–{max(b)}" if b else "–")])
        o.append(table(["Mức chơi", "Đảo", "Số người vỡ", "Ngày vỡ (trung vị)", "Sớm nhất – muộn nhất"], rows) + "\n")

    ok = [p for p in ps if p.get("brokenDay", -1) < 0]

    # 1. tiến độ
    o.append("## 1. Tiến độ (trung vị; người vỡ kinh tế bị loại)\n")
    rows = []
    for e in ENG:
        for m in MON:
            for c in CAS:
                g = group(ok, eng=e, m=m, cas=c)
                if not g:
                    continue
                fin = [p["finishedDay"] for p in g if p["finishedDay"] > 0]
                mx = [p["maxLevelDay"] for p in g if p["maxLevelDay"] > 0]
                rows.append([e, m, c, len(g)] + [f0(med(p["level"][d] for p in g)) for d in (1, 3, 7, 14, 30)] + [f0(med(p["cleared"][d] for p in g)) for d in (7, 14, 30)]
                            + [f"{len(mx)}/{len(g)}: {f0(med(mx))}" if mx else "–", f"{len(fin)}/{len(g)}: {f0(med(fin))}" if fin else "–", f1(avg(p["usdCum"][D] for p in g))])
    o.append(table(["Mức chơi", "Tiền", "Đảo", "n", "Cấp N1", "N3", "N7", "N14", "N30", "Ải N7", "N14", "N30", "Tới cấp 200 (số người: ngày)", "Hết 350 ải (số người: ngày)", "USD"], rows) + "\n")

    # 2. thu nhập bi mỗi ngày
    o.append("## 2. Bi thu mỗi ngày theo nguồn (trung bình 30 ngày, không tính bi máy trả lại)\n")
    keys = ["ải", "cây bi + Nhà", "quà free (ngày, quỹ, chuỗi, rương mốc, AFK)", "quảng cáo", "đảo Casino (ròng)", "IAP"]
    rows = []
    for e in ENG:
        for m in MON:
            for c in CAS:
                g = group(ok, eng=e, m=m, cas=c)
                if not g:
                    continue
                inc = [income(p) for p in g]
                dd = [days_of(p) for p in g]
                vals = [avg(i[k] / d for i, d in zip(inc, dd)) for k in keys]
                back = avg(i["máy bi trả lại"] / d for i, d in zip(inc, dd))
                drop = avg(p["droppedCum"][D] / d for p, d in zip(g, dd))
                rows.append([e, m, c] + [f0(v) for v in vals] + [f0(sum(vals)), f0(back), f0(drop)])
    o.append(table(["Mức chơi", "Tiền", "Đảo"] + ["Ải", "Cây + Nhà", "Quà free", "Quảng cáo", "Đảo (ròng)", "IAP"] + ["**Tổng thu**", "Máy trả lại", "Bi thả / ngày"], rows) + "\n")

    # 3. đảo theo trò
    o.append("## 3. Đảo Casino theo trò (người không trả tiền F0 + FA, bi mỗi ngày kể từ khi mở đảo ~ tính trên 30 ngày)\n")
    games = [("câu cá", ["đảo:câu cá"], []), ("quán trọ", ["đảo:quán trọ"], []), ("đua", ["đảo:đua (trả)", "đảo:cúp đua tuần"], ["đảo:đua (cược)"]),
             ("hầm đấu", ["đảo:hầm đấu (thưởng)"], ["đảo:hầm đấu (lệ phí)"]), ("blackjack", ["đảo:blackjack (trả)"], ["đảo:blackjack (cược)"]),
             ("roulette", ["đảo:roulette (trả)"], ["đảo:roulette (cược)"]), ("slot", ["đảo:slot (trả)"], ["đảo:slot (cược)"]),
             ("hũ bàn", ["đảo:hũ bàn + mảnh khách mời"], []), ("chợ đen", ["đảo:bán thẻ thừa"], ["đảo:chợ đen"])]
    rows = []
    for e in ENG:
        for c in CAS[1:]:
            g = group(ok, eng=e, m=["F0", "FA"], cas=c)
            if not g:
                continue
            for gname, ins, outs in games:
                i = avg(sum(p["ballsIn"].get(k, 0) for k in ins) / days_of(p) for p in g)
                x = avg(sum(p["ballsOut"].get(k, 0) for k in outs) / days_of(p) for p in g)
                sh = avg(sum(p["shards"].get(k, 0) for k in ins + outs) / days_of(p) for p in g)
                ev = avg(sum(p["evo"].get(k, 0) for k in ins + outs) / days_of(p) for p in g)
                rows.append([e, c, gname, f0(x), f0(i), f0(i - x), (f1(i / x) if x > 0 else "–"), f1(sh), f1(ev * 1.0)])
    o.append(table(["Mức chơi", "Đảo", "Trò", "Bi bỏ ra / ngày", "Bi nhận / ngày", "Ròng / ngày", "Nhận ÷ bỏ", "Mảnh / ngày", "Đá tiến hóa / ngày"], rows) + "\n")

    # 4. mảnh và đá theo nguồn
    o.append("## 4. Mảnh tướng và đá tiến hóa theo nguồn (cả 30 ngày, trung bình mỗi người)\n")

    def bucket(k):
        if PACH(k): return "máy bi (trứng rương)"
        if k.startswith("đảo:"): return "đảo Casino"
        if k.startswith("qc:"): return "quảng cáo"
        if k.startswith("iap:"): return "IAP"
        if k.startswith("ải"): return "ải"
        if k.startswith("AFK"): return "AFK"
        return "khác (rương mốc, quỹ free, chuỗi free, Đền, Hang)"
    bk = ["ải", "AFK", "máy bi (trứng rương)", "khác (rương mốc, quỹ free, chuỗi free, Đền, Hang)", "quảng cáo", "đảo Casino", "IAP"]
    for key, title in (("shards", "Mảnh"), ("evo", "Đá tiến hóa")):
        rows = []
        for e in ENG:
            for m in MON:
                for c in CAS:
                    g = group(ok, eng=e, m=m, cas=c)
                    if not g:
                        continue
                    tot = defaultdict(float)
                    for p in g:
                        for k, v in p[key].items():
                            tot[bucket(k)] += v / len(g)
                    s = sum(tot.values())
                    rows.append([e, m, c] + [f0(tot[b]) for b in bk] + [f0(s), (f"{tot['đảo Casino'] / (s - tot['đảo Casino']) * 100:.0f}%" if s - tot["đảo Casino"] > 0 else "–")])
        o.append(f"**{title}**\n\n" + table(["Mức chơi", "Tiền", "Đảo"] + ["Ải", "AFK", "Máy bi", "Khác", "Quảng cáo", "Đảo", "IAP"] + ["Tổng", "Đảo ÷ nguồn khác"], rows) + "\n")

    # 5. quảng cáo
    o.append("## 5. Quảng cáo thưởng (nhóm có xem; số lượt mỗi ngày chơi)\n")
    rows = []
    places = sorted({k for p in ok for k in p["ads"]})
    for e in ENG:
        for label, pred in (("FA (ít)", lambda p: p["mon"].startswith("FA") and "ít" in p["mon"]), ("FA (nhiều)", lambda p: p["mon"].startswith("FA") and "nhiều" in p["mon"]),
                            ("P1", lambda p: p["m"] == "P1"), ("P2", lambda p: p["m"] == "P2"), ("P3", lambda p: p["m"] == "P3")):
            g = [p for p in group(ok, eng=e) if pred(p)]
            if not g:
                continue
            nd = [max(1, days_of(p) - p["count"].get("ngày nghỉ", 0)) for p in g]
            tot = avg(sum(v for k, v in p["ads"].items() if not k.endswith(")")) / d for p, d in zip(g, nd))
            inst = avg(sum(v for k, v in p["ads"].items() if k.endswith(")")) / d for p, d in zip(g, nd))
            balls = avg(src_sum(p, "ballsIn", lambda k: k.startswith("qc:")) / d for p, d in zip(g, nd))
            sh = avg(src_sum(p, "shards", lambda k: k.startswith("qc:")) / d for p, d in zip(g, nd))
            ev = avg(src_sum(p, "evo", lambda k: k.startswith("qc:")) / d for p, d in zip(g, nd))
            rows.append([e, label, f1(tot), f1(inst), f0(balls), f1(sh), f1(ev), f1(balls / tot) if tot > 0 else "–"])
    o.append(table(["Mức chơi", "Nhóm", "Lượt xem / ngày", "Lượt trao ngay / ngày", "Bi từ QC / ngày", "Mảnh từ QC / ngày", "Đá từ QC / ngày", "Bi mỗi lượt xem"], rows) + "\n")
    rows = []
    for pl in places:
        g = [p for p in ok if p["mon"].startswith("FA") and "nhiều" in p["mon"]]
        rows.append([pl, f1(avg(p["ads"].get(pl, 0) / max(1, days_of(p) - p["count"].get("ngày nghỉ", 0)) for p in g))])
    o.append("Theo chỗ đặt (nhóm FA xem nhiều, mọi mức chơi):\n\n" + table(["Chỗ đặt", "Lượt / ngày"], rows) + "\n")

    # 6. IAP
    o.append("## 6. IAP theo gói (nhóm trả tiền; giả định mua theo persona)\n")
    prods = sorted({k for p in ok for k in p["usd"]})
    rows = []
    for pr in prods:
        g = [p for p in ok if p["usd"].get(pr, 0) > 0]
        usd = sum(p["usd"][pr] for p in g)
        n = sum(p["count"].get("buy:" + pr, 0) for p in g)
        val = sum(p["iapValue"].get(pr, 0) for p in g)
        balls = sum(p["ballsIn"].get("iap:" + pr, 0) for p in g)
        sh = sum(p["shards"].get("iap:" + pr, 0) for p in g)
        ev = sum(p["evo"].get("iap:" + pr, 0) for p in g)
        rows.append([pr, len(g), f0(n), f1(usd), f0(balls / usd) if usd else "–", f1(sh / usd) if usd else "–", f1(ev / usd) if usd else "–", f0(val / usd) if usd else "–"])
    o.append(table(["Gói", "Người mua", "Lượt mua", "Tổng USD", "Bi / USD", "Mảnh / USD", "Đá / USD", "Bi quy đổi / USD (lúc mua)"], rows) + "\n")

    # 7. áp lực
    o.append("## 7. Điểm nghẽn (áp lực để mua / xem quảng cáo), trung bình mỗi người trong 30 ngày\n")
    cks = ["phiên", "hết bi", "vào máy không có bi", "thua", "tường (ải kế < 30%)", "ngày không qua ải mới", "phiên kẹt đá tiến hóa", "trận đánh lại", "trận ải mới"]
    rows = []
    for e in ENG:
        for m in MON:
            for c in CAS:
                g = group(ok, eng=e, m=m, cas=c)
                if not g:
                    continue
                rows.append([e, m, c] + [f1(avg(p["count"].get(k, 0) for p in g)) for k in cks] + [f0(avg(p["ballsHeld"][D] for p in g)), f0(avg(p["evoLeft"] for p in g))])
    o.append(table(["Mức chơi", "Tiền", "Đảo"] + ["Phiên", "Lần hết bi", "Vào máy 0 bi", "Trận thua", "Lần gặp tường", "Ngày không qua ải mới", "Phiên kẹt đá", "Trận đánh lại", "Trận ải mới", "Bi cầm cuối kỳ", "Đá thừa cuối kỳ"], rows) + "\n")

    # 8. popup
    o.append("## 8. Popup bán đã bật (trung bình mỗi người, 30 ngày)\n")
    pk = sorted({k for p in ok for k in p["count"] if k.startswith("popup:")})
    rows = []
    for m in MON:
        g = group(ok, m=m)
        rows.append([m] + [f1(avg(p["count"].get(k, 0) for p in g)) for k in pk])
    o.append(table(["Tiền"] + [k[6:] for k in pk], rows) + "\n")

    # 9. dân số có trọng số
    o.append("## 9. Quy về dân số (trọng số giả định: chăm 15%, vừa 35%, ít 50%; F0 35%, FA 55%, P1 7%, P2 2,5%, P3 0,5%; đảo: nửa thận trọng nửa máu me)\n")
    tw = usd = ads = 0
    for p in ok:
        w = W_ENG[p["eng"]] * W_MON[p["m"]]
        tw += w
        usd += w * p["usdCum"][D]
        ads += w * p["adsCum"][D]
    o.append(f"- Chi trung bình mỗi người cài trong 30 ngày (theo persona, không phải dự báo): {usd / tw:.2f} USD; quảng cáo xem trung bình: {ads / tw:.0f} lượt / 30 ngày.\n")
    text = "\n".join(o)
    with open(os.path.join(HERE, "out", f"tong_hop_{name}.md"), "w", encoding="utf-8") as fh:
        fh.write(text)
    return text


if __name__ == "__main__":
    for n in sys.argv[1:] or ["goc"]:
        print(report(n))
        print()
