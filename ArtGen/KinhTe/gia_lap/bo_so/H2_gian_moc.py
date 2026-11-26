# Vòng 1: giãn sức tướng theo mốc (bảng MOC của GD_Claude/34 mục 2.1) + địch mạnh dần theo mốc, chưa phát gói tướng.
MOC = [1.10, 1.00, 1.28, 1.45, 1.68, 1.95, 2.25, 2.60, 3.00, 3.80]
ALPHA = 0.6


def patch(b, grants=()):
    b["sim"] = {"mocPower": MOC, "grants": list(grants)}


def patch_stages(stg):
    stages = stg if isinstance(stg, list) else stg["stages"]
    zones = {}
    for st in stages:
        zones.setdefault(st["zone"], []).append(st)
    for z, lst in zones.items():
        lst.sort(key=lambda x: x["idx"])
        k = 0
        for st in lst:
            if st.get("tag") == "hero" or st.get("kind") in ("mini", "boss"):
                k += 1
            best = max(MOC[:max(1, k - 1)])  # tướng mạnh nhất người chơi đã có thể thu phục trước mốc này
            f = (best / MOC[0]) ** ALPHA
            for e in st["enemies"]:
                e["buff"] = round((1 + e.get("buff", 0)) * f - 1, 4)
