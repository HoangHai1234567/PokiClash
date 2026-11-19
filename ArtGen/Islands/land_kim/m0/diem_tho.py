# Tâm 10 bệ đảo Kim (ảnh nền nen/nen_boss_1.png 1344 x 752: môi trường từng vùng theo boss, bệ theo chất liệu vùng, đường lướt
# cạnh bệ như đảo Thủy; người dùng 2026-11-19), cỡ, bên bảng tên. do_duong.py, build_land.py dùng.
# ải tướng, tâm bệ (ảnh nền), cỡ 3/4 (4: mini boss lớn, boss), bên bảng tên (1 phải, -1 trái)

HABS = [
    (1, (640, 640), 3, -1),
    (5, (1110, 560), 3, -1),
    (10, (1175, 365), 3, -1),
    (15, (1035, 155), 3, -1),
    (20, (630, 145), 3, 1),
    (30, (245, 160), 3, 1),
    (40, (210, 365), 3, 1),
    (50, (360, 520), 4, 1),
    (60, (480, 270), 4, 1),
    (70, (827, 385), 4, 1),
]
RING = {3: (85, 44), 4: (95, 48)}
# bán trục riêng từng bệ (px ảnh nền), đọc trên ảnh soi
RING_OF = {1: (90, 42), 5: (90, 45), 10: (85, 48), 15: (75, 42), 20: (72, 35), 30: (75, 40), 40: (78, 45), 50: (82, 45), 60: (85, 45), 70: (105, 48)}
PIER = (626, 705)  # đầu đường ở bến (ảnh nền)
CONTACT = {}
# bệ cuối: nối thêm vào tâm cho điểm mốc bệ 70 nằm cuối đường
GUIDE = {70: [(827, 385)]}
# điểm chạm ghim tay: viền gỗ khúc màu kem giống màu đường
CONTACT = {15: (950, 172)}
