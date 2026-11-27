# Thêm bản dịch tiếng Anh cho chữ mới của màn Hang Tiềm Năng bản sân khấu (2026-11-27) vào Assets/Resources/Loc/en/ui.json.
# Chỉ thêm khoá chưa có (file dùng chung nhiều phiên: đọc bản mới nhất ngay lúc ghi, giữ khoá cũ và thứ tự).
# Chạy: py -3 -I loc_hang.py
import json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.environ.get("POKI_PROJ") or os.path.abspath(os.path.join(HERE, "..", ".."))
UI = os.path.join(PROJ, "Assets", "Resources", "Loc", "en", "ui.json")

ADD = {
    "Boss hệ {0}": "{0} boss",
    "Cuối tuần: chọn hệ boss": "Weekend: pick the boss element",
    "Tầng {0} · {1}": "Floor {0} · {1}",
    "Đã qua": "Cleared",
    "Qua tầng {0} để mở": "Clear floor {0} to unlock",
    "Lượt {0}/{1}": "Wins {0}/{1}",
    "Hết lượt": "No wins left",
    "Chọn hệ": "Pick element",
    "cuối tuần": "weekend",
    "Boss hệ {0}: {1} (cuối tuần tự chọn)": "{0} boss: {1} (you pick on weekends)",
    "; {0} tự chọn": "; {0} your pick",
    "{0}: {1}, cấp {2}": "{0}: {1}, level {2}",
    "Boss": "Boss",
    "Phụ": "Ally",
    "Cuối tuần: chọn hệ boss ở hàng dưới.": "Weekend: pick the boss element in the row below.",
    "Chưa mở: qua tầng {0} trước.": "Locked: clear floor {0} first.",
    "Cấp đề nghị {0} (bạn cấp {1})": "Recommended level {0} (you are level {1})",
    "Lần đầu qua: {0} (không cần lượt)": "First clear: {0} (no win needed)",
    "Đã qua lần đầu.": "First clear done.",
    "Mỗi trận thắng: +{0} đá tiềm năng": "Each win: +{0} potential stones",
    ", trận thắng đầu ngày thêm {0} đá tinh": ", first win of the day +{0} crystal shards",
    "Mỗi ngày {0} lượt thắng, thua không mất lượt.": "{0} wins per day; losses cost nothing.",
    "Hệ boss theo ngày: {0}.": "Boss element by day: {0}.",
    "Chọn hệ boss ở hàng dưới": "Pick the boss element below",
    "+1 lượt": "+1 win",
    "CN": "Sun",
    "T2": "Mon",
    "T3": "Tue",
    "T4": "Wed",
    "T5": "Thu",
    "T6": "Fri",
    "T7": "Sat",
}

raw = open(UI, encoding="utf-8-sig").read()
d = json.loads(raw)
added = [k for k in ADD if k not in d]
for k in added:
    d[k] = ADD[k]
if added:
    out = json.dumps(d, ensure_ascii=False, indent=1)
    if raw.endswith("\n"):
        out += "\n"
    open(UI, "w", encoding="utf-8", newline="\n").write(out)
print("thêm", len(added), "khoá:", added)
