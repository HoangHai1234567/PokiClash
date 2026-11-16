# -*- coding: utf-8 -*-
"""Đo trên rig robot cổ (robot_co_rig.py) các điểm lớp hạt cần bám, rồi SINH Assets/01 Script/Game/Battle/HatRobotBang.cs (chỉ bảng số;
mã hiệu ứng ở HatRobot.cs viết tay).

- attack: `cau_tay` (cầu năng lượng trước ổ nắm đấm tay phải hình) từng khung 30 / giây.
- cast:   `mieng` (cầu to giữa hai bàn tay giơ cao), `cau_tay` + `cau_tay_t` (hai lòng bàn tay) từng khung.
- skill:  `ong_0` (ống giữa = tâm lõi lục giác) từng khung; chỗ miệng ống `ong_<THU[k]>` đúng khung phóng thứ k và hướng tỏa ra từ tâm lõi.
Đơn vị: phần của chiều cao KHAI cho game (`height` trong <tên>_game.json), x về phía trước (phía đối thủ), y lên, gốc = chân.
Đổi clip, tỉ lệ hay hình rig thì xuất rig lại rồi chạy file này.

    py -3 -I ArtGen/Spine/robot_co_do_hat.py           đo cả hai dạng (dạng 1 non: tiền tố Rb1, dạng 2: Rb2) và ghi file C#
"""
import json
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
RA_CS = os.path.join(ROOT, "Assets", "01 Script", "Game", "Battle", "HatRobotBang.cs")


def do_mot():
    """chạy trong tiến trình con (RC_DANG đã đặt): in JSON số đo của dạng hiện tại."""
    import numpy as np
    sys.path.insert(0, HERE)
    import robot_co_rig as R
    import contextlib
    import io
    with contextlib.redirect_stdout(io.StringIO()):
        sk, info = R.dung()
        clips = {c.ten: c for c in R.lam_clip(sk, info)}
    g = json.load(open(os.path.join(R.RA, R.TEN + "_game.json"), encoding="utf-8"))
    cao = float(g["height"])

    def diem(W, bn):
        return [round(float(v), 4) for v in (W[bn][:2, 2] / cao)]

    out = dict(ten=R.TEN, cao=cao, non=bool(R.NON))
    for ten in ("attack", "cast", "skill"):
        c = clips[ten]
        fr = R.nuong(sk, c)
        Ws = [sk.the_gioi(P) for P in fr]
        d = dict(dur=round(c.dur, 4), trung=round(c.gio_trung(), 4), ev=[(round(t, 4), e, p) for t, e, p in c.ev])
        if ten == "attack":
            d["cau"] = [diem(W, "cau_tay") for W in Ws]
        elif ten == "cast":
            d["cau"] = [diem(W, "mieng") for W in Ws]
            d["tay"] = [diem(W, "cau_tay") for W in Ws]
            d["tay_t"] = [diem(W, "cau_tay_t") for W in Ws]
        else:
            d["loi"] = [diem(W, "ong_0") for W in Ws]
            phong = [(t, int(p)) for t, e, p in c.ev if e == "phong"]
            P_, H_ = [], []
            for t, j in phong:
                i = min(len(Ws) - 1, int(round(t * R.FPS)))
                W = Ws[i]
                p = np.array(diem(W, f"ong_{j}"))
                o = np.array(diem(W, "ong_0"))
                v = p - o
                n = float(np.linalg.norm(v))
                P_.append([round(float(x), 4) for x in p])
                H_.append([round(float(x), 4) for x in (v / n if n > 1e-4 else np.array([0.0, 1.0]))])
            d["phong"] = [round(t, 4) for t, _ in phong]
            d["ong"] = P_
            d["huong"] = H_
        out[ten] = d
    print("@@" + json.dumps(out))


def chay(dang):
    env = dict(os.environ)
    env.pop("RC_DANG", None)
    if dang == 1:
        env["RC_DANG"] = "non"
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
        a, c, s = d["attack"], d["cast"], d["skill"]
        tien = f"Rb{k}"
        L.append(f"        // {d['ten']}: chiều cao khai {d['cao']:.1f}; attack {a['dur']:.2f} s trúng {a['trung']:.2f}; cast {c['dur']:.2f} s trúng "
                 f"{c['trung']:.2f}; skill {s['dur']:.2f} s trúng {s['trung']:.2f}")
        L.append(mang(f"{tien}ACauX", [p[0] for p in a["cau"]]))
        L.append(mang(f"{tien}ACauY", [p[1] for p in a["cau"]]))
        for nm, key in (("Cau", "cau"), ("Tay", "tay"), ("TayT", "tay_t")):
            L.append(mang(f"{tien}C{nm}X", [p[0] for p in c[key]]))
            L.append(mang(f"{tien}C{nm}Y", [p[1] for p in c[key]]))
        L.append(mang(f"{tien}SLoiX", [p[0] for p in s["loi"]]))
        L.append(mang(f"{tien}SLoiY", [p[1] for p in s["loi"]]))
        L.append(f"        // chỗ miệng ống ở từng phát (theo thứ tự phóng) và hướng tỏa từ tâm lõi")
        L.append(mang(f"{tien}SOngX", [p[0] for p in s["ong"]]))
        L.append(mang(f"{tien}SOngY", [p[1] for p in s["ong"]]))
        L.append(mang(f"{tien}SHuongX", [p[0] for p in s["huong"]]))
        L.append(mang(f"{tien}SHuongY", [p[1] for p in s["huong"]]))
    d = D[2]
    ev = {n: [(t, e, p) for t, e, p in d[n]["ev"]] for n in ("attack", "cast", "skill")}

    def t_(n, e):
        return next(t for t, e2, _ in ev[n] if e2 == e)

    phong = d["skill"]["phong"]
    for k in (1,):           # hai dạng cùng clip: mốc phải trùng
        for n in ("attack", "cast", "skill"):
            if [list(x[:2]) for x in D[k][n]["ev"]] != [list(x[:2]) for x in ev[n]]:
                raise SystemExit(f"mốc clip {n} của hai dạng khác nhau")
    hang = [
        "        // mốc clip (giây) của rig, chung hai dạng (robot_co_rig.py lam_clip)",
        "        const float RbDt = 1f / 30f;",
        f"        const float RbALead = {d['attack']['trung']:.3f}f, RbATu = {t_('attack', 'tu'):.3f}f, RbABan = {t_('attack', 'ban'):.3f}f;",
        f"        const float RbCLead = {d['cast']['trung']:.3f}f, RbCTu = {t_('cast', 'tu'):.3f}f, RbCXoay = {t_('cast', 'xoay'):.3f}f, "
        f"RbCNem = {t_('cast', 'nem'):.3f}f;",
        f"        const float RbSLead = {d['skill']['trung']:.3f}f, RbSMo = {t_('skill', 'mo_nguc'):.3f}f, RbSDong = {t_('skill', 'dong_nguc'):.3f}f;",
        "        static readonly float[] RbSPhong = { " + ", ".join(f3(v) for v in phong) + " };",
    ]
    cs = f'''// BẢNG SỐ ĐO trên rig robot cổ (suất thiet_phu đảo Kim): FILE SINH TỰ ĐỘNG bởi ArtGen/Spine/robot_co_do_hat.py, đừng sửa tay.
// Phần của chiều cao KHAI cho game (game.json "height"), x về phía trước (phía đối thủ), y lên, gốc = chân; khung 30 / giây từ đầu clip.
// Mã hiệu ứng: HatRobot.cs.
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
        s = D[k]["skill"]
        print(f"dạng {k} ({D[k]['ten']}): cao {D[k]['cao']:.0f}; cầu đánh thường lúc bắn ≈ "
              f"{D[k]['attack']['cau'][int(round(t_('attack', 'ban') * 30))]}; cầu to lúc ném ≈ {D[k]['cast']['cau'][int(round(t_('cast', 'nem') * 30))]}; "
              f"ống đầu {s['ong'][0]}, tâm lõi lúc mở {s['loi'][int(round(0.6 * 30))]}")


if __name__ == "__main__":
    if "--mot" in sys.argv:
        do_mot()
    else:
        main()
