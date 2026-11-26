# Soát đủ bản dịch tiếng Anh ngoài Unity (gần như LocTests.DuBanDich_ChuoiTrongCode + tên, mô tả gói trong balance.json).
#   py -3 -I kiem_dich.py [--nhap <thư mục nháp có App/, Game/, Core/, Loc/en, "02 Data/Json">]
import os, re, sys, json

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
A = os.path.join(PROJ, "Assets")
args = sys.argv[1:]
nhap = os.path.abspath(args[args.index("--nhap") + 1]) if "--nhap" in args else None


def pick(rel_nhap, rel_assets):
    p = os.path.join(nhap, rel_nhap) if nhap else None
    return p if p and os.path.exists(p) else os.path.join(A, rel_assets)


table = {}
for n in ("ui", "names", "cards"):
    table.update(json.loads(open(pick(os.path.join("Loc", "en", n + ".json"), os.path.join("Resources", "Loc", "en", n + ".json")), encoding="utf-8").read()))
VI = re.compile("[àáảãạăằắẳẵặâầấẩẫậđèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵ]", re.I)


def need(s):
    return bool(s) and bool(VI.search(s)) and s not in table and s.strip() not in table


call = re.compile(r'Loc\.(?:T|F)\(\s*"((?:[^"\\]|\\.)*)"')
miss = []
root = os.path.join(A, "01 Script")
for dp, _, fs in os.walk(root):
    for f in fs:
        if not f.endswith(".cs"):
            continue
        rel = os.path.relpath(os.path.join(dp, f), root).replace("\\", "/")
        if rel.startswith(("Editor/", "Tests/", "BanThu/")):
            continue
        src = open(pick(rel, os.path.join("01 Script", rel)), encoding="utf-8-sig").read()
        for m in call.finditer(src):
            s = m.group(1).encode("utf-8").decode("unicode_escape").encode("latin-1").decode("utf-8") if "\\" in m.group(1) else m.group(1)
            if need(s):
                miss.append((rel, s))
b = json.loads(open(pick(os.path.join("02 Data", "Json", "balance.json"), os.path.join("02 Data", "Json", "balance.json")), encoding="utf-8-sig").read())
for p in b.get("ads", {}).get("products", []) + b.get("shop", {}).get("packs", []):
    for k in ("name", "desc"):
        if need(p.get(k, "")):
            miss.append(("gói " + p["id"], p[k]))
for o in b.get("shop", {}).get("offers", []) + b.get("shop", {}).get("cards", []) + b.get("shop", {}).get("chains", []) + b.get("shop", {}).get("eggs", []):
    if need(o.get("name", "")):
        miss.append(("cửa hàng", o["name"]))
print(len(miss), "chuỗi chưa dịch")
for w, s in miss[:40]:
    print(" ", w, ":", s[:140])
