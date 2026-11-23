# 26. Cửa hàng, gói bán, ưu đãi chớp nhoáng, popup gạ mua, quảng cáo thưởng (kế hoạch 2026-11-23)

Người dùng dặn 2026-11-23: "quét kĩ shop của Clash of Critters, các gói của họ (chủ yếu gói tặng bóng và mở hộp nhận mảnh tướng), quét kĩ kịch
bản hiện pop up gợi ý người chơi mua các gói và lên plan làm shop, các gói bán, các gói flash sale, kịch bản hiện pop up gạ người chơi mua (đào
thật sâu vào, có thể gợi ý khi người chơi vừa thua, thi thoảng có gói sale trong 2-3 tiếng...), bổ sung thêm cả reward ad nữa, game này sẽ kết
hợp iap và reward ads".

**Đổi chốt cũ.** `07_MayBi.md` (2026-10-30) và `12_KeHoach_OpenSpec.md` ghi "không bán bi, đá tiềm năng, lượt quay máy bi". Kế hoạch này
bán bi và rương mảnh tướng theo lời dặn mới. Hai chỗ cũ sẽ sửa khi người dùng duyệt bản này (câu 1, mục 11).

## Tóm tắt

- **Critters bán gì** (mục 1): cửa hàng chính dạng danh sách gói có tab; popup "quà bốc đồng" tự bật kèm đồng hồ; gói bổ sung bi khi hết; ưu đãi
  bất ngờ một món 10 giờ; gói lần đầu nạp nhận dần 3 ngày; gói khởi hành; heo đất; gói chuỗi xen ô miễn phí; gói tự chọn tướng; hộp "dò" tướng
  có công bố tỉ lệ; thẻ tuần, thẻ tháng, gói 7 ngày, quỹ trưởng thành, pass. Nhãn ghi "siêu giá trị 200–540%", không gạch giá. **Họ không có
  quảng cáo thưởng.**
- **Công khai** (mục 2): Critters thu khoảng 250 nghìn USD/ngày, 100% IAP, 90% người chơi từ quảng cáo trả tiền. Người chơi chê nặng nhất là popup
  (mỗi lần mở game, mỗi lần bấm thả bi, cứ 2–15 phút) và xin được xem quảng cáo đổi bi.
- **Mình làm** (mục 3–9): cửa hàng 4 tab; khoảng 15 loại gói; bộ máy ưu đãi (Offer Engine) chọn popup theo sự kiện, phân nhóm người chơi, thang giá
  lên xuống, trần tần suất, ô "Hôm nay không hiện nữa"; ưu đãi chớp nhoáng 2–3 giờ và ưu đãi nóng 10 phút sau trận thắng lớn; gói sau khi thua chỉ
  hiện khi đã gợi ý cách miễn phí; quảng cáo thưởng 12 chỗ đặt có trần mỗi ngày và bảng mốc xem quảng cáo. Giai đoạn đầu không thêm tiền cứng: bán
  thẳng bằng tiền thật, vật phẩm là bi, Rương Tướng, vé chọn tướng.
- **Mốc** (mục 10): S0 dữ liệu và lõi, S1 cửa hàng, S2 popup, S3 gói định kỳ, S4 quảng cáo và SDK, S5 cấu hình từ xa và đo, S6 pass.
- 11 câu cần chốt ở mục 11, câu nào cũng có đề xuất.

## 1. Clash of Critters: mổ được gì

Nguồn: bản xuất AssetRipper `D:\Ripper\ClashOfCritters\AssetRipper_Export\...` (prefab, ảnh, anim đọc được) và chuỗi trong APK. Lua và bảng
số mã hoá, có NetEase HTProtect, không giải mã (memory `coc-config-extraction`). Vì vậy **tên gói thật, giá thật, điều kiện bật popup, tỉ lệ
gacha không lấy được**; chữ trong prefab là chữ giữ chỗ tiếng Trung của dev. Tờ ảnh tổng hợp và cây prefab gọn ở
`D:\Ripper\ClashOfCritters\Analysis\shop\` (`to_anh\01..06_*.png`, `cay_prefab_gon\`). Chỉ để học, không đăng, không gửi Magnific.

### 1.1. SDK

- Thanh toán: Google Play Billing 8.3, Lilith SDK (thu ngân web `H5MallActivity`, nút "chuyển sang thu ngân, hoàn 5%").
- Không SDK quảng cáo nào (AppLovin, IronSource, AdMob, Unity Ads, Mintegral, Pangle…). Chỉ lấy mã quảng cáo để đo nguồn cài (AppsFlyer,
  Facebook, Firebase).
- Mọi thứ "miễn phí" của họ không qua quảng cáo: ô quà free trong shop, ô đầu gói chuỗi, ngày free của gói người mới, lượt quay free.

### 1.2. Cửa hàng chính (`Shop/pbui_shop_view`)

- Cột tab trái, cột gói phải (danh sách cuộn). Tab theo icon: tuyển chọn ("精选礼包"), hằng ngày, siêu giá trị, nạp, hoàn tiền nạp.
- Ô tiêu đề mục có đồng hồ ("12天21小时") và nhãn HOT. Ô gói: tên, hàng vật phẩm, nhãn giá trị, "送" (tặng thêm), nút giá, "限购2/2" (giới hạn
  lượt mua), "已售罄" (hết hàng).
- Lưới bậc mua (bi hoặc đá) có nhãn **"首次购买 送100"**: lần đầu mua tặng thêm.
- Ô thẻ tháng và ô hằng ngày nằm cạnh nhau, có "còn lại" và dấu hết hàng.
- Ô quà miễn phí trong shop (bấm "领取" là nhận).
- Tiền đá chia **đá trả tiền / đá miễn phí** ("付费火红晶矿 / 免费火红晶矿") và có dòng "关于特定交易法": làm theo luật Nhật về tiền trong game.
- Nút shop ở màn chính đổi icon xoay vòng giữa các gói đang có, có chấm đỏ số và hạt sáng khi còn gói lần đầu.

### 1.3. Gói bi

- **"弹珠补充!" (bổ sung bi)**, `ImpulseGift/popup/pbui_shop_package_popup03`: banner rổ bi và hamster; **3 ô bậc** (đống nhỏ, rổ, đống lớn), mỗi ô có
  số bi, nút giá, nhãn **"额外赠送 / 送 600"** (tặng thêm). Đoán: bật khi hết bi. Có bản y hệt cho thuốc tiêu hoá ("消食丸补充!").
- **"惊喜特惠" (ưu đãi bất ngờ)**, `popup02`: nền vàng nổ, **một món lớn**, đồng hồ "10:00:00", nhãn "超值 400%", ví dụ giữ chỗ "30元 → 2000 bi".
- Bậc bi trong lưới shop, lần đầu tặng thêm.
- Thẻ tuần cộng **"弹珠树总存储上线+1500"** (sức chứa cây bi +1.500); pass cộng +500 mỗi cây.
- Buff "超级加倍" (bi ra kẹo ×2, 10 ngày), không rõ có bán không.

### 1.4. Hộp, rương ra tướng

- **Máy "dò" tướng** (`Pet/Collection/pbui_pet_detect_view`): mở theo nhóm, "再开一组" (mở nhóm nữa), có hiệu ứng nạp thường và nạp nâng cao.
- Vật phẩm: hộp "?" 3 cỡ (một hộp, vài hộp, cả đống), trứng con nhộng mặt mèo xanh / lam / tím (theo độ hiếm), **trứng tăng tỉ lệ**, rương theo
  độ hiếm (đồng, lam, tím, đỏ, cầu vồng), hộp hệ hỏa.
- **Bảng công bố tỉ lệ** ("卡片概率": thẻ trắng, thẻ vàng 50%).
- **Chọn tướng** (`Shop/pet/pbui_shop_petchoose_pop`): "chọn 3 trong 6 tướng", mỗi ô hiện % tiến độ nuôi và cấp của tướng đó; bản "chọn hết" lọc
  theo hệ.
- Trứng rơi trên máy bi kèm tiến độ và đồng hồ ("2/3", "00:14:32").

### 1.5. Gói người mới, lần đầu nạp

- **"新人豪礼" gói người mới 3 ngày**: thẻ dọc có tướng (sói), "超值 540%", **"连续3天每日可得!"** (nhận mỗi ngày 3 ngày liền), ngày 1 free, giới
  hạn 1 lần, có tên tướng tặng.
- **"首充特惠" lần đầu nạp 3 ngày**: ô ngày 1–3 (nhận được / đã nhận / khoá), tặng tướng ("小火柴") và khung avatar, "超值 540%".
- **"首充特惠!" chọn 1 trong 3**: ba cột xanh / tím / cam, "超值 200%", "你只能购买一个礼包哦~" (chỉ mua được một gói).
- **"启航礼包" gói khởi hành**: 5 ô gói, đồng hồ "04:24:20后结束", "$4.99", icon cúp vàng.
- Gói người mới tăng tốc ("beginner rush", chim đỏ): chỉ có ảnh.

### 1.6. Heo đất

- Nút ở màn chính: heo (bản sự kiện là voi) có **mặt nạ tròn nước dâng dần**, hai trạng thái chưa đầy / đầy, số bi tích được.
- Popup heo, đập heo, màn mở sự kiện heo: chỉ có tên (bundle tải sau). Tiếng: xuất hiện, đập, nghẽn, rơi, đầy.

### 1.7. Gói chuỗi, gói tự chọn

- **Gói chuỗi** (`ImpulseGift/chain`, `manual`): lưới ô xanh / tím / vàng nối bằng mũi tên trái / phải / xuống; **ô đầu "免费"**, các ô sau có giá
  ("$1.99") và khoá, mở lần lượt; đồng hồ. Bản "新宠降临" kèm tướng mới **tăng tỉ lệ mạnh**, "限购一次!".
- **Gói tự chọn** (`Shop/package/pbui_shop_package_selfselected_pop`): banner tướng, ô trứng tăng tỉ lệ, **2 ô "+" tự chọn món**, "任选2种道具",
  "超值 200%", "￥68".

### 1.8. Hẹn giờ, vòng quay, gói theo sự kiện

- **Vòng quay bất ngờ** (`surprise`, `surprise_new`): 11 ô cộng giải lớn, quay bằng chìa khoá; "mua một lần được hai lượt quay"; quay trả tiền
  "$4.99"; trúng giải lớn thì **vòng quay lên cấp**, thanh tiến độ "10/30".
- **Shop gạch bạc** làm mới theo giờ, "còn lại: 1".
- Gói người thắng sự kiện GVG, "限购一次!", 10 giờ.
- Thanh chuyển giữa các **bậc ưu đãi rẻ / thường / đắt** (`impulse_switch`: ảnh `cheap`, `gvg`; `normal`, `expensive` thiếu). Đoán: cùng một
  ưu đãi có nhiều bậc giá, người chơi lật qua.
- Điểm danh 7 ngày trả tiền theo mùa (Giáng sinh, Quốc khánh, Hè): ngày 4 và 7 tặng đồ trang trí.

### 1.9. Gói định kỳ

- **Thẻ tháng** ("精灵月卡"): nhận ngay một phần, mỗi ngày nhận tiếp, "一键领取" (nhận hết một lần).
- **Thẻ tuần** ("精灵周卡"): nhận ngay, sức chứa cây bi +1.500, 7 ngày.
- **Gói 7 ngày** ("七日礼包", "超值 540%"): ngày 7 ra hộp "?" ×20; popup riêng "七日累计可获得", "10:00:00后消失".
- **Quỹ trưởng thành II** ("成长基金II"): "đẩy tiến độ trận, nhận thưởng lớn", ô thưởng khoá theo mốc, "超值200%", không giới hạn giờ.
- **Pass** ("海底通行证", "沙城通行证"): hai hàng free / trả tiền, nhiệm vụ ra chìa khoá, quá cấp 50 thì cứ 100 chìa một phần thưởng; popup gạ:
  "超值 300%", "mỗi cây bi +500 tới hết mùa", "nhận ngay 60 chìa = lên 3 cấp"; mua cấp theo nhóm.
- **Mời VIP**: người chơi chi nhiều được mời vào kênh chăm sóc riêng (WhatsApp, Messenger, LINE…).
- **Club** trả tiền (gấu, "立即加入"); ô **nhập mã nhà sáng tạo** ("创作者计划").

### 1.10. Kiểu popup của họ

- Nền mờ (chụp màn rồi làm mờ), "点击空白继续" (bấm chỗ trống để tiếp), nút đóng tròn.
- Hầu hết có đồng hồ "…后结束" và nhãn giới hạn lượt mua.
- Nhóm popup gạ mua dùng chung anim trượt vào từ trái / phải: đoán là một **hàng popup nối nhau**, vuốt qua từng cái.
- Nhãn giá trị: sao tím, sao vàng, "HOT", nút "UP!". Không ảnh nào in giá; giá, % do code đè lên (đổi theo nước).

## 2. Thông tin công khai và số liệu ngành

Tìm trên web 2026-11-23. Một số trang chặn bot (PocketGamer.biz, Google Play, YouTube); dòng ghi "(trích)" là số lấy từ đoạn trích kết quả tìm
kiếm, chưa mở được trang gốc.

### 2.1. Clash of Critters

- **Ai làm:** Lilith phát triển, Farlight Games phát hành (`com.farlightgames.pgame.gp`). Ra toàn cầu 19–20/5/2026, Nhật 30/7/2026. App Store
  9+ có ghi "Contains Loot Boxes", Google Play Everyone 10+. 2 tuần ra một bản. ([App Store](https://apps.apple.com/us/app/-/id6741567125),
  [Bloxodes](https://bloxodes.com/wiki/clash-of-critters))
- **Doanh thu:** khoảng 250 nghìn USD/ngày lúc tháng 7; 34 triệu USD IAP và hơn 14 triệu lượt cài tới 9/2026, Mỹ 32%, Nhật 14%; 53,8 triệu USD tới
  19/10/2026 (trích). 90% lượt tải từ quảng cáo trả tiền. **100% IAP, không có quảng cáo** (AppGoblin: không SDK quảng cáo).
  ([Gamigion](https://www.gamigion.com/clash-of-critters-by-lilith-games-makes-250k-a-day/),
  [AppMagic](https://appmagic.rocks/blog/clash-of-critters-plinko-coin-looter), [AppGoblin](https://appgoblin.info/apps/com.farlightgames.pgame.gp))
- **Bậc giá App Store Mỹ:** "Tier 2 Offer" $1,99; các gói $2,99 / 4,99 / 9,99 / 14,99 / 19,99 / 29,99 / 49,99 / 99,99 / 199,99 (Anh, Nhật thêm $6,99).
  Android: mỗi món $0,79–199,99.
- **Gói (theo trang bán hộ và hướng dẫn, chưa chính thức):** thẻ tuần $4,99; thẻ tháng $19,99 = 27 hộp ước trong 30 ngày; quỹ trưởng thành = 7.000 bi
  và 30 hộp ước theo cấp; 25 hộp ước $99,99; gói lần đầu nạp **chọn 1 trong 3 mức giá, có hẹn giờ đẩy sang mức đắt**; thẻ tuần, thẻ tháng hiện
  từ những phiên đầu; tiền cứng 10.000 gem = $99,99. ([mturbogamer](https://mturbogamer.com/2026/07/clash-of-critters-wish-boxes/),
  [topuplive](https://www.topuplive.com/de/news/clash-of-critters-top-up-guide.html))
- **Bi miễn phí:** trần bi tự hồi 420; cây bi đầy sau 10–24 giờ được hơn 800 bi; quà ngày ở cửa hàng khoảng 60 bi (đặt **dưới** các gói trả tiền);
  nhiệm vụ ngày khoảng 10 bi; Badge Dojo 400 bi mỗi mốc. ([games.gg](https://games.gg/de/clash-of-critters/guides/clash-of-critters-so-farmst-du-schnell-kostenlose-pinballs/))
- **Người chơi chê popup** (review App Store; [Mỹ](https://apps.apple.com/us/app/clash-of-critters/id6741567125?see-all=reviews),
  [Anh](https://apps.apple.com/gb/app/clash-of-critters/id6741567125?see-all=reviews)):
  - popup mỗi lần mở game, mỗi lần bấm thả bi, không bỏ qua được, dội liên tiếp mấy cái;
  - "cứ 2 phút", "cứ 15 phút một lần"; "mỗi lần về sảnh 4–5 cái"; "máy bi luôn có 6 biểu tượng mồi mua bên trái kể cả khi đã từ chối hết";
  - xin nút "không hiện lại trong ngày";
  - "bấm lần đầu miễn phí, rồi bỗng thành 2,99" (gói chuỗi);
  - "thà xem quảng cáo lấy bi còn hơn trả 5 USD"; có người xin thêm lựa chọn xem quảng cáo đổi bi.
  - Bản 0.46.1 của họ có mục "tối ưu popup".

### 2.2. Số liệu ngành dùng trong kế hoạch

- **Người trả tiền:** 1,83% người dùng từng mua IAP; 28,8% trong số đó mua lần hai; 77% người mua mua lần đầu trong 2 tuần đầu
  ([Unity 2024](https://unity.com/en/resources/mobile-growth-monetization-report-2024)). 80–95% không trả tiền, 3–10% chi ít, 1–3% chi vừa, 0,1–1% chi
  lớn ([Facebook](https://developers.facebook.com/documentation/games/monetize/best-practices)).
- **Gói khởi đầu:** $0,99 với 3–5 lần giá trị (Facebook), hoặc $1,99–4,99 với 5–10 lần, mở trong 24–72 giờ sau cài (Unity); hiện ở phiên 3–5,
  mở 3–5 ngày ([Google](https://android-developers.googleblog.com/2016/08/5-tips-to-help-you-improve-game-as-a-service-monetization.html));
  gói rẻ nhất bán chạy nhất, phần lớn $0,99 ([Playliner](https://wnhub.io/news/other/item-11876)).
- **Thưởng lần đầu mỗi bậc:** phổ biến nhân đôi; thưởng thêm theo bậc cửa hàng 25–150% (Playliner).
- **Gói hẹn giờ** ([Sensor Tower Playliner 2/2026](https://investgame.net/news/pdf/2026-02-04-how-to-build-an-effective-offer-system-in-your-game/)):
  - gói bật lúc đang vui chỉ nên mở **5–10 phút**;
  - người chơi cần thấy một gói **khoảng 7 lần** mới mua;
  - ghi "+100%" hút hơn "-30%"; thưởng +100% chạy gần như mọi ngày thì mất giá trị cảm nhận;
  - mới làm thì 2–3 loại gói là đủ, hệ trưởng thành 4–5 loại; đừng xếp chồng gói cùng nội dung chỉ chênh 10–15%;
  - gói chính đặt gần mức chi trung bình mỗi lần; sau lần mua lớn thì hạ giá dần;
  - thang giá "Travel Deal" của Royal Match: 7 bậc $0,99 → 2,99 → 6,99 → 19,99 → 44,99 → 79,99 → 99,99; **mua thì lên một bậc, khoảng 1 tuần không
    mua thì xuống một bậc**.
- **Heo đất:** thường $1,99–4,99, người chơi mua nhiều nhất khi đầy, nên nhắm người đã từng trả tiền; Hexa Sort $4,99, mở ở màn 7, là IAP thứ 3
  của game ([Mistplay](https://business.mistplay.com/resources/piggy-banks-in-games/)).
- **Thẻ tháng:** Rise of Kingdoms $9,99 / 30 ngày ≈ 1,6 lần giá trị gói $49,99 ([Naavik](https://naavik.co/f2p-mobile/vip-subscriptions-recurring-revenue-revolution/)).
  **Battle pass** $5–15, giá trị 10–20 lần ([Deconstructor of Fun](https://www.deconstructoroffun.com/blog/2022/6/4/battle-passes-analysis)).
- **Quảng cáo thưởng** (Unity 2024):
  - 36% DAU game casual có xem;
  - vị trí lúc **hết tài nguyên** được xem nhiều nhất (38,1%), cửa hàng / sảnh / popup mỗi chỗ 25,2%;
  - 15–20 vị trí cho 46% người xem, 0–4 vị trí cho 33,4%;
  - người xem quảng cáo thưởng mua IAP nhiều hơn 4,5 lần (tương quan, [Tapjoy](https://unity.com/blog/understanding-the-impact-of-rewarded-ads-on-iap-retention-and-engagement)).
- **Trần quảng cáo:** Facebook đề xuất 5–10 lần/ngày; quảng cáo ra tiền mềm nên có trần, ví dụ 4 lần/ngày
  ([Sensor Tower hybrid 3/2026](https://investgame.net/news/pdf/2026-03-26-st-adhybrid-monetization_wp/)); Hempire nâng một chỗ từ 10 lên 20 lần/ngày
  thì ARPDAU +37% ([Unity](https://unity.com/resources/lbc-studios)).
- **Cân quảng cáo với IAP:** một quảng cáo cho khoảng 5% gói $4,99 (Facebook). Hồi sinh: thua lần 1 cho xem quảng cáo, thua lần 2 cùng màn chỉ trả
  tiền; **quảng cáo đặt đúng lúc người ta định mua sẽ ăn mất IAP**; phiên đầu không quảng cáo, phiên 2–3 mới có quảng cáo thưởng (Sensor Tower,
  Facebook).
- **"Bỏ quảng cáo" khi chỉ có quảng cáo thưởng:** Rollic, Voodoo giữ quảng cáo thưởng; vài game bán "skip-it" (bỏ qua mà vẫn nhận thưởng); Sensor
  Tower gợi ý chỉ kèm Bỏ quảng cáo trong gói từ $6,99, hoặc tặng tạm làm quà người quay lại.
- **Luật** ([Apple](https://developer.apple.com/app-store/review/guidelines/),
  [Google](https://support.google.com/googleplay/android-developer/answer/9858738), [FTC](https://www.ftc.gov/node/87282)):
  - Apple 3.1.1, Google mục 7: công bố tỉ lệ loot box trước khi mua, sát chỗ mua. Apple 2.3.1, 5.6: cấm giá quảng bá sai, cấm lừa mua.
  - FTC xử HoYoverse (1/2025, 20 triệu USD): công bố tỉ lệ và tỉ giá các tầng tiền ảo, loot box phải mua thẳng được bằng tiền thật, không bán loot box
    cho trẻ dưới 16 khi chưa có phụ huynh đồng ý. Kiện tập thể ở Mỹ nhắm "giá gốc bịa ra" (FunPlus, Warner Bros).
  - Hà Lan (ACM): giá giảm tính từ giá thấp nhất 30 ngày trước. EU (CPC 3/2025, không bắt buộc): ghi kèm giá tiền thật, tránh nhiều loại tiền ảo.
  - Bỉ coi loot box trả tiền là cờ bạc (thực thi lỏng); Hà Lan: toà xử EA thắng (gói FIFA không phạm luật cờ bạc). Hàn Quốc bắt công bố tỉ lệ từ
    3/2024, phạt nặng.
  - Google Families: quảng cáo phải đóng được sau 5 giây, chỉ SDK được chứng nhận, cấm "chiêu thương mại quá hung hăng".
- **Không tìm được số đo:** trần popup mỗi phiên ảnh hưởng thế nào tới bỏ game; flash sale 1–3 giờ so với 24 giờ; tỉ lệ chuyển đổi từng bước gói chuỗi.
  Các số này phải tự đo (mục 9.6).

## 3. Nguyên tắc

1. **Giá trị thật.** Nhãn "giá trị ×N" tính từ bảng giá gốc (mục 4.2), không gạch giá ảo. Đồng hồ là thật: hết giờ thì gói mất, không tự hồi
   lại ngay sau đó (đếm ngược giả vi phạm luật bảo vệ người tiêu dùng ở EU, Anh).
2. **Tỉ lệ công khai.** Rương Tướng và máy bi có nút "Tỉ lệ" (máy bi đã công khai, `07_MayBi.md`). Không làm "suýt trúng" (giữ chốt `23_MayBi_TraiNghiem.md`).
3. **Không chặn đường miễn phí.** Mọi thứ bán được đều kiếm được bằng chơi, chỉ chậm hơn. Sau khi thua, gợi ý cách miễn phí trước, gói sau.
4. **Popup có trần.** Tối đa 2 popup tự bật mỗi lần vào game, 4 mỗi ngày, cách nhau ít nhất 3 phút; không bật trong trận, lúc đang thả bi, lúc
   đang có bước hướng dẫn, trong phiên đầu tiên. Popup bán nào cũng có ô **"Hôm nay không hiện nữa"**. Đây là chỗ người chơi Critters chê nhiều nhất
   (mục 2.1): họ thắng nhờ người chi lớn và quảng cáo mua người chơi, mình không đi đường đó.
5. **Quảng cáo không ép.** Chỉ quảng cáo thưởng, người chơi tự bấm. Không quảng cáo xen kẽ, không banner.
6. **Hợp với chất "sổ tay phiêu lưu".** Popup là tờ giấy, nhãn là sticker, đồng hồ viết bút chì; theo bộ UI (`17_BoUI.md`), không bóng.

## 4. Tiền, vật phẩm, bảng giá gốc

### 4.1. Bán gì

| Vật phẩm | Đã có trong game | Nguồn miễn phí | Ghi chú |
|---|---|---|---|
| Bi | có (`balls`) | cây bi, Nhà, AFK, huy hiệu, máy bi | **bán từ nay** (đổi chốt cũ) |
| Rương Tướng | **mới** (vật phẩm) | quảng cáo mỗi ngày, bảng mốc quảng cáo, sự kiện | mở ra mảnh tướng; 2 loại: Rương Tướng, Rương Tướng Vàng |
| Rương hệ | **mới** | sự kiện | như Rương Tướng nhưng chỉ tướng một hệ |
| Vé chọn tướng | **mới** | quỹ, pass | chọn 1 trong 6 tướng gợi ý, nhận mảnh tướng đó |
| Mảnh tướng | có (`shards`) | ải, AFK | bán qua rương, vé, gói tướng |
| Đá tiến hóa, đá tiềm năng, đá tinh | có | huy hiệu, Hang, máy bi | bán ít, chỉ trong gói (chốt cũ cấm bán đá tiềm năng: câu 1) |
| Bản sao thẻ | có (`copies`) | rương máy bi | không bán riêng, có trong Rương Tướng (mảnh thừa đổi bản sao) |
| Quyền lợi: Thẻ Tuần, Thẻ Phiêu Lưu (tháng), Bỏ quảng cáo, Quỹ | Thẻ Phiêu Lưu, Bỏ quảng cáo có (`Entitlements`) | không | |

**Chưa thêm tiền cứng (kim cương).** Bán thẳng bằng tiền thật đơn giản hơn: không phải chia tiền trả / tiền free như Critters, không phải cân
thêm một loại tiền. Khi cần shop làm mới theo giờ, vòng quay hay mua cấp pass thì tính lại (câu 2).

### 4.2. Bảng giá gốc (đơn vị "bi quy đổi")

Dùng để tính nhãn giá trị và cân gói; số đầu, chỉnh bằng `ProgressSim`.

| Món | Bi quy đổi |
|---|---|
| 1 bi | 1 |
| 1 mảnh tướng Thường / Khá / Hiếm / Sử thi / Huyền thoại | 8 / 10 / 15 / 25 / 45 |
| 1 Rương Tướng (kỳ vọng) | 120 |
| 1 Rương Tướng Vàng (kỳ vọng) | 450 |
| 1 vé chọn tướng | 300 |
| 1 đá tiến hóa / đá tiềm năng / đá tinh | 150 / 25 / 100 |
| Giá gốc tiền thật | **$0,99 = 100 bi quy đổi** (bậc bi nhỏ nhất, không thưởng) |

Nhãn "giá trị ×N" = tổng bi quy đổi trong gói ÷ (giá × 100 / 0,99). Ví dụ gói $4,99 chứa 2.000 bi quy đổi: 2.000 ÷ 504 ≈ ×4.

**Bi theo cấp.** Bi thụ động tăng từ khoảng 300/ngày (đầu game) lên 700–1.100/ngày (cuối game) (`12_KeHoach_OpenSpec.md`). Số bi trong gói nhân
theo 5 bậc cấp người chơi (×1, ×1,5, ×2, ×2,5, ×3; bậc mở theo cấp 1/20/50/90/130) để gói luôn bằng khoảng cùng số giờ bi thụ động. Trong một
bậc thì số cố định, không đổi theo từng cấp.

### 4.3. Bậc giá

Dùng bậc giá của store: $0,99, $1,99, $2,99, $4,99, $9,99, $19,99, $49,99, $99,99. Giá hiện lấy chuỗi đã bản địa hoá từ store (Việt Nam khoảng
25.000đ, 49.000đ, 75.000đ, 125.000đ, 249.000đ, 499.000đ, 1.249.000đ, 2.499.000đ). Không ghi giá cứng trong ảnh.

## 5. Cửa hàng

### 5.1. Lối vào

- Nút **Cửa hàng** ở sảnh (cạnh thanh trên), icon xoay vòng giữa các gói đang có như Critters, chấm đỏ khi có quà free chưa nhận hoặc gói mới.
- **Bong bóng ưu đãi** dọc mép trái sảnh: mỗi gói có hẹn giờ đang mở là một bong bóng sticker kèm đồng hồ bút chì (tối đa 3, quá thì gộp "+2").
  Chạm là mở popup của gói. Đây là chỗ nhắc chính, ít phiền hơn popup tự bật.
- **Lọ Bi** (heo đất, mục 6.7) là một nút riêng ở sảnh, nước bi dâng dần.
- Từ máy bi: chip bi trên thanh trên chạm vào thì mở tab Bi. Từ hộp chi tiết tướng: nút "Mảnh" mở tab Tướng lọc theo tướng đó.

### 5.2. Bốn tab

| Tab | Có gì |
|---|---|
| **Ưu đãi** | quà free mỗi ngày (bấm nhận); gói đang có hẹn giờ (chớp nhoáng, chuỗi, người mới, trở lại); Lọ Bi; gói 7 ngày theo mùa |
| **Bi** | xem quảng cáo nhận bi; 6 bậc bi, **lần đầu mỗi bậc tặng gấp đôi**; gói bổ sung bi |
| **Tướng** | Rương Tướng (1 / 10), Rương Tướng Vàng (1 / 10), bảo hiểm (mục 6.3); rương miễn phí hôm nay (quảng cáo); gói tướng tuần (2 tướng xoay vòng); nút "Tỉ lệ" |
| **Đặc quyền** | Thẻ Tuần, Thẻ Phiêu Lưu (tháng), Quỹ Phiêu Lưu, Bỏ quảng cáo; Khôi phục giao dịch |

Mỗi ô gói: tên, hàng vật phẩm (icon + số), sticker "giá trị ×N", nút giá, "còn N lượt", đồng hồ nếu có hẹn giờ. Mua xong: món bay vào túi
(dùng `FarmFx.Fly` như hái Cây bi), ô đổi "Đã mua" hoặc biến mất.

## 6. Các gói

Giá, số lượng là số đầu (bậc cấp ×1), chỉnh bằng `ProgressSim` và số đo thật.

### 6.1. Gói người mới

| Gói | Khi nào | Giá | Có gì | Giới hạn |
|---|---|---|---|---|
| **Quà Nhập Môn** (học "新人豪礼 / 首充特惠" 3 ngày) | xong chuỗi hướng dẫn bắt buộc (C17, `25_FTUE.md`): hiện ở tab Ưu đãi và bong bóng sảnh; popup tự bật lần đầu ở **phiên 2** (Google gợi ý phiên 3–5, Facebook: phiên đầu gần như không gạ); mở 72 giờ tính từ lúc popup | $0,99 | ngày 1: 300 bi + 1 Rương Tướng; ngày 2: vé chọn tướng Hiếm; ngày 3: 2 Rương Tướng + khung chân dung "Nhà thám hiểm" | 1 lần; phải vào game mỗi ngày để nhận (kéo người chơi về D2, D3) |
| **Gói Khởi Hành** (học "启航礼包") | ngày 2, hoặc khi mua Quà Nhập Môn xong | $4,99 | 1.200 bi + 5 Rương Tướng + 1 Rương Tướng Vàng + 2 đá tiến hóa (≈×6) | 1 lần, 48 giờ |
| **Lần đầu nạp tặng đôi** | mọi bậc bi | | bi gấp đôi lần đầu mỗi bậc | 1 lần mỗi bậc |

### 6.2. Bi

| Bậc | Giá | Bi | Lần đầu |
|---|---|---|---|
| Túi bi | $0,99 | 100 | +100 |
| Rổ bi | $4,99 | 550 | +550 |
| Thùng bi | $9,99 | 1.200 | +1.200 |
| Xe bi | $19,99 | 2.600 | +2.600 |
| Núi bi | $49,99 | 7.000 | +7.000 |
| Đảo bi | $99,99 | 15.000 | +15.000 |

**Gói Bổ Sung Bi** (học "弹珠补充!"): popup 3 ô bậc ($1,99 / $4,99 / $9,99, mỗi ô tặng thêm 30–50%), bật khi hết bi (mục 7.4). Có ô xem quảng cáo
nhận bi ở đầu popup nếu còn lượt.

### 6.3. Tướng: Rương Tướng

- Mở ra mảnh của **một tướng**, theo độ hiếm:

  | | Thường | Khá | Hiếm | Sử thi | Huyền thoại |
  |---|---|---|---|---|---|
  | Rương Tướng: tỉ lệ | 40% | 32% | 18% | 8% | 2% |
  | Rương Tướng: số mảnh | 6–8 | 5–7 | 4–6 | 3–5 | 2–3 |
  | Rương Tướng Vàng: tỉ lệ | | 30% | 38% | 24% | 8% |
  | Rương Tướng Vàng: số mảnh | | 12–16 | 10–14 | 8–12 | 6–9 |

- Tướng trong độ hiếm: ưu tiên tướng đã có hoặc đang góp mảnh (60%), còn lại chia đều. Tướng đã tối đa sao thì mảnh đổi bản sao thẻ (có sẵn
  trong `Progress.AddShards`).
- **Bảo hiểm:** cứ 10 rương mở liền chắc có ít nhất 1 Sử thi; đếm từ lần Huyền thoại gần nhất, tới rương thứ 40 chắc Huyền thoại. Bộ đếm hiện
  trên nút ("còn 7 rương chắc Sử thi").
- **Giá:** 1 Rương Tướng $0,99 (1 lần mỗi ngày, dùng làm cửa mua rẻ); 10 Rương Tướng $9,99; 1 Rương Tướng Vàng $4,99; 10 Rương Tướng Vàng $39,99.
- **Free:** 1 Rương Tướng mỗi ngày bằng quảng cáo; thêm từ bảng mốc quảng cáo (mục 8.2), Quỹ, sự kiện.
- Mở nhiều: "Mở 10" diễn nhanh, dừng lâu ở rương Sử thi / Huyền thoại (rig rương AtomSpine như máy bi, `23_MayBi_TraiNghiem.md`).
- **Gói tướng tuần:** 2 tướng xoay vòng mỗi tuần; gói $4,99 = 1 vé chọn tướng (chọn 1 trong 2) + 3 Rương Tướng; tỉ lệ ra 2 tướng đó ×3 trong Rương
  Tướng suốt tuần (học "新宠降临 / 新塔塔甄选").

### 6.4. Vé chọn tướng

- Học "自选精灵: chọn 3 trong 6". Mở vé: hiện 6 tướng gợi ý (ưu tiên tướng chưa có của đảo đang đánh, tướng khắc hệ boss sắp tới, tướng sắp lên
  sao); mỗi ô ghi tiến độ mảnh ("12/20"). Chọn 1: nhận đủ mảnh để mở khoá tướng đó (hoặc 20 mảnh nếu đã có).
- Có trong Quà Nhập Môn, Quỹ, gói tướng tuần, pass. Không bán lẻ.

### 6.5. Gói chuỗi "Chuỗi Quà"

- Học "除臭礼包 / 饲养礼包": 8 ô nối nhau, mở lần lượt; ô 1, 3, 6 **miễn phí**, ô 2 $0,99, ô 4 $1,99, ô 5 $2,99, ô 7 $4,99, ô 8 miễn phí (phần
  lớn nhất). Ô miễn phí kéo người chơi mua ô trả tiền ngay trước nó.
- Kéo dài 72 giờ, 2 tuần một lần. Mỗi lần một chủ đề: Chuỗi Bi, Chuỗi Tướng (theo gói tướng tuần), Chuỗi Tiến Hóa (đá tiến hóa, mảnh).
- Người chưa mua lần nào: ô trả tiền rẻ hơn một bậc.

### 6.6. Ưu đãi chớp nhoáng "Ưu Đãi Bất Ngờ" (2–3 giờ)

- Học "惊喜特惠": tờ giấy vàng nổ, **một món lớn**, đồng hồ, sticker "giá trị ×4".
- Món theo nhu cầu lúc đó (Offer Engine chọn, mục 7.3): sắp hết bi thì bi; tướng trong đội sắp lên sao thì mảnh tướng đó; vừa thua boss thì mảnh
  tướng khắc hệ; tướng đủ mảnh mà thiếu đá tiến hóa thì đá.
- Giá theo nhóm người chơi (mục 7.2): chưa mua lần nào $0,99–$1,99; đã mua $4,99 (bằng lần mua gần nhất); chi nhiều $9,99–$19,99.
- Kéo dài **2–3 giờ** (bật lúc vào game: 2 giờ; bật khi vừa vào máy bi mà bi dưới 20% mức cược đang dùng: 3 giờ). 1 lượt mua. Tối đa 1 cái đang
  mở, 2 cái mỗi ngày, cách nhau ít nhất 6 giờ.
- **Ưu Đãi Nóng** (biến thể ngắn): bật ngay sau trận thắng boss đảo, jackpot, rương Huyền thoại; mở **10 phút** (Playliner: gói lúc đang vui chỉ
  nên 5–10 phút); cùng giá, một món ăn mừng (bi hoặc Rương Tướng Vàng). Tính chung trần với Ưu Đãi Bất Ngờ.
- Hết giờ thì tắt. Bấm đóng thì thành bong bóng ở sảnh tới hết giờ (người chơi cần thấy gói nhiều lần mới mua, bong bóng là chỗ cho thấy mà
  không phiền).

### 6.7. Lọ Bi (heo đất)

- Học heo đất của Critters, đổi hình cho hợp chất game: **lọ thuỷ tinh** ở sảnh, bi dâng dần (mặt nạ nước như `txvx_shop_package_piggy_water`).
- Mỗi bi thả vào máy bỏ 1 bi vào lọ (đã tính cược, nên cược ×10 bỏ 10). Lọ chứa tối đa 2.000 bi (bậc cấp ×1).
- Đập lọ $4,99 khi đã đủ 40% (800 bi). Đầy thì lọ phập phồng, popup một lần (mục 7.1) và không tích thêm. Đập xong lọ về 0, sức chứa lần sau
  +20% (tối đa ×2).
- Giá trị lúc đầy: 2.000 bi cho $4,99 ≈ ×4.

### 6.8. Gói định kỳ

| Gói | Giá | Có gì | Ghi chú |
|---|---|---|---|
| **Thẻ Tuần** | $1,99 | nhận ngay 300 bi; mỗi ngày 100 bi × 7; sức chứa cây bi +50% trong 7 ngày | học "精灵周卡" |
| **Thẻ Phiêu Lưu** (tháng, đã có) | $4,99 | giữ quyền lợi cũ (cây ×1,5, khay AFK 5 ô, rương AFK 1 giờ); **thêm** nhận ngay 1 Rương Tướng Vàng, mỗi ngày 150 bi + 1 lượt xem quảng cáo không cần xem | mỗi ngày phải vào game nhận |
| **Quỹ Phiêu Lưu** | $9,99 | thưởng ở cấp 10, 15, 20 … 60: tổng 12.000 bi quy đổi (bi, Rương Tướng, vé chọn tướng, đá tiến hóa); hàng miễn phí nhỏ hơn cho mọi người | học "成长基金", không hẹn giờ |
| **Bỏ quảng cáo** (đã có) | $4,99 | quảng cáo thưởng trao ngay, vẫn theo trần mỗi ngày | non-consumable, khôi phục được |
| **Gói 7 Ngày** theo mùa | $4,99 | mua một lần, nhận mỗi ngày, ngày 7 ra 3 Rương Tướng Vàng + đồ trang trí Nhà theo mùa | làm sau (S5), học "七日礼包" và điểm danh mùa |

Critters bán thẻ tuần $4,99, thẻ tháng $19,99 (theo trang bán hộ, mục 2.1); người chơi của họ chi lớn. Mình có quảng cáo thưởng và nhắm người chơi
casual hơn nên để $1,99 / $4,99; sau khi có số đo thì thử A/B $2,99 / $9,99 (câu 11).

### 6.9. Gói theo lúc (Offer Engine bật, mục 7)

| Gói | Bật khi | Giá | Có gì | Hẹn giờ |
|---|---|---|---|---|
| **Gói Tiếp Sức** | thua ≥ 2 lần liền ở một ải và đã có gợi ý miễn phí (7.3) | $1,99 / $4,99 | mảnh tướng chủ lực đang thiếu sao, bản sao thẻ Chiêu, bi | 2 giờ |
| **Gói Đồng Hành** | vừa mở khoá một tướng | $2,99 | mảnh lên sao của tướng đó + 1 Rương Tướng | 24 giờ |
| **Gói Sắp Lên Sao** | tướng trong đội có ≥ 80% mảnh lên sao | $1,99 | đủ mảnh còn thiếu + 1 đá tiến hóa | 3 giờ |
| **Gói Đảo Mới** | mở một đảo mới (sau C11) | $4,99 | vé chọn tướng hệ khắc boss đảo đó + bi | 48 giờ |
| **Quà Trở Lại** | vắng ≥ 3 ngày | miễn phí + gói $1,99 | 200 bi free; gói: 600 bi + 2 Rương Tướng | 48 giờ |
| **Gói Hết Bi** | xem 6.2 | | | |

**Không làm** (học Critters nhưng bỏ): vòng quay trả tiền (gần cờ bạc), thu ngân web hoàn 5% (trái chính sách store), mời VIP qua WhatsApp, Club.

## 7. Kịch bản popup (Offer Engine)

### 7.1. Hàng popup lúc vào game

Mỗi lần vào sảnh từ màn tải (lần mở game, quay lại sau ≥ 30 phút), xét theo thứ tự, **lấy tối đa 2**:

1. Quà hằng ngày chưa nhận (Thẻ Tuần / Thẻ Phiêu Lưu / Quà Nhập Môn ngày N). Miễn phí, không tính vào trần popup bán.
2. Lọ Bi vừa đầy (chỉ lần đầu đầy).
3. Gói đang mở còn dưới 1 giờ ("sắp hết"), mỗi gói một lần.
4. Quà Trở Lại (vắng ≥ 3 ngày).
5. Gói người mới tới lượt (Quà Nhập Môn ở phiên 2, Gói Khởi Hành ngày 2).
6. Ưu Đãi Bất Ngờ mới (xác suất, mục 7.5).
7. Chuỗi Quà mới mở (lần đầu của đợt).

Popup sau mở khi popup trước đóng (trượt vào từ phải như Critters). Phần còn lại thành bong bóng ở sảnh.

### 7.2. Nhóm người chơi

| Nhóm | Điều kiện | Khác gì |
|---|---|---|
| Mới | chưa xong chuỗi hướng dẫn, hoặc phiên đầu | **không popup bán** |
| Chưa mua | chưa giao dịch nào | gói $0,99–$1,99; nhấn quảng cáo thưởng |
| Mua nhỏ | đã mua, tổng < $20 trong 30 ngày | gói ngang lần mua gần nhất, thỉnh thoảng bậc trên |
| Mua vừa | $20–$100 / 30 ngày | $4,99–$19,99; chuỗi, Quỹ |
| Mua nhiều | > $100 / 30 ngày | $19,99–$49,99; gói Rương Tướng Vàng ×10 |
| Vắng | không vào ≥ 3 ngày | Quà Trở Lại |

**Thang giá** (học "Travel Deal" của Royal Match, mục 2.2): gói chớp nhoáng, gói theo lúc dùng thang $0,99 → 1,99 → 4,99 → 9,99 → 19,99 → 49,99.
Người chưa mua đứng ở $0,99. Mua thì lần sau lên một bậc; 7 ngày không mua gói nào trên thang thì xuống một bậc. Sau một lần mua lớn (≥ $19,99)
thì gói kế xuống một bậc, không đẩy tiếp.

### 7.3. Sau khi thua

Thua không mất gì (`25_FTUE.md` E2). Kịch bản theo số lần thua liền ở cùng ải:

| Lần thua | Hộp kết quả hiện | Gói |
|---|---|---|
| 1 | "Thua không mất gì", nút Máy bi, Tướng (đã có) | không |
| 2 | thêm dòng "Đội bạn yếu hơn ải khoảng X%" và **cách miễn phí đang làm được ngay**: nâng Chiêu (có bản sao), lên sao (đủ mảnh), đổi tướng khắc hệ, nhận AFK; nút quảng cáo **"Tiếp sức"**: đánh lại với +15% công và máu, 3 lần mỗi ngày | không |
| ≥ 3, và **không còn cách miễn phí nào làm ngay được** | như trên | **Gói Tiếp Sức** (2 giờ), đúng món đang thiếu |
| ≥ 3, còn cách miễn phí | như lần 2 | không |

- Gói Tiếp Sức tối đa 1 lần mỗi 24 giờ, không bật với nhóm Mới, không bật ở 2 trận có kịch bản hướng dẫn.
- Boss đảo: thua lần đầu đã hiện dòng gợi ý khắc hệ; gói như trên.

### 7.4. Hết bi

Khi bấm thả mà không đủ bi cho mức cược:

1. Còn bi nhưng thiếu cho cược hiện tại: hạ cược tự động, toast "Đã hạ cược ×N" (không popup).
2. Hết hẳn: popup "Hết bi!" gồm: xem quảng cáo +N bi (nếu còn lượt); Cây bi đầy lúc nào (nút đi hái nếu có bi chờ); Lọ Bi (nếu ≥ 40%); 3 ô Gói
   Bổ Sung Bi. Tối đa 1 lần mỗi 20 phút; lần sau trong 20 phút chỉ toast.
3. Hết bi lần đầu trong đời: chỉ có quảng cáo và Cây bi, chưa có gói (người chơi mới học máy bi).

### 7.5. Ưu Đãi Bất Ngờ: khi nào bật

- Lúc vào game: 25% nếu không có gói chớp nhoáng nào đang mở và đã quá 6 giờ từ gói trước; nhóm Mua vừa / Mua nhiều 35%.
- Vào máy bi mà bi dưới 20% mức cược đang dùng: 30% (chưa phải hết bi, nên chưa bật popup Hết bi).
- Sau trận thắng boss đảo, jackpot máy bi, mở được rương Huyền thoại: Ưu Đãi Nóng 10 phút, 30%.
- Tối đa 2 mỗi ngày (cả hai loại). Chọn món theo 6.6.

### 7.6. Theo mốc

| Mốc | Popup |
|---|---|
| Xong C17 (hết chuỗi hướng dẫn) | Quà Nhập Môn hiện ở tab Ưu đãi và bong bóng; popup ở phiên 2 |
| Ngày 2 | Gói Khởi Hành |
| Cấp 10 | giới thiệu Thẻ Tuần (một lần, kèm nút "Xem sau") |
| Cấp 15 hoặc ngày 3 | giới thiệu Quỹ Phiêu Lưu |
| Mở khoá tướng | Gói Đồng Hành |
| Mở đảo mới | Gói Đảo Mới |
| Tướng trong đội ≥ 80% mảnh lên sao | Gói Sắp Lên Sao (tối đa 1 mỗi ngày) |
| Mua xong một gói | không popup bán trong 10 phút; sau đó gói kế của chuỗi nếu có |

### 7.7. Trần và chặn

- Popup bán tự bật: ≤ 2 mỗi lần vào sảnh, ≤ 4 mỗi ngày, cách nhau ≥ 3 phút.
- Cùng một gói: bị đóng 1 lần thì không tự bật lại trong 24 giờ; bị đóng 3 lần thì 72 giờ.
- Tích "Hôm nay không hiện nữa": không popup bán tự bật tới 0 giờ hôm sau (bong bóng sảnh vẫn còn).
- Không bật popup khi người chơi chỉ vừa bấm thả bi (Critters bị chê vì việc này); popup Hết bi chỉ bật khi thật sự hết.
- Bong bóng sảnh tối đa 3 cái, không hiện trên màn máy bi (Critters có tới 6 biểu tượng bên trái máy bi, bị chê).
- Không bật khi: đang trận, đang thả bi / mở rương, có bước hướng dẫn chờ (`Guide.Idle` sai), có hộp thoại khác đang mở, đang chuyển cảnh,
  vừa xem quảng cáo xong (5 giây).
- Ngày đầu (D0): tối đa 1 popup bán (Quà Nhập Môn).
- Có công tắc tắt từng gói, từng kịch bản qua cấu hình từ xa (mục 9.6).

## 8. Quảng cáo thưởng

### 8.1. Chỗ đặt

Đã có 6 chỗ (`balance.json` → `ads.limits`). Thêm 6 chỗ (đánh dấu **mới**):

| Chỗ đặt | Thưởng | Trần / ngày | Ghi chú |
|---|---|---|---|
| `tree_double` Hái ×2 | bi cây ×2 | 3 | có |
| `afk_chest_open` Mở ngay rương AFK | mở ngay | 4 | có |
| `afk_boost` Tăng tốc AFK ×2 | 2 giờ | 3 | có |
| `farm_boost` | | 3 | có (trang trại cũ) |
| `cave_extra` +1 lượt Hang | +1 lượt | 1 | có |
| `home_speed` Rút 30 phút xây | 30 phút | 3 | có |
| **`free_balls`** Bi miễn phí (tab Bi, popup Hết bi) | 30 bi × bậc cấp | 5, cách 10 phút | **mới** |
| **`hero_chest`** Rương Tướng miễn phí | 1 Rương Tướng | 1 | **mới** |
| **`battle_retry`** Tiếp sức sau khi thua | đánh lại +15% công, máu | 3 | **mới** |
| **`win_double`** Nhận ×2 thưởng ải | mảnh, bi của ải ×2 | 5 | **mới**; không áp cho trận có kịch bản hướng dẫn |
| **`chest_upgrade`** Nâng rương máy bi | Gỗ → Bạc (hoặc Bạc → Vàng 1 lần/ngày) | 3 | **mới**; nút trên màn mở rương |
| **`daily_gift`** Quà ngày ×2 | quà free tab Ưu đãi ×2 | 1 | **mới** |

### 8.2. Bảng mốc quảng cáo

- Tab Ưu đãi có dải "Hôm nay đã xem N quảng cáo": mốc 3 → 50 bi, mốc 6 → 1 Rương Tướng, mốc 10 → 1 Rương Tướng + 1 đá tiến hóa. Về 0 mỗi ngày.
- Thẻ Phiêu Lưu và Bỏ quảng cáo cũng tính lượt (trao ngay vẫn đếm).

### 8.3. Luật

- Không quảng cáo trong phiên đầu và trước khi xong C17 (chuỗi hướng dẫn).
- Tổng trần khoảng 30 lượt mỗi ngày. Trung bình người xem nhiều khoảng 8–12 lượt.
- Nút quảng cáo ghi rõ thưởng và lượt còn ("Xem quảng cáo: +30 bi (4/5)"), dùng `Ads.Bind` có sẵn.
- Quảng cáo không tải được: nút xám "Chưa có quảng cáo, thử lại sau", không trừ lượt.
- **Cân với IAP:** một lượt `free_balls` (30 bi) bằng khoảng 5% Rổ bi $4,99 (550 bi), đúng mức Facebook gợi ý (mục 2.2). Quảng cáo nhiều nhất một
  ngày (khoảng 400 bi quy đổi) dưới một ngày bi thụ động cuối game.
- **Không ăn mất IAP:** trong popup Hết bi, ô quảng cáo nằm trên nhưng chỉ cho 30 bi (đủ chơi vài phút); muốn chơi tiếp lâu thì Cây bi hoặc gói.
  Tiếp sức bằng quảng cáo ở lần thua 2, gói ở lần thua ≥ 3 (giống "thua lần 1 xem quảng cáo, lần 2 trả tiền" của Sensor Tower).
- Người chơi Critters xin "xem quảng cáo đổi bi" (mục 2.1): đây là chỗ mình hơn họ cho người không trả tiền.

## 9. Kỹ thuật

### 9.1. Dữ liệu

- File mới `Assets/02 Data/Json/shop.json`, nhập bằng menu `PokiClash/Nhập dữ liệu` vào `BalanceConfig.shop`:
  - `products`: mã SKU store, loại (consumable / non-consumable / subscription), bậc giá;
  - `packs`: mã, tên, nội dung (`balls`, `heroChest`, `goldChest`, `ticket`, `shards:<hero>`, `evo`…), giá, giới hạn, hẹn giờ, tab;
  - `chests`: tỉ lệ độ hiếm, số mảnh, bảo hiểm;
  - `offers`: kịch bản (sự kiện, điều kiện, nhóm, xác suất, gói, hẹn giờ, ưu tiên);
  - `caps`: trần popup; `segments`; `valueOf` (bảng 4.2); `levelBands`.
- `ads.limits` thêm 6 chỗ mới; `ads.milestones` cho bảng mốc.
- Tên gói, mô tả theo luật đa ngôn ngữ (`24_DaNgonNgu.md`): khoá tiếng Việt, bản Anh trong `Loc/en/names.json`.

### 9.2. Lõi (C# thuần, `Assets/01 Script/Core`)

- `Shop.cs`: mua gói → trao nội dung, ghi lượt mua, lần đầu tặng đôi, Lọ Bi, Thẻ Tuần / tháng nhận mỗi ngày, Quỹ.
- `HeroChest.cs`: mở rương (tỉ lệ, bảo hiểm, ưu tiên tướng đang góp), trả danh sách mảnh; dùng `Rng` có hạt để test.
- `Offers.cs`: nhận sự kiện (`AppOpen`, `BattleLost`, `BattleWon`, `OutOfBalls`, `LevelUp`, `HeroUnlocked`, `ZoneOpened`, `NearStar`, `Jackpot`,
  `Purchased`, `Returned`), xét điều kiện, nhóm, trần, chặn; trả gói cần bật. Không gọi Unity, test được ngoài Editor.
- `AdGate` có sẵn: thêm chỗ đặt, bảng mốc.
- Test NUnit: tỉ lệ rương (10.000 lần mở trong khoảng tin cậy), bảo hiểm, trần popup, thang giá, hết giờ, chuyển ngày, Lọ Bi.

### 9.3. Bản lưu

`SaveData.shop` (bản lưu lên một số, có bước chuyển):
- `bought` (gói → số lần, ngày mua gần nhất), `firstBuy` (bậc đã tặng đôi);
- `offers` (gói đang mở: hạn, đã mua; lịch sử: lần bật, lần đóng, số lần đóng);
- `piggy` (bi trong lọ, số lần đập), `chain` (đợt, ô đã mở), `chestPity` (đếm Sử thi, Huyền thoại);
- `cards` (Thẻ Tuần / tháng: hạn, ngày nhận cuối), `fund` (đã mua, mốc đã nhận);
- `spend` (tổng 30 ngày theo bậc, số lần mua, lần mua cuối), `lossStreak` theo ải, `adsWatched` theo ngày.
- Gói người mới, đồng hồ dùng giờ máy. Chỉnh giờ máy để gian được; giảm bằng cách lấy giờ mạng khi có (câu 9).

### 9.4. Giao diện (prefab, theo luật "mọi thứ là prefab")

- `Screens/CuaHang` (4 tab, danh sách cuộn), `Items/OGoi` (ô gói), `Items/OBac` (ô bậc bi).
- `Dialogs/UuDai` (popup một gói, biến thể: chớp nhoáng, người mới 3 ngày, chuỗi 8 ô, bổ sung 3 ô, Lọ Bi), `Dialogs/TiLe` (bảng tỉ lệ),
  `Dialogs/MoRuongTuong` (mở 1 / 10, rig AtomSpine).
- Sảnh: nút Cửa hàng, cột bong bóng ưu đãi, nút Lọ Bi (`HubScene`; nút đáy đang được phiên khác sửa, xếp chỗ sau).
- Hộp kết quả trận: dòng gợi ý, nút Tiếp sức (quảng cáo), Gói Tiếp Sức.
- Ảnh cần gen (Magnific / file prompt GPT): nền popup chớp nhoáng (nổ vàng vẽ chì sáp), banner rổ bi, Rương Tướng và Rương Tướng Vàng (đóng / mở),
  vé chọn tướng, Lọ Bi (lọ trống + lớp bi), thẻ tuần / tháng, sticker "giá trị ×N", icon bong bóng ưu đãi. Không vẽ bóng (luật UI).

### 9.5. SDK

- IAP: **Unity IAP** (Google Play Billing, App Store), gắn vào `IStore` có sẵn (`App/Ads.cs`). Khôi phục giao dịch cho Bỏ quảng cáo; giao dịch
  chưa trao (tắt app giữa chừng) trao lại lúc mở game.
- Quảng cáo: **AppLovin MAX** làm mediation (AdMob, Unity Ads, Mintegral, Pangle, Liftoff…), gắn vào `IRewardAds`. Đồng ý quảng cáo: Google UMP
  (EU), ATT (iOS).
- Đo: Firebase Analytics (+ Remote Config), AppsFlyer nếu chạy quảng cáo mua người chơi.
- Không có máy chủ: xác thực hoá đơn trên máy (Unity IAP kiểm chữ ký Google / Apple). Có máy chủ thì chuyển sau.

### 9.6. Cấu hình từ xa và đo

- Remote Config đè `shop.json` theo khoá: bật / tắt gói, đổi xác suất, trần, giá trị, thử A/B hai nhóm.
- Sự kiện ghi lại: `offer_shown` (gói, kịch bản, nhóm), `offer_closed`, `offer_bought`, `iap_start`, `iap_done`, `iap_fail`, `ad_offer`,
  `ad_start`, `ad_done`, `ad_fail`, `out_of_balls`, `battle_lost` (lần thứ mấy), `chest_open`.
- Chỉ số theo dõi: tỉ lệ người trả tiền D7, ARPDAU (IAP / quảng cáo), số quảng cáo mỗi người mỗi ngày, tỉ lệ bật → mua từng kịch bản, giữ chân D1
  / D7 (popup có làm rơi giữ chân không).

### 9.7. Luật store và pháp lý

- Rương Tướng, máy bi: công bố tỉ lệ trước khi mua, sát nút mua (Apple 3.1.1, Google Play mục 7); Rương Tướng mua thẳng được bằng tiền thật
  (đúng hướng FTC xử HoYoverse). App Store sẽ ghi "Contains Loot Boxes" như Critters.
- Bỉ coi loot box trả tiền là cờ bạc: phát hành ở Bỉ thì tắt bán Rương Tướng (cờ theo nước trong Remote Config), để vé chọn tướng. Hà Lan đã xử EA
  thắng, không cần tắt. Hàn Quốc: bắt buộc công bố tỉ lệ, phạt nặng.
- Đồng hồ phải thật; nhãn giá trị tính từ bảng giá gốc công khai, không gạch "giá gốc" chưa từng bán (Apple 2.3.1, 5.6; ACM Hà Lan; kiện tập thể
  ở Mỹ). Hết giờ không chạy lại ngay.
- Đối tượng: không nhắm trẻ dưới 13 (không vào chương trình Families của Google). Critters để 9+ / Everyone 10+; mình đề xuất 12+ vì có loot box
  trả tiền và gói hẹn giờ. Muốn mở cho trẻ em thì phải bỏ bớt gói gạ, quảng cáo đóng được sau 5 giây, chỉ dùng SDK được chứng nhận, không gửi mã
  quảng cáo.
- Một loại tiền (tiền thật, không tiền cứng) cũng hợp hướng dẫn CPC của EU (tránh nhiều loại tiền ảo).
- Phát hành ở Nhật: hiển thị theo luật thương mại đặc định (Critters có dòng "关于特定交易法").

## 10. Mốc

| Mốc | Việc | Phụ thuộc |
|---|---|---|
| **S0** | `shop.json`, nhập dữ liệu, `Shop.cs`, `HeroChest.cs`, `Offers.cs`, bản lưu, test NUnit; đo kinh tế bằng `ProgressSim` (người chơi không mua / mua nhỏ / mua vừa) | — |
| **S1** | màn Cửa hàng 4 tab, ô gói, mua giả lập (`App/Dev/FakeMonetization`), mở Rương Tướng 1 / 10, bảng tỉ lệ, nút sảnh | S0, ảnh |
| **S2** | Offer Engine trong game: hàng popup lúc vào game, Hết bi, Sau khi thua, Ưu Đãi Bất Ngờ, gói người mới, bong bóng sảnh; menu thử tua giờ, ép sự kiện | S1 |
| **S3** | Lọ Bi, Chuỗi Quà, Thẻ Tuần, Thẻ Phiêu Lưu mới, Quỹ, gói theo mốc | S2 |
| **S4** | 6 chỗ quảng cáo mới, bảng mốc quảng cáo; gắn Unity IAP và AppLovin MAX vào `IStore` / `IRewardAds`; thử trên máy Android thật | S1 |
| **S5** | Remote Config, sự kiện đo, gói 7 Ngày theo mùa | S4 |
| **S6** | Pass mùa (nhiệm vụ, hai hàng thưởng), nếu cần | S5 |

## 11. Câu cần chốt

**Đã chốt 2026-11-23:** người dùng "ok theo đề xuất hết, làm đi (chưa cần cài sdk)": cả 11 câu theo đề xuất. Làm ở mục 12.

1. **Bán bi và Rương Tướng** (đổi chốt 2026-10-30 "không bán bi, đá tiềm năng, lượt quay máy bi"): đề xuất bán bi và Rương Tướng; đá tiềm năng,
   đá tinh vẫn không bán lẻ, chỉ có trong gói.
2. **Tiền cứng:** đề xuất chưa thêm, bán thẳng bằng tiền thật (mục 4.1).
3. **Rương Tướng:** tỉ lệ và bảo hiểm như 6.3 (10 rương chắc Sử thi, 40 rương chắc Huyền thoại)?
4. **Bảng giá:** $0,99 = 100 bi quy đổi, bi trong gói nhân theo bậc cấp (4.2)?
5. **Trần popup:** 2 mỗi lần vào sảnh, 4 mỗi ngày, D0 chỉ 1 (7.7)?
6. **Gói sau khi thua:** chỉ khi thua ≥ 3 lần liền và không còn cách miễn phí làm ngay (7.3)?
7. **Ưu Đãi Bất Ngờ:** 2 giờ lúc vào game (25–35%), 3 giờ khi vào máy bi lúc bi còn ít (30%); Ưu Đãi Nóng 10 phút sau trận thắng lớn (30%); tối đa 2
   mỗi ngày (6.6, 7.5)?
8. **SDK:** Unity IAP + AppLovin MAX + Firebase (9.5)?
9. **Giờ máy:** chấp nhận gian giờ máy ở bản đầu, hay lấy giờ mạng (cần mạng lúc mở gói hẹn giờ)? Đề xuất lấy giờ mạng khi có, không có mạng
   thì tạm dùng giờ máy nhưng không cho mở gói mới.
10. **Đối tượng 12+, không nhắm trẻ em** (9.7)?
11. **Giá Thẻ Tuần / Thẻ Phiêu Lưu:** $1,99 / $4,99 lúc đầu (Critters $4,99 / $19,99), thử A/B sau khi có số đo?

## 12. Đã làm (2026-11-23, chưa gắn SDK)

### Dữ liệu

- Khối `shop` trong `Assets/02 Data/Json/balance.json` (không tách `shop.json` như mục 9.1: cùng chỗ với khối `home`, khỏi đổi chữ ký
  `GameData.FromJson`), nhập bằng menu `PokiClash/Nhập dữ liệu` vào `BalanceConfig.shop` (`Core/ShopConfig.cs`, có `Validate`).
  - bảng giá gốc `value`, 5 bậc cấp `bands`, thang giá `ladder`;
  - 2 rương (tỉ lệ, số mảnh, bảo hiểm), 25 gói, 8 mẫu ưu đãi động, trần popup `caps`, Lọ Bi, 3 Chuỗi Quà, Quỹ 11 mốc, 2 thẻ, 3 mốc quảng
    cáo, quà ngày, quà trở lại; `adBalls` (bi mỗi lượt quảng cáo), `retryBoost` (Tiếp sức).
  - Mã sản phẩm store suy từ giá: `poki_<xu>` (gói cùng giá dùng chung một mã consumable), Bỏ quảng cáo `poki_noads`.
- `ads.limits` thêm 6 chỗ: `free_balls` 5, `hero_chest` 1, `battle_retry` 3, `win_double` 5, `chest_upgrade` 3, `daily_gift` 1.
- Bản tiếng Anh: 124 chuỗi giao diện (`Loc/en/ui.json`), 43 tên / mô tả gói (`Loc/en/names.json`).

### Lõi (C# thuần, `Assets/01 Script/Core`)

- `Shop.cs`: trạng thái lưu `SaveData.shop` (đọc / ghi trong `SaveCodec`, không đổi số phiên bản: khoá mới, bản lưu cũ đọc ra `null`); mua
  gói (giới hạn đời / ngày / tuần, lần đầu tặng đôi, bi nhân bậc cấp), trao món, gói nhận theo ngày, Thẻ Tuần (cây bi chứa ×1,5), Thẻ Phiêu
  Lưu (quyền lợi cũ + quà ngày + 1 lượt quảng cáo trao ngay), Lọ Bi, Chuỗi Quà, Quỹ, quà ngày, mốc quảng cáo, vé chọn tướng (theo độ hiếm,
  theo hệ), tướng tuần, nhóm người chơi, thang giá, nhãn giá trị ×N.
- `HeroChests.cs`: mở Rương Tướng (bảo hiểm Sử thi / Huyền thoại theo từng loại rương, ưu tiên tướng đang có, tướng tuần ×3), bảng tỉ lệ công khai.
- `Offers.cs`: hàng popup lúc vào game, sự kiện (thua, thắng boss, hết bi, bi ít, jackpot, rương Huyền thoại), quét mốc (tướng mới, đảo
  mới, sắp lên sao, cấp 10 / 15), dựng ưu đãi động theo nhu cầu, trần và chặn, "Hôm nay không hiện nữa", cách miễn phí trước khi bán.
- `Trees.cs`: sức chứa cây bi nhân Thẻ Tuần. `AdGate.cs`: hằng 6 chỗ đặt mới. `Pachinko.cs`: thêm loại thưởng `Crystal`, `HeroChest`,
  `GoldChest`, `Ticket`, `Perk`.
- Test `Tests/ShopTests.cs` (19 test).

### App và giao diện

- `App/Shop/ShopService.cs`: mua qua `Store.Pay` (bản dev: cửa hàng giả lập mua ngay), trao, hiện quà bằng hộp mở rương có sẵn
  (`ChestBox`), mở Rương Tướng, dùng vé, quảng cáo của cửa hàng; `ShopLog` ghi `Logs/shop.csv` (chỗ gắn Firebase sau).
- `App/Shop/OfferHost.cs` (gắn trong `App.prefab`): hàng popup, chỉ hiện khi màn rảnh; "vào game mới" khi quay lại sau 30 phút.
- `App/Shop/ShopSheet.cs` (`Dialogs/CuaHang`): một tờ cho cửa hàng 4 tab và mọi popup, trang con Quỹ, Chuỗi Quà, chọn tướng bằng vé.
  Cửa hàng là hộp thoại toàn tờ, không phải scene mới (mở được từ sảnh, máy bi, mọi màn).
- `App/Shop/PackCell.cs` (`Items/OGoi`): ô gói. `App/Shop/HubShop.cs` (nhóm `cua_hang_san` trong `Screens/Hub`): nút Lọ Bi, 3 bong bóng
  ưu đãi mép trái. Nút Cửa hàng là nút sẵn có ở hàng nút đáy sảnh (phiên làm hàng nút đáy dựng), nay mở `ShopSheet`, chấm đỏ khi có quà chờ nhận.
- Nối vào màn:
  - trận: báo thua / thắng; thua từ lần 2 liền ghi cách miễn phí làm ngay được và nút quảng cáo **Tiếp sức +15%** (đánh lại, `BattleArgs.boost`);
    thắng có nút **Nhận ×2** (quảng cáo); nút nằm ở hàng riêng `hang_qc` của `Dialogs/TranKetQua`;
  - máy bi: mỗi bi thả bỏ vào Lọ Bi; bấm thả khi thiếu bi cho cược thì tự hạ cược, hết hẳn bi thì popup Hết bi; jackpot báo Ưu Đãi Nóng;
    vào máy lúc bi còn ít có thể bật Ưu Đãi Bất Ngờ 3 giờ;
  - **nâng rương** (`chest_upgrade`): khác mục 8.1, màn mở rương tung thưởng trước khi diễn nên không đổi bậc giữa chừng được; thay bằng
    hộp hỏi "xem quảng cáo nâng 1 Rương Gỗ thành Bạc?" một lần mỗi lần vào máy, khi nhóm sắp mở có Rương Gỗ;
  - Sổ tay: mục "Gói hỗ trợ" mua qua `ShopService` (Thẻ Phiêu Lưu, Bỏ quảng cáo nhận cả quà của gói).
- Menu: `PokiClash/Prefab/Khác/Hộp thoại và màn∕Cửa hàng: dựng hết` (`Editor/ShopMenu.cs`); thử (đang Play): `PokiClash/Thử/Cửa hàng: mở`, `popup Hết bi`,
  `popup Ưu Đãi Bất Ngờ`, `popup Gói Tiếp Sức`, `popup Quà Nhập Môn`, `popup Lọ Bi đầy`, `popup Chuỗi Quà`, `popup Quà hôm nay`,
  `vào game lại`, `đặt lại trạng thái cửa hàng`, `tour chụp` (ảnh ở `Temp/PokiShots/cua_hang/`).

### Kiểm (2026-11-23)

- EditMode cả bộ 175 test: 172 đạt. 3 trượt không do cửa hàng: `AtomikKeysTests.ImportedPoseMatchesJson` (phiên nén .atomik đang sửa test),
  `PrefabOnlyTests` (3 chỗ cũ: NumberTicker, UiMotion, HomeScene gridMat), `LocTests` chữ in hoa trên nút prefab mới (đã thêm bản dịch).
  Chạy lại 7 bộ liên quan (Shop, Loc, Ads, Trees, Save, Tutorial, Pachinko): 66/66 đạt.
- Tour chụp `PokiClash/Thử/Cửa hàng: tour chụp` (13 ảnh, `Temp/PokiShots/cua_hang/`): 4 tab, mua Túi bi (cửa hàng giả lập), mở 10 Rương Tướng,
  popup Hết bi, Lọ Bi, Chuỗi Quà, Ưu Đãi Bất Ngờ, Gói Tiếp Sức, Quà Nhập Môn, giới thiệu Quỹ. Vào sảnh với bản lưu thật thì hàng popup lúc
  vào game bật "quà hôm nay" và giới thiệu Thẻ Tuần (cấp 11).
- Bộ dựng phải gán tạm `Theme.Init(UiAssets)` khi dựng trong Editor: sprite giấy mã hoá (`Sketch.*`) và material `Theme.Kit` chỉ có khi game chạy.
- Phông không có ký tự ô tích: nút "Hôm nay không hiện nữa" đổi sang xanh, chữ "Đã tắt tới mai" khi đã tích.
- Thử trong game thật (menu `PokiClash/Thử/Cửa hàng: trận (Nhận ×2, Tiếp sức), máy bi (hạ cược, Hết bi, nâng rương)`, ảnh
  `Temp/PokiShots/cua_hang_tran/`): Nhận ×2 ra nút và quảng cáo giả lập; thua 2 lần liền ra dòng cách làm ngay và nút Tiếp sức, vào lại trận
  máu 660 → 759, công 198 → 228 (+15%); máy bi tự hạ cược ×5 → ×2, hết bi bật popup Hết bi; rương gỗ hỏi "Nâng rương?" rồi ra rương bạc.
  Sửa kèm: dòng "Làm ngay được" lấy theo đội vừa đánh (`Offers.FreeFix(s, d, team)`), trước lấy đội trong bản lưu.

### Chưa làm

- SDK (Unity IAP, AppLovin MAX, Firebase, Remote Config): người dùng dặn chưa cài. Đã có chỗ gắn: `Store.Current`, `Store.PriceText`,
  `Ads.Current`, `ShopLog.Sink`.
- Gói 7 Ngày theo mùa, Pass mùa (S5, S6), giờ mạng chống chỉnh giờ máy (câu 9).
- Ảnh riêng (nền popup, Lọ Bi, vé, sticker): đang dùng icon và kit có sẵn. Popup ưu đãi vẫn là tờ giấy cũ (ShopSheet + Items/OGoi).

## 13. Trứng capsule, màn cửa hàng mới, nở trứng, mở khoá tướng (2026-11-23)

Người dùng: "bố cục shop nhìn xấu quá, học tập clash of critters, phần rương đổi sang dạng trứng capsule đi để dễ hiểu hơn, có thể thêm
trứng vào phần thưởng để người chơi biết nó nở ra mảnh tướng, chia trứng theo tier thường hiếm... như những tướng trong game, ngoài ra khi
unlock được 1 tướng làm phần hoạt ảnh như trong brawl star khi unlock tướng". Sau đó: "làm tướng xoay xoay liên tục rồi hiện ra play
animation gì đó (ulti hoặc appear rồi idle), nhìn hình hơi vỡ, background bỏ mấy cái icon đi để nền trơn thôi".

### Trứng thay Rương Tướng

- 5 bậc trùng độ hiếm tướng: Trứng Thường, Khá, Hiếm, Sử Thi, Huyền Thoại (`shop.eggs`, `Core/Eggs.cs` thay `HeroChests.cs`). Trứng bậc nào
  nở 12–16 mảnh của **một tướng đúng bậc đó** (trong bậc: 60% tướng đang có / đang góp mảnh, tướng tuần ×3). Bỏ bảo hiểm (bậc đã cố định).
- Nở lên một bậc (như Starr Drop đổi màu): Thường 12%, Khá 10%, Hiếm 8%, Sử Thi 5%. Ghi trong bảng tỉ lệ công khai.
- Món gói `{ k: "egg", r: bậc }`, túi `egg_0..egg_4`. Bản lưu cũ: Rương Tướng → Trứng Khá, Rương Tướng Vàng → Trứng Sử Thi (`Shop.Norm`, đọc
  túi trong `Shop.Read`); ưu đãi đang mở còn món cũ cũng trao thành trứng.
- Giá trị (bi quy đổi): 110 / 140 / 210 / 350 / 630. Gói (mục Trứng): Trứng Hiếm hôm nay $0,99 (1/ngày), Trứng Khá $0,99, Hiếm $1,49,
  Sử Thi $2,49, Huyền Thoại $4,49, 10 Hiếm $9,99, 10 Sử Thi $19,99, 10 Huyền Thoại $39,99; Trứng Thường miễn phí qua quảng cáo
  (`free_egg`, 1/ngày, thay `hero_chest`). Mua gói trứng thì nở luôn.
- Trứng trong phần thưởng: Quà Nhập Môn (ngày 1 Trứng Hiếm, ngày 3 Trứng Sử Thi), Gói Khởi Hành, Gói Tướng Tuần (4 Trứng Hiếm), Thẻ Phiêu Lưu
  (1 Trứng Sử Thi), Chuỗi Quà, Quỹ, mốc quảng cáo, Quà Trở Lại, ưu đãi động (Ưu Đãi Bất Ngờ / Nóng / Đồng Hành). Ô thưởng trứng ghi
  "nở mảnh" để người chơi biết trứng ra mảnh tướng.
- **Rương máy bi rơi trứng** (người dùng 2026-11-23: "cho rương máy bi rơi trứng đi"): dòng mảnh của rương bạc (4,6%, 1–2 mảnh) thành
  1 Trứng Thường, của rương vàng (8,8%, 2–4 mảnh) thành 1 Trứng Khá; số nhân theo cược như mọi món. Bảng rương có loại `egg` + `tier`
  (`ChestRoll.tier`, `Pachinko.RollChest`), trứng vào túi, màn mở rương nhóm hiện ô trứng (xếp sau đá tiến hóa), máy bi nhắc "Trứng vào
  túi: nở ở Cửa hàng". Rương Đền Huy Hiệu dùng chung bảng nên cũng rơi trứng. Bảng tỉ lệ máy bi ghi tên trứng (sửa kèm: dòng đá tiến
  hóa trước ghi nhầm "mảnh tướng"). Golden `pachinko.json` tính lại bằng menu "Tính lại golden theo tướng mẫu"; test
  `RuongBacVang_RoiTrung_VaoTui`.
- Hình: `Assets/03 Art/Shop/trung_0..4.png` (gen GPT 2.6 qua Magnific theo nét vật phẩm của game, `ArtGen/Shop/trung/`, cắt bằng
  `ArtGen/Shop/cat_trung.py`, đo đường nối vòm / thân cho hoạt ảnh nở); 6 hình gói bi `goi_bi_1..6` (nắm, túi, rổ, thùng, rương, xe;
  `ArtGen/Shop/bi/`, `cat_luoi.py`). Tên 6 gói bi đổi cho khớp hình: Nắm, Túi, Rổ, Thùng, Rương, Xe bi.

### Màn cửa hàng toàn màn hình (học bố cục Critters)

- `App/Shop/ShopPage.cs` (`Dialogs/CuaHangLon`, biến thể tờ giấy gốc trải kín màn, cờ `ModalSheet.flat`: trượt vào không nghiêng). Một
  trang cuộn dài, hàng 5 nút mục nhảy tới mục (chấm đỏ khi có quà chờ), số bi góc trên:
  Ưu đãi (thẻ ngang to) · Quà miễn phí (quà hôm nay, quà thẻ / gói ngày, bi và trứng xem quảng cáo, mốc quảng cáo) · Trứng tướng (túi trứng chờ
  nở, lưới 3 cột theo bậc, gói ×10 chồng 3 quả, gói tướng tuần, vé, tỉ lệ) · Bi (lưới 3 cột 6 gói có hình riêng, nhãn "Lần đầu ×2") ·
  Đặc quyền (lưới 2 cột: Thẻ Tuần, Thẻ Phiêu Lưu, Quỹ, Bỏ quảng cáo; Khôi phục giao dịch).
- Ô: `Items/MucCuaHang` (ruy băng đỏ máy bi + đồng hồ), `Items/LuoiCuaHang`, `Items/OCuaHang` (ô đứng: nền giấy pha màu, hình to, số,
  nhãn góc, sticker ×N, nút giá), `Items/TheCuaHang` (thẻ ngang: hình / mặt tướng, tên, mô tả, hàng ô thưởng, đồng hồ, sticker giá trị, hai
  nút; thẻ gọn khi không có món). Mỗi MonoBehaviour một file (Unity chỉ nhận lớp trùng tên file khi gắn vào prefab).
- `ShopSheet.OpenShop` mở màn mới; tờ giấy cũ chỉ còn lo popup và trang con (Quỹ, Chuỗi Quà, vé).

### Màn nở trứng

- `App/Shop/EggHatchView.cs` (`Items/NoTrung`, `UiKit.eggHatch`, canvas riêng): trứng rơi vào, tia phẳng màu bậc xoay, lắc 3 nhịp mạnh dần
  (nở lên bậc: chớp, đổi trứng, chữ NÂNG BẬC!), vòm bật lên theo đường nối, thân rơi, chớp + vòng toả + sao bắn, ô mảnh tướng hiện ra theo
  nhịp kéo dọc 0,3 × 1,63 → ép 1,1 × 0,94 (học Brawl Stars), tên và bậc; chạm sang quả kế. Nhiều quả: chạy nhanh, bảng tổng, nút Nhận, Bỏ qua.
- Nền tối alpha 0,985 bằng ô trắng thường (sprite giấy mã hoá kênh làm sai alpha). Màn chỉ dùng chân dung (luôn có trong bản cài).

### Màn mở khoá tướng (học nhịp Brawl Stars)

- Mổ Brawl Stars 70.877 (`D:\Ripper\BrawlStar`, báo cáo `Analysis\unlock\BAO_CAO.md`): clip `gatcha_screen_hero_drop` 60 khung/giây, khoá
  tuyến tính, nảy nhờ khoá vượt rồi về; bậc cao chỉ chồng thêm lớp, vũ đạo giống nhau.
- `App/Shop/HeroUnlockView.cs` (`Items/MoKhoaTuong`, `UiKit.heroUnlock`): tụ lực 1,2 s (nền mực xanh thẫm, vệt tốc độ lặp 0,18 s, tướng là
  bóng tối quay quanh trục dọc 3 vòng nhanh dần, phóng 0,1 → 1, sao tụ vào) → lấy đà 2 khung (co 0,83) → bùng: cắt cứng sang nền trơn màu bậc,
  chớp 5 khung → lộ diện 0,3 s (kéo dọc / ép) và rig diễn clip ra sân (không có thì chiêu cuối nếu không nhảy đè, không nữa thì đánh) rồi
  đứng → tướng lên, bảng tin giấy trượt từ phải vào vượt 20 (TƯỚNG MỚI!, tên, bậc, hệ, danh hiệu, huy hiệu hệ), nút Xem tướng / Tiếp nảy nhắc.
  Lớp chồng theo bậc: Khá đĩa giấy, Hiếm tia xoay, Sử Thi thêm sao lấp lánh và lớp tia thứ hai, Huyền Thoại thêm sao băng.
- Rig qua `AolaSticker` (thêm tham số `maxPx`, màn này 2048 cho nét); dạng chưa có rig (gói tải sau) thì dùng chân dung.
- Bật ở: nở trứng (ngay sau ô mảnh; nở nhiều thì sau bảng tổng), hộp nhận quà của cửa hàng (vé, gói mảnh), kết quả trận (trừ trận hướng dẫn).
- Gói tải sau (GD_Claude/27): rig của tướng ngoài 5 dòng khởi đầu nằm trong gói; màn gọi `AolaActor.Ready(form)` lúc mở để xin gói, pha tụ
  lực tạm dùng bóng chân dung, tới lúc bùng mà gói đã về thì đổi sang rig, chưa về thì chân dung.
- Xem thử: menu `PokiClash/Thử/Khác/Cửa hàng∕Màn mở khoá tướng: xem (ngẫu nhiên)` và theo bậc (Thường … Huyền thoại), `Editor/HeroUnlockMenu.cs`: chưa
  Play thì tự mở Boot, vào Play, tắt màn mở game; chọn ngẫu nhiên tướng đúng bậc có rig, chờ gói tối đa 10 giây; không ghi bản lưu.

### Kiểm

- Tour `PokiClash/Thử/Cửa hàng: tour chụp` (20 ảnh, `Temp/PokiShots/cua_hang/`: 5 mục, mua bi, nở 1 trứng theo pha, nở 3 trứng, popup); tour
  `Cửa hàng: màn mở khoá tướng, 5 bậc` (35 ảnh, `Temp/PokiShots/mo_khoa/`). Cả hai sao lưu và trả bản lưu.
- EditMode 182 test: 181 đạt; trượt 1 bài cũ `PrefabOnlyTests` (NumberTicker, UiMotion, HomeScene, không do phần này). Test mới:
  `Trung_NoDungBac_CoLucLenBac`, `Trung_NoTuTui_RaManh`, `Trung_RuongCuDoiThanhTrung`, `RuongBacVang_RoiTrung_VaoTui`.

