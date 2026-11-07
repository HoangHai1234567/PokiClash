"""Bộ đòn của tools/anim_thuy.py: mỗi dạng một hàm dựng clip 1_4 (đánh, 32 khung) và 1_6 (chiêu cuối, 44-48 khung).

Toạ độ đơn vị chiều cao dáng đứng (H), x tới trước, y xuống:
- space "root": theo chân lúc nghỉ, đi theo thân (cú lao, nhún); "foot": theo chân, không theo thân;
- space "far": quanh thân đối thủ ((0, 0) = giữa thân, chân đối thủ ở y ≈ 0,45), trận kéo về đúng chỗ đối thủ; x >= -1 (lệch
  trái hơn thì trận chỉ kéo một phần, như đạn đang bay);
- ("piece", mảnh, điểm): điểm trên mảnh lúc nghỉ, đi theo mảnh.
Khoá: k(khung, kênh=giá trị, e=kiểu nội suy đoạn sau: smooth | lin | in | out | back | hold).
Thân: x y (dời), r (độ, dương theo chiều kim đồng hồ), sx sy; mảnh: r x y sx sy a.
"""
from anim_thuy import Clip, k

ICE = [0.72, 0.86, 0.95, 62, 74, 78]  # nhuộm nước thành băng nhạt (nhân rgb, cộng rgb 0..255)
DARK = [0.5, 0.36, 0.72, 14, 0, 26]  # nước tím than (Lam Quân dạng 3)
JADE = [0.7, 1.0, 0.85, 0, 18, 0]  # nước ngọc bích (Huyền Vũ)
GOLD = [1.0, 0.9, 0.55, 40, 20, 0]  # lấp lánh vàng đồng


def P(r, p, fx=0.5, fy=0.5):
    return ("piece", p, r.part_pt(p, fx, fy))


def to_far(r, pt):
    """điểm clip -> toạ độ space far (đơn vị E quanh F)"""
    return (pt[0] - r.F[0]) / r.E, (pt[1] - r.F[1]) / r.E


# ---------------------------------------------------------------- hiệu ứng

def charge(c, space, f0, f1, size=0.35, tint=None, spin=-1, drops=True, at=None):
    """tụ nước ở một điểm: vòng xoáy co lại, lấp lánh, giọt bay vào (theo thân thì mặc định trước ngực)"""
    ax, ay = at or ((0.35, -0.55) if space in ("root", "foot") else (0, 0))
    c.fx("xoay", [k(f0, x=ax, y=ay, s=1.4, r=0, a=0), k(f0 + 2, a=1), k(f1 - 1, s=0.7, r=spin * 260, a=1), k(f1 + 1, s=0.3, r=spin * 320, a=0)],
         size=size, space=space, tint=tint)
    c.fx("lap", [k(f0 + 2, x=ax, y=ay, s=0.3, r=0, a=0), k((f0 + f1) // 2 + 1, s=1, r=25, a=1), k(f1 + 1, s=0.5, r=50, a=0)],
         size=size * 0.6, space=space, tint=tint)
    if drops:
        for i, (dx, dy, rr) in enumerate([(-0.7, -0.5, -40), (0.6, -0.6, 40), (-0.5, 0.6, -130)]):
            fs = f0 + i * 2
            c.fx("giot", [k(fs, x=ax + dx * size, y=ay + dy * size, s=0.7, r=rr, a=0), k(fs + 2, a=1),
                          k(min(f1, fs + 7), x=ax, y=ay, s=0.25, a=0.2, e="in")], size=size * 0.45, space=space, tint=tint)


def shot(c, img, src, f0, f1, size, tint=None, spin=0, arc=0.0, r0=0, end=(0.0, 0.0), s0=0.6, s1=1.0, flip=False):
    """đạn bay từ điểm clip src tới đối thủ (end trong space far), tới nơi ở khung f1"""
    r = c.r
    x0, y0 = to_far(r, src)
    mid = (f0 + f1) // 2
    ys = [k(f0, y=y0, e="out" if arc else "smooth"), k(f1, y=end[1])] if not arc else \
        [k(f0, y=y0, e="out"), k(mid, y=min(y0, end[1]) - arc, e="in"), k(f1, y=end[1])]
    ks = [k(f0, x=x0, s=s0, r=r0, a=0, e="in"), k(f0 + 1, a=1), k(f1, x=end[0], s=s1, r=r0 + spin, a=1)] + ys
    ks.sort(key=lambda t: t[0])
    c.fx(img, ks + [k(f1 + 1, a=0)], size=size, space="far", tint=tint, vis=(f0, f1), flip=flip)


def impact(c, f, size=1.0, tint=None, ring=True, drops=True, shards=False, burst="no", sparkle=False, y=0.0):
    """nổ trúng ở thân đối thủ: nổ nước, vòng sóng dưới chân, giọt văng (luôn nhỏ hơn thân đối thủ)"""
    c.fx(burst, [k(f - 1, y=y, s=0.3, r=0, a=0), k(f, s=0.75, a=1), k(f + 3, s=1.1, r=20, a=1), k(f + 7, s=1.25, r=35, a=0)],
         size=0.55 * min(size, 1.0), space="far", tint=tint)
    if ring:
        c.fx("vong", [k(f, x=0.02, y=0.44, s=0.35, a=1), k(f + 4, s=1.0, a=0.9), k(f + 9, s=1.35, a=0)], size=1.1 * size,
             space="far", tint=tint, z="back")
    if drops:
        c.fx("giot", [k(f, x=0.05, y=y - 0.1, s=0.5, r=-150, a=1), k(f + 4, x=0.4, y=y - 0.45, s=0.9, a=1, e="out"),
                      k(f + 9, x=0.6, y=y - 0.15, s=0.8, a=0)], size=0.45 * size, space="far", tint=tint)
        c.fx("giot", [k(f + 1, x=0.03, y=y - 0.1, s=0.5, r=-60, a=1), k(f + 5, x=0.15, y=y - 0.6, s=0.8, a=1, e="out"),
                      k(f + 10, x=0.25, y=y - 0.3, s=0.7, a=0)], size=0.4 * size, space="far", tint=tint)
        c.fx("giot", [k(f, x=-0.03, y=y - 0.1, s=0.5, r=150, a=1), k(f + 4, x=-0.4, y=y - 0.4, s=0.85, a=1, e="out"),
                      k(f + 9, x=-0.55, y=y - 0.1, s=0.75, a=0)], size=0.4 * size, space="far", tint=tint, flip=True)
    if shards:
        c.fx("bang", [k(f, x=0.03, y=y, s=0.4, r=0, a=1), k(f + 4, x=0.25, y=y - 0.3, s=1.0, r=35, a=1, e="out"),
                      k(f + 10, x=0.4, y=y - 0.1, s=1.1, r=60, a=0)], size=0.7 * size, space="far", tint=tint)
    if sparkle:
        c.fx("lap", [k(f + 1, x=0.3, y=y - 0.45, s=0.3, a=0), k(f + 4, s=1, r=30, a=1), k(f + 9, s=0.5, r=60, a=0)],
             size=0.35 * size, space="far", tint=GOLD if sparkle == "gold" else None)


def orb_drop(c, f0, fh, size=0.55, h=0.82, tint=None, img="cau", torrent="cot", thick=0.75, swirl=True):
    """quả cầu nước hiện trên đầu đối thủ, xoáy, to dần, rồi xả cột nước thẳng xuống (trúng ở khung fh)"""
    oy = -h
    if swirl:
        c.fx("xoay", [k(f0, x=0.01, y=oy, s=0.4, r=0, a=0), k(f0 + 3, s=1.0, a=1), k(fh, s=1.1, r=-420), k(fh + 3, s=1.35, r=-470, a=0)],
             size=size * 1.5, space="far", tint=tint, z="back")
    c.fx(img, [k(f0, x=0.01, y=oy, s=0.15, r=0, a=0), k(f0 + 4, s=0.85, a=1, e="back"), k(fh - 4, s=1.0, r=-160),
               k(fh - 2, s=1.12, sx=1.08, sy=0.92), k(fh, s=1.0, sx=0.95, sy=1.06, r=-210), k(fh + 5, s=0.7, sx=1, sy=1, a=1),
               k(fh + 9, s=0.25, a=0)], size=size, space="far", tint=tint)
    L = h + 0.45
    c.fx(torrent, [k(fh - 3, x=0.01, y=oy + size * 0.3, sx=0.08, sy=thick * 0.7, r=90, a=1), k(fh, sx=1, sy=thick, e="out"),
                   k(fh + 5, sx=1, sy=thick * 1.05, a=1), k(fh + 9, sy=thick * 0.35, a=0)],
         size=L, space="far", pivot=(0.03, 0.5), tint=tint)


def tsunami(c, f0, fh, size=1.15, tint=None, back=0.3, end=0.06):
    """sóng thần dâng sau lưng đối thủ rồi đổ ập lên (lật ngang cho mào sóng quay về phía đối thủ)"""
    c.fx("than", [k(f0, x=back, y=0.46, s=0.35, sx=1, sy=0.35, r=0, a=0), k(f0 + 3, a=1), k(fh - 3, x=back * 0.6, s=0.9, sy=1.0),
                  k(fh, x=end, s=1.05, sy=1.05, r=-8), k(fh + 5, x=end * 0.5, s=1.1, sy=0.75, r=-14, a=0.9),
                  k(fh + 10, x=0.02, sy=0.3, a=0)], size=size, space="far", pivot=(0.5, 1.0), flip=True, tint=tint)


def geyser(c, f0, fh, size=1.4, tint=None, whirl=1.0, thick=0.85):
    """xoáy nước dưới chân đối thủ, rồi mạch nước phun thẳng lên (trúng ở khung fh)"""
    c.fx("xoay_dat", [k(f0, x=0.02, y=0.45, s=0.3, a=0), k(f0 + 3, s=1.0, a=1), k(fh + 4, s=1.12, a=1), k(fh + 9, s=1.25, a=0)],
         size=1.05 * whirl, space="far", z="back", tint=tint)
    c.fx("cot", [k(fh - 3, x=0.02, y=0.5, sx=0.1, sy=thick * 0.8, r=-90, a=1), k(fh, sx=1, sy=thick, e="out"), k(fh + 5, sx=1.06),
                 k(fh + 10, sx=0.85, sy=thick * 0.4, a=0)], size=size, space="far", pivot=(0.03, 0.5), tint=tint)


def spear_drop(c, f0, fh, size=1.3, tint=None, x=0.02):
    """giáo băng rơi thẳng xuống đối thủ, mũi chạm giữa thân ở khung fh"""
    yc = -size / 2 + 0.05
    c.fx("giao", [k(f0, x=x, y=yc - 2.0, r=90, s=0.7, a=0), k(f0 + 2, a=1, s=1.0), k(fh, y=yc, e="in"), k(fh + 3, y=yc + 0.05, a=1),
                  k(fh + 6, s=1.05, a=0)], size=size, space="far", tint=tint)


def shard_rain(c, f0, fh, n=3, size=0.55, tint=None):
    """mưa mảnh băng rơi chéo xuống đối thủ"""
    for i in range(n):
        fs = f0 + i * 3
        fe = min(fh, fs + 6)
        x0 = 0.55 + 0.18 * i
        c.fx("bang", [k(fs, x=x0, y=-1.7, r=10 * i, s=0.6, a=0), k(fs + 1, a=1), k(fe, x=0.05 + 0.08 * i, y=-0.15 + 0.1 * i, r=40 + 10 * i, s=1.0,
                                                                              e="in"), k(fe + 2, a=0)],
             size=size, space="far", tint=tint)


def rings(c, src, starts, travel=6, size=0.6, tint=None):
    """vòng sóng âm bay từ điểm clip src tới đối thủ, to dần, mỗi vòng bắt đầu ở một khung trong starts"""
    for f0 in starts:
        shot(c, "am", src, f0, f0 + travel, size, tint=tint, s0=0.35, s1=1.15)
        c.fx("am", [k(f0 + travel, s=1.15, a=1), k(f0 + travel + 4, s=1.6, a=0)], size=size, space="far", tint=tint)


def bell_drop(c, pieces, f0, fh, size=0.5, h=0.8, tint=None, sway=True):
    """bản sao chuông hiện trên đầu đối thủ (cao size H), đung đưa ngân, rơi đập lên đỉnh đầu (khung fh), nảy lên rồi tan"""
    r = c.r
    bs = [r.f.bbox(r.rest[p]) for p in pieces]
    hb = (max(b[3] for b in bs) - min(b[1] for b in bs)) / r.H  # cỡ chuông theo H; bản sao trong far nhân thêm E/H
    s = size / hb
    land = -0.42 - size / 2 + 0.12  # đáy chuông chạm đỉnh đầu đối thủ
    ks = [k(f0, x=0.03, y=-h - 0.4, s=s * 0.4, r=0, a=0), k(f0 + 4, y=-h, s=s, a=1, e="back")]
    if sway:
        mid = (f0 + 4 + fh - 4) // 2
        ks += [k(f0 + 4, r=0), k(mid - 3, r=9), k(mid, r=-8), k(mid + 3, r=5), k(fh - 4, r=0)]
    ks += [k(fh - 4, y=-h, sx=1, sy=1), k(fh, y=land, e="in"), k(fh + 1, sx=1.08, sy=0.9), k(fh + 3, y=land - 0.25, sx=1, sy=1, e="out"),
           k(fh + 6, y=land - 0.35, a=1), k(fh + 9, y=land - 0.4, a=0)]
    ks.sort(key=lambda t: t[0])
    c.fx(("copy", pieces), ks, space="far", tint=tint)


# ---------------------------------------------------------------- thân (đòn đứng tại chỗ: thân dời ít)

def cast_body(c, fa, fh, n, back=-6, fwd=5, dy=0.0):
    """ngả ra sau lấy đà (quanh chân) rồi đẩy tới lúc bắn"""
    c.root(k(0, r=0, x=0, y=0, sx=1, sy=1), k(fa, r=back, x=-0.04, y=dy, sx=0.97, sy=1.04), k(fh - 1, r=fwd, x=0.05, sx=1.04, sy=0.97, e="out"),
           k(fh + 4, r=fwd * 0.4, x=0.02, sx=1, sy=1), k(n - 1, r=0, x=0, y=0))


def lunge_body(c, fa, fp, n, dist=0.9, back=-7, fwd=8, hop=0.0):
    """lấy đà rồi lao tới (đỉnh lao ở khung fp, trận lấy làm lúc trúng), lùi về"""
    c.root(k(0, x=0, y=0, r=0, sx=1, sy=1), k(fa, x=-0.1, r=back, sx=0.95, sy=1.06), k(fp - 3, x=dist * 0.8, y=-hop, r=fwd * 0.7, sx=1.06, sy=0.95),
           k(fp, x=dist, y=0, r=fwd, sx=1.04, sy=0.97, e="out"), k(fp + 5, x=dist * 0.55, r=0, sx=1, sy=1), k(n - 1, x=0, y=0, r=0))


def head_bob(c, head, f0, f1, ang=-12):
    c.piece(head, k(0, r=0), k(f0, r=ang), k(f1, r=-ang * 0.5), k(f1 + 6, r=0))


# ================================================================ Lam Quân (rái cá tiểu tướng, chuông đồng)

def lam_quan_1(a):
    """dạng 1: đánh thường gõ chuông bằng đinh ba, sóng âm bay tới; chiêu cuối gọi chuông của mình úp xuống đầu đối thủ"""
    r = a.rig
    bell, arm, head = 7, 17, 14
    tip = r.part_pt(18, 0.95, 0.5)
    # 1_4: giơ đinh ba ra sau gõ chuông (chuông rung), rồi chĩa tới: vòng sóng âm bay tới đối thủ, nổ nước nhỏ
    c = Clip(r, 32)
    c.root(k(0, r=0, x=0), k(8, r=-7, x=-0.05), k(13, r=-4), k(18, r=6, x=0.05, e="out"), k(24, r=2), k(31, r=0, x=0))
    c.piece(arm, k(0, r=0), k(6, r=-55), k(9, r=-62), k(11, r=-40), k(17, r=22, e="out"), k(22, r=14), k(31, r=0))
    c.piece(bell, k(0, r=0), k(9, r=0), k(10, r=-10), k(12, r=8), k(14, r=-6), k(16, r=4), k(19, r=0))
    head_bob(c, head, 9, 17, -6)
    c.fx("am", [k(9, s=0.3, a=1), k(13, s=1.0, a=0)], size=0.45, space=P(r, bell, 0.5, 0.55))
    rings(c, tip, [13], travel=6, size=0.55)
    c.fx("song", [k(14, s=0.4, a=0), k(15, a=1), k(19, s=1.0, a=1), k(20, a=0)], size=0.5, space="far", vis=(14, 19))
    impact(c, 19, size=0.75)
    a.add("1_4", c, hit=19)
    # 1_6: nhảy lên quất đinh ba vào chuông ba nhịp (vòng âm bung quanh chuông), chuông của mình bay lên rồi hiện to trên đầu
    # đối thủ, đung đưa ngân, rơi úp xuống (khung 28), nổ nước, vòng sóng, giọt văng; chuông hiện lại sau lưng
    c = Clip(r, 46)
    c.root(k(0, y=0, sx=1, sy=1, r=0), k(4, y=0.03, sx=1.08, sy=0.9), k(8, y=-0.12, sx=0.95, sy=1.06, e="out"), k(12, y=0, sx=1.05, sy=0.95),
           k(14, sx=1, sy=1), k(22, r=-6), k(27, r=7, e="out"), k(32, r=0), k(45, y=0, r=0))
    c.piece(arm, k(0, r=0), k(5, r=-60), k(7, r=-10), k(9, r=-60), k(11, r=-10), k(13, r=-60), k(15, r=-15), k(22, r=-70), k(27, r=25, e="out"),
            k(34, r=10), k(45, r=0))
    c.piece(bell, k(0, r=0, sx=1, sy=1), k(6, r=-12), k(8, r=10), k(10, r=-12), k(12, r=10), k(14, r=-8), k(16, r=0, sx=1, sy=1),
            k(18, sx=0.6, sy=0.6, a=0.0), k(38, a=0, sx=0.4, sy=0.4), k(42, a=1, sx=1.1, sy=1.1, e="back"), k(45, sx=1, sy=1))
    head_bob(c, head, 22, 27, -10)
    for f0 in (6, 10, 14):
        c.fx("am", [k(f0, s=0.35, a=1), k(f0 + 5, s=1.3, a=0)], size=0.55, space=P(r, bell, 0.5, 0.55))
    c.fx("lap", [k(15, s=0.3, a=0), k(17, s=1.0, r=30, a=1), k(20, s=0.4, r=60, a=0)], size=0.4, space=P(r, bell, 0.5, 0.4),
         tint=GOLD)
    bell_drop(c, [bell], 17, 28, size=0.52, h=0.8)
    c.fx("am", [k(22, x=0.03, y=-0.8, s=0.5, a=1), k(26, s=1.4, a=0)], size=0.55, space="far")
    impact(c, 28, size=1.15, sparkle="gold")
    c.fx("vong", [k(29, x=0.02, y=0.44, s=0.6, a=1), k(36, s=1.8, a=0)], size=1.3, space="far", z="back")
    a.add("1_6", c, hit=28)


def lam_quan_2(a):
    """dạng 2 (đại tướng, đinh ba lớn, chuông khổng lồ): đánh thường xoay đinh ba đập xuống, sóng lưỡi liềm lướt tới, mạch
    nước phun dưới chân đối thủ; chiêu cuối gõ chuông ba nhịp, mỗi nhịp một vòng sóng âm lớn bay tới, nhịp cuối phóng triều
    đinh ba và sóng thần đổ ập"""
    r = a.rig
    bell, arm, head = [28, 29, 35, 36], 10, 24
    tip = r.part_pt(27, 0.9, 0.5)
    bc = r.part_pt(28, 0.5, 0.55)
    c = Clip(r, 32)
    c.root(k(0, r=0, x=0, y=0), k(7, r=-6, x=-0.04, y=0.02), k(12, y=-0.04), k(17, r=6, x=0.05, y=0.02, e="out"), k(23, r=1, y=0), k(31, r=0, x=0))
    c.piece(arm, k(0, r=0), k(6, r=-50), k(10, r=-85), k(13, r=-60), k(17, r=35, e="out"), k(23, r=20), k(31, r=0))
    c.top(arm, 8, 24)
    head_bob(c, head, 8, 17, -6)
    c.fx("no", [k(17, s=0.3, a=1), k(20, s=0.8, a=0)], size=0.45, space=P(r, 27, 0.9, 0.5))
    c.fx("song", [k(15, x=-0.25, y=0.35, s=0.4, a=0), k(16, a=1), k(19, x=0.0, y=0.35, s=1.0, e="lin"), k(20, a=0)], size=0.65, space="far")
    geyser(c, 12, 19, size=1.35)
    impact(c, 19, size=0.8, ring=False)
    a.add("1_4", c, hit=19)
    # 1_6
    c = Clip(r, 48)
    c.root(k(0, r=0, x=0), k(5, r=-5, x=-0.03), k(9, r=3), k(13, r=-5), k(17, r=3), k(21, r=-7), k(27, r=8, x=0.05, e="out"), k(34, r=1), k(47, r=0, x=0))
    c.piece(arm, k(0, r=0), k(5, r=-60), k(8, r=-20, e="out"), k(12, r=-60), k(15, r=-20, e="out"), k(19, r=-75), k(26, r=40, e="out"), k(34, r=15),
            k(47, r=0))
    c.top(arm, 3, 34)
    c.piece(28, k(0, r=0), k(8, r=-9), k(10, r=7), k(15, r=-9), k(17, r=7), k(21, r=-6), k(23, r=4), k(27, r=-10), k(30, r=6), k(34, r=0))
    head_bob(c, head, 20, 27, -9)
    for f0, sz in ((8, 0.7), (15, 0.85), (26, 1.05)):
        c.fx("am", [k(f0, s=0.35, a=1), k(f0 + 5, s=1.4, a=0)], size=sz, space=("piece", 28, bc))
    rings(c, bc, [9, 16], travel=6, size=0.75)
    shot(c, "tia_trieu", tip, 26, 30, 1.1, s0=0.5, s1=1.0)
    tsunami(c, 22, 30, size=1.25)
    impact(c, 30, size=1.2, sparkle="gold")
    c.fx("lap", [k(10, x=0.2, y=-0.5, s=0.3, a=0), k(12, s=1, r=40, a=1), k(15, s=0.4, a=0)], size=0.35, space="far", tint=GOLD)
    c.fx("lap", [k(17, x=0.1, y=-0.6, s=0.3, a=0), k(19, s=1, r=40, a=1), k(22, s=0.4, a=0)], size=0.35, space="far", tint=GOLD)
    a.add("1_6", c, hit=30)


def lam_quan_3(a):
    """dạng 3 (thống soái cánh cá đuối đen, nước tím than): đánh thường vỗ cánh tung hai sóng lưỡi liềm tím; chiêu cuối bay
    lên trên cánh đen, chuông đen hiện trên đầu đối thủ giữa xoáy tím ngân hai nhịp, sóng thần tím đổ ập rồi chuông úp xuống"""
    r = a.rig
    bell, wing, head, arm = [28], 4, 9, 22
    c = Clip(r, 32)
    c.root(k(0, r=0, x=0, y=0), k(7, r=-6, x=-0.04, y=-0.03), k(13, y=-0.06), k(17, r=6, x=0.05, y=0, e="out"), k(31, r=0, x=0, y=0))
    c.piece(wing, k(0, r=0, sy=1), k(7, r=-14, sy=1.12), k(12, r=-18), k(16, r=12, sy=0.9, e="out"), k(22, r=4, sy=1), k(31, r=0))
    c.piece(arm, k(0, r=0), k(8, r=-35), k(16, r=25, e="out"), k(31, r=0))
    c.piece(2, k(0, y=0), k(12, y=-0.06), k(20, y=0.02), k(31, y=0))
    w0 = r.pt(0.35, -0.5)
    shot(c, "song", w0, 12, 18, 0.62, tint=DARK, end=(0.03, -0.12))
    shot(c, "song", r.pt(0.3, -0.25), 14, 19, 0.55, tint=DARK, end=(0.02, 0.05), flip=False)
    c.fx("xoay", [k(5, y=-0.45, s=0.4, a=0), k(8, a=1), k(14, s=1.0, r=-240, a=0)], size=0.5, space="root", tint=DARK, z="back",
         vis=(5, 14))
    impact(c, 19, size=0.8, tint=DARK)
    a.add("1_4", c, hit=19)
    # 1_6: bay lên (thân nhấc 0,22H, cánh vỗ), chuông đen hiện giữa xoáy tím trên đầu đối thủ, ngân hai nhịp vòng tím, sóng thần tím
    c = Clip(r, 48)
    c.root(k(0, y=0, r=0, x=0, sx=1, sy=1), k(4, y=0.03, sx=1.06, sy=0.93), k(10, y=-0.22, sx=1, sy=1, e="out"), k(14, y=-0.18), k(18, y=-0.24),
           k(22, y=-0.2), k(26, y=-0.24, r=-6), k(31, y=-0.12, r=7, e="out"), k(38, y=0, r=0), k(47, y=0, r=0))
    c.piece(wing, k(0, r=0, sy=1), k(6, r=-20, sy=1.15), k(9, r=14, sy=0.9), k(13, r=-20, sy=1.15), k(16, r=14, sy=0.9), k(20, r=-20, sy=1.15),
            k(23, r=10, sy=0.92), k(27, r=-22, sy=1.15), k(31, r=16, sy=0.9, e="out"), k(38, r=0, sy=1))
    c.piece(arm, k(0, r=0), k(10, r=-50), k(26, r=-60), k(31, r=30, e="out"), k(40, r=0))
    c.piece(28, k(0, a=1, sx=1, sy=1), k(10, a=1), k(14, a=0, sx=0.5, sy=0.5), k(40, a=0, sx=0.5, sy=0.5), k(44, a=1, sx=1.08, sy=1.08, e="back"),
            k(47, sx=1, sy=1))
    head_bob(c, head, 24, 31, -10)
    c.fx("xoay", [k(4, y=-0.45, s=0.4, a=0), k(8, s=1.1, a=1), k(30, s=1.2, r=-900), k(34, s=1.4, a=0)], size=0.9, space="root", tint=DARK, z="back")
    c.fx("xoay", [k(12, x=0.03, y=-0.82, s=0.4, a=0), k(16, s=1.0, a=1), k(30, s=1.1, r=-700), k(33, s=1.2, a=0)], size=0.75, space="far",
         tint=DARK, z="back")
    bell_drop(c, bell, 12, 34, size=0.55, h=0.82, tint=[0.55, 0.5, 0.75, 0, 0, 20])
    for f0 in (18, 24):
        c.fx("am", [k(f0, x=0.03, y=-0.82, s=0.45, a=1), k(f0 + 6, s=1.6, a=0)], size=0.65, space="far", tint=DARK)
    tsunami(c, 19, 27, size=1.25, tint=DARK)
    impact(c, 34, size=1.0, tint=DARK)
    c.fx("vong", [k(35, x=0.02, y=0.44, s=0.6, a=1), k(42, s=1.9, a=0)], size=1.35, space="far", tint=DARK, z="back")
    a.add("1_6", c, hit=34)


# ================================================================ Thương Lam (rồng biển băng)

def thuong_lam_1(a):
    """dạng 1 (rồng con): đánh thường hít hơi phun mũi giáo băng; chiêu cuối chồm lên, cầu băng hiện trên đầu đối thủ, mưa
    mảnh băng rồi giáo băng lớn cắm xuống"""
    r = a.rig
    head, wing, tail = 13, 17, 9
    mouth = r.part_pt(14, 0.9, 0.6)
    c = Clip(r, 32)
    c.root(k(0, r=0, x=0, sy=1, sx=1), k(9, r=-8, x=-0.05, sy=1.05, sx=0.96), k(15, r=-9), k(18, r=7, x=0.06, sy=0.95, sx=1.05, e="out"),
           k(24, r=2, sy=1, sx=1), k(31, r=0, x=0))
    c.piece(head, k(0, r=0), k(9, r=-16), k(15, r=-18), k(18, r=12, e="out"), k(25, r=3), k(31, r=0))
    c.piece(wing, k(0, r=0), k(9, r=-18), k(18, r=12), k(31, r=0))
    c.piece(tail, k(0, r=0), k(9, r=12), k(18, r=-10), k(31, r=0))
    charge(c, ("piece", head, mouth), 6, 16, size=0.3, tint=ICE)
    shot(c, "giao", mouth, 16, 20, 0.6, s0=0.5, s1=1.0)
    impact(c, 20, size=0.8, tint=ICE, shards=True)
    a.add("1_4", c, hit=20)
    c = Clip(r, 46)
    c.root(k(0, r=0, y=0, sx=1, sy=1), k(5, sy=0.92, sx=1.06), k(11, r=-10, y=-0.08, sy=1.05, sx=0.97, e="out"), k(24, r=-12, y=-0.1),
           k(28, r=7, y=0, sy=0.95, sx=1.05, e="out"), k(34, r=0, sy=1, sx=1), k(45, r=0))
    c.piece(head, k(0, r=0), k(11, r=-22), k(24, r=-25), k(28, r=14, e="out"), k(36, r=0))
    c.piece(wing, k(0, r=0), k(8, r=-25), k(12, r=10), k(16, r=-25), k(20, r=10), k(24, r=-28), k(28, r=15), k(36, r=0))
    c.piece(tail, k(0, r=0), k(11, r=15), k(24, r=18), k(28, r=-12), k(38, r=0))
    c.fx("lap", [k(9, s=0.3, a=0), k(12, s=1.0, r=30, a=1), k(16, s=0.4, r=60, a=0)], size=0.35, space=P(r, head, 0.6, 0.2), tint=ICE)
    orb_drop(c, 10, 28, size=0.5, h=0.82, tint=ICE, torrent="giao", thick=1.0)
    shard_rain(c, 15, 26, n=3, size=0.45, tint=None)
    impact(c, 28, size=0.95, tint=ICE, shards=True, sparkle=True)
    a.add("1_6", c, hit=28)


def thuong_lam_2(a):
    """dạng 2: đánh thường lao tới quét cánh băng (cận chiến); chiêu cuối vỗ cánh bay lên, sóng thần băng đổ ập, ba giáo băng
    cắm xuống liên tiếp"""
    r = a.rig
    head, wing, tail = 9, 10, 5
    c = Clip(r, 32)
    lunge_body(c, 8, 18, 32, dist=0.95, back=-8, fwd=9, hop=0.05)
    c.piece(wing, k(0, r=0), k(8, r=-30), k(15, r=-35), k(18, r=28, e="out"), k(25, r=5), k(31, r=0))
    c.top(wing, 12, 24)
    c.piece(head, k(0, r=0), k(8, r=-10), k(18, r=10), k(31, r=0))
    c.piece(tail, k(0, r=0), k(8, r=15), k(18, r=-15), k(31, r=0))
    c.fx("song", [k(16, x=0.75, y=-0.45, s=0.5, r=-20, a=0), k(17, a=1), k(20, x=1.05, y=-0.35, s=1.0, r=10), k(23, a=0)], size=0.75,
         space="root", tint=ICE)
    c.fx("bang", [k(18, x=1.1, y=-0.45, s=0.4, r=0, a=1), k(22, x=1.35, y=-0.75, s=1.0, r=40, e="out"), k(27, x=1.45, y=-0.55, a=0)],
         size=0.55, space="root")
    a.add("1_4", c, lunge=True)
    c = Clip(r, 48)
    c.root(k(0, y=0, r=0, sx=1, sy=1), k(5, sy=0.9, sx=1.07), k(11, y=-0.16, sy=1.04, sx=0.97, e="out"), k(15, y=-0.12), k(19, y=-0.18),
           k(23, y=-0.13), k(27, y=-0.2, r=-8), k(31, y=-0.05, r=8, e="out"), k(38, y=0, r=0, sx=1, sy=1), k(47, y=0))
    c.piece(wing, k(0, r=0), k(7, r=-35), k(10, r=15), k(14, r=-35), k(17, r=15), k(21, r=-35), k(24, r=15), k(28, r=-40), k(31, r=30, e="out"),
            k(38, r=0))
    c.piece(head, k(0, r=0), k(11, r=-15), k(27, r=-20), k(31, r=12), k(38, r=0))
    c.piece(tail, k(0, r=0), k(11, r=12), k(20, r=-8), k(28, r=14), k(32, r=-12), k(40, r=0))
    c.fx("xoay", [k(6, y=-0.45, s=0.4, a=0), k(10, s=1.0, a=1), k(28, s=1.1, r=-600), k(32, s=1.3, a=0)], size=0.8, space="root", tint=ICE, z="back")
    tsunami(c, 18, 30, size=1.2, tint=ICE)
    for i, fh in enumerate((27, 30, 33)):
        spear_drop(c, fh - 6, fh, size=0.75 if i != 1 else 1.0, x=0.02 + 0.22 * (i % 2) * (1 if i else 0))
    impact(c, 30, size=0.95, tint=ICE, shards=True, ring=True)
    a.add("1_6", c, hit=30)


def thuong_lam_3(a):
    """dạng 3 (rồng lam cánh băng): đánh thường vỗ hai cánh tung ba giáo băng xoè quạt; chiêu cuối Băng Long Thiên Giáng: chồm
    bay lên dang cánh, xoáy băng và cầu băng tụ trên đầu đối thủ, mảnh băng xoay quanh, rồng hất đầu: giáo băng khổng lồ cắm
    xuống, băng vỡ tung, hai giáo nhỏ cắm theo"""
    r = a.rig
    head, w1, w2, tail, neck = 26, 15, 20, 11, 18
    mouth = r.part_pt(head, 0.95, 0.6)
    c = Clip(r, 32)
    c.root(k(0, r=0, x=0, y=0), k(8, r=-6, x=-0.04, y=-0.03), k(14, r=-7, y=-0.05), k(18, r=5, x=0.05, y=0, e="out"), k(31, r=0, x=0, y=0))
    c.piece([w1, w2], k(0, r=0), k(8, r=-22), k(13, r=-26), k(17, r=18, e="out"), k(23, r=4), k(31, r=0))
    c.piece(head, k(0, r=0), k(8, r=-10), k(17, r=8), k(31, r=0))
    c.piece(neck, k(0, r=0), k(8, r=-6), k(17, r=6), k(31, r=0))
    c.piece(tail, k(0, r=0), k(8, r=10), k(17, r=-8), k(31, r=0))
    for i, (f0, ey) in enumerate(((13, -0.35), (15, 0.0), (17, 0.3))):
        src = r.pt(0.35, -0.75 + 0.18 * i)
        shot(c, "giao", src, f0, f0 + 4, 0.55, end=(0.04, ey * 0.6), r0=-8 + 8 * i)
    c.fx("lap", [k(9, x=0.2, y=-0.9, s=0.3, a=0), k(12, s=1, r=30, a=1), k(15, s=0.4, a=0)], size=0.3, space="root", tint=ICE)
    impact(c, 21, size=0.9, tint=ICE, shards=True)
    a.add("1_4", c, hit=21)
    c = Clip(r, 50)
    c.root(k(0, y=0, r=0, x=0, sx=1, sy=1), k(5, sy=0.92, sx=1.05), k(12, y=-0.14, r=-7, sy=1.04, sx=0.97, e="out"), k(17, y=-0.1, r=-6),
           k(22, y=-0.16, r=-9), k(27, y=-0.18, r=-10), k(30, y=-0.04, r=7, x=0.04, sx=1.04, sy=0.96, e="out"), k(37, y=0, r=0, x=0, sx=1, sy=1),
           k(49, y=0, r=0))
    c.piece([w1, w2], k(0, r=0, sy=1), k(6, r=-20), k(12, r=-42, sy=1.08), k(15, r=-30), k(18, r=-44), k(21, r=-30), k(24, r=-44),
            k(27, r=-48, sy=1.1), k(30, r=24, sy=0.95, e="out"), k(37, r=4, sy=1), k(49, r=0))
    c.piece(head, k(0, r=0), k(12, r=-24), k(27, r=-26), k(30, r=14, e="out"), k(38, r=0))
    c.piece(neck, k(0, r=0), k(12, r=-10), k(27, r=-12), k(30, r=8, e="out"), k(38, r=0))
    c.piece(tail, k(0, r=0), k(12, r=14), k(20, r=6), k(27, r=16), k(31, r=-14), k(40, r=0))
    c.fx("xoay", [k(4, y=-0.45, s=0.4, a=0), k(9, s=1.0, a=1), k(28, s=1.1, r=-700), k(32, s=1.3, a=0)], size=0.85, space="root", tint=ICE, z="back")
    for i, (dx, dy, f0) in enumerate(((0.1, -1.1, 10), (0.5, -0.8, 13), (-0.25, -0.6, 16))):
        c.fx("lap", [k(f0, x=dx, y=dy, s=0.3, a=0), k(f0 + 3, s=1.0, r=30, a=1), k(f0 + 7, s=0.4, r=60, a=0)], size=0.3, space="root", tint=ICE)
    # trên đầu đối thủ: xoáy băng, cầu băng, mảnh băng xoay quanh
    oy = -0.82
    c.fx("xoay", [k(9, x=0.02, y=oy, s=0.3, r=0, a=0), k(13, s=1.0, a=1), k(30, s=1.15, r=-820), k(33, s=1.35, a=0)], size=0.62,
         space="far", tint=ICE, z="back")
    c.fx("cau", [k(11, x=0.02, y=oy, s=0.15, a=0), k(15, s=0.8, a=1, e="back"), k(27, s=1.05, r=-200), k(30, s=1.15, r=-240),
                 k(32, s=0.4, a=0)], size=0.42, space="far", tint=ICE)
    for i in range(3):
        ang = i * 120
        import math
        ks = []
        for f in range(14, 30, 2):
            t = math.radians(ang + (f - 14) * 28)
            ks.append(k(f, x=0.02 + 0.42 * math.cos(t), y=oy + 0.16 * math.sin(t), s=0.75, r=(f - 14) * 20, a=1))
        ks[0] = (ks[0][0], dict(ks[0][1], a=0))
        c.fx("bang", ks + [k(31, a=0)], size=0.32, space="far", tint=None)
    spear_drop(c, 26, 32, size=1.15)
    spear_drop(c, 30, 35, size=0.7, x=0.4)
    spear_drop(c, 32, 37, size=0.6, x=0.15)
    impact(c, 32, size=1.0, tint=ICE, shards=True, sparkle=True)
    c.fx("vong", [k(33, x=0.02, y=0.44, s=0.6, a=1), k(41, s=1.7, a=0)], size=1.3, space="far", tint=ICE, z="back")
    a.add("1_6", c, hit=32)


# ================================================================ Huyền Vũ (rùa ngọc, mai đen viền đồng)

def huyen_vu_1(a):
    """dạng 1 (rùa con, ngọc trai đen bay trên đầu): đánh thường phóng ngọc trai trong xoáy nước ngọc bích; chiêu cuối dậm
    hai nhịp, xoáy nước dưới chân đối thủ, mạch nước phun"""
    r = a.rig
    pearl, head = 22, 12
    pc = r.center(pearl)
    c = Clip(r, 32)
    c.root(k(0, r=0, sx=1, sy=1), k(8, r=-6, sy=1.05, sx=0.96), k(15, r=5, sy=0.95, sx=1.05, e="out"), k(22, r=0, sx=1, sy=1), k(31, r=0))
    c.piece(head, k(0, r=0), k(8, r=-12), k(15, r=10), k(31, r=0))
    c.piece(pearl, k(0, y=0, a=1, sx=1, sy=1), k(8, y=-0.08), k(12, y=0.0, a=1), k(13, a=0), k(26, a=0, sx=0.4, sy=0.4), k(30, a=1, sx=1.1, sy=1.1, e="back"),
            k(31, sx=1, sy=1))
    c.fx("xoay", [k(4, s=0.3, a=0), k(7, s=1.0, a=1), k(13, s=0.7, r=-300, a=1), k(14, a=0)], size=0.4, space=("piece", pearl, pc), tint=JADE)
    shot(c, ("copy", [pearl]), pc, 13, 19, 1.0, spin=-360)
    shot(c, "xoay", pc, 13, 19, 0.45, tint=JADE, spin=-500)
    impact(c, 19, size=0.75, tint=JADE)
    a.add("1_4", c, hit=19)
    c = Clip(r, 46)
    c.root(k(0, y=0, sx=1, sy=1), k(5, y=-0.1, sy=1.06, sx=0.95, e="out"), k(8, y=0, sy=0.88, sx=1.1, e="in"), k(11, sy=1, sx=1),
           k(15, y=-0.12, sy=1.06, sx=0.95, e="out"), k(18, y=0, sy=0.86, sx=1.12, e="in"), k(22, sy=1, sx=1), k(45, y=0))
    c.piece(head, k(0, r=0), k(5, r=-15), k(8, r=8), k(15, r=-15), k(18, r=10), k(24, r=-8), k(30, r=6), k(40, r=0))
    c.piece(pearl, k(0, y=0, sx=1, sy=1), k(10, y=-0.15, sx=1.25, sy=1.25), k(20, y=-0.2, sx=1.35, sy=1.35), k(26, sx=1.0, sy=1.0, y=-0.05),
            k(30, sx=1.3, sy=1.3), k(40, y=0, sx=1, sy=1))
    for f in (8, 18):
        c.fx("vong", [k(f, s=0.4, a=1), k(f + 6, s=1.3, a=0)], size=0.9, space="root", tint=JADE, z="back")
    c.fx("lap", [k(20, s=0.3, a=0), k(23, s=1.0, r=40, a=1), k(27, s=0.4, a=0)], size=0.35, space=("piece", pearl, pc), tint=JADE)
    geyser(c, 12, 26, size=1.45, tint=JADE)
    impact(c, 26, size=0.9, tint=JADE, ring=False)
    c.fx("giot", [k(27, x=0.05, y=-1.0, s=0.6, a=1, r=0), k(33, x=0.35, y=-0.2, s=0.9, r=30, a=0, e="in")], size=0.45, space="far", tint=JADE)
    a.add("1_6", c, hit=26)


def huyen_vu_2(a):
    """dạng 2 (rùa biển ngọc): đánh thường chồm dậm hai chân trước, ba vòng sóng lan tới, mạch nước phun dưới đối thủ; chiêu cuối
    xoay tròn trong mai giữa lốc nước, phóng tia xoắn, xoáy nước dưới chân đối thủ, sóng thần ngọc"""
    r = a.rig
    head, f1, f2 = 17, 2, 6
    c = Clip(r, 32)
    c.root(k(0, r=0, y=0, sx=1, sy=1), k(8, r=-9, y=-0.05, sy=1.05, sx=0.96, e="out"), k(12, r=-10), k(15, r=3, y=0, sy=0.88, sx=1.1, e="in"),
           k(19, r=0, sy=1, sx=1), k(31, r=0))
    c.piece([f1, f2], k(0, r=0), k(8, r=-25), k(12, r=-28), k(15, r=15, e="in"), k(22, r=0))
    c.piece(head, k(0, r=0), k(8, r=-14), k(15, r=8), k(31, r=0))
    for i, f0 in enumerate((15, 17, 19)):
        c.fx("vong", [k(f0, x=0.5 + 0.0 * i, y=0.0, s=0.4, a=1), k(f0 + 5, x=1.0, s=1.0, a=0.8), k(f0 + 7, a=0)], size=0.8, space="foot",
             tint=JADE, z="back")
    geyser(c, 14, 20, size=1.2, tint=JADE)
    impact(c, 20, size=0.75, tint=JADE, ring=False)
    a.add("1_4", c, hit=20)
    c = Clip(r, 48)
    # xoay hai vòng tại chỗ quanh tâm thân (lật ngang qua 0 mỗi nửa vòng tối thiểu 3 khung)
    c.root(k(0, sx=1, sy=1, y=0), k(5, sx=1.06, sy=0.92), k(8, sx=1, sy=1, y=-0.05), k(11, sx=-1), k(14, sx=1), k(17, sx=-1), k(20, sx=1),
           k(22, y=0, sx=1.06, sy=0.94), k(25, sx=1, sy=1), k(47, sx=1, y=0))
    c.piece(head, k(0, r=0), k(8, r=-10), k(22, r=-10), k(25, r=10, e="out"), k(32, r=0))
    c.piece([f1, f2], k(0, r=0), k(8, r=-20), k(22, r=-20), k(25, r=15), k(32, r=0))
    c.fx("xoay", [k(4, y=-0.45, s=0.4, a=0), k(8, s=1.15, a=1), k(22, s=1.2, r=-900, a=1), k(26, s=1.45, a=0)], size=1.0, space="root", tint=JADE, z="back")
    c.fx("xoay", [k(6, y=-0.45, s=0.4, a=0), k(9, s=0.9, a=1), k(22, s=1.0, r=800, a=1), k(25, s=1.2, a=0)], size=0.75, space="root", tint=None, z="front")
    mouth = r.part_pt(head, 0.9, 0.6)
    shot(c, "tia_xoay", mouth, 25, 29, 0.9, s0=0.5, s1=1.0)
    c.fx("xoay_dat", [k(16, x=0.02, y=0.45, s=0.3, a=0), k(20, s=1.1, a=1), k(34, s=1.25, a=1), k(38, s=1.35, a=0)], size=1.15, space="far",
         z="back", tint=JADE)
    tsunami(c, 21, 30, size=1.2, tint=JADE)
    impact(c, 29, size=0.95, tint=JADE)
    a.add("1_6", c, hit=29)


def huyen_vu_3(a):
    """dạng 3 (thần rùa cầm mái chèo): đánh thường vung mái chèo quét sóng lưỡi liềm lớn; chiêu cuối Huyền Vũ Thần Xà: cắm mái
    chèo dậm hai nhịp, xoáy nước dưới chân đối thủ, rắn thần bằng nước trồi lên sau lưng đối thủ, ngóc đầu rồi mổ xuống"""
    r = a.rig
    arm, oar, head, beard = 8, 14, 12, 36
    c = Clip(r, 32)
    c.root(k(0, r=0, x=0), k(8, r=-7, x=-0.05), k(13, r=-8), k(17, r=7, x=0.06, e="out"), k(24, r=2), k(31, r=0, x=0))
    c.piece(arm, k(0, r=0), k(8, r=-45), k(13, r=-55), k(17, r=40, e="out"), k(24, r=12), k(31, r=0))
    c.piece(head, k(0, r=0), k(8, r=-6), k(17, r=6), k(31, r=0))
    c.piece(beard, k(0, r=0), k(9, r=8), k(18, r=-10), k(25, r=4), k(31, r=0))
    c.top(arm, 13, 26)
    c.fx("song", [k(15, x=0.5, y=-0.15, s=0.4, a=0), k(16, a=1), k(19, x=1.1, y=-0.2, s=1.0), k(21, a=0)], size=0.85, space="foot", tint=JADE,
         vis=(15, 20))
    shot(c, "song", r.pt(1.0, -0.25), 18, 22, 0.8, tint=JADE, s0=0.9, s1=1.0)
    c.fx("giot", [k(17, x=0.7, y=-0.3, s=0.5, r=-60, a=1), k(22, x=1.1, y=-0.7, s=1.0, a=0, e="out")], size=0.4, space="foot", tint=JADE)
    impact(c, 22, size=0.9, tint=JADE)
    a.add("1_4", c, hit=22)
    c = Clip(r, 52)
    c.root(k(0, y=0, r=0, sx=1, sy=1), k(6, y=-0.08, r=-5, e="out"), k(9, y=0, sy=0.9, sx=1.08, r=2, e="in"), k(12, sy=1, sx=1),
           k(17, y=-0.1, r=-6, e="out"), k(20, y=0, sy=0.88, sx=1.1, r=3, e="in"), k(24, sy=1, sx=1, r=0), k(28, r=-8), k(32, r=8, sy=0.92, sx=1.06, e="out"),
           k(38, r=0, sy=1, sx=1), k(51, r=0, y=0))
    c.piece(arm, k(0, r=0), k(6, r=-40), k(9, r=25, e="in"), k(13, r=0), k(17, r=-45), k(20, r=25, e="in"), k(24, r=-10), k(28, r=-60),
            k(32, r=45, e="out"), k(40, r=10), k(51, r=0))
    c.top(arm, 4, 40)
    c.piece(head, k(0, r=0), k(26, r=-12), k(32, r=10), k(40, r=0))
    c.piece(beard, k(0, r=0), k(9, r=-10), k(20, r=-10), k(28, r=10), k(33, r=-12), k(42, r=0))
    for f in (9, 20):
        c.fx("vong", [k(f, x=0.35, y=0.0, s=0.4, a=1), k(f + 6, s=1.2, a=0)], size=0.9, space="foot", tint=JADE, z="back")
        c.fx("no", [k(f, x=0.45, y=-0.05, s=0.3, a=1), k(f + 4, s=0.7, a=0)], size=0.5, space="foot", tint=JADE)
    c.fx("xoay_dat", [k(10, x=0.1, y=0.45, s=0.3, a=0), k(15, s=1.0, a=1), k(36, s=1.12, a=1), k(40, s=1.2, a=0)], size=1.1, space="far",
         z="back", tint=JADE)
    # rắn thần: gốc sau lưng đối thủ, lật ngang cho đầu quay về phía đối thủ; trồi lên, ngóc, mổ xuống ở khung 32
    c.fx("ran", [k(16, x=0.42, y=0.47, sx=0.7, sy=0.15, r=0, a=0), k(18, a=1), k(24, sx=1.0, sy=1.0, r=4, e="out"), k(27, r=8, sy=1.05),
                 k(29, r=10, sy=1.08), k(32, r=-30, sx=1.05, sy=0.95, e="in"), k(36, r=-32, a=1), k(41, r=-34, sy=0.7, a=0)],
         size=1.2, space="far", pivot=(0.22, 0.95), flip=True, tint=None)
    impact(c, 32, size=1.0, tint=JADE, shards=False, sparkle="gold")
    c.fx("cot", [k(31, x=-0.2, y=0.5, sx=0.1, sy=0.6, r=-90, a=1), k(34, sx=0.9, e="out"), k(40, sx=0.7, sy=0.3, a=0)], size=1.0, space="far",
         pivot=(0.03, 0.5), tint=JADE)
    c.fx("cot", [k(33, x=0.25, y=0.5, sx=0.1, sy=0.6, r=-90, a=1), k(36, sx=0.8, e="out"), k(42, sx=0.6, sy=0.3, a=0)], size=1.0, space="far",
         pivot=(0.03, 0.5), tint=JADE)
    c.fx("vong", [k(33, x=0.02, y=0.44, s=0.6, a=1), k(42, s=1.8, a=0)], size=1.3, space="far", tint=JADE, z="back")
    a.add("1_6", c, hit=32)


# ================================================================ Vây Lam (cá mập rẽ sóng)

def vay_lam_1(a):
    """dạng 1 (cá mập con trong trứng bong bóng): đánh thường lao húc trứng bong bóng; chiêu cuối gọi bong bóng nước trên đầu
    đối thủ rồi xả nước xuống"""
    r = a.rig
    c = Clip(r, 32)
    lunge_body(c, 8, 18, 32, dist=0.9, back=-10, fwd=12, hop=0.08)
    c.piece([13, 14], k(0, sx=1, sy=1), k(8, sx=0.92, sy=1.08), k(18, sx=1.12, sy=0.9), k(24, sx=1, sy=1))
    c.fx("no", [k(18, x=1.25, y=-0.45, s=0.3, a=1), k(22, s=0.8, a=0)], size=0.5, space="root")
    c.fx("cau", [k(18, x=1.2, y=-0.6, s=0.3, a=1), k(24, x=1.4, y=-1.0, s=0.6, a=0, e="out")], size=0.25, space="root")
    a.add("1_4", c, lunge=True)
    c = Clip(r, 44)
    c.root(k(0, r=0, y=0), k(8, r=-10, y=-0.08), k(14, r=-14, y=-0.12), k(24, r=6, y=0, e="out"), k(32, r=0), k(43, r=0))
    c.piece([13, 14], k(0, sx=1, sy=1), k(8, sx=1.1, sy=1.1), k(14, sx=1.15, sy=1.15), k(24, sx=0.95, sy=0.95), k(30, sx=1, sy=1))
    charge(c, "root", 4, 14, size=0.45)
    orb_drop(c, 10, 26, size=0.55, h=0.82)
    impact(c, 26, size=0.85)
    a.add("1_6", c, hit=26)


def vay_lam_2(a):
    """dạng 2 (Cá Song Tiễn): đánh thường phóng hai mũi tên nước của mình; chiêu cuối mưa tên nước từ trên trời rồi sóng thần"""
    r = a.rig
    arrows = [12, 10]
    c = Clip(r, 32)
    c.root(k(0, r=0, x=0), k(8, r=-7, x=-0.05), k(14, r=6, x=0.05, e="out"), k(20, r=0, x=0), k(31, r=0))
    c.piece(12, k(0, a=1, sx=1, sy=1), k(11, a=1), k(12, a=0), k(25, a=0, sx=0.5, sy=0.5), k(29, a=1, sx=1, sy=1, e="back"))
    c.piece(10, k(0, a=1, sx=1, sy=1), k(13, a=1), k(14, a=0), k(25, a=0, sx=0.5, sy=0.5), k(29, a=1, sx=1, sy=1, e="back"))
    shot(c, ("copy", [12]), r.center(12), 12, 18, 1.0, end=(0.02, -0.1), s0=1.0, s1=1.0)
    shot(c, ("copy", [10]), r.center(10), 14, 19, 1.0, end=(0.02, 0.08), s0=1.0, s1=1.0)
    impact(c, 19, size=0.8)
    a.add("1_4", c, hit=19)
    c = Clip(r, 46)
    c.root(k(0, r=0, y=0), k(8, r=-10, y=-0.1, e="out"), k(20, r=-12, y=-0.12), k(26, r=6, y=0, e="out"), k(34, r=0), k(45, r=0))
    c.piece(arrows, k(0, a=1, sx=1, sy=1), k(8, a=1), k(10, a=0), k(38, a=0, sx=0.5, sy=0.5), k(42, a=1, sx=1, sy=1, e="back"))
    for i, (p, x0, f0) in enumerate(((12, 0.3, 12), (10, -0.0, 15), (12, 0.6, 18), (10, 0.15, 21), (12, 0.45, 24))):
        fe = f0 + 5
        c.fx(("copy", [p]), [k(f0, x=x0 + 0.3, y=-1.8, r=70, s=1.35, a=0), k(f0 + 1, a=1), k(fe, x=x0 * 0.4, y=-0.1, e="in"), k(fe + 1, a=0)],
             space="far")
        c.fx("no", [k(fe, x=x0 * 0.4 + 0.02, y=0.0, s=0.3, a=1), k(fe + 4, s=0.7, a=0)], size=0.4, space="far")
    tsunami(c, 22, 30, size=1.2)
    impact(c, 30, size=0.9)
    a.add("1_6", c, hit=30)


def vay_lam_3(a):
    """dạng 3 (Cá Mập Vây Lam, nhiều vây lưỡi sóng): đánh thường quẫy mình tung hai sóng lưỡi liềm; chiêu cuối cưỡi sóng thần
    lao tới cắn (cận chiến)"""
    r = a.rig
    c = Clip(r, 32)
    c.root(k(0, r=0, x=0), k(8, r=-9, x=-0.04), k(14, r=8, x=0.05, e="out"), k(18, r=-4), k(22, r=2), k(31, r=0, x=0))
    shot(c, "song", r.pt(0.4, -0.6), 12, 18, 0.55, end=(0.03, -0.15))
    shot(c, "song", r.pt(0.4, -0.35), 15, 20, 0.5, end=(0.02, 0.1))
    impact(c, 20, size=0.85)
    a.add("1_4", c, hit=20)
    c = Clip(r, 44)
    lunge_body(c, 10, 24, 44, dist=0.95, back=-10, fwd=10, hop=0.12)
    c.fx("than", [k(4, x=-0.45, y=0.05, s=0.3, sy=0.3, a=0), k(9, s=0.9, sy=0.9, a=1), k(20, x=0.35, s=1.0, sy=1.05), k(24, x=0.7, sy=1.1),
                  k(30, x=0.75, sy=0.6, a=0)], size=1.2, space="root", pivot=(0.5, 1.0), z="back")
    c.fx("no", [k(23, x=1.2, y=-0.5, s=0.3, a=1), k(28, s=0.85, a=0)], size=0.6, space="root")
    c.fx("giot", [k(24, x=1.1, y=-0.7, s=0.5, a=1), k(31, x=1.4, y=-1.0, s=0.9, a=0, e="out")], size=0.4, space="root")
    a.add("1_6", c, lunge=True)


# ================================================================ Kuba (ốc mượn hồn)

def kuba_1(a):
    """dạng 1: đánh thường lao kẹp càng; chiêu cuối vỏ ốc bắn liên ba quả cầu nước"""
    r = a.rig
    claws, shell, head = [16, 9], 19, 18
    c = Clip(r, 32)
    lunge_body(c, 8, 18, 32, dist=0.9, back=-8, fwd=8)
    c.piece(claws, k(0, r=0), k(8, r=-30), k(15, r=-35), k(18, r=15, e="out"), k(26, r=0))
    c.fx("no", [k(18, x=1.2, y=-0.45, s=0.3, a=1), k(22, s=0.75, a=0)], size=0.5, space="root")
    a.add("1_4", c, lunge=True)
    c = Clip(r, 46)
    c.root(k(0, r=0, sx=1, sy=1), k(6, r=-6, sy=1.06, sx=0.95), k(12, r=4, sy=0.94, sx=1.06), k(15, r=-3), k(19, r=4, sy=0.94), k(22, r=-3),
           k(26, r=5, sy=0.94), k(32, r=0, sx=1, sy=1), k(45, r=0))
    c.piece(shell, k(0, sx=1, sy=1), k(8, sx=1.12, sy=1.12), k(12, sx=0.95, sy=0.95), k(16, sx=1.08, sy=1.08), k(19, sx=0.95, sy=0.95),
            k(23, sx=1.08, sy=1.08), k(26, sx=0.95, sy=0.95), k(32, sx=1, sy=1))
    src = r.part_pt(shell, 0.7, 0.3)
    charge(c, ("piece", shell, src), 3, 12, size=0.4)
    for f0 in (12, 19, 26):
        shot(c, "cau", src, f0, f0 + 5, 0.45, spin=-300, arc=0.3)
        c.fx("no", [k(f0 + 5, x=0.02, s=0.3, a=1), k(f0 + 9, s=0.7, a=0)], size=0.45, space="far")
    impact(c, 31, size=0.85, sparkle=True)
    a.add("1_6", c, hit=31)


def kuba_2(a):
    """dạng 2 (càng cam đỏ to): đánh thường đập càng xuống đất, sóng đất lan tới, mạch nước phun; chiêu cuối chui vỏ xoay lốc
    nước lao tới húc (cận chiến)"""
    r = a.rig
    claw, shell = 3, 13
    c = Clip(r, 32)
    c.root(k(0, r=0, y=0), k(8, r=-8, y=-0.04), k(14, r=6, y=0, sy=0.92, sx=1.06, e="in"), k(18, r=0, sy=1, sx=1), k(31, r=0))
    c.piece(claw, k(0, r=0), k(8, r=-45), k(14, r=30, e="in"), k(20, r=10), k(31, r=0))
    c.fx("no", [k(14, x=0.55, y=-0.05, s=0.3, a=1), k(18, s=0.7, a=0)], size=0.45, space="foot")
    for f0 in (14, 16):
        c.fx("vong", [k(f0, x=0.55, y=0.0, s=0.4, a=1), k(f0 + 5, x=1.05, s=1.0, a=0)], size=0.75, space="foot", z="back")
    geyser(c, 13, 19, size=1.2)
    impact(c, 19, size=0.75, ring=False)
    a.add("1_4", c, hit=19)
    c = Clip(r, 44)
    lunge_body(c, 12, 24, 44, dist=1.0, back=-6, fwd=6, hop=0.0)
    c.piece(shell, k(0, sx=1, sy=1), k(10, sx=1.15, sy=1.15), k(24, sx=1.12, sy=1.12), k(32, sx=1, sy=1))
    c.fx("xoay", [k(3, y=-0.45, s=0.4, a=0), k(8, s=1.05, a=1), k(24, s=1.15, r=-900, a=1), k(28, s=1.35, a=0)], size=0.85, space="root", z="back")
    c.fx("xoay", [k(5, y=-0.45, s=0.4, a=0), k(10, s=0.8, a=1), k(24, s=0.9, r=800, a=1), k(27, s=1.1, a=0)], size=0.7, space="root")
    c.fx("no", [k(23, x=1.1, y=-0.4, s=0.3, a=1), k(28, s=0.85, a=0)], size=0.6, space="root")
    c.fx("vong", [k(24, x=1.0, y=0.0, s=0.4, a=1), k(32, s=1.3, a=0)], size=0.9, space="root", z="back")
    a.add("1_6", c, lunge=True)


def kuba_3(a):
    """dạng 3 (vỏ kim cương): đánh thường vồ đập (cận chiến) bung mảnh kim cương; chiêu cuối cầu kim cương trên đầu đối thủ
    xả nước, kim cương vỡ tung"""
    r = a.rig
    c = Clip(r, 32)
    lunge_body(c, 9, 18, 32, dist=0.85, back=-9, fwd=9, hop=0.1)
    c.fx("no", [k(18, x=1.1, y=-0.45, s=0.3, a=1), k(22, s=0.8, a=0)], size=0.5, space="root")
    c.fx("bang", [k(18, x=1.1, y=-0.5, s=0.4, a=1), k(24, x=1.35, y=-0.85, s=1.0, r=40, a=0, e="out")], size=0.45, space="root")
    c.fx("lap", [k(17, x=1.0, y=-0.8, s=0.3, a=0), k(20, s=1.0, r=30, a=1), k(24, s=0.4, a=0)], size=0.3, space="root", tint=GOLD)
    a.add("1_4", c, lunge=True)
    c = Clip(r, 46)
    c.root(k(0, r=0, y=0, sx=1, sy=1), k(6, sy=0.92, sx=1.06), k(12, r=-8, y=-0.08, sy=1.05, sx=0.97, e="out"), k(24, r=-10),
           k(28, r=6, y=0, sy=0.95, sx=1.04, e="out"), k(36, r=0, sy=1, sx=1), k(45, r=0))
    c.fx("lap", [k(6, x=0.0, y=-1.0, s=0.3, a=0), k(10, s=1.0, r=40, a=1), k(14, s=0.4, a=0)], size=0.35, space="root", tint=GOLD)
    orb_drop(c, 10, 28, size=0.55, h=0.85, thick=0.8)
    for i in range(3):
        c.fx("bang", [k(13 + i * 3, x=-0.25 + 0.25 * i, y=-0.95 + 0.08 * i, s=0.4, r=i * 60, a=0), k(16 + i * 3, s=0.8, a=1),
                      k(27, x=0.02, y=-0.85, s=0.6, r=i * 60 + 200, a=0)], size=0.3, space="far")
    impact(c, 28, size=0.95, shards=True, sparkle="gold")
    a.add("1_6", c, hit=28)


# ================================================================ Tám Tay (bạch tuộc)

def tam_tay_1(a):
    """dạng 1 (bong bóng): đánh thường phun bong bóng nước bay vòng cung; chiêu cuối bong bóng lớn trên đầu đối thủ xả nước"""
    r = a.rig
    body = 11
    mouth = r.part_pt(body, 0.6, 0.75)
    c = Clip(r, 32)
    c.root(k(0, r=0, sx=1, sy=1), k(8, r=-6, sx=1.06, sy=0.94), k(14, r=5, sx=0.94, sy=1.06, e="out"), k(20, r=0, sx=1, sy=1), k(31, r=0))
    shot(c, "cau", mouth, 13, 19, 0.38, spin=-200, arc=0.35)
    shot(c, "cau", mouth, 15, 20, 0.25, spin=-260, arc=0.5, end=(0.15, -0.2))
    impact(c, 19, size=0.75)
    a.add("1_4", c, hit=19)
    c = Clip(r, 44)
    c.root(k(0, r=0, y=0, sx=1, sy=1), k(6, sy=0.9, sx=1.08), k(12, y=-0.1, sy=1.08, sx=0.94, e="out"), k(24, y=-0.12), k(28, y=0, sy=0.92, sx=1.06),
           k(34, sy=1, sx=1), k(43, y=0))
    charge(c, "root", 3, 12, size=0.45)
    orb_drop(c, 9, 26, size=0.6, h=0.82)
    impact(c, 26, size=0.85)
    a.add("1_6", c, hit=26)


def tam_tay_2(a):
    """dạng 2 (pháo thủ): đánh thường bắn pháo nước giật lùi; chiêu cuối hai pháo bắn liên hoàn ba quả vòng cung rồi sóng thần"""
    r = a.rig
    can1, can2 = 6, 12
    m1, m2 = r.part_pt(can1, 0.95, 0.45), r.part_pt(can2, 0.95, 0.45)
    c = Clip(r, 32)
    c.root(k(0, r=0, x=0), k(9, r=-4, x=0.0), k(13, r=-8, x=-0.07, e="out"), k(20, r=0, x=0), k(31, r=0))
    c.piece(can1, k(0, r=0, x=0), k(9, r=-6), k(13, r=-14, x=-0.06, e="out"), k(20, r=0, x=0))
    c.fx("no", [k(12, s=0.3, a=1), k(16, s=0.8, a=0)], size=0.4, space=("piece", can1, m1))
    shot(c, "cau", m1, 12, 18, 0.35, spin=-400, arc=0.25)
    impact(c, 18, size=0.8)
    a.add("1_4", c, hit=18)
    c = Clip(r, 46)
    c.root(k(0, r=0, x=0), k(8, r=-5), k(10, r=-9, x=-0.06, e="out"), k(13, r=-2, x=0), k(15, r=-9, x=-0.06, e="out"), k(18, r=-2, x=0),
           k(20, r=-9, x=-0.06, e="out"), k(24, r=0, x=0), k(45, r=0))
    for f0, cn, m in ((10, can1, m1), (15, can2, m2), (20, can1, m1)):
        c.piece(cn, k(f0 - 2, r=0), k(f0, r=-14, e="out"), k(f0 + 3, r=0))
        c.fx("no", [k(f0, s=0.3, a=1), k(f0 + 4, s=0.8, a=0)], size=0.4, space=("piece", cn, m))
        shot(c, "cau", m, f0, f0 + 7, 0.38, spin=-400, arc=0.55, end=(0.05 * (f0 % 3), -0.05))
        c.fx("no", [k(f0 + 7, x=0.05 * (f0 % 3), s=0.3, a=1), k(f0 + 11, s=0.75, a=0)], size=0.45, space="far")
    tsunami(c, 22, 30, size=1.15)
    impact(c, 30, size=0.9)
    a.add("1_6", c, hit=30)


# ================================================================ Cá Ngựa

def ca_ngua_1(a):
    """dạng 1 (tân binh): đánh thường phun tia nước từ mõm; chiêu cuối chọc giáo cờ xuống, mạch nước phun dưới đối thủ"""
    r = a.rig
    head, spear = 9, 16
    snout = r.part_pt(head, 0.98, 0.55)
    c = Clip(r, 32)
    c.root(k(0, r=0, x=0), k(8, r=-8, x=-0.05), k(13, r=-9), k(16, r=6, x=0.05, e="out"), k(22, r=1), k(31, r=0, x=0))
    c.piece(head, k(0, r=0), k(8, r=-12), k(16, r=8), k(31, r=0))
    charge(c, ("piece", head, snout), 5, 14, size=0.28)
    shot(c, "tia", snout, 14, 18, 0.6, s0=0.5, s1=1.0)
    shot(c, "giot", snout, 15, 18, 0.3, s0=0.5, s1=0.9, end=(0.05, -0.1))
    impact(c, 18, size=0.75)
    a.add("1_4", c, hit=18)
    c = Clip(r, 44)
    c.root(k(0, r=0, y=0), k(8, r=-8, y=-0.08), k(14, r=-10, y=-0.1), k(20, r=6, y=0, sy=0.92, sx=1.06, e="in"), k(26, r=0, sy=1, sx=1), k(43, r=0))
    c.piece(spear, k(0, r=0), k(8, r=-35), k(14, r=-40), k(20, r=35, e="in"), k(28, r=10), k(43, r=0))
    c.fx("no", [k(20, x=0.5, y=-0.05, s=0.3, a=1), k(24, s=0.7, a=0)], size=0.45, space="foot")
    geyser(c, 12, 25, size=1.45)
    impact(c, 25, size=0.85, ring=False)
    a.add("1_6", c, hit=25)


def ca_ngua_2(a):
    """dạng 2 (song đao): đánh thường lao tới chém chéo hai đao; chiêu cuối chém chữ thập tung hai sóng lưỡi liềm bắt chéo"""
    r = a.rig
    b1, b2 = 13, 4
    c = Clip(r, 32)
    lunge_body(c, 8, 18, 32, dist=0.95, back=-8, fwd=9)
    c.piece(b1, k(0, r=0), k(8, r=-40), k(16, r=-45), k(18, r=35, e="out"), k(25, r=5), k(31, r=0))
    c.piece(b2, k(0, r=0), k(8, r=30), k(16, r=35), k(18, r=-35, e="out"), k(25, r=-5), k(31, r=0))
    c.top([b1, b2], 12, 24)
    c.fx("song", [k(17, x=1.05, y=-0.5, s=0.4, r=-35, a=1), k(21, s=1.0, r=-30, a=0)], size=0.6, space="root")
    c.fx("song", [k(18, x=1.05, y=-0.45, s=0.4, r=35, a=1), k(22, s=1.0, r=30, a=0)], size=0.6, space="root")
    a.add("1_4", c, lunge=True)
    c = Clip(r, 44)
    c.root(k(0, r=0, x=0), k(8, r=-8, x=-0.05), k(15, r=-10), k(18, r=7, x=0.06, e="out"), k(21, r=-6), k(24, r=7, e="out"), k(30, r=0, x=0),
           k(43, r=0))
    c.piece(b1, k(0, r=0), k(8, r=-50), k(15, r=-55), k(18, r=40, e="out"), k(24, r=30), k(32, r=0))
    c.piece(b2, k(0, r=0), k(8, r=40), k(18, r=35), k(21, r=45), k(24, r=-40, e="out"), k(32, r=0))
    c.top([b1, b2], 6, 32)
    charge(c, "root", 4, 15, size=0.5)
    shot(c, "song", r.pt(0.4, -0.65), 18, 24, 0.7, r0=-30, end=(0.03, -0.05))
    shot(c, "song", r.pt(0.4, -0.3), 21, 26, 0.7, r0=30, end=(0.03, -0.05))
    impact(c, 26, size=0.9)
    a.add("1_6", c, hit=26)


def ca_ngua_3(a):
    """dạng 3 (tướng quân): đánh thường lao tới đâm cán cờ; chiêu cuối giương cờ hiệu triệu sóng thần và mưa giáo nước"""
    r = a.rig
    flag, head, shield = 24, 25, 16
    c = Clip(r, 32)
    lunge_body(c, 8, 18, 32, dist=0.9, back=-7, fwd=8)
    c.piece(flag, k(0, r=0, x=0), k(8, r=-20, x=-0.05), k(18, r=25, x=0.12, e="out"), k(26, r=0, x=0))
    c.fx("no", [k(18, x=1.2, y=-0.6, s=0.3, a=1), k(22, s=0.8, a=0)], size=0.5, space="root")
    a.add("1_4", c, lunge=True)
    c = Clip(r, 46)
    c.root(k(0, r=0, y=0), k(8, r=-6, y=-0.06), k(20, r=-8, y=-0.08), k(26, r=6, y=0, e="out"), k(34, r=0), k(45, r=0))
    c.piece(flag, k(0, r=0), k(8, r=-30), k(12, r=-15), k(16, r=-35), k(20, r=-20), k(26, r=35, e="out"), k(34, r=5), k(45, r=0))
    c.piece(shield, k(0, r=0), k(8, r=10), k(26, r=-8), k(34, r=0))
    c.fx("lap", [k(8, s=0.3, a=0), k(11, s=1.0, r=30, a=1), k(15, s=0.4, a=0)], size=0.35, space=P(r, 23, 0.5, 0.5), tint=GOLD)
    tsunami(c, 16, 28, size=1.2)
    for i, (x0, f0) in enumerate(((0.35, 20), (0.1, 23), (0.55, 25))):
        c.fx("tia", [k(f0, x=x0 + 0.2, y=-1.6, r=80, s=0.8, a=0), k(f0 + 1, a=1), k(f0 + 4, x=x0 * 0.5, y=-0.3, e="in"), k(f0 + 5, a=0)],
             size=0.55, space="far")
    impact(c, 28, size=0.95)
    a.add("1_6", c, hit=28)


# ================================================================ Mập Răng Cưa (cá mập)

def map_rang_1(a):
    """dạng 1 (cá mập con): đánh thường lao cắn; chiêu cuối phun tia nước lớn"""
    r = a.rig
    c = Clip(r, 30)
    lunge_body(c, 8, 17, 30, dist=0.9, back=-10, fwd=12, hop=0.08)
    c.fx("no", [k(17, x=1.2, y=-0.5, s=0.3, a=1), k(21, s=0.75, a=0)], size=0.45, space="root")
    a.add("1_4", c, lunge=True)
    c = Clip(r, 42)
    mouth = r.pt(0.55, -0.4)
    c.root(k(0, r=0, x=0), k(8, r=-10, x=-0.06), k(16, r=-12, x=-0.07), k(20, r=6, x=0.05, e="out"), k(28, r=0, x=0), k(41, r=0))
    charge(c, "root", 6, 18, size=0.4, at=(0.55, -0.4))
    shot(c, "cau", mouth, 18, 23, 0.5, spin=-300, s0=0.4, s1=1.0)
    shot(c, "tia", mouth, 18, 23, 0.65, s0=0.4, s1=0.9)
    impact(c, 23, size=0.85)
    a.add("1_6", c, hit=23)


def map_rang_2(a):
    """dạng 2: đánh thường lao cắn quẫy đuôi; chiêu cuối quẫy đuôi gọi xoáy nước, mạch nước phun dưới đối thủ"""
    r = a.rig
    tail = 4
    c = Clip(r, 30)
    lunge_body(c, 8, 17, 30, dist=0.9, back=-9, fwd=10, hop=0.06)
    c.piece(tail, k(0, r=0), k(8, r=20), k(17, r=-25), k(24, r=5), k(29, r=0))
    c.fx("no", [k(17, x=1.2, y=-0.5, s=0.3, a=1), k(21, s=0.8, a=0)], size=0.5, space="root")
    a.add("1_4", c, lunge=True)
    c = Clip(r, 44)
    c.root(k(0, r=0), k(6, r=-6), k(10, r=6), k(14, r=-6), k(18, r=6), k(22, r=-4), k(26, r=4), k(30, r=0), k(43, r=0))
    c.piece(tail, k(0, r=0), k(6, r=25), k(10, r=-25), k(14, r=25), k(18, r=-25), k(22, r=20), k(26, r=-15), k(32, r=0))
    c.fx("xoay", [k(4, y=-0.45, s=0.4, a=0), k(8, s=1.0, a=1), k(24, s=1.1, r=-700, a=1), k(28, s=1.3, a=0)], size=0.8, space="root", z="back")
    geyser(c, 10, 26, size=1.5)
    impact(c, 26, size=0.9, ring=False)
    a.add("1_6", c, hit=26)


def map_rang_3(a):
    """dạng 3 (vua cá mập): đánh thường quật đuôi tung sóng lưỡi liềm; chiêu cuối cưỡi sóng thần lao tới cắn (cận chiến)"""
    r = a.rig
    c = Clip(r, 30)
    c.root(k(0, r=0, x=0), k(8, r=-10, x=-0.05), k(13, r=9, x=0.05, e="out"), k(17, r=-4), k(22, r=0, x=0), k(29, r=0))
    shot(c, "song", r.pt(0.5, -0.5), 12, 18, 0.6, end=(0.02, -0.05))
    impact(c, 18, size=0.8)
    a.add("1_4", c, hit=18)
    c = Clip(r, 44)
    lunge_body(c, 10, 24, 44, dist=1.0, back=-10, fwd=10, hop=0.15)
    c.fx("than", [k(4, x=-0.5, y=0.05, s=0.3, sy=0.3, a=0), k(9, s=0.9, sy=0.9, a=1), k(20, x=0.3, s=1.0, sy=1.05), k(24, x=0.7, sy=1.1),
                  k(30, x=0.75, sy=0.6, a=0)], size=1.4, space="root", pivot=(0.5, 1.0), z="back")
    c.fx("no", [k(23, x=1.25, y=-0.5, s=0.3, a=1), k(28, s=0.85, a=0)], size=0.6, space="root")
    c.fx("giot", [k(24, x=1.1, y=-0.7, s=0.5, a=1), k(31, x=1.4, y=-1.0, s=0.9, a=0, e="out")], size=0.45, space="root")
    a.add("1_6", c, lunge=True)


CHOREO = {
    "thuy_1831": lam_quan_1, "thuy_1832": lam_quan_2, "thuy_2955": lam_quan_3,
    "thuy_805": thuong_lam_1, "thuy_806": thuong_lam_2, "thuy_807": thuong_lam_3,
    "thuy_713": huyen_vu_1, "thuy_714": huyen_vu_2, "thuy_715": huyen_vu_3,
    "thuy_546": vay_lam_1, "thuy_547": vay_lam_2, "thuy_548": vay_lam_3,
    "thuy_94": kuba_1, "thuy_95": kuba_2, "thuy_96": kuba_3,
    "thuy_1053": tam_tay_1, "thuy_1054": tam_tay_2,
    "thuy_181": ca_ngua_1, "thuy_182": ca_ngua_2, "thuy_183": ca_ngua_3,
    "thuy_31": map_rang_1, "thuy_32": map_rang_2, "thuy_33": map_rang_3,
}


# ================================================================ animation phụ như bản gốc aola (người dùng dặn 2026-11-07:
# "các con hôm qua làm chưa có đầy đủ animation như con gốc, đặc biệt là phần nước bao quanh/các animation phụ")
# Kiểm kê bằng tools/kiem_anim_phu.py (mảnh có khung con chạy ở clip đứng gốc). Nước, bọt, giọt: SUB (khung con gốc tô lại bằng
# to_nuoc, đi theo mảnh ở mọi clip). Thân (cánh, đuôi, xúc tu, râu, chuông, áo choàng): PHU (xoay thêm quanh khớp, lệch nhịp).

TIM = [[110, 70, 200], [168, 132, 236], [242, 234, 255]]  # nước tím than của Lam Quân 3: xanh đậm, xanh nhạt, bọt

SUB = {
    "thuy_1053": [(2, None), (3, None), (9, None)],          # bọt sủi quanh chân (30 khung)
    "thuy_1054": [(2, None), (3, None), (4, None)],          # chuỗi bọt bay lên (8-10 khung)
    # thuy_548 mảnh 1 (vòng sóng trắng mảnh dưới thân): to_nuoc tô thành vòng mực sẫm như bóng, nên không dùng
    "thuy_95": [(37, None)],                                 # giọt nước bay quanh (4 khung)
    "thuy_96": [(28, None), (29, None)],                     # giọt nước bay quanh (14 khung)
    "thuy_1832": [(2, None), (37, None)],                    # sóng cuộn bên trái, xoáy nước tan thành bụi bên phải (8-9 khung)
    "thuy_2955": [(1, TIM), (2, TIM)],                       # nước tím dưới chân, lửa nước tím bốc lên (4, 8 khung)
}

# (mảnh hoặc [mảnh], biên độ độ, số vòng mỗi clip, kiểu): sway đung đưa, wave lệch pha theo thứ tự (xúc tu), spin quay tròn
PHU = {
    "thuy_548": [([9, 24, 28, 31, 2, 6, 23, 26, 27, 11, 12], 9, 1, "wave")],                # các lưỡi sóng bay quanh uốn lượn
    "thuy_547": [([12, 2], 9, 1, "wave")],                                              # mũi tên nước, sóng bọt hai bên
    "thuy_1053": [([16], 5, 1)],                                                         # mũ phập phồng
    "thuy_1054": [([8, 10, 14, 15, 16], 10, 2, "wave"), ([20, 22], 12, 1, "wave"), ([5, 6], 6, 1, "wave")],  # xúc tu, râu, pháo
    "thuy_95": [([8], 12, 1), ([16, 24, 25, 27, 29, 30], 8, 2, "wave")],                 # đuôi, vây và tóc
    "thuy_96": [([7], 10, 1)],                                                           # đuôi
    "thuy_806": [([5], 14, 1), ([10], 8, 1)],                                            # vây đuôi, cánh
    "thuy_807": [([15, 20], 10, 1, "wave"), ([21], 8, 1), ([27], 12, 2)],                 # hai cánh, vây dưới, râu
    "thuy_713": [([22], 0, 1, "spin")],                                                  # ngọc trai đen xoay
    "thuy_1831": [([7], 10, 1)],                                                         # chuông lắc
    "thuy_1832": [([28], 5, 1)],                                                         # chuông khổng lồ lắc
    "thuy_2955": [([4], 9, 2), ([28], 4, 1)],                                            # áo choàng phất, chuông đen lắc
}
