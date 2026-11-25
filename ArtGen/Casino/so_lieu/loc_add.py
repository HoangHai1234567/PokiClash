# Gộp bản dịch tiếng Anh của đảo Casino vào Assets/Resources/Loc/en (ui.json: chữ giao diện / code; names.json: tên trong dữ liệu).
# Chỉ thêm khoá chưa có, giữ nguyên khoá cũ; giữ thứ tự sắp xếp nếu file đang sắp xếp.
import json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
EN = os.path.join(r"C:\Atomik\PokiWar", "Assets", "Resources", "Loc", "en")

UI = {
    "Cần {0} tướng để mở": "Need {0} heroes to unlock",
    "Lều Đêm Bài chưa mở": "The Card Night tent isn't open",
    "Hết ván hôm nay": "No hands left today",
    "Không đủ bi": "Not enough marbles",
    "Hàng đã đổi": "The stock has changed",
    "Nâng cần câu để câu chỗ này": "Upgrade your rod to fish here",
    "Hết mồi": "Out of bait",
    "Chưa có tướng này": "You don't have this hero yet",
    "Lều Vòng Xoay chưa mở": "The Wheel tent isn't open",
    "Đặt ít nhất một chip": "Place at least one chip",
    "Tối đa {0} chip mỗi vòng": "Up to {0} chips per spin",
    "Hết vòng hôm nay": "No spins left today",
    "Lều Máy Quả chưa mở": "The Fruit Machine tent isn't open",
    "Luật thường": "Standard rules",
    "mọi tướng": "all heroes",
    "tướng hệ {0}": "{0} heroes",
    "Công +{0}% cho {1}": "Attack +{0}% for {1}",
    "Máu +{0}% cho {1}": "HP +{0}% for {1}",
    "Thủ +{0}% cho {1}": "Defense +{0}% for {1}",
    "Mỗi lượt chỉ chọn {0} thẻ": "Only {0} card picks per turn",
    "Mỗi bên chỉ một tướng": "One hero per side",
    "Đội ngầm mạnh thêm {0}%": "Pit team is {0}% stronger",
    "Hôm nay không có trận này": "This match isn't on today",
    "Tuần này đã thắng Nhà Vô Địch": "You already beat the Champion this week",
    "Mở ở cấp {0}": "Unlocks at level {0}",
    "Hết lượt hôm nay": "No plays left today",
    "Đã mua": "Bought",
    "Câu {0} con cá": "Catch {0} fish",
    "Câu {0} con cá Hiếm trở lên": "Catch {0} Rare or better fish",
    "Thả {0} bi ở Tháp Máy Bi": "Drop {0} marbles at the Marble Tower",
    "Đua {0} lần": "Race {0} times",
    "Về top 3 {0} lần ở Trường đua": "Finish top 3 at the Racetrack {0} times",
    "Chơi {0} ván ở lều lữ khách": "Play {0} rounds at the traveler tents",
    "Mua {0} món ở Chợ đen": "Buy {0} items at the Black Market",
    "Thắng {0} trận ở Hầm đấu": "Win {0} fights in the Pit",
}

UI.update({
    "Bến Lữ Khách": "Traveler's Rest",
    "Bến câu": "Fishing Pier",
    "Trường đua": "Racetrack",
    "Chợ đen": "Black Market",
    "Hầm đấu": "The Pit",
    "Quán trọ": "Inn",
    "Lều lữ khách": "Traveler Tents",
    "Giữa năm đảo hệ có một bến nghỉ chân. Thám hiểm gia nào đi qua cũng ghé lại: sửa thuyền, đổi đồ, kể chuyện và thử vận ở Tháp Máy Bi giữa đảo.":
        "Between the five element islands lies a resting harbor. Every explorer passing by stops here to mend their boat, trade, swap stories and try their luck at the Marble Tower in the middle of the island.",
    "Quanh tháp có bến câu, trường đua, chợ đen, hầm đấu và quán trọ, mở dần theo cấp. Thỉnh thoảng có đoàn lữ khách ghé bến dựng lều chơi vài ngày rồi đi.":
        "Around the tower are a fishing pier, a racetrack, a black market, a fighting pit and an inn, opening as you level up. Now and then a traveling caravan docks, pitches its tents for a few days, then moves on.",
    "Vào bến": "Come ashore",
    "Mới mở: {0}": "Now open: {0}",
    "Tháp Máy Bi": "Marble Tower",
    "{0} mồi": "{0} bait",
    "Lễ Hội Đua ×{0}": "Race Festival ×{0}",
    "{0} lượt có thưởng": "{0} rewarded runs",
    "Đổi hàng sau {0}": "New stock in {0}",
    "Đã thắng {0}/{1} trận hôm nay": "Won {0}/{1} fights today",
    "Nhiệm vụ {0}/{1}": "Tasks {0}/{1}",
    "Lịch lữ khách": "Caravan Schedule",
    "Chưa có đoàn nào": "No caravan yet",
    "Bãi lều": "Tent Ground",
    "{0} ghé sau {1} ngày": "{0} arrives in {1} days",
    "Bãi lều trống": "Empty Tent Ground",
    "Hệ may mắn hôm nay: {0}. Cá hệ này cắn câu nhiều gấp đôi, tướng hệ này chạy nhanh hơn.":
        "Today's lucky element: {0}. Fish of this element bite twice as often and heroes of this element run faster.",
    "Lật Bói sao để biết hệ may mắn hôm nay.": "Flip the Star Reading to learn today's lucky element.",
    "Bói sao": "Star Reading",
    "Về sảnh": "To Lobby",
    "Trò này đang được dựng": "This game is still being built",
    "Hệ may mắn hôm nay: {0}": "Today's lucky element: {0}",
    "Hôm nay chưa có đoàn lữ khách nào ở bến.": "No caravan is docked today.",
    "{0}: còn {1}": "{0}: {1} left",
    "khách mời {0}": "guest {0}",
    "Sắp ghé:": "Coming soon:",
    "{0}: sau {1} ngày": "{0}: in {1} days",
    "Đóng": "Close",
    "Nhận thưởng": "Claim",
    "Đã nhận thưởng nhiệm vụ": "Task rewards claimed",
    "Ra đảo": "To Island",
    # Trường đua bản 3–5 tướng, đánh nhau, choáng
    "Chọn tướng rồi bấm Đua. Trên đường các tướng sẽ húc nhau, ai về nhất thì hên!": "Pick a hero and tap Race. Heroes bump each other on the way, so whoever wins got lucky!",
    "Trường đua: về thứ {0}/{1}, +{2} bi": "Racetrack: finished {0}/{1}, +{2} marbles",
    "{0} tướng vào vạch xuất phát. Chạy!": "{0} heroes at the starting line. Go!",
    "Tuyệt! Tăng tốc, né được một cú húc": "Perfect! Speed up and dodge one bump",
    "Tốt! Tăng tốc": "Good! Speed up",
    "Choáng!": "Stunned!",
    "{0} húc {1} choáng váng!": "{0} bumps {1}, who's seeing stars!",
    "Vấp!": "Tripped!",
    "{0} lao vào {1} nhưng hụt, vấp ngã!": "{0} lunges at {1}, misses and trips!",
    "{0} né gọn cú húc của {1}!": "{0} dodges {1}'s bump!",
    "Gió thuận!": "Tailwind!",
    "{0} gặp gió thuận, phóng vụt lên!": "{0} catches a tailwind and shoots ahead!",
    "{0} về nhất!": "{0} wins!",
    "Về thứ {0}/{1}": "Finished {0}/{1}",
    "{0}. {1} · húc trúng {2} · bị choáng {3}": "{0}. {1} · bumps {2} · stunned {3}",
})

NAMES = {
    "Đêm Bài": "Card Night",
    "Vòng Xoay Ngũ Hành": "Five Elements Wheel",
    "Hội Máy Quả": "Fruit Machine Fair",
    "Lễ Hội Đua": "Race Festival",
    "Cúp Đồng": "Bronze Cup",
    "Cúp Bạc": "Silver Cup",
    "Cúp Vàng": "Gold Cup",
    "Cúp Kim Cương": "Diamond Cup",
    "Cúp Huyền Thoại": "Legend Cup",
    "Cá Thiếc": "Tin Fish",
    "Cá Bơn Sắt": "Iron Flounder",
    "Cá Hộp Đồng": "Copper Boxfish",
    "Cá Ngựa Bánh Răng": "Gear Seahorse",
    "Cá Mập Thép": "Steel Shark",
    "Cá Rồng Vàng": "Golden Dragonfish",
    "Cá Lá Tre": "Bamboo Leaf Fish",
    "Cá Rêu": "Moss Fish",
    "Cá Trê Rễ Cây": "Rootwhisker Catfish",
    "Cá Hoa Sen": "Lotus Fish",
    "Cá Tầm Cổ Thụ": "Elder Oak Sturgeon",
    "Cá Linh Chi": "Lingzhi Fish",
    "Cá Mòi Bạc": "Silver Sardine",
    "Cá Bống Sông": "River Goby",
    "Cá Chép Lam": "Azure Carp",
    "Cá Nóc Bong Bóng": "Bubble Puffer",
    "Cá Đuối Sóng": "Wave Ray",
    "Cá Voi Ngọc": "Jade Whale",
    "Cá Rô Lửa": "Fire Perch",
    "Cá Kìm Than": "Charcoal Halfbeak",
    "Cá Mú Dung Nham": "Lava Grouper",
    "Cá Thổi Lửa": "Fire-Breathing Fish",
    "Cá Kiếm Hỏa": "Blaze Swordfish",
    "Phượng Ngư": "Phoenix Fish",
    "Cá Sỏi": "Pebble Fish",
    "Cá Lóc Bùn": "Mud Snakehead",
    "Cá Đá Hoa Cương": "Granite Fish",
    "Cá Hóa Thạch": "Fossil Fish",
    "Cá Ngạnh Núi": "Mountain Barbel",
    "Cá Kỳ Lân Đất": "Earth Unicorn Fish",
    "Thủy Quái Râu Dài": "Longwhisker Leviathan",
    "Hỏa Ngư Vương": "Flame Fish King",
    "Kim Giáp Ngư Vương": "Iron-Scale Fish King",
    "Mộc Lão Ngư": "Ancient Wood Fish",
    "Thạch Ngư Vương": "Stone Fish King",
    "Gần bờ": "Shallows",
    "Xa bờ": "Open Water",
    "Rạn đá": "Rocky Reef",
    "Đá": "Stone",
    "Huyền Thoại": "Legend",
    "Nhà Vô Địch": "Champion",
}
THEMES = {"Xưởng Thép": "Steel Works", "Rừng Gai": "Thorn Wood", "Sóng Ngầm": "Undertow", "Lò Lửa": "Furnace", "Mỏ Đá": "Quarry", "Liên Minh": "Alliance"}
WORDS = {"tân binh": "rookies", "đấu sĩ": "fighters", "cựu binh": "veterans", "thủ lĩnh": "chiefs", "huyền thoại": "legends"}
for vt, et in THEMES.items():
    for vw, ew in WORDS.items():
        NAMES[f"{vt}: {vw}"] = f"{et}: {ew}"


def merge(fname, add):
    p = os.path.join(EN, fname)
    raw = open(p, "rb").read()
    bom = raw.startswith(b"\xef\xbb\xbf")
    t = raw.decode("utf-8-sig")
    crlf = "\r\n" in t
    d = json.loads(t)
    was_sorted = list(d.keys()) == sorted(d.keys())
    n = 0
    for k, v in add.items():
        if k not in d:
            d[k] = v
            n += 1
    if was_sorted:
        d = dict(sorted(d.items()))
    out = json.dumps(d, ensure_ascii=False, indent=1) + "\n"
    if crlf:
        out = out.replace("\n", "\r\n")
    with open(p, "w", encoding="utf-8-sig" if bom else "utf-8", newline="") as f:
        f.write(out)
    print(fname, "+", n, "khoa", "(sap xep)" if was_sorted else "")


if __name__ == "__main__":
    # tên Nhà Vô Địch ghép tên tướng: dịch theo names.json hiện có
    names = json.load(open(os.path.join(EN, "names.json"), encoding="utf-8-sig"))
    bal = json.load(open(os.path.join(r"C:\Atomik\PokiWar", "Assets", "02 Data", "Json", "balance.json"), encoding="utf-8-sig"))
    for day in bal["casino"]["underground"]["rotation"]:
        for e in day["entries"]:
            if e["name"].startswith("Nhà Vô Địch: "):
                hn = e["name"][len("Nhà Vô Địch: "):]
                NAMES[e["name"]] = "Champion: " + names.get(hn, hn)
    merge("ui.json", UI)
    merge("names.json", NAMES)
