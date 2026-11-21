# Sinh trang nghe thử nhạc + tiếng (ArtGen/Sfx/nghe_thu.html), đường dẫn tương đối tới file âm thanh.
import json, os, sys
from pathlib import Path

ROOT = Path(sys.argv[1])          # d:/PokiClash/ArtGen
SFX = ROOT / "Sfx"
OUT = SFX / "nghe_thu.html"

def rel(p):
    return os.path.relpath(p, SFX).replace("\\", "/")

def kenney(pack, *prefixes):
    d = SFX / "kenney" / pack
    files = sorted(d.rglob("*.ogg"))
    out = []
    for f in files:
        if f.stem.lower() == "preview":
            continue
        if any(f.stem.startswith(p) for p in prefixes):
            out.append((f"{pack.split('-')[0]}:{f.stem}", rel(f)))
    return out

def pin(name):
    fs = sorted((SFX / "pinball").glob(f"{name}_[0-9].mp3"))
    return [(f.stem, rel(f)) for f in fs]

M = ROOT / "Music" / "thu_1122"
music = [
    ("bgm_dao_tho_v3a", "MỚI · Đảo Thổ bản A (cùng họ nhạc cụ các đảo)", "Sunny Canyon Revelry"),
    ("bgm_dao_tho_v3b", "MỚI · Đảo Thổ bản B (guitar, mandolin, nhịp vó)", "The Joyful Quest of Bouncy Crystalline Creatures"),
    ("bgm_dao_tho_v2", "Đảo Thổ v2 (bỏ, để so)", "What Lies Beneath the Canyon"),
    ("bgm_dao_hoa_v2", "Đảo Hỏa v2 (đã duyệt)", "Fiery Adventure Pulse"),
    ("bgm_dao_moc_v2", "Đảo Mộc v2 (đã duyệt)", "The Curious Flute of the Woodland Sprite"),
    ("bgm_maybi_jazz_v2", "Máy bi A swing jazz v2 (đã duyệt)", "Lucky Jamboree"),
    ("bgm_maybi_hoicho_v2", "Máy bi B hội chợ v2 (đã duyệt)", "Joyful Whirlwind"),
    ("bgm_chude_v1", "Chủ đề chính (đã duyệt)", "Ready for Adventure"),
    ("bgm_sanh_v1", "Sảnh / Nhà / Nông trại (đã duyệt)", "Exploring Sunny Shores"),
    ("bgm_dao_thuy_v1", "Đảo Thủy (đã duyệt)", "Lagoon Quest"),
    ("bgm_dao_kim_v1", "Đảo Kim (đã duyệt)", "The Clockwork Explorer's Serenade"),
    ("bgm_tran_v1", "Trận thường (đã duyệt)", "Fierce Whimsy Duel"),
    ("bgm_boss_v1", "Trận boss (đã duyệt)", "Titan's Serenade"),
]
music_items = [(k, label, title, rel(M / f"{k}.mp3")) for k, label, title in music]

pinball = [
    ("dinh", "Bi chạm đinh", "Tiếng lặp nhiều nhất. Game tự đổi cao độ theo combo, nên chọn bản ngắn, gọn, ít đuôi."),
    ("phong_bi", "Phóng bi", "Lúc bấm thả bi."),
    ("roi_o", "Bi rơi vào ô", "Bi chui vào ô thưởng dưới đáy."),
    ("nhat_xp", "+XP", "Ô thường cho XP."),
    ("them_bi", "+bi", "Ô hoặc đinh cho thêm bi."),
    ("dinh_qua", "Bi trúng đinh quà", "Đinh sáng có quà."),
    ("trung_qua", "Trúng rương", "Rương thường."),
    ("jackpot", "Trúng lớn (rương vàng)", "Dài 5 giây, chỉ dùng cho cú lớn."),
    ("doi_cuoc", "Đổi cược ×", "Bấm nút cược."),
    ("dem_so", "Bảng số đếm", "Lặp nhanh khi bảng số chạy."),
    ("len_cap", "Thanh XP máy đầy", "Lên cấp máy."),
    ("bi_chan", "Bị chặn", "Bấm thả khi chưa được thả."),
    ("mo_ruong", "Mở rương", "Nắp rương bật ra."),
]
pin_groups = [(k, label, note, pin(k)) for k, label, note in pinball]
pin_groups.append(("bi_lan", "Bi lăn (lặp, tuỳ chọn)", "Tiếng nền lúc bi đang lăn, có thể không dùng.",
                   [("bi_lan_loop", rel(SFX / "pinball" / "bi_lan_loop.mp3"))]))

ui = [
    ("click", "Nút bấm thường", "Tên trong game: click. Dùng ở hầu hết nút.",
     kenney("interface-sounds", "click_") + kenney("ui-audio", "click", "mouseclick")),
    ("pick", "Chọn (thẻ, tướng, ô)", "Tên trong game: pick. Game đổi cao độ theo thứ tự chọn.",
     kenney("interface-sounds", "select_", "pluck_", "glass_")),
    ("open", "Mở hộp thoại", "Hiện chưa có tiếng riêng (đang dùng whoosh).",
     kenney("interface-sounds", "open_", "maximize_")),
    ("close", "Đóng / quay lại", "Hiện chưa có tiếng riêng.",
     kenney("interface-sounds", "close_", "back_", "minimize_")),
    ("buff", "Xác nhận / thành công", "Tên trong game: buff (đặt tướng, đổi dòng tiềm năng...).",
     kenney("interface-sounds", "confirmation_", "bong_")),
    ("error", "Lỗi / không được", "Tên trong game: error.",
     kenney("interface-sounds", "error_")),
    ("toggle", "Bật tắt", "Công tắc trong cài đặt.",
     kenney("interface-sounds", "toggle_", "switch_")),
    ("tick", "Cuộn / tích tắc", "Cuộn danh sách, bước đếm.",
     kenney("interface-sounds", "tick_", "scroll_")),
    ("drop", "Thả / đặt xuống", "Thả tướng, đặt đồ.",
     kenney("interface-sounds", "drop_")),
    ("card", "Thẻ bài", "Tên trong game: deal, card, swap.",
     kenney("casino-audio", "card-", "cards-")),
    ("coin", "Tiền / phỉnh", "Tên trong game: coin. Cũng thay được cho +bi của máy bi.",
     kenney("casino-audio", "chip")),
]

data = {"music": music_items, "pin": pin_groups, "ui": ui}

html = r"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Nghe thử âm thanh</title>
<style>
:root{--bg:#f6f1e7;--card:#fffdf8;--ink:#2b2420;--muted:#7a6e64;--line:#e3d9cb;--acc:#c8642d;--accbg:#fbe7d9}
@media (prefers-color-scheme:dark){:root{--bg:#1d1a17;--card:#272320;--ink:#f1e9df;--muted:#a89b8e;--line:#3a3430;--acc:#f0965a;--accbg:#3b2a1f}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.45 system-ui,"Segoe UI",sans-serif}
main{max-width:980px;margin:0 auto;padding:20px 16px 160px}
h1{font-size:22px;margin:0 0 4px}h2{font-size:18px;margin:28px 0 8px;border-bottom:2px solid var(--line);padding-bottom:4px}
.sub{color:var(--muted);margin:0 0 12px}
.g{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 12px;margin:8px 0}
.g h3{font-size:15px;margin:0}.g p{margin:2px 0 8px;color:var(--muted);font-size:13px}
.opts{display:flex;flex-wrap:wrap;gap:6px}
.o{display:flex;align-items:center;gap:4px;border:1px solid var(--line);border-radius:8px;padding:3px 6px 3px 4px;background:var(--bg)}
.o.sel{border-color:var(--acc);background:var(--accbg)}
.o button{border:0;background:var(--acc);color:#fff;border-radius:6px;width:28px;height:28px;cursor:pointer;font-size:13px}
.o label{cursor:pointer;font-size:13px;white-space:nowrap}
.trk{display:grid;grid-template-columns:1fr auto;gap:4px 10px;align-items:center}
.trk audio{width:100%;max-width:420px;height:34px}
.trk .t{font-size:12px;color:var(--muted)}
#out{position:fixed;left:0;right:0;bottom:0;background:var(--card);border-top:2px solid var(--line);padding:8px 16px}
#out div{max-width:980px;margin:0 auto;display:flex;gap:8px;align-items:center}
#out textarea{flex:1;height:64px;font:12px ui-monospace,monospace;background:var(--bg);color:var(--ink);border:1px solid var(--line);border-radius:6px;padding:6px}
#out button{background:var(--acc);color:#fff;border:0;border-radius:8px;padding:10px 14px;cursor:pointer}
.vol{margin-left:auto;display:flex;gap:6px;align-items:center;font-size:13px;color:var(--muted)}
</style></head><body><main>
<h1>Nghe thử âm thanh PokiClash</h1>
<p class="sub">Bấm ▶ để nghe, bấm vào tên để chọn bản ưng ý cho từng nhóm. Lựa chọn hiện ở ô dưới cùng: bấm "Chép" rồi dán lại cho Claude.</p>
<div class="vol">Âm lượng <input id="vol" type="range" min="0" max="1" step="0.05" value="0.8"></div>
<h2>Nhạc nền</h2><div id="music"></div>
<h2>Máy bi (gen bằng Magnific)</h2><div id="pin"></div>
<h2>UI (Kenney, CC0)</h2><div id="ui"></div>
</main>
<div id="out"><div><textarea id="sum" readonly></textarea><button id="cp">Chép</button></div></div>
<script>
const D = __DATA__;
const KEY="pokiclash_nghe_thu_v1";
let pick={};try{pick=JSON.parse(localStorage.getItem(KEY)||"{}")}catch(e){}
let cur=null;
const vol=document.getElementById("vol");
function play(src){try{if(cur){cur.pause()}cur=new Audio(src);cur.volume=+vol.value;cur.play()}catch(e){}}
function save(){try{localStorage.setItem(KEY,JSON.stringify(pick))}catch(e){}summary()}
function summary(){const lines=[];
 const add=(sec,list)=>{const p=list.filter(g=>pick[sec+"/"+g]).map(g=>g+"="+pick[sec+"/"+g]);if(p.length)lines.push(sec+": "+p.join(", "))};
 add("nhac",D.music.map(m=>m[0]));add("maybi",D.pin.map(g=>g[0]));add("ui",D.ui.map(g=>g[0]));
 document.getElementById("sum").value=lines.join("\n")||"(chưa chọn gì)"}
function group(host,sec,key,label,note,items){
 const g=document.createElement("div");g.className="g";
 g.innerHTML=`<h3>${label}</h3><p>${note}</p>`;const o=document.createElement("div");o.className="opts";
 const opts=[...items.map(([n,src])=>[n,src]),["không dùng",null]];
 opts.forEach(([n,src])=>{const e=document.createElement("div");e.className="o";
  if(pick[sec+"/"+key]===n)e.classList.add("sel");
  if(src){const b=document.createElement("button");b.textContent="▶";b.onclick=()=>play(src);e.appendChild(b)}
  const l=document.createElement("label");l.textContent=n;l.onclick=()=>{pick[sec+"/"+key]=n;o.querySelectorAll(".o").forEach(x=>x.classList.remove("sel"));e.classList.add("sel");save()};
  e.appendChild(l);o.appendChild(e)});
 g.appendChild(o);host.appendChild(g)}
const mh=document.getElementById("music");
D.music.forEach(([k,label,title,src])=>{const g=document.createElement("div");g.className="g trk";
 g.innerHTML=`<div><h3>${label}</h3><div class="t">${title} · ${k}.mp3</div></div><div></div><audio controls preload="none" src="${src}"></audio>`;
 const a=g.querySelector("audio");a.addEventListener("play",()=>{document.querySelectorAll("audio").forEach(x=>{if(x!==a)x.pause()});if(cur)cur.pause()});
 const o=document.createElement("div");o.className="opts";
 ["ổn","gen lại"].forEach(n=>{const e=document.createElement("div");e.className="o";if(pick["nhac/"+k]===n)e.classList.add("sel");
  const l=document.createElement("label");l.textContent=n;l.onclick=()=>{pick["nhac/"+k]=n;o.querySelectorAll(".o").forEach(x=>x.classList.remove("sel"));e.classList.add("sel");save()};e.appendChild(l);o.appendChild(e)});
 g.appendChild(o);mh.appendChild(g)});
const ph=document.getElementById("pin");D.pin.forEach(([k,l,n,it])=>group(ph,"maybi",k,l,n,it));
const uh=document.getElementById("ui");D.ui.forEach(([k,l,n,it])=>group(uh,"ui",k,l,n,it));
document.getElementById("cp").onclick=()=>{const t=document.getElementById("sum");t.select();try{navigator.clipboard.writeText(t.value)}catch(e){document.execCommand("copy")}};
summary();
</script></body></html>"""

OUT.write_text(html.replace("__DATA__", json.dumps(data, ensure_ascii=False)), encoding="utf-8")
print(OUT, sum(len(g[3]) for g in pin_groups), "pinball,", sum(len(g[3]) for g in ui), "ui,", len(music_items), "music")
missing = [m[3] for m in music_items if not (SFX / m[3]).exists()]
print("missing music:", missing)
