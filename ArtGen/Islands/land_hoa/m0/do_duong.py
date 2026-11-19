# (đảo Hỏa, chép từ land_moc/m0) Dò tâm con đường trên ảnh nền (GD_Claude/18, M0): mặt nạ màu cát của đường, che lòng các bệ, rồi tìm đường rẻ nhất
# (Dijkstra, lưới nửa độ phân giải) từ bến qua điểm sát mép từng bệ theo thứ tự ải, làm mượt. Ghi duong.json (toạ độ ảnh nền).
import sys, json, heapq, math
sys.stdout.reconfigure(encoding="utf-8")
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
sys.path.insert(0, '.')
from diem_tho import HABS, CONTACT, GUIDE, RING, PIER
try:
    from diem_tho import RING_OF
except ImportError:
    RING_OF = {}
try:
    from diem_tho import VIA  # điểm phải đi qua sau khi rời bệ (đường dò dễ đi tắt)
except ImportError:
    VIA = {}
SRC = "../nen/nen_boss_1.png"
im = Image.open(SRC).convert("RGB"); W, H = im.size
a = np.asarray(im).astype(int)
road = (abs(a[..., 0] - 250) < 14) & (abs(a[..., 1] - 233) < 16) & (abs(a[..., 2] - 166) < 26)
road = ndi.binary_opening(ndi.binary_closing(road, iterations=1), iterations=1)
yy, xx = np.mgrid[0:H, 0:W]
ring = np.zeros_like(road)
for st, (cx, cy), s, side in HABS:
    rx, ry = RING_OF.get(st, RING[s])
    ring |= ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 <= 1
road &= ~ring
# lưới nửa độ phân giải
S = 2
r2 = road[::S, ::S]; h2, w2 = r2.shape
dt = ndi.distance_transform_edt(r2)
cost = np.where(r2, 1 + 3.0 / (1 + dt), 40.0)
cost[ring[::S, ::S]] = 400.0
def nearest_road(cx, cy):
    ys, xs = np.nonzero(r2)
    d = (xs * S - cx) ** 2 + (ys * S - cy) ** 2
    i = int(np.argmin(d)); return (int(xs[i]), int(ys[i]))
def dijkstra(src, dst):
    sx, sy = src; tx, ty = dst
    dist = np.full((h2, w2), np.inf); prev = np.full((h2, w2, 2), -1, np.int32)
    dist[sy, sx] = 0; pq = [(0.0, sx, sy)]
    nb = [(-1, 0, 1), (1, 0, 1), (0, -1, 1), (0, 1, 1), (-1, -1, 1.414), (1, -1, 1.414), (-1, 1, 1.414), (1, 1, 1.414)]
    while pq:
        dd, x, y = heapq.heappop(pq)
        if (x, y) == (tx, ty): break
        if dd > dist[y, x]: continue
        for ox, oy, k in nb:
            nx, ny = x + ox, y + oy
            if 0 <= nx < w2 and 0 <= ny < h2:
                nd = dd + k * (cost[ny, nx] + cost[y, x]) * 0.5
                if nd < dist[ny, nx]:
                    dist[ny, nx] = nd; prev[ny, nx] = (x, y); heapq.heappush(pq, (nd, nx, ny))
    out = [(tx, ty)]
    while out[-1] != (sx, sy):
        x, y = out[-1]; px, py = prev[y, x]
        if px < 0: raise SystemExit(f"không tới được {dst} từ {src}")
        out.append((int(px), int(py)))
    return out[::-1]
pier = (PIER[0] // S, PIER[1] // S)
# đảo Mộc: Dijkstra chỉ dò đoạn giữa hai bệ (điểm ra bệ trước → điểm chạm bệ sau); lòng bệ nối thẳng điểm chạm → tâm → điểm ra
# (né lòng bệ thì đường vòng vèo; trong game phần trong vòng đá không đặt cờ)
def straight(a, b):
    n = max(1, int(math.dist(a, b)))
    return [(int(round(a[0] + (b[0] - a[0]) * t / n)), int(round(a[1] + (b[1] - a[1]) * t / n))) for t in range(n + 1)]
def g2(p):
    return (int(p[0]) // S, int(p[1]) // S)
pts, contacts, prev = [], [], pier
for k, (st, (cx, cy), s, side) in enumerate(HABS):
    c = g2(CONTACT[st]) if st in CONTACT else nearest_road(cx, cy)
    contacts.append([int(c[0] * S), int(c[1] * S)])
    if k > 0:
        for v in VIA.get(HABS[k - 1][0], []):
            seg = dijkstra(prev, g2(v))
            pts += seg[1:]
            prev = pts[-1]
    seg = dijkstra(prev, c)
    pts += seg if not pts else seg[1:]
    inside = [c] + [g2(g) for g in GUIDE.get(st, [])]  # bệ không có GUIDE: đường đi cạnh bệ (như Thủy), không vào tâm
    for a, b in zip(inside, inside[1:]):
        pts += straight(a, b)[1:]
    prev = pts[-1]
P = np.array(pts, float) * S + S / 2
# lấy mẫu đều 4 px rồi làm mượt
L = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(P, axis=0).T))])
t = np.arange(0, L[-1], 4.0)
Q = np.stack([np.interp(t, L, P[:, 0]), np.interp(t, L, P[:, 1])], 1)
k = 7
Qs = np.copy(Q)
for j in range(len(Q)):
    lo, hi = max(0, j - k), min(len(Q), j + k + 1); Qs[j] = Q[lo:hi].mean(0)
Qs[0], Qs[-1] = Q[0], Q[-1]
json.dump({"src": SRC, "size": [W, H], "path": [[round(x, 1), round(y, 1)] for x, y in Qs[::3]], "contacts": contacts},
          open("duong.json", "w"), indent=0)
print("điểm", len(Qs[::3]), "dài", round(L[-1]), "px ảnh nền")
