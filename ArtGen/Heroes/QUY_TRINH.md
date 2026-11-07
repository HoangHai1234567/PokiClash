# Quy trình gen hình tướng (2026-11-02)

Người dùng chốt (2026-11-02), sau nhiều lần đổi trong ngày:
- **vẫn vẽ đè lên rig vector của aola** để giữ animation aola;
- **nét vẽ tay của game** như ảnh mốc bản đồ, **thiết kế** học từ tướng aola;
- tướng có **vẻ "chiến"**;
- **viền trắng kiểu giấy xé** quanh tướng do game vẽ (shader), GPT không vẽ.

Mọi file prompt tướng cũ (`PROMPTS.md`, `Thuy.md`, `thuy/*.md`) đã xoá; prompt nay sinh từ `build.py`.

## 1. Phong cách

- **Tướng là sinh vật kiểu thú nuôi đánh nhau**, không phải người (ngoại lệ: dòng Tiểu Y và dòng Mi Nhi, xem dưới).
- **Nét vẽ** lấy từ `ArtGen/Islands/refs/world_style.png` (người dùng nhắc lại 2026-11-04):
  - hình vẽ tay trên giấy bằng bút mực: viền nâu sẫm `#2B2118` dày đều, hơi rung như bút thật;
  - mỗi vùng tô bằng chì màu và sáp màu, nét tô gạch chéo lộ rõ;
  - họa sĩ vẽ tay đẹp: không nguệch ngoạc kiểu trẻ con, không quá chi tiết;
  - không bóng loáng kiểu số, không chuyển sắc, không 3D.
- **Tô phẳng, không bóng, không ánh sáng** (người dùng dặn 2026-11-04, áp cho mọi tướng; thay luật 2026-11-03 "bóng chì gạch chéo bên trong hình, vài điểm sáng trắng"):
  - mỗi vùng một màu đều, nét chì sáp chỉ là vân, không tạo sáng tối; vùng nào đậm hơn là do thiết kế có màu đậm (lòng áo choàng...);
  - không mảng sáng tối, không bóng đổ, không bóng dưới chân hay in xuống nền, không điểm sáng trắng, không bóng loáng, không quầng sáng; chỉ chừa một chấm sáng nhỏ trong mắt;
  - áp cho concept, mảnh, vũ khí, hiệu ứng chiêu và mặt tướng: `build.py` (`FLAT`, `RENDER`, `LINE`), `build_fx.py`, `ArtGen/BattleIntro/build.py` (`FACE_STYLE`) tự chèn vào mọi file prompt;
  - ảnh mốc style (concept Giọt Sương dạng 1) có chấm sáng và mảng tối: prompt dặn chỉ học nét mực và vân chì sáp của nó;
  - hình Giọt Sương đã gen trước ngày này còn bóng chì gạch chéo và điểm sáng, chưa vẽ lại.
- **Thiết kế** học từ tướng aola (người dùng gọi là "style pokemon"): dáng gọn mập, đọc được khi nhỏ, mắt to, hình đơn giản, ít chi tiết. Không lấy nét bóng loáng của aola, không chép con nào.
- **Vẻ "chiến"**: mày xếch xuống, cười tự tin lộ răng nanh nhỏ, thế sẵn sàng đánh; dễ thương, không linh vật vui tươi, không đáng sợ.
- **Viền trắng giấy xé**: game vẽ bằng shader (mục 7). Prompt dặn GPT không vẽ viền trắng.

Lịch sử 2026-11-02 (để khỏi lặp lại):
- nét vector bóng như hình gốc: "không giống style game";
- nét trẻ con vẽ vở nháp: "xấu";
- nét số bóng loáng kiểu sprite: "mất style vẽ tay";
- bỏ rig, vẽ bộ mảnh rời: người dùng quay lại rig cũ;
- kỳ giông, cá chép: bỏ; Giọt Sương dạng 1 là tinh linh nước hiệp sĩ tập sự.

**Dòng Tiểu Y (`tieu_y_1`, `tieu_y_2`, rig aola #1319, #1320), người dùng chốt 2026-11-04:**
- **ngoại lệ của luật "không phải người"**: giữ theme thần biển Poseidon, **dạng người** (dạng 1 tiểu thần biển chibi, dạng 2 thần biển trẻ);
- thiết kế theo `DESIGN_CHIBI` (cách thiết kế như tướng thú nhưng là nhân vật); concept đính thêm ảnh mốc style (`"anchor": True`);
- hiệu ứng nước tự chạy (lốc nước thay chân, vòng nước, dải nước) giữ hình gốc aola để không mất animation: bỏ khỏi bóng xám, không có nhóm vẽ lại.
  - GPT không vẽ lại (người dùng chốt 2026-11-04). Khi ghép, Claude dùng script tô lại mọi khung con cho hợp nét tướng: viền mực nâu dày như các mảnh khác, tô phẳng hai tông xanh của lốc nước trong concept, bọt trắng viền mực mảnh, vân chì chéo nhẹ, bỏ viền trắng và vụn sáng của aola. Dáng từng khung giữ nguyên.
  - #1319 có 41 hình: lốc nước c23 19 hình, vòng nước c57 7 hình, c8 15 hình. Tóc của #1320 (mảnh 30, 35, 40) cũng tự chạy: khi ghép phải khớp hình mới vào từng khung con.

**Dòng Mi Nhi (`mi_nhi_1`, `mi_nhi_2`, rig aola #983, #984), người dùng chốt 2026-11-06:**
- **ngoại lệ thứ hai của luật "không phải người"**: giữ tiên cá chibi dạng người chơi đàn (người dùng chọn thay cho rái cá biển Claude đề xuất); thiết kế theo `DESIGN_CHIBI`, concept đính ảnh mốc style;
- thiết kế (Claude đề xuất, chờ duyệt concept), khác hẳn bản gốc (tóc xanh ngọc, kẹp sao, mắt xanh lá, đàn vàng đỏ, đuôi xanh lam):
  - tóc tím oải hương ngọn bọt trắng, mắt xanh sapphire, vây tai xanh nhạt gân tím, kẹp vỏ sò hồng giữ ngọc trai, đuôi xanh ngọc bích vây tím nhạt;
  - dạng 1 ôm đàn lia san hô trắng hồng;
  - dạng 2 tóc rất dài, quạt san hô sau đầu, khăn quấn hông trắng ngọc, đàn hạc khung xương trắng ngà uốn như sóng;
- vòng sao (tự chạy) bỏ khỏi bóng xám, không có nhóm (khi ghép sẽ bỏ như vòng băng của Cánh Cụt);
- đầu dạng 2 (#984) là một mảnh (mặt, mái, kẹp sao liền), nên GPT vẽ mặt trong nhóm đầu. Khung các nhóm mảnh nhỏ nới rộng cho viền không quá 24 px.
- concept dạng 1 Claude duyệt 2026-11-06 (lần gen đầu):
  - đủ phần, đúng chỗ; đế đàn là vỏ sò điệp, nên prompt N07 sửa theo;
  - concept cao và hẹp hơn rig, đuôi dài hơn: N05, N08 giữ viền rig nên không sao.
- concept dạng 2 duyệt cùng ngày (lần gen đầu): khớp rig rất sát; chỉ cuộn đỉnh đàn hạc nằm trên phải thay vì trên trái sau đầu (prompt N09 giữ đường khung cũ).
- nhóm dạng 1 (GPT vẽ đủ 8 nhóm một lượt): đúng chỗ, mắt trùng chỗ cũ.
  - Nét đều 12–15 px nên lệch số đã ghi: N03, N04 dày hơn (12 so với 9 px), N06, N07 mảnh hơn (12, 15 so với 21 px).
  - Khi ghép: mài N03, N04; nới N06, N07.
- ghép dạng 1 (`reskin/thuy_983`, cùng ngày):
  - mài N03, N04 bớt 3 px; nới N06 thêm 5 px;
  - N07 (đàn) giữ nguyên: nới viền sẽ lấp khe giữa các dây đàn;
  - bỏ vòng sao (2, 27).
- animation dạng 1 (`anim_moi.json`, cả 5 clip):
  - đứng lơ lửng, tay gảy đàn bốn nhịp; trúng đòn bật lùi;
  - **đánh thường đánh từ xa như bản gốc:** gốc dời rất ít nên trận coi là đòn bắn xa (AolaSticker.Lunge: độ lao ≤ 30 đơn vị sân), sóng âm FX02 bay tới, nổ ở chỗ đối thủ (`far` [560, 95]) đúng khung 21 = 60% clip, là lúc trận tính trúng;
  - chiêu mana bắn tia từ đàn lia ở khung 12;
  - chiêu cuối (`lunge`): nhảy vòng cung như cá heo, gảy đàn giữa không trung, đáp xuống quất đuôi kèm hợp âm nổ nước ở khung 21.
- ghép dạng 2 (`reskin/thuy_984`, cùng ngày):
  - nới viền N05, N06 6 px; N07, N08 3 px (tay chỉ 3 px cho ngón khỏi dính);
  - bỏ vòng sao (2, 26);
  - đàn hạc (5) và tóc dài (8) có khung con tự chạy ở clip đứng gốc: bộ ghép tự đưa về hình mới, clip viết lại không dùng nữa.
- animation dạng 2:
  - đứng, hai tay gảy dây so le;
  - đánh thường đánh từ xa: quét dây, sóng âm lớn nổ ở chỗ đối thủ (`far` [760, 150]) khung 21;
  - chiêu mana: tia cỡ 1,4 từ bàn tay trên dây;
  - chiêu cuối (`lunge`): lao tới, đàn hạc quay một vòng sau lưng như bánh xe dây đàn, dựng đàn lại, hai tay quét dây ở khung 21 (sóng âm lớn, nổ nước, vòng sóng); trận tính trúng ở khung 23.
- kiểm khung trúng: script mô phỏng AolaActor.MotionOf phải bỏ hình ở xa (hình không có trong dáng đứng, tâm cách bóng hơn 1,5 lần chiều cao) như trận, không thì đòn bắn xa bị tính nhầm thành đòn lao.

**Dòng Cánh Cụt (`canh_cut_1`, `canh_cut_2`, rig aola #1691, #1692), Claude đề xuất 2026-11-06, người dùng chưa duyệt:**
- cánh cụt mào kiểu rockhopper: đầu, lưng, mặt xanh thẫm, bụng trắng, mắt to lòng trắng, mày lông vàng xếch (cho vẻ chiến), mỏ cam đỏ, chân hồng nhạt, khăn bếp xanh trời; khác con gốc (xanh trời, mặt trắng, bụng nâu nhạt, khăn đỏ, má hồng);
- dạng 1 tập sự bếp: chảo gang mép đóng sương thay con cá băng; dạng 2 bếp trưởng: mũ bếp cao đai xanh, cổ áo và tạp dề trắng, khay băng trong có ba con cá nướng thay đĩa sứ bánh cá, chim non lông tơ xám thay chim con tím;
- vòng băng có sao băng (tự chạy) và hơi nóng trên đĩa giữ hình gốc, bỏ khỏi bóng xám; khi ghép Claude tô lại như hiệu ứng nước của Tiểu Y;
- đòn đánh dạng 2 tung chim con lao tới đối thủ (hình chim trượt to là biến thể), clip chiêu dạng 1 có chỏm lông dựng gai, mặt há mỏ: xử lý khi ghép.
- concept dạng 1 Claude duyệt 2026-11-06 (lần gen đầu): đủ phần, đúng hướng như rig; thân hình trứng cao và hẹp hơn khối tròn của rig, chảo cao ngang mỏ (rig: cá ngay dưới mỏ). N02 giữ viền rig và mắt đúng chỗ mắt cũ (xa nhau hơn concept), nên khi soi thử xem mặt có bị dãn không.
- concept dạng 2 duyệt cùng ngày (lần gen đầu): đủ phần, đúng chỗ; vây trái giơ cao hơn rig (ngang khăn), khay có bốn con cá (rig ba mảnh món ăn) nên prompt N06 ép đúng ba con.
- nhóm dạng 1 (GPT vẽ cả 6 nhóm một lượt, 2026-11-06): đúng chỗ, đúng đầu chi, mắt và mỏ trùng chỗ cũ. GPT vẽ nét mực đều khoảng 13–16 px ở mọi nhóm, nên N02, N03, N06 dày gấp khoảng 2 lần số đã ghi (8, 6, 8 px); N01, N04, N05 gần đúng. Mào N01 hẹp hơn chỏm cũ, đuôi N06 cao hơn đuôi cũ. Khi ghép: mài mỏng viền ngoài ba nhóm dày (bỏ phần mực phía ngoài, hình co chưa tới 1%) thay vì gen lại.
- ghép dạng 1 (`reskin/thuy_1691`, 2026-11-06), dùng bản gen lại của người dùng: `N01_2`, `N03_2`, `N06_3`.
  - Mài viền bằng `sua_manh.py mong` (lệnh mới): N02 bớt 8 px, N03_2 bớt 6 px, N06 bớt 5 px.
  - Bàn chân N06_3 vẽ cao hơn chỗ cũ 34 px (sẽ khuất sau thân), đuôi thì khớp: dời cả ảnh xuống 34 px (`doi`) rồi mới mài.
  - Vòng băng có sao băng: tô lại bằng `to_nuoc` thì nhoè (hình gốc độ phân giải thấp), nên bỏ hẳn (`drop` 2, 21).
- animation dạng 1 viết lại cả 5 clip (`anim_moi.json`):
  - đứng nhún thở; trúng đòn bật lùi;
  - đánh thường: ngồi thụp kéo chảo sang trái ngực, vồ tới quật chảo ngang (khung 18);
  - chiêu mana (1_5 dựng mới): đẩy chảo ra trước, bắn tia từ mặt chảo ở khung 12, cỡ tia 0,7;
  - chiêu cuối (`lunge`): xoay như con quay lao tới, chảo chìa ngang, lốc nước FX01 quanh người; bật dậy đập chảo ở khung 26.
  - Bài học:
    - mặt chảo chỉ đọc rõ ở góc khoảng 30–40°, quá 70° thì nhìn nghiêng thành mảnh;
    - chảo nằm dưới hai vây nên lúc vung phải `top`;
    - lật ngang (sx qua 0) mỗi nửa vòng tối thiểu 3 khung, 2 khung thì khung giữa co về 0 và con biến mất;
    - thân xoay 70° để trượt bụng thì mặt xoay ngang, bóng tụt lại sau: bỏ cách đó.
- ghép dạng 2 (`reskin/thuy_1692`, cùng ngày):
  - GPT vẽ nét đều 12–13 px, nên chỉnh viền: N02–N05, N07 mài bớt 3 px; N06 nới 3 px, N08 nới 5 px.
  - Chim non gộp một mảnh (N08 chỉ mảnh 22, bỏ 23–32); đầu gộp mặt, mỏ (bỏ 11–16, 43).
  - Bỏ vòng băng (2, 44) và hơi nóng (41, 42): hơi nóng không có khung con, viết lại clip thì đứng im.
- animation dạng 2:
  - đứng, chim non nhún theo nhịp riêng;
  - trúng đòn: cá trên khay nảy;
  - đánh thường: hạ khay lấy đà, vồ tới đẩy khay ngang mặt đối thủ (khung 18), ba con cá văng lên rồi rơi lại;
  - chiêu mana: đẩy khay tới, bắn tia cỡ 1,4 từ tâm khay;
  - chiêu cuối (`lunge`): xoay như con quay như dạng 1, nhảy lên giơ khay rồi đập xuống trước mặt (khung 26).
  - Bài học: khay nằm ngang tầm mặt và vẽ sau đầu, nên nhấc khay lên là che mặt; lấy đà bằng cách hạ khay, lúc giơ cao thì dời khay sang phải đầu (dx +30).
- **chiêu cuối viết lại cho độc đáo** (người dùng dặn cùng ngày; trước đó hai dạng cùng kiểu xoay con quay rồi đập). Khoá dựng bằng script `<aola>/reskin/thuy_1691/chieu_cuoi.py` và `thuy_1692/chieu_cuoi.py` (ghi clip 1_6 vào `anim_moi.json` cùng thư mục, rồi chạy `anim_moi.py`).
  - Dạng 1, trượt băng, lộn nhào, lật chảo:
    - ngồi thụp, sương băng tụ ở chảo;
    - ngả 25° trượt băng lao tới, chảo chĩa trước như mũi tàu, sóng lưỡi liềm FX02 và giọt nước sau lưng;
    - bật lên lộn nhào 360° quanh tâm thân trong lốc FX01, đập chảo ở khung 29;
    - tung chảo xoay hai vòng lên bên phải đầu rồi bắt lại.
  - Dạng 2, lướt sóng trên khay băng:
    - tung ba con cá lên; khay thành ván dưới chân: vây phải −20°, khay +20° (ván nằm ngang), khay dời (−124,5; 71,5);
    - sóng thần FX07 dâng sau lưng; lướt tới, chim non đứng mũi ván, cá xoay vòng trên đầu;
    - sóng đổ ập ở khung 28, cá rơi xuống chỗ đối thủ; nhảy khỏi ván, bắt lại khay, cá nhảy về khay.
  - Bài học:
    - **khung trúng** của trận (AolaActor.MotionOf) là khung mà trung bình góc trên trái của mọi hình (trừ bóng) đi xa nhất, có trung bình trượt 5 khung. Xoay thân 180° làm góc trên trái các hình văng ra trước khoảng nửa cỡ hình, nên lộn nhào phải ở quãng gần hơn nhát đập. Hiệu ứng nổ phía trước làm khung trúng trễ nhát đánh khoảng 2 khung ở mọi đòn hiện có.
    - **lộn quanh tâm thân:** gốc xoay quanh khớp ở chân, nên muốn lộn quanh tâm thân phải bù dx = X − v·sin θ, dy = Y − v + v·cos θ (v = tâm thân cao hơn khớp gốc). Lúc đó bóng chạy theo dx nên lệch khỏi thân khi đang lộn.
    - **hiệu ứng không gắn mảnh** (không có `anchor` hay `pin`) đi theo cả dx lẫn dy của gốc: đặt toạ độ theo dáng nghỉ. Con được nhấc lên thì bù ey để chân sóng vẫn sát đất.

**Dòng Ma Kết (`ma_ket_1..3`, rig aola #758, #759, #760), Claude đề xuất 2026-11-06, người dùng chưa duyệt:**
- dê biển (thân dê, đuôi cá), tướng Hiếm ải 20, danh hiệu "Thánh giáp sừng bạc";
- khác con gốc: gốc lông trắng xù, xoáy lông trên trán, tai thỏ hồng, mắt đỏ, sừng nâu nhạt; dạng 2 sừng tím hồng, mắt xanh ngọc; dạng 3 mũ giáp vàng ngọc xanh lá, vây xanh tím;
- thiết kế mới: lông xanh mòng két, mõm và len trắng kem, sừng bạc có ngấn, tai là vây cam san hô gân xanh mòng két, mắt hổ phách, móng xanh thẫm, vây đuôi cam san hô;
- giáp vỏ sò điệp hồng san hô viền bạc lớn dần: dạng 1 chưa có, dạng 2 vỏ sò đeo ngực, dạng 3 mũ thánh giáp có ngọc trai xanh thẫm và giáp vai;
- rig #758 lơ lửng, 12 mảnh; #759 đứng hai chân trước, 17 mảnh; #760 nhìn nghiêng khom sắp vồ, 26 mảnh, clip đánh gốc có hình sừng to quét ngang (biến thể);
- đã có `regions.json` cả ba dạng; `groups.json` #758: N01 hai sừng, N02 hai tai, N03 đầu, N04 thân, N05 hai chân trước, N06 vây đuôi. Nhóm #759, #760 dựng khi duyệt concept từng dạng.
- concept dạng 1 Claude duyệt 2026-11-06 (lần gen đầu):
  - đúng thiết kế, nét mực và vân chì sáp rõ, vẻ chiến;
  - chồng lên rig thì sừng, tai, chân, vây đúng chỗ; đầu hẹp hơn vùng 5 một chút, thân nhỏ hơn vùng 6. N03, N04 giữ viền rig nên không sao;
  - sừng còn sáng tối giữa các ngấn, tròng mắt hai tông: prompt N01 dặn sừng một màu bạc đều.
- lượt 2 dạng 1: gen thử N03 (đầu, giữ viền) và N02 (vây tai, đổi dáng). Viền: N01–N03 10 px, N04 23 px, N05 22 px, N06 16 px.
- concept dạng 2 Claude duyệt cùng ngày (lần gen đầu): mọi phần đúng chỗ như rig, có vỏ sò đeo ngực; sừng vẫn sáng tối giữa các ngấn (N01 dặn tô một màu).
  - Nhóm #759: N01 hai sừng, N02 vây tai, N03 đầu gộp túm len má và chỏm len, N04 thân có vỏ sò, N05 hai chân trước, N06 đuôi cá và vây.
  - Khung N02 gồm cả sừng to và túm len má, để vây tai to hơn tai cũ vẫn còn chỗ.
  - Viền: N01 10 px, N02 11, N03 11, N04 21, N05 18, N06 13.
- concept dạng 3 Claude duyệt cùng ngày (lần gen đầu): vây gai chữ L, vây giữa, vây dưới, ba vây nhỏ, đuôi, hai chân, đầu, mũ, hai sừng khớp rig rất sát.
  - Lệch: vây tai nằm ngang ra sau (rig chĩa lên sau), bờm sẫm lùi về sau hơn rig, ngọc có chấm sáng. Prompt N04, N02 ép về chỗ cũ, bỏ chấm sáng.
  - Nhóm #760 (10 nhóm): N01 hai sừng, N02 mũ vỏ sò, N03 đầu và bờm, N04 vây tai và bờm sẫm, N05 thân, N06 giáp vai và dây, N07 chân gần, N08 chân xa, N09 đuôi cá và ba vây nhỏ, N10 ba vây lớn.
  - Hai chân để hai nhóm riêng vì chân gần che gần hết chân xa.
  - Viền: N01 14 px, N02 14, N03 13, N04 14, N05 16, N06 16, N07 19, N08 21, N09 11, N10 8.
- ghép cả ba dạng (`reskin/thuy_758`, `thuy_759`, `thuy_760`, 2026-11-06):
  - GPT vẽ nét đều khoảng 10–12 px ở mọi nhóm, nên nới bằng `sua_manh.py vien`:
    - dạng 1: N04 +3 px, N05 +7, N06 +3;
    - dạng 2: N02 +2, N04 +8, N05 +6;
    - dạng 3: N01 +4, N02 +4, N03 +3, N04 +4, N05 +6, N06 +5, N07 +8, N08 +9.
  - Đo viền: thang đo tự động lẫn mực nâu với màu xanh mòng két đậm, nên cắt ảnh 1:1 có thước 10 px rồi xem bằng mắt.
  - Lệch chỗ so với hình cũ (giữ nguyên, ghép vẫn liền):
    - dạng 1: chân dài hơn chân cũ (móng lộ dưới bụng như concept), vây đuôi to hơn, phần gốc giấu sau thân;
    - dạng 3: mũ vỏ sò thấp hơn mũ cũ (không có phần ôm má, đầu mới đã vẽ đủ nên không hở); móng hai chân lùi về sau một chút.
  - Bỏ mắt, miệng cũ vì đầu mới đã vẽ mặt.
- animation cả 5 clip, dựng bằng script `reskin/thuy_<id>/dung_anim.py` (ghi `anim_moi.json` rồi chạy `anim_moi.py`):
  - dạng 1 (gốc xoay ở tâm hình, nên lộn vòng quanh tâm):
    - đứng lơ lửng nhấp nhô; đánh thường húc sừng (khung 18);
    - chiêu mana: tia 0,7 từ trán giữa hai sừng;
    - chiêu cuối (viết lại cùng ngày, xem dưới): xoay một vòng trong lốc nước, tụ cầu nước giữa hai sừng, gật đầu bắn thẳng.
  - dạng 2 (gốc ở giữa hai móng):
    - đứng thở; đánh thường phi tới húc (khung 18);
    - chiêu mana: tia 1,0 từ trán;
    - chiêu cuối (viết lại): chồm ngửa, tụ cầu lớn giữa hai sừng, dậm xuống ném cầu bay vòng cung, cột sóng FX07 sau đối thủ.
  - dạng 3:
    - đứng khom thở, ba vây lớn đung đưa lệch nhịp; đánh thường vồ húc (khung 18);
    - chiêu mana: tia 1,4 từ ngọc trai trên mũ;
    - chiêu cuối (viết lại): bắn liên hoàn hai cầu nhỏ từ ngọc, rồi tụ cầu lớn trước mũ bắn ra, sóng thần FX07 sau đối thủ.
  - **Chiêu cuối viết lại không lao** (người dùng dặn 2026-11-06: "không làm kiểu húc", đổi sang tụ cầu nước rồi bắn):
    - cả ba dạng 50 khung, bỏ `lunge`, khai `far` (dạng 1 [670, 80], dạng 2 [800, 78], dạng 3 [1150, 130]: khoảng 4 lần chiều
      cao về phía trước, ngang giữa thân đối thủ); cầu lớn nổ ở chỗ đối thủ khung 27 = 55% clip, là lúc trận tính trúng;
    - thân phải dời ít (trung bình góc trên trái ≤ 60 sau trượt 5 khung: 30, 48, 17), không thì trận lấy đỉnh dời làm lúc trúng;
    - cầu tụ là FX10 (gói `tieu_y_fx`) gắn mảnh đầu, có vòng xoáy FX01, giọt FX04 bay về, lấp lánh FX05; `fx_dir` thêm gói
      Tiểu Y trước gói Giọt Sương;
    - cầu bay gắn `pin` vào đúng điểm cầu tụ trên mảnh đầu ở khung bắn, toạ độ đích tính bằng hàm `where()` trong
      `dung_anim.py` (lặp lại phép biến đổi của `anim_moi.py`: gốc dời, xoay, co giãn quanh pivot rồi tới khớp đầu), nên cầu rời
      đúng chỗ rồi tới đúng tâm vụ nổ;
    - dạng 1: khung 5–14 xoay một vòng tại chỗ, 14–22 cầu tụ giữa hai sừng (ngả ra sau nên cầu ở sau đầu), 23 gật đầu bắn,
      bay thẳng 4 khung;
    - dạng 2: khung 11–19 chồm ngửa (xoay −24° quanh hai móng), móng trước cào so le, cầu cỡ 54 tụ; 21 dậm xuống (nước bắn ở
      móng, vòng sóng nhỏ), hất đầu ném, cầu bay vòng cung cao 150 trong 6 khung; nổ kèm cột sóng FX07;
    - dạng 3: cầu nhỏ cỡ 36 rời ngọc ở khung 9 và 14, nổ nhỏ ở chỗ đối thủ khung 13, 18 (chỉ là hình, trận vẫn tính trúng một
      lần ở khung 27); cầu lớn cỡ 92 tụ trước mũ (không che mắt, mõm), bắn ở khung 23; nổ kèm sóng thần FX07 cỡ 220;
    - đánh thường (1_4) cả ba dạng vẫn húc sừng;
    - thử: menu `PokiClash/Thử/Ma Kết ra trận: húc, bắn tia, cầu nước ở 3 dạng (đang Play)`, ảnh vào
      `Temp/PokiShots/ma_ket_combat/`.
  - Bài học:
    - khung trúng của trận thường trễ nhát húc 1–2 khung, vì hình nổ nước phía trước (FX03, FX05, FX04) giữ trung bình góc trên trái ở xa vài khung;
    - sửa bằng cách cho con lao tới gần đích sớm hơn và rút về nhanh hơn ngay sau nhát húc;
    - kiểm bằng script mô phỏng `AolaActor.MotionOf` (trung bình tx, ty mọi hình trừ bóng, trượt 5 khung, dời > 60 thì trúng ở đỉnh);
    - xoay hai vòng phải làm tại chỗ (dx nhỏ): lúc xoay 180° góc trên trái các hình văng xa, nên nếu xoay khi đang lao thì đỉnh rơi vào giữa vòng xoay;
    - khoá gốc mỗi khung khi xoay liên tục: nội suy smoothstep giữa hai khoá thưa làm vòng xoay khựng ở từng khoá.
- vào game cùng ngày:
  - `heroes.json`: `ma_ket` đổi `aola` sang `thuy_758`, `thuy_759`, `thuy_760`;
  - menu Nhập dữ liệu, rồi "Nhập dạng aola có nguồn mới hơn bản trong project" (nhập mới đúng 3 dạng, atlas 0,8 triệu điểm ảnh);
  - Chụp thử prefab: `Library/PokiHeroShots/ma_ket.png` đủ ba dạng (chân dung, đứng, đỉnh đòn đánh, khung trúng chiêu cuối).

**Concept đầu tiên được chốt** (2026-11-02): Giọt Sương dạng 1, `inbox/giot_suong_1/concept_duyet.png` (bản giáp ngực trơn, găng giáp bạc, kiếm chắn tay vàng). Chép thành **ảnh mốc style** `refs/style_anchor.png`: concept các tướng sau đính thêm ảnh này (lấy nét và độ chi tiết, không lấy thiết kế).

## 2. Rig

- **Mỗi tướng là một dòng tiến hóa của aola** (`GD_Claude/13_DanhSachTuong.md`); mỗi dạng vẽ đè lên rig của đúng con aola ứng với dạng đó. Chỉ con vector (`fightassets/pet<id>.swf`) làm được.
- **Con mới khác hẳn con gốc, nhưng tay chân trùng rig**: cùng số chi, khớp cùng chỗ, chi chĩa cùng hướng, đầu nào nối với gì giữ nguyên.
- Hai loại nhóm:
  - **đổi dáng** (đầu, tai, mào, đuôi, phụ kiện): viền theo concept, to hơn được; chỉ đầu khớp ở nguyên chỗ;
  - **giữ viền** (thân, tay, chân): giữ viền hình gốc, lấy màu, chi tiết, nét từ concept.
- **Vũ khí, đồ cầm tay**: vẽ riêng thành một mảnh thêm (không có ảnh gốc); bàn tay vẽ nắm chuôi. Claude gắn mảnh vào mảnh cẳng tay khi ghép, nên vũ khí đi theo tay ở mọi khung. Animation vẫn là của con gốc: con gốc không chém thì kiếm chỉ đi theo tay.
- Ảnh rig của mỗi dạng ở `refs/<hệ>/<mã>/`: `Silhouette.png`, `RegionMap.png`, `Rig_Numbered.png`, `orig/Nxx.png` (hình gốc từng nhóm, vuông 1024, nền trắng, đúng chỗ trên rig). Dựng bằng công cụ AolaRipper (`part_map.py`, `region_map.py`, `orig_refs.py` theo `regions.json`, `groups.json` ở `<aola>/reskin/<hệ>_<id>/`).
  - Các bước dạng mới (làm cho Ma Kết 2026-11-06):
    1. clip đứng = `states.1_1.clip` trong `reskin/pet<id>_parts/timeline_front.json`;
    2. `part_map.py reskin/pet<id>_parts/svg/DefineSprite_<clip>/1.svg reskin/pet<id>_parts/front_idle --scale 4`;
    3. `part_context.py` để nhận từng mảnh;
    4. `region_map.py` ra `reskin/<hệ>_<id>/refs/<id>_Front_*.png`.
  - Chưa có script chép sang PokiWar: cắt `Silhouette`, `RegionMap`, `part_map.png` (thành `Rig_Numbered.png`) theo khung bao của bóng xám, chừa lề trắng 6% cạnh dài; `orig/` chép nguyên.
- `<aola>`: máy này `E:\ProjectAtomik\aola` (có `reskin/pet<id>_parts` của 83 dạng và `reskin/thuy_7` đã ghép; `regions.json`, `groups.json` của #7, #8, #9 chỉ có ở máy kia, ảnh rig dựng từ đó đã có trong `refs/thuy/giot_suong_1..3`); máy kia `D:\Aola-20261029T161238Z-1-001\Aola\AolaRipper\AolaRipper`.

## 3. Viết prompt

- Xem từng mảnh trong ngữ cảnh, ghi bảng giải phẫu: mảnh là gì, hai đầu nối gì, chĩa hướng nào; trái, phải theo người xem.
- Concept: mục **KEEP FROM THE RIG** (số phần, chỗ khớp, hướng chi, cỡ thân tay chân) và **CHANGE** (từng vùng thành gì).
- Nhóm: nói rõ đầu nào của chi là gì ("TOP end = shoulder", "hand at the BOTTOM end") và cái **không được vẽ**. Hình mảnh cũ thắng cách hiểu thông thường.
- **Độ dày viền theo pixel từng nhóm**: ảnh mẫu mỗi nhóm phóng một tỉ lệ khác nhau, ghi chung một tỉ lệ thì ghép xong viền lệch nhau.
  - tỉ lệ phóng = cỡ vật trong `orig/Nxx.png` ÷ cỡ vùng đó trong `RegionMap.png`;
  - viền đích ≈ 0,85% chiều cao cả con trong `RegionMap.png` (khoảng 3 px khi con cao 350 px trong game);
  - số px = viền đích × tỉ lệ phóng. Rig #7: N01, N02 khoảng 10 px; N07 khoảng 25 px; N03–N06, N08 khoảng 28 px; mảnh kiếm vẽ riêng khoảng 18 px.
- Không nhắc tên game nào trong prompt.

## 4. Gói gửi GPT

- `build.py` giữ bảng `FORMS` (thiết kế, giải phẫu, prompt concept, prompt từng nhóm, mảnh thêm, thứ tự gen thử) và sinh `gui_gpt/<mã>/`:
  - `luot_1_concept.txt`: ảnh mẫu là bóng xám, bản đồ vùng, tờ mẫu thiết kế (`refs/style/style_sheet.png`, 8 tướng aola, dựng bằng `tools/make_refs.py`), ảnh mốc nét vẽ (bản đồ); dạng 2, 3 của một dòng đính thêm concept đã duyệt của dạng 1 (khoá `prev` trong `FORMS`: giữ màu, mũ, mặt, giáp, nét để cả dòng ra cùng một con lớn lên); GPT lưu `inbox/<mã>/tai_ve/concept.png`;
  - `luot_2_nhom_manh.txt` (chỉ dựng khi đã có concept duyệt): ảnh mẫu là ảnh gốc từng nhóm và concept đã duyệt; GPT vẽ một nhóm mỗi lượt theo thứ tự (2 nhóm gen thử trước, chờ soi), lưu mỗi nhóm thành `inbox/<mã>/tai_ve/<Nxx>.png`;
  - `HUONG_DAN.md`: tiếng Việt, file prompt từng lượt, đường dẫn và mô tả từng ảnh mẫu, kiểm từng ảnh, câu sửa nhanh.
- Người dùng chỉ gửi GPT đường dẫn file prompt (dặn 2026-11-03). File prompt mở đầu bằng danh sách ảnh mẫu kèm đường dẫn đầy đủ (GPT tự mở), rồi chỗ GPT tự lưu ảnh; trùng tên thì GPT thêm `_2`, `_3`.
- Đường dẫn trong gói tính từ chỗ đặt `build.py`, nên chạy được trên cả hai máy.
- `py -3 -I build.py <mã> ...` chỉ dựng các dạng đó; không có mã thì dựng lại mọi gói. Dạng khai `"anchor": True` thì concept đính thêm ảnh mốc style `refs/style_anchor.png`, vì ảnh mốc này chưa được đính tự động cho các dạng khác.
- Thư mục `1_concept/`, `2_nhom_manh/` trong gói cũ là cách kéo thả trước đây, không dùng nữa.
- Đính hình aola cho GPT: người dùng cho phép ("cứ đính hình vào", 2026-11-02).

## 5. Claude duyệt

**Concept** ("duyệt concept <mã>"):
- nét vẽ tay trên giấy như bản đồ (bút mực, chì sáp), tô phẳng: không mảng sáng tối, không điểm sáng, không bóng, không bóng loáng; thiết kế gọn, không chép con aola nào; vẻ chiến;
- đủ, đúng chỗ như rig: số chi, khớp, hướng chi, bàn tay ở đầu dưới;
- duyệt xong: lưu `inbox/<mã>/concept_duyet.png`, chạy lại `build.py` để gói lượt 2 có concept.

**Nhóm** ("soi thử <mã>" cho 2 nhóm đầu, rồi "ghép <mã>"):
- chồng ảnh lên `orig/Nxx.png`: vật đúng chỗ, đầu khớp đúng chỗ cũ, bàn tay bàn chân đúng đầu;
- nét như concept, viền dày gần số đã ghi; nền trắng, không viền trắng quanh mảnh.
- lỗi nhẹ thì Claude tự sửa bằng `tools/sua_manh.py`, khỏi gen lại (ảnh GPT giữ nguyên, ảnh sửa mới hơn nên bộ ghép lấy nó):
  - cả nhóm vẽ lệch chỗ nhưng dáng đúng: `doi <ảnh> <dx> <dy>` ra `<Nxx>_doi_cho.png`;
  - viền ngoài mỏng hơn số đã ghi: `vien <ảnh> <px>` (nới thêm px) ra `<Nxx>_vien_day.png`;
  - đo viền: chiều dày nét mực sát nền ngoài, so với số px của nhóm.
  - Tiểu Y dạng 1 (2026-11-04): N01 lệch lên 180 px; N04, N06, N07 viền 10, 11, 10 px (cần 13, 18, 16) nên nới thêm 3, 7, 6 px.

## 6. Ghép (Claude)

Công cụ ở repo aola (`<aola>/tools/`), cấu hình mỗi dạng ở `<aola>/reskin/<hệ>_<id>/ghep.json` (mẫu: `reskin/thuy_7/ghep.json`):
- `groups`: nhóm → mảnh (số theo thứ tự vẽ khung đứng đầu, như `Rig_Numbered.png`), mảnh ẩn (`drop`: mắt, má, miệng cũ khi đầu mới đã vẽ mặt);
- `extra`: mảnh vẽ riêng gắn vào một mảnh (kiếm: `attach`, góc lưỡi, độ dài theo chiều cao con);
- `variants`: hình biến thể thay một hay nhiều mảnh (ví dụ một hình chứa cả hai tai lúc vẫy tai); `drop_chars` (mặt hoảng, mắt nhắm), `keep_chars` (hiệu ứng). Liệt kê biến thể bằng cách đếm hình không có ở khung đứng đầu rồi xem từng hình. Có con (như #8) thay đuôi, vây, mào bằng biến thể ngay ở clip đứng, nên phải soi cả clip đứng.
  - hình chứa nhiều mảnh rời mỗi mảnh xoay riêng (bốn vây của #8): thêm `"split": true` để mỗi mảnh khớp riêng tâm, góc, cỡ; khớp khung bao chung làm mảnh rời khỏi chỗ.
  - biến thể khác dáng hẳn (thân đuôi uốn của #8): khớp khung bao với `squash` lớn hơn (2,6); muốn đẹp hơn thì cho GPT vẽ lại từng biến thể.
  - biến thể vẽ lại một mảnh, cùng cỡ nhưng xoay trong khung (đầu, thân, chân, đuôi của #9 lúc đánh, chiêu): `"local": true` để khớp theo khung riêng của hình (giữ góc xoay); hình dài mảnh hơn mảnh gốc thì thêm `"squash"`. Khớp khung bao chung làm mất góc xoay (chân thành cột dựng đứng, vây phồng tròn).
- Mảnh vẽ lại sau khi ghép: lượt 3 (`luot_3_ve_lai.txt`, khoá `redo` trong `FORMS`), GPT lưu `<mã>_ve_lai.png`; bộ ghép lấy ảnh mới nhất của mỗi nhóm.

Chạy `py -3 -I tools/ghep_nhom.py reskin/<hệ>_<id>`:
1. tách nền trắng nối với mép, mép nửa trong suốt tính lại từ độ trắng;
2. khớp ảnh mẫu nhóm với mảnh gốc ở khung đứng đầu (tỉ lệ, độ dời; in IoU, cần gần 1);
3. nhóm nhiều mảnh: chia ảnh theo vùng mảnh gốc gần nhất, chồng một dải ở khớp;
4. dựng lại mọi khung của 4 clip, gắn mảnh thêm; ra `sprites/`, `export/anim.json`, `ghep_log.json`.

Sau đó:
- `tools/portrait_png.py reskin/<hệ>_<id>` cho chân dung;
- **soi**: `tools/so_sanh_reskin.py <hệ>_<id> goc_<id> <ảnh> 6` (mỗi clip 6 khung, hàng trên gốc, hàng dưới mới) và phóng to vài khung xem khuỷu, hông, cổ, chỗ cầm vũ khí; không còn hình cũ lọt vào;
- đổi `aola` của dạng đó sang `<hệ>_<id>` ở `Assets/02 Data/Json/heroes.json` rồi menu `PokiClash/Nhập dữ liệu` (làm ở Unity, người dùng dặn 2026-11-03; bản web chỉ sửa khi được yêu cầu); nhập lại hình thành prefab như dưới;
- chụp trong game (menu `PokiClash/Thử/Thanh tiến hóa: chụp hộp chi tiết ở các mốc`).

Bộ ghép này thay cho trình chỉnh sửa cũ (`so_sanh.html`, `adjust.json`) của máy kia; muốn chỉnh tay thì sửa `ghep.json` (góc, độ dài kiếm, độ chồng khớp) rồi chạy lại.

Hình ghép chỉ có ở máy đã ghép (repo aola không mang `reskin/<hệ>_<id>` sang máy kia): ghép xong phải nhập lại thành prefab ở máy đó (menu `PokiClash/Tướng/Nhập hình tướng aola thành prefab`), xem `Library/PokiHeroShots/<tướng>.png` (menu `PokiClash/Tướng/Chụp thử prefab tướng`), rồi commit `Assets/03 Art/Heroes/Resources/<hệ>_<id>/`. Máy không có thư mục ghép thì bộ nhập giữ hình đã nhập, không đè bằng hình gốc.

**Animation viết lại (người dùng dặn 2026-11-03: ghép xong thì sửa animation cho khác bản gốc aola).** `tools/anim_moi.py` dựng lại clip theo khớp từ dáng đứng đầu: mỗi mảnh xoay quanh khớp nối với mảnh cha (khớp tự tìm ở chỗ chồng lên mảnh cha, mảnh chồng nhiều như bắp tay thì ghi `pivot` tay), gốc dời, xoay, co giãn (co ngang qua 0 để xoay người), vệt mờ theo vũ khí, đưa mảnh lên trên trong vài khung. Cấu hình `reskin/<hệ>_<id>/anim_moi.json`; `ghep_nhom.py` tự chạy nó sau khi ghép (ghép lại không mất). Giọt Sương (2026-11-03):
- dạng 1 đánh: giơ kiếm dựng bên mặt (không giơ qua đầu: đầu to, tay ngắn nên che mặt), lao tới, chém bổ xuống;
- dạng 2 đánh: giơ kiếm lên trước, lao tới, chém chéo xuống;
- dạng 3 đánh: lao tới, xoay người (lật ngang) quất đuôi lưỡi kiếm (đuôi là một mảnh cứng nối thấp sau lưng, vung qua đầu kiểu bọ cạp thì quét ngang qua ngực);
- cả ba: clip đứng và trúng đòn mới; clip chiêu giữ bản gốc. Khung lao xa nhất (game lấy làm lúc trúng đòn) trùng nhát chém: 19, 19, 20.
- thử: menu `PokiClash/Thử/Clip đánh Giọt Sương: chụp các dạng (đang Play)`.

Tiểu Y dạng 1 (`reskin/thuy_1319`, người dùng dặn 2026-11-04), viết lại cả 5 clip:
- đứng 40 khung (bằng vòng lốc nước gốc để nước chạy liền); trúng đòn bật lùi;
- đánh thường: lùi lấy đà, lao tới, đinh ba xoay ngang đâm thẳng, nước bắn ở mũi (đỉnh lao khung 19);
- chiêu mana (clip bắn 1_5 dựng mới, con gốc không có): chĩa đinh ba ngang về phía địch, tụ nước ở mũi, bắn tia ở khung 12 từ mũi đinh ba;
- chiêu cuối (1_6, không lao): giơ đinh ba lên trước mặt, tụ quả cầu nước có vòng xoáy, vung tới ném (khung 23), cầu bay ra xa rồi nổ nước ở khung 27 (= 55% clip, lúc trúng);
- hiệu ứng: quả cầu nước FX10 vẽ riêng (gói `gui_gpt/tieu_y_fx/`, `build_fx.py tieu_y_fx`, thay bong bóng FX06 còn vệt sáng trắng), còn lại dùng gói `giot_suong_fx` (vòng xoáy FX01, giọt FX04, lấp lánh FX05, nổ nước FX03, vòng sóng FX08). `fx_dir` của anim_moi.json là danh sách hai gói, gói Tiểu Y trước;
- hình vẽ xa hơn 1,5 lần chiều cao về phía trước là hiệu ứng ở xa: trận kéo về chỗ đối thủ (AolaActor). Khoá `"far": [x, y]` của clip trong anim_moi.json ghi tâm vụ nổ (ra `far_center` trong anim.json), để cầu bay dọc đường không kéo vụ nổ lệch khỏi thân đối thủ.
- Tiểu Y dạng 2 (Y Trạch, `reskin/thuy_1320`, cùng ngày): cùng bộ đòn, người dùng dặn đâm lực hơn và quả cầu to hơn.
  - Đánh thường: đinh ba xoay ngang kéo lùi hẳn ra sau (mũi cạnh nắm tay, không che mặt), lao nhanh 4 khung, đinh ba trượt qua nắm tay đâm thẳng, vệt mờ, nước nổ to ở mũi.
  - Chiêu mana: tia cỡ 1,4.
  - Chiêu cuối: đẩy đinh ba lên cao, tay phải giơ triệu nước, cầu FX10 cỡ 100 (gấp khoảng 1,6 lần dạng 1 trên màn hình), `far` [1100, 150].
  - GPT vẽ viền chỉ bằng 0,4–0,6 lần số đã ghi ở mọi nhóm: nới bằng `sua_manh.py vien` lên khoảng 0,85 lần.
  - Ba lọn tóc trước của bờm (45, 46, 50) GPT vẽ to hơn mà che mặt: `"behind"` trong anim_moi.json đưa ra sau đầu.
  - Hiệu ứng nước tự chạy có màu nhuộm cộng xanh và glow của aola: bộ ghép bỏ ở hình đã tô lại.
- Công cụ thêm hôm đó: khoá mảnh `[khung, góc, dx, dy]` (dời mảnh, như đâm đinh ba); mảnh tự chạy (lốc nước, vòng nước) phát lại khung con của clip đứng ở mọi clip viết lại; `anim_moi.py` dựng từ `anim_ghep.json` nên chạy lại một mình không cộng dồn; bỏ hình không clip nào dùng; `ghep.json` `"to_nuoc"` tô lại hình nước (`tools/to_nuoc.py`).

**Trong trận (người dùng dặn 2026-11-03):**
- con đang ra đòn nằm trên con kia (StageView.Play);
- clip CHIÊU (1_6) chỉ dùng cho tuyệt kỹ; khoá `"lunge": true` trong anim_moi.json thì trận kéo nó lao tới đối thủ như đòn đánh. Giọt Sương: dạng 1 lao tới xoay vòng chém, dạng 2 lao tới chém bổ, dạng 3 lao tới xoay người quật đuôi lưỡi kiếm (đòn đánh thường dạng 3 đổi thành vồ tới dậm hai chân trước);
- chiêu dùng mana bắn tia: **mặc định của mọi tướng, quái thường và phần lớn mini boss** (người dùng: chỉ số ít boss làm riêng, khai `"mana": "clip"` trong anim_moi.json thì phát clip CHIÊU). Dạng có clip bắn `1_5` (20 khung, trúng ở khung 12) + khoá `"cast"` (mảnh, điểm chỗ bắn, khung, cỡ tia) thì dùng đúng clip và chỗ bắn đó; không có thì đứng nhún về phía đối thủ, tia từ trước ngực, cỡ to dần theo dạng (0,7 tới 1,4; một dạng: 1; boss ×1,2). StageView.Beam phóng prefab `Items/TiaNuoc` (ảnh `Assets/03 Art/Fx/tia_nuoc.png` do `build_fx.py --xuat` cắt từ ảnh GPT FX09, menu `PokiClash/Prefab/Sàn đấu: tia nước của chiêu bắn`); tướng hệ khác tạm nhuộm màu hệ tới khi có ảnh tia riêng từng hệ;
- hiệu ứng vẽ tay của tuyệt kỹ: gói GPT `gui_gpt/giot_suong_fx/` (`build_fx.py`); clip có hiệu ứng nhưng chưa có ảnh thì để `"fx_off": true`;
- thử: menu `PokiClash/Thử/Giọt Sương ra trận: đánh, bắn tia, chiêu cuối ở 3 dạng (đang Play)`.

## 7. Viền trắng giấy xé (Unity, chưa làm)

- Đã có shader `PokiClash/StickerOutline` (`Assets/03 Art/Shaders/StickerOutline.shader`): tướng aola render ra RenderTexture (`AolaSticker`), shader vẽ viền trắng rồi viền mực quanh **cả hình**.
- Kiểu giấy xé: thêm nhiễu theo vị trí để bề rộng viền trắng lồi lõm, mép răng cưa nhỏ, có thể thêm bóng mờ dưới giấy.
- Nếu muốn **viền giấy quanh từng mảnh** (kiểu con rối giấy, lộ mép trắng ở khớp): nướng vào từng PNG mảnh khi xuất (nới alpha, mép răng cưa), không làm bằng shader trên cả hình.

## 8. Thư mục

| Đường dẫn | Chứa gì |
|---|---|
| `ArtGen/Heroes/build.py` | Bảng các dạng, prompt, bộ sinh gói |
| `ArtGen/Heroes/gui_gpt/<mã>/` | Gói gửi GPT: `luot_1_concept.txt`, `luot_2_nhom_manh.txt`, `HUONG_DAN.md` (sinh ra, không sửa tay) |
| `ArtGen/Heroes/refs/<hệ>/<mã>/` | Ảnh rig: bóng xám, bản đồ vùng, rig đánh số, `orig/Nxx.png` |
| `ArtGen/Heroes/refs/style/` | Tờ mẫu thiết kế từ hình aola (`style_sheet.png`); `parts_example.png` của cách bộ mảnh rời, không dùng nữa |
| `ArtGen/Heroes/tools/` | `make_refs.py` (tờ mẫu), `explode.py`, `sua_manh.py` (dời ảnh nhóm, nới viền) |
| `ArtGen/Heroes/inbox/<mã>/tai_ve/` | Ảnh GPT tự lưu (`concept.png`, `<Nxx>.png`), Claude chưa duyệt |
| `ArtGen/Heroes/inbox/<mã>/concept_duyet.png` | Concept đã duyệt |
| `ArtGen/Heroes/refs/style_anchor.png` | Ảnh mốc style: concept Giọt Sương dạng 1 đã chốt |
| `ArtGen/Heroes/inbox/<mã>/Concept*.png` | Concept của các lần trước, không dùng nữa |

## 9. Tự động bằng Codex và bộ ghép ở máy ổ D (2026-11-07)

Người dùng chọn (2026-11-07): Claude tự gọi Codex gen ảnh (cách 1), làm trọn một tướng (mức B); người dùng duyệt concept bằng chữ trước khi gen và xem trang so sánh cuối. Làm 3 dòng một lô.

- **Gen:** `py -3 -I tools/gen_codex.py <file prompt> [--steps N01,N02] [--note "câu sửa"]`. Gọi `codex exec` (gói ChatGPT, không cần API key; `codex.exe` tìm qua gói AppX), đính ảnh mẫu đúng thứ tự, chạy ở gốc PokiClash, liệt kê ảnh mới, ghi `inbox/<mã>/gen_log.jsonl`. Khoảng 2 phút một concept, 1,3 phút một nhóm. Chạy từng lệnh một. Codex đọc `AGENTS.md` (đã sửa cho khớp luật này).
- **Tự kiểm:** `tools/kiem_anh.py <ảnh> --orig refs/.../orig/Nxx.png --px N`: nền, đốm trắng, độ trùng, độ lệch. Số đo viền chỉ để tham khảo (lẫn màu đậm của thiết kế); vẫn phải xem bằng mắt.
- **Rig, ghép, so sánh, animation** ở `<aola>/tools/` (máy ổ D, Claude viết lại vì bộ của máy công ty chưa có ở đây; trùng tên với bộ máy công ty, khi đồng bộ repo aola thì người dùng chọn giữ bản nào):
  - `dung_rig.py reskin/<hệ>_<id>`: ảnh rig không cần Chrome (ghép `chars/*.png` theo `frames.json`), `part_context`, `region_map` (cần `regions.json`), `orig_refs` (cần `groups.json`), chép `Silhouette`, `RegionMap`, `Rig_Numbered`, `orig/` sang `refs/<hệ>/<mã>/` (cần `ghep.json` có `code`, `elem`). Mảnh 2 của nhiều rig là lớp viền đen cả con nằm sau cùng: bỏ khỏi vùng (`exclude`) và khi ghép (`drop`).
  - `ghep_nhom.py reskin/<hệ>_<id>`: ảnh mới nhất mỗi nhóm; tách nền; khớp dời nhỏ; chia nhóm theo mảnh gần nhất, mảnh dưới có dải chồng ở khớp; mảnh nằm trong mảnh khác (mắt trên đầu) gộp và ẩn; tự đoán biến thể (tách cụm, dư ảnh dựng lại từ dáng mới, bỏ mặt cũ và vụn nhỏ), tờ `ghep_bien_the.png`; mảnh thêm (vũ khí) `extra` có `attach`, `angle`, `length`, `grip_frac`, `top`. `ghep.json` `groups.<Nxx>.drop` bỏ mảnh trong nhóm (vành vòm Tám Tay). Ra `export/anim.json` và `anim_ghep.json` (kèm `idle_parts`), chân dung; có `anim_moi.json` thì chạy luôn `anim_moi.py`.
  - `anim_moi.py`: dựng lại clip từ dáng đứng đầu; cây khớp tự dò theo nhóm (mảnh chính chạm thân thì nối vào thân, mảnh rời cùng nhóm cùng cha, xúc tu cạnh nhau phải ghim `parent`); khoá `root` (quanh chân) và từng mảnh (quanh khớp); xoay cả con thì khoá ở mảnh gốc (quay quanh tâm thân), xoay ở `root` thì quay quanh chân, góc trên trái văng xa làm trận tính trúng sai; in khung trúng như `AolaActor.MotionOf` (bỏ hình ở xa quá 1,5 lần chiều cao). Khoá `cast`, `far`, `lunge`, `mana` như trận đọc.
  - `so_sanh_reskin.py <mới> <gốc> <ảnh> [n] [--frame clip:i]`: mỗi bản một khung nhìn, cùng tỉ lệ.
- Thử nghiệm ở thư mục không có trong heroes.json (`reskin/thu_ghep_7`): ghi vào `thuy_*` đang dùng thì menu "nguồn mới hơn" sẽ đè prefab.

## 10. Đảo Thủy lô 2: 5 dòng boss (2026-11-07 đêm, người dùng ủy quyền làm một mạch, Claude tự chốt concept)

Boss đảo Thủy: Vây Lam (ải 30), Kuba (40), Thương Lam (50), Huyền Vũ (60), Lam Quân (70, boss cuối). Đặc tả gọn từng dạng ở `tools/lo_thuy2.py` (sinh regions, groups, ghep, mục FORMS vào `forms_thuy_lo2.json`, build.py nạp thêm); animation boss theo khuôn `tools/anim_lo2.py` (đứng, trúng đòn, đánh lao có hiệu ứng, bắn tia có tụ nước, chiêu cuối 44 khung trúng ở khung 24 với 6–8 hiệu ứng); `tools/chay_lo2.py` chạy trọn một dạng (chờ concept, duyệt, gen nhóm, ghép, so sánh).
- **Vây Lam** (cá mập rẽ sóng): lưng xanh coban đốm trắng, bụng trắng, vây viền vàng nghệ, mắt hổ phách. Dạng 1 cá mập con cuộn trong trứng bong bóng; dạng 2 mũ vỏ ốc vàng có sừng, hai mũi tên nước bay hai bên; dạng 3 nhiều vây lưỡi sóng nước bay quanh. Chiêu: sóng lưỡi liềm, sóng thần.
- **Kuba** (mai cứng kim cương): ốc mượn hồn da cam san hô, tóc tảo tím, vỏ ốc xoắn vàng cát, khăn bọt biển, mắt xanh ngọc. Dạng 2 càng cam đỏ to, vỏ gai; dạng 3 vỏ mọc kim cương trắng xanh. Chiêu: chui vỏ lăn húc, lấp lánh, vòng sóng đất.
- **Thương Lam** (rồng lam cánh băng): rồng biển trắng tuyết xanh băng, vân xanh mòng két, cánh vây băng gân xanh, sừng bạc, ngọc hoa tuyết. Chiêu: mảnh băng, sóng thần. Tia mana riêng: **tia băng** (`tia_bang`, văng mảnh băng dọc đường).
- **Huyền Vũ**: rùa da ngọc bích, mai đen than viền đồng vàng hoa văn lục giác, ngọc trai đen; dạng 3 thần rùa đứng râu trắng sừng đồng cầm mái chèo gỗ lũa. Chiêu: nhảy dậm, vòng sóng, sóng thần, xoáy. Tia mana riêng: **tia xoắn** (`tia_xoay`, vòng xoáy quay dọc tia).
- **Lam Quân** (tiểu tướng chuông đồng): rái cá biển tiểu tướng lông nâu mặt kem, mũ chuông đồng tua san hô, đinh ba san hô, chuông đồng lớn; dạng 2 đại tướng giáp đồng chuông khổng lồ; dạng 3 thống soái cánh cá đuối đen, chuông đồng đen, nước tím than. Chiêu: gõ chuông ba nhịp bật vòng sóng âm rồi lao đâm. Tia mana riêng: **tia triều đinh ba** (`tia_trieu`, vòng sóng âm nở dọc tia, rung sân mạnh).
- Tia riêng: gói `gui_gpt/thuy_boss_fx/` (FX11–FX15), xuất bằng `build_fx.py --xuat-boss` (máy không có OpenCV thì cắt nền bằng Pillow), gán bằng menu `PokiClash/Prefab/Sàn đấu: tia nước của chiêu bắn` (StageView.beamStyles, beamShard, beamVortex, beamSoundRing). anim.json khai `"cast": {"tia": "tia_bang"}`; `AolaActor.BeamStyle`, `StageView.Beam` đổi ảnh thân tia, giữ lâu hơn, dày hơn, thêm hiệu ứng riêng lúc bay và lúc trúng.
- **Soi sau ghép (lô 2, lỗi gặp và cách sửa, nên kiểm ở mọi dạng sau):**
  - *Cây khớp tự dò sai* khi rig có cánh, đuôi, áo choàng to: mảnh vung hay mảnh đung đưa kéo theo nửa thân (Thương Lam 3: cánh 20 gắn vào cánh 15, đuôi gắn vào cánh; Lam Quân 3: cả thân trên gắn vào áo choàng; Lam Quân 2: đầu và đinh ba treo vào chuông; chân treo vào vòng nước bay). Dấu hiệu: khung đỉnh đòn đánh mảnh văng tán loạn. Kiểm bằng dòng `khớp a<b` anim_moi in ra: mảnh vung, mảnh đung đưa, mảnh bay không được có con là thân, đầu, chân. Sửa bằng `parent` trong SPEC của `anim_lo2.py`, nhìn `refs/<hệ>/<mã>/Rig_Numbered.png`.
  - *Mặt bị thân đè*: các mảnh mặt cũ vẽ trên thân được gộp vào mảnh đầu, nhưng mảnh đầu gốc nằm dưới thân, nên mắt biến mất (Vây Lam 2). Sửa bằng `top=[<mảnh đầu>]` trong SPEC (khoá `top` mọi clip, trận chỉ dùng 1_1, 1_2, 1_4, 1_5, 1_6).
  - *GPT chép hoa văn của hình cũ* (Kuba 3: sọc quần thành cột sọc tím xanh). Gen lại một nhóm: `gen_codex.py <luot_2> --steps N05 --note "..."`, nói rõ mảnh là gì (tay, không phải thân) và cấm hoa văn; ảnh mới `N05_2.png` được ghép lấy vì mới nhất.
  - Hình biến thể "giữ hình gốc" trong cảnh báo của ghép chỉ ảnh hưởng clip không dựng lại; 5 clip trận dựng từ dáng đứng nên không lọt.
- Codex hết hạn mức gói ChatGPT giữa chừng (lỗi "usage limit", tầm 70 ảnh mỗi đợt): `chay_lo2.py` chờ 10 phút rồi thử lại, nhóm còn thiếu thì không ghép.
- Thử tia riêng trong trận: menu `PokiClash/Thử/Thương Lam | Huyền Vũ | Lam Quân ra trận` (đang Play, mở từ Boot), ảnh ở `Temp/PokiShots/<id>_combat/`. Lần soi đầu (2026-11-07): `anim_moi.py` chưa chép `cast.tia` nên cả ba vẫn bắn tia nước (đã sửa); Huyền Vũ 3 bắn từ đầu mái chèo sau lưng nên tia che kín đầu (đổi sang miệng); dạng cuối tia xoắn và vòng sóng âm quá to, che cả hai con (tia xoắn mảnh lại 0,85, vòng sóng âm theo `g`, vòng nổ lúc trúng nhỏ hơn thân).
