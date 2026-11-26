# Gọi cầu nối mcp-for-unity (HTTP, cổng 8080 trên máy ổ C) bằng thư viện chuẩn.
#   py -3 -I unity_mcp.py state                      -> in is_playing / is_compiling
#   py -3 -I unity_mcp.py call <tool> '<json args>'  -> gọi một công cụ (refresh_unity, read_console, ...)
#   py -3 -I unity_mcp.py refresh-neu-ranh           -> chỉ refresh khi Unity không Play, không biên dịch; đang bận thì thoát mã 3
import json, sys, urllib.request

sys.stdout.reconfigure(encoding="utf-8")
URL = "http://127.0.0.1:8080/mcp"


def post(body, sid=None):
    h = {"Content-Type": "application/json; charset=utf-8", "Accept": "application/json, text/event-stream"}
    if sid:
        h["mcp-session-id"] = sid
    req = urllib.request.Request(URL, data=json.dumps(body, ensure_ascii=False).encode("utf-8"), headers=h)
    with urllib.request.urlopen(req, timeout=120) as r:
        raw = r.read().decode("utf-8", "replace")
        sid = r.headers.get("mcp-session-id") or sid
    out = None
    for line in raw.splitlines():
        if line.startswith("data:"):
            try:
                out = json.loads(line[5:].strip())
            except ValueError:
                pass
    if out is None and raw.strip().startswith("{"):
        out = json.loads(raw)
    return out, sid


def open_session():
    _, sid = post({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                   "params": {"protocolVersion": "2025-03-26", "capabilities": {}, "clientInfo": {"name": "kinhte", "version": "1"}}})
    post({"jsonrpc": "2.0", "method": "notifications/initialized"}, sid)
    return sid


def state(sid):
    r, _ = post({"jsonrpc": "2.0", "id": 2, "method": "resources/read", "params": {"uri": "mcpforunity://editor/state"}}, sid)
    txt = r["result"]["contents"][0]["text"]
    return json.loads(txt)


def find(o, key):
    if isinstance(o, dict):
        if key in o:
            return o[key]
        for v in o.values():
            x = find(v, key)
            if x is not None:
                return x
    elif isinstance(o, list):
        for v in o:
            x = find(v, key)
            if x is not None:
                return x
    return None


def call(sid, tool, args):
    r, _ = post({"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": tool, "arguments": args}}, sid)
    return r


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "state"
    sid = open_session()
    if cmd == "state":
        st = state(sid)
        print("is_playing", find(st, "is_playing"), "| is_compiling", find(st, "is_compiling"), "| transition", find(st, "is_changing") or find(st, "playmode_transition"))
    elif cmd == "call":
        print(json.dumps(call(sid, sys.argv[2], json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}), ensure_ascii=False)[:3000])
    elif cmd == "refresh-neu-ranh":
        st = state(sid)
        if find(st, "is_playing") or find(st, "is_compiling"):
            print("BẬN: is_playing", find(st, "is_playing"), "is_compiling", find(st, "is_compiling"))
            sys.exit(3)
        print(json.dumps(call(sid, "refresh_unity", {"mode": "force", "scope": "all", "compile": "request", "wait_for_ready": False}), ensure_ascii=False)[:600])
