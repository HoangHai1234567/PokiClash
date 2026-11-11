"""Soi rig Hải Long bản 4 (inbox/hai_long/rig/), không sửa thư viện chung (mo_xe/chay.py không biết clip aura):

    py -3 -I ArtGen/Spine/quai/khoa.py chrome -- py -3 -I ArtGen/Spine/hai_long_soi.py sheet [n=12] [clip,clip]   tờ khung từng
        clip (khung_<clip>.png), aura phủ track 1 trộn cộng như AtomikPose.Overlay; thêm "view=cx,cy,w,h&t0=..&t1=.." qua --q
    py -3 -I ArtGen/Spine/quai/khoa.py chrome -- py -3 -I ArtGen/Spine/hai_long_soi.py can                       bộ ảnh cận: miệng
        há to nhất (skill), ngửa đầu lè lưỡi (die), chỗ nối cổ và râu lúc giật (hit), hàm hai xương (cast)
    py -3 -I ArtGen/Spine/hai_long_soi.py luoi        rig/luoi.png (lưới + màu theo xương nặng nhất + xương), luoi_dau.png (cận thủ lĩnh)
    py -3 -I ArtGen/Spine/hai_long_soi.py so_sanh     rig/so_sanh.md: so với monster_3705 (scan) và bản Hải Long cũ trong Assets/05 Atomik Thu
    py -3 -I ArtGen/Spine/hai_long_soi.py chan_dung   rig/chan_dung.png: chân dung vuông 512 cắt từ concept đã duyệt (đầu thủ lĩnh)
    py -3 -I ArtGen/Spine/hai_long_soi.py lech        đo lệch khung cuối mỗi clip so với khung 0 idle (đọc rig JSON, nội suy khoá)
"""
import base64
import gzip
import html
import http.server
import json
import math
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import threading
import urllib.parse
import zlib

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
RIG = os.path.join(HERE, "inbox", "hai_long", "rig")
NAME = "hai_long"
for _a in list(sys.argv[1:]):   # soi rig khác của dòng (dạng 1, 2): --rig=<thư mục> --name=<tên>
    if _a.startswith("--rig="):
        RIG = os.path.abspath(_a[6:])
        sys.argv.remove(_a)
    elif _a.startswith("--name="):
        NAME = _a[7:]
        sys.argv.remove(_a)
MO_XE = os.path.join(HERE, "mo_xe")
OLD_ATOMIK = os.path.normpath(os.path.join(HERE, "..", "..", "Assets", "05 Atomik Thu", "hai_long.atomik"))
SCAN = r"D:\RefAnimation\SwordxStaff\scan\monster_3705"
REF_FILES = r"D:\RefAnimation\SwordxStaff\web\assets\Monster\monster_3705"
CHROMES = [r"C:\Program Files\Google\Chrome\Application\chrome.exe", r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
           r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"]
VIEW = "-20,470,1900,1500"


# ---------------------------------------------------------------- tờ khung bằng runtime Spine, có aura
def patched_html():
    """mo_xe.html của bộ mổ xẻ + aura trên track 1 (trộn cộng) trong chế độ sheet."""
    src = open(os.path.join(MO_XE, "mo_xe.html"), encoding="utf-8").read()
    hook = "st.setAnimation(0, nm, false);"
    assert hook in src, "mo_xe.html đổi: không thấy chỗ chèn aura"
    add = (hook + " if (Q.get(\"aura\") !== \"0\" && sd.findAnimation(\"aura\")) { const ae = st.setAnimation(1, \"aura\", true); "
                  "ae.mixBlend = (spine.MixBlend && spine.MixBlend.add !== undefined) ? spine.MixBlend.add : 3; }")
    src = src.replace(hook, add, 1)
    # trộn cộng của Spine CỘNG DỒN vào dáng hiện tại mỗi lần apply (không tự về dáng gốc): phải đặt lại dáng gốc trước mỗi apply, như
    # AtomikPose.Sample làm trong Unity. Không có dòng này thì sóng phình to dần theo thời gian (lỗi đã gặp 2026-11-11).
    assert "st.apply(sk);" in src
    return src.replace("st.apply(sk);", "sk.setToSetupPose(); st.apply(sk);")


def serve(data_dir, page):
    class H(http.server.SimpleHTTPRequestHandler):
        def translate_path(self, path):
            p = urllib.parse.unquote(path.split("?", 1)[0].split("#", 1)[0])
            if p.startswith("/d/"):
                return os.path.join(data_dir, *p[3:].split("/"))
            if p.startswith("/lib/"):
                return os.path.join(HERE, "lib", *p[5:].split("/"))
            return os.path.join(page, *p.lstrip("/").split("/"))

        def log_message(self, *a):
            pass

    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def run(query, budget=180000):
    chrome = next((c for c in CHROMES if os.path.exists(c)), None)
    if not chrome:
        sys.exit("không tìm thấy Chrome / Edge")
    page = tempfile.mkdtemp(prefix="hl_soi_")
    open(os.path.join(page, "mo_xe.html"), "w", encoding="utf-8").write(patched_html())
    srv = serve(RIG, page)
    prof = tempfile.mkdtemp(prefix="hl_prof_")
    try:
        url = f"http://127.0.0.1:{srv.server_address[1]}/mo_xe.html?name={NAME}&dir=d&fmt=json&{query}"
        r = subprocess.run([chrome, "--headless=new", "--disable-gpu-sandbox", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist",
                            "--no-first-run", "--user-data-dir=" + prof, f"--virtual-time-budget={budget}", "--dump-dom", url],
                           capture_output=True, timeout=900)
    finally:
        srv.shutdown()
        shutil.rmtree(prof, ignore_errors=True)
        shutil.rmtree(page, ignore_errors=True)
    s = r.stdout.decode("utf-8", "replace")
    a = s.find("JSON_BEGIN")
    b = s.find("JSON_END", a)
    if a < 0 or b < 0:
        i = s.find('<pre id="out">')
        print("KHÔNG CÓ JSON:", s[i:i + 1500] if i >= 0 else s[:1500], file=sys.stderr)
        sys.exit(1)
    return json.loads(html.unescape(s[a + 10:b]))


def save_sheets(d, prefix):
    outs = []
    for k, v in d["sheets"].items():
        p = os.path.join(RIG, f"{prefix}{k}.png")
        jpg = base64.b64decode(v.split(",", 1)[1])
        import io
        Image.open(io.BytesIO(jpg)).convert("RGB").save(p, optimize=True)
        outs.append(p)
        print(p)
    return outs


def sheet(n=12, clips=None, extra=""):
    q = f"mode=sheet&n={n}&cols=4&tw=560&th=440&view={VIEW}"
    if clips:
        q += "&anims=" + ",".join(clips)
    if extra:
        q += "&" + extra
    d = run(q)
    print("khung nhìn", d["view"])
    return save_sheets(d, "khung_")


def can():
    """ảnh cận theo 'Kiểm' của skill-petclash mục 15: miệng há to nhất (skill 1,45–1,75 s, thủ lĩnh), ngửa đầu lè lưỡi (die, thủ lĩnh
    1,0–1,7 s), chỗ nối cổ + râu ở clip trúng đòn (0–0,3 s), hàm hai xương lúc phun (cast, đầu d thấp bên phải)."""
    # đọc chỗ đầu thủ lĩnh từ rig JSON (dáng gốc) để đặt khung nhìn
    J = json.load(open(os.path.join(RIG, NAME + ".json"), encoding="utf-8"))
    W = world_bones(J)
    hk = W["hk"][:2]
    hd = W.get("hd", W["hk"])[:2]   # rig một đầu (dạng 1) không có đầu d
    jobs = [("can_mieng_skill", "skill", 1.40, 1.80, (hk[0] + 60, hk[1] - 10, 560, 440)),
            ("can_ngua_die", "die", 1.00, 1.75, (hk[0] - 60, hk[1] + 40, 760, 600)),
            ("can_rau_hit", "hit", 0.0, 0.33, (hk[0] + 40, hk[1] - 60, 760, 600)),
            ("can_noico_hit", "hit", 0.0, 0.33, (hk[0] - 420, hk[1] - 330, 900, 700)),
            ("can_ham_cast", "cast", 0.95, 1.45, (hd[0] + 120, hd[1] - 20, 620, 480)),
            ("can_mieng_attack", "attack", 0.36, 0.56, (hd[0] + 330, hd[1] - 30, 620, 480)),
            # chỗ nối đầu–cổ lúc đầu xoay mạnh nhất (cách lai 2026-11-11): bổ xuống ở attack và ngửa ở die, nhìn vào gáy thủ lĩnh
            ("can_noi_dau_attack", "attack", 0.30, 0.62, (hk[0] - 120, hk[1] - 80, 620, 480)),
            ("can_noi_dau_die", "die", 0.90, 1.70, (hk[0] - 120, hk[1] - 40, 620, 480))]
    for nm, clip, t0, t1, (cx, cy, w, h) in jobs:
        d = run(f"mode=sheet&n=8&cols=4&tw=620&th=480&anims={clip}&t0={t0}&t1={t1}&view={cx:.0f},{cy:.0f},{w},{h}")
        for k, v in d["sheets"].items():
            p = os.path.join(RIG, nm + ".png")
            import io
            Image.open(io.BytesIO(base64.b64decode(v.split(",", 1)[1]))).convert("RGB").save(p, optimize=True)
            print(p)


# ---------------------------------------------------------------- lưới + trọng số (vẽ từ JSON Spine, dáng gốc)
def world_bones(J):
    """ma trận thế giới dáng gốc của từng xương: {tên: (wx, wy, a, b, c, d)} với [x', y'] = [a b; c d] [x, y] + [wx, wy]."""
    W = {}
    for b in J["bones"]:
        r = math.radians(b.get("rotation", 0.0))
        sx, sy = b.get("scaleX", 1.0), b.get("scaleY", 1.0)
        la, lb, lc, ld = math.cos(r) * sx, -math.sin(r) * sy, math.sin(r) * sx, math.cos(r) * sy
        lx, ly = b.get("x", 0.0), b.get("y", 0.0)
        p = b.get("parent")
        if p is None:
            W[b["name"]] = (lx, ly, la, lb, lc, ld)
            continue
        px, py, pa, pb, pc, pd = W[p]
        W[b["name"]] = (pa * lx + pb * ly + px, pc * lx + pd * ly + py,
                        pa * la + pb * lc, pa * lb + pb * ld, pc * la + pd * lc, pc * lb + pd * ld)
    return W


def mesh_world(att, bones, W):
    """vị trí thế giới từng đỉnh của lưới có trọng số + xương nặng nhất."""
    v = att["vertices"]
    out, dom = [], []
    i = 0
    n = len(att["uvs"]) // 2
    for _ in range(n):
        k = int(v[i]); i += 1
        X = Y = 0.0
        best = (-1, None)
        for _ in range(k):
            bi, x, y, w = int(v[i]), v[i + 1], v[i + 2], v[i + 3]
            i += 4
            wx, wy, a, b, c, d = W[bones[bi]["name"]]
            X += (a * x + b * y + wx) * w
            Y += (c * x + d * y + wy) * w
            if w > best[0]:
                best = (w, bones[bi]["name"])
        out.append((X, Y))
        dom.append(best[1])
    return out, dom


def color_of(name):
    h = zlib.crc32(name.encode()) & 0xFFFFFF
    r, g, b = (h >> 16) & 255, (h >> 8) & 255, h & 255
    return (80 + r // 2, 80 + g // 2, 80 + b // 2)


def luoi():
    J = json.load(open(os.path.join(RIG, NAME + ".json"), encoding="utf-8"))
    W = world_bones(J)
    bones = J["bones"]
    slot_alpha = {s["name"]: (int(s["color"][6:8], 16) / 255 if "color" in s else 1.0) for s in J["slots"]}
    atts = J["skins"][0]["attachments"]

    def render(view, scale, path, title, bones_on=True):
        cx, cy, vw, vh = view
        Wd, Hd = int(vw * scale), int(vh * scale)
        im = Image.new("RGB", (Wd, Hd), (236, 236, 232))
        d = ImageDraw.Draw(im)
        T = lambda p: ((p[0] - (cx - vw / 2)) * scale, (cy + vh / 2 - p[1]) * scale)
        nv = nt = 0
        for sname, amap in atts.items():
            if slot_alpha.get(sname, 1.0) < 0.5:
                continue
            for aname, a in amap.items():
                if a.get("type") == "mesh":
                    P, dom = mesh_world(a, bones, W)
                    tris = a["triangles"]
                    nv += len(P)
                    nt += len(tris) // 3
                    for k in range(0, len(tris), 3):
                        i0, i1, i2 = tris[k], tris[k + 1], tris[k + 2]
                        col = color_of(dom[i0])
                        d.polygon([T(P[i0]), T(P[i1]), T(P[i2])], outline=col)
                elif a.get("type", "region") == "region":
                    # mảnh cứng: khung chữ nhật xoay theo xương của slot
                    bn = next(s["bone"] for s in J["slots"] if s["name"] == sname)
                    wx, wy, ma, mb, mc, md = W[bn]
                    ax, ay, aw, ah = a.get("x", 0), a.get("y", 0), a["width"] * a.get("scaleX", 1), a["height"] * a.get("scaleY", 1)
                    rr = math.radians(a.get("rotation", 0))
                    cs, sn = math.cos(rr), math.sin(rr)
                    pts = []
                    for qx, qy in ((-aw / 2, ah / 2), (aw / 2, ah / 2), (aw / 2, -ah / 2), (-aw / 2, -ah / 2)):
                        lx, ly = ax + qx * cs - qy * sn, ay + qx * sn + qy * cs
                        pts.append(T((ma * lx + mb * ly + wx, mc * lx + md * ly + wy)))
                    d.polygon(pts, outline=(60, 60, 60))
                    nv += 4
                    nt += 2
        if bones_on:
            for b in bones:
                if b.get("parent") is None:
                    continue
                wx, wy, a_, b_, c_, d_ = W[b["name"]]
                L = b.get("length", 0) or 6
                p0, p1 = T((wx, wy)), T((wx + a_ * L, wy + c_ * L))
                d.line([p0, p1], fill=(200, 30, 30), width=1)
                d.ellipse([p0[0] - 1.5, p0[1] - 1.5, p0[0] + 1.5, p0[1] + 1.5], fill=(200, 30, 30))
        try:
            f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 16)
        except Exception:
            f = None
        d.text((8, 6), f"{title}: {nv} đỉnh, {nt} tam giác (slot ẩn mặc định không vẽ); màu = xương nặng nhất; đỏ = xương", fill=(20, 20, 20), font=f)
        im.save(path, optimize=True)
        print(path, f"{nv} đỉnh {nt} tam giác")

    render((-20, 540, 1900, 1400), 1.0, os.path.join(RIG, "luoi.png"), "Lưới cả con (dáng gốc)")
    hk = W["hk"]
    render((hk[0] + 40, hk[1] + 20, 620, 460), 2.5, os.path.join(RIG, "luoi_dau.png"), "Cận đầu thủ lĩnh: đầu 14×10, hàm 9×4 hai xương, lòng miệng 7×4, râu, bờm")
    render((-80, 60, 1500, 420), 1.4, os.path.join(RIG, "luoi_nuoc.png"), "Cận nước: cuộn sóng 8×8, dải nước 25×4, vòng thân 13×8, đuôi")


# ---------------------------------------------------------------- so sánh
def read_atomik(path):
    b = open(path, "rb").read()
    body = gzip.decompress(b[6:])
    n = struct.unpack("<I", body[:4])[0]
    d = json.loads(body[4:4 + n])
    nk = 0
    for a in d["anims"]:
        for t in a["tls"]:
            nk += len(t["keys"]) // (7 if t["type"] == 0 else 12)
        for k in (a.get("sa") or []):
            nk += len(k["keys"]) // 7
    return dict(file=len(b), json=n, png=len(body) - 8 - n, bones=len(d["bones"]), slots=len(d["slots"]), atts=len(d["atts"]),
                verts=sum(len(a["uvs"]) // 2 for a in d["atts"]), tris=sum(len(a["tris"]) // 3 for a in d["atts"]), keys=nk,
                clips={a["name"]: (a["dur"], sum(len(t["keys"]) // (7 if t["type"] == 0 else 12) for t in a["tls"]) + sum(len(k["keys"]) // 7 for k in (a.get("sa") or []))) for a in d["anims"]},
                game=d.get("game"), masks=len(d.get("masks") or []))


def so_sanh():
    st = json.load(open(os.path.join(RIG, "stat.json"), encoding="utf-8"))
    new = read_atomik(os.path.join(RIG, NAME + ".atomik"))
    old = read_atomik(OLD_ATOMIK) if os.path.exists(OLD_ATOMIK) else None
    ref = json.load(open(os.path.join(SCAN, "info.json"), encoding="utf-8"))
    ratts = ref["skins"][0]["atts"]
    rmesh = [a for a in ratts if a["type"] == "_MeshAttachment"]
    rkeys = sum(t.get("frames", 0) for a in ref["anims"] for t in a["tls"])
    rsize = sum(os.path.getsize(os.path.join(REF_FILES, f)) for f in ("monster_3705.skel", "monster_3705.png") if os.path.exists(os.path.join(REF_FILES, f)))
    mb = lambda n: f"{n / 1e6:.2f} MB"
    L = ["# Hải Long Ngũ Đầu bản 4: so với con gốc (monster_3705) và bản 3 (2026-11-11)", "",
         "Bản 4 dựng lại từ cùng 7 tờ mảnh: lưới dày, mịn, gần đều cạnh; hàm dưới lưới hai xương; nước tách thành clip `aura` lặp riêng "
         "(runtime phủ lên mọi clip, AtomikPose.Overlay); clip đổi sang tên game. Số của con gốc đọc từ `scan/monster_3705/info.json`; "
         "bản 3 đọc từ `Assets/05 Atomik Thu/hai_long.atomik` (chỉ đọc).", "",
         "| | monster_3705 (gốc) | Hải Long bản 3 | Hải Long bản 4 |", "|---|---|---|---|",
         f"| Xương | {len(ref['bones'])} (thân 131, nước 354) | {old['bones'] if old else '?'} (thân 193, nước 288) | {st['bones']} (thân {st['bones_body']}, nước {st['bones_water']}) |",
         f"| Slot | {len(ref['slots'])} | {old['slots'] if old else '?'} | {st['slots']} |",
         f"| Lưới / hình | {len(rmesh)} lưới, 0 mảnh cứng | {old['atts'] if old else '?'} hình | {st['meshes']} lưới + {st['slots'] - st['meshes'] - 1} mảnh cứng |",
         f"| Đỉnh | {sum(a['verts'] for a in rmesh)} | {old['verts'] if old else '?'} | {st['verts']} |",
         f"| Tam giác | {sum(a['tris'] for a in rmesh)} | {old['tris'] if old else '?'} | {st['tris']} |",
         f"| Clip | {len(ref['anims'])} | {len(old['clips']) if old else '?'} | {st['clips']} (7 + aura) |",
         f"| Khoá | {rkeys:,} (nước chép vào từng clip) | {old['keys']:,} | {st['keys']:,} (JSON Spine; .atomik {new['keys']:,}) |",
         f"| Dung lượng | skel {mb(os.path.getsize(os.path.join(REF_FILES, 'monster_3705.skel')))} + atlas {mb(os.path.getsize(os.path.join(REF_FILES, 'monster_3705.png')))} = {mb(rsize)} | .atomik {mb(old['file']) if old else '?'} (json {mb(old['json']) if old else '?'} + png {mb(old['png']) if old else '?'} trước nén) | .atomik **{mb(new['file'])}** (json {mb(new['json'])} + png {mb(new['png'])} trước nén); JSON Spine {mb(st['json'])} + atlas {mb(st['png'])} |",
         f"| Atlas | 2048 × 1228 | | {st['atlas'][0]} × {st['atlas'][1]}, bảng 256 màu |",
         "", "## Khoá và thời lượng từng clip", "", "| Clip (bản 4) | Dài (s) | Khoá bản 4 | Clip bản 3 tương ứng | Khoá bản 3 |", "|---|---|---|---|---|"]
    map3 = {"appear": "xuat_hien", "idle": "dung", "attack": "tan_cong", "cast": "chieu_phun", "skill": "chieu", "hit": "trung_don", "die": "chet", "aura": "(nằm trong từng clip)"}
    for cn, dur in st["durs"].items():
        o = old["clips"].get(map3.get(cn, ""), (None, None)) if old else (None, None)
        L.append(f"| {cn} | {dur:.2f} | {new['clips'][cn][1]:,} | {map3.get(cn, '')} | {o[1] if o[1] is not None else ''} |")
    L += ["", "## Mật độ lưới từng loại mảnh (bản 3 → bản 4)", "",
          "| Mảnh | Bản 3 | Bản 4 | Ghi chú |", "|---|---|---|---|",
          "| Cổ (14 đốt) | 29 cột × 3 hàng = 87 đỉnh | 43 cột × 7 hàng = 301 đỉnh (cổ to), hàng tự giảm cho cổ nhỏ | ô lưới ~26 × 25 đơn vị, gần vuông; đường chéo so le; trọng số B-spline bậc hai |",
          "| Đầu | 10 × 7 = 70 | 15 × 11 = 165 | bờm hoà sang 2 đốt bờm |",
          "| Hàm dưới | mảnh cứng (1 xương) | lưới 10 × 5 = 50 đỉnh, HAI xương | họng sát bản lề theo đầu (tối đa 0,88), cằm và mõm theo hàm, như `xiae` của con gốc |",
          "| Lòng miệng | 5 × 3 = 15 | 8 × 5 = 40 | hàng dưới bám hàm 100%, hàng trên theo đầu ở sát bản lề (luật thịt trong miệng) |",
          "| Râu (6 đốt) | 13 × 3 = 39 | 19 × 3 = 57 | dải mỏng: 3 hàng là đủ đều |",
          "| Lưỡi (5 đốt) | 11 × 3 | 16 × 3–4 | |",
          "| Đuôi (6 đốt) | 13 × 3 | 19 × 5–7 | |",
          "| Cuộn sóng (46 bản) | 6 × 6 = 36 | 9 × 9 = 81 | bám chuỗi 4 đốt trên sống lưng sóng |",
          "| Dải nước (3 dải, 8 xương) | 17 × 3 = 51 | 25 × 4 = 100 | hàng đáy bám gốc |",
          "| Vòng thân | 9 × 6 = 54 | 14 × 9 = 126 | 5 điểm điều khiển |",
          "", "## Khác bản 3", "",
          "- Clip đổi tên theo đặc tả lô Thủy mục 5: `appear, idle, attack, cast (phun nước), skill (gầm), hit, die`; thêm `aura`.",
          "- Nước (băng chuyền 46 cuộn, 3 dải, mảng nền, vòng thân phập phồng, đuôi quẫy) chỉ còn trong `aura` (2 vòng sóng = 3,2 s); clip "
          "chính chỉ khoá `nuoc` (nở / tan), `song` (ép dẹt khi lặng) + độ đậm slot sóng (lặng), `coil`/`tail` (chìm). Khoá giảm tương ứng.",
          "- Slot sóng hiện sẵn (độ đậm 1) vì Overlay NHÂN độ đậm: trang xem hay bộ chụp nào không phát `aura` sẽ thấy mọi cuộn sóng đứng yên ở "
          "dáng gốc. Trang `xem.html` và tờ khung ở đây phát aura trên track 1 (trộn cộng).",
          "- Sự kiện giữ nguyên: `troi, can, gam, het_gam, phun (chuỗi = đầu), het_phun, roi_nuoc`; xương `mieng_<đầu>` giữ nguyên.",
          "- `hai_long_game.json`: fps 30, đứng tại chỗ (`stay` cả ba clip đánh), `muzzle` = xương `mieng_k` lúc phun, khung trúng attack 0,45 / "
          "cast " + f"{new['game']['hitTimes'][1] if new.get('game') else '?'}" + " / skill 1,32; cảm giác trúng boss (khựng 0,08 / 0,2, rung 0,45 / 0,95, chớp màn ở skill).",
          "- Không chép `.atomik` vào `Assets/` nữa (Claude điều phối chép khi đưa vào game)."]
    p = os.path.join(RIG, "so_sanh.md")
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
    print(p)


# ---------------------------------------------------------------- chân dung
def chan_dung(src=None, box=(600, 40, 1070, 510)):
    """chân dung vuông 512 cắt từ concept đã duyệt; mặc định đầu thủ lĩnh Hải Long dạng 3 (--src=<ảnh> --box=x0,y0,x1,y1 cho dạng khác)."""
    src = src or os.path.join(HERE, "inbox", "hai_long", "tai_ve", "L1_duyet.png")
    im = Image.open(src).convert("RGB")
    crop = im.crop(box)
    a = np.asarray(crop)
    light = (a.min(axis=2) > 236).astype(np.uint8)
    import cv2
    ff = np.zeros((light.shape[0] + 2, light.shape[1] + 2), np.uint8)
    bg = light.copy()
    h, w = light.shape
    for x, y in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1), (w // 2, 0), (0, h // 2), (w - 1, h // 2)]:
        if bg[y, x] == 1:
            cv2.floodFill(bg, ff, (x, y), 2)
    fg = (bg != 2).astype(np.uint8)
    n, lab, stt, _ = cv2.connectedComponentsWithStats(fg, 8)   # chỉ giữ khối lớn nhất (đầu + cổ thủ lĩnh), bỏ mẩu bờm đầu khác lọt vào khung
    if n > 2:
        big = 1 + int(np.argmax(stt[1:, cv2.CC_STAT_AREA]))
        fg = (lab == big).astype(np.uint8)
    alpha = cv2.GaussianBlur(fg.astype(np.float32), (0, 0), 0.8)
    rgba = np.dstack([a, (np.clip(alpha * 1.1, 0, 1) * 255).astype(np.uint8)])
    out = Image.fromarray(rgba, "RGBA").resize((512, 512), Image.LANCZOS)
    p = os.path.join(RIG, "chan_dung.png")
    out.save(p, optimize=True)
    print(p)


# ---------------------------------------------------------------- so khung 0 idle với concept (cùng tỉ lệ theo chiều cao hình)
def so_concept(src, out="so_concept.png"):
    """khung t = 0 của idle (runtime Spine thật, có aura giây 0) cạnh concept đã duyệt, co về cùng chiều cao hình bóng. Soi: sừng,
    bờm, số đầu, đuôi, cỡ đầu so với thân phải khớp concept (bài học DAC_TA mục 5)."""
    d = run(f"mode=sheet&n=1&cols=1&tw=1400&th=1000&anims=idle&t0=0&t1=0&view={VIEW}")
    import io
    im = Image.open(io.BytesIO(base64.b64decode(d["sheets"]["idle"].split(",", 1)[1]))).convert("RGB")
    a = np.asarray(im).astype(int)
    a[:26, :300] = (107, 112, 122)   # xoá nhãn chữ
    im = Image.fromarray(a.astype(np.uint8))
    bg = np.array([107, 112, 122])
    m = (np.abs(a - bg).sum(axis=2) > 60)
    ys, xs = np.nonzero(m)
    rig = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    con = Image.open(src).convert("RGB")
    c = np.asarray(con)
    mc = c.min(axis=2) < 236
    ys, xs = np.nonzero(mc)
    con = con.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    H = 700
    rig = rig.resize((max(1, round(rig.width * H / rig.height)), H), Image.LANCZOS)
    con = con.resize((max(1, round(con.width * H / con.height)), H), Image.LANCZOS)
    W_ = con.width + rig.width + 60
    sheet = Image.new("RGB", (W_, H + 60), (236, 236, 232))
    sheet.paste(con, (20, 40))
    sheet.paste(rig, (con.width + 40, 40))
    dr = ImageDraw.Draw(sheet)
    try:
        f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 18)
    except Exception:
        f = None
    dr.text((20, 10), "concept đã duyệt", fill=(20, 20, 20), font=f)
    dr.text((con.width + 40, 10), f"{NAME}: khung 0 idle (runtime Spine, aura giây 0), cùng chiều cao hình", fill=(20, 20, 20), font=f)
    dr.text((20, H + 42), f"rộng/cao: concept {con.width / H:.2f}, rig {rig.width / H:.2f}", fill=(20, 20, 20), font=f)
    p = os.path.join(RIG, out)
    sheet.save(p, optimize=True)
    print(p, f"rộng/cao concept {con.width / H:.2f} vs rig {rig.width / H:.2f}")


# ---------------------------------------------------------------- lệch nối clip đo trên ĐỈNH LƯỚI (mọi slot, kể cả râu, lưỡi, sóng)
def _pose_bones(J, anims_at, bones_setup):
    """ma trận thế giới của từng xương ở dáng = setup + tổng các (clip, t) trong anims_at (xoay/dời cộng, tỉ lệ nhân)."""
    loc = {}
    for b in bones_setup:
        loc[b["name"]] = [b.get("x", 0.0), b.get("y", 0.0), b.get("rotation", 0.0), b.get("scaleX", 1.0), b.get("scaleY", 1.0)]
    for an, t in anims_at:
        for bn, tl in J["animations"][an].get("bones", {}).items():
            if bn not in loc:
                continue
            for kind, ks in tl.items():
                ts = [k.get("time", 0.0) for k in ks]
                if kind == "rotate":
                    loc[bn][2] += float(np.interp(t, ts, [k["value"] for k in ks]))
                elif kind == "translate":
                    loc[bn][0] += float(np.interp(t, ts, [k["x"] for k in ks]))
                    loc[bn][1] += float(np.interp(t, ts, [k["y"] for k in ks]))
                else:
                    loc[bn][3] *= float(np.interp(t, ts, [k["x"] for k in ks]))
                    loc[bn][4] *= float(np.interp(t, ts, [k["y"] for k in ks]))
    W = {}
    for b in bones_setup:
        lx, ly, rot, sx, sy = loc[b["name"]]
        r = math.radians(rot)
        la, lb, lc, ld = math.cos(r) * sx, -math.sin(r) * sy, math.sin(r) * sx, math.cos(r) * sy
        p = b.get("parent")
        if p is None:
            W[b["name"]] = (lx, ly, la, lb, lc, ld)
            continue
        px, py, pa, pb, pc, pd = W[p]
        W[b["name"]] = (pa * lx + pb * ly + px, pc * lx + pd * ly + py, pa * la + pb * lc, pa * lb + pb * ld, pc * la + pd * lc, pc * lb + pd * ld)
    return W


def _slot_alpha(J, an, t, s):
    base = int(s["color"][6:8], 16) / 255.0 if "color" in s else 1.0
    tl = J["animations"][an].get("slots", {}).get(s["name"])
    if not tl:
        return base
    ks = tl["alpha"]
    return float(np.interp(t, [k.get("time", 0.0) for k in ks], [k["value"] for k in ks]))


def lech_dinh():
    """lệch khung cuối mỗi clip không lặp so với khung 0 idle, đo trên đỉnh lưới đã vẽ (sau trọng số, kể cả chuỗi lò xo / dây mềm),
    chỉ slot đang hiện ở khung 0 idle; aura lấy cùng giây 0 ở cả hai bên. In slot lệch nhất (px rig) từng clip."""
    J = json.load(open(os.path.join(RIG, NAME + ".json"), encoding="utf-8"))
    bones = J["bones"]
    atts = J["skins"][0]["attachments"]
    has_aura = "aura" in J["animations"]
    base = [("idle", 0.0)] + ([("aura", 0.0)] if has_aura else [])
    W0 = _pose_bones(J, base, bones)

    def verts(W, s):
        out = []
        for an, a in atts.get(s["name"], {}).items():
            if a.get("type") == "mesh":
                out += mesh_world(a, bones, W)[0]
            elif a.get("type", "region") == "region":
                wx, wy, ma, mb, mc, md = W[s["bone"]]
                ax, ay, aw, ah = a.get("x", 0), a.get("y", 0), a["width"] * a.get("scaleX", 1), a["height"] * a.get("scaleY", 1)
                rr = math.radians(a.get("rotation", 0))
                cs, sn = math.cos(rr), math.sin(rr)
                for qx, qy in ((-aw / 2, ah / 2), (aw / 2, ah / 2), (aw / 2, -ah / 2), (-aw / 2, -ah / 2)):
                    lx, ly = ax + qx * cs - qy * sn, ay + qx * sn + qy * cs
                    out.append((ma * lx + mb * ly + wx, mc * lx + md * ly + wy))
        return np.array(out) if out else None

    vis = [s for s in J["slots"] if not s["name"].startswith("n_") and _slot_alpha(J, "idle", 0.0, s) > 0.05 and s.get("attachment")]
    V0 = {s["name"]: verts(W0, s) for s in vis}
    print("lệch nối clip trên đỉnh lưới (px rig), so với khung 0 idle (+ aura giây 0):")
    rows = []
    for an, A in J["animations"].items():
        if an in ("idle", "aura"):
            continue
        D = max([k.get("time", 0.0) for tl in A.get("bones", {}).values() for ks in tl.values() for k in ks] +
                [k.get("time", 0.0) for tl in A.get("slots", {}).values() for k in tl["alpha"]], default=0.0)
        W1 = _pose_bones(J, [(an, D)] + ([("aura", 0.0)] if has_aura else []), bones)
        worst = []
        for s in vis:
            a1 = _slot_alpha(J, an, D, s)
            v0, v1 = V0[s["name"]], verts(W1, s)
            if v0 is None or v1 is None or len(v0) != len(v1) or a1 < 0.05:   # slot đã tan (die, evolve): không so
                continue
            worst.append((float(np.hypot(*(v1 - v0).T).max()), s["name"]))
        worst.sort(reverse=True)
        top = ", ".join(f"{n} {d:.1f}" for d, n in worst[:4]) if worst else "(mọi slot đã ẩn)"
        print(f"  {an:7s} (D = {D:.2f} s): {top}")
        rows.append((an, D, worst[:4]))
    return rows


# ---------------------------------------------------------------- lệch khung cuối so với idle
def lech():
    J = json.load(open(os.path.join(RIG, NAME + ".json"), encoding="utf-8"))
    anims = J["animations"]

    def pose(an, t):
        out = {}
        for b, tl in anims[an].get("bones", {}).items():
            for kind, ks in tl.items():
                ts = [k.get("time", 0.0) for k in ks]
                if kind == "rotate":
                    vs = [k["value"] for k in ks]
                    out[(b, kind)] = (float(np.interp(t, ts, vs)),)
                else:
                    out[(b, kind)] = (float(np.interp(t, ts, [k["x"] for k in ks])), float(np.interp(t, ts, [k["y"] for k in ks])))
        return out

    p0 = pose("idle", 0.0)
    print("lệch khung cuối mỗi clip so với khung 0 idle (chỉ xương thân; bỏ qua sóng / hiệu ứng):")
    for an, A in anims.items():
        if an in ("idle", "aura"):
            continue
        D = max((k.get("time", 0.0) for tl in A.get("bones", {}).values() for ks in tl.values() for k in ks), default=0.0)
        p1 = pose(an, D)
        worst = []
        for key in set(p0) | set(p1):
            b, kind = key
            if b.startswith(("w", "cr", "dr", "rg", "band", "ripple", "mound", "nuoc", "song")):
                continue
            dflt = {"rotate": (0.0,), "translate": (0.0, 0.0), "scale": (1.0, 1.0)}[kind]
            a0 = p0.get(key, dflt)
            a1 = p1.get(key, dflt)
            if kind == "rotate":
                dv = abs((a0[0] - a1[0] + 180) % 360 - 180)
            else:
                dv = max(abs(x - y) for x, y in zip(a0, a1))
            if kind == "scale":
                dv *= 100
            worst.append((dv, b, kind))
        worst.sort(reverse=True)
        top = ", ".join(f"{b}.{k} {v:.1f}" for v, b, k in worst[:4])
        print(f"  {an:7s} (D = {D:.2f} s): lớn nhất {top}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "sheet"
    if cmd == "sheet":
        n = 12
        clips = None
        extra = ""
        for a in sys.argv[2:]:
            if a.startswith("n="):
                n = int(a[2:])
            elif a.startswith("--q="):
                extra = a[4:]
            else:
                clips = a.split(",")
        sheet(n, clips, extra)
    elif cmd == "can":
        can()
    elif cmd == "luoi":
        luoi()
    elif cmd == "so_sanh":
        so_sanh()
    elif cmd == "chan_dung":
        src, box = None, (600, 40, 1070, 510)
        for a in sys.argv[2:]:
            if a.startswith("--src="):
                src = a[6:]
            elif a.startswith("--box="):
                box = tuple(int(v) for v in a[6:].split(","))
        chan_dung(src, box)
    elif cmd == "lech":
        lech()
    elif cmd == "lech_dinh":
        lech_dinh()
    elif cmd == "so_concept":
        src = next((a[6:] for a in sys.argv[2:] if a.startswith("--src=")), os.path.join(HERE, "inbox", "hai_long", "tai_ve", "L1_duyet.png"))
        so_concept(src)
    else:
        print(__doc__)
