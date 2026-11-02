# GDD game Pokiwar

GDD cho game mới (PokiWar/PokiClash)

Core loop cốt lõi: Đánh ải nhận ball, dung ball để chơi pachinko dropball, nhận thưởng từ đó để nâng cấp pet, lên level pet => đi săn các quái cao cấp hơn. Những ải nào đánh boss (boss to hoặc các mini boss có cơ hội nhận mảnh tướng). Khi chinh phục được 1 ải ngươi chơi có thể afk cho đánh afk để nhận ball hoặc mảnh tướng (tỉ lệ thấp thôi, có thể khai thác reward ở đây)

Gameplay chính: 

### Vào màn chơi sẽ có 2 tướng đấu nhau. Người chơi có thể mang 1-3 tướng theo để đánh. Bên địch cũng có thể có tương tự từ 1-3 tướng.

## Lối chơi turn base theo lượt, khi vào đầu lượt người chơi có thể chọn swap tướng (địch cũng có thể làm vậy).

- Trong lượt chơi, người chơi sẽ được chọn 1 trong 3 thẻ bài random, sẽ có 5 lần chọn. Khi chọn xong thì 5 thẻ bài đó sẽ lần lượt bắt đầu được thực hiện. Ở đây, các thẻ bài có thể là: tăng chỉ số tấn công lên 10% trong lượt này, tăng 15% máu, hi sinh 30% máu hiện tại để tăng 20% chỉ số tấn công, hồi 30% máu, tăng 10 mana, tăng 10% phòng thủ, Hi sinh giảm 30% phòng thủ trong 2 lượt tiếp theo để được tăng 100% chỉ số công kích, nhận 10 nộ,…. nghĩ thêm sau
- Các tướng sẽ có 1-3 thẻ nội tại riêng biệt không liên quan tới các thẻ trên (1 hay 3 thẻ tùy thuộc gd). Các thẻ này sẽ là các thẻ skill trực tiếp hoặc passive skill, ví dụ như có những thẻ yêu cầu mana để lập tức đánh 1 đòn vào đối thủ gây dam, có thẻ cần full thanh nộ và mana để tung skill ultimate,.. các thẻ tung kĩ năng người chơi có thể dùng trong lượt của mình trước khi việc chọn random thẻ kết thúc. Các thẻ passive thì kĩ năng của nó sẽ kích hoạt tùy vào mô tả, có thể là xuyên suốt game đấu hoặc có những thẻ chỉ kích khi người chơi còn dưới 15% máu,… cái này thì nghĩ sau, bạn có thể gợi ý 1 vài thẻ. Các thẻ này sẽ có độ hiếm thu thập được khác nhau. Khi unlock tướng thì sẽ unlock các thẻ của nó ở level 1, người chơi có thẻ nâng cấp sức mạnh thẻ bằng cách thu thập chúng. Việc afk cày ải cugnx có thể kiếm được thẻ nhưng độ hiếm ra sẽ khó hơn rất nhiều. (phần này có thể kích mở rương, kích x2 tốc độ,… bằng reward hoặc kích mua iap)
- Khi kết thúc lượt, lần lượt các thẻ sẽ được dùng. Nếu trong lượt đó người chơi không kích hoạt ultimate thì sau khi đã kích đủ 5 thẻ chọn, tướng của người chơi sẽ tấn công tướng địch dựa theo các chỉ số được tăng/giảm vừa rồi. Nếu người chơi chọn ultimate, thì sau khi đã kích đủ 5 thẻ thì sẽ ra chiêu ultimate (không đánh thường nữa).

### Màn chơi kết thúc khi tất cả các tướng của 1 trong 2 bên hết máu/không thể hồi sinh nữa (Lỡ có thẻ hồi sinh skill của con nào đó)

## Hệ tộc:

- Game ban đầu sẽ chia 5 hệ chính ngũ hành xung khắc lẫn nhau. Sau mà phát triển thì thêm sau.

## Máy pachinko drop ball

Đây sẽ là thứ kiểm soát player progression và tăng sự phụ thuộc/độ dày coreloop. Khi quay máy pachinko, người chơi sẽ nhận ấc hạt kinh nghiệm. Các hạt này dùng để nâng cấp người chơi (kinh nghiệm là để nâng tướng còn thẻ là để tiến hóa tướng). Cấp của người chơi sẽ chính là cấp của tướng, càng level cao chỉ số càng mạnh.  Ngoài ra ở máy pachinko này sẽ có những ô nếu bóng rơi vào sẽ có người chơi mở rương để nhận quà (có thể là thẻ tướng hoặc lại ra ball tiếp để chơi pachinko). Để kiểm soát việc người chơi tích nhiều bóng thả cùng 1 lúc thì tối đa 1 lần cho người chơi thả 20 bóng hoặc 30 bóng nhưng sẽ có nút X là nhân phần thưởng lên cho người chơi. Ví dụ X1 các ô kinh nghiệm có thể là 5, 10, 15 thì x2 x3 sẽ là 10,20,30 hoặc 15,30,45. Các phần thưởng nhận được từ hòm cũng vậy (đa số các phần thưởng thì hòm sẽ lại là ball hoặc kinh nghiệm, rất hiếm khi ra thẻ, nếu có ra thẻ thì cũng chỉ ra những thẻ common/uncommon/rare, các tướng thẻ epic/legend tỉ lệ ra cực thấp). Các thẻ ra cũng sẽ không phải nhân theo số kia, miễn ra đủ thẻ là được. Ví dụ khi ở X1 mở hòm ra thẻ 1 common thì x5 sẽ không phải là ra 5 thẻ đó mà là ra 5 thẻ common nhưng chúng có thể khác nhau, cso thể là 2 thẻ này 3 thẻ khác,… áp dụng với các thẻ có rarity khác. Riêng thẻ legend có thể cho người chơi trúng lần đầu khi tiêu ball ở 1 mốc nào đấy nhưng từ đấy về sau sẽ cực kì khó có thể ra (0.001% hoặc 0.0001%) vì sau này progression lên số bóng thả sẽ nhiều hơn.

## Side Meta

- Đánh boss để nhận huy hiệu nâng cấp tộc hệ (học từ clash of critters): Đánh boss (theo hệ tộc) Nếu thắng 5 hoặc 10 ải (tùy tiến độ) sẽ nhận được huy hiệu hệ đó. Huy hiệu sẽ tăng 5% sức mạnh cho các tướng hệ đó. Huy hiệu về sau càng mạnh thì ải càng khó.
- Thu thập tiềm năng: những đá tiềm năng có thể lấy được từ việc mở hòm pachinko, 1 tướng có thể trang bị 4 tiềm năng. Các tiềm năng sẽ buff chỉ số cho tướng. Mỗi lần cho tướng vào khai phá tiềm năng sẽ mất đá tiềm năng. Những tiềm năng hiếm có tỉ lệ ra sẽ thấp. Cũng có thể build 1 side quest riêng đánh boss cày đá tiềm năng  nhưng người chơi sẽ phải chơi chứ không afk (tương tự với việc đánh để cày huy hiệu).
- Farm ball: có thể có 1 màn trang trại, người chơi có thể deploy 8 con tướng xuoogsn để chúng có thể trồng rau, chăn vịt,… 1 dạng afk lấy được ball. Tướng càng mạnh thì năng suất càng cao, thời lượng làm việc càng lâu (Nghĩa là 1 tướng khi được deploy sẽ làm việc được trong n giờ, hết thời gian thì chúng sẽ ngồi nghỉ không làm nữa, phải vào đổi tướng khác cho tướng kia nghỉ ngơi  (nghỉ nhanh tầm 15-30 phút hoặc 1 tiếng, sức này không liên quan gì đến việc cho tướng đi cày ải)