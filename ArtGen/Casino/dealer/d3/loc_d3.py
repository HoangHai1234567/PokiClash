# Bản dịch tiếng Anh cho chuỗi mới của lều Đêm Bài có Lão Mực (D3): câu thoại của dealer, nhãn chip. Chỉ THÊM khoá chưa có vào
# Assets/Resources/Loc/en/ui.json (đọc file mới nhất ngay lúc ghi: nhiều phiên cùng thêm khoá), giữ BOM / xuống dòng / thứ tự sắp xếp.
# Chạy: py -3 -I loc_d3.py [--thieu]   (--thieu: chỉ in chuỗi Loc.T / Loc.F của BlackjackScene.cs còn thiếu bản dịch)
import json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
UI = os.path.join(PROJ, "Assets", "Resources", "Loc", "en", "ui.json")
SRC = os.path.join(PROJ, "Assets", "01 Script", "App", "Scenes", "Casino", "BlackjackScene.cs")

ADD = {
    "Ván đầu ta khao, thua không mất gì.": "First hand's on me. Lose and it costs you nothing.",
    "Hôm nay hết ván có thưởng rồi, chơi tập cho vui nhé.": "No more prize hands today. Play a practice one for fun.",
    "Chào khách! Chọn mức cược rồi bấm Chia bài.": "Welcome, traveller! Pick a bet, then tap Deal.",
    "Quá 21 rồi, khè khè!": "Over 21! Heh heh!",
    "Hừm...": "Hmm...",
    "Hừ... quá 21.": "Hmph... over 21.",
    "Ha! Blackjack của ta!": "Ha! Blackjack for me!",
    "Hừm... chưa có gì.": "Hmm... nothing yet.",
    "Blackjack?! Hên thôi!": "Blackjack?! Pure luck!",
    "Hừ... hên thôi!": "Hmph... just luck!",
    "Ván sau ta gỡ.": "I'll win it back next hand.",
    "Chà, khá đấy.": "Well, not bad.",
    "Ba ván liền?! Xui xẻo!": "Three in a row?! Rotten luck!",
    "Hoà. Chẳng ai mất gì.": "A push. Nobody loses.",
    "Khè khè, của ta hết!": "Heh heh, it's all mine!",
    "Lần sau nhé, khách.": "Better luck next time, traveller.",
    "Bàn này ta làm chủ mà.": "This is my table, after all.",
    "Hôm nay thế đủ rồi. Mai ghé, ta còn khối chiêu.": "That's enough for today. Come back tomorrow, I've got more tricks.",
    "Chơi lớn hả?": "Playing big, eh?",
    "{0} bi": "{0} marbles",
    "miễn phí": "free",
    "Xào bài nào!": "Shuffle time!",
    "Tách thì tách!": "Split it is!",
    "{0} điểm + ?": "{0} points + ?",
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
