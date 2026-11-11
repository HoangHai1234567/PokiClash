"""Lô 10 tướng mới đảo Thủy (2026-11-11): thêm 10 tướng vào heroes.json, thẻ vào cards.json, đổi tướng ở 10 suất đảo Thủy trong
stages.json. Chạy lại bao nhiêu lần cũng được (idempotent): tướng, thẻ đã có thì ghi đè đúng theo bảng, chưa có thì chèn.

Quyết định người dùng (DAC_TA_LO_THUY.md mục 1, VAO_GAME.md):
- tướng mới id mới, tên mới; chỉ số, độ hiếm, mảnh CHÉP từ tướng cũ cùng suất; thẻ chép số và hiệu ứng của thẻ tướng cũ, đổi tên
  theo chiêu mới (skill ~ chiêu `cast` dạng 1, ult ~ chiêu `skill` dạng 1);
- tướng cũ giữ trong danh sách, chỉ mất suất trên đảo; Tí Tách thay Giọt Sương (Thủy Long) trong `starters`;
- bị động boss ải 40, 60, 70 chép từ bị động boss tướng cũ (kuba_boss, huyen_vu_boss, lam_quan_boss) thành `<id>_boss`, thay đúng
  chỗ trong `traits` (test IslandTests: mọi bị động boss phải gắn cho đúng chủ ở một ải, nên bản cũ không giữ lại được).

Chỗ chèn: tướng mới ngay sau tướng cũ cùng suất (Tí Tách ngay sau Giọt Sương: thứ tự tướng có tướng khởi đầu không đổi so với các
tướng khác, golden máy bi, rương ít lệch), thẻ ngay sau thẻ của tướng cũ.

    py -3 -I ArtGen/Spine/quai/tuong_moi_thuy.py           ghi heroes.json, cards.json, stages.json (chỉ ải đảo Thủy)
    py -3 -I ArtGen/Spine/quai/tuong_moi_thuy.py --kiem    chỉ in sẽ đổi gì, không ghi

Bản Unity: sau khi chạy, menu "PokiClash/Nhập dữ liệu". Menu "PokiClash/Dữ liệu/Đảo 70 ải: sinh lại (5 đảo)" (IslandGen.Plan Thuy
đã đổi theo cùng bảng) cho ra đúng stages.json này (đã so ngoài Unity, xem VAO_GAME.md).
"""
import copy
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
JSON_DIR = os.path.join(ROOT, "Assets", "02 Data", "Json")

# (id mới, tướng cũ cùng suất, ải, tên, danh hiệu, dòng, các dạng (tên, mã hình, cỡ), thẻ (tên, biểu tượng), bị động boss (tên, biểu tượng))
NEW = [
    dict(id="ti_tach", old="giot_suong", at=1, name="Tí Tách", title="Võ sĩ giọt mưa", line="Dòng Tí Tách",
         forms=[("Tí Tách", 0.92), ("Sóng Thần", 1.1)],
         skill=("Súng Nước", "drop"), ult=("Mưa Rào", "wave"), pas=("Mưa Đầu Mùa", "drop")),
    dict(id="thach_giai", old="tieu_y", at=5, name="Thạch Giải", title="Cua ẩn sĩ nhà đá", line="Dòng Thạch Giải",
         forms=[("Thạch Giải", 0.92), ("Thạch Thành Giải", 1.1)],
         skill=("Bọt Nước", "bubble"), ult=("Đá Ngầm Trồi", "rock"), pas=("Vũng Triều", "drop")),
    dict(id="nong_xoay", old="canh_cut", at=10, name="Nòng Xoáy", title="Nòng nọc mắt bão", line="Dòng Nòng Xoáy",
         forms=[("Nòng Xoáy", 0.92), ("Ếch Lốc", 1.1)],
         skill=("Đuôi Xoáy", "wave"), ult=("Xoáy Bong Bóng", "bubble"), pas=("Vụng San Hô", "drop")),
    dict(id="ha_ba", old="mi_nhi", at=15, name="Hà Bá", title="Hà mã nuốt sóng", line="Dòng Hà Bá",
         forms=[("Hà Mã Con", 0.92), ("Hà Bá", 1.1)],
         skill=("Súng Nước", "drop"), ult=("Ngáp Sóng", "wave"), pas=("Hồn Nước", "drop")),
    dict(id="so_ngoc", old="ma_ket", at=20, name="Sò Ngọc", title="Pháo đài ngọc trai", line="Dòng Sò Ngọc",
         forms=[("Sò Gai", 0.92), ("Bạng Vương", 1.1)],
         skill=("Phun Bọt Ngọc", "bubble"), ult=("Mưa Gai", "fang"), pas=("Tim Ngọc Trai", "moon")),
    dict(id="giong_bao", old="vay_lam", at=30, name="Giông Bão", title="Kỳ giông gọi mưa", line="Dòng Giông Bão",
         forms=[("Giông Mưa", 0.92), ("Giông Bão", 1.1)],
         skill=("Bầu Phun", "drop"), ult=("Cầu Mưa", "wave"), pas=("Bầu Hứng Mưa", "drop")),
    dict(id="lien_kinh", old="kuba", at=40, name="Liên Kình", title="Kình ngư cõng sen thiêng", line="Dòng Liên Kình",
         forms=[("Kình Nụ", 0.92), ("Liên Kình", 1.1)],
         skill=("Bong Bóng Sen", "bubble"), ult=("Nụ Bung", "lotus"), pas=("Sen Thiêng", "lotus"),
         trait=("kuba_boss", "Sen Hộ Thể", "lotus")),
    dict(id="uyen_xa", old="thuong_lam", at=50, name="Uyên Xà", title="Rắn đèn vực sâu", line="Dòng Uyên Xà",
         forms=[("Uyên Nhi", 0.92), ("Uyên Xà", 1.1)],
         skill=("Thủy Thương", "trident"), ult=("Mưa Bọt", "bubble"), pas=("Đèn Vực Sâu", "torch")),
    dict(id="han_ngac", old="huyen_vu", at=60, name="Hàn Ngạc", title="Cá sấu băng vực sâu", line="Dòng Hàn Ngạc",
         forms=[("Ngạc Nhi", 0.92), ("Hàn Ngạc Vương", 1.1)],
         skill=("Hàn Phong", "wind"), ult=("Cọc Băng", "crack"), pas=("Hàm Băng", "fang"),
         trait=("huyen_vu_boss", "Giáp Băng Hộ Thể", "shield")),
    dict(id="hai_long", old="lam_quan", at=70, name="Hải Long", title="Rồng biển nhiều đầu", line="Dòng Hải Long",
         forms=[("Hải Long Nhi", 0.95), ("Hải Long Tam Thủ", 1.1), ("Hải Long Ngũ Đầu", 1.16)],
         skill=("Hải Long Phun", "wave"), ult=("Hải Long Gầm", "rage"), pas=("Vảy Ngọc", "shield"),
         trait=("lam_quan_boss", "Long Uy Chấn", "rage")),
]
OLD2NEW = {n["old"]: n["id"] for n in NEW}
STARTER_OLD, STARTER_NEW = "giot_suong", "ti_tach"


def load(name):
    p = os.path.join(JSON_DIR, name)
    raw = open(p, encoding="utf-8", newline="").read()
    return p, json.loads(raw), "\r\n" in raw, raw


def dump(d, crlf):
    s = json.dumps(d, indent=1, ensure_ascii=False) + "\n"
    return s.replace("\n", "\r\n") if crlf else s


def hero_entry(n, old):
    forms = [{"name": fn, "aola": f"{n['id']}_{k + 1}", "size": sz} for k, (fn, sz) in enumerate(n["forms"])]
    return {
        "id": n["id"], "name": n["name"], "title": n["title"], "aola": forms[0]["aola"], "elem": old["elem"],
        "rarity": old["rarity"], "stats": list(old["stats"]), "skill": f"{n['id']}_skill", "ult": f"{n['id']}_ult",
        "passive": f"{n['id']}_pas", "shards": old["shards"], "line": n["line"], "size": forms[0]["size"], "forms": forms,
    }


def card_entry(src, new_id, owner, name, icon):
    c = copy.deepcopy(src)
    out = {}
    for k, v in c.items():  # giữ thứ tự khoá như thẻ gốc
        out[k] = v
    out["id"], out["owner"], out["name"], out["icon"] = new_id, owner, name, icon
    return out


def upsert(lst, entry, after_idx):
    """thay phần tử cùng id nếu có, không thì chèn sau after_idx; trả chỉ số của phần tử"""
    for i, x in enumerate(lst):
        if x.get("id") == entry["id"]:
            lst[i] = entry
            return i
    lst.insert(after_idx + 1, entry)
    return after_idx + 1


def patch_heroes(h, log):
    heroes = h["heroes"]
    by = {x["id"]: x for x in heroes}
    taken = {x["id"] for x in heroes} | {x["id"] for x in h.get("minions", [])}
    for n in NEW:
        old = by.get(n["old"])
        if old is None:
            raise SystemExit(f"thiếu tướng cũ {n['old']} trong heroes.json")
        if n["id"] in {x["id"] for x in h.get("minions", [])}:
            raise SystemExit(f"id {n['id']} trùng lính")
        e = hero_entry(n, old)
        cur = next((x for x in heroes if x["id"] == n["id"]), None)
        if cur == e:
            continue
        idx = heroes.index(old)
        upsert(heroes, e, idx)
        log.append(f"heroes: {'ghi đè' if cur else 'thêm'} {n['id']} ({n['name']}, chép {n['old']}: {old['rarity']}, {old['stats']}, "
                   f"{old['shards']} mảnh, {len(e['forms'])} dạng)")
    st = h["starters"]
    if STARTER_OLD in st and STARTER_NEW not in st:
        st[st.index(STARTER_OLD)] = STARTER_NEW
        log.append(f"starters: {STARTER_OLD} -> {STARTER_NEW}")
    elif STARTER_OLD in st:
        st.remove(STARTER_OLD)
        log.append(f"starters: bỏ {STARTER_OLD} (đã có {STARTER_NEW})")


def patch_cards(c, log):
    inn = c["innate"]
    for n in NEW:
        old_cards = [x for x in inn if x.get("owner") == n["old"]]
        by_kind = {x["kind"]: x for x in old_cards}
        if not all(k in by_kind for k in ("skill", "ult", "passive")):
            raise SystemExit(f"thiếu thẻ của {n['old']}")
        idx = max(inn.index(x) for x in old_cards)
        for kind, key, suf in (("skill", "skill", "skill"), ("ult", "ult", "ult"), ("passive", "pas", "pas")):
            name, icon = n[key]
            e = card_entry(by_kind[kind], f"{n['id']}_{suf}", n["id"], name, icon)
            cur = next((x for x in inn if x.get("id") == e["id"]), None)
            if cur != e:
                log.append(f"cards.innate: {'ghi đè' if cur else 'thêm'} {e['id']} \"{name}\" (chép {by_kind[kind]['id']})")
            idx = upsert(inn, e, idx)
    tr = c["traits"]
    for n in NEW:
        if "trait" not in n:
            continue
        old_id, name, icon = n["trait"]
        new_id = f"{n['id']}_boss"
        cur_i = next((i for i, x in enumerate(tr) if x.get("id") == new_id), None)
        old_i = next((i for i, x in enumerate(tr) if x.get("id") == old_id), None)
        if cur_i is not None:
            src = tr[old_i] if old_i is not None else tr[cur_i]
            e = card_entry(src, new_id, n["id"], name, icon)
            if tr[cur_i] != e:
                tr[cur_i] = e
                log.append(f"cards.traits: ghi đè {new_id}")
            if old_i is not None:
                del tr[old_i]
                log.append(f"cards.traits: bỏ {old_id} (đã có {new_id})")
        elif old_i is not None:
            tr[old_i] = card_entry(tr[old_i], new_id, n["id"], name, icon)
            log.append(f"cards.traits: {old_id} -> {new_id} \"{name}\" (cùng chỗ, chép số)")
        else:
            raise SystemExit(f"không có {old_id} lẫn {new_id} trong traits")


def patch_stages(s, log):
    trait_map = {n["trait"][0]: f"{n['id']}_boss" for n in NEW if "trait" in n}
    n_e = n_d = n_t = 0
    for st in s["stages"]:
        if st.get("zone") != "thuy":
            continue
        for e in st.get("enemies", []):
            if e.get("hero") in OLD2NEW:
                e["hero"] = OLD2NEW[e["hero"]]
                n_e += 1
            if e.get("trait") in trait_map:
                e["trait"] = trait_map[e["trait"]]
                n_t += 1
        for d in st.get("drops", []):
            for k in ("hero", "altHero"):
                if d.get(k) in OLD2NEW:
                    d[k] = OLD2NEW[d[k]]
                    n_d += 1
    if n_e or n_d or n_t:
        log.append(f"stages (đảo Thủy): đổi {n_e} địch, {n_d} mảnh rơi, {n_t} bị động boss")


def main():
    kiem = "--kiem" in sys.argv
    log = []
    out = []
    for name, fn in (("heroes.json", patch_heroes), ("cards.json", patch_cards), ("stages.json", patch_stages)):
        p, d, crlf, raw = load(name)
        fn(d, log)
        s = dump(d, crlf)
        if s != raw:
            out.append((p, s))
    for line in log:
        print(" ", line)
    if not out:
        print("không có gì phải đổi")
        return
    if kiem:
        print(f"--kiem: {len(out)} file sẽ đổi: " + ", ".join(os.path.basename(p) for p, _ in out))
        return
    for p, s in out:  # tính xong mọi chuỗi rồi mới mở file ghi
        with open(p, "w", encoding="utf-8", newline="") as f:
            f.write(s)
    print("đã ghi: " + ", ".join(os.path.basename(p) for p, _ in out))


if __name__ == "__main__":
    main()
