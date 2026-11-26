# Đặt một cờ tour trong Temp/ (chỉ khi Unity không Play, không biên dịch, không có cờ nào khác), chờ Unity vào Play rồi thoát Play.
#   py -3 -I unity_tour.py <tên cờ, ví dụ casino_market_tour.flag> [giây tối đa]
import os, sys, time, glob

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import unity_mcp as um

PROJ = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
flag = os.path.join(PROJ, "Temp", sys.argv[1])
limit = float(sys.argv[2]) if len(sys.argv) > 2 else 480


def st():
    try:
        s = um.state(um.open_session())
        return bool(um.find(s, "is_playing")), bool(um.find(s, "is_compiling"))
    except Exception:
        return None, None


playing, compiling = st()
others = glob.glob(os.path.join(PROJ, "Temp", "*.flag"))
if playing or compiling or playing is None or others:
    print("BẬN: playing", playing, "compiling", compiling, "cờ khác", [os.path.basename(x) for x in others])
    sys.exit(3)
open(flag, "w", encoding="utf-8").write("assets-85 kinh te")
t0 = time.time()
seen = False
while time.time() - t0 < limit:
    time.sleep(4)
    playing, _ = st()
    if playing:
        seen = True
    elif seen and playing is False and not os.path.exists(flag):
        break
print("đã vào Play:", seen, "| đã thoát:", seen and not playing, "| %.0f giây" % (time.time() - t0), "| cờ còn:", os.path.exists(flag))
if os.path.exists(flag) and not seen:
    os.remove(flag)
    print("gỡ cờ vì tour không chạy")
