# Liệt kê chuỗi chưa dịch của phần Casino (code: Loc.T / Loc.F; dữ liệu: tên trong khối casino). Dùng: loc_missing.py [file.cs ...]
import re, json, glob, sys, os
sys.stdout.reconfigure(encoding="utf-8")
PROJ = r"C:\Atomik\PokiWar"
en = {}
for f in glob.glob(os.path.join(PROJ, "Assets", "Resources", "Loc", "en", "*.json")):
    en.update(json.load(open(f, encoding="utf-8-sig")))
call = re.compile(r'Loc\.(?:T|F)\(\s*"((?:[^"\\]|\\.)*)"')
files = sys.argv[1:] or (glob.glob(os.path.join(PROJ, "Assets", "01 Script", "Core", "Casino*.cs")) + glob.glob(os.path.join(PROJ, "Assets", "01 Script", "Core", "Casino", "*.cs")))
code = []
for f in files:
    for m in call.finditer(open(f, encoding="utf-8").read()):
        s = m.group(1).encode("utf-8").decode("unicode_escape").encode("latin-1").decode("utf-8") if "\\" in m.group(1) else m.group(1)
        if s not in en and s not in code:
            code.append(s)
data = []
if not sys.argv[1:]:
    b = json.load(open(os.path.join(PROJ, "Assets", "02 Data", "Json", "balance.json"), encoding="utf-8-sig"))["casino"]

    def add(s):
        if s and s not in en and s not in data and s not in code:
            data.append(s)

    for e in b["events"]: add(e["name"])
    for c in b["race"]["cups"]: add(c["name"])
    for f in b["fishing"]["fish"] + b["fishing"]["kings"]: add(f["name"])
    for s in b["fishing"]["spots"]: add(s["name"])
    for t in b["underground"]["tiers"]: add(t["name"])
    for d in b["underground"]["rotation"]:
        for e in d["entries"]: add(e["name"])
    for q in b["inn"]["quests"]: add(q["text"])
print(json.dumps({"code": code, "data": data}, ensure_ascii=False, indent=1))
