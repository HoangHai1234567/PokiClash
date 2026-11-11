"""Golden của bản Unity sau lô 10 tướng mới đảo Thủy (2026-11-11), phần KHÔNG có menu Unity tính lại.

    py -3 -I ArtGen/Spine/quai/golden_thuy.py doi_id [--kiem]
        afk.json, pachinko.json: đổi id tướng cũ -> tướng mới cùng suất (và id thẻ của chúng). Hai golden này lấy mảnh từ ải đảo
        Thủy (ải 15, 70; boss đã gặp của máy bi). Tướng mới là bản chép (cùng độ hiếm, mảnh, thẻ cùng độ hiếm) đứng đúng chỗ tướng cũ
        trong ải và ngay sau tướng cũ trong danh sách, nên kết quả y hệt, chỉ khác tên. Giọt Sương không đổi (test máy bi dựng bản
        lưu "đã chọn Giọt Sương", TestData.OldStarter). Đã so bằng bộ chạy test ngoài Unity (VAO_GAME.md).
    py -3 -I ArtGen/Spine/quai/golden_thuy.py ghep_sim [--kiem]
        sim.json: ghép ô (win, rounds) từ Temp/GoldenRecalc.json (menu "PokiClash/Thử/Tính lại golden sim, tướng trên nút ải") vào
        sim.json, chỉ đổi ô khác, giữ định dạng một dòng. Chạy sau menu đó.
    --assets <thư mục Assets>   mặc định Assets của repo (dùng để thử trên bản chép)

Chạy lại bao nhiêu lần cũng được.
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))

# tướng cũ -> tướng mới cùng suất đảo Thủy (trừ Giọt Sương -> Tí Tách: xem đầu file)
HEROES = {
    "tieu_y": "thach_giai", "canh_cut": "ca_den", "mi_nhi": "ha_ba", "ma_ket": "so_ngoc", "vay_lam": "giong_bao",
    "kuba": "lien_kinh", "thuong_lam": "uyen_xa", "huyen_vu": "han_ngac", "lam_quan": "hai_long",
}
ID_FILES = ["afk.json", "pachinko.json"]


def arg(name, default=None):
    if name in sys.argv:
        i = sys.argv.index(name)
        return sys.argv[i + 1]
    return default


def card_map(assets):
    h = json.load(open(os.path.join(assets, "02 Data", "Json", "heroes.json"), encoding="utf-8"))
    by = {x["id"]: x for x in h["heroes"]}
    m = {}
    for old, new in HEROES.items():
        if new not in by:
            raise SystemExit(f"heroes.json chưa có {new}: chạy tuong_moi_thuy.py trước")
        for k in ("skill", "ult", "passive"):
            m[by[old][k]] = by[new][k]
    return m


def doi_id(assets, kiem):
    tokens = dict(HEROES)
    tokens.update(card_map(assets))
    for f in ID_FILES:
        p = os.path.join(assets, "02 Data", "Golden", f)
        raw = open(p, encoding="utf-8", newline="").read()
        s = raw
        counts = {}
        for old, new in tokens.items():
            n = s.count(f'"{old}"')
            if n:
                s = s.replace(f'"{old}"', f'"{new}"')
                counts[old] = n
        json.loads(s)  # vẫn là JSON hợp lệ
        if s == raw:
            print(f"{f}: không có gì phải đổi")
            continue
        print(f"{f}: " + ", ".join(f"{k}->{tokens[k]} x{v}" for k, v in counts.items()))
        if not kiem:
            with open(p, "w", encoding="utf-8", newline="") as fo:
                fo.write(s)


def ghep_sim(assets, kiem):
    rec_p = os.path.normpath(os.path.join(assets, "..", "Temp", "GoldenRecalc.json"))
    if not os.path.exists(rec_p):
        raise SystemExit(f"chưa có {rec_p}: chạy menu \"PokiClash/Thử/Tính lại golden sim, tướng trên nút ải\" trước")
    rec = json.load(open(rec_p, encoding="utf-8"))
    p = os.path.join(assets, "02 Data", "Golden", "sim.json")
    raw = open(p, encoding="utf-8", newline="").read()
    g = json.loads(raw)
    zones = {z["zone"]: z for z in g["zones"]}
    changed = []
    for rz in rec["sim"]:
        z = zones.get(rz["zone"])
        if z is None:
            raise SystemExit(f"sim.json không có đảo {rz['zone']}")
        st_by = {s["id"]: s for s in z["stages"]}
        for rs in rz["stages"]:
            s = st_by.get(rs["id"])
            if s is None:
                raise SystemExit(f"sim.json đảo {rz['zone']} không có ải {rs['id']}")
            cells = [{"win": int(c["win"]), "rounds": c["rounds"]} for c in rs["cells"]]
            for c in cells:  # số nguyên ghi không phần thập phân như bản gốc
                if isinstance(c["rounds"], float) and c["rounds"].is_integer():
                    c["rounds"] = int(c["rounds"])
            if cells != s["cells"]:
                changed.append((rz["zone"], rs["id"]))
                s["cells"] = cells
    out = json.dumps(g, separators=(",", ":"), ensure_ascii=False) + ("\n" if raw.endswith("\n") else "")
    by_zone = {}
    for z, i in changed:
        by_zone.setdefault(z, []).append(i)
    print("sim.json: " + ("không đổi" if not changed else "; ".join(f"{z} {len(v)} ải ({v[0]}..{v[-1]})" for z, v in by_zone.items())))
    if changed and not kiem:
        with open(p, "w", encoding="utf-8", newline="") as fo:
            fo.write(out)


def main():
    kiem = "--kiem" in sys.argv
    assets = os.path.abspath(arg("--assets", os.path.join(ROOT, "Assets")))
    mode = next((a for a in sys.argv[1:] if a in ("doi_id", "ghep_sim")), None)
    if mode == "doi_id":
        doi_id(assets, kiem)
    elif mode == "ghep_sim":
        ghep_sim(assets, kiem)
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main()
