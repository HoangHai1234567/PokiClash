# Chạy bộ test EditMode trong Unity qua cầu nối MCP (nhóm công cụ testing phải bật trong cùng phiên MCP).
#   py -3 -I unity_test.py [tên lớp test hoặc bộ lọc ...]      (không lọc: chạy hết EditMode)
import os, sys, json, time

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unity_mcp as um


def text(r):
    try:
        return json.loads(r["result"]["content"][0]["text"])
    except Exception:
        return r


sid = um.open_session()
st = um.state(sid)
if um.find(st, "is_playing") or um.find(st, "is_compiling"):
    print("BẬN, không chạy test")
    sys.exit(3)
print("bật nhóm testing:", json.dumps(text(um.call(sid, "manage_tools", {"action": "activate", "group": "testing"})), ensure_ascii=False)[:200])
if "--schema" in sys.argv:
    r, _ = um.post({"jsonrpc": "2.0", "id": 9, "method": "tools/list"}, sid)
    for t in r["result"]["tools"]:
        if t["name"] in ("run_tests", "get_test_job"):
            print(json.dumps(t["inputSchema"], ensure_ascii=False)[:1500])
    sys.exit(0)
names = [a for a in sys.argv[1:] if not a.startswith("--")]
args = {"mode": "EditMode", "include_failed_tests": True}
if names:
    args["group_names"] = names
r = text(um.call(sid, "run_tests", args))
job = um.find(r, "job_id")
print("job:", job, json.dumps(r, ensure_ascii=False)[:300] if not job else "")
if not job:
    sys.exit(1)
t0 = time.time()
while time.time() - t0 < 1500:
    time.sleep(6)
    try:
        j = text(um.call(sid, "get_test_job", {"job_id": job, "include_failed_tests": True}))
    except Exception as e:
        print("lỗi hỏi:", e)
        continue
    stt = um.find(j, "status")
    if stt and stt not in ("running", "queued", "pending"):
        break
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "unity_test.json")
open(out, "w", encoding="utf-8").write(json.dumps(j, ensure_ascii=False, indent=1))
res = um.find(j, "result") or j
print("trạng thái:", stt, "| sau %.0f giây" % (time.time() - t0))
print("tóm tắt:", json.dumps(um.find(j, "summary"), ensure_ascii=False))
for f in (um.find(j, "failures") or um.find(j, "failed_tests") or [])[:40]:
    print(" HỎNG", json.dumps(f, ensure_ascii=False)[:600])
print("chi tiết:", out)
