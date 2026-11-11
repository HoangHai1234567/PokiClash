# -*- coding: utf-8 -*-
"""Tiến hóa nối liền (pokiclash-spine-rig mục 11): rig dạng k gộp rig dạng k+1 trong một file. Xương dạng sau mang tiền tố n_,
gốc của nó treo dưới xương `evo` (co theo tỉ lệ chiều cao hai dạng); slot dạng sau vẽ sau (trên) slot dạng trước và ẨN mặc định
(clip trận của dạng k không phải khoá gì); clip `evolve` 2,8 s: dạng cũ gồng, tan lúc lốc đậm nhất (VFX lốc là lớp riêng của game,
sự kiện doi_dang), dạng sau hiện lớn dần, gầm, rồi hoà về ĐÚNG khung 0 idle của dạng sau (HeroViewer giữ khung cuối tới khi
sticker dạng mới xong: hai hình trùng khít nên không giật).

    M = tienhoa.gop(skA, skB)
    ev = tienhoa.clip_tien_hoa(M, skA, skB, framesB["idle"][0], tiB=hA / hB, fnA=gong_A, fnB=gam_B)
    xuat.xuat_het(M, clipsA + [ev], ...)        # clip trận của A nướng trên M vẫn đúng (tên xương A giữ nguyên)
"""
import copy

import numpy as np

from . import hoat
from .khung import Sk, Pose, ZERO


def gop(A, B, tien_to="n_", evo="evo", cha=None):
    """M = A + B (B thêm tiền tố). Gốc B (xương đầu tiên của B) thay bằng xương evo, con của cha (mặc định gốc của A)."""
    M = Sk(A.ten)
    M.bones = [dict(b) for b in A.bones]
    M.bi = dict(A.bi)
    M.W0 = {k: v.copy() for k, v in A.W0.items()}
    M.slots = [dict(s) for s in A.slots]
    M.si = dict(A.si)
    M.atts = {k: dict(v) for k, v in A.atts.items()}
    M.images = dict(A.images)
    M.points = dict(A.points)
    M.events = dict(A.events)
    M.luoi = dict(A.luoi)
    M.info = dict(A.info)
    rootA, rootB = A.bones[0]["name"], B.bones[0]["name"]
    M.xuong(evo, cha or rootA)
    for b in B.bones[1:]:
        par = evo if b["parent"] == rootB else tien_to + b["parent"]
        M.xuong(tien_to + b["name"], par, b["x"], b["y"], b["rot"], b["length"], b["sx"], b["sy"], khong_ti_le=b["noScale"])
    for nm, im in B.images.items():
        M.images[tien_to + nm] = im
    alphaB = {}
    for s in B.slots:
        sn = tien_to + s["name"]
        M.slot(sn, tien_to + s["bone"], tien_to + s["att"] if s["att"] else None, an=True)
        alphaB[sn] = s["alpha"]
        for an, spec in B.atts[s["name"]].items():
            sp = dict(spec)
            if "path" in sp:
                sp["path"] = tien_to + sp["path"]
            if "bone" in sp:
                sp["bone"] = tien_to + sp["bone"]
            if sp["type"] == "mesh":
                sp["verts"] = [[(tien_to + b, x, y, w) for b, x, y, w in row] for row in sp["verts"]]
            if sp["type"] == "clipping":
                sp["end"] = tien_to + sp["end"]
            M.atts[sn][tien_to + an] = sp
            if (s["name"], an) in B.luoi:
                M.luoi[(sn, tien_to + an)] = B.luoi[(s["name"], an)]
    for nm, (b, x, y) in B.points.items():
        M.points[tien_to + nm] = (tien_to + b, x, y)
    M.events.update(B.events)
    M.info["alpha_B"] = alphaB
    M.info["tien_to"] = tien_to
    M.info["slots_A"] = [s["name"] for s in A.slots]
    return M


def doi_ten_pose(P, tien_to="n_"):
    Q = Pose()
    Q.t = {tien_to + k: list(v) for k, v in P.t.items()}
    Q.alpha = {tien_to + k: v for k, v in P.alpha.items()}
    Q.att = {tien_to + k: (tien_to + v if v else v) for k, v in P.att.items()}
    return Q


def doi_ten_mem(mem, tien_to="n_"):
    """lò xo / dây mềm của dạng sau chạy trên rig gộp: đổi tên xương."""
    out = []
    for m in mem:
        m2 = copy.copy(m)
        m2.bones = [tien_to + b for b in m.bones]
        out.append(m2)
    return out


def doi_ten_clip(clip, tien_to="n_", ten=None):
    """clip của dạng sau (vd. aura) chạy trên rig gộp: đặt dáng trên Pose tạm rồi đổi tên."""
    f0 = clip.fn

    def fn(t, P):
        Q = Pose()
        f0(t, Q)
        R = doi_ten_pose(Q, tien_to)
        for k, v in R.t.items():
            g = P._g(k)
            g[0] += v[0]
            g[1] += v[1]
            g[2] += v[2]
            g[3] *= v[3]
            g[4] *= v[4]
        P.alpha.update(R.alpha)
        P.att.update(R.att)
    return hoat.Clip(ten or clip.ten, clip.dur, fn, loop=clip.loop, ev=clip.ev, trung=clip.trung, mem=doi_ten_mem(clip.mem, tien_to))


def gop_aura(clipA, clipB, tien_to="n_"):
    """aura của rig gộp = aura dạng cũ + aura dạng sau (đổi tên). Hai clip phải cùng độ dài (hoặc chỉ một bên có)."""
    if clipB is None:
        return clipA
    cb = doi_ten_clip(clipB, tien_to)
    if clipA is None:
        return cb

    def fn(t, P):
        clipA.fn(t, P)
        cb.fn(t, P)
    return hoat.Clip("aura", clipA.dur, fn, loop=True, mem=list(clipA.mem) + list(cb.mem))


def lech_cuoi(M, frames_evolve, B, idleB0, tiB, tien_to="n_"):
    """khung cuối evolve (rig gộp M) so với khung 0 idle của dạng sau B (dạng sau trong M co tiB quanh gốc): lệch lớn nhất theo
    cỡ dạng sau (px rig của B), và slot dạng cũ còn hiện. Trả (lệch, [slot còn hiện], chuỗi báo cáo)."""
    from . import soi
    A, _ = soi.Ve(M).skin(frames_evolve[-1])
    Bi, _ = soi.Ve(B).skin(idleB0)
    dB = {x[0]: x for x in Bi}
    worst = 0.0
    for x in A:
        if x[0].startswith(tien_to) and x[5] > 0.05 and x[0][len(tien_to):] in dB:
            worst = max(worst, float(np.hypot(*(x[2] / tiB - dB[x[0][len(tien_to):]][2]).T).max()))
    vis = [x[0] for x in A if not x[0].startswith(tien_to) and x[5] > 0.02]
    hide = [x[0] for x in Bi if x[5] > 0.05 and tien_to + x[0] not in {y[0] for y in A if y[5] > 0.05}]
    s = f"khung cuối lệch khung 0 idle dạng sau {worst:.2f} px; slot dạng cũ còn hiện: {', '.join(vis) or 'không'}"
    if hide:
        s += f"; slot dạng sau CHƯA hiện: {', '.join(hide)}"
    return worst, vis, s


def clip_tien_hoa(M, A, B, idleB0, tiB=1.0, dur=2.8, fnA=None, fnB=None, tan=(1.05, 1.35), hien=(1.12, 1.45), gam=(1.55, 2.0, 2.4, 2.75),
                  mem=None, evo="evo", ev=None):
    """clip evolve trên rig gộp M. idleB0: Pose khung 0 idle của dạng sau (tên xương của B, chưa tiền tố). tiB: tỉ lệ dạng sau
    trong rig gộp = chiều cao dạng cũ / chiều cao dạng sau (game co mỗi dạng theo game.height của nó). fnA(t, P): động tác dạng
    cũ (gồng, ngửa...) trên xương A; fnB(t, P, fl): động tác dạng sau trên xương n_* với fl = độ gầm 0 → 1 → 0. Không có thì dùng
    nhún, gồng rung đơn giản trên xương "move". Sự kiện: tu_luc (0,3), doi_dang (lúc đổi), gam (dạng sau gầm)."""
    tt = M.info.get("tien_to", "n_")
    alphaB = M.info.get("alpha_B", {})
    slotsA = [(s["name"], s["alpha"]) for s in A.slots]
    endB = doi_ten_pose(idleB0, tt)
    g0, g1, g2, g3 = gam

    def f(t, P):
        aA = 1 - hoat.ease((t - tan[0]) / (tan[1] - tan[0]))
        aB = hoat.ease((t - hien[0]) / (hien[1] - hien[0]))
        if fnA:
            fnA(t, P)
        elif "move" in A.bi:
            sq = hoat.cv(t, [(0, 0), (0.3, -0.08), (0.45, 0.05, "out"), (1.0, 0.03), (1.3, 0.0)])
            P.scale("move", 1 - 0.5 * sq, 1 + sq)
            P.move("move", 2.0 * hoat.rung(t, 0.5, 1.3), 0.0)
        for s, a0 in slotsA:
            if a0 > 0:
                P.alpha[s] = a0 * aA
        for s, a0 in alphaB.items():
            P.alpha[s] = a0 * aB
        P.scale(evo, tiB * hoat.cv(t, [(0, 0.86), (1.0, 0.86), (1.95, 1.0, "out"), (dur, 1.0)]))
        P.move(evo, 0, hoat.cv(t, [(0, -10), (1.0, -10), (1.85, 0, "out"), (dur, 0)]))
        fl = hoat.cv(t, [(0, 0), (g0, 0), (g1, 1, "out"), (g2, 1), (g3, 0, "io"), (dur, 0)])
        if fnB:
            fnB(t, P, fl)
        elif tt + "move" in M.bi:
            P.scale(tt + "move", 1 + 0.06 * fl, 1 + 0.06 * fl)

    def post(t, P):
        w = hoat.ease((t - (dur - 0.35)) / 0.35)
        if w <= 0:
            return
        names = set(endB.t) | {b for b in P.t if b.startswith(tt)}
        for b in names:
            tb = endB.t.get(b, list(ZERO))
            ta = P._g(b)
            for q in range(5):
                ta[q] = ta[q] * (1 - w) + tb[q] * w
        for s, a0 in alphaB.items():
            want = endB.alpha.get(s, a0)
            P.alpha[s] = P.alpha.get(s, a0) * (1 - w) + want * w
        for s, a in endB.att.items():
            if w >= 1:
                P.att[s] = a

    evs = list(ev) if ev is not None else [(0.3, "tu_luc", ""), (0.5 * (tan[0] + hien[1]), "doi_dang", ""), (g1, "gam", "")]
    return hoat.Clip("evolve", dur, f, ev=evs, post=post, mem=mem)
