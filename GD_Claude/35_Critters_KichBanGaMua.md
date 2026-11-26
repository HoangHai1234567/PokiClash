# 35. Clash of Critters gạ mua IAP thế nào: mổ kịch bản popup (2026-11-26)

Người dùng dặn 2026-11-26: "Bạn xem kĩ kịch bản clash of critters gợi ý người chơi mua iap như nào, pop up gạ người chơi mua lúc nào, đục
kĩ đào sâu vào logic game."

Tiếp `26_CuaHang_IAP_QuangCao.md` mục 1 (mổ từng loại gói) và `34_KiemTien_KhoPhaDao.md`. File này chỉ nói **khi nào và ở đâu** họ chào bán.

## 0. Đọc được gì, không đọc được gì

| Nguồn | Trạng thái | Cho biết |
|---|---|---|
| Lua và bảng số (điều kiện bật popup, giá, thời hạn) | **mã hoá, có lớp bảo vệ; không giải mã** (memory `coc-config-extraction`) | (không đọc) |
| Prefab UI trong bản AssetRipper (1.021 prefab) | đọc được | mọi màn chào bán, chữ giữ chỗ của dev (tiếng Trung), nút, đồng hồ, nhãn |
| Danh mục tài nguyên (catalog Addressables, 815 màn UI, tên ảnh, tên âm thanh) | đọc được | danh sách đầy đủ loại popup, gói theo sự kiện, bậc giá |
| Quan sát công khai (review store, hướng dẫn, diễn đàn) | tra web | thứ tự, thời điểm, tần suất |
| Chơi thật rồi bấm giờ | **chưa làm được**: máy này không có giả lập Android / adb | (xem mục 6) |

Vì vậy mọi dòng dưới đây ghi rõ **bằng chứng**: `prefab` (thấy trong file), `công khai` (người chơi kể), `suy ra` (tôi nối hai thứ lại).
Chữ trong prefab là chữ giữ chỗ của dev, số tiền và % trên đó không phải giá thật.

Script quét: `D:\Ripper\ClashOfCritters\Analysis\shop\quet_chu_ban_hang.py` (chữ liên quan bán hàng trong mọi prefab),
`in_kich_ban.py` (danh sách màn theo catalog), `dump_prefab.py` (cây một prefab).

## 1. Bản đồ các điểm chào bán (theo prefab)

### 1.1. Chỗ đặt cố định (luôn ở đó)

| Chỗ | Bằng chứng | Chi tiết |
|---|---|---|
| Nút Shop ở màn chính (`pbui_mainview_btn_shop_item`) | prefab | icon **đổi hình xoay vòng** (anim `btn_shop_item_change`), chấm đỏ kèm **số gói**, hạt sáng riêng cho trạng thái "chưa nạp lần đầu" (`first_pay_status`) |
| Nút Heo đất (`btn_piggybank_item`, bản sự kiện là voi) | prefab | nước dâng theo mức đầy, bong bóng "chưa đầy" / "đầy", số bi đang có trong heo; 5 tiếng riêng: xuất hiện, rơi, nghẽn, đầy, đập |
| Cột nút trái / phải trên màn máy bi (`group_btns_left`, `group_btns_right`) | prefab | khung rỗng, code đổ nút vào: nút sự kiện (`btn_activity_main_new`: icon, tên, **đồng hồ**, thanh tiến độ), nút gói |
| Đồng hồ ×2 trên máy bi (`group_double_time`: "x2 04:50") | prefab | cửa sổ nhân đôi có giờ: lúc người chơi muốn dồn bi nhất |
| Thanh bi "10/30, hồi 30 sau 2:30" | prefab | luôn cho thấy bi đang thiếu và bao lâu mới hồi |
| Popup mức cược (`pbui_pinball_multi_popup`) | prefab | "Mọi thưởng ×2. **Bậc kế: có 8.000 bi thì mở**": nhắc giữ nhiều bi mới được cược cao |
| Ô quà miễn phí và ô thẻ tháng trong Shop | prefab (`26` 1.2) | kéo người chơi mở Shop mỗi ngày |

### 1.2. Popup "bốc đồng" (ImpulseGift): bật theo tình huống

Tất cả nằm trong một khung chung `pbui_shop_impulse_switch_view`: **băng chuyền có tab**, mỗi gói đang sống là một tab, lật trái / phải
(anim `pop_left_in/out`, `pop_right_in/out`), nền là ảnh chụp màn hình làm mờ, "chạm chỗ trống để tiếp". Tab mang icon bậc giá
`cheap` / `normal` / `expensive` (và `gvg`): **cùng một lúc bày nhiều bậc giá cho người chơi lật**.

| Popup | Chữ của dev | Bật khi (bằng chứng) |
|---|---|---|
| `popup03` "弹珠补充!" (bổ sung bi) | 3 ô bậc, mỗi ô "tặng thêm" | hết bi (suy ra từ tên; công khai: "hết bi là 3 popup liền") |
| `popup04` "消食丸补充!" (bổ sung thuốc tiêu hoá) | y hệt popup03 | hết lượt cho ăn trong ngày (suy ra): mỗi tài nguyên bị chặn đều có popup bổ sung riêng |
| `HotSpring/…supply_popup`, `GVG/Shop/…supply_popup` | (chỉ có tên trong catalog) | tiếp tế riêng cho Suối nước nóng và cho sự kiện liên minh |
| `popup02` "惊喜特惠" (ưu đãi bất ngờ) | một món lớn, đồng hồ "10:00:00", "siêu giá trị 400%" | không rõ điều kiện; sống 10 giờ |
| `popup_gvg` "海岛夺金胜者礼包" (gói người thắng) | "siêu giá trị 400%", "chỉ mua 1 lần" | **vừa thắng** sự kiện liên minh: bán lúc đang vui |
| `chain` "除臭礼包" (gói chuỗi "khử mùi") | ô đầu "miễn phí", ô sau "$1.99", đồng hồ "04:24:20 nữa hết" | gắn với thử thách người mới "Stinky sắp chạy mất" (1.3) |
| `manual` "饲养礼包" (gói nuôi) | chuỗi, ô đầu miễn phí | liên quan cho ăn (suy ra) |
| `manual_pet` | "tỉ lệ mở ra thú mới **tăng mạnh**", "chỉ mua 1 lần" | có thú mới ra mắt (suy ra từ `26` 1.7) |
| `surprise`, `surprise_new`, `surprise_upgrade` (vòng quay) | "mua 1 lần được 2 lượt quay", "quay $4.99", "vòng quay lên cấp!" | icon riêng ở menu máy bi (`txui_menu_shop_surprise`) |
| `silverbrick_popup` | shop gạch bạc làm mới theo giờ | |

**Gói theo chủ đề sự kiện.** Catalog có một ảnh nền popup riêng cho từng hoạt động: `txui_shop_popup_adventure`, `_farm`, `_fish`, `_run`,
`_run_rafting`, `_trap`, `_treasurehunt`, cộng `_bg_beginnerrush` (tăng tốc người mới), `_manual`, `_manual_pet`; và 5 nền "gói đẩy"
`txui_shop_package_push_bg01..05`. Tức **mỗi sự kiện xoay vòng đều kéo theo một gói bốc đồng mặc đồ của sự kiện đó**.

### 1.3. Kịch bản người mới

| Màn | Chữ của dev | Ý nghĩa |
|---|---|---|
| `Beginner/pbui_beginner_warning_view` | "臭臭即将逃跑!!" (Stinky sắp chạy mất!!), đồng hồ **"04:00"**, ô thưởng, nút "前往推关" (đi vượt ải) | thử thách có giờ cho người mới: tạo gấp gáp ngay những phút đầu, thưởng nếu kịp |
| `Beginner/pbui_beginner_warning_banner` | băng báo đi kèm | |
| `Shop/first/pbui_shop_package_first_choose` "首充特惠!" | 3 cột, "siêu giá trị 200%", "你只能购买一个礼包哦~" (chỉ mua được một gói) | nạp đầu chọn 1 trong 3 bậc |
| `…first_3day` | "siêu giá trị 540%", nhận 3 ngày liền | kéo quay lại ngày 2, 3 |
| `…first_choose_food` "盛宴特惠" | bản đồ ăn của nạp đầu, có đồng hồ | nạp đầu lần hai theo chủ đề khác |
| `Shop/package/pbui_shop_package_open` "启航礼包" (gói khởi hành) | "$4.99", đồng hồ, "hết hàng" | |
| `Opening/pbui_a_view_activity_piggybank_open` | màn "mở sự kiện" riêng cho heo đất | heo đất được giới thiệu như một sự kiện |

### 1.4. Chỗ gợi ý tiêu đồ trả tiền mà không phải popup bán

| Màn | Chữ của dev | Ý nghĩa |
|---|---|---|
| `Pet/Obtain/pbui_pet_upgrade_selected_pop` | "**X sắp tiến hoá rồi!** Dùng hộp ước để lên sao?" | lúc thú gần mốc: mời dùng Wishbox (vật phẩm bán 4–5 USD) |
| `Pet/Recommend/pbui_pet_recommend_pop` "塔塔使用率" | "99% người chơi ưu tiên nuôi", nhãn HOT, "thành hình nhanh / đơn mục tiêu mạnh" | bằng chứng xã hội: hướng người chơi dồn vào vài con, là các con có gói |
| `BattlePass/…tip_pop` | "nhận ngay 60 chìa = lên 3 cấp", "mỗi cây bi +500 tới hết mùa", "còn 10 ngày 10 giờ" | gạ mua pass bằng lợi ích có ngay |
| `BattlePass/…trial_complete_pop` | (màn "xong bản thử") | có **dùng thử pass** rồi mới chào mua |
| `BattlePass/…buy_pop` | "x20 / nhóm, mua 12 nhóm", "mua xong nhận ngay" | bán cấp pass theo nhóm |
| `MainCity/…build_tips_pop` | "xẻng không đủ, lấy bằng vượt ải", nút "đi vượt ải" | thiếu đồ **không bán được** thì chỉ đường chơi |

### 1.5. Chỗ **không** bán

- **Màn thua** (`Battle/result/pbui_a_view_battle_defeat_view`): chỉ có hai mẹo ("phối hệ khắc cho hợp lý", "chỉnh vị trí thú") và ba nút
  "thống kê", "đánh lại", "**đi nâng cấp**". Không có nút mua, không có gói. Thua thì họ dẫn người chơi về màn nuôi thú.
- **Màn thắng** (`…victory_view`, `…boss_victory`): "tiếp tục", "về chương", công tắc tự vượt ải. Không gói.

### 1.6. Sau khi đã nạp

| Màn | Chữ của dev | Ý nghĩa |
|---|---|---|
| `Shop/rebate/pbui_shop_recharge_rebate_pop` "充值返利" | mốc "#1200元", "nhận hoàn tiền" | nạp dồn tới mốc được hoàn |
| `Shop/payment/pbui_shop_checkoutcounter_pop` | "vào shop, chuyển sang thu ngân, **hoàn 5%**" | đẩy sang thanh toán web |
| `Common/pbui_common_shop_tips` | "已变更为快捷购买模式" (đã chuyển sang chế độ mua nhanh) | có chế độ mua nhanh, bớt bước xác nhận |
| `Shop/payment/pbui_shop_club_pop` | "mời bạn vào câu lạc bộ chính thức, hưởng thêm hoàn tiền" | |
| `FriendNew/card/pbui_friend_vip_pop` "VIP邀约" | "đã mở quyền lợi VIP, mời thêm chăm sóc viên riêng, một kèm một" | người chi lớn được người thật chăm |

## 2. Khung kịch bản rút ra (suy ra từ mục 1)

1. **Mỗi thứ bị chặn có một popup bổ sung riêng**, cùng một mẫu 3 bậc + "tặng thêm": bi, thuốc tiêu hoá, tiếp tế suối nước nóng, tiếp tế
   sự kiện liên minh.
2. **Mỗi sự kiện có gói của riêng nó**, mặc ảnh sự kiện, có đồng hồ. Sự kiện xoay 3 ngày một lần nên luôn có gói "mới".
3. **Bán lúc vui, không bán lúc thua**: gói người thắng, gói thú mới; màn thua chỉ dẫn đi nâng cấp.
4. **Băng chuyền nhiều bậc giá**: popup không đứng một mình mà xếp tab rẻ / thường / đắt cho người chơi tự lật.
5. **Miễn phí trước, trả tiền sau**: gói chuỗi và gói nuôi mở bằng ô miễn phí; pass cho dùng thử; nạp đầu 3 ngày phát dần.
6. **Đồng hồ ở mọi nơi**: 4 phút (thử thách người mới), khoảng 4 giờ (chuỗi, khởi hành), 10 giờ (ưu đãi bất ngờ, gói 7 ngày), cả mùa (pass).
7. **Nấc thang sau khi nạp**: hoàn tiền theo mốc, thu ngân web 5%, mua nhanh, câu lạc bộ, VIP.

## 3. Thời điểm và tần suất theo quan sát công khai

Tra web 2026-11-26. Mức tin: **chắc** (store, ghi chú bản cập nhật, AppMagic), **cộng đồng** (review, hướng dẫn, diễn đàn). Không đọc
trực tiếp được Reddit, Discord, trang review Google Play, bình luận YouTube (chỉ có đoạn trích của máy tìm kiếm). Nguồn hay nhất là trang
hướng dẫn Hàn [ttugaguide](https://ttugaguide.kr/index.php/guide/2197) (bảng gói, lịch xoay) và review App Store nhiều nước.

### 3.1. Popup bật khi nào

| Lúc | Bật gì | Lặp lại | Nguồn |
|---|---|---|---|
| **Mở game** | 2 tới khoảng 5 popup gói nối nhau, phải đóng từng cái | mỗi lần mở, kể cả mở 3–4 lần một ngày; "vắng một lúc quay lại là mấy cửa sổ nối đuôi" | review App Store [Mỹ](https://apps.apple.com/us/app/clash-of-critters/id6741567125), [Anh](https://apps.apple.com/gb/app/clash-of-critters/id6741567125); [check-app.de](https://www.check-app.de/2026/08/20/clash-of-critters-update-0-46-1-neuer-tatari-horde-invasion-saisons-und-grosse-cozy-farm-aenderungen/) (cộng đồng) |
| **Vào màn máy bi** | popup shop; nút mua nằm đúng chỗ nút thả bi; có người gặp 3 lần mời mua bi liền | mỗi lần vào; cùng một gói hiện lại sau "vài giờ" | review Google Play, [App Store Nhật](https://apps.apple.com/jp/app/id6741567125?see-all=reviews&platform=iphone) (cộng đồng) |
| **Hết bi** | gói bổ sung bi kèm ưu đãi; khoảng 20 giây popup dồn dập mới làm được việc khác | đóng rồi, bi hồi lại rồi hết lần nữa thì bật lại | [friendlygamedev](https://friendlygamedev.com/game-reviews/clash-of-critters/) (chắc); review Úc, Anh (cộng đồng) |
| **Đánh xong khoảng 3 trận** | popup nạp; nút X sát đáy màn hình | | [appreview.jp](https://appreview.jp/app/7feb36d6ab1e249bccc1a41f4ddfd335) (cộng đồng) |
| **Chuyển màn ngay sau khi từ chối** | chính gói vừa từ chối | | appreview.jp (cộng đồng) |
| **Mỗi lần dùng bi, dùng vật phẩm** | popup | | appreview.jp (cộng đồng) |
| **Qua chương** | "gói qua chương": 4,99 USD = 2.000 bi; 9,99 USD = 4.000 bi | | ttugaguide (cộng đồng; không ghi chương nào) |
| **Sự kiện 3 ngày bắt đầu** | gói sự kiện 5 bậc (xem 3.3) | sống đúng 3 ngày của sự kiện | ttugaguide; review Nhật, Đức (cộng đồng) |
| **Ra thú mới** (2 tuần một lần) | gói thú mới từ 14,99 USD, viên gacha 16% ra thú mới | | ttugaguide (cộng đồng) |

Tần suất tổng theo người chơi: "mỗi 15 phút một loạt gói" (Malaysia), "mỗi phút đều ép mua" (Philippines), "popup dày như vảy nến" (TapTap).

**Không nguồn công khai nào** kể về popup bật vì: thua ải / thua boss nhiều lần, vừa bắt được thú hiếm, lên cấp / lên sao, mở tính năng
mới, thiếu N điểm tới mốc sự kiện, tụt hạng. Điều này khớp với prefab: **màn thua của họ không có gói** (1.5).

### 3.2. Dòng thời gian người mới

- Bản Trung: mở tới **ải 1-10** thì nạp đầu, gói 7 ngày, thẻ tháng cùng lộ ra ([TapTap](https://www.taptap.cn/review/50324565), cộng đồng).
- AppMagic: "ngay từ các phiên đầu, game mở dần từng lớp kiếm tiền": thẻ tuần / tháng, heo đất, gói chuỗi, ưu đãi hẹn giờ
  ([AppMagic](https://appmagic.rocks/blog/clash-of-critters-plinko-coin-looter/?hl=en), chắc là có lớp, không có mốc).
- Lúc ra mắt có "sprinting pack" hẹn giờ để kéo người chưa nạp mua nhiều gói nhỏ (PocketGamer.biz, chắc). Khớp nền `beginnerrush` và thử
  thách 4 phút trong prefab (1.3).
- Người chơi: bi được cho đủ chơi **vài giờ** (4 giờ liền tới cấp 89, ải 4-29, không nạp); hết bi tích trữ thì "tiến độ sụp", sau đó mỗi
  lần chỉ chơi được khoảng 20 phút là cần nạp (review New Zealand, Malaysia, Canada; cộng đồng).
- Thứ tự cộng đồng Hàn khuyên mua, cũng là thứ tự gói hiện ra: gói tân thủ + gói qua chương → pass + gói 7 ngày → gói sự kiện → heo đất,
  gói đặc huệ.
- Không tìm được: phút chính xác của popup đầu, heo đất và quỹ mở ở cấp nào.

### 3.3. Lịch xoay và thang giá

- **Ba gói xoay vòng theo lịch cố định**: heo đất → vòng quay → gói cho ăn, **mỗi gói mở 3 ngày, lặp mỗi 9 ngày**
  ([lịch ttugaguide](https://ttugaguide.kr/index.php/calendar), cộng đồng). Song song là sự kiện 3 ngày, mỗi sự kiện có gói riêng. Thêm
  "ưu đãi tiệc lớn" 3 ngày một lần, mở 1 ngày. Tức lúc nào cũng có ít nhất hai gói "chỉ còn N ngày".
- **Gói sự kiện 5 bậc** (đều kèm tiền sự kiện): 1,99 USD = 700 bi; 2,99 = 1.000 bi; 9,99 = 2.800 bi + **nhân đôi kinh nghiệm máy bi 10
  phút**; 19,99 = 4.000 bi + 2 hộp cơm; 29,99 = 5.100 bi + nhân đôi 40 phút.
- **Gói đặc huệ 7 bậc** (bi / hộp ước / viên gacha): 1,99 USD = 450 / 2 / 5; 2,99 = 700 / 2 / 5; 4,99 = 1.200 / 2 / 7; 9,99 = 2.200 / 5 /
  12; 14,99 = 3.250 / 6 / 24; 39,99 = 6.500 / 15 / 60; 99,99 = 17.500 / 30 / 100.
- **Giá leo theo hành vi**: gói đặc huệ "mỗi lần mua thì giá tăng, không mua thì hạ dần"; chăm sóc khách hàng trả lời rằng "giá gói hiện
  ngẫu nhiên"; có người kể một số gói biến mất tuỳ số tiền đã nạp (ttugaguide, bình luận YouTube; cộng đồng). Khớp ba icon rẻ / thường /
  đắt trong prefab.
- **Nạp đầu 3 bậc chọn 1**: 4,99 / 9,99 / 19,99 USD = 1.000 / 3.000 / 6.400 bi + 20 / 30 / 75 viên + khung + 1 thú; chỉ mua được một, khung
  "chỉ một lần" đẩy người chơi lên bậc đắt (AppMagic, chắc).
- **Heo đất** 4,99 USD = 2.500 bi (khoảng 2,8 lần giá bi thường). **Vòng quay** 4 tầng: lượt đầu miễn phí chắc trúng ô xanh, tầng 2–4 giá
  4,99 / 9,99 / 14,99 USD mỗi lượt.
- **Quà miễn phí hằng ngày** (60 bi) đặt **dưới cùng** mục gói nổi bật, phải cuộn qua mọi gói trả tiền
  ([games.gg](https://games.gg/clash-of-critters/guides/clash-of-critters-how-to-farm-free-pinballs-fast/), cộng đồng).
- Có đủ gem thì giá USD trên nút đổi thành biểu tượng gem (từ 1/2026).

### 3.4. Sau khi nạp, và phản ứng của nhà phát hành

- Người đã nạp vẫn bị popup **cùng tần suất** (appreview.jp, cộng đồng).
- Không có công tắc tắt popup hay "hôm nay không hiện nữa": người chơi xin từ tháng 6 tới tháng 11. Bản 0.46.1 (27/8) chỉ ghi "tối ưu
  logic popup"; ngày 15/11 nhà phát triển còn trả lời "giới hạn theo ngày là hợp lý, đang xem lại giao diện" (chắc).
- Bản 7/10 ghi "cải thiện hiển thị gói ở Mall và máy bi": màn máy bi là chỗ đặt gói chính thức (chắc).
- Hoàn tiền thì gem bị trừ thành số âm, phải nạp bù mới chơi tiếp (review Singapore, Hàn; cộng đồng).
- Mời VIP có trong prefab (1.6) nhưng không nguồn công khai nào nhắc: có thể chỉ hiện với người chi rất lớn, hoặc chỉ ở bản Trung.

### 3.5. Chỗ prefab và quan sát công khai lệch nhau

| | Prefab | Công khai | Kết luận |
|---|---|---|---|
| Ưu đãi bất ngờ "10:00:00" | có đồng hồ 10 giờ | không ai nhắc con số 10 giờ | chưa xác nhận thời hạn thật |
| Thua thì bán | màn thua không có gói | không ai kể popup sau khi thua | **họ không bán ở màn thua** (hai nguồn khớp) |
| "Xong 3 trận ra popup" | không có prefab riêng | 1 nguồn Nhật | có thể là popup chung bật theo số trận; cần bấm giờ |
| VIP | có prefab | không ai nhắc | chưa rõ |

## 4. So với PokiClash đang có

Của mình: `Core/Offers.cs`, `Core/Shop.cs`, kế hoạch `26` mục 6–7.

| Cách của Critters | PokiClash | Nhận xét |
|---|---|---|
| Mở game: 2–5 popup, không trần, không tắt được | tối đa 2 mỗi lần vào, 4 mỗi ngày, ô "Hôm nay không hiện nữa" | **giữ của mình.** Đây là chỗ họ bị chê nặng nhất suốt 6 tháng và chưa sửa |
| Vào máy bi là popup; nút mua ở chỗ nút thả | chỉ có Ưu Đãi Bất Ngờ 30% khi bi còn ít | không chép popup; nhưng **chưa có chỗ đặt cố định trên màn máy bi** (5.1) |
| Hết bi: 3 bậc bổ sung + ưu đãi, bật lại mỗi lần hết | popup Hết bi 3 bậc + quảng cáo, 20 phút một lần | đã có, lành hơn |
| Mỗi tài nguyên bị chặn có popup bổ sung riêng | chỉ có bi | **thiếu**: đá tiến hóa là thứ người chơi kẹt nhiều nhất (`33` mục 2.5) |
| Mỗi sự kiện 3 ngày có gói 5 bậc riêng | sự kiện Bến Lữ Khách chưa có gói | **thiếu** |
| Lịch xoay 9 ngày: heo đất → vòng quay → gói cho ăn | Lọ Bi luôn mở; Chuỗi Quà 14 ngày một lần | **thiếu nhịp**: của mình không có gì "chỉ còn 3 ngày" đều đặn |
| Băng chuyền rẻ / thường / đắt | mỗi lần một gói, một giá | **thiếu**: không có neo giá |
| Giá leo khi mua, hạ khi không mua; hiện "ngẫu nhiên" | thang giá: mua lên một bậc, 7 ngày không mua xuống một bậc | đã có, và minh bạch hơn. Không chép phần "ngẫu nhiên" |
| Nạp đầu 3 bậc chọn 1, kèm thú | Quà Nhập Môn 0,99 + Gói Khởi Hành 4,99 | thêm (`34` mục 3) |
| Gói qua chương | Gói Đảo Mới, Ưu Đãi Nóng sau boss | gần đủ; thêm gói qua mốc tướng (`34` mục 2.4) |
| Bán lúc thắng, không bán lúc thua | Ưu Đãi Nóng lúc thắng; Gói Tiếp Sức sau 3 lần thua | mình bán cả lúc thua. Với vòng "thiếu cấp → mua bi" của `34` thì nên giữ, nhưng học họ: **lối miễn phí và nút nâng cấp luôn đứng trước gói** |
| Thử thách người mới có giờ (4 phút) + gói tăng tốc | không có | **thiếu** |
| "X sắp tiến hoá, dùng hộp ước?" | Gói Sắp Lên Sao (80% mảnh) | đã có |
| Bảng "99% người chơi ưu tiên nuôi" | không có | thêm vào quảng cáo gói tướng (`34` mục 2.5) |
| "Bậc cược kế: có 8.000 bi thì mở" | mức cược mở ở 150 / 300 / 700 bi, không nhắc | **thiếu** lời nhắc, và bậc cược của mình dừng quá sớm |
| Bán "nhân đôi kinh nghiệm máy bi 10 / 40 phút" trong gói | không có | **thiếu**, và rất hợp vòng bi → cấp của `34` |
| Quà miễn phí chôn dưới cùng shop | quà ngày ở mục riêng, có chấm đỏ | giữ của mình |
| Hoàn tiền theo mốc nạp, thu ngân web 5%, VIP | không làm (đã chốt `26`) | giữ |

## 5. Đề xuất cho PokiClash

### 5.1. Chép (theo thứ tự nên làm)

| # | Việc | Chi tiết | Vì sao |
|---|---|---|---|
| 1 | **Một ô gói cố định trên màn máy bi** (không phải popup) | cạnh số bi: gói hợp nhất lúc đó (sắp hết bi → bổ sung; đang kẹt cấp → gói bi vừa đủ; có ưu đãi đang sống → ưu đãi đó), kèm đồng hồ nếu có | họ bán nhiều nhất ở màn máy bi; mình hiện không có gì ở đó. Ô cố định không vi phạm trần popup |
| 2 | **Vật phẩm "×2 EXP máy bi N phút"** | bán trong gói bi từ 9,99 USD (10 phút) và 29,99 USD (40 phút); cũng làm phần thưởng sự kiện | đang nhân đôi thì người chơi muốn thả thật nhiều bi ngay: tự nó tạo lý do mua bi. Khớp vòng bi → cấp → vượt ải |
| 3 | **Gói theo sự kiện của Bến Lữ Khách** | mỗi sự kiện (Đêm Bài, Vòng Xoay, Hội Máy Quả, Lễ Hội Đua) một gói 3 bậc 1,99 / 4,99 / 9,99 USD: bi + mảnh tướng khách mời + điểm đường thưởng; sống đúng số ngày sự kiện | họ thu đều nhờ gói "3 ngày"; mình đã có lịch sự kiện 14 ngày sẵn |
| 4 | **Lịch xoay 9 ngày cho ba gói hẹn giờ** | Lọ Bi (3 ngày) → Chuỗi Quà (3 ngày) → Gói Tướng Tuần (3 ngày), rồi lặp | lúc nào cũng có đúng một gói "còn N ngày"; Lọ Bi không mở suốt cũng tự giải quyết việc đập liên tục (`33` việc 15) |
| 5 | **Ba bậc cạnh nhau** cho Ưu Đãi Bất Ngờ và Gói Tiếp Sức | rẻ / vừa / đắt (bậc thang hiện tại −1, 0, +1), bậc giữa làm nổi | neo giá; họ dùng cho mọi popup bốc đồng |
| 6 | **Bổ sung đá tiến hóa** | khi tướng trong đội tới mốc tiến hóa, đủ cấp, thiếu đá: nút "Bổ sung" ngay trên màn tướng, 3 bậc (5 / 15 / 40 đá) | mỗi thứ bị chặn một popup bổ sung; đá là chỗ kẹt lớn nhất của mình |
| 7 | **Nhắc bậc cược + thêm bậc cao** | "Bậc kế ×20: có 1.500 bi thì mở"; thêm ×20 (1.500 bi), ×50 (4.000 bi) | cho người chơi lý do giữ nhiều bi, và gói bi lớn có chỗ dùng |
| 8 | **Thử thách người mới có giờ** | sau chuỗi hướng dẫn: "Qua ải 10 của một đảo trong 15 phút": thưởng trứng Hiếm; hết giờ hoặc xong thì mở Chuỗi Quà đầu tiên (ô đầu miễn phí) | gấp gáp ngay phiên đầu mà không bán gì ở phiên đầu; dẫn tự nhiên vào gói chuỗi |
| 9 | Nạp đầu 3 bậc kèm tướng, gói qua mốc, bảng tỉ lệ dùng tướng | xem `34` mục 2–3 | |

### 5.2. Không chép

- Không trần, không nút tắt (giữ trần và ô "Hôm nay không hiện nữa" của mình).
- Nút mua đặt ở chỗ nút chơi; popup bật lại ngay sau khi từ chối; popup mỗi lần thả bi.
- Giá hiện "ngẫu nhiên" theo người (rủi ro pháp lý, `26` mục 9.7); mình giữ thang giá có luật.
- Chôn quà miễn phí dưới đáy shop.
- Trừ âm tiền khi hoàn tiền, thu ngân web hoàn 5%, vòng quay trả tiền.

### 5.3. Kịch bản đề xuất cho một người chơi mới (gộp `26` mục 7 với các việc trên)

| Lúc | Hiện gì | Kiểu |
|---|---|---|
| Phiên 1, trong hướng dẫn | không bán gì | |
| Hết chuỗi hướng dẫn | thử thách có giờ "qua ải 10 trong 15 phút" (việc 8) | băng báo, không bán |
| Xong hoặc hết giờ thử thách | Chuỗi Quà đầu tiên, ô 1 miễn phí | popup 1 lần |
| Phiên 2 | Quà Nhập Môn 0,99 USD (72 giờ) | popup 1 lần, rồi thành bong bóng |
| Hết bi lần đầu | chỉ quảng cáo + cây bi (đã có) | |
| Hết bi lần sau | quảng cáo, rồi 3 bậc bổ sung | popup, 20 phút một lần |
| Ngày 2 | nạp đầu 3 bậc kèm tướng (thay Gói Khởi Hành) | popup 1 lần |
| Cấp 8, mở đảo Casino | gói sự kiện đang chạy (việc 3) | ô cố định trên đảo, không popup |
| Cấp 10 | giới thiệu Thẻ Tuần | popup 1 lần |
| Qua mốc 3 của một đảo | gói tướng mốc 6 (`34`) | popup 1 lần, rồi bong bóng |
| Kẹt cấp (thua 2 lần liền một ải) | "thiếu X cấp ≈ Y bi": chờ / quảng cáo / gói bi vừa đủ, 3 bậc | trên màn thua, sau lối miễn phí |
| Tướng tới mốc tiến hóa thiếu đá | Bổ sung đá (việc 6) | nút trên màn tướng |
| Mọi lúc trên máy bi | ô gói cố định (việc 1) | không popup |
| Mỗi 3 ngày | gói xoay vòng kế tiếp (việc 4) | bong bóng + 1 popup ngày đầu |

Trần giữ như `26` mục 7.7: tối đa 2 popup bán mỗi lần vào, 4 mỗi ngày, ngày đầu 1.

## 6. Muốn chắc hơn: bấm giờ trong game thật

Điều kiện bật chính xác chỉ có hai cách biết: giải mã (không làm) hoặc **chơi và ghi lại**. Nếu người dùng quay màn hình một tài khoản mới
(2 giờ đầu, rồi mỗi lần mở game trong 3 ngày), tôi dựng được dòng thời gian từng popup: phút thứ mấy, sau hành động nào, giá, đồng hồ,
đóng rồi bao lâu bật lại. Chỉ cần file video, không cần ghi chú.
