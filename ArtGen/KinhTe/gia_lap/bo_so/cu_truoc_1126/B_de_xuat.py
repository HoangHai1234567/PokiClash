# Bộ số B: đề xuất cân bằng lần 1 (GD_Claude/33_CanBangKinhTe.md). Phần "sim" là các đổi cần sửa code game, runner giả lập trước.
def patch(b):
    c = b["casino"]
    # 1. Chợ đen: bỏ đổi thẻ thừa ra bi (vòng lặp vô hạn). Đề xuất đổi ra đá tiềm năng có trần ngày (code).
    c["market"]["copySell"] = 0
    # 2. Hầm đấu: thắng hoàn đúng lệ phí (trước trả 2,5 lần): thưởng là mảnh và đá, không phải bi; mảnh mỗi bậc giảm khoảng nửa; đá tiến hóa chỉ từ bậc Cao Thủ
    u = c["underground"]
    u["winMult"] = 1.0
    shards = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 5]
    for i, t in enumerate(u["tiers"]):
        t["shards"] = shards[i]
    u["tiers"][5]["items"] = [{"k": "stones", "n": 4}]
    u["tiers"][6]["items"] = [{"k": "stones", "n": 5}]
    # 3. Câu cá: giá cá còn khoảng một phần năm, thưởng loài mới còn một phần ba
    f = c["fishing"]
    f["price"] = [1, 1, 2, 6, 15]
    f["first"] = [3, 5, 8, 15, 30]
    f["king"] = [{"k": "shards", "n": 5, "h": "*elem"}, {"k": "evo", "n": 1}, {"k": "balls", "n": 50}]
    # 4. Quán trọ: bi mỗi việc còn một phần năm
    for q in c["inn"]["quests"]:
        for it in q["items"]:
            if it["k"] == "balls":
                it["n"] = 6 if it["n"] <= 30 else 8
    c["inn"]["all"] = [{"k": "bait", "n": 3}, {"k": "balls", "n": 10}]
    # 5. Đua: cược nhỏ không còn lời (hoàn trả 0,98 thay 1,18); Lễ Hội Đua ×1,25 phần lời (trước ×1,5)
    c["race"]["oddsLow"] = [0.135, 0.17, 0.235]
    for e in c["events"]:
        if e.get("booth") == "race_fest":
            e["mult"] = 1.25
    for cup in c["race"]["cups"]:
        for it in cup["week"]:
            if it["k"] == "balls":
                it["n"] = it["n"] // 3
    # 6. Rương máy bi: trứng hiếm lại (bạc 4,6% -> 1%, vàng 8,8% -> 2,5%), phần trọng số bỏ ra chuyển sang dòng EXP
    ch = b["pachinko"]["chests"]
    for name, w in (("chest_silver", 1.0), ("chest_gold", 2.5)):
        egg = next(r for r in ch[name] if r["k"] == "egg")
        exp = next(r for r in ch[name] if r["k"] == "exp")
        exp["w"] = round(exp["w"] + egg["w"] - w, 2)
        egg["w"] = w
    # 7. Luật cần sửa code (runner giả lập)
    b["sim"] = {
        "replayFull": 10, "replayPct": 0.25,  # đánh lại ải: 10 trận đầu mỗi ngày đủ bi, sau đó 25%
        "noAdsInstant": 8,                    # Bỏ quảng cáo: 8 lượt trao ngay mỗi ngày, còn lại vẫn xem
        "piggyGapDays": 3,                    # Lọ Bi: cách nhau ít nhất 3 ngày
        "reliefFix": True,                    # Gói Tiếp Sức bật đúng lúc kẹt
    }
