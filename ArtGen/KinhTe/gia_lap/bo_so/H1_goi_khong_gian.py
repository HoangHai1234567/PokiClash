# Vòng 1 (2026-11-26, sau khi game đã sửa): gói tướng trọn bộ "đi trước xa" KHÔNG giãn sức tướng (sức vẫn theo độ hiếm như game):
# mốc 6 (6 sao, thẻ cấp 3, 20 đá) ngày 2; mốc 10 (11 sao, thẻ cấp 4, 120 đá) ngày 7. Chạy --nhom 0,1 --ngay 90.
GRANTS = [{"day": 2, "moc": 6, "star": 6, "card": 3, "evo": 20}, {"day": 7, "moc": 10, "star": 11, "card": 4, "evo": 120}]


def patch(b):
    b["sim"] = {"grants": GRANTS}
