# Tờ khung và ảnh động duyệt clip máy quả, KHUNG NHÌN CỐ ĐỊNH (khung.mts gọi thẳng lõi AtomSpine, như camera trong game).
# Ra ../xem/<clip>_to.png (tờ khung 15 khung/giây), ../xem/<clip>.gif (30 khung/giây); --lon clip:giây,giây -> ../xem/lon/<clip>_<giây>.png
# Chạy: py -3 -I xem.py [clip ...] [--lon clip:t,t ...] [--khong-gif]
import os, subprocess, sys
from PIL import Image
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ATOM = os.path.abspath(os.path.join(HERE, "..", "atom"))
OUT = os.path.abspath(os.path.join(HERE, "..", "xem"))
TMP = os.path.join(os.environ.get("TEMP", "C:/Temp"), "may_qua_xem")
sys.path.insert(0, HERE)
from atom_cli import TSX, ATOMSPINE  # noqa: E402
import hoat_anh as H  # noqa: E402
BOX = (-560, -40, 560, 1840)          # khung nhìn thế giới: rộng 1120, cao 1880 (đủ cho cú nhảy jackpot)
BG = "F3E9D6"


def khung(clips, fps, w, h, cols, out):
    os.makedirs(out, exist_ok=True)
    env = dict(os.environ, ATOMSPINE_DIR=ATOMSPINE)
    r = subprocess.run(TSX + [os.path.join(HERE, "khung.mts"), ATOM, out, str(fps), ",".join(map(str, BOX)), str(w), str(h), str(cols),
                              ",".join(clips), BG], capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    if r.returncode != 0:
        print((r.stdout + r.stderr)[-1500:])
        raise SystemExit("khung.mts lỗi")
    return r.stdout


def main():
    args = sys.argv[1:]
    lon = [a for i, a in enumerate(args) if i > 0 and args[i - 1] == "--lon"]
    gif = "--khong-gif" not in args
    clips = [a for a in args if a in H.CLIPS] or ([] if lon else list(H.CLIPS))
    os.makedirs(OUT, exist_ok=True)
    if clips:
        # tờ khung 15 khung/giây, ô 168 x 282
        khung(clips, 15, 168, 282, 12, TMP)
        for c in clips:
            Image.open(os.path.join(TMP, f"{c}_sheet.png")).convert("RGB").save(os.path.join(OUT, f"{c}_to.png"))
        if gif:
            W, Hh, cols = 280, 470, 10
            print(khung(clips, 30, W, Hh, cols, os.path.join(TMP, "g")).strip())
            for c in clips:
                sh = Image.open(os.path.join(TMP, "g", f"{c}_sheet.png")).convert("RGB")
                n = int(round(H.CLIPS[c]["dur"] * 30)) + (0 if H.CLIPS[c]["loop"] else 1)
                fr = [sh.crop(((k % cols) * W, (k // cols) * Hh, (k % cols + 1) * W, (k // cols + 1) * Hh)) for k in range(n)]
                if not H.CLIPS[c]["loop"]:
                    fr += [fr[-1]] * 12
                pal = fr[0].quantize(128, method=Image.Quantize.MEDIANCUT)
                fr = [f.quantize(palette=pal, dither=Image.Dither.NONE) for f in fr]
                fr[0].save(os.path.join(OUT, f"{c}.gif"), save_all=True, append_images=fr[1:], duration=33, loop=0, disposal=1)
    for item in lon:
        c, ts = item.split(":")
        os.makedirs(os.path.join(OUT, "lon"), exist_ok=True)
        khung([c], 30, 560, 940, 10, os.path.join(TMP, "l"))
        sh = Image.open(os.path.join(TMP, "l", f"{c}_sheet.png")).convert("RGB")
        for t in ts.split(","):
            k = int(round(float(t) * 30))
            sh.crop(((k % 10) * 560, (k // 10) * 940, (k % 10 + 1) * 560, (k // 10 + 1) * 940)).save(os.path.join(OUT, "lon", f"{c}_{float(t):.2f}.png"))


if __name__ == "__main__":
    main()
