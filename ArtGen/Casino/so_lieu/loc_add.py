# Gộp bản dịch tiếng Anh của đảo Casino vào Assets/Resources/Loc/en (ui.json: chữ giao diện / code; names.json: tên trong dữ liệu).
# Chỉ thêm khoá chưa có, giữ nguyên khoá cũ; giữ thứ tự sắp xếp nếu file đang sắp xếp.
import json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
# thư mục project tính từ chỗ đặt script (hai máy khác ổ)
PROJ = os.environ.get("POKI_PROJ") or os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
EN = os.path.join(PROJ, "Assets", "Resources", "Loc", "en")

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

# C6: Chợ đen (MarketScene), Quán trọ (InnDialog), chữ thưởng chung (CasinoUi.Items)
UI.update({
    "Hàng đêm": "Night stock",
    "Từ 19 giờ tối tới 5 giờ sáng, lái buôn bày thêm 2 ô hàng hiếm.": "From 7 PM to 5 AM the trader lays out 2 extra rare items.",
    "Hết lượt làm mới": "No restocks left",
    "Làm mới · {0} bi": "Restock · {0} marbles",
    "Làm mới": "Restock",
    "Tỉ lệ túi lậu": "Smuggler's Bag odds",
    "Giỏ cá: {0} con": "Fish basket: {0}",
    "Giỏ cá trống": "Fish basket is empty",
    "Bán · {0} bi": "Sell · {0} marbles",
    "Bán": "Sell",
    "Bản sao thẻ thừa: {0}": "Spare card copies: {0}",
    "Chưa có bản sao thẻ thừa (thẻ đã tối đa cấp)": "No spare card copies yet (cards at max level)",
    "làm mới hôm nay {0}/{1}": "restocks today {0}/{1}",
    "Lái buôn thu mua": "The trader buys",
    "Có cá trong giỏ hay thẻ thừa thì để ta mua lại, giá phải chăng.": "Got fish in your basket or spare cards? I'll buy them at a fair price.",
    "Hàng đêm bày rồi đấy. Thứ này ban ngày không có đâu.": "The night stock is out. You won't find these by day.",
    "Hết hàng rồi! Đợi lượt hàng sau, hoặc trả chút bi để ta lục kho.": "Sold out! Wait for the next stock, or pay a few marbles and I'll dig through the back.",
    "Hàng mới về. Mảnh tướng ở đây biết trước, không may rủi, chỉ hơi chát.": "Fresh stock. My hero shards are exactly what you see, no luck involved, just a bit pricey.",
    "Đêm xuống ta bày thêm hàng hiếm. Ghé lại sau 7 giờ tối nhé.": "When night falls I bring out the rare goods. Come back after 7 PM.",
    "Túi hàng lậu thì hên xui, tỉ lệ ta dán ngay đây, không giấu ai.": "Smuggler's Bags are luck of the draw. The odds are posted right here, nothing hidden.",
    "Mồi câu": "Bait",
    "Túi hàng lậu": "Smuggler's Bag",
    "Biết trước, không may rủi": "Exactly as shown, no luck",
    "Bản sao thẻ của tướng này": "Card copies of this hero",
    "Hàng hiếm, có hạn": "Rare, limited",
    "Nâng tiềm năng tướng": "Raises hero potential",
    "Dùng ở Bến câu": "Use at the Fishing Pier",
    "Hên xui, xem Tỉ lệ": "Luck of the draw, see Odds",
    "{0} mồi câu": "{0} bait",
    "{0} mảnh {1}": "{0} {1} shards",
    "{0} bản sao thẻ {1}": "{0} {1} card copies",
    "Cần {0} bi, bạn có {1}": "Need {0} marbles, you have {1}",
    "Mua hàng": "Buy",
    "Mua {0} với {1} bi?": "Buy {0} for {1} marbles?",
    "Được rồi, để ta lục kho xem còn gì...": "Alright, let me see what's left in the back...",
    "Giá túi: {0} bi. Mỗi túi ra một món:": "Bag price: {0} marbles. Each bag gives one item:",
    "{0} mảnh tướng": "{0} hero shards",
    "Bán thẻ thừa": "Sell spare cards",
    "Bán {0} bản sao thẻ thừa (thẻ đã tối đa cấp, không dùng được nữa) lấy {1} bi?": "Sell {0} spare card copies (cards at max level, no longer usable) for {1} marbles?",
    "Bán thẻ thừa được {0} bi": "Sold spare cards for {0} marbles",
    "Việc mới sau {0}": "New tasks in {0}",
    "Bà chủ quán: Xong hết việc rồi à? Giỏi lắm! Ngồi nghỉ, mai lại có việc mới.": "Innkeeper: All done already? Well done! Take a rest, there'll be new tasks tomorrow.",
    "Bà chủ quán: Ghé nghỉ chân đi! Hôm nay quán có mấy việc vặt, làm xong thì ghé nhận quà.": "Innkeeper: Come rest your feet! I've got a few odd jobs today. Finish them and come back for a reward.",
    "Đi làm": "Go",
    "Xong cả {0} việc hôm nay ({1}/{0})": "Finish all {0} tasks today ({1}/{0})",
    "Hôm nay chưa có lều lữ khách nào ở bến": "No traveler tents at the pier today",
    "Quà xong cả ngày: ": "Daily reward: ",
    "+{0} mảnh tướng": "+{0} hero shards",
    "+{0} bản sao thẻ": "+{0} card copies",
    # chữ nút trong prefab lưu in hoa (SketchButton.SetText)
    "ĐI LÀM": "GO",
    "LÀM MỚI": "RESTOCK",
    "TỈ LỆ TÚI LẬU": "SMUGGLER'S BAG ODDS",
    "BÁN": "SELL",
})

# C7: ba lều lữ khách (CasinoTableScene, BlackjackScene, RouletteScene, SlotScene)
UI.update({
    # phần chung
    "Lều này đã nhổ đi rồi, hẹn đoàn sau": "This tent has packed up. Catch the next caravan",
    "Hôm nay đã cược {0} bi · đã thắng {1} bi · còn {2} ván có thưởng": "Bet today {0} marbles · won {1} marbles · {2} prize rounds left",
    "Ván đầu miễn phí: không mất bi, thắng thì nhận phần lời": "First round free: nothing to lose, keep the winnings",
    "Hết ván có thưởng hôm nay: ván tập (không cược, không thưởng)": "No prize rounds left today: practice rounds (no bet, no prize)",
    "Hũ bàn {0}%": "Table jar {0}%",
    "Hũ đầy: {0}": "Full jar: {0}",
    "Lều đã đóng": "Tent closed",
    "Khách mời: {0} (mảnh ở Hũ bàn bậc cao)": "Guest hero: {0} (shards in high-tier table jars)",
    "Bậc cược: {0} bi (bậc cao mở theo cấp). Mỗi ngày {1} ván có thưởng; hết thì chơi ván tập.": "Bet tiers: {0} marbles (higher tiers unlock with level). {1} prize rounds per day; after that, practice rounds.",
    "Hũ bàn: mọi bi đã cược (thắng hay thua) đổ vào hũ; hũ đầy cho rương theo bậc cao nhất đã cược, bậc cao có mảnh tướng khách mời.": "Table jar: every marble you bet (win or lose) goes into the jar. A full jar gives a chest based on your highest bet tier; high tiers include guest hero shards.",
    "Đã hiểu": "Got it",
    "Hũ bàn đầy!": "Table jar full!",
    "Hũ bàn đầy: ": "Table jar full: ",
    "Không đủ bi. Thử bậc thấp hơn, hoặc ghé Bến câu, Trường đua kiếm thêm": "Not enough marbles. Try a lower tier, or earn more at the Fishing Pier or Race Track",
    "Cách chơi": "How to play",
    # Blackjack
    "Đêm Bài": "Card Night",
    "Rút bài cho tổng gần 21 nhất mà không quá 21. A là 1 hoặc 11, J Q K là 10.": "Draw cards to get as close to 21 as you can without going over. A counts as 1 or 11, J Q K count as 10.",
    "Dealer rút tới 17 thì dừng. Blackjack (A + lá 10 ngay hai lá đầu) trả 3:2, thắng trả 1:1, hoà trả lại cược.": "The dealer stands at 17. Blackjack (A + a 10 card as your first two) pays 3:2, a win pays 1:1, a push returns your bet.",
    "Gấp đôi: cược thêm bằng cược đầu, nhận đúng một lá. Tách: hai lá cùng điểm tách thành hai tay, mỗi tay một cược.": "Double: add a bet equal to your first and take exactly one card. Split: two cards of the same value become two hands, one bet each.",
    "Chọn mức cược rồi bấm Chia bài": "Pick a bet, then tap Deal",
    "Đêm Bài: ván bỏ dở đã tính, {0} bi": "Card Night: unfinished hand settled, {0} marbles",
    "Ván miễn phí!": "Free round!",
    "Ván tập": "Practice round",
    "Ván miễn phí": "Free round",
    "Dealer có Blackjack!": "Dealer has Blackjack!",
    "Blackjack!": "Blackjack!",
    "Hoà": "Push",
    "Thua": "Lose",
    "(ván tập)": "(practice)",
    "−{0} bi": "−{0} marbles",
    "Dealer: {0} + ?": "Dealer: {0} + ?",
    "Dealer: {0}": "Dealer: {0}",
    "Dealer: {0} (quá 21)": "Dealer: {0} (bust)",
    "Cược {0} bi": "Bet {0} marbles",
    "cược {0} bi": "bet {0} marbles",
    "miễn phí": "free",
    "ván tập": "practice",
    "{0} điểm": "{0} points",
    "(mềm)": "(soft)",
    "gấp đôi": "doubled",
    "Quá 21": "Bust",
    "Chia bài · {0} bi": "Deal · {0} marbles",
    "Rút": "Hit",
    "Dằn": "Stand",
    "Gấp đôi · {0}": "Double · {0}",
    "Gấp đôi": "Double",
    "Tách": "Split",
    "Gợi ý: bật": "Hints: on",
    "Gợi ý: tắt": "Hints: off",
    "Nên: {0}": "Suggested: {0}",
    # Roulette
    "Vòng Xoay Ngũ Hành": "Five Elements Wheel",
    "Bánh xe có 26 ô: 5 hệ, mỗi hệ số 1 tới 5, và một ô Sao Vàng. Đặt chip rồi quay, viên bi dừng ở ô nào thì cửa trúng ô đó thắng.": "The wheel has 26 pockets: 5 elements, numbers 1 to 5 for each, plus a Gold Star pocket. Place chips and spin; every bet covering the pocket where the ball stops wins.",
    "Hệ: trúng một trong 5 ô của hệ, trả {0}:1. Số: trúng một trong 5 ô cùng số, trả {1}:1. Ô đơn (chạm ô trên bánh xe): trả {2}:1. Sao Vàng: trả {3}:1, cược từ bậc {4} được thêm mảnh tướng khách mời.": "Element: any of its 5 pockets, pays {0}:1. Number: any of the 5 pockets with that number, pays {1}:1. Single pocket (tap it on the wheel): pays {2}:1. Gold Star: pays {3}:1, and from tier {4} it also gives guest hero shards.",
    "Tối đa {0} chip mỗi vòng. Mọi cửa hoàn trả {1}% (25/26).": "Up to {0} chips per spin. Every bet returns {1}% (25/26).",
    "Số {0} ×{1}": "No. {0} ×{1}",
    "Sao Vàng ×{0}": "Gold Star ×{0}",
    "Sao Vàng": "Gold Star",
    "Chạm cửa cược để đặt chip, rồi bấm Quay": "Tap a bet to place a chip, then tap Spin",
    "Vòng miễn phí!": "Free spin!",
    "Vòng tập": "Practice spin",
    "Bánh xe đang quay...": "The wheel is spinning...",
    "Trượt (vòng tập)": "Miss (practice)",
    "Trượt, không mất gì": "Miss, nothing lost",
    "Trượt · −{0} bi": "Miss · −{0} marbles",
    "Trúng {0} cửa (vòng tập)": "{0} bets hit (practice)",
    "Trúng {0} cửa · {1} bi": "{0} bets hit · {1} marbles",
    "Chip: {0}/{1} · mỗi chip {2} bi · tổng {3} bi": "Chips: {0}/{1} · {2} marbles each · total {3} marbles",
    "vòng tập": "practice",
    "Quay miễn phí": "Free spin",
    "Quay tập": "Practice spin",
    "Quay · {0} bi": "Spin · {0} marbles",
    "Bỏ chip": "Clear chips",
    "{0} chip": "{0} chips",
    # Máy quả
    "Hội Máy Quả": "Fruit Machine Fair",
    "Quay 3 cuộn. Ba biểu tượng giống nhau trên một trong 5 đường (ba hàng ngang, hai đường chéo) thì thắng; Sao thay được mọi biểu tượng trừ Rương.": "Spin 3 reels. Three matching symbols on any of 5 lines (three rows, two diagonals) win; the Star replaces any symbol except the Chest.",
    "Hai Rương ở đâu cũng được: trả gấp đôi cược. Ba Rương: được lượt quay miễn phí cùng mức cược.": "Two Chests anywhere pay out on your bet. Three Chests give free spins at the same bet.",
    "Ba huy hiệu khách mời trên một đường: thêm mảnh tướng khách mời. Không có tự quay; Quay nhanh chỉ bỏ bớt diễn.": "Three guest badges on a line: bonus guest hero shards. There is no auto-spin; Quick spin only shortens the animation.",
    "ngọc {0}": "{0} gem",
    "bi": "marble",
    "huy hiệu khách mời": "guest badge",
    "Sao": "Star",
    "Rương": "Chest",
    "Bảng trả": "Paytable",
    "Bấm Quay để thử vận": "Tap Spin to try your luck",
    "Quay nhanh: bật": "Quick spin: on",
    "Quay nhanh: tắt": "Quick spin: off",
    "Lượt miễn phí {0}/{1}": "Free spin {0}/{1}",
    "Lượt miễn phí đầu tiên!": "Your first spin is free!",
    "Đang quay...": "Spinning...",
    "{0}: 3 {1} ×{2}": "{0}: 3 {1} ×{2}",
    "Đường giữa": "Middle line",
    "Đường trên": "Top line",
    "Đường dưới": "Bottom line",
    "Chéo xuống": "Diagonal down",
    "Chéo lên": "Diagonal up",
    "2 Rương ×{0} cược": "2 Chests ×{0} bet",
    "3 Rương: +{0} lượt miễn phí!": "3 Chests: +{0} free spins!",
    "Không trúng đường nào": "No winning lines",
    "({0} lượt miễn phí)": "({0} free spins)",
    "Trúng {0} bi (quay tập, không nhận)": "Won {0} marbles (practice, not paid)",
    "Trượt (quay tập)": "Miss (practice)",
    "Trúng {0} bi": "Won {0} marbles",
    "lời {0}": "profit {0}",
    "lỗ {0}": "loss {0}",
    "khách mời": "guest",
    "Cược {0} bi chia đều 5 đường ({1} bi mỗi đường).": "A {0} marble bet is split across 5 lines ({1} marbles per line).",
    "3 {0}: ×{1} cược đường": "3 {0}: ×{1} line bet",
    "3 Sao: ×{0} cược đường": "3 Stars: ×{0} line bet",
    "2 Rương ở đâu cũng được: ×{0} tổng cược. 3 Rương: {1} lượt miễn phí": "2 Chests anywhere: ×{0} total bet. 3 Chests: {1} free spins",
    "3 huy hiệu trên một đường: +{0} mảnh khách mời (theo bậc cược)": "3 badges on a line: +{0} guest shards (by bet tier)",
    "Hoàn trả {0}% · trúng {1}% số lượt · ra lượt miễn phí {2}%": "Return {0}% · wins on {1}% of spins · free spins {2}%",
    # Chợ đen: Đồ Nhà; lịch lữ khách
    "Trang trí Nhà, vào túi đồ": "Home decoration, goes to your bag",
    "+{0} {1} (vào túi Nhà)": "+{0} {1} (to your Home bag)",
    "Lều lữ khách không mở ở khu vực của bạn.": "Traveler tents are not available in your region.",
    "Ở lều lữ khách từ trước tới nay: đã cược {0} bi · đã thắng {1} bi": "At the traveler tents so far: bet {0} marbles · won {1} marbles",
})

# Hầm đấu thành scene riêng (UndergroundScene, 2026-11-26)
UI.update({
    "Mỗi ngày một lứa đội ngầm mới. Thắng lần đầu trong ngày thưởng lớn, thua thì mất lệ phí.":
        "A fresh set of pit teams every day. Your first win of the day pays big; losing costs the entry fee.",
    "{0} tướng": "Heroes: {0}",
    "Đội của bạn": "Your team",
    "Đổi đội ngầm sau {0}": "New pit teams in {0}",
    "Luật hôm nay: {0}": "Today's rule: {0}",
    "Thắng lại trong ngày: hoàn lệ phí và quà nhỏ. Thua: mất lệ phí.": "Winning again the same day: fee refunded plus a small gift. Losing: the fee is gone.",
})

# Hầm đấu bản sàn đấu có Lão Mực (UndergroundScene, 2026-11-26 lượt 2): lời bình phẩm theo độ khó
UI.update({
    "Hừ... hên thôi! Lần sau đừng mong.": "Hmph... pure luck! Don't count on it next time.",
    "Thắng thật à?! Cả hầm ồ lên rồi kìa.": "You actually won?! The whole pit is roaring.",
    "Khè khè, lệ phí ta giữ nhé!": "Heh heh, I'll be keeping that fee!",
    "Thua rồi à? Về luyện thêm đi, khách.": "Lost already? Go train some more, friend.",
    "Xuống tới Hầm đấu rồi đấy! Chọn đối thủ đi, khách.": "Welcome down to the Pit! Pick your opponent, friend.",
    "Hôm nay hầm đông vui lắm. Vuốt xem các đội đi.": "The Pit is packed today. Swipe to look over the teams.",
    "Đội này khách thắng rồi còn gì. Đánh lại chỉ có quà nhỏ thôi.": "You already beat this team. A rematch only pays a small gift.",
    "Hừ... lại tới trêu đội thua à?": "Hmph... back to tease the losers?",
    "Nhà Vô Địch của tuần đấy. Thắng nổi thì ta phục!": "That's this week's Champion. Beat them and I'll tip my visor!",
    "Chọn đội dễ thế này à? Khè khè!": "Picking a team this easy? Heh heh!",
    "Bắt nạt tân binh vui lắm hả, khách?": "Having fun bullying the rookies, friend?",
    "Đội này thì ta nhắm mắt cũng đoán được ai thắng.": "I could call this one with my eyes shut.",
    "Kèo này cân đấy. Ta thích!": "Now that's an even match. I like it!",
    "Ngang tài ngang sức, cả hầm đang ngó kìa.": "Evenly matched. The whole pit is watching.",
    "Có chắc thắng được không vậy?": "Are you sure you can win this?",
    "Lệ phí ta không trả lại đâu nhé.": "No refunds on the entry fee, mind you.",
    "Đội này cứng đấy. Run chưa?": "This team is tough. Shaking yet?",
    "Liều thế?! Đội này mạnh gấp mấy lần đội của khách!": "That reckless?! This team is several times stronger than yours!",
    "Ô hô, gan to thật... hay là liều?": "Oho, real guts... or just reckless?",
})

# Hầm đấu lượt 3 (2026-11-26): 10 bậc, trần trận mỗi ngày
UI.update({
    "Còn {0}/{1} lượt đánh hôm nay": "{0}/{1} fights left today",
    "Còn {0} lượt đánh hôm nay": "{0} fights left today",
    "Hết lượt đánh hôm nay": "No fights left today",
    "Hôm nay khách đánh đủ rồi. Mai ghé, hầm có lứa đội mới.": "You've fought enough for today. Come back tomorrow, the Pit will have fresh teams.",
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
    "Đồng": "Bronze",
    "Bạc": "Silver",
    "Vàng": "Gold",
    "Bạch Kim": "Platinum",
    "Lục Bảo": "Emerald",
    "Kim Cương": "Diamond",
    "Cao Thủ": "Master",
    "Đại Cao Thủ": "Grandmaster",
}
THEMES = {"Xưởng Thép": "Steel Works", "Rừng Gai": "Thorn Wood", "Sóng Ngầm": "Undertow", "Lò Lửa": "Furnace", "Mỏ Đá": "Quarry", "Liên Minh": "Alliance"}
WORDS = {"tân binh": "rookies", "đấu sĩ": "fighters", "cựu binh": "veterans", "thủ lĩnh": "chiefs", "huyền thoại": "legends",
         "lính mới": "recruits", "tinh nhuệ": "elites", "đội trưởng": "captains", "cao thủ": "masters", "bá chủ": "overlords"}
for vt, et in THEMES.items():
    for vw, ew in WORDS.items():
        NAMES[f"{vt}: {vw}"] = f"{et}: {ew}"


# Trường đua bản sân vận động (2026-11-26)
UI.update({
    "Đường hôm nay": "Today's track",
    "{0} tướng vào vạch xuất phát!": "{0} heroes line up at the start!",
    "Chạy!": "Go!",
    "Xuất phát! Cả đoàn lao khỏi vạch!": "They're off! The whole pack bursts off the line!",
    "{0} đang dẫn đầu!": "{0} is in the lead!",
    "{0} vượt lên dẫn đầu!": "{0} takes the lead!",
    "Nước rút!": "Final sprint!",
    "Nước rút! Cả khán đài đứng hết dậy!": "Final sprint! The whole grandstand is on its feet!",
    "Sát nút!": "Neck and neck!",
    "{0} và {1} sát nút nhau!": "{0} and {1} are neck and neck!",
})

# Trường đua: luật đặt cược (2026-11-26)
UI.update({
    "Chạm vào một con để đặt cược. Về nhất, nhì thì thắng lớn!": "Tap a racer to bet on it. Finish first or second to win big!",
    "Bạn chọn {0}. Chọn mức cược rồi bấm Đặt cược!": "You picked {0}. Choose your stake, then tap Place bet!",
    "Trường đua: về thứ {0}/{1}, nhận {2} bi": "Racetrack: finished {0}/{1}, received {2} marbles",
    "Cúp tuần {0}/{1}": "Weekly cup {0}/{1}",
    "Chạm vào một con để đặt cược": "Tap a racer to bet on it",
    "Đặt cược · {0} bi": "Place bet · {0} marbles",
    "Đua thử (hết lượt hôm nay)": "Practice race (no bets left today)",
    "Cố lên, {0}!": "Go, {0}!",
    "{0} vấp ngã!": "{0} trips and falls!",
    "Bứt tốc!": "Burst!",
    "{0} bứt tốc vọt lên!": "{0} bursts ahead!",
    "Đua thử: không cược, không thưởng.": "Practice race: no bet, no prize.",
    "Thắng cược! Đặt {0} bi, nhận về {1} bi": "You won! Bet {0} marbles, got back {1} marbles",
    "Hoà tiền: nhận lại {0} bi": "Break even: {0} marbles returned",
    "Đặt {0} bi, nhận về {1} bi": "Bet {0} marbles, got back {1} marbles",
    "Thua cược: mất {0} bi": "You lost the bet: {0} marbles gone",
    "+{0} điểm cúp tuần": "+{0} weekly cup points",
    "Chọn một tướng để đặt cược": "Pick a racer to bet on",
    "Đặt từ {0} tới {1} bi": "Bet between {0} and {1} marbles",
    "Lượt hôm nay": "Bets today",
    "Đặt cược": "Place bet",
    "Đua tiếp": "Next race",
    "Nhất ×{0}": "1st ×{0}",
    "Nhì ×{0}": "2nd ×{0}",
    "Ba ×{0}": "3rd ×{0}",
    "Nhất: hoàn tiền": "1st: stake back",
    "Nhì: hoàn tiền": "2nd: stake back",
    "Ba: hoàn tiền": "3rd: stake back",
})

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
    bal = json.load(open(os.path.join(PROJ, "Assets", "02 Data", "Json", "balance.json"), encoding="utf-8-sig"))
    for day in bal["casino"]["underground"]["rotation"]:
        for e in day["entries"]:
            if e["name"].startswith("Nhà Vô Địch: "):
                hn = e["name"][len("Nhà Vô Địch: "):]
                NAMES[e["name"]] = "Champion: " + names.get(hn, hn)
    merge("ui.json", UI)
    merge("names.json", NAMES)
