# Sinh khối "casino" cho balance.json (GD_Claude/29_DaoCasino.md). Ghi ra casino_block.json; --apply <balance.json> chèn / thay khối.
import json, sys, os, random

sys.stdout.reconfigure(encoding="utf-8")
PROJ = r"C:\Atomik\PokiWar"
heroes = json.load(open(os.path.join(PROJ, "Assets", "02 Data", "Json", "heroes.json"), encoding="utf-8"))["heroes"]
H = {h["id"]: h for h in heroes}
RAR = ["common", "uncommon", "rare", "epic", "legend"]
ELEMS = ["kim", "moc", "thuy", "hoa", "tho"]


def by(elem=None, rars=None):
    return sorted([h["id"] for h in heroes if (elem is None or h["elem"] == elem) and (rars is None or h["rarity"] in rars)])


# ---------- cá: 6 loài mỗi hệ (2 Thường, 1 Khá, 1 Hiếm, 1 Sử thi, 1 Huyền thoại) ----------
FISH = {
    "thuy": [("ca_moi_bac", "Cá Mòi Bạc", 0, False, 8, 20), ("ca_bong_song", "Cá Bống Sông", 0, False, 6, 15), ("ca_chep_lam", "Cá Chép Lam", 1, False, 25, 60),
             ("ca_noc_bong", "Cá Nóc Bong Bóng", 2, True, 15, 35), ("ca_duoi_song", "Cá Đuối Sóng", 3, False, 60, 140), ("ca_voi_ngoc", "Cá Voi Ngọc", 4, True, 150, 320)],
    "hoa": [("ca_ro_lua", "Cá Rô Lửa", 0, False, 8, 18), ("ca_kim_than", "Cá Kìm Than", 0, True, 12, 28), ("ca_mu_dung_nham", "Cá Mú Dung Nham", 1, False, 30, 70),
            ("ca_thoi_lua", "Cá Thổi Lửa", 2, True, 20, 45), ("ca_kiem_hoa", "Cá Kiếm Hỏa", 3, False, 80, 180), ("phuong_ngu", "Phượng Ngư", 4, False, 90, 200)],
    "kim": [("ca_thiec", "Cá Thiếc", 0, False, 7, 16), ("ca_bon_sat", "Cá Bơn Sắt", 0, False, 15, 35), ("ca_hop_dong", "Cá Hộp Đồng", 1, False, 12, 30),
            ("ca_ngua_banh_rang", "Cá Ngựa Bánh Răng", 2, False, 10, 25), ("ca_map_thep", "Cá Mập Thép", 3, True, 120, 260), ("ca_rong_vang", "Cá Rồng Vàng", 4, False, 70, 150)],
    "moc": [("ca_la_tre", "Cá Lá Tre", 0, False, 6, 14), ("ca_reu", "Cá Rêu", 0, False, 9, 22), ("ca_tre_re", "Cá Trê Rễ Cây", 1, True, 30, 75),
            ("ca_hoa_sen", "Cá Hoa Sen", 2, False, 18, 40), ("ca_tam_co_thu", "Cá Tầm Cổ Thụ", 3, False, 100, 220), ("ca_linh_chi", "Cá Linh Chi", 4, True, 40, 90)],
    "tho": [("ca_soi", "Cá Sỏi", 0, False, 6, 15), ("ca_loc_bun", "Cá Lóc Bùn", 0, False, 20, 50), ("ca_da_hoa_cuong", "Cá Đá Hoa Cương", 1, False, 25, 55),
            ("ca_hoa_thach", "Cá Hóa Thạch", 2, True, 30, 70), ("ca_nganh_nui", "Cá Ngạnh Núi", 3, False, 70, 160), ("ca_ky_lan_dat", "Cá Kỳ Lân Đất", 4, False, 120, 250)],
}
KINGS = [("vua_thuy", "Thủy Quái Râu Dài", "thuy", 300, 600), ("vua_hoa", "Hỏa Ngư Vương", "hoa", 250, 500), ("vua_kim", "Kim Giáp Ngư Vương", "kim", 280, 560),
         ("vua_moc", "Mộc Lão Ngư", "moc", 260, 520), ("vua_tho", "Thạch Ngư Vương", "tho", 320, 640)]

fish = []
for e in ELEMS:
    for fid, name, r, night, mn, mx in FISH[e]:
        fish.append({"id": fid, "name": name, "elem": e, "rar": RAR[r], "night": night, "min": mn, "max": mx})
kings = [{"id": k, "name": n, "elem": e, "rar": "legend", "min": a, "max": b} for k, n, e, a, b in KINGS]


# ---------- đấu trường ngầm: 14 ngày (chỉ số 0 = thứ Hai 2026-11-23), 5 bậc; chủ nhật (6, 13) thêm Nhà Vô Địch ----------
STAR_AT = [5, 10, 16, 24, 35, 60, 85, 108, 125, 140, 155, 170, 185, 198, 200]


def star_at(level):
    return 1 + sum(1 for x in STAR_AT if x <= level)


TIER_LV = [40, 56, 84, 114, 145]
CHAMP_LV = 165
TIER_STAR = [2, 1, 0, 0, 0]
TIER_CARD = [4, 4, 4, 5, 5]
TIER_WORD = ["tân binh", "đấu sĩ", "cựu binh", "thủ lĩnh", "huyền thoại"]
THEME = {"kim": "Xưởng Thép", "moc": "Rừng Gai", "thuy": "Sóng Ngầm", "hoa": "Lò Lửa", "tho": "Mỏ Đá"}
TEAM_RARS = [["common", "uncommon"], ["uncommon", "rare"], ["uncommon", "rare", "epic"], ["rare", "epic"], ["epic", "legend"]]
TEAM_SIZE = [1, 2, 3, 3, 3]
RULES = [("atk", True, 0.2, 0), ("hp", False, 0.3, 0), ("picks", False, 0, 4), ("buff", False, 0.15, 0), ("def", True, 0.25, 0), ("solo", False, 0, 0), (None, False, 0, 0)]


def rank(hid):
    return (RAR.index(H[hid]["rarity"]), hid)


def team_for(elem, tier, rnd, mixed):
    size = TEAM_SIZE[tier]
    pool = by(None if mixed else elem, TEAM_RARS[tier])
    if len(pool) < size:
        pool = by(None if mixed else elem)
    pick = rnd.sample(pool, size)
    pick.sort(key=rank, reverse=True)  # tướng mạnh nhất đứng đầu (chủ lực, cũng là tướng khi luật solo)
    lv = TIER_LV[tier]
    st = min(20, star_at(lv) + TIER_STAR[tier])
    card = TIER_CARD[tier]
    return [{"hero": h, "level": lv, "star": st, "card": card} for h in pick]


rotation = []
week_elems = ["kim", "moc", "thuy", "hoa", "tho", None, None]
for d in range(14):
    rnd = random.Random(1000 + d)
    elem = week_elems[d % 7]
    mixed = elem is None
    theme_elem = elem or rnd.choice(ELEMS)
    entries = []
    for t in range(5):
        kind, has_elem, p, n = RULES[(d + t * 3) % len(RULES)]
        rule = {}
        if kind:
            rule = {"kind": kind}
            if has_elem:
                rule["elem"] = theme_elem
            if p:
                rule["p"] = p
            if n:
                rule["n"] = n
        team = team_for(theme_elem, t, rnd, mixed)
        name = ("Liên Minh" if mixed else THEME[elem]) + ": " + TIER_WORD[t]
        e = {"name": name, "rule": rule, "team": team, "lead": team[0]["hero"]}
        entries.append(e)
    if d % 7 == 6:  # chủ nhật: Nhà Vô Địch, đội mạnh nhất nhiều hệ
        champs = rnd.sample(by(None, ["legend"]), 1) + rnd.sample(by(None, ["epic"]), 2)
        champs.sort(key=rank, reverse=True)
        st = min(20, star_at(CHAMP_LV))
        entries.append({"name": "Nhà Vô Địch: " + H[champs[0]]["name"], "rule": {"kind": "buff", "p": 0.1},
                        "team": [{"hero": h, "level": CHAMP_LV, "star": st, "card": 5} for h in champs], "lead": champs[0]})
    rotation.append({"entries": entries})

# cấp, sao từng đội đã cân bằng máy tự đánh (runner ugcal → ug_levels.json)
_cal = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ug_levels.json")
if os.path.exists(_cal):
    cal = json.load(open(_cal, encoding="utf-8"))
    for d, day in enumerate(rotation):
        for k, e in enumerate(day["entries"]):
            if d < len(cal) and k < len(cal[d]):
                lv, st = cal[d][k]
                for m in e["team"]:
                    m["level"], m["star"] = lv, st

block = {
    "openLevel": 8,
    "anchor": "2026-11-23",
    "unlocks": [
        {"id": "fishing", "level": 8}, {"id": "inn", "level": 8}, {"id": "race", "level": 15, "heroes": 4},
        {"id": "booths", "level": 20}, {"id": "market", "level": 25}, {"id": "underground", "level": 35},
    ],
    "events": [
        {"id": "dem_bai", "name": "Đêm Bài", "booth": "blackjack", "period": 14, "offset": 0, "length": 3},
        {"id": "vong_xoay", "name": "Vòng Xoay Ngũ Hành", "booth": "roulette", "period": 14, "offset": 4, "length": 3},
        {"id": "hoi_may_qua", "name": "Hội Máy Quả", "booth": "slot", "period": 14, "offset": 8, "length": 3},
        {"id": "le_hoi_dua", "name": "Lễ Hội Đua", "booth": "race_fest", "period": 14, "offset": 11, "length": 3, "mult": 1.5},
    ],
    "blackjack": {
        "bets": [5, 10, 20, 40], "betLevel": [20, 20, 45, 70], "daily": 30, "jarBets": 30, "bjPays": 1.5,
        "jar": [[{"k": "balls", "n": 6}], [{"k": "balls", "n": 8}, {"k": "copies", "n": 1, "h": "*carry"}],
                [{"k": "shards", "n": 2, "h": "*guest"}, {"k": "balls", "n": 10}], [{"k": "shards", "n": 3, "h": "*guest"}, {"k": "evo", "n": 1, "chance": 0.2}]],
    },
    "roulette": {
        "bets": [5, 10, 20, 40], "betLevel": [20, 20, 45, 70], "daily": 30, "jarBets": 90, "chips": 5,
        "elemPays": 4, "numPays": 4, "singlePays": 24, "starPays": 24, "starTier": 2, "starShards": 2,
        "jar": [[{"k": "balls", "n": 18}], [{"k": "balls", "n": 24}, {"k": "copies", "n": 2, "h": "*carry"}],
                [{"k": "shards", "n": 5, "h": "*guest"}, {"k": "balls", "n": 30}], [{"k": "shards", "n": 8, "h": "*guest"}, {"k": "evo", "n": 1, "chance": 0.5}]],
    },
    "slots": {
        "bets": [5, 10, 20, 40], "betLevel": [20, 20, 45, 70], "daily": 50, "jarBets": 40,
        "reels": [[0, 1, 0, 4, 8, 7, 5, 3, 1, 6, 7, 4, 1, 2, 8, 5, 3, 5, 0, 2, 4, 2, 3],
                  [4, 2, 3, 4, 0, 8, 2, 3, 4, 1, 5, 8, 1, 5, 7, 2, 0, 6, 7, 0, 5, 1, 3],
                  [1, 3, 5, 0, 3, 7, 2, 3, 8, 4, 7, 1, 6, 5, 0, 2, 8, 4, 1, 5, 4, 0, 2]],
        "pays": [{"sym": 0, "pays": 8}, {"sym": 1, "pays": 8}, {"sym": 2, "pays": 8}, {"sym": 3, "pays": 8}, {"sym": 4, "pays": 8},
                 {"sym": 5, "pays": 15}, {"sym": 6, "pays": 80}],
        "wildPays": 100, "scatter2": 1, "freeSpins": 5, "badgeShards": [1, 1, 2, 3],
        "jar": [[{"k": "balls", "n": 8}], [{"k": "balls", "n": 10}, {"k": "copies", "n": 1, "h": "*carry"}],
                [{"k": "shards", "n": 2, "h": "*guest"}, {"k": "balls", "n": 12}], [{"k": "shards", "n": 4, "h": "*guest"}, {"k": "evo", "n": 1, "chance": 0.25}]],
    },
    "race": {
        "seg": 60, "segs": 3, "spdBase": 10, "spdK": 0.004, "spdMid": 60, "starK": 0.002, "lvK": 0.001, "lvClamp": 40,
        "same": 1.06, "weak": 0.96, "noise": 0.08, "cheer": [0, 0.06, 0.09], "cheerSec": 1.5, "lucky": 0.03,
        "daily": 20, "minRunners": 3, "maxRunners": 5, "fightRate": 0.55, "fightRange": 9, "fightCool": 2.6, "hitChance": 0.72,
        "stunSec": 1.3, "trip": 0.6, "guardSec": 0.9, "gustRate": 0.25, "gust": 0.3, "gustSec": 1.0,
        "placeK": [0.55, 0.3, 0.1, 0, 0], "points": [3, 2, 1, 0, 0], "weekPts": 10,
        "cups": [
            {"name": "Cúp Đồng", "level": 15, "oppLevel": 15, "oppStar": 2, "fee": 15, "skill": 0.45, "week": [{"k": "balls", "n": 120}, {"k": "stones", "n": 3}]},
            {"name": "Cúp Bạc", "level": 40, "oppLevel": 45, "oppStar": 5, "fee": 25, "skill": 0.55, "week": [{"k": "balls", "n": 200}, {"k": "shards", "n": 3, "h": "*carry"}]},
            {"name": "Cúp Vàng", "level": 70, "oppLevel": 80, "oppStar": 7, "fee": 40, "skill": 0.65, "week": [{"k": "balls", "n": 300}, {"k": "evo", "n": 1}]},
            {"name": "Cúp Kim Cương", "level": 100, "oppLevel": 110, "oppStar": 10, "fee": 60, "skill": 0.7, "week": [{"k": "shards", "n": 6, "h": "*carry"}, {"k": "evo", "n": 1}]},
            {"name": "Cúp Huyền Thoại", "level": 140, "oppLevel": 150, "oppStar": 12, "fee": 80, "skill": 0.75, "week": [{"k": "shards", "n": 10, "h": "*carry"}, {"k": "evo", "n": 2}, {"k": "crystal", "n": 1}]},
        ],
    },
    "fishing": {
        "freeBait": 10, "baitPack": 5, "baitPrice": 30, "farBonus": 1, "biteWindow": 0.6,
        "pull": [1, 1.5, 2.2, 3, 4], "first": [10, 15, 25, 50, 100], "price": [3, 6, 12, 30, 80], "setShards": 5,
        "kingChance": 0.15, "kingAssist": 0.25, "kingRod": 3,
        "rods": [{"cost": 0, "zone": 0.30, "spots": 1}, {"cost": 300, "zone": 0.33, "spots": 2}, {"cost": 900, "zone": 0.36, "spots": 2},
                 {"cost": 2000, "zone": 0.40, "spots": 3}, {"cost": 4000, "zone": 0.44, "spots": 3}],
        "spots": [{"name": "Gần bờ", "rar": [70, 25, 5, 0, 0]}, {"name": "Xa bờ", "rar": [35, 35, 22, 7, 1]}, {"name": "Rạn đá", "rar": [10, 25, 30, 25, 10]}],
        "fish": fish, "kings": kings,
        "king": [{"k": "shards", "n": 5, "h": "*elem"}, {"k": "evo", "n": 1}, {"k": "balls", "n": 150}],
    },
    "market": {
        "slots": 6, "nightSlots": 2, "periods": [0, 8, 16], "refresh": [20, 40, 80, 120, 160], "copySell": 6,
        "offers": [
            {"kind": "shards", "n": 5, "w": 30, "mark": 1.45, "rar": "uncommon"},
            {"kind": "copies", "n": 3, "w": 15, "mark": 1.4},
            {"kind": "stones", "n": 4, "w": 15, "mark": 1.5},
            {"kind": "evo", "n": 1, "w": 8, "mark": 1.8},
            {"kind": "crystal", "n": 1, "w": 8, "mark": 1.8},
            {"kind": "bait", "n": 5, "w": 12, "price": 30},
            {"kind": "mystery", "w": 12, "price": 120},
            {"kind": "shards", "n": 5, "w": 10, "mark": 1.6, "rar": "epic", "night": True},
            {"kind": "evo", "n": 2, "w": 5, "mark": 1.7, "night": True},
        ],
        "mystery": [{"w": 45, "k": "balls", "min": 60, "max": 140}, {"w": 25, "k": "stones", "min": 2, "max": 4}, {"w": 5, "k": "evo", "min": 1, "max": 1},
                    {"w": 20, "k": "shards", "min": 3, "max": 5}, {"w": 5, "k": "egg", "min": 1, "max": 1, "tier": 0}],
    },
    "underground": {
        "winMult": 2.5, "rewinMult": 1, "rewin": [{"k": "stones", "n": 1}],
        "tiers": [
            {"name": "Đá", "level": 35, "fee": 20, "shards": 1},
            {"name": "Đồng", "level": 50, "fee": 40, "shards": 2},
            {"name": "Bạc", "level": 80, "fee": 80, "shards": 3, "items": [{"k": "stones", "n": 2}]},
            {"name": "Vàng", "level": 110, "fee": 150, "shards": 5, "items": [{"k": "evo", "n": 1}]},
            {"name": "Huyền Thoại", "level": 140, "fee": 250, "shards": 8, "items": [{"k": "evo", "n": 1}, {"k": "crystal", "n": 1}]},
            {"name": "Nhà Vô Địch", "level": 160, "fee": 300, "shards": 10, "weekly": True, "items": [{"k": "evo", "n": 2}, {"k": "crystal", "n": 2}]},
        ],
        "rotation": rotation,
        "dates": [],
    },
    "inn": {
        "count": 3,
        "quests": [
            {"id": "fish5", "kind": "fish", "n": 5, "text": "Câu {0} con cá", "need": "fishing", "items": [{"k": "balls", "n": 30}]},
            {"id": "fish_rare", "kind": "fish_rare", "n": 1, "text": "Câu {0} con cá Hiếm trở lên", "need": "fishing", "items": [{"k": "bait", "n": 3}, {"k": "balls", "n": 30}]},
            {"id": "drop30", "kind": "drop", "n": 30, "text": "Thả {0} bi ở Tháp Máy Bi", "items": [{"k": "balls", "n": 30}]},
            {"id": "race2", "kind": "race", "n": 2, "text": "Đua {0} lần", "need": "race", "items": [{"k": "balls", "n": 40}]},
            {"id": "race_top3", "kind": "race_top3", "n": 1, "text": "Về top 3 {0} lần ở Trường đua", "need": "race", "items": [{"k": "stones", "n": 2}]},
            {"id": "table10", "kind": "table", "n": 10, "text": "Chơi {0} ván ở lều lữ khách", "need": "booths", "items": [{"k": "balls", "n": 40}]},
            {"id": "market1", "kind": "market_buy", "n": 1, "text": "Mua {0} món ở Chợ đen", "need": "market", "items": [{"k": "balls", "n": 30}]},
            {"id": "ug1", "kind": "ug_win", "n": 1, "text": "Thắng {0} trận ở Hầm đấu", "need": "underground", "items": [{"k": "stones", "n": 2}, {"k": "balls", "n": 40}]},
        ],
        "all": [{"k": "bait", "n": 5}, {"k": "balls", "n": 60}],
    },
}


def dump(v, ind=1, lvl=0):
    """Kiểu balance.json: thụt 1 dấu cách; object / mảng ngắn viết một dòng."""
    one = json.dumps(v, ensure_ascii=False, separators=(", ", ": "))
    if len(one) + (lvl + 1) * ind <= 150 or not isinstance(v, (dict, list)):
        return one
    pad = " " * (ind * (lvl + 1))
    end = " " * (ind * lvl)
    if isinstance(v, dict):
        items = [pad + json.dumps(k, ensure_ascii=False) + ": " + dump(x, ind, lvl + 1) for k, x in v.items()]
        return "{\n" + ",\n".join(items) + "\n" + end + "}"
    items = [pad + dump(x, ind, lvl + 1) for x in v]
    return "[\n" + ",\n".join(items) + "\n" + end + "]"


def apply(path):
    raw = open(path, "rb").read()
    bom = raw.startswith(b"\xef\xbb\xbf")
    t = raw.decode("utf-8-sig")
    crlf = "\r\n" in t
    t = t.replace("\r\n", "\n")
    data = json.loads(t)
    text = ' "casino": ' + dump(block, 1, 1)
    if "casino" in data:
        # thay khối cũ: tìm dòng ' "casino": ' tới hết file trừ dấu } cuối
        i = t.index('\n "casino": ')
        t = t[:i] + "\n" + text + "\n}\n"
    else:
        j = t.rstrip().rindex("}")
        body = t[:j].rstrip()
        t = body + ",\n" + text + "\n}\n"
    json.loads(t)  # kiểm hợp lệ
    if crlf:
        t = t.replace("\n", "\r\n")
    with open(path, "w", encoding="utf-8-sig" if bom else "utf-8", newline="") as f:
        f.write(t)
    print("da ghi", path)


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "casino_block.json"), "w", encoding="utf-8") as f:
        f.write(dump(block))
    if len(sys.argv) > 2 and sys.argv[1] == "--apply":
        apply(sys.argv[2])
    print("ca", len(fish), "vua", len(kings), "ngay ngam", len(rotation), "doi", sum(len(r["entries"]) for r in rotation))
