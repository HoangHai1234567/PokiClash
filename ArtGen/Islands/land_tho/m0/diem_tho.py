# Tâm 10 bệ đảo Thổ (ảnh nền nen/nen_boss_1.png 1344 x 752: môi trường từng vùng theo boss, bệ theo chất liệu vùng, đường lướt
# cạnh bệ như đảo Thủy; người dùng 2026-11-19), cỡ, bên bảng tên. do_duong.py, build_land.py dùng.
# ải tướng, tâm bệ (ảnh nền), cỡ 3/4 (4: mini boss lớn, boss), bên bảng tên (1 phải, -1 trái)

HABS = [
    (1, (590, 625), 3, 1),
    (5, (320, 565), 3, 1),
    (10, (165, 355), 3, 1),
    (15, (225, 180), 3, 1),
    (20, (615, 140), 3, 1),
    (30, (1022, 195), 3, -1),
    (40, (1125, 365), 3, -1),
    (50, (1020, 545), 4, -1),
    (60, (812, 410), 4, -1),
    (70, (505, 407), 4, 1),
]
RING = {3: (85, 44), 4: (95, 48)}
# bán trục riêng từng bệ (px ảnh nền), đọc trên ảnh soi
RING_OF = {1: (85, 40), 5: (85, 42), 10: (80, 45), 15: (80, 42), 20: (85, 42), 30: (77, 37), 40: (90, 45), 50: (93, 45), 60: (88, 45), 70: (130, 62)}
PIER = (600, 705)  # đầu đường ở bến (ảnh nền)
CONTACT = {}
# bệ cuối: nối thêm vào tâm cho điểm mốc bệ 70 nằm cuối đường
GUIDE = {70: [(505, 407)]}
# điểm chạm ghim tay: viền sỏi hổ phách, bậc kim tự tháp màu kem giống màu đường
CONTACT = {1: (500, 620), 70: (598, 470)}
