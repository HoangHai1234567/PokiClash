# Bản dịch tiếng Anh cho chuỗi mới của lều Vòng Xoay có Lão Mực (D4). Chỉ THÊM khoá chưa có vào Assets/Resources/Loc/en/ui.json
# (đọc file mới nhất ngay lúc ghi: nhiều phiên cùng thêm khoá), giữ BOM / xuống dòng / thứ tự sắp xếp.
# Chạy: py -3 -I loc_d4.py [--thieu]   (--thieu: chỉ in chuỗi Loc.T / Loc.F của RouletteScene.cs còn thiếu bản dịch)
import json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
UI = os.path.join(PROJ, "Assets", "Resources", "Loc", "en", "ui.json")
SRC = os.path.join(PROJ, "Assets", "01 Script", "App", "Scenes", "Casino", "RouletteScene.cs")
if not os.path.isfile(SRC) or "RouletteBall" not in open(SRC, encoding="utf-8").read():
    SRC = os.path.join(HERE, "ma", "RouletteScene.cs")

ADD = {
    "Mọi cửa hoàn trả {0}%.": "Every bet returns {0}%.",
    "Hoàn trả từ {0}% tới {1}% tuỳ cửa.": "Returns range from {0}% to {1}% depending on the bet.",
    "Bánh xe có 26 ô: 5 hệ, mỗi hệ số 1 tới 5, và một ô Sao Vàng. Đặt chip lên bảng cược rồi bấm Quay; viên bi nằm ở ô nào thì cửa trúng ô đó thắng.":
        "The wheel has 26 pockets: 5 elements, each numbered 1 to 5, plus one Gold Star pocket. Place chips on the layout and tap Spin; bets that cover the pocket where the ball rests win.",
    "Hệ (cột đầu): trúng một trong 5 ô của hệ, trả {0}:1. Số (hàng đầu): trúng một trong 5 ô cùng số, trả {1}:1. Ô đơn: trả {2}:1. Sao Vàng: trả {3}:1, cược từ bậc {4} được thêm mảnh tướng khách mời.":
        "Element (first column): any of that element's 5 pockets, pays {0}:1. Number (top row): any of the 5 pockets with that number, pays {1}:1. Single pocket: pays {2}:1. Gold Star: pays {3}:1, and from bet tier {4} also gives guest hero shards.",
    "Tối đa {0} chip mỗi vòng.": "Up to {0} chips per spin.",
    "Vòng đầu ta khao, trượt không mất gì.": "First spin's on me. Miss and it costs you nothing.",
    "Hôm nay hết vòng có thưởng rồi, quay tập cho vui nhé.": "No more prize spins today. Take a practice spin for fun.",
    "Đặt chip vào hệ, vào số, hay liều một ô. Bi dừng đâu, ta trả đó.": "Bet on an element, a number, or risk a single pocket. Where the ball stops, I pay.",
    "Sao Vàng? Gan đấy.": "Gold Star? Bold.",
    "Hết đặt!": "No more bets!",
    "Vòng miễn phí!": "Free spin!",
    "Vòng tập": "Practice spin",
    "Bánh xe đang quay...": "The wheel is spinning...",
    "trượt (vòng tập)": "miss (practice)",
    "trượt, không mất gì": "miss, nothing lost",
    "trượt · −{0} bi": "miss · −{0} balls",
    "trúng {0} cửa (vòng tập)": "{0} bets hit (practice)",
    "trúng {0} cửa · {1} bi": "{0} bets hit · {1} balls",
    "{0}!": "{0}!",
    "Cái gì?! Trúng to thế!": "What?! That big a win!",
    "Vòng sau ta gỡ.": "I'll win it back next spin.",
    "Ba vòng liền?! Xui xẻo!": "Three spins in a row?! Rotten luck!",
    "Trượt rồi. May cho khách là chưa mất gì.": "A miss. Lucky for you, nothing lost.",
    "+{0} bi": "+{0} balls",
    "Chạm ô trên bảng cược để đặt chip": "Tap a spot on the layout to place a chip",
    "Chip {0}/{1} · mỗi chip {2} bi": "Chips {0}/{1} · {2} balls each",
    "vòng tập": "practice",
    "Quay": "Spin",
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
