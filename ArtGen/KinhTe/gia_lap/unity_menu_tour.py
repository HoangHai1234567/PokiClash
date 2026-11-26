# Chạy một tour kiểu "menu (đang Play)": vào Play từ cảnh đang mở, bật chạy nền, chờ tới sảnh (Hub), gọi menu tour, chờ file log của tour
# đổi rồi thoát Play.   py -3 -I unity_menu_tour.py "<đường menu>" "<file log của tour>" [giây tối đa]
import os, sys, time, json, glob

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import unity_mcp as um

PROJ = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
menu, logf = sys.argv[1], sys.argv[2]
limit = float(sys.argv[3]) if len(sys.argv) > 3 else 420
BG = "PokiClash/Thử/Play chạy cả khi Unity nằm nền (tạm, tới khi thoát Play)"


def txt(r):
    try:
        return r["result"]["content"][0]["text"]
    except Exception:
        return json.dumps(r, ensure_ascii=False)


sid = um.open_session()
s = um.state(sid)
others = glob.glob(os.path.join(PROJ, "Temp", "*.flag"))
if um.find(s, "is_playing") or um.find(s, "is_compiling") or others:
    print("BẬN", um.find(s, "is_playing"), um.find(s, "is_compiling"), others)
    sys.exit(3)
m0 = os.path.getmtime(logf) if os.path.exists(logf) else 0
print("play:", txt(um.call(sid, "manage_editor", {"action": "play"}))[:160])
time.sleep(2)
print("nền:", txt(um.call(sid, "execute_menu_item", {"menu_path": BG}))[:160])
t0 = time.time()
hub = False
while time.time() - t0 < 240:
    time.sleep(4)
    try:
        r = txt(um.call(um.open_session(), "manage_scene", {"action": "get_active"}))
    except Exception as e:
        r = str(e)
    if '"Hub"' in r or "Hub" in r.split("path")[0]:
        hub = True
        break
print("tới Hub:", hub, "| %.0f giây" % (time.time() - t0))
ok = False
if hub:
    time.sleep(10)
    um.call(um.open_session(), "execute_menu_item", {"menu_path": BG})
    # menu "(đang Play)" tự bỏ qua nếu game chưa sẵn (log "bấm Play trước"): gọi lại tối đa 4 lần, mỗi lần cách 10 giây
    LOG = os.path.join(os.environ["LOCALAPPDATA"], "Unity", "Editor", "Editor.log")
    for lan in range(4):
        pos = os.path.getsize(LOG)
        print("tour:", txt(um.call(um.open_session(), "execute_menu_item", {"menu_path": menu}))[:120])
        time.sleep(6)
        with open(LOG, "rb") as f:
            f.seek(pos)
            new = f.read().decode("utf-8", "replace")
        if "bấm Play trước" not in new:
            break
        print("  game chưa sẵn, gọi lại sau 10 giây")
        time.sleep(10)
    t1 = time.time()
    while time.time() - t1 < limit:
        time.sleep(5)
        if os.path.exists(logf) and os.path.getmtime(logf) > m0:
            ok = True
            break
        try:
            um.state(um.open_session())
        except Exception:
            pass
    print("tour xong:", ok, "| %.0f giây" % (time.time() - t1))
time.sleep(3)
print("stop:", txt(um.call(um.open_session(), "manage_editor", {"action": "stop"}))[:160])
if ok:
    print(open(logf, encoding="utf-8").read()[:3000])
