# Tâm 10 bệ đảo Mộc (ảnh nền nen/nen_boss_1.png 1344 x 752: môi trường từng vùng theo boss, bệ theo chất liệu vùng, đường lướt
# cạnh bệ như đảo Thủy; người dùng 2026-11-19), cỡ, bên bảng tên. do_duong.py, build_land.py dùng.
# ải tướng, tâm bệ (ảnh nền), cỡ 3/4 (4: mini boss lớn, boss), bên bảng tên (1 phải, -1 trái)

HABS = [
    (1, (640, 595), 3, 1),
    (5, (1010, 560), 3, -1),
    (10, (1180, 350), 3, -1),
    (15, (1000, 150), 3, -1),
    (20, (680, 150), 3, 1),
    (30, (345, 165), 3, 1),
    (40, (147, 340), 3, 1),
    (50, (330, 540), 4, 1),
    (60, (415, 360), 4, 1),
    (70, (765, 420), 4, -1),
]
RING = {3: (85, 44), 4: (95, 48)}
# bán trục riêng từng bệ (px ảnh nền), đọc trên ảnh soi
RING_OF = {1: (100, 50), 5: (100, 50), 10: (95, 48), 15: (95, 45), 20: (70, 40), 30: (85, 45), 40: (100, 47), 50: (93, 48), 60: (95, 48), 70: (90, 32)}
PIER = (635, 700)  # đầu đường ở bến (ảnh nền)
CONTACT = {}
# bệ cuối: nối thêm vào tâm cho điểm mốc bệ 70 nằm cuối đường
GUIDE = {70: [(765, 420)]}
# điểm chạm ghim tay: viền vuốt / gốc cây màu kem giống màu đường
CONTACT = {40: (262, 335)}
