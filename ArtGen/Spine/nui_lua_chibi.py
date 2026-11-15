# -*- coding: utf-8 -*-
"""Khủng long núi lửa DẠNG 1 bản CHIBI (con non vẽ riêng; người dùng 2026-11-14 chọn concept A: inbox/nui_lua_non/tai_ve/L1_duyet.png).
Cùng xương, cùng clip với dạng lớn (nui_lua_rig.py, NL_DANG=chibi); tỉ lệ xương như hình bố cục đã dựng concept
(inbox/nui_lua_non/mau/bo_cuc_chibi.json). Dùng lại bộ cắt, bộ lắp và IK chân của hổ con (hoa_ho_chibi.py), chỉ đổi bảng.

MẢNH: gen "đúng chỗ, đúng cỡ" từ concept (nui_lua_non.py manh_prompt → tai_ve/C_THAN, C_CHAN, C_NUI, C_ONG, C_DAU), cắt theo cụm liền:
    c_chan2  chân sau xa (thứ hai từ trái)      TRỤ ĐÁ CỨNG trên một xương riêng <slot>_p (con của `move`), đáy đặt ở chỗ xương bàn chân
    c_chan4  chân trước xa (phải cùng)          sau xa / trước xa của họ; đỉnh trụ chui vào thân (xem ik)
    c_nui    núi lửa chính                      cứng trên bone28 (xương phiến đỉnh lưng của họ)
    c_ong_14 ống phải (sau đầu)                 cứng trên bone43 (xương ống 14 của họ: bẻ và giật theo chiêu cuối)
    c_ong_09 ống trái                           cứng trên bone40
    c_ong_02 ống trước                          cứng trên bone39
    c_chan1  chân sau gần (trái cùng)           trụ cứng, sau thân
    c_than   thân (tảng hông + khe dung nham + tảng vai)   tra trọng số theo lưới bụng P_duzi của họ (5 xương sống)
    c_chan3  chân trước gần (có móng)           trụ cứng, TRƯỚC thân (concept vẽ đỉnh chân này đè lên tảng vai)
  Chân: bản đầu dùng ba xương + IK gập gối của hổ con → lúc thân rạp (cast, skill) trụ đá ngắn bị gập nhàu, lòi gai. Đá không gập: mỗi chân là
  MỘT mảnh cứng, đáy bám chỗ bàn chân của họ, nghiêng nhẹ theo hướng lên hông, thân hạ thì đỉnh trụ chui vào thân, thân nhấc cao thì trụ dãn.
    c_dau    đầu trên (mắt, nụ sừng, răng trên); vùng hàm dưới tô màu lòng miệng        cứng trên bone7
    c_ham    hàm dưới ngà (tách khỏi ảnh đầu theo màu ngà)                              cứng trên xương riêng `ham_p` ở khớp hàm, góc theo bone8

    nui_lua_chibi.py cat     cắt năm tờ → inbox/nui_lua_non/manh_chibi/*.png + dat.json + _ghep.png (ghép lại so concept)
  Rig: NL_DANG=chibi py -3 -I nui_lua_rig.py → inbox/nui_lua_non/rig/
Xương, lưới, chuyển động gốc là của nhà phát hành game tham khảo: dùng nội bộ, không đăng công khai."""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hoa_ho_chibi as C  # noqa: E402

MA = os.environ.get("NL_MA", "nui_lua_non")           # nui_lua_non = dạng 1 (con non chibi); nui_lua_2 = dạng 2 (thiếu niên, 2026-11-15)
BASE = os.path.join(HERE, "inbox", MA)
TAI = os.path.join(BASE, "tai_ve")
MANH = os.path.join(BASE, "manh_chibi")
W, H = C.W, C.H
MIENG_MAU = (238, 118, 42)                            # lòng miệng: cam dung nham như concept
if MA == "nui_lua_2":
    # DẠNG 2 (concept A): năm tháp ống. Trên concept từ trái sang: tháp cao nhất = ống 10 (bone41), tháp thứ hai = 09 (bone40), tháp nhỏ
    # phía trước = 02 (bone39), tháp bên phải núi lửa = 14 (bone43), tháp trên đầu = 13 (bone44)
    THU_TU = ["c_chan2", "c_chan4", "c_ong_10", "c_ong_09", "c_ong_14", "c_nui", "c_ong_13", "c_ong_02", "c_chan1", "c_than", "c_chan3",
              "c_dau", "c_ham"]
    MIENG_ONG = {"cc": ("bone28", (770, 150), 90.0), "10": ("bone41", (345, 112), 95.0), "09": ("bone40", (515, 165), 92.0),
                 "02": ("bone39", (543, 365), 95.0), "14": ("bone43", (1025, 228), 85.0), "13": ("bone44", (1160, 320), 80.0)}
    HAM_KHOP = (925, 690)
    MIENG = ((1300, 700), -5.0)
    TO_ONG = [("C_ONG1", ["c_ong_10", "c_ong_14"]), ("C_ONG2", ["c_ong_09", "c_ong_13"])]      # mỗi tờ: tên mảnh theo thứ tự trái → phải
    KHOI = {"cc": (3, 1.15), "10": (2, 0.8), "09": (2, 0.8), "02": (1, 0.6), "14": (2, 0.7), "13": (1, 0.6)}
    BAN = ["cc", "10", "14", "09", "13", "02", "cc", "10", "14", "09", "13", "02"]             # chiêu cuối 12 phát
    IMPACT = {"attack": (0.09, 0.55, 0.13), "cast": (0.12, 0.72, 0.16, "#ffd9a055"), "skill": (0.18, 0.9, 0.19, "#fff3c066")}
    ONG_CHA = {"10": "bone3", "09": "bone4", "02": "bone4", "14": "bone6", "13": "bone6"}    # khúc thân mà chân tháp đứng lên (hông → vai)
    K_NGANG = 0.6                                     # phần ngẩng đầu thêm ở clip cast so với dạng lớn (dạng này đã ngẩng sẵn 26°)
else:
    THU_TU = ["c_chan2", "c_chan4", "c_nui", "c_ong_14", "c_ong_09", "c_ong_02", "c_chan1", "c_than", "c_chan3", "c_dau", "c_ham"]
    # miệng núi lửa / miệng ống trên concept (px) + hướng nhả (độ): chỗ khói bốc và chỗ đạn rời ống
    MIENG_ONG = {"cc": ("bone28", (640, 112), 90.0), "09": ("bone40", (372, 268), 100.0), "02": ("bone39", (522, 392), 95.0),
                 "14": ("bone43", (893, 178), 80.0)}
    HAM_KHOP = (800, 648)                             # khớp hàm trên concept (góc sau của hàm dưới): hàm quay quanh đây
    MIENG = ((1215, 600), -6.0)                       # giữa hai hàm, phía trước: chỗ tụ cầu lửa (bám bone7)
    TO_ONG = [("C_ONG", ["c_ong_09", "c_ong_14"])]
    KHOI = {"cc": (3, 1.0), "09": (2, 0.7), "02": (2, 0.65), "14": (1, 0.55)}
    BAN = ["cc", "09", "14", "02", "cc", "09", "14", "02"]                                     # chiêu cuối 8 phát, núi lửa chính cũng bắn
    IMPACT = {"attack": (0.08, 0.5, 0.12), "cast": (0.11, 0.65, 0.15, "#ffd9a055"), "skill": (0.16, 0.8, 0.18, "#fff3c066")}
    ONG_CHA = {"09": "bone3", "02": "bone4", "14": "bone6"}
    K_NGANG = 0.3
ONG = tuple(k for k in MIENG_ONG if k != "cc")


# chân: (xương thân mang hông, xương bàn chân của họ, pha bước ở clip walk: hai cặp chân chéo lệch nửa nhịp)
CHAN = {"c_chan1": ("bone3", "bone13", 0.0), "c_chan2": ("bone3", "bone25", 0.5), "c_chan3": ("bone5", "bone17", 0.5),
        "c_chan4": ("bone5", "bone21", 0.0)}


def cau_hinh():
    """đổi bảng của hoa_ho_chibi sang con này (gọi trước cat / lap)."""
    C.BASE, C.TAI, C.MANH = BASE, TAI, MANH
    C.THU_TU = THU_TU
    C.SINH_DOI, C.CHUOI, C.PHA, C.PHA_CAO = {}, {}, {}, {}
    C.NGUON = {"c_than": ("P_duzi",)}
    C.KIEU = {"c_than": "dong"}
    C.MUOT = {"c_than": 8}
    C.CUNG = {"c_dau": "bone7", "c_ham": "ham_p", "c_nui": "bone28"}
    C.CUNG.update({"c_ong_" + k: "ong_p_" + k for k in ONG})              # mỗi ống cứng trên xương riêng ở chân ống (xem xuong_ong)
    C.CUNG.update({s: s + "_p" for s in CHAN})
    C.KHOP = {}


def cat():
    cau_hinh()
    os.makedirs(MANH, exist_ok=True)
    dat = {}
    A, m = C._tach(C._moi("C_THAN"))
    C._luu(A, C._cum(m, 1)[0], "c_than", dat)
    A, m = C._tach(C._moi("C_CHAN"))
    cs = C._cum(m, 5)
    if len(cs) != 5:
        raise SystemExit(f"tờ CHAN có {len(cs)} cụm, cần 5 (bốn chân + ống trước)")
    i_ong = int(np.argmin([np.nonzero(c)[0].min() for c in cs]))        # ống trước: cụm có đỉnh cao nhất
    C._luu(A, cs[i_ong], "c_ong_02", dat)
    for k, c in enumerate([c for i, c in enumerate(cs) if i != i_ong]):   # bốn chân: trái → phải
        C._luu(A, c, f"c_chan{k + 1}", dat)
    A, m = C._tach(C._moi("C_NUI"))
    C._luu(A, C._cum(m, 1)[0], "c_nui", dat)
    for to, ten_manh in TO_ONG:
        A, m = C._tach(C._moi(to))
        cs = C._cum(m, len(ten_manh))
        if len(cs) != len(ten_manh):
            raise SystemExit(f"tờ {to} có {len(cs)} cụm, cần {len(ten_manh)}")
        for c, ten in zip(cs, ten_manh):
            C._luu(A, c, ten, dat)
    # đầu: tách HÀM DƯỚI theo màu ngà (cụm ngà lớn nhất; hai nụ sừng cũng ngà nhưng nhỏ và ở trên); chỗ hàm trên ảnh đầu tô màu lòng miệng
    A, m = C._tach(C._moi("C_DAU"))
    dau = C._cum(m, 1)[0]
    Ai = A.astype(int)
    nga = dau & (Ai[..., 0] > 195) & (Ai[..., 1] > 160) & (Ai[..., 0] - Ai[..., 2] > 38) & (Ai[..., 1] - Ai[..., 2] > 18)
    el = lambda r: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))  # noqa: E731
    nga = cv2.morphologyEx(nga.astype(np.uint8), cv2.MORPH_OPEN, el(2))
    n, lab, st, _ = cv2.connectedComponentsWithStats(nga, 8)
    ham_l = (lab == 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))).astype(np.uint8)
    ham_l = cv2.morphologyEx(ham_l, cv2.MORPH_CLOSE, el(9))              # lấp các nét nứt bên trong
    cnt, _ = cv2.findContours(ham_l, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    ham_l = cv2.drawContours(np.zeros_like(ham_l), cnt, -1, 1, -1)
    muc = Ai.max(2) < 120                                                # nét mực
    vien = (cv2.dilate(ham_l, el(10)) > 0) & muc & dau                   # viền mực quanh ngà
    ham = (ham_l > 0) | vien
    # ảnh ĐẦU: bỏ hàm dưới và viền NGOÀI của nó (để lại thì hàm hé xuống là lộ một nét viền thứ hai dưới cằm); giữ nét môi (viền kề phần
    # còn lại của đầu); chỗ hàm tô màu lòng miệng: phía trước tô cả (hàm há thì mũi hàm rơi hết chiều cao của nó), phía khoé chỉ một dải nông
    noi_dung = dau & ~muc & ~(ham_l > 0) & (Ai.min(2) < 236)
    moi = vien & (cv2.dilate(noi_dung.astype(np.uint8), el(12)) > 0)
    ys, xs = np.nonzero(ham_l)
    xa, xb = xs.min(), xs.max()
    dinh = np.full(W, H, int)
    day = np.zeros(W, int)
    for x in range(xa, xb + 1):
        col = np.flatnonzero(ham_l[:, x])
        if len(col):
            dinh[x], day[x] = col.min(), col.max()
    rel = np.clip((np.arange(W) - xa) / max(1, xb - xa), 0, 1)
    sau = (day - dinh) * np.clip(rel / 0.4, 0.18, 1.0)                   # độ sâu khoang miệng theo cột
    yy = np.arange(H)[:, None]
    khoang = (cv2.erode(ham_l, el(3)) > 0) & (yy <= (dinh + sau)[None, :])
    dau_m = (dau & ~ham) | moi | khoang
    A_dau = A.copy()
    A_dau[khoang] = MIENG_MAU
    C._luu(A_dau, dau_m, "c_dau", dat)
    C._luu(A, ham, "c_ham", dat)
    json.dump(dat, open(os.path.join(MANH, "dat.json"), "w"), indent=1)
    out = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    for ten in THU_TU:
        out.alpha_composite(Image.open(os.path.join(MANH, ten + ".png")), tuple(dat[ten]))
    con = Image.open(os.path.join(TAI, "L1_duyet.png")).convert("RGB")
    canh = Image.new("RGB", (W * 2, H), (255, 255, 255))
    canh.paste(con, (0, 0))
    canh.paste(out.convert("RGB"), (W, 0))
    canh.save(os.path.join(MANH, "_ghep.png"))
    d = np.abs(np.asarray(con).astype(int) - np.asarray(out.convert("RGB")).astype(int)).max(2)
    print(f"  ghép so concept: {100 * (d > 60).mean():.1f} % điểm lệch màu rõ → {os.path.join(MANH, '_ghep.png')}")


def xuong_ong(sk, WP, cpx):
    """xương riêng `ong_p_<k>` ở CHÂN từng tháp ống (con của khúc thân nó đứng lên: ONG_CHA); góc và tỉ lệ chép từ xương ống của họ ở từng khung
    (nui_lua_rig, lam_clip). Bám thẳng xương ống của họ thì tháp quay quanh gốc xương đó (ở xa chỗ tháp đứng trên concept): clip die, skill
    xoay mạnh làm tháp văng khỏi thân, lơ lửng."""
    dat = json.load(open(os.path.join(MANH, "dat.json")))
    for k in ONG:
        w, h = Image.open(os.path.join(MANH, f"c_ong_{k}.png")).size
        x0, y0 = dat["c_ong_" + k]
        p = cpx((x0 + w / 2, y0 + 0.86 * h))
        cha = ONG_CHA.get(k, "bone3")                 # khúc thân ngay dưới chân tháp: thân trước gục xuống thì tháp phía trước đi theo
        M = WP[cha]
        lp = np.linalg.solve(M, np.array([p[0], p[1], 1.0]))
        sk.xuong("ong_p_" + k, cha, float(lp[0]), float(lp[1]), goc=-float(np.degrees(np.arctan2(M[1, 0], M[0, 0]))))
    sk.ong_nl = [(k, MIENG_ONG[k][0]) for k in ONG]


def lap(sk, by, ten, Wc, P0, d_px, luoi, anh, cpx):
    """cpx: px concept → thế giới rig (ở dáng khung 0 idle). Dựng xương trụ chân trước, rồi lắp mọi mảnh bằng bộ lắp của hổ con."""
    cau_hinh()
    WP = sk.the_gioi(P0)
    dat = json.load(open(os.path.join(MANH, "dat.json")))
    ds = []
    for slot, (cha, ban, pha) in CHAN.items():
        w, h = Image.open(os.path.join(MANH, slot + ".png")).size
        x0, y0 = dat[slot]
        A = cpx((x0 + w / 2, y0 + h - 5))                                # đáy trụ (chỗ chạm đất)
        Hp = cpx((x0 + w / 2, y0 + 0.2 * h))                             # chỗ trụ cắm vào thân
        sk.xuong(slot + "_p", "move", float(A[0]), float(A[1]), goc=0.0)
        hip = np.linalg.solve(WP[cha], np.array([Hp[0], Hp[1], 1.0]))[:2]
        mc = np.linalg.solve(WP[ban], np.array([A[0], A[1], 1.0]))[:2]
        d0 = Hp - A
        ds.append(dict(b=slot + "_p", cha=cha, hip=hip, ban=ban, mc=mc, A0=A, H0=Hp, pha=pha, dai=float(np.hypot(*d0)),
                       g0=float(np.degrees(np.arctan2(d0[1], d0[0]))),
                       day=np.linalg.solve(WP[cha], np.array([A[0], A[1], 1.0]))[:2],      # đáy trụ trong hệ của xương thân mang nó
                       gcha0=float(np.degrees(np.arctan2(WP[cha][1, 0], WP[cha][0, 0])))))
    sk.chan_nl = ds
    # hàm dưới: xương riêng `ham_p` đặt ở khớp hàm, con của xương đầu; góc lấy theo xương hàm bone8 của họ (nui_lua_rig, lam_clip). Bám
    # thẳng bone8 thì hàm quay quanh gốc đầu (xa phía sau): mũi hàm lùi lại, lộ khoang miệng thành một vệt cam dưới cằm.
    kh = cpx(HAM_KHOP)
    lp = np.linalg.solve(WP["bone7"], np.array([kh[0], kh[1], 1.0]))
    sk.xuong("ham_p", "bone7", float(lp[0]), float(lp[1]), goc=0.0)
    return C.lap(sk, by, ten, Wc, P0, d_px, luoi, anh)


def ik(sk, P, t, ten, dur, theo=0.0):
    """đặt bốn trụ chân cho khung này (tính trong hệ chưa áp xương `move`). Clip `walk`: đáy trụ đi theo một vòng bước tự viết (hai nhịp mỗi
    vòng clip, hai cặp chân chéo lệch nửa nhịp). Clip khác: đáy trụ ở chỗ xương bàn chân của họ, nhưng không được lệch ngang quá 0,3 chiều
    dài trụ so với chỗ nghỉ dưới hông (chân của họ dài, duỗi xa: trụ ngắn của mình bám theo thì choãi quá). Trụ nghiêng nhẹ về phía hông; hông
    ở xa hơn chiều dài trụ thì trụ dãn dọc (không co: thân hạ thì đỉnh trụ chui vào thân).
    theo (0..1): phần chân ĐI THEO THÂN như gắn cứng vào thân (dùng lúc cả con rời đất hoặc đổ nghiêng: đang rơi ở appear, gục ở die). Người
    dùng 2026-11-14: "die lỗi chân" (thân đổ nghiêng mà chân vẫn đứng theo bàn chân của họ nên rời khỏi thân), "xuất hiện 2 chân trước bị bẻ
    ra trước hơi nhiều"."""
    ds = getattr(sk, "chan_nl", None)
    if not ds:
        return
    Q = P.copy()
    Q.t.pop("move", None)
    Wd = sk.the_gioi(Q)
    for c in ds:
        Hh = (Wd[c["cha"]] @ np.array([c["hip"][0], c["hip"][1], 1.0]))[:2]
        if ten == "walk":
            ph = 2 * np.pi * (2 * t / dur + c["pha"])
            T = np.array([Hh[0] + (c["A0"][0] - c["H0"][0]) - 0.34 * c["dai"] * np.cos(ph), c["A0"][1] + 0.26 * c["dai"] * max(0.0, np.sin(ph))])
        else:
            T = (Wd[c["ban"]] @ np.array([c["mc"][0], c["mc"][1], 1.0]))[:2]
            nghi = Hh[0] + (c["A0"][0] - c["H0"][0])                # chỗ nghỉ của đáy trụ: dưới hông như ở dáng đứng
            T[0] = nghi + float(np.clip(T[0] - nghi, -0.3 * c["dai"], 0.3 * c["dai"]))
            T[1] = max(float(T[1]), float(c["A0"][1]) - 6.0)     # không lún dưới mặt đất (bàn chân của họ có lúc ấn xuống lúc dộng)
        d = Hh - T
        lech = (float(np.degrees(np.arctan2(d[1], d[0]))) - c["g0"] + 180.0) % 360.0 - 180.0
        goc = float(np.clip(0.6 * lech, -20.0, 20.0))
        k = float(np.hypot(*d)) / c["dai"]
        if theo > 0.001:                                           # đi theo thân: đáy trụ và góc trụ như gắn cứng vào xương thân
            Wc_ = Wd[c["cha"]]
            Tf = (Wc_ @ np.array([c["day"][0], c["day"][1], 1.0]))[:2]
            gf = (float(np.degrees(np.arctan2(Wc_[1, 0], Wc_[0, 0]))) - c["gcha0"] + 180.0) % 360.0 - 180.0
            T = T + (Tf - T) * theo
            goc = goc + (gf - goc) * theo
            k = 1.0 + (k - 1.0) * (1.0 - theo)
        P.move(c["b"], float(T[0] - c["A0"][0]), float(T[1] - c["A0"][1]))
        P.rot(c["b"], goc)
        if k > 1.02:
            P.scale(c["b"], 1.0, min(k, 1.8))


if __name__ == "__main__":
    if sys.argv[1:2] == ["cat"]:
        cat()
    else:
        print(__doc__)
