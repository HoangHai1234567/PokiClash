# Máy bi (gacha kiểu pachinko)

Tóm từ research đã có: `ClashMaster/reports/Máy bi Critters và ClashMaster.md` và `ClashMaster/research_notes/Máy bi Critters và ClashMaster/`. Phần cuối là áp vào game này.

Số đo từ bản đục 0.50.1 (hình học bàn, vật lý bi, hiệu ứng, âm thanh, rung theo từng ô): `D:\CrittersRipper\analysis\PINBALL_REPORT.md`, sơ đồ `table_01.png`. Phần đã áp vào máy bi của game (két vàng, vật lý và hiệu ứng chép, phản hồi chia bậc): change `update-pachinko-feel`, mục "Vật lý chép" và "Hiệu ứng chép" ở cuối file này.

## Clash of Critters làm gì

- Máy bi nằm **ngoài trận**, theo dòng Coin Master (máy slot xã hội). Thả bi, bi dội qua đinh rồi rơi vào ô.
- Mặt máy và tỉ lệ (game tự hiện khi chạm vào máy): khoảng 95 % bi rơi vào ô candy, 3,3 % ô thẻ, 1,7 % ô jackpot (cướp hoặc thăm trại người khác). Hai nấm bật trên cùng đổ thanh; thanh đầy cho một sinh vật ngẫu nhiên hoặc một khiên.
- Candy **tự nâng cấp cả đội**. Trận thủ thành tự đánh, chỉ là cửa kiểm tra đội đã đủ mạnh chưa.
- Lilith chọn máy bi vì bi va nhau khi rơi, nên một lần thả thành một chuỗi sự kiện chứ không ra kết quả ngay như rương.
- Tiền nằm ở **vòi bi**: cây bi hồi chậm, hệ số cược ×1–×100 (đổi cỡ cược, không đổi giá trị mỗi bi), hết bi thì hiện gói giảm giá. Tỉ lệ ô cố định và công khai.
- Kết quả: research ghi khoảng 45,6 triệu USD trong bốn tháng đầu (ước tính AppMagic). Nhưng giữ chân sau ngày 7 yếu, và đánh giá trên App Store chuyển dần sang chê tiến độ chậm.

Những móc tâm lý có bằng chứng tốt nhất (research mục "Mười cái móc"): gần như lần nào cũng trúng; thỉnh thoảng trúng hiếm; cú nào cũng được ăn mừng, kể cả khi thực chất là lỗ; thanh tiến độ sắp đầy. Bán bi tức là bán lượt quay, dạng game đã thua những vụ kiện lớn ở Mỹ (Big Fish Casino dàn xếp 155 triệu USD).

## Khác ClashMaster ở chỗ nào

Research kết luận máy bi kiểu Critters đặt sai chỗ ở ClashMaster, vì bot ĐÁNH lên cấp theo bộ bài của người chơi: cả đội mạnh lên thì đối thủ cũng mạnh lên.

**Game này thì khác:** ải có địch cấp cố định ([05_VuotAi_ThuPhuc.md](05_VuotAi_ThuPhuc.md)), nên sức mạnh từ máy bi có tác dụng thật, đúng như ở Critters. Vòng "bi → mạnh lên → qua ải khó hơn → thêm bi" chạy được. Vì thế phải cẩn thận theo chiều ngược lại: máy quá hào phóng thì tay nghề xếp khối không còn quan trọng.

## Đề xuất: máy bi Thu phục

- **Chỗ đặt:** một tab riêng ở menu dưới. Máy đứng dọc gần cả màn hình, bi rơi từ trên xuống.
- **Bi từ đâu:** 1 bi mỗi ải thắng, +2 khi đạt 3★ lần đầu, +3 khi thu phục được tướng, nhiệm vụ ngày. Không hồi theo giờ.
- **Mặt máy:**

| Ô | Tỉ lệ (đề xuất, đo lại bằng mô phỏng) | Trả |
|---|---|---|
| Hai ô ngoài | khoảng 60 % | vàng hoặc kinh nghiệm |
| Hai ô giữa | khoảng 33 % | đá tiến hóa, hệ ngẫu nhiên |
| Ô tâm | khoảng 6 % | mảnh của một tướng đã gặp trong ải |
| Ô vàng nhỏ ở tâm | khoảng 1 % | **quả cầu phong ấn**: thêm 2 lượt cho lần phong ấn kế tiếp |

- **Một thanh "hũ sắp đầy"**: mỗi bi đổ một nấc, bắt đầu đã có sẵn vài nấc. Đầy hũ thì chắc chắn được 10 mảnh của một tướng tự chọn trong số tướng đã gặp.
- **Không mở tướng chưa gặp.** Tướng mới đến từ thu phục; máy chỉ giúp nuôi. Thu phục vẫn là lý do để vượt ải.
- **Canh lúc thả:** một mái chèo đung đưa trên đỉnh. Thả đúng lúc thì bi dễ vào giữa hơn một chút. Ghi rõ tác dụng này trên máy.
- **Tiếng và hiệu ứng tỉ lệ với giá trị thật:** ô vàng chỉ kêu nhỏ; ô hiếm mới có kèn. Research ghi đây là cách chữa đã được chứng minh cho việc "lỗ mà tưởng thắng".
- **In tỉ lệ lên mặt máy.** Apple buộc công bố tỉ lệ cho mọi thứ ngẫu nhiên bán bằng tiền.
- **Thả nhiều bi một lúc** (×5, ×10) chỉ để nhanh, không nhân thưởng, không cần giữ bi mới mở. (Đề xuất ban đầu. Đã đổi 2026-11-05: mức cược mở theo số bi đang có, như Critters, xem mục "Cược theo số bi" bên dưới.)

## Nếu muốn kiếm tiền từ máy

**Đã chốt (2026-10-30): bi chỉ kiếm bằng chơi, không bán bi.** Bảng dưới giữ lại để biết lý do.

| | Bán vẻ ngoài | Bán bi (như Critters) |
|---|---|---|
| Bán gì | mặt máy, bi màu, hiệu ứng | gói bi, gói giảm giá khi hết bi |
| Doanh thu | thấp hơn | cao hơn (Critters là ví dụ) |
| Pháp lý | an toàn | thuộc loại casino xã hội; Úc xếp game mô phỏng cờ bạc R18+ từ 9/2024 |
| Ảnh hưởng tay nghề | không | có: mua bi thành mua sức mạnh qua ải |

Research đề xuất cho ClashMaster là bán vẻ ngoài. Với game này, đề xuất giữ hướng đó, và kiếm tiền ở chỗ khác: thẻ tháng, gói tướng có sẵn, vé ải hằng ngày.

## Vật lý chép

Chủ dự án bảo chép vật lý và hiệu ứng của máy Critters (2026-11-02). Vật liệu chép nguyên, đổi theo đường kính bi: bi ở đó 0,162 u, ở đây 18, nên 1 u = 111.

| Mục | Critters | Máy bi Thu phục |
|---|---|---|
| Nảy | 0,8 (nấm đỉnh 0,9) | 0,8 mọi thứ |
| Ma sát | tường, vách, nấm lớn 0,22; đinh, mái, đáy V 0 | tường, trần, vai, vách, nấm, cọc 0,22; đinh, mái, đáy két 0 |
| Va chậm không nảy | dưới 1 u/giây | dưới 111 |
| Bi va bi | không nảy | không nảy |
| Cản | 0,3 | 0,3 |
| Trọng lực | 2 u/giây² (= 222) | 1.100 |
| Kẹp tốc | 4–14 u/giây (= 444–1.556) | 150–525 |

**Trọng lực và kẹp tốc không chép nguyên.** Mặt máy này dày đinh hơn nhiều: khoảng 85 đinh trên 26 × 38 đường kính bi, máy Critters có 22 đinh trên 33 × 50. Chép nguyên thì bi bay trung vị 9 giây. Muốn bi bồng bềnh đúng như Critters thì phải đổi mặt máy sang ít đinh to.

Lý do và các lần thử ghi ở change `update-pachinko-feel` (design, mục vật lý).

## Hiệu ứng chép

**Phần chép:** cấu trúc hệ hạt (số hạt, đời, tốc, cỡ và màu theo đời, trọng lực, kẹp tốc) lấy từ prefab hiệu ứng của Critters, chi tiết trong `PINBALL_REPORT.md` mục 6.

**Phần của mình:** hình hạt (`fx_*`, sau này là ảnh gen P4). Code ở `Assets/01 Script/Game/Machine/MachineFx.cs`.

**Tô phẳng (2026-11-06):** lớp quầng mềm của máy đó (glow, flash) đổi sang hình vẽ tay phẳng có viền mực `pk_fx_*` (loé, vòng dày,
vòng đứt, tia toả, chấm), theo luật hiệu ứng không quầng. Cỡ khoảng một nửa cỡ quầng cũ, tô màu nhạt. Cùng đợt có nút vòm, viên cược,
đèn vòm chạy, trạng thái sáng của đinh, nấm, cốc, két, ô. Bảng đối chiếu toàn bộ bộ phận và 36 hiệu ứng của máy đó:
`ArtGen/Pachinko/THAM_KHAO_MAY_BI.md`.

**Đơn vị:** cỡ và tốc tính theo u của Critters, đổi ra px như sau:
- hiệu ứng theo bi: 1 u = 191 px canvas;
- hiệu ứng ô: theo bề rộng ô (ô Critters rộng 0,9 u).

| Lúc | Critters | Ở đây |
|---|---|---|
| Bi lăn | TrailRenderer 0,3 giây, rộng 0,18 u, xanh lơ alpha 0,52 → tím trong suốt | dải `TrailGraphic` 0,3 giây, rộng 0,18 u, màu bi alpha 0,6 → 0, mép mềm |
| Chạm đinh | ảnh sáng 1,15 → 1 và quầng 1,10 → 0,68 trong 0,067 giây | như vậy, rồi mờ 0,1 giây, thêm 2 lấp lánh |
| Chạm nấm | nấm 0,90 → 1,18 → 0,89 → 1,05 → 1 trong 0,23 giây; quầng 3 co 0,15 giây, vòng 1,62 lan 0,19 giây, quầng 1,75 (tím) | như vậy, màu đỏ của nấm |
| Thả bi | cần phóng co giãn 0,63 → 1,57 → 0,89 → 1,2; lửa 0,15 giây, quầng, chấm | mây co giãn nửa biên độ; khói, quầng, chấm |
| Rơi vào ô | 3 quầng 0,1–0,15 giây, 6 sao tốc 15–60 bị hãm, 6 vệt "she" 0,07–0,1 giây | như vậy, sao vàng thay xanh lơ |
| Cốc | 10 chấm, 10 sao (trọng lực 0,3), chớp, vòng | như vậy, ở cốc bạc và két |
| Rương | bảng điểm cấp 1–4 (chớp, quầng, vòng, sao; cấp 3 thêm 6 tia tốc 10–20) | gỗ, bạc cấp 2; vàng cấp 3 |
| Jackpot | vòng 0,24 giây, 2 quầng 0,35 giây, 4 tia, 3 sao (trễ 0,05), 1 sao nảy (trễ 0,1), sao lõi | như vậy, ở két hoặc ô khuất |

**Hạt chạy theo giờ máy:** lúc rương vàng làm máy chạy chậm, hạt cũng chậm.

**Lượt thử soi:** `PokiClash/Thử/Máy bi: soi hiệu ứng`. Nó dừng máy và tua giờ hạt để chụp từng mốc.

## Thanh kinh nghiệm và số theo cược

Chủ dự án dặn (2026-11-04): máy phải có thanh kinh nghiệm ở trên, EXP nhận được thì bay về đó; đổi ×2, ×3… thì số trên máy đổi theo.

**Máy tham khảo làm gì** (bản đục, `D:\CrittersRipper`):
- Thanh cấp (`pbui_pinball_level_bar`) nằm trên đầu màn máy: vòng cấp bên trái ("LV" và số), thanh bo tròn phần đầy xanh lơ, quầng sáng ở đầu phần đầy, chữ "10/30".
- Bi vào ô kẹo thì kẹo hiện số rồi bay về thanh. Tiếng theo thứ tự: số nhảy, cộng điểm (0,33 giây), thanh lên (2,1 giây), thanh đầy (trễ 0,55 giây). Rung `ExpbarFull` khi đầy.
- Mỗi ô có ô chữ tối viền vàng ghi số thưởng (`txt_ball`); code đổi số theo mức cược. Ô thẻ, ô cướp ghi "x10".
- Nút cược vàng ghi "x15" cạnh nút PUSH; đổi cược thì bảng hệ số bật lên (`multi_popup`).
- Tủ máy đứng có đỉnh vòm viền bóng đèn và bảng điểm trên đầu.

**Ở đây:**
- **Thanh kinh nghiệm trên đầu máy** (`MachineExpBar`, phần `thanh_kinh_nghiem` của `Screens/Machine`, dựng bằng menu `PokiClash/Prefab/Máy bi: thanh kinh nghiệm`). Có vòng cấp (chép vòng cấp của thanh trên) và thanh kit `Thanh` loại EXP ghi "số/số", chừa nút Tỉ lệ bên phải.
- **Sao EXP bay lên thanh:**
  - bi vào ô EXP thì hiện chữ "+N XP" như cũ, kèm 1–4 sao EXP (10 EXP một sao);
  - sao văng sang một bên rồi lao về đầu phần đầy trong 0,55–0,67 giây, sao sau trễ 0,06 giây, có vệt lấp lánh tím;
  - tới nơi thì thanh mới cộng, nảy nhẹ, loé tím; tiếng `pick` nhỏ cao dần khi sao tới liền nhau, cách nhau ít nhất 0,07 giây;
  - lên cấp thì thanh đầy rồi về 0, vòng cấp nhún, loé vàng, tiếng `level`;
  - bản lưu vẫn cộng ngay lúc bi rơi, chỉ thanh hiện chậm. Hộp "Lên cấp!" cuối đợt chờ sao cuối tới.
- **Số trên ô theo cược** (`MachineBoard.SetMult`):
  - ô EXP ghi EXP × cược, ô bi ghi "+cược";
  - rương ở ô, cốc, két có nhãn "×cược" khi cược trên 1;
  - đổi cược thì các số nhún 1,4 → 1 trong 0,25 giây, chữ "×N" cam nổi giữa máy.
- **Thân máy vẽ tay:** gói prompt `ArtGen/Pachinko/gui_gpt/than_may/` (sinh bằng `ArtGen/Pachinko/build.py`). Tủ đỉnh vòm có bóng đèn, đầu máy có rãnh cho thanh kinh nghiệm, hốc vòng cấp, hốc nút tỉ lệ, mặt chơi trống đúng cỡ bàn.
  - Ảnh đã vào game (2026-11-04): `Assets/03 Art/Pachinko/pk_than_may.png` (851 × 1401, đúng cỡ hiện trên màn). Nhập bằng `build.py --duyet`, rồi chạy menu `PokiClash/Prefab/Máy bi: thân máy vẽ tay`.
  - Thân máy nằm sau mặt máy và thay khung giấy tạm. Thanh kinh nghiệm nằm trong rãnh. Nút tỉ lệ thành chữ "i" trong hốc tròn bên phải.
  - Cột cược và khay rương sát mép màn, thu nhỏ cho khỏi đè viền tủ.
- **Bộ phận, hiệu ứng, rương vẽ tay** (vào game 2026-11-04, gói `ArtGen/Pachinko/gui_gpt/than_may/` lượt 2–4):
  - **Mặt máy tĩnh** `Baked/Machine/may_tinh.png` ghép từ 12 bộ phận GPT bằng `build.py --duyet bo_phan`. Chỗ đặt theo hình học `Board.Build`, có bản chép trong `build.py`: đổi mặt máy thì đổi cả hai.
  - **Nấm, máng mây, bi** là hình động: `pk_bumper` (thay hình tạm cùng tên), `pk_may_tha`, `pk_bi` (trắng xám, game tô màu theo cược). Gắn bằng menu `PokiClash/Prefab/Máy bi: ảnh bộ phận`.
  - **Hiệu ứng** `fx_glow`, `fx_sparkle`, `fx_ring`, `fx_star`, `fx_streak`, `fx_puff` trong `Assets/03 Art/Pachinko` thay hình tạm cùng tên ở mọi chỗ (menu `PokiClash/Dựng lại danh mục ảnh`).
  - **Rương** `pk_ruong_go`, `pk_ruong_bac`, `pk_ruong_vang` (bản mở thêm `_mo`): `ChestIcon` tự dùng khi có. Hộp mở rương đổi sang bản mở lúc bật nắp. Rương AFK có màu riêng nên giữ hình vẽ tạm.

## Cược theo số bi, mốc quà, thanh nhún cả viền (2026-11-05)

Chủ dự án dặn: thanh kinh nghiệm phải nhún cả viền; học mốc quà của Critters (thả n bi nhận một món rồi đổi món mới); nút ×N mở theo số bi đang có chứ không theo cấp. Change `add-ball-milestones`.

**Critters làm gì** (bản đục; ảnh dựng lại từ prefab ở `D:\CrittersRipper\analysis\ui_shots\sheet.png`):
- Bảng cược `multi_popup`: "Mọi phần thưởng ×2"; ở mức tối đa ghi "Mốc tiếp theo: mở khi có 8000 bi". Ngưỡng theo wiki: ×1, ×2 luôn mở, ×3 từ 240, ×5 từ 360, ×10 từ 600–720, ×20 từ 1.200 … ×100 từ 7.200 bi đang có (khoảng 60–80 lần thả). Tụt dưới ngưỡng thì mất mức đó.
- Thanh cấp: nền và phần đầy cùng nhún 1,2 → 1,08 → 1,2 → 1,08 → 1,2 → 1 trong 0,25 giây; dọc thanh có mốc nhỏ (icon hệ, mũi tên lên).
- Quà theo tiến độ: nấm trứng có vòng, đầy thì ra tướng hoặc bi, mỗi ngày tối đa vài lần ("2/3", đếm ngược); sự kiện 150 bậc quà, số món theo cược.

**Ở đây:**
- **Cược:** ×1, ×2 luôn mở; ×3 từ 150, ×5 từ 300, ×10 từ 700 bi (`progression.xSteps[].balls`). Mô phỏng: người chăm có 600–1.200 bi một ngày, người ít 50–150.
  - Nút chưa mở mờ, ghi "n bi", chạm thì báo. Đủ bi mở thêm mức thì báo và nút nhún.
  - Bi tụt dưới ngưỡng thì hết đợt cược về mức cao nhất còn mở.
- **Mốc quà** (`pachinko.gifts`): sau mốc Huyền thoại, cứ tiêu đủ bi (×N tính N) thì nhận một món, rồi sang món kế, hết thì vòng lại.
  - Bảng: 30 bi rương gỗ, 40 bi +8 bi, 50 bi rương bạc, 60 bi +120 XP, 80 bi rương vàng. Thêm khoảng 7–8 % giá trị mỗi vòng 260 bi.
  - Thanh mốc nằm chỗ thanh Huyền thoại cũ, có ô quà tròn ở đầu thanh. Nhận quà thì ô nhún, quà bay ra (rương vào khay, sao EXP lên thanh, bi về dòng đếm), rồi ô đổi sang món kế.
  - Chạm thanh hoặc ô quà thì báo ba mốc kế.
- **Thanh kinh nghiệm nhún cả viền:** rãnh vẽ tay cắt khỏi thân máy (`ArtGen/Pachinko/cat_ranh.py` → `pk_ranh_exp.png`), đặt trùng khít lên rãnh, gom với thanh thành `khung_thanh`. Cả nhóm nhún theo dáng Critters (ngang 3 %, dọc 18 %, chữ thêm 12 %), không nhỏ hơn cỡ gốc.
- **Menu:** `PokiClash/Prefab/Máy bi: thân máy vẽ tay` (dựng `khung_thanh`), `PokiClash/Prefab/Máy bi: mốc quà` (ô quà). Tour thử: `PokiClash/Thử/Máy bi: mốc quà, cược theo số bi`.
- Duyệt lại thân máy (`build.py --duyet`) thì chạy lại `cat_ranh.py` rồi menu thân máy.

## Việc còn lại (ghi 2026-11-04)

Thanh kinh nghiệm, số theo cược, thân máy, bộ phận, hiệu ứng, rương vẽ tay đã vào game (Unity), 96/96 test EditMode qua.

**Làm trước:**
1. **Thử trên điện thoại Android** (Build thường):
   - thanh kinh nghiệm đọc được không; sao EXP bay có rõ không; tiếng `pick` khi sao tới có dày quá không lúc "Thả liền";
   - cột cược và khay rương đã thu còn 0,82–0,84: chữ "×10 / 700 bi" còn đọc được không;
   - nút "i" tỉ lệ (khoảng 65 px) có dễ bấm không;
   - đinh, bi, nấm vẽ tay có rõ ở cỡ nhỏ không.
2. **Kiểm dung lượng:** chạy menu `PokiClash/Dung lượng: ảnh nặng trong build`. Ảnh mới gồm thân máy 851 × 1401, mặt máy 920 × 1360, 6 rương 320 px, 6 hiệu ứng 256 px.

**Tuỳ chọn:**
- **Rương AFK** (màu xanh ngọc riêng) vẫn là hình vẽ tạm. Có hai cách: gen thêm rương AFK đóng và mở theo dáng rương mới, hoặc bỏ màu riêng để dùng ảnh rương gỗ.
- **Hình vẽ code còn lại**, sẽ đẹp theo khi gen các gói chung:
  - thanh EXP và vòng cấp (`Kit/Thanh`, vòng cấp chép từ thanh trên): chờ gói `ArtGen/UIKit`;
  - icon XP, bi, rương trên thanh trên cùng và trong ô thưởng: chờ gói `ArtGen/Icons`.
- **Nền màn máy bi** vẫn là màu xanh nhạt trơn, chưa có ảnh.
- **Tiếng và rung:** máy tham khảo có tiếng riêng cho thanh lên (`expbar_up` 2,1 giây) và thanh đầy (`expbar_full`), cùng rung `ExpbarFull`. Ở đây đang dùng tiếng `pick`, `level` và rung lên cấp có sẵn.
- **Thanh trên cùng** ("Cấp n") đổi ngay lúc bi rơi, nên nhanh hơn thanh trên máy một nhịp.
- **Bản web** chưa có thanh kinh nghiệm và số theo cược. Theo luật 2026-11-03 chỉ làm ở Unity, khi nào dặn mới làm web.

**Lưu ý:**
- File prompt ghi đường dẫn tuyệt đối của máy đang chạy. Sang máy khác thì chạy `py -3 -I ArtGen/Pachinko/build.py` trước để dựng lại đường dẫn, rồi mới gửi GPT.
- Đổi bố cục mặt máy trong `Pachinko.cs` thì sửa cả `board_geometry` trong `ArtGen/Pachinko/build.py`, rồi chạy `--duyet bo_phan` lại.
- Không chạy `Web/scripts/draw_machine.py`: script đó ghi đè mặt máy vẽ tay bằng bản vẽ code.
- Gen lại tờ nào thì làm theo `ArtGen/Pachinko/gui_gpt/than_may/HUONG_DAN.md`: `build.py --duyet <tờ>`, rồi chạy các menu Unity ghi ở đó.
