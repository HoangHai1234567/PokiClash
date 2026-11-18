# Gọt thoi cỏ nền có viền dưới chân hình (cây, công trình) cho hình hoà vào đất bên dưới (người dùng dặn 2026-11-18).
# Dùng chung cho trees/pack_trees.py và import_home.py. Hàm chính: strip_foot(img, bottom) trên ảnh RGBA đã tách nền trắng,
# giữ nguyên khung ảnh để điểm neo không đổi.


def is_fill(p):
    # nền thoi cỏ: xanh vàng nhạt (khoảng 190, 238, 96); bụi, tán cây xanh đậm hơn (R < 165)
    r, g, b_ = p[:3]
    return r >= 165 and g >= 215 and b_ <= 150 and g - b_ >= 80 and g - r >= 25  # g > r: không lẫn tường kem, gỗ sáng


def is_dark(p):
    return max(p[:3]) < 110


def is_body(p):
    # màu thân vật ở chân: lá xanh (bụi, dương xỉ), gỗ nâu (gốc, khúc gỗ), đá xám
    r, g, b_ = p[:3]
    green = g >= 140 and r < 165 and g - r >= 25
    wood = r >= 120 and r - g >= 15 and b_ < 130
    stone = abs(r - g) < 15 and abs(r - b_) < 15 and 140 < r < 225  # xám trung tính; nét nâu pha nền trắng ngả nâu nên không tính
    return green or wood or stone


def components(px, w, h, y0, pts):
    """Các khối liền (8 hướng) của điểm còn màu trong tập pts."""
    seen, out = set(), []
    for start in pts:
        if start in seen or px[start][3] == 0:
            continue
        comp, st = [], [start]
        seen.add(start)
        while st:
            c = st.pop()
            comp.append(c)
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)):
                q = (c[0] + dx, c[1] + dy)
                if 0 <= q[0] < w and y0 <= q[1] < h and q not in seen and px[q][3] > 0:
                    seen.add(q)
                    st.append(q)
        out.append(comp)
    return out


def measure_diamond(img, bottom):
    """Đo thoi cỏ dưới chân: từ mũi dưới đi lên, bề ngang thoi tăng đều (khoảng 3,5 tới 4 px mỗi hàng) cho tới mũi trái, phải rồi
    thôi tăng. Hàng mũi là chỗ bề ngang lớn nhất ngay trước khi thôi tăng. Trả (giữa x, hàng mũi, bề ngang)."""
    a = img.split()[3].load()
    w, _ = img.size
    def width(y):
        xs = [x for x in range(w) if a[x, y] > 0]
        return (min(xs), max(xs)) if xs else (0, -1)
    rows = [width(bottom - v) for v in range(0, min(bottom, 200))]
    W = [r - l for l, r in rows]
    v = 6
    while v + 4 < len(W) and W[v + 4] - W[v] >= 4:
        v += 1
    v = max(range(max(0, v - 2), min(len(W), v + 5)), key=lambda k: W[k])
    l, r = rows[v]
    return (l + r) / 2, bottom - v, r - l


def strip_foot(img, bx, bottom, foot, inner=0.0):
    """Bỏ nền thoi cỏ có viền dưới chân (người dùng dặn 2026-11-18: cây phải hoà vào đất bên dưới). Giữ khung ảnh để điểm neo không đổi.
    1. xoá màu nền thoi và quầng nhạt trong thoi;
    2. khối rời trong thoi: túm cỏ (ngả xanh) giữ, nét viền đứt (nâu sẫm) xoá;
    3. nét viền dính vào vật (bụi, đá phủ lên mép thoi): ở dải mép, điểm không phải màu thân vật và quanh 3 px không có màu thân vật thì xoá."""
    w, h = img.size
    px = img.load()
    bx, cy, foot = measure_diamond(img, bottom)
    hw, hh = foot / 2 + 3, (bottom - cy) + 3  # thoi vẽ tay hơi cao hơn 2:1 (0,54 tới 0,59)
    dia = lambda x, y: abs(x - bx) / hw + abs(y - cy) / hh  # 1 = mép ngoài thoi; viền vẽ tay dày, lệch tới khoảng 1,15
    y0 = max(0, int(cy - hh * 1.3))
    pts = [(x, y) for y in range(y0, h) for x in range(w) if px[x, y][3] > 0 and dia(x, y) <= 1.22]
    # nền thoi có nét chì xanh đậm hơn, trùng màu rêu, lá dương xỉ: không lọc theo màu mà loang từ nền ở nửa trước của thoi qua các
    # điểm xanh vàng liền nhau (lá, rêu có viền sẫm riêng nên loang không lọt vào); quầng nhạt sát nền cũng xoá
    # màu nền thoi: nền sáng (R >= 172) và nét chì xanh của nền (B <= 72); bụi (R 128-160, B 80-112) không lọt
    lime = lambda p: p[1] - p[0] >= 25 and ((p[0] >= 172 and p[1] >= 220 and p[1] - p[2] >= 80) or (p[2] <= 72 and p[1] >= 190 and p[0] >= 128))
    ptset = set(pts)
    seeds = [q for q in pts if q[1] > cy and is_fill(px[q])]  # nửa trước thoi: nền lộ ra trước vật; nửa sau loang tới qua quanh gốc
    seen = set(seeds)
    st = list(seeds)
    while st:
        c = st.pop()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            q = (c[0] + dx, c[1] + dy)
            if q in ptset and q not in seen and dia(*q) >= inner and lime(px[q]):
                seen.add(q)
                st.append(q)
    for q in seen:
        px[q] = (0, 0, 0, 0)
    pts = [q for q in pts if px[q][3] > 0]
    # màu thân vật thật (vùng dày, không phải dải pha màu một hai px dọc nét viền)
    body0 = {q for q in pts if px[q][3] > 0 and not is_dark(px[q]) and not is_fill(px[q])}  # mọi màu không sẫm (tường, mái, gỗ, lá, đá)
    body = {(x, y) for (x, y) in body0 if sum((x + dx, y + dy) in body0 for dx in range(-2, 3) for dy in range(-2, 3)) >= 12}
    # nét viền thoi: ở dải mép, điểm không thuộc thân vật và quanh 3 px không có thân vật thì xoá (viền của vật luôn sát thân vật)
    for (x, y) in pts:
        if px[x, y][3] == 0 or dia(x, y) < 0.8 or (x, y) in body:
            continue
        if not any((x + dx, y + dy) in body for dx in range(-3, 4) for dy in range(-3, 4)):
            px[x, y] = (0, 0, 0, 0)
    # khối rời còn lại trong thoi (khúc viền, vụn): giữ túm cỏ ngả xanh đủ lớn, còn lại xoá
    is_obj = lambda comp: any(y == y0 or dia(x, y) > 1.3 for x, y in comp)
    for comp in components(px, w, h, y0, [q for q in pts if px[q][3] > 0]):
        if is_obj(comp):
            continue
        n = len(comp)
        mr = sum(px[q][0] for q in comp) / n
        mg = sum(px[q][1] for q in comp) / n
        if mg - mr < 25 or n < 14:
            for q in comp:
                px[q] = (0, 0, 0, 0)
    return img
