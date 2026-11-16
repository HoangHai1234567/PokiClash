# -*- coding: utf-8 -*-
"""Tinh linh tinh thể sắt DẠNG 2 (tinh_sat_2, rig monster_3347): ảnh mẫu cả con gốc + prompt concept.

Concept = thân hình (từng mảnh, chỗ, cỡ, thứ tự chồng) của con gốc 3347 + màu, chất liệu (tinh thể SẮT), kiểu mặt, nét vẽ của dạng 1 đã duyệt
(`inbox/tinh_sat_1/tai_ve/L1_duyet.png`). Đổi dáng mảnh nhận diện ngay lượt đầu (memory doi-dang-manh-nhan-dien): chỏm tinh thể trên đỉnh thành
vương miện ba mũi nhọn (gợi ba tinh thể trên đầu dạng 1), năm tinh thể bay dài, nhọn hơn. Ít chi tiết như con gốc (memory concept-it-chi-tiet).

    tinh_sat_2_da.py ca_con     cả con gốc ở khung 0 idle trên nền trắng → inbox/tinh_sat_2/mau/goc_ca_con.png (+ .json tỉ lệ) + bảng chỗ mảnh
    tinh_sat_2_da.py concept    ba file prompt concept → gui_gpt/tinh_sat_2/luot_1_concept_<A|B|C>.txt + HUONG_DAN.md
Ảnh con gốc là của game tham khảo: chỉ dùng trong máy làm mẫu, không đăng công khai."""
import json
import os
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tinh_sat_2 as G  # noqa: E402
from quai.soi import _tris  # noqa: E402

W, H = 1536, 1024
GUI = os.path.join(HERE, "gui_gpt", "tinh_sat_2")
GOC = os.path.join(G.MAU, "goc_ca_con.png")
DANG1 = os.path.join(HERE, "inbox", "tinh_sat_1", "tai_ve", "L1_duyet.png")
MUC = "#2B2118"

# mảnh của con gốc → tên đọc trong prompt
TEN = {"P_lian": "mat", "P_yanjing": "mat_mat", "P_lian_1": "vo", "P_maozi": "mu", "P_zui": "cam",
       "P_tui_R2": "chan_trai_tren", "P_tui_R1": "chan_trai_duoi", "P_tui_L2": "chan_phai_tren", "P_tui_L1": "chan_phai_duoi",
       "P_bc_01": "bay_trai", "P_bc_02": "bay_tren_trai", "P_bc_03": "bay_tren_phai", "P_bc_04": "bay_phai", "P_bc_05": "bay_duoi_phai"}


def Wp(p):
    return os.path.normpath(p)


def ghi(p, lines):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def luu(ten):
    out = os.path.join(G.TAI, ten + ".png")
    return out, [f"SAVE: save it as a PNG to {Wp(out)}",
                 f"If a file with that name already exists, save as {ten}_2.png, {ten}_3.png ... in the same folder. Do not edit, move or "
                 "delete any other file."]


def khung(atts, cao=760.0):
    P = np.concatenate([np.array(a["xy"], float).reshape(-1, 2) for a in atts])
    x0, y0, x1, y1 = P[:, 0].min(), P[:, 1].min(), P[:, 0].max(), P[:, 1].max()
    s = min(cao / (y1 - y0), 1250.0 / (x1 - x0))
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    return s, cx, cy, (lambda V: np.stack([W / 2 + (V[:, 0] - cx) * s, H / 2 - (V[:, 1] - cy) * s], 1))


def ca_con():
    """cả con gốc ở khung 0 idle, nền trắng, khung 1536 × 1024; in khung từng mảnh (px trên ảnh) → mau/goc_ca_con.json."""
    _, imgs, atts = G.nap("att_idle0.json")
    s, cx, cy, T = khung(atts)
    S = 2
    can = Image.new("RGBA", (W * S, H * S), (255, 255, 255, 255))
    vung = {}
    for a in atts:
        im = G.part_goc(a)
        uv, tr = G.luoi(a)
        V = T(np.array(a["xy"], float).reshape(-1, 2))
        lay = Image.new("RGBa", (W * S, H * S), (0, 0, 0, 0))
        _tris(lay, im.convert("RGBa"), V * S, uv, tr)
        lay = lay.convert("RGBA")
        can.alpha_composite(lay)
        A = np.asarray(lay)[..., 3] > 40                                  # khung theo điểm ảnh thật (không theo lưới)
        ys, xs = np.nonzero(A)
        vung[a["slot"]] = [int(xs.min() / S), int(ys.min() / S), int(xs.max() / S), int(ys.max() / S)]
    os.makedirs(G.MAU, exist_ok=True)
    can.convert("RGB").resize((W, H), Image.LANCZOS).save(GOC)
    json.dump(dict(s=s, cx=cx, cy=cy, vung=vung), open(GOC[:-4] + ".json", "w"), indent=1)
    print(GOC, f"tỉ lệ {s:.3f} px / đơn vị")
    for k, v in vung.items():
        print(f"  {k:12s} {TEN.get(k, '?'):16s} x {v[0]}–{v[2]}, y {v[1]}–{v[3]}")


# ------------------------------------------------------------------ sơ đồ bố cục (Codex từ chối khi đính hình con gốc, 2026-11-16)
# Hình bóng từng mảnh của rig ở khung 0 idle (cùng khung với goc_ca_con.png), tô HAI tông phẳng của thiết kế mình (mặt chính / mặt bên tách theo
# độ sáng của mảnh gốc), viền mực; chỏm đỉnh P_maozi thay bằng VƯƠNG MIỆN ba mũi vẽ bằng mã; năm tinh thể bay kéo dài 1,15 lần (thon 0,9) từ đầu
# trong. Không mang nét, vân, màu của con gốc.
S2 = 2
INK = (43, 33, 24)
TAM_MAT = (820.0, 610.0)            # tâm mặt trên ảnh (px), để biết đầu nào của tinh thể bay là đầu trong
VUONG_MIEN = [                       # mỗi mũi: (đáy trái, [điểm đáy thêm], đáy phải, đỉnh); vẽ trái → phải → giữa (giữa đè lên)
    ((668, 400), [], (800, 515), (652, 236)),
    ((878, 505), [], (1006, 444), (982, 292)),
    ((758, 505), [(895, 557)], (962, 478), (796, 172)),
]


def hx(s):
    s = s.lstrip("#")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


MAU_BO_CUC = {   # vai → (mặt chính, mặt bên, màu nét trong)
    "A": dict(vo=("#8EA3CB", "#5E6F9C", None), mu=("#8EA3CB", "#5E6F9C", None), chan=("#8EA3CB", "#5E6F9C", None),
              cam=("#BCD3DA", "#86A2AD", None), bay=("#A79FD3", "#7570A8", None), mat="#F7F4EC", mat_mat="#F3C536", mi="#2C2A5C",
              may=True),
    "B": dict(vo=("#6F84BC", "#4B5A8E", None), mu=("#8EA3CB", "#5E6F9C", None), chan=("#A79FD3", "#7570A8", None),
              cam=("#A79FD3", "#7570A8", None), bay=("#8EA3CB", "#5E6F9C", None), mat="#2C3150", mat_mat="#F3C536", mi="#1E2238",
              may=False),
    "C": dict(vo=("#646B7E", "#3F4455", "#C8CDD8"), mu=("#8EA3CB", "#5E6F9C", None), chan=("#646B7E", "#3F4455", "#C8CDD8"),
              cam=("#646B7E", "#3F4455", "#C8CDD8"), bay=("#8EA3CB", "#5E6F9C", None), mat="#2C3150", mat_mat="#F3C536", mi="#1E2238",
              may=False),
}


def vai(slot):
    if slot.startswith("P_bc_"):
        return "bay"
    if slot.startswith("P_tui"):
        return "chan"
    return {"P_lian": "mat", "P_yanjing": "mat_mat", "P_lian_1": "vo", "P_zui": "cam", "P_maozi": "mu"}.get(slot)


def el(r):
    import cv2
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def vien(m, r):
    import cv2
    return m & ~cv2.erode(m.astype(np.uint8), el(r)).astype(bool)


def keo_dai(lay, k=1.15, mong=0.9):
    """kéo dài một tinh thể bay dọc trục chính của nó, giữ yên đầu trong (đầu gần tâm mặt)."""
    import cv2
    A = np.asarray(lay).astype(np.float32)
    ys, xs = np.nonzero(A[..., 3] > 110)
    P = np.stack([xs, ys], 1).astype(np.float64)
    c = P.mean(0)
    u = np.linalg.svd(P - c, full_matrices=False)[2][0]
    t = (P - c) @ u
    tam = np.array(TAM_MAT) * S2
    a = c + u * (t.min() if np.linalg.norm(c + u * t.min() - tam) < np.linalg.norm(c + u * t.max() - tam) else t.max())
    n = np.array([-u[1], u[0]])
    R = np.stack([u, n], 1)
    M = R @ np.diag([k, mong]) @ R.T
    b = a - M @ a
    out = cv2.warpAffine(A, np.hstack([M, b[:, None]]), (A.shape[1], A.shape[0]), flags=cv2.INTER_LINEAR, borderValue=0)
    return out


def mui(can, day_l, them, day_r, dinh, chinh, ben):
    """một mũi tinh thể: đa giác đáy → vai → đỉnh; sống từ đỉnh xuống giữa đáy chia nửa trái (mặt chính) / nửa phải (mặt bên)."""
    import cv2
    L, Rr, D = np.array(day_l, float), np.array(day_r, float), np.array(dinh, float)
    giua = (L + Rr) / 2
    truc = D - giua
    n = np.array([-truc[1], truc[0]]) / np.linalg.norm(truc)
    vl = L + (D - L) * 0.55 - n * 14 * np.sign(np.dot(L - giua, -n) or 1) * -1
    vr = Rr + (D - Rr) * 0.55 + n * 14 * np.sign(np.dot(Rr - giua, n) or 1)
    poly = [L] + [np.array(p, float) for p in them] + [Rr, vr, D, vl]
    P = (np.array(poly) * S2).astype(np.int32)
    m = np.zeros(can.shape[:2], np.uint8)
    cv2.fillPoly(m, [P], 1)
    m = m.astype(bool)
    can[m] = chinh
    nua = np.zeros_like(m, np.uint8)                                    # nửa phải của sống = mặt bên
    Q = (np.array([D, vr, Rr] + [np.array(p, float) for p in them][::-1] + [giua]) * S2).astype(np.int32)
    cv2.fillPoly(nua, [Q], 1)
    can[m & nua.astype(bool)] = ben
    cv2.line(can, tuple((D * S2).astype(int)), tuple((giua * S2).astype(int)), INK, 3 * S2 // 2 + 1, cv2.LINE_AA)
    can[vien(m, 3 * S2)] = INK
    return m


def mat_phang(A, m, k=3):
    """chia mảnh gốc thành k mặt phẳng theo độ sáng (bỏ viền mực của họ), trả nhãn 0 (tối nhất) .. k-1 cho mọi điểm của m (-1 ngoài m)."""
    import cv2
    g = cv2.cvtColor(np.clip(A[..., :3] / np.maximum(A[..., 3:4], 1) * 255, 0, 255).astype(np.uint8), cv2.COLOR_RGB2GRAY)
    trong = cv2.erode(m.astype(np.uint8), el(10 * S2)).astype(bool)
    lab = np.full(m.shape, -1, np.int16)
    if trong.sum() < 50:
        lab[m] = 1
        return lab
    z = g[trong].reshape(-1, 1).astype(np.float32)
    _, l, c = cv2.kmeans(z, k, None, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.5), 3, cv2.KMEANS_PP_CENTERS)
    thu = np.argsort(np.argsort(c.ravel()))
    L = np.zeros(m.shape, np.uint8)
    L[trong] = thu[l.ravel()] + 1
    for _ in range(4):
        L = cv2.medianBlur(L, 11)
        L[~trong] = 0

    def lap(L, vung):
        """điểm của `vung` chưa có nhãn lấy nhãn của điểm có nhãn gần nhất."""
        _, idx = cv2.distanceTransformWithLabels((L == 0).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
        zy, zx = np.nonzero(L > 0)
        bang = np.zeros(idx.max() + 1, np.uint8)
        bang[idx[zy, zx]] = L[zy, zx]
        L2 = bang[idx]
        L2[L > 0] = L[L > 0]
        L2[~vung] = 0
        return L2

    amin = (20 * S2) ** 2                                                # mảng nhỏ (vệt sáng, vạch) gộp vào mảng kề
    for lv in range(1, k + 1):
        n, cc, st, _ = cv2.connectedComponentsWithStats((L == lv).astype(np.uint8))
        for i in range(1, n):
            if st[i, 4] < amin:
                L[cc == i] = 0
    if (L > 0).any():
        L = lap(L, trong)
        L = lap(L, m)                                                    # vành ngoài (viền mực của họ đã bỏ)
    lab[m] = L[m].astype(np.int16) - 1
    return lab


def canh_thang(lab, m):
    """ranh giữa các mặt phẳng kẻ thành đường gấp khúc thẳng (đa giác xấp xỉ), trong lòng mảnh."""
    import cv2
    out = np.zeros(m.shape, np.uint8)
    for lv in np.unique(lab[m]):
        n, cc = cv2.connectedComponents(((lab == lv) & m).astype(np.uint8))
        for i in range(1, n):
            cs, _ = cv2.findContours((cc == i).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            for c in cs:
                p = cv2.approxPolyDP(c, 3.0 * S2, True)
                cv2.polylines(out, [p], True, 1, max(2, int(1.4 * S2)), cv2.LINE_AA)
    return out.astype(bool) & cv2.erode(m.astype(np.uint8), el(4 * S2)).astype(bool)


def mat_na():
    """hình bóng ĐỦ (cả phần bị che) của từng mảnh trên ảnh 1536 × 1024 theo thiết kế dạng 2: tinh thể bay đã kéo dài, P_maozi = vương miện."""
    import cv2
    G.H._C.pop("att", None)
    _, imgs, atts = G.nap("att_idle0.json")
    s, cx, cy, T = khung(atts)
    out = {}
    for a in atts:
        v = vai(a["slot"])
        if v is None:
            continue
        if v == "mu":
            m = np.zeros((H * S2, W * S2), np.uint8)
            for day_l, them, day_r, dinh in VUONG_MIEN:
                tmp = np.full((H * S2, W * S2, 3), 255, np.uint8)
                m |= mui(tmp, day_l, them, day_r, dinh, (0, 0, 0), (0, 0, 0)).astype(np.uint8)
        else:
            im = G.part_goc(a)
            uv, tr = G.luoi(a)
            V = T(np.array(a["xy"], float).reshape(-1, 2)) * S2
            lay = Image.new("RGBa", (W * S2, H * S2), (0, 0, 0, 0))
            _tris(lay, im.convert("RGBa"), V, uv, tr)
            A = keo_dai(lay) if v == "bay" else np.asarray(lay).astype(np.float32)
            m = (A[..., 3] > 110).astype(np.uint8)
            m = (cv2.GaussianBlur(cv2.morphologyEx(m, cv2.MORPH_CLOSE, el(4)) * 255, (0, 0), 3) > 127).astype(np.uint8)
        out[a["slot"]] = cv2.resize(m, (W, H), interpolation=cv2.INTER_AREA) > 0
    return out


def bo_cuc(huong):
    import cv2
    C = MAU_BO_CUC[huong]
    G.H._C.pop("att", None)
    _, imgs, atts = G.nap("att_idle0.json")
    s, cx, cy, T = khung(atts)
    can = np.full((H * S2, W * S2, 3), 255, np.uint8)
    for a in atts:
        v = vai(a["slot"])
        if v is None:
            continue
        if v == "mu":
            for day_l, them, day_r, dinh in VUONG_MIEN:
                mui(can, day_l, them, day_r, dinh, hx(C["mu"][0]), hx(C["mu"][1]))
            continue
        im = G.part_goc(a)
        uv, tr = G.luoi(a)
        V = T(np.array(a["xy"], float).reshape(-1, 2)) * S2
        lay = Image.new("RGBa", (W * S2, H * S2), (0, 0, 0, 0))
        _tris(lay, im.convert("RGBa"), V, uv, tr)
        A = keo_dai(lay) if v == "bay" else np.asarray(lay).astype(np.float32)
        m = A[..., 3] > 110
        m = cv2.GaussianBlur(cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_CLOSE, el(4)) * 255, (0, 0), 3) > 127
        if not m.any():
            continue
        if v == "mat":
            can[m] = hx(C["mat"])
            can[vien(m, 3 * S2)] = INK
            continue
        if v == "mat_mat":                                               # vàng = lòng mắt, phần đục còn lại = mí / viền
            rgb = A[..., :3] / np.maximum(A[..., 3:4], 1) * 255
            vang = m & (rgb[..., 0] > 150) & (rgb[..., 1] > 120) & (rgb[..., 2] < 140)
            vang = cv2.morphologyEx(vang.astype(np.uint8), cv2.MORPH_OPEN, el(2)).astype(bool)
            can[m] = hx(C["mi"])
            can[vang] = hx(C["mat_mat"])
            n, lab, st, ce = cv2.connectedComponentsWithStats(vang.astype(np.uint8))
            for i in range(1, n):
                if st[i, 4] < 200:
                    continue
                x, y, w, h = st[i, :4]
                cv2.circle(can, (int(x + w * 0.62), int(y + h * 0.38)), 4 * S2, (255, 255, 255), -1, cv2.LINE_AA)
                if C["may"]:                                             # mày: nét dày nghiêng, đầu trong thấp
                    trong_phai = x + w / 2 < TAM_MAT[0] * S2 + 30 * S2
                    xi, xo = (x + w, x) if trong_phai else (x, x + w)
                    cv2.line(can, (int(xo), int(y - 16 * S2)), (int(xi), int(y - 4 * S2)), hx(C["mi"]), 7 * S2, cv2.LINE_AA)
            continue
        chinh, ben, net = (hx(q) if q else None for q in C[v])
        lab = mat_phang(A, m, 3 if v == "vo" else 2)
        can[m] = chinh
        can[m & (lab == 0)] = ben                                        # mặt tối nhất của mảnh gốc = mặt bên
        can[canh_thang(lab, m)] = net or INK
        can[vien(m, 3 * S2)] = INK
    im = Image.fromarray(can, "RGB").resize((W, H), Image.LANCZOS)
    p = os.path.join(G.MAU, f"bo_cuc_{huong}.png")
    im.save(p)
    print(p)
    return p


def _o(v, k, pad=0):
    x0, y0, x1, y1 = v[k]
    r = lambda q: int(round(q / 5.0) * 5)  # noqa: E731
    return f"about x = {r(x0 - pad)} to x = {r(x1 + pad)}, y = {r(y0 - pad)} to y = {r(y1 + pad)}"


# ba hướng (Claude đề xuất, chờ người dùng chọn). (tên Việt, mô tả mặt tiếng Anh, bảng màu tiếng Anh, mô tả Việt cho HUONG_DAN)
# Con gốc 3347 không có miệng và dưới mắt là hai tinh thể cằm (không còn chỗ): không hướng nào vẽ miệng.
HUONG = {
    "A": ("mặt kem + mày, giáp thép lam (gần dạng 1 nhất)",
          "THE FACE ({mat}): the face window is the stage-1 spirit's warm milky-white body #F7F4EC peeking out of the armour (one flat "
          "colour). THE EYES ({mat_mat}): two golden-yellow #F3C536 eyes with a thick dark-navy rim #2C2A5C along the top, ONE tiny light "
          "dot each, shaped and slanted as in image 1 (the inner corners low, an angry, determined look); above each eye a short thick "
          "angled navy BROW stroke as in image 1 (inner ends low). No mouth (the chin crystals sit right under the eyes).",
          "COLOURS (each area ONE flat colour, exactly as image 1): the SHELL, the CROWN and the two LEGS are BLUE STEEL like the big "
          "crystals of image 2: main faces #8EA3CB, side faces darker steel blue #5E6F9C. The two CHIN crystals are pale SILVER-CYAN steel: "
          "main faces #BCD3DA, side faces #86A2AD. The five FLOATING shards are LAVENDER STEEL like the tail of image 2: main faces "
          "#A79FD3, side faces #7570A8.",
          "mặt kem như thân dạng 1, mắt vàng viền xanh đen + mày, không miệng; vỏ, vương miện, chân thép lam (#8EA3CB); cằm bạc lam nhạt; "
          "năm tinh thể bay thép oải hương"),
    "B": ("mặt sắt tối, mắt vàng xếch như con gốc, giáp thép lam đậm",
          "THE FACE ({mat}): the face window is dark navy IRON #2C3150 (one flat colour), like a dark visor inside the armour. THE EYES "
          "({mat_mat}): two golden-yellow #F3C536 eyes with a dark lid rim #1E2238 along the top, ONE tiny light dot each, shaped and "
          "slanted as in image 1 (the inner corners low, an angry, determined look). No brows, no mouth: the face is only the two eyes on "
          "the dark visor.",
          "COLOURS (each area ONE flat colour, exactly as image 1): the SHELL is deep COBALT STEEL: main faces #6F84BC, side faces #4B5A8E. "
          "The CROWN and the five FLOATING shards are bright BLUE STEEL like the big crystals of image 2: main faces #8EA3CB, side faces "
          "#5E6F9C. The two CHIN crystals and the two LEGS are LAVENDER STEEL like the tail of image 2: main faces #A79FD3, side faces "
          "#7570A8.",
          "mặt sắt xanh than (#2C3150), chỉ hai mắt vàng xếch như con gốc, không mày không miệng; vỏ thép lam đậm (#6F84BC); vương miện + "
          "năm tinh thể bay thép lam như dạng 1; cằm + chân thép oải hương"),
    "C": ("mặt sắt tối, giáp sắt rèn xám than, lưỡi tinh thể thép lam",
          "THE FACE ({mat}): the face window is dark navy IRON #2C3150 (one flat colour), like a dark visor inside the armour. THE EYES "
          "({mat_mat}): two golden-yellow #F3C536 eyes with a dark lid rim #1E2238 along the top, ONE tiny light dot each, shaped and "
          "slanted as in image 1 (the inner corners low, an angry, determined look). No brows, no mouth.",
          "COLOURS (each area ONE flat colour, exactly as image 1): the SHELL, the two CHIN crystals and the two LEGS are dark FORGED IRON: "
          "main faces gunmetal grey #646B7E, side faces darker iron #3F4455; on these iron pieces the INNER facet lines are thin "
          "pale-silver lines #C8CDD8 instead of ink (the outline stays dark-brown ink). The CROWN and the five FLOATING shards are bright "
          "BLUE STEEL like the big crystals of image 2: main faces #8EA3CB, side faces #5E6F9C.",
          "mặt sắt xanh than, mắt vàng xếch; vỏ, cằm, chân sắt rèn xám than (#646B7E, cạnh mặt bạc); vương miện + năm tinh thể bay thép lam "
          "như dạng 1"),
}

STYLE = (
    f"DRAWING STYLE (very important): exactly the hand-drawn look of image 2: a wobbly dark-brown INK outline ({MUC}, about 7 px) running "
    "all the way round every piece exactly on its silhouette, thinner ink lines (about 3 px) for the inner FACET edges of every crystal "
    "(the facet edges of image 1, as a few clean straight lines), and every area filled with ONE flat colour with visible coloured-pencil "
    "/ wax-crayon hatching. Image 1 is a flat computer diagram with jagged outlines: redraw it by hand, cleanly; keep its shapes and its "
    "colour areas, not its jagged digital edges. No shading, no highlights, no white shine streaks on the crystals, no gradients, no glow, "
    "no shadows, no gloss, no sparkles: flat colour only. A different tone appears only where a different face (main face / side face) or "
    "material is listed. The only exception: one tiny light dot in each eye. Drawn carefully and cleanly, not scribbled.")
BG = "Plain pure-white background (#FFFFFF), no paper grain outside the drawing, no labels, no numbers, no frame, nothing added."


def prompt_concept():
    v = json.load(open(GOC[:-4] + ".json"))["vung"]
    o = {TEN[k]: _o(v, k) for k in v if k in TEN}
    for c, (a, b) in dict(chan_trai=("P_tui_R2", "P_tui_R1"), chan_phai=("P_tui_L2", "P_tui_L1")).items():
        q = [min(v[a][0], v[b][0]), min(v[a][1], v[b][1]), max(v[a][2], v[b][2]), max(v[a][3], v[b][3])]
        o[c] = _o({c: q}, c)
    anh2 = (DANG1, "STAGE 1 of the SAME creature, our approved design, 1536x1024, white background: a small cream round spirit with golden "
                   "eyes, angled navy brows, a one-fang smile, surrounded by faceted steel-blue IRON crystals, a lavender crystal tail, "
                   "drawn in our hand-drawn style (wobbly dark-brown ink outline, crayon hatching, completely flat colours). Take from it the "
                   "MATERIAL (iron crystals with flat main and side faces), the face style and the DRAWING STYLE. Do NOT copy its body plan.",
            "Dạng 1 đã duyệt (1536 × 1024, nền trắng): thân kem, mắt vàng, mày xếch, răng nanh, 9 tinh thể thép lam, đuôi oải hương. Lấy chất "
            "liệu, kiểu mặt, nét vẽ; không lấy thân hình")
    hd = ["# Gói GPT: tinh linh tinh thể sắt DẠNG 2 (tinh_sat_2), tướng 1 đảo Kim", "",
          "Con gốc của rig: `monster_3347` (game tham khảo, dạng tiến hoá của `monster_3346` mà dạng 1 bám). Codex từ chối khi đính hình con "
          "gốc (`mau/goc_ca_con.png`, chỉ để Claude đo), nên ảnh mẫu 1 là SƠ ĐỒ BỐ CỤC máy dựng từ rig (`tinh_sat_2_da.py bo_cuc`): hình "
          "bóng từng mảnh tô hai tông phẳng của hướng đó, đã vẽ sẵn vương miện ba mũi và năm tinh thể bay dài hơn.", "",
          "## Lượt 1: concept dạng 2, ba hướng (2026-11-16)", "",
          "Người dùng: \"quét tướng 1 đảo kim mới làm và làm dạng 2 của nó\"; chọn rig 3347; dòng 2 dạng (dạng 2 là dạng cuối); đòn, chiêu "
          "như dạng 1 nhưng mạnh hơn. Ba hướng là đề xuất của Claude. Cả ba giữ thân hình 3347, đổi chỏm đầu thành vương miện ba mũi tinh "
          "thể (gợi ba tinh thể trên đầu dạng 1), năm tinh thể bay dài, nhọn hơn ~15 %; không miệng (như con gốc).", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|",
          "| 1 | `" + Wp(os.path.join(G.MAU, "bo_cuc_<A|B|C>.png")) + "` | Sơ đồ bố cục của hướng đó (1536 × 1024, nền trắng, máy vẽ, viền răng "
          "cưa): mặt ở giữa có hai mắt vàng xếch, vỏ tinh thể chữ C ôm mặt, vương miện ba mũi trên đỉnh, hai tinh thể che cằm, hai chân "
          "ngắn, năm tinh thể bay quanh; mỗi mảnh hai tông phẳng (mặt chính / mặt bên) đúng màu của hướng |",
          f"| 2 | `{Wp(DANG1)}` | {anh2[2]} |", ""]
    for k, (vi, mat_en, mau_en, vi2) in HUONG.items():
        so = os.path.join(G.MAU, f"bo_cuc_{k}.png")
        anh1 = (so, "LAYOUT GUIDE of the creature to draw, 1536x1024, white background, assembled by computer from the animation rig: "
                    "every piece already at its final place, size, angle and overlap, filled with the final flat colours (main face / "
                    "side face) and with its main facet edges. Seen from the front, turned slightly to the viewer's RIGHT: a face window "
                    "with two slanted yellow eyes, a C-shaped shell of chunky crystal plates round the face, a crown of three crystal "
                    "spikes on top, two chin crystals in front of the lower face, two stubby legs, five slim crystal shards floating "
                    "around. It is crude (jagged edges, no drawing style). Follow its SHAPES, PLACES and COLOURS exactly.")
        out, save = luu(f"L1_{k}")
        p = os.path.join(GUI, f"luot_1_concept_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(anh1[0])}: {anh1[1]}", f"image 2 = {Wp(anh2[0])}: {anh2[1]}"]
        t += [""] + save + ["",
              "TASK: draw STAGE 2, the FINAL evolved form of the iron-crystal spirit of image 2, exactly as laid out in image 1: the same "
              "pose, the same view (front, turned slightly to the viewer's right), every piece at the same place and the same size with the "
              "same overlaps (laid over image 1, every piece must coincide) and in the same colours, redrawn cleanly by hand in the style of "
              "image 2. It is the grown-up, battle-ready form: the soft little spirit of image 2 now wears a full ARMOUR of iron crystals. "
              "Determined and ready to fight; still cute, not scary. Do not add, remove or merge pieces; keep the white gaps between pieces "
              "where image 1 has gaps.", "",
              "PIECE BY PIECE (positions on the 1536x1024 canvas, as in image 1):",
              "- " + mat_en.format(**o),
              f"- THE SHELL ({o['vo']}): a C-shaped band of chunky faceted crystal plates wrapped round the face: from the lower left, over "
              "the top, down the right side, ending at the lower right of the face. Keep its lumpy faceted outline, its plates and its "
              "size as in image 1.",
              "- THE CROWN (about x = 650 to x = 1005, y = 170 to y = 560): THREE sharp crystal spikes growing from the top of the shell, "
              "like the three crystals on the head of image 2: the middle one the tallest, leaning a little to the left; a shorter one on "
              "each side. Each spike has one ridge line from its tip down to its base, one side main colour, the other side the side "
              "colour. Its base covers the top edge of the face as in image 1.",
              f"- THE CHIN ({o['cam']}): two chunky faceted crystals side by side in front of the lower face, like a jaw guard.",
              f"- THE LEGS (left leg {o['chan_trai']}; right leg {o['chan_phai']}): two short stubby legs under the body, each a rounded "
              "upper part and a faceted crystal foot. Both legs clearly grow out from under the shell and the chin: no white gap between "
              "a leg and the body.",
              "- THE FIVE FLOATING SHARDS (slim pointed crystal blades, as in image 1): a long one at the left pointing out to the left; a "
              "slim one at the upper left pointing up and to the left; a long slim one at the upper right, slanting like a halo above the "
              "head; one at the right, half behind the shell, pointing to the right; a small one at the lower right behind the shell "
              "pointing down and to the right. Each shard is separate with its own complete outline and a sharp tip.", "",
              mau_en, "",
              "VERY SIMPLE DESIGN, FEW DETAILS (like image 1): no extra spikes on the shell, no badges, no rivets, no bands, no cracks, no "
              "runes, no chains, no weapons, no mouth, no cheek marks, nothing that is not in image 1.", "",
              STYLE, "",
              "CANVAS: landscape 1536x1024, pure-white background, no ground line, no cast shadow; the creature at the same place and size as "
              "in image 1. No sparkles, no glints, no dust, no glow, no speed lines.", BG]
        ghi(p, t)
        hd += [f"- **Hướng {k}** ({vi}: {vi2}): ảnh mẫu 1 = `{Wp(so)}`; chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}` "
               "(trùng tên thì `_2`, `_3`…)."]
        print(p)
    hd += ["", "Bản được chọn chép thành `L1_duyet.png` cùng thư mục.", "",
           "Kiểm: chồng lên ảnh 1 thì từng mảnh trùng chỗ, cỡ; mặt ở giữa, vỏ chữ C, hai tinh thể cằm, hai chân dính thân (không khe trắng), "
           "năm tinh thể bay rời nhau, mỗi cái viền mực riêng; vương miện ba mũi; màu đúng bảng của hướng; nét bút mực rung, vân sáp, tô "
           "phẳng, không bóng, không vệt sáng trắng, không lấp lánh; không thêm gai, đinh, huy hiệu, miệng; nền trắng tinh.", "",
           "Câu sửa nhanh: \"remove the white highlights / shine on the crystals, flat colour only\"; \"keep every piece at the same place "
           "and size as in image 1\"; \"the legs must touch the body, no white gap\"; \"the crown must be three separate sharp spikes\"."]
    ghi(os.path.join(GUI, "HUONG_DAN.md"), hd)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "ca_con":
        ca_con()
    elif cmd == "bo_cuc":
        for h in (MAU_BO_CUC if len(sys.argv) < 3 else sys.argv[2:]):
            bo_cuc(h)
    elif cmd == "concept":
        prompt_concept()
    else:
        print(__doc__)
