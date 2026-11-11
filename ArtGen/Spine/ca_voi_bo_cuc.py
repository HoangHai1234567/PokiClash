# -*- coding: utf-8 -*-
"""Sơ đồ bố cục dòng cá voi biến dị (mã làm việc ca_voi, tướng thứ 7 đảo Thủy) để đính vào prompt concept. Bản 2 (2026-11-11, sau
khi người dùng chê bản đầu "sơ sài, nhìn lại con gốc"): dựng theo đúng cách dựng hình của con gốc đọc trên ảnh cận đầu / đuôi:
vòm hàm trên như cái mũ sọ ôm quanh miệng, miệng hình quả trứng nghiêng có KHOÉ NHỌN kéo dài vào thân, nanh RẤT TO cong không đều
đan cài như khoá kéo, lòng miệng hai tông (vòm họng sẫm ở trên, sàn miệng nhạt ở dưới), dải hoa văn dưới bụng, đùi góc cạnh có
mỏm gối nhọn, đuôi có khoanh và ba mảnh đá nhiều mặt cắt. Hình phẳng tự vẽ bằng mã (không phải ảnh của game nào); GPT chỉ lấy bố
cục và tỉ lệ, không lấy nét.

    py -3 -I ArtGen/Spine/ca_voi_bo_cuc.py [1|2]   →  inbox/ca_voi_<k>/mau/bo_cuc.png (1536 × 1024, nền trắng)
"""
import os
import sys

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
S = 2
W, H = 1536, 1024
INK = (43, 33, 24)
PAL = {
    2: dict(back=(47, 74, 110), lip=(79, 134, 176), belly=(230, 241, 244), wave=(79, 134, 176), groove=(143, 184, 204),
            floor=(226, 96, 122), palate=(142, 42, 85), fang=(251, 241, 210), rock=(38, 37, 44), facet=(90, 88, 102),
            vein=(143, 184, 204), barn=(251, 241, 210)),
    1: dict(back=(79, 134, 176), lip=(126, 176, 210), belly=(230, 241, 244), wave=(126, 176, 210), groove=(143, 184, 204),
            floor=(240, 138, 150), palate=(196, 84, 120), fang=(251, 241, 210), rock=(38, 37, 44), facet=(90, 88, 102),
            vein=(143, 184, 204), barn=(251, 241, 210)),
}


def C(x, y):
    """Toạ độ đọc trên ảnh cận ĐẦU của con gốc (1500 × 1300) → khung 1536 × 1024."""
    return (1132.1 + 0.5377 * (x - 750), 579.8 + 0.5377 * (y - 650))


def T(x, y):
    """Toạ độ đọc trên ảnh cận ĐUÔI của con gốc (1500 × 1100) → khung 1536 × 1024."""
    return (631.7 + 0.4818 * (x - 750), 704.9 + 0.4818 * (y - 550))


def cr(pts, closed, n=14):
    out = []
    m = len(pts)
    rng = range(m) if closed else range(m - 1)
    for i in rng:
        p0 = pts[(i - 1) % m] if (closed or i > 0) else pts[i]
        p1, p2 = pts[i], pts[(i + 1) % m]
        p3 = pts[(i + 2) % m] if (closed or i + 2 < m) else p2
        for k in range(n):
            t = k / n
            out.append(tuple(0.5 * ((2 * p1[a]) + (-p0[a] + p2[a]) * t + (2 * p0[a] - 5 * p1[a] + 4 * p2[a] - p3[a]) * t * t
                                    + (-p0[a] + 3 * p1[a] - 3 * p2[a] + p3[a]) * t ** 3) for a in (0, 1)))
    if not closed:
        out.append(pts[-1])
    return out


class Ve:
    def __init__(self, tf):
        self.im = Image.new("RGB", (W * S, H * S), (255, 255, 255))
        self.d = ImageDraw.Draw(self.im)
        self.tf = tf

    def sc(self, pts):
        return [(self.tf(p)[0] * S, self.tf(p)[1] * S) for p in pts]

    def fill(self, pts, col, w=7):
        self.d.polygon(self.sc(pts), fill=col)
        if w:
            self.line(pts + pts[:1], w)

    def line(self, pts, w, col=INK):
        p = self.sc(pts)
        self.d.line(p, fill=col, width=w * S, joint="curve")
        r = w * S / 2
        for x, y in (p[0], p[-1]):
            self.d.ellipse([x - r, y - r, x + r, y + r], fill=col)


def ve(k):
    c = PAL[k]
    if k == 2:
        tf = lambda p: (1400 + (p[0] - 1400) * 0.9, 880 + (p[1] - 880) * 0.9)   # thu lại cho đủ chỗ đuôi dài
    else:                                   # dạng 1: cùng bố cục, thân sau và đuôi ngắn lại, cả con nhỏ đi (cá voi con đầu to)
        def tf(p):
            x, y = p
            if x < 880:
                x = 880 - (880 - x) * 0.66
            return (760 + (x - 800) * 0.74, 860 + (y - 880) * 0.74)
    v = Ve(tf)
    cs = lambda pts, closed=True: cr([C(*p) for p in pts], closed)
    ts = lambda pts, closed=True: cr([T(*p) for p in pts], closed)
    pc = lambda pts: [C(*p) for p in pts]
    pt = lambda pts: [T(*p) for p in pts]

    def claw(pts, fac, tr):
        v.fill(tr(pts), c["rock"])
        v.fill(tr(fac), c["facet"], 0)
        v.line(tr(pts) + tr(pts)[:1], 7)

    def rock(pts, fac, vein):
        v.fill(pt(pts), c["rock"])
        v.fill(pt(fac), c["facet"], 0)
        v.line(pt(vein), 4, c["vein"])
        v.line(pt(pts) + pt(pts)[:1], 7)

    # 1. vây ngực bên xa (dùng như chân chống): nấp sau cằm, đầu vây chia ba mấu, mỗi mấu bọc một móng đá mọc liền ra
    for cx in (905, 1035, 1160):
        claw([(cx - 62, 1200), (cx - 30, 1110), (cx + 30, 1110), (cx + 56, 1200)], [(cx - 30, 1110), (cx + 30, 1110), (cx + 40, 1200),
                                                                                 (cx - 5, 1200)], pc)
    v.fill(cs([(930, 720), (1000, 650), (1040, 820), (1080, 1000), (1196, 1090), (1212, 1130), (1150, 1150), (1090, 1118),
               (1030, 1150), (960, 1118), (900, 1146), (872, 1096), (900, 960)]), c["back"])

    # đường lưng: từ chót đuôi chạy chéo thẳng lên đỉnh vòm đầu rồi ôm xuống má phải tới khớp hàm
    BACK = [(218, 668), (300, 688), (400, 676), (490, 640), T(640, 290), C(300, 245), C(520, 160), C(700, 132), C(860, 158), C(962, 232), C(1012, 330),
            C(1028, 440), C(1018, 540), C(985, 620), C(925, 740)]
    MTOP = [(95, 648), (270, 592), (352, 480), (430, 392), (540, 300), (700, 255), (860, 285), (938, 392), (940, 520), (890, 640),
            (925, 740)]                                                         # mép môi trên, từ khoé nhọn bên trái tới khớp hàm
    MBOT = [(925, 740), (935, 840), (905, 925), (830, 975), (700, 985), (560, 960), (430, 880), (300, 770), (95, 648)]

    # 3. vây đuôi cá voi hai thuỳ bằng ĐÁ ĐEN nhiều mặt cắt, khe chữ V ở giữa; vài mẩu đá bám quanh chỗ nối với cuống đuôi
    def da(pts, fac):
        if k == 1:                          # cá voi con: vây đá nhỏ, co 0,62 quanh chỗ nối cuống đuôi
            pts = [(225 + (x - 225) * 0.62, 690 + (y - 690) * 0.62) for x, y in pts]
            fac = [(225 + (x - 225) * 0.62, 690 + (y - 690) * 0.62) for x, y in fac]
        v.fill(pts, c["rock"])
        v.fill(fac, c["facet"], 0)
        v.line([fac[0], fac[-2], fac[-1]] if len(fac) > 3 else fac, 4)
        v.line(pts + pts[:1], 7)
    da([(236, 662), (204, 596), (146, 520), (66, 458), (92, 548), (130, 632), (194, 694)],
       [(236, 662), (204, 596), (146, 520), (66, 458), (150, 584), (212, 680)])
    da([(194, 694), (126, 744), (72, 806), (34, 874), (126, 838), (198, 778), (242, 716)],
       [(242, 716), (198, 778), (126, 838), (34, 874), (138, 782), (206, 706)])
    da([(246, 668), (268, 620), (300, 676)], [(268, 620), (300, 676), (276, 672)])
    da([(258, 718), (288, 764), (312, 728)], [(288, 764), (312, 728), (292, 730)])
    da([(378, 680), (404, 628), (434, 672)], [(404, 628), (434, 672), (410, 674)])

    # 4. hàm dưới + bụng (cái bát trắng băng): mép môi dưới dày, cằm tròn nhô ra bên phải; dải sóng lam chạy dọc đáy bụng
    jaw = cr([C(*q) for q in reversed(MBOT)] + [C(985, 620), C(1010, 800), C(1030, 960), C(960, 1070), C(800, 1110), C(600, 1125),
              C(350, 1140), C(60, 1150), T(900, 800), T(840, 690), T(920, 420)], True)
    v.fill(jaw, c["belly"])
    wave = cs([(60, 990), (260, 962), (440, 1002), (330, 1010), (268, 1042), (410, 1108), (330, 1116), (250, 1100), (300, 1142),
               (60, 1150), (-40, 1080)])
    v.fill(wave, c["wave"], 5)
    for dy in (0, 26):
        v.line(cs([(520, 1040 + dy), (700, 1050 + dy), (860, 1030 + dy), (960, 985 + dy)], False), 4, c["groove"])

    # 5. lòng miệng: quả trứng nghiêng, khoé nhọn bên trái kéo dài vào thân; vòm họng sẫm ở trên, sàn miệng nhạt ở dưới
    mouth = cs(MTOP + MBOT[1:-1])
    v.fill(mouth, c["floor"], 0)
    palate = cs(MTOP[:-1] + [(760, 610), (600, 640), (430, 700), (280, 690)])
    v.fill(palate, c["palate"], 0)

    # 6. lưng + đuôi + hàm trên (vòm sẫm như cái mũ sọ): ôm quanh nửa trên miệng, má phải chạy xuống tới khớp hàm
    UNDER = [C(95, 648), T(860, 660), (600, 770), (480, 768), (360, 748), (232, 712)]      # mặt dưới cuống đuôi, thon dần
    body = cr(BACK, False) + cr([C(*q) for q in reversed(MTOP)], False) + cr(UNDER, False)
    v.fill(body, c["back"], 0)
    lip = cs(MTOP + [(985, 620), (985, 520), (975, 380), (880, 248), (700, 208), (520, 256), (396, 356), (310, 450), (240, 548)])
    v.fill(lip, c["lip"], 0)                                                    # dải môi trên nhạt hơn, dày
    v.line(cr(BACK, False), 7)
    v.line(cr(UNDER[1:], False) + [(218, 668)], 7)
    v.line(mouth + mouth[:1], 7)
    v.line(pc([(95, 648), (20, 640)]), 7)                                       # ranh hai hàm chạy từ khoé miệng về chân sau
    v.line(pc([(520, 200), (590, 184)]), 9)                                     # lỗ phun
    for bx, by, r in ((110, 470, 30), (196, 410, 22), (40, 528, 18)):          # ba con hà trên lưng
        b = cs([(bx - r, by + r * 0.7), (bx - r * 0.5, by - r * 0.6), (bx + r * 0.5, by - r * 0.7), (bx + r, by + r * 0.5)])
        v.fill(b, c["barn"], 5)

    # 7. nanh: rất to, cong, to nhỏ không đều; gốc bám trên môi (đè ra ngoài mép), mũi chĩa vào trong; hai hàng đan cài, không chạm
    fangs = [
        ("d5", [(790, 835), (838, 762), (872, 850), (850, 920)]),                                            # nanh dưới trong cùng
        ("u1", [(368, 512), (408, 418), (502, 452), (492, 560), (468, 668), (410, 610)]),
        ("u2", [(486, 436), (522, 288), (642, 268), (668, 344), (660, 470), (636, 566), (540, 500)]),
        ("u3", [(690, 334), (752, 246), (902, 268), (944, 398), (880, 500), (800, 584), (730, 470)]),
        ("u4", [(902, 440), (962, 398), (1012, 470), (1000, 590), (930, 660), (868, 706), (890, 560)]),
        ("u5", [(852, 628), (900, 600), (928, 660), (900, 730), (862, 700)]),
        ("d1", [(330, 792), (366, 700), (402, 668), (440, 744), (432, 860), (352, 852)]),
        ("d2", [(450, 792), (520, 716), (572, 688), (592, 850), (520, 940), (455, 900)]),
        ("d3", [(570, 900), (680, 790), (772, 718), (800, 872), (762, 992), (620, 1002)]),
        ("d4", [(800, 902), (850, 820), (882, 768), (922, 902), (882, 1012), (790, 1002)]),
    ]
    if k == 1:                              # cá voi con: sáu nanh
        keep = {"u2", "u3", "u4", "d2", "d3", "d4"}
        fangs = [(n, p) for n, p in fangs if n in keep]
    for n, p in fangs:
        if k == 1:                          # nanh sữa: co 0,72 về phía gốc nanh (đỉnh xa tâm miệng nhất)
            g = max(p, key=lambda q: (q[0] - 650) ** 2 + (q[1] - 620) ** 2)
            p = [(g[0] + (x - g[0]) * 0.72, g[1] + (y - g[1]) * 0.72) for x, y in p]
        v.fill(cs(p), c["fang"])
    if k == 2:
        v.line(pc([(760, 300), (800, 380), (780, 430)]), 3)                         # một vết nứt trên nanh to nhất

    # 8. vây ngực bên gần (dùng như chân chống): mỏm khuỷu nhọn ở trên, bản vây rộng dần xuống, đầu vây chia ba mấu tì đất;
    #    mỗi mấu bọc một móng đá mọc liền ra (móng vẽ trước, mấu vây đè lên gốc móng: không có khoanh ngăn giữa vây và móng)
    for cx in (745, 915, 1085):
        claw([(cx - 95, 944), (cx - 50, 850), (cx + 45, 850), (cx + 72, 944)], [(cx - 50, 850), (cx + 45, 850), (cx + 50, 944),
                                                                              (cx - 20, 944)], pt)
    flip = ts([(940, 268), (1075, 390), (1128, 520), (1140, 690), (1180, 790), (1190, 850), (1120, 874), (1040, 842), (960, 876),
               (880, 846), (800, 876), (724, 856), (704, 800), (760, 650), (778, 480), (850, 360)])
    v.fill(flip, c["back"])
    v.line(pt([(940, 268), (968, 500), (950, 720)]), 4)

    im = v.im.resize((W, H), Image.LANCZOS)
    out = os.path.join(HERE, "inbox", f"ca_voi_{k}", "mau", "bo_cuc.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im.save(out)
    print(out)


if __name__ == "__main__":
    for k in ([int(a) for a in sys.argv[1:]] or [2, 1]):
        ve(k)
