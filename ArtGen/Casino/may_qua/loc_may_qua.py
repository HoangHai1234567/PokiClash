# Bản dịch tiếng Anh cho chuỗi mới của lều Hội Máy Quả (câu thoại của Lão Mực bên máy quả). Chỉ THÊM khoá chưa có vào
# Assets/Resources/Loc/en/ui.json (đọc file mới nhất ngay lúc ghi: nhiều phiên cùng thêm khoá), giữ BOM / xuống dòng / thứ tự sắp xếp.
# Chạy: py -3 -I loc_may_qua.py [--thieu] [đường dẫn SlotScene.cs]   (--thieu: chỉ in chuỗi Loc.T / Loc.F còn thiếu bản dịch)
import json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
UI = os.path.join(PROJ, "Assets", "Resources", "Loc", "en", "ui.json")
SRC = next((a for a in sys.argv[1:] if a.endswith(".cs")), os.path.join(PROJ, "Assets", "01 Script", "App", "Scenes", "Casino", "SlotScene.cs"))

ADD = {
    "Lượt đầu ta khao, trượt không mất gì.": "First spin's on me. Miss and it costs you nothing.",
    "Hôm nay hết lượt có thưởng rồi, quay tập cho vui nhé.": "No more prize spins today. Take a practice spin for fun.",
    "Ba hình giống nhau trên một đường là trúng. Cái máy này thật thà hơn ta đấy.": "Three of a kind on a line wins. This machine is more honest than I am.",
    "Trời đất, nổ hũ rồi!": "Good grief, a jackpot!",
    "Cái máy phản chủ này!": "You traitor of a machine!",
    "Khè khè, lần sau nhé.": "Heh heh, next time.",
    "Máy đói rồi, cho nó ăn tiếp đi.": "The machine's hungry. Feed it again.",
    "Hừ... hên thôi!": "Hmph... just luck!",
    "Chà, khá đấy.": "Well, not bad.",
    "Hôm nay thế đủ rồi. Mai ghé, ta còn khối chiêu.": "That's enough for today. Come back tomorrow, I've got more tricks.",
}


def missing():
    s = open(SRC, encoding="utf-8").read()
    keys = set(re.findall(r'Loc\.[TF]\("((?:[^"\\]|\\.)*)"', s))
    d = json.loads(open(UI, "rb").read().decode("utf-8-sig"))
    return sorted(k for k in keys if k not in d and k not in ADD)


def merge():
    raw = open(UI, "rb").read()
    bom = raw.startswith(b"\xef\xbb\xbf")
    t = raw.decode("utf-8-sig")
    crlf = "\r\n" in t
    d = json.loads(t)
    was_sorted = list(d.keys()) == sorted(d.keys())
    n = 0
    for k, v in ADD.items():
        if k not in d:
            d[k] = v
            n += 1
    if was_sorted:
        d = dict(sorted(d.items()))
    out = json.dumps(d, ensure_ascii=False, indent=1) + "\n"
    if crlf:
        out = out.replace("\n", "\r\n")
    with open(UI, "w", encoding="utf-8-sig" if bom else "utf-8", newline="") as f:
        f.write(out)
    print("ui.json +", n, "khoá")


if __name__ == "__main__":
    left = missing()
    if left:
        print("Còn thiếu bản dịch (thêm vào ADD):")
        for k in left:
            print(" ", repr(k))
    if "--thieu" not in sys.argv:
        merge()
