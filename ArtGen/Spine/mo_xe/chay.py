"""Mổ xẻ / soi một rig Spine 4.2 bằng runtime gốc (lib/spine-player.js) trong Chrome chạy ngầm. Tự mở server tĩnh tạm, không
cần chạy server riêng. Rig là bộ <tên>.skel hoặc <tên>.json + <tên>.atlas + ảnh, nằm ở thư mục bất kỳ.

    chay.py info   <thư mục rig> <tên> <ra.json>
        cấu trúc: xương, slot, hình (mesh, số đỉnh, xương bám), ràng buộc, clip (từng timeline, số khoá, biên độ), vùng atlas
    chay.py sample <thư mục rig> <tên> <ra.json> <clip[,clip...]> [fps] [extra.json]
        lấy mẫu từng khung: toạ độ, góc, tỉ lệ, ma trận thế giới của mọi xương; độ đậm, tên hình, thứ tự vẽ của mọi slot (đủ để
        NƯỚNG rig có IK / path constraint thành khoá FK). extra.json (trong thư mục rig): animation tự viết thêm trên bộ xương gốc
    chay.py keys   <thư mục rig> <tên> <ra.json> <clip[,clip...]>
        mọi khoá của từng timeline (giờ, giá trị, kiểu đường cong): để đọc nhịp người làm animation đặt dáng
    chay.py mesh   <thư mục rig> <tên> <ra.json> [slot,slot...]
        lưới của từng slot: mỗi đỉnh có uv, toạ độ dáng gốc và danh sách (xương, trọng số): để đọc cách chia trọng số
    chay.py att    <thư mục rig> <tên> <ra.json> ["anim=<clip>&t=<giây>"]
        MỌI hình của mọi slot (cả hình không bật mặc định), đỉnh thế giới, uv, trọng số, thứ tự vẽ: xem họ tách mảnh thế nào.
        Thêm anim và t: chỉ các hình đang bật ở dáng đó (dáng duỗi, dáng lao dùng mảnh nào, đặt đâu)
    chay.py sheet  <thư mục rig> <tên> <thư mục ra> ["tham số thêm"]
        tờ khung từng clip (jpg). Tham số thêm dạng query: anims=a,b  n=10  tw=520  th=420  cols=5  view=cx,cy,rộng,cao
        t0=0.2  t1=0.9  loop=1 (khung cuối không trùng khung đầu)  bones=1 (vẽ xương)

Ví dụ:  chay.py sheet ../inbox/hai_long/rig hai_long ../inbox/hai_long/khung "n=10&view=-20,470,1900,1500"
phan_tich.py và do_chuyen_dong.py là ví dụ đọc info.json / mẫu khung của một con cụ thể (tên xương ghi cứng), chép ra mà sửa."""
import base64
import html
import http.server
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
SPINE = os.path.dirname(HERE)
CHROMES = [r"C:\Program Files\Google\Chrome\Application\chrome.exe", r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
           r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"]


def serve(data_dir):
    class H(http.server.SimpleHTTPRequestHandler):
        def translate_path(self, path):
            p = urllib.parse.unquote(path.split("?", 1)[0].split("#", 1)[0])
            if p.startswith("/d/"):
                return os.path.join(data_dir, *p[3:].split("/"))
            if p.startswith("/lib/"):
                return os.path.join(SPINE, "lib", *p[5:].split("/"))
            return os.path.join(HERE, *p.lstrip("/").split("/"))

        def log_message(self, *a):
            pass

    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def run(data_dir, name, query, budget=120000):
    data_dir = os.path.abspath(data_dir)
    fmt = "skel" if os.path.exists(os.path.join(data_dir, name + ".skel")) else "json"
    chrome = next((c for c in CHROMES if os.path.exists(c)), None)
    if not chrome:
        sys.exit("không tìm thấy Chrome / Edge")
    srv = serve(data_dir)
    prof = tempfile.mkdtemp(prefix="mo_xe_")
    try:
        url = f"http://127.0.0.1:{srv.server_address[1]}/mo_xe.html?name={name}&dir=d&fmt={fmt}&{query}"
        r = subprocess.run([chrome, "--headless=new", "--disable-gpu-sandbox", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist",
                            "--no-first-run", "--user-data-dir=" + prof, f"--virtual-time-budget={budget}", "--dump-dom", url],
                           capture_output=True, timeout=900)
    finally:
        srv.shutdown()
        shutil.rmtree(prof, ignore_errors=True)
    s = r.stdout.decode("utf-8", "replace")
    a = s.find("JSON_BEGIN")
    b = s.find("JSON_END", a)  # JSON_END đầu tiên SAU JSON_BEGIN (chuỗi này cũng có trong mã của trang)
    if a < 0 or b < 0:
        i = s.find('<pre id="out">')
        print("KHÔNG CÓ JSON:", s[i:i + 1500] if i >= 0 else s[:1500], file=sys.stderr)
        print(r.stderr.decode("utf-8", "replace")[-1500:], file=sys.stderr)
        sys.exit(1)
    return json.loads(html.unescape(s[a + 10:b]))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 5:
        sys.exit(__doc__)
    mode, data_dir, name, out = sys.argv[1:5]
    if mode == "info":
        d = run(data_dir, name, "mode=info")
        json.dump(d, open(out, "w", encoding="utf-8"), ensure_ascii=False)
        nk = sum(t["frames"] for a in d["anims"] for t in a["tls"])
        print(f"{len(d['bones'])} xương, {len(d['slots'])} slot, {len(d['anims'])} clip, {nk} khoá -> {out}")
    elif mode == "keys":
        d = run(data_dir, name, f"mode=keys&anims={sys.argv[5]}")
        json.dump(d, open(out, "w", encoding="utf-8"))
        for k, v in d.items():
            print(f"{k}: {v['dur']:.2f} s, {len(v['tls'])} timeline, {sum(len(t['f']) // t['n'] for t in v['tls'])} khoá -> {out}")
    elif mode == "mesh":
        d = run(data_dir, name, f"mode=mesh&slots={sys.argv[5] if len(sys.argv) > 5 else ''}")
        json.dump(d, open(out, "w", encoding="utf-8"))
        for k, v in d.items():
            print(f"{k}: {v['att']}, {len(v['verts'])} đỉnh, {len(v['tris']) // 3} tam giác")
    elif mode == "att":
        d = run(data_dir, name, "mode=att&" + (sys.argv[5] if len(sys.argv) > 5 else ""))
        json.dump(d, open(out, "w", encoding="utf-8"))
        print(f"{len(d['atts'])} hình ({'dáng gốc, mọi hình' if not d['anim'] else d['anim'] + ' @ ' + str(d['t']) + ' s, hình đang bật'}) -> {out}")
    elif mode == "sample":
        fps = sys.argv[6] if len(sys.argv) > 6 else "30"
        extra = f"&extra={sys.argv[7]}" if len(sys.argv) > 7 else ""            # file json animation tự viết, nằm trong thư mục rig
        d = run(data_dir, name, f"mode=sample&anims={sys.argv[5]}&fps={fps}{extra}")
        json.dump(d, open(out, "w", encoding="utf-8"))
        for k, v in d.items():
            print(f"{k}: {v['dur']:.2f} s, {len(v['frames'])} khung -> {out}")
    else:
        extra = sys.argv[5] if len(sys.argv) > 5 else ""
        os.makedirs(out, exist_ok=True)
        d = run(data_dir, name, "mode=sheet&" + extra)
        print("khung nhìn", d["view"])
        for k, v in d["sheets"].items():
            p = os.path.join(out, k.replace("/", "_") + ".jpg")
            open(p, "wb").write(base64.b64decode(v.split(",", 1)[1]))
            print(p)
