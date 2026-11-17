# -*- coding: utf-8 -*-
"""Đo trên rig thú giáp pháo (thu_phao_rig.py) chỗ HỌNG PHÁO (xương `mieng`, con của bone97) và HƯỚNG NÒNG (trục x của bone97) từng khung
30 / giây ở attack, cast, skill, rồi SINH Assets/01 Script/Game/Battle/HatPhaoBang.cs (chỉ bảng số; mã hiệu ứng ở HatPhao.cs viết tay).

Đơn vị: phần của chiều cao KHAI cho game (`height` trong <tên>_game.json), x về phía trước (phía đối thủ), y lên, gốc = chân. Hướng nòng là
vectơ đơn vị cùng hệ (x tới trước, y lên). Đổi clip, tỉ lệ hay hình rig thì xuất rig lại rồi chạy file này.

    py -3 -I ArtGen/Spine/thu_phao_do_hat.py           đo cả hai dạng (dạng 1 non: tiền tố Pf1, dạng 2: Pf2) và ghi file C#
"""
import json
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
RA_CS = os.path.join(ROOT, "Assets", "01 Script", "Game", "Battle", "HatPhaoBang.cs")


def do_mot():
    """chạy trong tiến trình con (TP_DANG đã đặt): in JSON số đo của dạng hiện tại."""
    import numpy as np
    sys.path.insert(0, HERE)
    import thu_phao_rig as R
    import contextlib
    import io
    with contextlib.redirect_stdout(io.StringIO()):
        sk, info = R.dung()
        clips = {c.ten: c for c in R.lam_clip(sk, info)}
    g = json.load(open(os.path.join(R.RA, R.TEN + "_game.json"), encoding="utf-8"))
    cao = float(g["height"])

    def diem(W, bn):
        return [round(float(v), 4) for v in (W[bn][:2, 2] / cao)]

    def huong(W, bn):
        v = W[bn][:2, 0]
        v = v / max(1e-9, float(np.linalg.norm(v)))
        return [round(float(x), 4) for x in v]

    out = dict(ten=R.TEN, cao=cao, non=bool(R.NON))
    for ten in ("attack", "cast", "skill"):
        c = clips[ten]
        fr = R.nuong(sk, c)
        Ws = [sk.the_gioi(P) for P in fr]
        out[ten] = dict(dur=round(c.dur, 4), trung=round(c.gio_trung(), 4), ev=[(round(t, 4), e, p) for t, e, p in c.ev],
                        mieng=[diem(W, "mieng") for W in Ws], huong=[huong(W, "bone97") for W in Ws], loi=[diem(W, "loi") for W in Ws])
    print("@@" + json.dumps(out))


def chay(dang):
    env = dict(os.environ)
    env.pop("TP_DANG", None)
    env.pop("TP_GOC", None)
    if dang == 1:
        env["TP_DANG"] = "non"
    r = subprocess.run([sys.executable, "-I", os.path.abspath(__file__), "--mot"], env=env, capture_output=True, text=True, encoding="utf-8")
    dong = [x for x in r.stdout.splitlines() if x.startswith("@@")]
    if r.returncode != 0 or not dong:
        print(r.stdout[-3000:], r.stderr[-3000:])
        raise SystemExit(f"đo dạng {dang} hỏng")
    return json.loads(dong[-1][2:])


def f3(v):
    return f"{v:.3f}f"


def mang(ten, xs):
    return f"        static readonly float[] {ten} = {{ " + ", ".join(f3(v) for v in xs) + " };"


def main():
    D = {1: chay(1), 2: chay(2)}
    L = []
    for k in (1, 2):
        d = D[k]
        tien = f"Pf{k}"
        L.append(f"        // {d['ten']}: chiều cao khai {d['cao']:.1f}; attack {d['attack']['dur']:.2f} s trúng {d['attack']['trung']:.2f}; cast "
                 f"{d['cast']['dur']:.2f} s trúng {d['cast']['trung']:.2f}; skill {d['skill']['dur']:.2f} s trúng {d['skill']['trung']:.2f}")
        for cl, ch in (("attack", "A"), ("cast", "C"), ("skill", "S")):
            c = d[cl]
            L.append(mang(f"{tien}{ch}MX", [p[0] for p in c["mieng"]]))
            L.append(mang(f"{tien}{ch}MY", [p[1] for p in c["mieng"]]))
            L.append(mang(f"{tien}{ch}HX", [p[0] for p in c["huong"]]))
            L.append(mang(f"{tien}{ch}HY", [p[1] for p in c["huong"]]))
        L.append(mang(f"{tien}SLX", [p[0] for p in d["skill"]["loi"]]))
        L.append(mang(f"{tien}SLY", [p[1] for p in d["skill"]["loi"]]))
    d = D[2]
    ev = {n: [(t, e, p) for t, e, p in d[n]["ev"]] for n in ("attack", "cast", "skill")}
    for n in ("attack", "cast", "skill"):           # hai dạng cùng clip: mốc phải trùng
        if [list(x[:2]) for x in D[1][n]["ev"]] != [list(x[:2]) for x in ev[n]]:
            raise SystemExit(f"mốc clip {n} của hai dạng khác nhau")

    def t_(n, e):
        return next(t for t, e2, _ in ev[n] if e2 == e)

    ban_c = [t for t, e, _ in ev["cast"] if e == "ban"]
    hang = [
        "        // mốc clip (giây) của rig, chung hai dạng (thu_phao_rig.py lam_clip)",
        "        const float PfDt = 1f / 30f;",
        f"        const float PfALead = {d['attack']['trung']:.3f}f, PfABan = {t_('attack', 'ban'):.3f}f;",
        f"        const float PfCLead = {d['cast']['trung']:.3f}f, PfCNap = {t_('cast', 'nap'):.3f}f;",
        "        static readonly float[] PfCBan = { " + ", ".join(f3(v) for v in ban_c) + " };",
        f"        const float PfSLead = {d['skill']['trung']:.3f}f, PfSGong = {t_('skill', 'gong'):.3f}f, PfSDay = {t_('skill', 'day'):.3f}f, "
        f"PfSBan = {t_('skill', 'ban'):.3f}f;",
    ]
    cs = f'''// BẢNG SỐ ĐO trên rig thú giáp pháo (suất ung_thep đảo Kim): FILE SINH TỰ ĐỘNG bởi ArtGen/Spine/thu_phao_do_hat.py, đừng sửa tay.
// Phần của chiều cao KHAI cho game (game.json "height"), x về phía trước (phía đối thủ), y lên, gốc = chân; khung 30 / giây từ đầu clip.
// M = họng pháo (xương mieng), H = hướng nòng (đơn vị, x tới trước, y lên), L = lõi tròn đuôi pháo. Mã hiệu ứng: HatPhao.cs.
namespace PokiClash
{{
    public sealed partial class HatLua
    {{
{chr(10).join(hang)}

{chr(10).join(L)}
    }}
}}
'''
    open(RA_CS, "w", encoding="utf-8", newline="\n").write(cs)
    print(RA_CS)
    for k in (1, 2):
        dd = D[k]
        ia = int(round(t_("attack", "ban") * 30))
        isk = int(round(t_("skill", "ban") * 30))
        print(f"dạng {k} ({dd['ten']}): cao {dd['cao']:.0f}; họng lúc bắn đánh thường {dd['attack']['mieng'][ia]} hướng {dd['attack']['huong'][ia]}; "
              f"họng lúc bắn chiêu cuối {dd['skill']['mieng'][isk]}; cast bắn đầu {dd['cast']['mieng'][int(round(ban_c[0] * 30))]} "
              f"hướng {dd['cast']['huong'][int(round(ban_c[0] * 30))]}")


if __name__ == "__main__":
    if "--mot" in sys.argv:
        do_mot()
    else:
        main()
