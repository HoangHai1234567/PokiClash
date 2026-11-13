# -*- coding: utf-8 -*-
"""Chụp hình bố cục của một rig .atomik đã đổi tỉ lệ xương, bằng runtime Spine thật (Chrome ngầm).

    py -3 -I bocuc.py <tệp.atomik> <tỉ lệ.json | -> <ra.png> [clip=idle] [giây=0] [--an slot,slot] [--w 1400 --h 1000] [--nen ffffff]
             [--khung x0,y0,x1,y1]  (khung nhìn cố định theo đơn vị rig; không có thì tự ôm hình)

tỉ lệ.json: {"xương": k | [kx, ky], ...} nhân vào scaleX / scaleY dáng gốc (xương con thừa hưởng).
In ra khung ôm hình (đơn vị rig) để dùng lại --khung khi so hai bản.
"""
import base64
import json
import os
import subprocess
import sys
import tempfile

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import atomik_spine as A  # noqa: E402

LIB = os.path.join(os.path.dirname(HERE), "lib", "spine-player.js")
CH = [r"C:\Program Files\Google\Chrome\Application\chrome.exe", r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"]


def opt(a, k, d=None):
    return a[a.index(k) + 1] if k in a else d


def main(a):
    src, ti, out = a[0], a[1], a[2]
    pos = [x for x in a[3:] if not x.startswith("--")]
    # bỏ giá trị của các cờ khỏi pos
    flags = {"--an", "--w", "--h", "--nen", "--khung"}
    pos, i, rest = [], 3, a[3:]
    j = 0
    while j < len(rest):
        if rest[j] in flags:
            j += 2
            continue
        pos.append(rest[j])
        j += 1
    clip = pos[0] if pos else "idle"
    t = float(pos[1]) if len(pos) > 1 else 0.0
    an = [x for x in (opt(a, "--an", "") or "").split(",") if x]
    W, H = int(opt(a, "--w", 1400)), int(opt(a, "--h", 1000))
    nen = opt(a, "--nen", "ffffff")
    khung = opt(a, "--khung")
    sk, atlas, png, J = A.convert(src)
    scales = {} if ti == "-" else (json.load(open(ti, encoding="utf-8")) if os.path.isfile(ti) else json.loads(ti))
    bi = {b["name"]: b for b in sk["bones"]}
    for nm, k in scales.items():
        if nm not in bi:
            raise SystemExit(f"không có xương {nm}")
        if isinstance(k, dict):                 # {"s": k | [kx, ky], "dx": .., "dy": ..} (dời theo hệ cha, đơn vị rig)
            bi[nm]["x"] = bi[nm].get("x", 0) + k.get("dx", 0)
            bi[nm]["y"] = bi[nm].get("y", 0) + k.get("dy", 0)
            k = k.get("s", 1)
        kx, ky = (k, k) if not isinstance(k, list) else k
        bi[nm]["scaleX"] = bi[nm].get("scaleX", 1) * kx
        bi[nm]["scaleY"] = bi[nm].get("scaleY", 1) * ky
    name = J.get("rigName") or "rig"
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0;background:#{nen}}}canvas{{display:block}}</style></head>
<body><canvas id="cv" width="{W}" height="{H}"></canvas><pre id="st">dang</pre>
<script src="{('file:///' + LIB.replace(chr(92), '/'))}"></script><script>
const SKEL = {json.dumps(sk, ensure_ascii=False).replace("</", "<\\/")};
const NAME = {json.dumps(name)}, CLIP = {json.dumps(clip)}, T = {t}, AN = {json.dumps(an)}, KHUNG = {json.dumps([float(v) for v in khung.split(",")] if khung else None)};
const canvas = document.getElementById("cv");
const ctx = new spine.ManagedWebGLRenderingContext(canvas, {{alpha: false, preserveDrawingBuffer: true}});
const am = new spine.AssetManager(ctx, "");
am.setRawDataURI(NAME + ".atlas", "data:text/plain;base64,{base64.b64encode(atlas.encode()).decode()}");
am.setRawDataURI(NAME + ".png", "data:image/png;base64,{base64.b64encode(png).decode()}");
am.loadTextureAtlas(NAME + ".atlas");
function go() {{
  if (!am.isLoadingComplete()) return requestAnimationFrame(go);
  const sd = new spine.SkeletonJson(new spine.AtlasAttachmentLoader(am.require(NAME + ".atlas"))).readSkeletonData(SKEL);
  const s = new spine.Skeleton(sd);
  const st = new spine.AnimationState(new spine.AnimationStateData(sd));
  const e = st.setAnimation(0, CLIP, false);
  e.trackTime = T; st.update(0); st.apply(s);
  for (const n of AN) {{ const sl = s.findSlot(n); if (sl) sl.setAttachment(null); }}
  s.updateWorldTransform(spine.Physics.update);
  const off = new spine.Vector2(), size = new spine.Vector2(); s.getBounds(off, size, []);
  let bx = KHUNG || [off.x, off.y, off.x + size.x, off.y + size.y];
  const r = new spine.SceneRenderer(canvas, ctx);
  const cam = r.camera, pad = 1.06;
  cam.position.x = (bx[0] + bx[2]) / 2; cam.position.y = (bx[1] + bx[3]) / 2;
  cam.zoom = Math.max((bx[2] - bx[0]) * pad / canvas.width, (bx[3] - bx[1]) * pad / canvas.height);
  cam.update();
  const c = [{int(nen[0:2], 16) / 255}, {int(nen[2:4], 16) / 255}, {int(nen[4:6], 16) / 255}];
  ctx.gl.clearColor(c[0], c[1], c[2], 1); ctx.gl.clear(ctx.gl.COLOR_BUFFER_BIT);
  r.begin(); r.drawSkeleton(s, true); r.end();
  document.getElementById("st").textContent = "OK " + [off.x, off.y, off.x + size.x, off.y + size.y].map(v => v.toFixed(1)).join(",");
}}
go();
</script></body></html>"""
    tmp = tempfile.mkdtemp(prefix="bocuc_")
    p = os.path.join(tmp, "p.html")
    open(p, "w", encoding="utf-8").write(html)
    exe = [c for c in CH if os.path.exists(c)][0]
    url = "file:///" + p.replace("\\", "/")
    base = [exe, "--headless=new", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist", "--allow-file-access-from-files",
            "--user-data-dir=" + os.path.join(tmp, "prof"), "--virtual-time-budget=6000", "--hide-scrollbars"]
    r = subprocess.run(base + ["--dump-dom", url], capture_output=True, timeout=180)
    dom = r.stdout.decode("utf-8", "replace")
    import re
    m = re.search(r'id="st">([^<]*)', dom)
    print("trạng thái:", m.group(1) if m else "(không có)")
    subprocess.run(base + [f"--window-size={W},{H}", "--screenshot=" + os.path.abspath(out), url], capture_output=True, timeout=180)
    # cắt bỏ dòng chữ dưới canvas nếu có
    from PIL import Image
    im = Image.open(out).convert("RGB").crop((0, 0, W, H))
    im.save(out)
    print(out, im.size)


if __name__ == "__main__":
    main(sys.argv[1:])
