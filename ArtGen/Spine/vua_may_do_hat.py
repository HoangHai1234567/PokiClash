# -*- coding: utf-8 -*-
"""Đo trên hai rig vua robot (.atomik vào game: dạng 1 inbox/vua_may_non/rig/vua_may_non.atomik, dạng 2 inbox/vua_may_1/rig/vua_may.atomik)
chỗ MẶT TRỜI (xương `mieng`, tâm Mặt Trời trên quyền trượng) từng khung 30 / giây ở attack, cast, skill, cùng mốc sự kiện, rồi SINH
Assets/01 Script/Game/Battle/HatVuaBang.cs (chỉ bảng số; mã hiệu ứng ở HatVua.cs viết tay).

Đơn vị: phần của chiều cao KHAI cho game (`game.height`), x về phía trước (phía đối thủ, rig quay phải), y lên, gốc = chân. VmFar<k> =
1130 / height: cột hành tinh / Mặt Trời của chiêu mana dựng trên đầu đối thủ theo bội của 1130 đơn vị rig (vua_may_rig.py cast).
Đổi clip, tỉ lệ hay hình rig thì xuất rig lại rồi chạy file này.

    py -3 -I ArtGen/Spine/vua_may_do_hat.py
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(HERE, "mo_xe"))
import atomik_dang as A  # noqa: E402

RA_CS = os.path.join(ROOT, "Assets", "01 Script", "Game", "Battle", "HatVuaBang.cs")
RIG = {1: os.path.join(HERE, "inbox", "vua_may_non", "rig", "vua_may_non.atomik"), 2: os.path.join(HERE, "inbox", "vua_may_1", "rig", "vua_may.atomik")}
FARU = 1130.0


def do(p):
    J, _, _ = A.load(p)
    cao = float(J["game"]["height"])
    bi = A.bi(J)
    mi = bi["mieng"]
    out = dict(cao=cao, ten=os.path.basename(p))
    for ten in ("attack", "cast", "skill"):
        ci = A.clip(J, ten)
        an = J["anims"][ci]
        n = int(round(an["dur"] * 30)) + 1
        m = []
        for i in range(n):
            P = A.Pose(J).at(ci, min(an["dur"], i / 30))
            m.append((P.w[mi][4] / cao, P.w[mi][5] / cao))
        out[ten] = dict(dur=an["dur"], ev=[(e["t"], e["name"], e.get("s", "")) for e in an.get("ev") or []], m=m)
    # ba thiên thạch của chiêu cuối (xương ff_m<j>, con của far; hình fx_m<j>): chỗ so với far từng khung, giờ hiện / tắt
    si = {s["name"]: i for i, s in enumerate(J["slots"])}
    ci = A.clip(J, "skill")
    an = J["anims"][ci]
    n = int(round(an["dur"] * 30)) + 1
    tt = []
    for j in range(3):
        xs, ys, vis = [], [], []
        for i in range(n):
            P = A.Pose(J).at(ci, min(an["dur"], i / 30))
            b, f = P.w[bi[f"ff_m{j}"]], P.w[bi["far"]]
            xs.append((b[4] - f[4]) / cao)
            ys.append((b[5] - f[5]) / cao)
            vis.append(P.alpha[si[f"fx_m{j}"]] > 0.5 and P.att[si[f"fx_m{j}"]] >= 0)
        hien = [i for i, v in enumerate(vis) if v]
        tt.append((hien[0] / 30, hien[-1] / 30, xs, ys))
    out["thien_thach"] = tt
    return out


def f3(v):
    return f"{v:.3f}f"


def mang(ten, xs):
    return f"        static readonly float[] {ten} = {{ " + ", ".join(f3(v) for v in xs) + " };"


def main():
    D = {k: do(p) for k, p in RIG.items()}
    for n in ("attack", "cast", "skill"):
        if [x[:2] for x in D[1][n]["ev"]] != [x[:2] for x in D[2][n]["ev"]]:
            raise SystemExit(f"mốc clip {n} của hai dạng khác nhau")
    ev = {n: D[2][n]["ev"] for n in ("attack", "cast", "skill")}

    def t_(n, e, s=None):
        return next(t for t, e2, s2 in ev[n] if e2 == e and (s is None or s2 == s))

    no = [t for t, e, _ in ev["skill"] if e == "no"]
    hang = [
        "        // mốc clip (giây) của rig, chung hai dạng (vua_may_rig.py lam_clip)",
        "        const float VmDt = 1f / 30f;",
        f"        const float VmALead = {t_('attack', 'trung'):.3f}f, VmATu = {t_('attack', 'tu'):.3f}f, VmADap = {t_('attack', 'dap'):.3f}f, "
        f"VmAAn = {t_('attack', 'an'):.3f}f;",
        f"        const float VmCLead = {t_('cast', 'trung'):.3f}f, VmCTu = {t_('cast', 'tu'):.3f}f, VmCHang = {t_('cast', 'thang_hang'):.3f}f, "
        f"VmCDinh = {t_('cast', 'len_dinh'):.3f}f, VmCBan = {t_('cast', 'ban'):.3f}f;",
        f"        const float VmSLead = {t_('skill', 'trung'):.3f}f, VmSBay = {t_('skill', 'bay'):.3f}f, VmSQuy = {t_('skill', 'quy_dao'):.3f}f, "
        f"VmSThuc = {t_('skill', 'nhat_thuc'):.3f}f, VmSPhong = {t_('skill', 'phong'):.3f}f, VmSSang = {t_('skill', 'sang'):.3f}f;",
        "        static readonly float[] VmSNo = { " + ", ".join(f3(v) for v in no) + " };",
        "        // giờ hiện / tắt của ba thiên thạch (rig vẽ; hạt chỉ bám theo)",
        "        static readonly float[] VmSMHien = { " + ", ".join(f3(v[0]) for v in D[2]["thien_thach"]) + " };",
        "        static readonly float[] VmSMTat = { " + ", ".join(f3(v[1]) for v in D[2]["thien_thach"]) + " };",
    ]
    L = []
    for k in (1, 2):
        d = D[k]
        L.append(f"        // {d['ten']}: chiều cao khai {d['cao']:.1f}; attack {d['attack']['dur']:.2f} s, cast {d['cast']['dur']:.2f} s, skill "
                 f"{d['skill']['dur']:.2f} s")
        L.append(f"        const float VmFar{k} = {FARU / d['cao']:.4f}f;")
        for cl, ch in (("attack", "A"), ("cast", "C"), ("skill", "S")):
            L.append(mang(f"Vm{k}{ch}MX", [p[0] for p in d[cl]["m"]]))
            L.append(mang(f"Vm{k}{ch}MY", [p[1] for p in d[cl]["m"]]))
        for j, (_, _, xs, ys) in enumerate(d["thien_thach"]):          # so với far (x tới trước, y lên), phần của chiều cao
            L.append(mang(f"Vm{k}T{j}X", xs))
            L.append(mang(f"Vm{k}T{j}Y", ys))
    cs = f'''// BẢNG SỐ ĐO trên rig vua robot (suất kim_nghe đảo Kim): FILE SINH TỰ ĐỘNG bởi ArtGen/Spine/vua_may_do_hat.py, đừng sửa tay.
// Phần của chiều cao KHAI cho game (game.height), x về phía trước (phía đối thủ), y lên, gốc = chân; khung 30 / giây từ đầu clip.
// M = tâm Mặt Trời trên quyền trượng (xương mieng); T<j> = thiên thạch j của chiêu cuối so với điểm đích far. Mã hiệu ứng: HatVua.cs.
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
        d = D[k]
        print(f"dạng {k}: cao {d['cao']:.0f}; Mặt Trời lúc đập (attack {t_('attack', 'dap')}) "
              f"{[round(v, 3) for v in d['attack']['m'][int(round(t_('attack', 'dap') * 30))]]}; lúc nhật thực (skill) "
              f"{[round(v, 3) for v in d['skill']['m'][int(round(t_('skill', 'nhat_thuc') * 30))]]}")


if __name__ == "__main__":
    main()
