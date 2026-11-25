# -*- coding: utf-8 -*-
"""Trang so sánh các bản phun lửa (chạy 24 khung/giây, nền cát / nền tối).

    py -3 -I xay_trang.py phun_lua,phun_gptA,phun_video      -> xem/so_sanh.html
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MAN = json.load(open(os.path.join(HERE, "frames", "manifest.json"), encoding="utf-8"))
NHAN = {
    "nuoc_bl": "Tia nước bắn · Blender theo clip water (tia mảnh → ống nước phình, vệt lam trôi, dải xoắn, bông gai ở đích, giọt)",
    "phun_lua": "A0 · vẽ bằng code (bản đầu)",
    "phun_gptA": "A · GPT 2.6 vẽ tờ 24 khung (bám khung dáng)",
    "phun_video": "B · video Kling 2.5 từ khung GPT (lửa lỏng)",
    "phun_video2": "B2 · video Kling 2.5, chất lửa + tàn khói (sai)",
    "phun_video3": "B3 · phun của B2, cuối vỡ thành mảnh tàn (như clip giây 19)",
    "phun_bl": "C · dựng bằng Blender (5 lớp màu phẳng, ăn mòn, vỡ mảnh)",
    "phun_bl2": "C2 · Blender, bùng từ từ (mép đầu vươn ra), đứt đuôi xé, tàn bay",
    "cau_bl": "Cầu lửa tròn (lặp) · shader Voronoi lỗ tròn kiểu Blender Box, 4 lớp lồng nhau",
    "no_bl": "Nổ trúng · Blender (sao chớp, lột lớp, mảnh toả)",
    "kim_bl": "Mũi kim lửa (lặp) · Blender",
    "loc_bl": "Lốc xoáy lửa · file mẫu Tornado, màu rực cháy, gió cuốn + khói bụi + tàn tro bay vòng",
    "lua_bl": "Lửa cháy (lặp) · shader Voronoi kiểu Blender Box, giọt lửa lồng nhau, ngọn vệt kem",
    "khoi_bl": "Cụm khói · Blender (múi to vừa nhỏ, đỉnh nhạt đáy đậm, tách cụm rồi tan)",
    "duoi_bl": "Hạt đuôi cầu lửa: lửa đậm → khói (thả dày theo đường bay)",
}

names = sys.argv[1].split(",") if len(sys.argv) > 1 else [k for k in NHAN if k in MAN]
items = [dict(fx=n, label=NHAN.get(n, n), count=MAN[n]["count"]) for n in names if n in MAN]

html = """<!doctype html><html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Bộ lửa Blender</title>
<style>
:root{--bg:#f4efe4;--fg:#2b2118;--card:#fffaf0;--line:#d9ccb3}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.45 system-ui,Segoe UI,sans-serif}
header{padding:14px 18px;display:flex;gap:14px;align-items:center;flex-wrap:wrap}
h1{font-size:18px;margin:0 12px 0 0}
button,select{font:inherit;padding:5px 10px;border:1px solid var(--line);background:var(--card);border-radius:6px;cursor:pointer}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(420px,1fr));gap:14px;padding:0 18px 18px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px}
.card h2{font-size:15px;margin:0 0 8px}
canvas{width:100%;height:auto;border-radius:6px;display:block}
.note{font-size:13px;opacity:.75;margin-top:6px}
</style></head><body>
<header><h1>Bộ lửa dựng bằng Blender</h1>
<button id="play">Tạm dừng</button>
<label>Tốc độ <select id="spd"><option value="1">1×</option><option value="0.5">0.5×</option><option value="0.25">0.25×</option></select></label>
<label>Nền <select id="bgsel"><option value="#E8DCC0">cát (sân trận)</option><option value="#3a3346">tối</option><option value="#9fc6e8">trời</option></select></label>
</header>
<div class="grid" id="grid"></div>
<script>
const ITEMS = __ITEMS__;
const FPS = 24, HOLD = 0.45;
let playing = true, speed = 1, bg = "#E8DCC0";
const players = ITEMS.map(it => {
  const card = document.createElement("div"); card.className = "card";
  card.innerHTML = `<h2>${it.label}</h2><canvas width="660" height="330"></canvas><div class="note">${it.count} khung · ${(it.count / FPS).toFixed(2)} s</div>`;
  document.getElementById("grid").appendChild(card);
  const imgs = [];
  for (let i = 0; i < it.count; i++) { const im = new Image(); im.src = `../frames/${it.fx}/${it.fx}_${String(i).padStart(2, "0")}.png`; imgs.push(im); }
  return {it, cv: card.querySelector("canvas"), imgs};
});
let t = 0, last = performance.now();
function draw(now) {
  const dt = (now - last) / 1000; last = now;
  if (playing) t += dt * speed;
  for (const p of players) {
    const ctx = p.cv.getContext("2d");
    ctx.fillStyle = bg; ctx.fillRect(0, 0, p.cv.width, p.cv.height);
    const total = p.it.count / FPS + HOLD;
    const f = Math.floor((t % total) * FPS);
    const im = p.imgs[Math.min(f, p.it.count - 1)];
    if (f < p.it.count && im.complete && im.naturalWidth) {
      const s = Math.min((p.cv.width - 20) / im.naturalWidth, (p.cv.height - 20) / im.naturalHeight);
      const w = im.naturalWidth * s, h = im.naturalHeight * s;
      ctx.drawImage(im, 10, (p.cv.height - h) / 2, w, h);
    }
  }
  requestAnimationFrame(draw);
}
requestAnimationFrame(draw);
document.getElementById("play").onclick = e => { playing = !playing; e.target.textContent = playing ? "Tạm dừng" : "Chạy"; };
document.getElementById("spd").onchange = e => speed = +e.target.value;
document.getElementById("bgsel").onchange = e => bg = e.target.value;
</script></body></html>
"""
os.makedirs(os.path.join(HERE, "xem"), exist_ok=True)
out = os.path.join(HERE, "xem", "so_sanh.html")
open(out, "w", encoding="utf-8").write(html.replace("__ITEMS__", json.dumps(items, ensure_ascii=False)))
print(out, [i["fx"] for i in items])
