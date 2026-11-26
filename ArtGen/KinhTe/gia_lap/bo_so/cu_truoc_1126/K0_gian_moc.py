# Bộ K0: D (EXP dốc) + giãn sức mạnh theo MỐC tướng của mỗi đảo + địch mạnh dần theo mốc. Chưa bán gói tướng.
# - MOC: hệ số sức của tướng mốc 1..10 (game hiện theo độ hiếm: 1,1; 1; 1,1; 1,1; 1,23; 1,23; 1,38; 1,38; 1,38; 1,76).
#   Đề xuất: từ mốc 3 mỗi mốc hơn mốc trước khoảng 15% (bằng khoảng 5 cấp).
# - Địch từ ải tướng mốc k trở đi mạnh thêm (sức tướng mạnh nhất trước mốc k / sức mốc 1)^ALPHA: phải đổi sang tướng mốc sau mới theo kịp.
# - grants: giả lập gói tướng {day, moc, star, card}: tướng mốc đó của đảo cùng hệ tướng khởi đầu.
import importlib.util, os


def _load(n):
    spec = importlib.util.spec_from_file_location(n, os.path.join(os.path.dirname(os.path.abspath(__file__)), n + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


D = _load("D_exp_doc")
MOC = [1.10, 1.00, 1.28, 1.45, 1.68, 1.95, 2.25, 2.60, 3.00, 3.80]
ALPHA = 0.6


def patch(b, grants=()):
    D.patch(b)
    b["sim"]["mocPower"] = MOC
    b["sim"]["grants"] = list(grants)


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
