# Xem clip của cậu thám hiểm ngay trên nền Bến câu (đúng chỗ, đúng cỡ như cảnh A đã duyệt): kết xuất 30 khung/giây bằng khung.mts
# (khung nhìn cố định, nền trong suốt), ghép lên nen_A.png nửa cỡ, xuất GIF + trang xem.
# Cậu đứng giữa bến: gốc mặt đất (0, 0) của rig = điểm (512, 1405) trên nền gốc; cao 610 px nền gốc như cảnh A.
# Ra: xem/<clip>.gif, xem/xem_rig.html. Chạy: py -3 -I xem.py [clip,clip...]
import os, sys, subprocess, shutil
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from atom_cli import TSX, ATOMSPINE  # noqa: E402
import hoat_anh  # noqa: E402

PROJ = os.path.join(HERE, "atom")
OUT = os.path.join(HERE, "xem")
TMP = os.path.join(OUT, "_tmp")
PLATE = os.path.join(HERE, "..", "nen_A.png")
FPS = 30
FEET = (512, 1405)      # px nền gốc
S = 610 / 683.0         # px nền gốc / đơn vị rig
BOX = (-360, -20, 660, 1010)  # hộp thế giới kết xuất
HALF = 0.5              # GIF nửa cỡ nền


def main():
    clips = sys.argv[1].split(",") if len(sys.argv) > 1 else list(hoat_anh.CLIPS)
    os.makedirs(TMP, exist_ok=True)
    k = S * HALF
    w = round((BOX[2] - BOX[0]) * k)
    h = round((BOX[3] - BOX[1]) * k)
    env = dict(os.environ, ATOMSPINE_DIR=ATOMSPINE)
    r = subprocess.run(TSX + [os.path.join(HERE, "khung.mts"), PROJ, TMP, str(FPS), ",".join(map(str, BOX)), str(w), str(h), "10",
                              ",".join(clips), "none"], capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    print(r.stdout.strip())
    if r.returncode:
        print(r.stderr[-2000:])
        raise SystemExit("khung.mts lỗi")
    plate = Image.open(PLATE).convert("RGBA")
    plate = plate.resize((round(plate.width * HALF), round(plate.height * HALF)), Image.LANCZOS)
    px = round((FEET[0] + BOX[0] * S) * HALF)
    py = round((FEET[1] - BOX[3] * S) * HALF)
    # khung GIF: cắt nửa dưới nền quanh cậu cho nhẹ
    crop = (0, 300, plate.width, plate.height)
    for line in r.stdout.strip().splitlines():
        name, n, _ = line.split()
        n = int(n)
        sheet = Image.open(os.path.join(TMP, f"{name}_sheet.png")).convert("RGBA")
        frames = []
        for i in range(n):
            cx, cy = (i % 10) * w, (i // 10) * h
            f = sheet.crop((cx, cy, cx + w, cy + h))
            base = plate.copy()
            base.alpha_composite(f, (px, py))
            frames.append(base.crop(crop).convert("RGB").quantize(colors=200, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE))
        loop = hoat_anh.CLIPS[name][1]
        if not loop:  # clip một lần: giữ khung cuối nửa giây cho dễ nhìn
            frames += [frames[-1]] * 15
        frames[0].save(os.path.join(OUT, f"{name}.gif"), save_all=True, append_images=frames[1:], duration=round(1000 / FPS), loop=0,
                       optimize=False)
        print("gif", name, len(frames))
    shutil.rmtree(TMP, ignore_errors=True)
    cards = "\n".join(f'<figure><img src="{c}.gif" alt="{c}"><figcaption><b>{c}</b> · {hoat_anh.CLIPS[c][0]} s'
                      f'{" · lặp" if hoat_anh.CLIPS[c][1] else ""}</figcaption></figure>' for c in hoat_anh.CLIPS)
    html = f"""<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Bến câu rig</title><style>
:root{{--bg:#f6efdf;--ink:#2b2118;--card:#fffaf0;--line:#e2d3b4}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#1f1a15;--ink:#f1e6d2;--card:#2a231c;--line:#4a3d30}}}}
body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}}
main{{max-width:1400px;margin:0 auto;padding:20px 16px 40px}} h1{{font-size:20px;margin:0 0 12px}}
.g{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}}
figure{{margin:0;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:8px}}
figure img{{width:100%;height:auto;display:block;border-radius:6px}} figcaption{{margin-top:6px;font-size:14px}}
</style></head><body><main><h1>Bến câu: cậu thám hiểm câu cá (AtomSpine, bản rig 1)</h1>
<p>Dây câu và phao do game vẽ (chưa có ở đây). Viền mực vẽ sau cùng khi chốt animation.</p><div class="g">{cards}</div></main></body></html>"""
    open(os.path.join(OUT, "xem_rig.html"), "w", encoding="utf-8").write(html)
    print("trang:", os.path.join(OUT, "xem_rig.html"))


if __name__ == "__main__":
    main()
