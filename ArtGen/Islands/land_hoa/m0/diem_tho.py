# Tâm 10 bệ đảo Hỏa (ảnh nền nen/nen_boss_1.png 1344 x 752: môi trường từng vùng theo boss, bệ theo chất liệu vùng, đường lướt
# cạnh bệ như đảo Thủy; người dùng 2026-11-19), cỡ, bên bảng tên. do_duong.py, build_land.py dùng.
# ải tướng, tâm bệ (ảnh nền), cỡ 3/4 (4: mini boss lớn, boss), bên bảng tên (1 phải, -1 trái)

HABS = [
    (1, (622, 618), 3, -1),
    (5, (338, 577), 3, 1),
    (10, (180, 355), 3, 1),
    (15, (292, 158), 3, 1),
    (20, (630, 140), 3, 1),
    (30, (950, 127), 3, -1),
    (40, (1132, 352), 3, -1),
    (50, (975, 575), 4, -1),
    (60, (850, 400), 4, -1),
    (70, (580, 250), 4, 1),
]
RING = {3: (85, 44), 4: (95, 48)}
# bán trục riêng từng bệ (px ảnh nền), đọc trên ảnh soi
RING_OF = {1: (95, 45), 5: (88, 43), 10: (80, 48), 15: (85, 42), 20: (88, 38), 30: (85, 45), 40: (82, 42), 50: (90, 45), 60: (85, 45), 70: (127, 53)}
PIER = (635, 700)  # đầu đường ở bến (ảnh nền)
CONTACT = {}
# bệ cuối: nối thêm vào tâm cho điểm mốc bệ 70 nằm cuối đường
GUIDE = {70: [(580, 250)]}
# điểm chạm ghim tay: viền sen, viền mây lửa màu kem giống màu đường
CONTACT = {30: (950, 162), 60: (850, 455)}
