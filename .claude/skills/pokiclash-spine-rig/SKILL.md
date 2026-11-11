---
name: pokiclash-spine-rig
description: >
  Rig xương và làm animation cho nhân vật 2D từ ảnh (ảnh GPT vẽ hoặc một ảnh liền bất kỳ): cắt mảnh, khớp vị trí, dựng xương,
  mảnh cứng, một lưới hay nhiều lớp lưới có trọng số (uốn mềm, không hở khớp), viết animation (đứng, đánh, trúng đòn, chiêu,
  nhảy, đi/chạy), dựng khung soi, GIF, trang Spine Web Player; xuất JSON Spine 4.2 và định dạng riêng .atomik chạy trong Unity
  của PokiClash (importer + runtime AtomikPlayer). Dùng khi người dùng muốn rig xương / làm animation từ một hình, sửa hở
  khớp, uốn tóc, áo, đuôi, hoặc đưa animation vào Unity bằng .atomik.
---

# Rig xương từ ảnh và định dạng .atomik (thử nghiệm)

> Skill gốc: `skill-petclash` (nguyên tắc thiết kế, nhịp clip, khớp animation với hiệu ứng, hiệu năng, bảng kiểm; kèm bộ
> `VFX_KNOWLEDGE_BASE.md` và ba file ghi chú nghiên cứu). Đọc nó trước, rồi quay lại đây làm chi tiết.

Làm 2026-11-07 để đo khả năng rig tự động. **Không thay quy trình chính của game** (vẽ đè lên rig aola, xem CLAUDE.md mục
Hình tướng). Mọi thứ ở đây là thử nghiệm cho tới khi người dùng chốt khác. Ngoại lệ người dùng yêu cầu 2026-11-08: Rồng Giọt
(dạng 1 dòng Giọt Sương) vào game bằng .atomik, xem mục 10.

## 00. Có file Spine gốc làm mẫu thì PHẢI dịch ngược xem họ tách bộ phận thế nào (người dùng dặn 2026-11-11, bắt buộc)

Khi tướng làm theo một con gốc mà ta **có file Spine của nó** (`.skel` / `.json` + `.atlas` + ảnh; kho đã rút:
`D:\Ripper\SwordxStaff\web\assets\Monster\monster_<số>\`), thì **trước khi chia mảnh, viết prompt tờ mảnh hay cắt lớp** phải dịch
ngược file đó và chia mảnh của mình **theo đúng cách họ tách**. Không đoán từ ảnh chụp, không tự gộp các khúc thành một lưới chỉ vì
concept vẽ liền màu.

Lý do: tướng thứ 5 đảo Thủy (rắn sừng, 2026-11-11) bị trả hai lần vì tôi tự chia mảnh: lần đầu cắt cổ + bụng + vòng cuộn thành một
lưới liền; lần hai tách được vòng cuộn nhưng vẫn gộp cổ với ngực, thân sau với đuôi, cả đầu là một ảnh cứng. Người dùng: "bạn
không thể dịch ngược file spine gốc để xem họ tách mảnh như nào à?", "xem animation họ tách bộ phận như thế nào, dựa vào đó mà gen
theo thôi".

Cách làm (công cụ ở `ArtGen/Spine/mo_xe/`, chạy qua `quai/khoa.py chrome`):
1. `chay.py info <rig> <tên> info.json`: xương, slot (thứ tự vẽ), ràng buộc IK / path, clip.
2. `chay.py att <rig> <tên> att_goc.json`: **mọi hình của mọi slot** ở dáng gốc, kể cả hình không bật mặc định (bộ mảnh cho dáng
   khác). `chay.py att ... "anim=<clip>&t=<giây>"`: các hình đang bật ở một dáng của clip (dáng duỗi, lao, há miệng, trúng đòn).
3. `to_manh.py anh <rig> <tên> manh_anh.png`: mọi ảnh mảnh trong atlas (gỡ xoay), tên và cỡ.
   `to_manh.py dang <rig> <tên> att_goc.json manh_dang_goc.png`: cả con + viền từng mảnh, rồi **từng mảnh vẽ riêng** trên nền cả
   con mờ, ghi slot, ảnh, thứ tự vẽ, xương bám. Làm thêm cho dáng duỗi / lao / há miệng.
4. Mở các tờ đó ra XEM, rồi ghi vào ghi chú của tướng: bảng mảnh (tên, cỡ, là gì, đè lên mảnh nào, phần khuất vẽ ra sao, mép nào
   vẽ nét nhạt thay mực), cây xương, mảnh nào đổi ảnh ở clip nào.
5. Chia mảnh của mình **một – một theo bảng đó** (cùng số mảnh, cùng thứ tự vẽ, cùng kiểu xương bám), rồi mới viết prompt tờ mảnh
   cho GPT gen từng mảnh (mỗi mảnh vẽ đủ cả phần khuất, viền kín như mảnh của họ). Chỉ lấy cách tách và nhịp; hình là của mình.

Chỉ khi không có file Spine gốc mới tự chia mảnh theo các mục dưới.

**Gen mảnh "đúng chỗ, đúng cỡ" từ concept đã duyệt** (sò đột biến, 2026-11-11; người dùng trả bản cắt vá: "đập đi gen lại từ đầu",
"lòi xòm nhiều quá"): KHÔNG cắt mảnh ra từ ảnh concept rồi vá phần khuất bằng mã (tách theo màu, vẽ lòng miệng, nối vành, mí
mắt...): mép rách, mẩu vụn lòi ra ở mọi dáng há. Mỗi mảnh lớn của bảng mổ gen một lượt riêng, ảnh mẫu là concept, câu lệnh:
*"redraw image 1 with ONLY <bộ phận>, in the SAME POSITION and at the SAME SIZE; REMOVE <mọi thứ khác>; COMPLETE it into ONE
CLOSED SHAPE with an ink outline all the way around (<phần khuất vẽ thế nào>)"*. GPT trả mảnh trùng concept (lệch 0–1 px), không
phải dò tỉ lệ, ghép lại ra đúng dáng nghỉ đã duyệt. Mảnh nhỏ hoặc mảnh không có trong concept (mắt nhắm, môi, lưỡi dài) mới vẽ
trên tờ mảnh rời. Mã chỉ tách nền trắng, đặt chỗ, co giãn CẢ mảnh. Mẫu: `ArtGen/Spine/build_so_gai2.py`, `so_gai2.py`,
ghi chú `ArtGen/Spine/inbox/so_gai_ghichu.md` mục 8.

**CÁCH CHUẨN khi có rig gốc: vẽ mảnh ĐÚNG KHUNG từng part của rig, dùng nguyên lưới và chuyển động của rig** (rồng vây /
`monster_3458`, người dùng chốt 2026-11-11 sau nhiều bản tự dựng bị trả: "dịch ngược các part của con gốc được không?", "sao không
gen theo đó ghép lại rồi đổi pose là được", "gen theo y hệt đúng tỉ lệ luôn, đúng hướng"). Tự dựng xương, tự chia trọng số, tự viết
clip "theo nhịp con gốc" cho ra hết lỗi này tới lỗi khác (khớp hở, đuôi rời, cánh giả, khớp giật). Làm thế này:
1. **Xuất từng part của con gốc ra file riêng**, cắt đúng theo tam giác lưới của nó (atlas xếp theo đa giác nên ảnh vùng chữ nhật dính
   mảnh bên cạnh): `scan/monster_<số>/parts/<thứ tự>_<slot>.png` + tờ tổng. Đây là khung chuẩn: cỡ, hướng, hình bóng từng mảnh.
2. **Tờ hướng dẫn theo khung part** (`rong_vay.py nhom_part`, `nhom_part_het`): mỗi part một ô đúng cỡ ảnh vùng (phóng 2 lần; part
   nhỏ phóng 4), trong ô là HÌNH BÓNG của part (làm trơn nhẹ; không mang nét vẽ, hoa văn, màu của game gốc). Đã có mảnh của mình
   nằm đúng chỗ dáng gốc thì NƯỚNG nó vào khung (qua lưới của part: chỗ đứng ở dáng gốc → chỗ trong ảnh vùng), phần hình bóng còn
   thiếu tô hồng. Chưa có gì thì tô phẳng màu của mình.
3. **Prompt**: "giữ nguyên hình bóng từng part: cùng viền, cùng cỡ, cùng hướng, cùng chỗ trên tờ; giữ phần đã vẽ; thay phần hồng bằng
   phần nối tiếp". Codex giữ hình bóng rất sát (IoU 0,90–0,96). Khúc thân: dặn KHÔNG kẻ viền ở hai đầu cắt.
4. **Cắt**: mỗi part lấy đúng Ô của nó trên tờ (ô đó chính là khung ảnh vùng), tách nền trắng → `manh/part/<slot>.png`. Không dò chỗ.
5. **Rig = của họ**: đủ mọi xương của họ đúng cha – con và biến đổi riêng; mỗi slot dùng NGUYÊN lưới của họ (đỉnh, tam giác, uv,
   trọng số) với ảnh của mình (`gan_nguyen`). Điểm gắn tính bằng ma trận dáng gốc ĐÃ ÁP RÀNG BUỘC của họ (`att_goc.json`), vì xương
   chạy trên đường cong ở dáng gốc lệch biến đổi riêng tới ~9 đơn vị.
6. **Chuyển động = của họ**: `chay.py sample` cho biến đổi RIÊNG đã áp của mọi xương từng khung (trường `l`; ràng buộc đường cong đã
   được runtime nướng) → lệch so với dáng gốc (xoay, dời × tỉ lệ đơn vị, tỉ lệ nhân) → đặt lên đúng xương đó. Đừng tính ngược từ ma
   trận thế giới đã làm tròn (khớp nhỏ rung). Đổi hình (mắt nhắm) đọc ở trường `n`.
7. Mảnh của mình chưa vẽ theo khung part thì tạm gắn bằng `gan_goc` (lưới dày, mỗi đỉnh biến dạng như điểm tương ứng trên lưới của họ).
Hình vẫn phải là THIẾT KẾ CỦA MÌNH đã duyệt (khác hẳn con gốc; không tô lại y nguyên lông, bờm, hoa văn của họ). Xương, lưới, chuyển
động là của nhà phát hành game gốc, như phần aola: ghi rõ trong ghi chú tướng, dùng nội bộ, không đăng công khai.
Mẫu: `ArtGen/Spine/rong_vay.py`, `rong_vay_rig.py`, `build_rong_vay.py` (`build_part`, `build_part2`).

**Các khúc NỐI NHAU thì gen LIỀN một ảnh rồi cắt, không gen riêng từng khúc** (người dùng dặn 2026-11-11, rồng vây: "những khớp
nối thì gen cả con ra rồi cắt chứ không gen riêng không thì sẽ lệch"). Thân rắn / rồng, cổ – ngực – lưng – đuôi, tay hay chân nhiều
đoạn: nếu mỗi khúc là một lượt gen (hay một ô trên tờ mảnh) thì GPT vẽ bù phần khuất mỗi khúc một kiểu: vạch bụng lệch nhịp, bề dày
lệch vài px, đầu khúc có viền mực. Chồng mép lên nhau là thấy đường nối ngay, sửa bằng mã (xoá viền đầu khúc, cho phần chờm lấy màu khúc
dưới) vẫn bị trả. Cách đúng:
1. Tách vùng các khúc trên concept; dựng MỘT tờ hướng dẫn chỉ còn cả dải thân (mọi khúc), phần thân bị cánh, vây, đầu che tô hồng.
2. Gen MỘT ảnh "cả thân liền một ống, đúng chỗ, đúng cỡ, bỏ hết cánh vây đầu" (thay vùng hồng bằng thân chạy tiếp: vạch bụng cùng bề
   rộng, cùng nhịp).
3. Cắt khúc bằng mã ngay trên ảnh đó: mỗi điểm thân thuộc khúc có vùng lộ gần nhất; mỗi khúc lấy thêm ~34 px sang khúc kề, mép cắt mờ
   dần ~10 px. Lát cắt của cùng một ảnh nên vạch hai khúc trùng nhau từng điểm, không có viền mực ở chỗ nối.
4. Hai khúc kề phải **bám chung các đốt quanh chỗ nối** (nhóm xương mỗi khúc nới thêm một đốt về mỗi phía), không thì chỗ chờm trượt
   lên nhau khi đốt kế xoay.
5. Giấy trắng khép kín trong ảnh cả thân (lòng vòng cuộn) phải đục thành trong suốt (`doc_to` giữ nó như thịt của mảnh).
6. Chỗ thân chui ra sau chính nó (khúc đáy nấp sau ngực) ảnh liền không vẽ được: phần nấp lấy từ một lượt gen riêng, đặt khớp nối ở
   chỗ khuất.
Gen riêng chỉ dành cho bộ phận KHÔNG nối liền màu với cái khác (vây, sừng, mỏ, cánh, vũ khí). Mẫu: `ArtGen/Spine/rong_vay.py`
(`nhom_than`, `cat_than`), `build_rong_vay.py` (`build_body`).

**CÁNH: làm đúng như cánh của con gốc, đừng tự chế cơ chế** (rồng vây / `monster_3458`, 2026-11-11; người dùng: "cánh họ đập lên
xuống tôi thấy cả 2 lớp trên dưới", "cánh gốc cả mảng này dính vào thân, phần khớp xương khi quạt lên xuống mà không flip thì nhìn
fake quá", "làm giống 100% cánh gốc đi rồi note lại cách làm cánh vào skill"). Ba bản tự chế đều bị trả: gập màng về sống cánh (không
thấy mặt kia); lật gốc từng chuỗi quanh sống cánh (màng vò nát); cho cả cánh quay cứng quanh một xương ở vai rồi lật bằng tỉ lệ âm
(gốc cánh rời khỏi thân, cục khớp ở vai trông giả).

Cánh của họ dựng thế này (đọc bằng `chay.py info`, `att`, `sample`, và tờ nhuộm màu từng lớp cánh theo 12–14 thời điểm):
- **Ba lớp, ba slot** (sau → trước): màng (ảnh lớn, sáng), dải cạnh (một thanh trơn một màu, không viền, 301 × 22, dùng chung hai
  cánh), lớp sẫm phía mép trước (một lưỡi rộng cỡ 1/4 bề ngang cánh, không phải một thanh xương mảnh).
- **Màng bám 12 xương**: ba chuỗi 3 đốt chạy dọc cánh (mép trước, giữa, mép sau) có **ba gốc rải dọc thân** (đều là con của đốt thân,
  không chung một điểm vai), cộng **ba xương đáy màng bám thân**. Vì thế cả mép gốc cánh dính vào thân khi vỗ.
- **Không có xương nào bị lật bằng tỉ lệ âm trên ba chuỗi chính**: ba chuỗi chỉ xoay và dời (4 khoá mỗi xương); cánh "lật mặt" là do
  chuỗi giữa và chuỗi sau **bắt chéo qua chuỗi mép trước** (màng tự gấp qua). Lưới màng rất thưa (32 đỉnh) nên gấp thành mảng lớn sạch.
- **Lớp sẫm bám 6 xương con riêng** (con của ba đốt mép trước + một xương bám thân), các xương này mới khoá tỉ lệ (13–17 khoá): lớp
  sẫm co mỏng khi cánh quay ngang. **Dải cạnh bám 4 xương riêng** (cũng khoá xoay / dời / tỉ lệ): lúc nghỉ nấp sau lớp sẫm, lúc cánh
  quay ngang thì duỗi ra thay cho lớp sẫm.
- Nhịp một vòng idle 1,33 s: vung nhẹ về trước → giơ lên, quay ngang ở ~0,38 chu kỳ → lật, giơ cao tới ~0,64 → quay ngang lần nữa ở
  ~0,71 → trả mặt, đập xuống nhanh.

Cách dựng cho tướng của mình (mẫu `ArtGen/Spine/rong_vay_rig.py`):
1. Giữ **đủ mọi xương cánh của họ, đúng cha – con, đúng chỗ đặt** (đổi về toạ độ của mình). Đừng thêm xương vai gom cả cánh.
2. Mảnh của mình (màng, lớp sẫm) lưới dày tuỳ ý, nhưng mỗi đỉnh phải **biến dạng đúng như điểm tương ứng trên lưới thưa của họ**
   (`gan_goc`): tìm tam giác của họ chứa đỉnh (toạ độ trọng tâm β; nằm ngoài thì kéo dài tam giác gần nhất), rồi gắn đỉnh vào xương b
   với trọng số `W_b = Σ β_k w_b(k)` và **điểm gắn riêng từng xương** `q_b = Σ β_k w_b(k) v_k / W_b` (lưới Spine và `.atomik` cho mỗi
   xương một điểm gắn; ghi thẳng vào `sk.atts[slot][hình]["verts"]`). Chỉ nội suy trọng số (một điểm gắn chung) thì trong lòng mỗi
   tam giác của họ lưới mình gấp khác đi: màng nhăn đúng lúc các chuỗi bắt chéo.
3. Dải cạnh cánh: dùng **nguyên lưới của họ** (đỉnh, tam giác, uv, trọng số) với một thanh trơn màu sống cánh của mình.
4. Chuyển động các xương cánh: lấy mẫu clip của họ 30 khung/giây (`chay.py sample`), đổi ma trận thế giới thành **lệch so với dáng
   gốc trong hệ xương cha** (xoay, dời × tỉ lệ đơn vị, tỉ lệ nhân; góc `unwrap` theo thời gian; nếu xương cha của mình đã nắn hướng
   khác con gốc thì quay vectơ dời theo hiệu góc) rồi đặt lên đúng các xương đó (`canh_goc`, `canh`). Thân, cổ, vây của mình vẫn
   clip tự viết; chu kỳ nền đặt bằng đúng chu kỳ idle của họ. Clip khác (đòn, chiêu, trúng đòn, chết) lấy cánh từ clip tương ứng
   của họ, co giãn thời gian theo độ dài clip của mình.
5. Kiểm: tờ khung bằng runtime Spine thật ở đúng các giây đã mổ, đặt cạnh tờ nhuộm màu của con gốc.
Chuyển động lấy mẫu là của nhà phát hành game gốc (như hình và chuyển động aola): ghi rõ trong ghi chú tướng, không đăng công khai.

## 0a. Tiêu chí bắt buộc cho tướng .atomik (người dùng chốt 2026-11-09, soát trước khi báo xong)

Hình, dạng tiến hóa:
- **Chibi chỉ ở dạng 1.** Dạng sau tỉ lệ trưởng thành, dữ dần: đầu nhỏ lại, mắt xếch, nanh, móng, thế sẵn sàng đánh.
- **Dạng cuối khác hẳn dạng trước** chứ không chỉ thêm chi tiết: đổi màu chủ đạo (đậm hơn), thêm giáp/đồ/phụ kiện, đổi chi tiết đặc
  trưng (râu, đuôi, sừng) và **đổi dáng** (bóng dáng nhìn đã biết là con khác). Vẫn giữ vài nét nhận ra cùng dòng.
- Con dài dẹt thì co cho vừa sân (`max_w`); không để lòi khỏi mép màn.

Animation:
- **Không có gì đứng im:** mây, đồ bay, vòng quanh tướng phải chuyển động; phụ kiện bay quanh dùng clip lặp `aura` (liền qua mọi clip).
- Thân dài (rồng, rắn, đuôi to) **nhiều xương, uốn sóng** (`spine`); **tóc, bờm, râu nhiều xương có lò xo** (`soft`), tách lớp riêng nếu
  lắc làm nhoè phần khác (`sep`).
- **Bắn từ miệng thì phải há miệng:** tách hàm dưới thành vùng `jaw` (xương `jaw` con của đầu, khớp ở góc hàm); đòn, chiêu nhả từ
  miệng tự há theo nhịp (`beast.jaw_open`).

Đòn và chiêu:
- **Đòn đánh xa đứng một chỗ bắn**, không lao lên nhả chiêu; chỉ giật nhẹ ngược chiều khi bắn (cổ, thân vươn là đủ).
- **Không một màu**: tránh để cả loạt tướng "lao lên húc rồi lộn". Phần lớn chiêu đứng tại chỗ (tia, xoáy, mưa đạn, cột trồi, sóng
  âm, triệu hồi...); chỉ dòng có lore lao húc (dê, bò, tê giác) mới lao.
- **Mỗi dạng một chiêu khác, mạnh dần**: dạng sau to hơn, nhiều nhát hơn, dữ dội hơn (khựng, rung, chớp màn tăng theo dạng),
  thường đổi cả kiểu chiêu chứ không chỉ phóng to (`*_form`, `attack`/`skill`/`motion` theo dạng).
- Chiêu lấy ý từ lore con vật và chiêu Pokémon cùng hệ (Thủy: Hydro Pump, Whirlpool, Surf, Icicle Crash; Mộc: Leaf Storm, Solar
  Beam, Frenzy Plant, Petal Blizzard; Hỏa: Flamethrower, Fire Spin, Eruption, Heat Wave...), học nhịp Critters (skill
  `pokiclash-hero-fx` mục 1b).
- Hạt nhỏ (lá...) vẽ không viền sticker (`game.plain`).

## 0. Trước khi làm

- **Giấy phép:** code repo `spine-animation-ai` là PolyForm Noncommercial (không dùng thương mại). Runtime `spine-unity` đòi
  giấy phép Spine Editor. Vì vậy đưa vào game thì dùng **định dạng riêng `.atomik`** (mục 9), không dùng runtime Spine.
- **Bản quyền ảnh:** ảnh lấy trên mạng (nhân vật của hãng khác: Snorlax, Agnes Tachyon...) chỉ để thử. Để ngoài PokiWar, trong
  `<ProjectAtomik>/spine-animation-ai/work/<tên>/`. Không commit, không publish artifact. Ngoại lệ do người dùng yêu cầu: con mận
  trong `Assets/05 Atomik Thu/` (scene thử Unity), không commit thư mục đó.
- **Repo và Python:** repo clone cạnh PokiWar: `E:\ProjectAtomik\spine-animation-ai` (máy kia: clone cạnh project, hoặc biến
  môi trường `SPINE_AI`). venv riêng `.venv` có `opencv-python Pillow numpy`. Chạy bằng `<repo>/.venv/Scripts/python -I`.
  Không cần API key (bước Gemini của repo không dùng).
- Chỉ dùng lại 3 thứ của repo: `make_atlas.pack`, `build_spine_json._convert_timeline` (đổi khoá sang dạng 4.2), Spine Web
  Player. Bộ rig dáng người của repo không hợp con thú chibi; dùng công cụ ở `ArtGen/Spine/`.

## 1. Chọn cách

| Cách | Khi nào | Lệnh |
|---|---|---|
| **A. GPT vẽ hình trọn con + tờ mảnh** | tướng mới, muốn mảnh sạch có đầu khớp tròn | `build.py` → `gen.py` → `rig.py all` |
| **B. Một ảnh, mảnh cứng** | ảnh nét viền rõ, chuyển động nhẹ | `rig.py one1 <mã>` |
| **C. Một ảnh, một lưới có trọng số** | con gọn, ít lớp chồng (khuyên dùng) | `mesh.py <mã>` |
| **D. Một ảnh, nhiều lớp lưới** | áo choàng, tay áo, đuôi chồng lên thân, chân | `mesh.py <mã>` (spec có `pieces`) |

Người dùng nghĩ "rig" là làm từ **một ảnh liền**: đưa một ảnh thì đi thẳng B/C/D, không bắt GPT vẽ tờ mảnh.

Ảnh dễ rig: đứng thẳng hoặc nghiêng nhẹ, tay chân tách khỏi thân, không chéo nhau, nền trắng. Dáng chữ T là dễ nhất.

Chọn đa giác vùng: kẻ lưới toạ độ lên ảnh (bước 10–25 px, phóng 2–3x, số mỗi 50/100 px, chữ bằng `arial.ttf`), cắt cận từng
vùng khó rồi đọc toạ độ. Sau mỗi lần dựng, soi bản đồ vùng tô màu (mục 6).

## 2. Cách A: GPT vẽ (ArtGen/Spine)

- `build.py <mã>` sinh gói `ArtGen/Spine/gui_gpt/<mã>/`: `luot_1_tong.txt` (hình trọn con dáng dễ rig, 1024x1536) và
  `HUONG_DAN.md`. `luot_2_tach_manh.txt` (2 tờ: nhóm đầu, nhóm thân; mỗi mảnh vẽ đủ phần bị che, đầu khớp thừa ~30 px tròn,
  cách nhau ≥ 60 px) **chỉ sinh khi đã có** `inbox/<mã>/L1_duyet.png`. File prompt theo luật ArtGen của CLAUDE.md (ảnh mẫu
  đường dẫn tuyệt đối, mục SAVE dạng `save it as a PNG to <path>` để `gen_codex.py` dò được chỗ lưu).
- `gen.py <file prompt>`: gọi Codex qua `ArtGen/Heroes/tools/gen_codex.py`, giữ chung khoá `ArtGen/Heroes/inbox/.codex.lock`
  với các lô tướng. Chạy nền. Hết hạn mức thì hỏi giờ có lại bằng
  `codex.exe exec --skip-git-repo-check -s read-only -- "Reply ok."` (exe trong `%TEMP%\pokiclash_codex_path.txt`): lỗi trả
  về có "try again at <giờ>". Báo người dùng, đừng chờ mù.
- `rig.py cut <mã>`: cắt tờ mảnh theo `SPEC[<mã>]["sheets"]`. Mẩu rời sát mảnh lớn (< 45 px) tự gộp. **Đếm sai số mảnh thì
  dừng**, in khung từng mảnh.
- `rig.py place <mã>`: khớp từng mảnh vào ảnh trọn con (SQDIFF có mặt nạ trên Lab, dò tỉ lệ + góc + vị trí, 3 tầng). Mảnh lớn
  nhất mỗi tờ dò tỉ lệ cả tờ (0.35–2.8), mảnh khác dò quanh đó; mảnh trái/phải giới hạn theo nửa người. Ra `so_ghep.png` + IoU.
- `rig.py build <mã>`: khớp xương = tâm vùng giao giữa mảnh con và mảnh cha.

## 3. Cách B: một ảnh, mảnh cứng (`rig.py one1`)

Spec trong `rig.py` (mẫu `SPEC["snorlax"]`): `base`, `src`, `fg` (ngưỡng sáng, ngưỡng bão hoà của nền), `dark_thr`.
`one`: mỗi mảnh `{poly, excl, keep, minus, cap, cap_keep, inpaint}`:
- `excl`: giành pixel trước (đầu → tay → thân); mảnh không excl (bụng, tai, chân) được chồng.
- `keep: "light"/"dark"`: chỉ lấy lớp màu đó. `minus`: đa giác trừ ra.
- `cap: (mảnh cha, r)`: phần chồng lấn r px vào mảnh cha, mờ dần; `cap_keep` chỉ lấy màu lông.
- `inpaint`: vẽ bù lớp màu đó trong mảnh (chỗ bị mảnh khác che).
`draw`: thứ tự vẽ sau → trước. `root`: gốc (giữa hai chân, mặt đất). `bones`: `(xương, cha, mảnh, (x, y) khớp)`.

## 4. Cách C và D: lưới có trọng số (`mesh.py`) — uốn mềm, không hở

Chung:
- Lưới: điểm viền cách đều `step_edge` (đầu danh sách = hull, mọi khối rời) + lưới điểm trong `step_in`, Delaunay
  (`cv2.Subdiv2D`), bỏ tam giác có trọng tâm hoặc trung điểm cạnh ra ngoài hình.
- `bones`: `(xương, cha, (x, y) khớp)` hoặc thêm phần tử thứ 4 `{"inherit": "noScale"}`.
- `labels` = vùng của từng xương, ưu tiên theo thứ tự (vùng trước giành pixel trước):
  - `(xương, đa giác hoặc danh sách đa giác, lọc)`; lọc là `None`, `"dark"`/`"light"` (theo `dark_thr`) hoặc `("lt", 80)` /
    `("gt", 150)` (độ sáng trung bình).
  - Nhiều vùng cho một xương: đặt tên `"xương#ghi chú"` (vd. `root#shoes` cho giày với lọc khác quần tất).
  - Vùng cuối là `body` phủ cả ảnh để không pixel nào thiếu vùng.
- Trọng số: `w = exp(-(khoảng cách tới vùng / sigma)^2)`, giữ 4 xương nặng nhất, chuẩn hoá. `sigma` theo xương: tóc 8, tai 6,
  vải áo 16–18, thân 14, chân 4, vũ khí 5.
- `"geodesic": True`: khoảng cách đi trong hình, không nhảy qua khe trắng (lưỡi dao sát mép mũ vài px).
- `"smooth_labels": 5`: mỗi pixel theo vùng chiếm đa số trong ô 5x5, dải mảnh 1–2 px nhập về vùng bên cạnh (dải mảnh không
  phủ lưới được, để lộ nền thành đường kẻ).
- Thứ tự vẽ tam giác theo `layer` của vùng (tay vẽ sau cùng để đè lên bụng).
- Vũ khí, đồ cứng: gộp vào vùng xương bàn tay, sigma nhỏ để bám 100%, đi cứng không cong.
- Thân dẹp giãn làm méo tay, vũ khí: xương tay con của thân đặt `noScale`.
- Thêm xương khuỷu để tay cong; bụng có xương riêng để nảy.

Cách D thêm `pieces` (mỗi lớp một slot, một lưới, xếp sau → trước), mẫu `MESH["tachyon"]`:
- `{"name", "labels": [...] hoặc "rest", "into": [vùng], "px": n}`. `rest` = mọi vùng không thuộc lớp khác.
- Lớp nằm dưới **mọc thêm** n px dưới mép các vùng `into` (vùng của lớp đè lên nó). Dải đó được inpaint từ màu của chính lớp,
  nên khi lớp trên đung đưa không lộ nền. Ví dụ Tachyon: đuôi (mọc 22 px dưới vạt áo), chân (mọc 16 px dưới áo, thân),
  thân + áo + đầu (mọc 18 px dưới tay áo trái), tay áo trái trên cùng.
- `fh`, `gif_scale`: cỡ khung và GIF cho ảnh lớn. `detail: {times, boxes}`: ra `chi_tiet.png` cận cảnh tỉ lệ gốc từng vùng ở
  vài thời điểm (soi tóc, áo, đuôi).
- Tóc, đuôi lọc theo độ sáng: ngưỡng phải đủ rộng cho cả vệt sáng (Tachyon: `("lt", 165)`). Ngưỡng hẹp (120) đẩy highlight
  sang lớp thân, chúng đứng yên khi tóc/đuôi lay và lộ thành mảng, đường cắt.
- Chân (quần tất): ngưỡng chặt `("lt", 80)` và đa giác bám dáng chân, nếu không lớp chân ăn sang lót áo tím, nút áo.
- `bg_holes` (khe trắng nằm lọt giữa vùng được kê thì coi là nền) có trong code nhưng **đang không dùng**: thử với đuôi
  Tachyon thì xoá được khe nhưng mất luôn lọn ngọn mảnh (lưới không phủ được), để lại vết khuyết. Khe hẹp giữa lọn tạm để lấp.

Giới hạn: lưới chỉ kéo giãn ảnh có sẵn. Vai giơ quá ~50° cộng khuỷu ~25° là tay gập đè lên đầu; chỗ bị che không tự có hình.
Mái tóc trước mặt không cho động (mặt, mắt méo).

## 5. Animation

- Viết trong `<mã>_anims()` (rig.py) hoặc hàm trong `ANIMS` (mesh.py). `tl([(t, góc, curve)])` cho **rotate**,
  `tl2([(t, x, y, curve)])` cho **translate/scale**. Dùng nhầm `tl` cho translate là sai cả JSON (lỗi đã gặp).
- `curve` gắn với đoạn **kết thúc** ở khoá đó: `E` êm hai đầu, `EO` bật nhanh rồi chậm (đánh trúng), `EI` chậm rồi nhanh
  (lao vào), `None` thẳng. `_convert_timeline` đổi sang bezier tuyệt đối của 4.2.
- Vòng lặp nhiều phần phụ (idle tóc, áo, đuôi): hàm `wave(amp, phase)` (sin khép kín 8 khoá), trễ pha tăng dần từ gốc ra ngọn
  (tóc gốc 0.7, ngọn 1.3; đuôi 0.6 → 1.3 → 2.0), biên độ tăng dần ra ngọn (đuôi 4° → 7° → 10°).
- Xương setup không xoay. Góc dương = ngược kim (y lên). Tay trái người xem chĩa sang trái: góc âm là giơ lên; tay phải: dương.
- Chém bằng dao cầm dựng: kết thúc thấp trước bụng thì bàn tay xoay ~120°; 60–90° thì lưỡi dao quét ngang qua mặt.
- Con của `root` đã đi theo `root` (nhảy): **đừng cộng thêm** độ cao cho chân, chỉ co nhẹ.
- Bộ chuẩn: `idle` (lặp, thở; phần phụ lắc trễ pha; chớp mắt hoặc giật tai), `attack`/`slash` (lấy đà → đánh → dư lực → về),
  `hit`, `jump`/`skill` (ngồi → bật → rơi → dẹp nảy), `walk`/`run`.
- Khoá đầu = khoá cuối với vòng lặp; dẹp-giãn khi lấy đà và chạm đất; phần phụ trễ 0.1–0.2 s.

## 6. Soi trước khi báo (bắt buộc)

- `khung.png` (9 khung mỗi animation) và `anim_<tên>.gif`: bộ dựng khung Python riêng (`rig.render`, `rig.draw_pose`,
  `mesh.make_draw`, `mesh.make_draw_multi`). Soi: hở khớp, mảnh lệch, mất mảnh, cắt khung.
- `luoi.png`: lưới + màu trọng số + khớp (cách D: mỗi lớp một ô, nền xám để thấy dải vẽ bù).
- Bản đồ vùng tô màu (dựng tạm từ `mesh.label_map`): soi vùng ăn lẹm (chân lấy lót áo, đuôi lấy dây đeo ống nghiệm...).
- So khung t=0 với ảnh gốc ở tỉ lệ gốc: phải trùng khít. Đường kẻ mảnh, mảng lạ ở t=0 là lỗi vùng, không phải animation.
- Trang xem `rig/index.html`, `rig_mesh/index.html`: server tĩnh `.claude/launch.json` cấu hình `spine-work` (cổng 8771, phục vụ
  `spine-animation-ai/work`), `preview_start` rồi tới `http://localhost:8771/<tên>/rig_mesh/index.html`. Kiểm bằng JS
  `Object.entries(players).map(([k,p])=>[k,!!p.skeleton])`; ảnh lớn tải tới ~10 s. Spine player ghim `4.2.119`.
- Gửi người dùng khung, GIF, ảnh so sánh bằng SendUserFile; nói rõ cái gì chưa ổn.

## 7. Lỗi đã gặp và cách tránh

- Nền ô cờ "giả trong suốt" in vào pixel: mặt nạ nền theo vùng sáng nối mép ảnh, gọt 1 px + làm mượt (blur 1.6, ngưỡng 0.5).
- Ảnh webp: nền không còn đúng 255 (nén); đọc bằng Pillow rồi lưu `src.png`.
- Đa giác đầu ăn lẹm vai: kẻ sát mép đầu, để vai cho tay.
- Vẽ bù ra màu xám, vệt chữ V: nới vùng vẽ bù 2 px, phần ngoài tô màu trung vị trước khi inpaint.
- Phần chồng của tay quét vệt sẫm: bán kính ~9 px, chỉ lấy màu lông.
- `Subdiv2D` trả float32: làm tròn điểm theo bước 0.25 trước khi chèn.
- In tiếng Việt: `sys.stdout.reconfigure(encoding="utf-8")` (`-I` bỏ qua `PYTHONIOENCODING`); vẽ chữ Việt lên ảnh dùng
  `ImageFont.truetype("C:/Windows/Fonts/arial.ttf")`.
- Heredoc Bash nuốt `\\`: script có regex, đường dẫn Windows thì sửa bằng Edit/Write.

## 8. Tệp

- `ArtGen/Spine/build.py` (gói prompt), `gen.py` (Codex có khoá), `rig.py` (cắt, khớp, dựng, mảnh cứng, khung, trang xem,
  animation, `pose` có `noScale`), `mesh.py` (lưới một lớp `main`, nhiều lớp `main_multi`, nhãn vùng, trọng số, animation các
  con thử), `atomik.py` (xuất .atomik).
- Đầu ra: `<base>/rig/` (mảnh cứng), `<base>/rig_mesh/` (lưới: `<mã>_mesh.json/.atlas/.png`, `luoi.png`, `khung.png`,
  `chi_tiet.png`, GIF, `index.html`).
- Con đã chạy: Giọt Sương dữ liệu giả (scratchpad), `work/snorlax` (mảnh cứng + một lưới), `work/man_kiem` (một lưới, hai dao,
  idle/jump/slash), `work/tachyon` (4 lớp, 23 xương, idle tóc/áo/đuôi). Đều chỉ để thử.

## 9. Định dạng riêng .atomik (Unity của PokiClash, không cần runtime Spine)

**File:** `"ATMK"` + uint16 phiên bản (1) + gzip( uint32 dài JSON + JSON utf-8 + uint32 dài PNG + PNG atlas ). Con mận 213 KB.
JSON đúng khuôn `JsonUtility` (chỉ mảng, không từ điển):
- `rigName, version, ppu` (100 pixel = 1 đơn vị Unity);
- `bones[]: {name, parent, x, y, rot, sx, sy, noScale}`;
- `slots[]` (thứ tự vẽ sau → trước): `{name, bone, att}` (att = chỉ số hình mặc định, -1 trống);
- `atts[]: {slot, name, uvs[] (UV Unity của atlas, gốc dưới trái), tris[], wInfo[]}`; wInfo mỗi đỉnh `n, n x (xương, x, y, w)`
  theo xương ở tư thế gốc. Mảnh cứng, lưới không trọng số đều đổi về dạng này (một xương, trọng số 1);
- `anims[]: {name, dur, tls[], sk[]}`; `tls: {bone, type, keys[]}`: type 0 xoay sải 7 `[t, v, kiểu, c1..c4]`, 1 dời và 2 tỉ lệ
  sải 12 `[t, x, y, kiểu, 8 số]`; kiểu 0 thẳng, 1 bậc, 2 bezier (điểm điều khiển tuyệt đối như Spine 4.2, curve trên khoá i áp
  cho đoạn i → i+1); `sk: {slot, times[], atts[]}` đổi hình (chớp mắt).

**Xuất:** `py -3 -I ArtGen/Spine/atomik.py <tên>.json <tên>.atlas <ra>.atomik --name <tên>`. Đọc JSON Spine 4.2 bất kỳ do bộ rig
sinh (region, mesh có/không trọng số, rotate/translate/scale, attachment), atlas kiểu cũ (xy/size) hoặc `bounds`.

**Unity** (namespace `PokiClash.Game`, `PokiClash.EditorTools`):
- `Assets/01 Script/Game/Atomik/AtomikAsset.cs`: ScriptableObject + các lớp dữ liệu (khuôn JSON ở trên), `FindClip`.
- `AtomikPlayer.cs` (`[ExecuteAlways]`, cần MeshFilter + MeshRenderer): tính xương mỗi khung (xoay cộng, dời cộng, tỉ lệ nhân
  như Spine; `noScale`), da trên CPU, một Mesh một lần vẽ, tam giác theo thứ tự slot. API: `Play(clip, loop)` (trộn tư thế
  `mixTime` 0.12 s), `Sample(clip, t)`, `Done`, `Time01`, `speed`. Chỉ tạo Mesh lúc chạy (luật `PrefabOnlyTests`: không
  `new GameObject`, `AddComponent`, `new Material`, `new Texture2D` trong mã runtime).
- `AtomikDemo.cs`: scene thử, OnGUI nút đổi clip từng con (clip không lặp xong thì về idle), thanh tốc độ; tự xếp theo khung
  (màn dọc xếp cột, màn ngang xếp hàng, camera ôm vừa).
- `Assets/01 Script/Editor/AtomikImporter.cs`: `[ScriptedImporter(3, "atomik")]` tạo asset chính kèm atlas (nén theo nền tảng,
  xem bản 2 dưới), material `Sprites/Default` (nhân alpha trong shader, hợp atlas alpha thường) và **icon 128x128 vẽ con ở tư thế gốc**
  (thumbnail của `AddObjectToAsset`, hiện trong cửa sổ Project). Đổi cách nhập thì tăng số phiên bản importer để nhập lại.
- Menu `PokiClash/Thử/Atomik: dựng scene con mận (idle, nhảy, chém)`: dựng `Assets/05 Atomik Thu/AtomikMan.unity` bằng scene
  additive (lưu rồi đóng, không đổi scene đang mở), chụp 9 khung mỗi clip vào `Temp/AtomikShots/<tên>_khung.png` để so với
  khung Python (render bằng `RenderPipeline.SubmitRenderRequest`, đặt con ở xa mọi thứ của scene đang mở).

**Quy trình đưa code vào editor dùng chung** (đã chạy 2026-11-07):
1. Viết trong scratchpad, typecheck bằng dotnet: chép `PokiClash.Core/Game/Editor.csproj`, đường dẫn tuyệt đối, file scratch
   **thay** file cùng tên đã có trong csproj (không thì trùng định nghĩa), `dotnet build ... -v q`. **Xong thì chạy
   `dotnet build-server shutdown`**: nút MSBuild tái dùng (`/nodeReuse:true`) giữ file, lần biên dịch kế của Unity hỏng
   "Access is denied" (`Script Compilation Error ... Csc ... Access is denied`), Unity giữ DLL cũ nên code mới như không có
   (lỗi đã gặp 2026-11-11: kiểm số tướng vẫn đòi 78 dù nguồn đã ghi 88).
2. Đọc `mcpforunity://editor/state` qua MCP HTTP (`127.0.0.1:8090/mcp`). Đang Play thì hỏi người dùng rồi `manage_editor stop`:
   thêm `.cs` mới lúc Play làm hỏng biên dịch cho mọi session.
3. Chép file vào Assets một lệnh, `refresh_unity mode=force`, chờ hết compile, `read_console` lỗi, kiểm `.rsp` có file mới.
4. Chạy menu qua `execute_menu_item`. Mở scene: `manage_scene load` với `name` + `path` (thư mục), sau khi chắc scene đang mở
   không bẩn (`get_active` → `isDirty`). Đưa cửa sổ Unity lên trước bằng `WScript.Shell.AppActivate(pid)` để editor chạy khung.
5. Báo các session PokiWar khác (ListAgents + SendMessage) khi đã dừng Play, refresh, thêm script.
6. Xem xong muốn chạy game thì mở lại `Assets/00 Scenes/Boot.unity` rồi Play.

**Bản 2 (2026-11-08):** `anims[].sa: {slot, keys[]}` độ đậm slot (timeline `alpha` của Spine 4.2, sải 7 như xoay) cho hiệu ứng hiện,
tan; `game` (tuỳ chọn) thông tin trận khi rig là dạng tướng: `fps, height, hitClips, hitTimes, lunge, stay, muzzle, beam,
beamStyle, move, shadow` (`atomik.py ... --game <tệp.json>`, hoặc `convert(..., game=dict)`). Phần tính tư thế và dựng lưới tách
ra `Game/Atomik/AtomikPose.cs`, dùng chung cho `AtomikPlayer` và `AolaActor`. Importer bản 3 nén atlas theo nền tảng (ASTC 8x8
Android/iOS như atlas tướng aola, DXT5 máy tính khi cạnh chia hết cho 4; `pack` của `spine_compat.py` làm tròn cạnh lên bội 8).

**Bản 3 (2026-11-10, làm cho quái Hải Long, mục 20):**
- `masks[]`: mặt nạ cắt từ attachment `clipping` của Spine: `{slot, end, bone, verts[]}`. Mọi hình trong các slot `slot..end` chỉ còn
  phần nằm trong đa giác (lồi, bám một xương, luôn bật). `AtomikPose.Skin` cắt tam giác trên CPU (`ClipTris`): tam giác nằm hẳn
  trong giữ nguyên, hẳn ngoài một cạnh thì bỏ, bị xén thì cắt Sutherland–Hodgman và thêm đỉnh vào cuối mảng. Rig có mặt nạ thì
  `maxVerts` chừa thêm chỗ, `Tris` có sức chứa cố định (phần thừa là tam giác rỗng) và `trisChanged` luôn true: nơi gọi không
  phải đổi gì (AtomikPlayer, AolaActor nạp như cũ).
- `slots[].fade`: độ mờ mặc định của slot (1 − alpha màu slot trong Spine). Slot hiệu ứng ẩn sẵn (vương miện nước, mí mắt, lưỡi)
  phải có cái này, không thì clip nào không khoá nó là nó hiện. Dùng "độ mờ" thay vì "độ đậm" để rig cũ (không có trường này,
  giá trị 0) vẫn hiện đủ mà không phải nhập lại.
- `anims[].ev[]`: sự kiện `{t, name, s}`. `AtomikPlayer.Fired(tên, chuỗi)` bắn khi đầu phát đi qua mốc (clip lặp tính theo từng
  vòng, mốc ở giây 0 bắn ngay lúc `Play`); `AtomikPlayer.BoneWorld("mieng_k")` trả vị trí thế giới của xương cho VFX bám.
- Không tăng số phiên bản importer: file cũ nhập như cũ, không phải nhập lại 24 dạng tướng.
- Kiểm: menu `PokiClash/Thử/Atomik: dựng scene Hải Long (7 clip) và chụp khung` (scene `Assets/05 Atomik Thu/AtomikHaiLong.unity`,
  ảnh `Temp/AtomikShots/hai_long/<clip>.png`, cùng giờ và khung nhìn với `mo_xe/chay.py sheet n=10`); so hình bóng từng khung với
  ảnh Spine ra 0,93–1,00 (lệch còn lại do khử răng cưa và nén ảnh).

**Còn thiếu:** vệt chém dạng lưới; bẻ đỉnh lưới (deform), màu tint, thứ tự vẽ đổi theo clip; nhiều trang atlas; mặt nạ lõm hoặc
bật tắt theo clip; `AolaActor` (tướng trong trận) chưa nghe sự kiện.

## 10. Dạng tướng .atomik trong game (Rồng Giọt thay Giọt Nước, 2026-11-08, máy ổ D)

Người dùng chọn: tướng mới "rồng con giọt nước" thay dạng 1 dòng Giọt Sương (`thuy_7`), gen bằng Codex, có clip tiến hóa nối vào
nút Tiến hóa. Mẫu để làm dạng khác:
- **Gói prompt** `ArtGen/Spine/build_rong_giot.py` (concept trọn con dáng dễ rig không cần ảnh thiết kế: đính ảnh mốc style,
  bản đồ, tờ mẫu thiết kế aola, dạng lớn của dòng; lượt 2 hai tờ mảnh: đầu, đầu nhắm mắt, đầu hét, mào, 2 tai / 2 cánh, thân,
  đuôi, kiếm, tay, nắm tay, đùi, bàn chân). Gọi `py -3 -I ArtGen/Spine/gen.py <file prompt> [--note ...]`. Mục SAVE phải viết
  đúng `save it as a PNG to <đường dẫn>` (cả từng bước), không thì `gen_codex.py` báo "không có mục SAVE".
- **Rig** `ArtGen/Spine/rong_giot.py cut | place [mảnh ...] | build` (venv có opencv, máy ổ D: `D:/spine-venv/Scripts/python -I`):
  - mảnh xanh trơn giống nhau nên `rig.place` dò tự do lạc 8/17 mảnh: dò quanh tâm đọc trên ảnh kẻ lưới (`HINT`), giới hạn góc
    (`ROT`), đặt tay mảnh khó (`FIXED`); `place <mảnh>` chỉ dò lại mảnh đó;
  - nắm tay cầm kiếm GPT vẽ rỗng ở giữa, bộ cắt lấp thành trắng: `fix_parts` tô lòng nắm màu cán kiếm;
  - tay xa và tay cầm kiếm nằm sau thân (vai không lộ cục tròn), nắm tay và kiếm trước thân.
- **Dựng** `ArtGen/Spine/rong_giot_build.py`: xương `root → move (cú lao, cú nhảy) → core (tâm thân: lộn, xoay, thu nhỏ) → hip →
  body → chest (chỉ mảnh thân: thở, dẹp giãn)`, đầu/tay/cánh/đuôi con của body, chân con của hip, `shadow` con của move (theo cú
  lao, dời ngược độ cao khi nhảy). **Không dùng noScale** khi có clip thu nhỏ cả con: noScale giữ nguyên cỡ đầu, tay. Hiệu ứng là
  slot riêng dùng lại 8 ảnh FX dòng Giọt Sương (`ArtGen/Heroes/inbox/giot_suong_fx/tai_ve`), lưu nhỏ trong atlas rồi phóng bằng
  cỡ attachment; xương hiệu ứng là con của move (không theo core). Cỡ rig: dáng đứng 340 điểm (sticker vẽ tối đa ~301).
  Ra `inbox/rong_giot/rig/` (`khung.png`, `anim_*.gif`, `xuong.png`, `<mã>_game.json`), `.atomik` và chân dung (khung 4:5, chân
  cách đáy 6%, lưu vuông 512, không bóng) vào `Assets/03 Art/Heroes/Resources/rong_giot/`.
- **Clip** tên chữ trong file, `AolaActor` đổi: idle (1_1), hit (1_2), attack (1_4), cast (1_5), skill (1_6), evolve. Khung 0 mọi
  clip là dáng nghỉ. Khung trúng khai trong `game.hitTimes`; cú lao đo trên xương `move` (attack luôn lao, clip khác khai `lunge`);
  đỉnh lao phải là lúc chém (độ dời x lúc chém lớn hơn độ cao lúc nhảy, vì trận xoay cả quỹ đạo cho đỉnh trỏ vào đối thủ); chỗ
  bắn tia = mũi kiếm ở khung trúng của cast (`muzzle`).
- **Unity**:
  - `AolaAnim.atomik` trỏ rig; `AolaActor.Load` thấy atomik thì vẽ một Mesh bằng `AtomikPose`, trả `FrameCount`, `HitFrame`,
    `Disp`, `Lunges`, `Beam` theo `game`, nên trận, sticker, hộp chi tiết, đội hình chạy như dạng aola;
  - `heroes.json` đổi `aola` của dạng sang tên thư mục (`rong_giot`), menu `PokiClash/Nhập dữ liệu`, rồi
    `PokiClash/Tướng/Gắn dạng .atomik vào prefab tướng` (Editor/AtomikForms: dựng `<dạng>.asset`, cập nhật prefab tướng). **Không
    chạy menu nhập aola thường** để gắn (nó nhập lại dạng aola từ AolaRipper máy này); menu đó bỏ qua dạng có atomik;
  - `HeroViewer`: dạng cũ có clip `evolve` thì đổi dạng phát clip đó trên sticker cũ, giữ khung cuối tới khi sticker dạng mới xong,
    clip gọi trong lúc đó chạy sau;
  - soi: `PokiClash/Tướng/Chụp thử dạng .atomik (mọi clip)` (Library/PokiHeroShots/<id>_atomik_<dạng>.png, Editor.log in khung
    trúng, đỉnh lao, chỗ bắn tia), tour `PokiClash/Thử/Giọt Sương ra trận...` và `PokiClash/Thử/Giọt Sương tiến hóa...` (đang Play
    từ Boot, ảnh Temp/PokiShots/gs_combat, gs_tien_hoa).
- Máy không có repo `spine-animation-ai`: `rig.py` tự dùng `spine_compat.py` (`_convert_timeline`, `pack` viết lại, cùng cách dùng).
- Rồng Giọt (mảnh cứng, xoay cả người, khoá thưa) bị người dùng chê: thay bằng Thủy Long, mục 11.

## 11. Thủy Long: rig lưới trọng số, animation mềm, tiến hóa nối liền (2026-11-08, cách làm chuẩn cho tướng .atomik)

Người dùng dặn: animation mềm, hạn chế xoay cả người, để ý tiểu tiết, rig xương kỹ, tiến hóa phải hiện ra dạng sau (không giật);
đổi sang Spine là để mượt, không làm kiểu cũ. Tướng: long chiến binh 3 dạng, chiến, không cute.
- **Gói prompt** `ArtGen/Spine/build_thuy_long.py`: concept dạng k đính concept đã duyệt các dạng trước; 3 tờ mảnh (A: đầu liền cổ,
  đầu nhắm mắt, đầu gầm, mào; B: **tay, chân vẽ liền cả chi** từ vai tới cổ tay, hông tới cổ chân + nắm tay, bàn chân; C: thân, đuôi,
  áo choàng, vũ khí, giáp vai, vải trước).
- **Khớp mảnh vào concept** (`thuy_long.py place k`): so khớp màu tự do lệch về mảnh nhỏ (chuẩn hoá theo diện tích, mảnh nhỏ lọt
  vào vùng xanh trơn), nên: mảnh gọn có nét riêng dò ±12% quanh **tỉ lệ ước theo khung bao** (`HINT` x, y, ô, tỉ lệ); mảnh dài xanh trơn
  (tay, chân, vũ khí) đặt theo **hai đầu khớp đọc trên concept** (`TWO`: hai đầu đường dài nhất trong mảnh, bỏ phần đầu tròn);
  mảnh vẽ khác concept (mào, vải, áo choàng) đặt tay (`FIXED`). Soi `rig/so_ghep.png`.
- Sau khi cắt: `fix_grip` (tô lòng nắm tay), `fix_stubs` (GPT tô đầu tròn khớp xanh nhạt, ghép lộ chấm nhạt ở mắt cá: tô khối
  tròn nhạt gọn về màu da).
- **Rig** (`longrig.py`, `thuy_long.build_rig`): lưng 3 đốt, cổ + đầu 2 đốt (mặt nhắm mắt, mặt gầm lấy trọng số theo bản đồ của
  đầu chính), mào 3, tay 2 đoạn + nắm tay cứng, chân 2 đoạn + bàn chân cứng (IK), đuôi 4, vải 3, áo choàng 4, giáp vai cứng trên
  cánh tay trên, vũ khí cứng trên bàn tay. Mảnh chuỗi: geodesic từ đầu khớp chia đều n đoạn, trọng số hoà quanh khớp, đoạn đầu
  hoà nửa vào xương cha (vai, hông mềm). Soi `rig/luoi.png` (lưới, màu trọng số, xương).
- **Animation** viết bằng hàm thời gian (`curve` khoá có đường cong), nướng 30 khung/giây: chân giải IK (bàn chân bám đất, bước
  lao có nhấc cong); chuỗi mềm chạy lò xo đuổi theo dáng động học (độ cứng giảm ra ngọn; vải cứng hơn đuôi kẻo bay ngang như cờ);
  khoá dày lược RDP. Mọi dao động idle bằng 0 ở t = 0. Không xoay cả người: cong lưng chia 3 đốt (`bend`), dời hông, bước chân.
  **Vũ khí theo góc thế giới** (`aim`: tự tính góc cổ tay): giơ vũ khí lệch sang phải đầu, không dựng trước mặt (đại đao tay cầm
  giữa ngực phải giơ cánh tay ít hơn, đao nghiêng phải). Hiệu ứng: `fx_on` (hiện, đậm dần, tan dần), cột nước = ảnh tia nước xoay
  90°, lấp lánh và bong bóng gắn mũi vũ khí.
- **Tiến hóa nối liền**: rig dạng k gộp rig dạng k+1 (`merge_next`, xương `n_` dưới xương `evo` co theo tỉ lệ chiều cao hai dạng,
  slot vẽ sau). Clip `evolve`: dạng k nện vũ khí, nước dâng lốc, đổi dạng ngắn (0,3 s) lúc lốc phía trước đậm nhất, dạng sau lớn dần,
  nước vỡ, gầm, rồi `post` hoà về đúng khung đầu clip idle dạng sau. Các clip trận trên rig gộp ẩn slot `n_`. HeroViewer giữ khung
  cuối tới khi sticker dạng mới xong: hai hình trùng khít nên không giật.
- **Game**: `AolaActor.ShowTime` vẽ .atomik theo thời gian liên tục (60 khung/giây màn hình), hình aola vẫn theo bậc 25 khung.
- Lệnh: `D:/spine-venv/Scripts/python -I ArtGen/Spine/thuy_long.py cut k | place k [mảnh] | rig k | all | show k clip t1,t2 [follow]`
  (`show` dựng khung lớn từ `rig/baked.pkl`, khỏi nướng lại). `all` dựng dạng 3 trước (dạng k cần dạng k+1 cho tiến hóa).

## 12. Tướng .atomik từ MỘT ảnh liền (cách chuẩn từ 2026-11-08 sáng: Thủy Long sửa lỗi, Tám Tay)

Người dùng chê bản ghép tờ mảnh (mục 11): lỗi nhiều (khe trắng giữa đầu, mào, cổ; nắm tay vẽ lệch; viền sticker thắt vòng), dặn
"không cần tách nhiều bộ phận, gen liền cũng được". Từ đây **chỉ gen concept trọn con một ảnh**, rig thẳng từ ảnh đó.
- **Ảnh**: dáng rig được (mục 1): tay chân tách thân, chân không chéo, **vũ khí không vắt qua người** (vũ khí dài dựng bên phải
  người), không đường đất. Gói prompt mẫu: `build_tam_tay.py` (tướng mới, đính Thủy Long dạng 1 làm mốc nét), `build_thuy_long.py
  luot_1_lien` (vẽ lại concept đã duyệt, chỉ đổi tư thế).
- **Bộ dựng chung** `ArtGen/Spine/thuy_long_lien.py` (tướng khác cấu hình lại như `tam_tay.py`: `CFG`, `LAYERS`, `JD`, `MARKD`,
  `OVERRIDE`, `CLAMP`, `CHAINS`, `PARENT`, `LINEAR_Y`, `FULL_SHEET`, `WARM_FIX`):
  - nền: trắng nối mép ảnh; xoá nét đất mảnh (trên dưới đều trắng); khe trắng kín > 3000 px là nền;
  - **vùng từng phần**: loang đều 1 px mỗi bước từ hạt giống trong vùng màu, **nét mực (độ sáng TB < 72) là tường**; watershed
    loang dọc theo nét mực nên kéo viền chân theo vải (đã bỏ). Hạt giống: mảnh khớp cũ co 8 px (nếu có) hoặc đường xương / đa
    giác kẻ tay đọc trên ảnh kẻ lưới (`JD` khớp, `MARKD` hạt giống). Pixel chưa có nhãn lấy **nhãn gần nhất**
    (`fill_nearest`, đừng giãn ảnh lấy nhãn số lớn: xúc tu này nuốt xúc tu kia). Lọc đa số 7x7, bỏ mẩu < 500 px; `OVERRIDE` ép
    vùng, `CLAMP` giới hạn phần trong đa giác (vải ăn sang dải chân thì khi vải bay kéo theo dải chân);
  - **ít lớp** (sau → trước), ví dụ: đuôi, tay sau, chân sau, chân trước, mào/bờm (lớp riêng: chung lưới với đầu thì mào lắc xé gáy),
    thân + đầu (Tám Tay: đầu lớp riêng vì râu xúc tu buông trước ngực), vải, tay trước + vũ khí + giáp vai. Áo choàng lộ rời rạc:
    dựng **cả tấm** (bao lồi ∩ hình), phần khuất lát vân sáp thật của áo choàng;
  - lớp dưới **mọc thêm** n px dưới các lớp trên, vẽ bù từ màu chính lớp (TELEA), mép mượt, kẻ nét mực dọc mép (lúc nghỉ khuất);
  - trọng số: phần chuỗi theo khoảng cách đi trong hình từ khớp đầu, khớp giữa lấy đúng khớp kẻ (`chain_w`), hoà quanh khớp và vào
    xương cha; phần cứng (nắm tay, bàn chân, vũ khí, giáp vai) 100% một xương hoặc chia (giáp vai to: 65% ngực);
  - súng, pháo: góc vũ khí theo **trục nòng** (`JD[k]["axis"]`), không theo tay cầm → miệng nòng, kẻo tia nước bay chếch.
- **Lò xo**: mào/bờm dài và áo choàng cứng hơn và giới hạn góc văng (`maxang` trong `longrig.Springs`), kẻo bờm văng ngang thành dải.
- **Soi** (bắt buộc): `rig_lien/nhan.png` (bản đồ vùng trên ảnh), `lop.png` (từng lớp, dải vẽ bù), khung lớn `show` ở các pha
  nhanh nhất (lao, bắn, trúng đòn): tìm sợi viền bị lớp khác kéo theo, mẩu vũ khí dính chân, mảng vẽ bù lộ ra.
- Clip dùng chung tên xương nên tướng thiếu mào, vải, áo choàng vẫn chạy: `clean()` bỏ khoá của xương, slot, hình không có.
- Lệnh: `D:/spine-venv/Scripts/python -I ArtGen/Spine/thuy_long_lien.py nhan k | rig k | all | show k clip t1,t2 [follow]`;
  Tám Tay `ArtGen/Spine/tam_tay.py` cùng lệnh (`all` dựng dạng 2 trước).
- Unity: `heroes.json` đổi `aola` của dạng, menu `PokiClash/Nhập dữ liệu`, `PokiClash/Tướng/Gắn dạng .atomik vào prefab tướng`.
  Nạp lại `.atomik` khi Editor đang Play: `AtomikPose.Stale` báo, `AolaActor` dựng lại (trước đó văng IndexOutOfRange mỗi khung).

## 13. Thú huyền thoại rig đơn giản kiểu Clash of Critters (đảo Thủy, 2026-11-08 chiều)

Người dùng dặn:
- thú huyền thoại hơi chibi kiểu Pokémon, style cũ (bút mực, sáp màu, tô phẳng);
- dạng sau dữ hơn nhưng không quá; hạn chế dạng người;
- animation đơn giản, ít khớp, hiệu ứng bù vào; càng gần boss cuối càng đẹp.

Các bước:
- **Concept:** `ArtGen/Spine/build_beasts.py [id]`. Ảnh 1536x1024, ảnh mẫu nét là 2 concept chibi đã duyệt cùng bản đồ thế giới. Dạng k > 1 đính ảnh các dạng trước. Gen bằng `gen.py`; dạng chưa có ảnh dạng trước thì chưa dựng.
- **Rig:** `beast.py <id> grid|nhan|rig|all|show <k>`, cấu hình từng dạng ở `beasts_cfg.py`.
  - Xương: root, move (lao, nhảy), shadow, ground (bàn chân bám đất), base (ở đất: nghiêng, nén giãn), body (một khối), head (cứng), phụ kiện cứng (`ear*`, `wing*`, `claw*`, `arm*`, `bell*`, `tuft*`), đuôi một chuỗi 1-3 đốt.
  - Chân (phần tên `leg*`): nửa trên theo body, bàn chân theo ground, chân tự giãn, co; không IK.
  - Đầu liền thân (chim, cá mập) dùng kind `("soft", "body", "head", p0, p1)`.
  - Đạo cụ cứng theo xương tay: `("rigid", "arm_f")`.
- **Clip:** khoá tay, không lò xo. Chuyển động phụ (đuôi, tai, chuông) trễ, ngược chiều độ nghiêng thân.
  - idle 2 s: nhún nén 3%, đuôi trễ từng đốt, tai ngược pha, một cú giật tai.
  - Đòn đánh kiểu lao (pounce, ram, bite, claw, smack, slam): lao 0,55H, trận kéo tới 72% quãng.
  - Đòn đánh kiểu xa (song, breath, roar): dời dưới 0,2H, trận tự nhún tới.
  - Mọi đòn: lấy đà 0,3 s, ra đòn 0,12 s, khựng 0,1 s.
  - cast: tụ cầu ở miệng (điểm `mouth` là chỗ bắn tia).
  - skill leap, dash hoặc summon: cả ba đều lướt tới để hiệu ứng lớn rơi đúng chỗ đối thủ. Phải có `lunge: ["skill"]`.
  - evolve: lốc nước, đổi dạng, khung cuối khớp idle dạng sau.
- **Hiệu ứng:** `build_fx_beasts.py`, tờ 1536x1024 chia lưới 3x2 ô 512 px, mỗi ô một hình. `--cat` cắt theo ô ra `inbox/fx/<id>_<tên>.png`.
  - Gắn qua `"fx"` của tướng: `fx_hit`, `fx_hit2` (đòn), `fx_orb`, `fx_charge` (cast), `fx_big` (`"up"` là đáy ở đất), `fx_big2`, `fx_wave`, `fx_ground`, `fx_p` (hạt văng `burst()` có biến thiên).
  - `skill_fx.drop` cho vật rơi từ trên (chuông, tảng băng).
  - Boss cuối thêm tờ thứ hai (`<id>_b`).
- **pixelfx** (`D:/_ref/pixelfx`) là pixel art có lớp sáng cộng dồn. Chỉ học cách diễn: đà ngược chiều, khựng lúc chạm, hạt nhanh vào chậm ra rồi tan. Không lấy glow, luật game vẫn tô phẳng.
- **Bẫy đã gặp:**
  - mảng trắng khép kín lớn (tròng mắt, lông kem, ngọc trai) bị `Q.load` coi là khe nền. `beast.load` trả lỗ về hình nếu có vân hoặc ngả màu (giấy trắng thật là ~254, không vân). `keep`, `drop` ép tay.
  - lưới `mesh_mask` chỉ lấy viền ngoài nên bỏ trống vùng có lỗ (dây đàn mất). Lưới phải dựng trên hình đã lấp lỗ, độ trong của ảnh vẫn giữ khe.
  - tai, đuôi xoay cùng chiều thân làm văng quá đà. Chuyển động phụ phải ngược chiều, trễ.
  - hạt giống chân đặt sát bụng làm chân ăn mất bụng: đặt thấp, gần bàn chân.

## 15. Một lưới liền, chiêu đa dạng (2026-11-09, cách chuẩn từ nay, thay mục 14)

Người dùng chê bản ghép lớp (mục 13, 14) lỗi nhiều: vệt khe, cắt cụt, đuôi nứt. Dặn gen một con nguyên chân tay đuôi, chỉ tách vũ khí, cánh khi thật cần; chiêu không được toàn "nhảy lên rồi ra chiêu".

- **Rig:** `beast.py` có `ONE = True`.
  - Cả con là MỘT lưới (lớp `main`). Trọng số mỗi đỉnh là tổng có trọng của các vùng theo độ thuộc vùng (`membership`: lan 3x3 chỉ trong hình, dải hoà `BLEND` px). Cấu hình vùng, khớp vẫn ở `beasts_cfg.py` như mục 13.
  - Khe giấy trắng giữa hai bộ phận (`drop_gaps`) thành trong suốt, lưới vẫn phủ qua (cắt lưới theo khe làm gốc đuôi rách răng cưa).
  - Đầu xoay nhân `HEADK` 0,55; đuôi idle nhân 0,6; gốc chuỗi hoà vào cha tới 30% chiều dài.
  - Lưới chỉ lấp lỗ nhỏ (`fill_small_holes`, dưới 0,006·H² px rig); khoảng trống lớn (giữa đuôi và thân) để trống, kẻo đuôi lắc kéo tam giác thành vệt sọc. Đàn có dây mảnh giữa các lỗ khai `"mesh_fill": "all"` (Mi Nhi).
  - `cut_gaps`: bỏ tam giác vắt qua chỗ trong suốt mà các đỉnh thuộc hai bộ phận khác hẳn nhau (độ giống trọng số < 0,5), như chóp đuôi sát móng vuốt.
  - Phần trong `"sep"` của dạng thành lớp riêng sau/trước (mọc thêm, loang màu như cũ). Chỉ dùng khi vũ khí, cánh che thân mà phải cử động mạnh.
- **Xương:**
  - `spin` giữa thân (cha của `ground` và `base`): lăn, lật quất đuôi, trượt bụng.
  - `paw`: chân trước (tự chọn `leg_fn`/`leg_f`, khai `"paw"` được) xoay cả chân quanh vai, vẽ trên cùng (đá, vồ quét qua trước vải, thân; lúc đứng không chồng nên không đổi hình).
  - `flyp_<đồ>` (khai `"throw"`): đồ bay ném được, con của `move`.
  - `far` (con của root, dáng gốc trước mặt 0,9H, cao 0,45H), `fp*` hạt, `fly0..4` đạn từ miệng, `flyw` sóng đất.
- **Game:** `game.far` liệt kê clip có hiệu ứng ở xa. `AolaActor.FarAtomik` dời `far` tới tâm thân đối thủ và `fly*` theo quãng đã bay (x so với chỗ xuất phát). Clip đánh xa phải dời `move` dưới 0,15H để trận không coi là lao.
- **Kiểu đòn** (`attack`, theo dạng được): `bite`, `ram`, `claw`, `smash`, `swipe`, `punch`, `kick`, `tailwhip`, `spin`, `song`, `breath`, `roar`, `throw`.
- **Kiểu chiêu cuối** (`skill`): `erupt`, `storm`, `barrage`, `summon_prop`, `shockwave` (đứng tại chỗ, `far`); `charge`, `spin_dash`, `slide`, `combo` (lao, `lunge`). `motion` chọn dáng tụ lực: `stomp`, `roar`, `howl`, `claws`, `wings`, `rear`.
- `game_info` tự tính `lunge`, `far` theo kiểu. Vòng tụ lực kiểu mới chỉ vòng sau, nhạt, không khiên (khiên, vòng trước che kín dáng).
- **Soi:** nền xám (`render(..., bg=(150,150,150))`) để thấy vệt trắng, chỗ hở. Soi khung lúc xoay, lật, trượt và lúc đuôi lắc mạnh nhất.

## 16. Đảo Hỏa: tướng mới từ chữ tới game trong một buổi (2026-11-09, máy ổ E)

Cách mục 15 áp cho 10 dòng, 28 dạng chưa có concept nào (QUY_TRINH mục 19):
- **Gói prompt** `build_hoa.py`: thiết kế chữ (giữ chủ đề dòng aola, mỗi dòng một bảng màu), ảnh mẫu là ảnh liền đã vào game theo kiểu
  dáng (`POSE_REF`; tránh ảnh mẫu cùng loài kẻo Codex chép), luật lửa `FLAMES` (viền khép kín, tối đa 3 dải, không phát sáng,
  không tàn bay). Dạng k chỉ dựng khi đã có ảnh dạng k-1.
- **Cấu hình** riêng một file `beasts_cfg_hoa.py` (nạp cuối `beasts_cfg.py`); hàm `_fx` đặt bộ hiệu ứng lửa thay bộ nước mặc định
  (vòng dưới chân, lốc tụ lực/tiến hóa chỉ vòng sau, sóng cuối chiêu, hạt). Mỗi dạng: soi `nhan.png`, sửa hạt giống chỗ lẹm (sừng mũ
  bị tính vào mào, gốc tai bị tính vào đầu) rồi mới dựng.
- **Hiệu ứng** tờ 3x2 như mục 13; ảnh hình vòng khai trong `HOLLOW` của `build_fx_beasts.py` để xoá lòng giấy trắng khép kín.
- **Dựng thử không đụng Assets:** vá `thuy_long.RES` sang scratchpad (và `fx_img` thay ảnh thiếu bằng FX03) để soi `khung.png`,
  tiến hóa (`show <k> evolve ...`) trước khi có đủ hiệu ứng, rồi chép `Resources/<dạng>/` vào Assets một lần khi Unity rảnh.
- **Gen dài**: `chay_hoa.py <prompt ...>` chạy tách (Start-Process), bỏ qua file đã có ảnh. Lệnh nền của phiên bị ngắt vẫn sống:
  kiểm tiến trình `gen.py` trước khi chạy lại kẻo gen trùng.
- `AtomikForms.Attach` tự dựng prefab cho tướng chỉ có dạng .atomik (chưa từng có hình aola) và thêm vào HeroModels.

## 17. Rồng rắn uốn lượn, mây bay vòng, dạng sau "chiến" (Thanh Long, 2026-11-09 tối)

Người dùng dặn: mây quanh rồng phải bay xung quanh; thêm xương cho thân rồng mềm mại, uốn lượn; dạng 2, 3 chưa đủ chiến, chibi chỉ
ở dạng 1. Học từ aola 1749 (mây nước nhiều cụm chảy vòng trước, sau thân liên tục) và Critters (skill `pokiclash-hero-fx` mục 1b).
- **Concept dạng sau:** `build_thanh_long_chien.py` (ảnh mẫu: dạng 1 lấy nét, một tướng Hỏa dữ lấy thần thái, dạng hiện tại lấy màu,
  bản đồ). Tỉ lệ trưởng thành: đầu chỉ ~1/4 chiều cao, mắt xếch đồng tử dọc, nanh, móng giương; thân rắn chữ S nằm ngang, chân
  tách thân, **không vẽ mây**. Dạng khai `"src": "tai_ve/L1_chien.png"` (`beast.src`) để không đè `L1_duyet.png` cũ.
- **Mây bay vòng = clip lặp `aura`** (không khoá trong clip trận: đổi clip là mây giật về chỗ cũ):
  - ảnh mây cắt từ concept cũ bằng `cat_may.py` → `inbox/fx/thanh_long_may<k>_<i>.png`; mây vẽ sẵn trong ảnh dạng 1 bỏ khỏi lưới
    bằng `"erase": [(x, y)...]` (bỏ cả mảng liền chứa điểm);
  - `"orbit"` (theo dạng): `clouds` [(ảnh, cỡ theo H, đuôi mây "r"/"l")], `period` 8 s, `ph` (lệch pha đầu, tránh mây nằm đúng điểm
    quay đầu lúc giây 0), `rx` (theo bề dài con), `ry`, `cy`, `depth`;
  - mỗi cụm một xương `jo<i>` (con của move) hai slot `jo<i>b` (sau thân, nửa vòng xa) / `jo<i>f` (trước thân, nửa vòng gần), mặc định
    trống; aura bật hình theo nửa vòng. Hai đầu vòng mây lật ngang qua bề rộng ~0 (như xoay trong không gian), đổi slot đúng lúc đó
    nên không lộ chỗ nối; đuôi mây luôn kéo sau hướng bay;
  - runtime `AtomikPose.Overlay(ci, t)` phủ clip `aura` lên clip chính (xương cộng, hình theo khoá, độ đậm nhân); `AolaActor` chạy
    theo `Time.time` (liền qua mọi clip; Editor không Play thì đứng ở giây 0), `AtomikPlayer` theo đồng hồ riêng. Rig gộp tiến hóa:
    mây dạng sau (`n_jo*`) ẩn bằng độ đậm 0 ở clip trận, hiện cùng dạng sau trong `evolve`; mây dạng cũ tan cùng dạng cũ;
  - bản soi (`khung.png`, GIF, `baked.pkl` của `show`) đã ghép aura cùng giây như runtime (`beast.with_aura`).
- **Thân rắn nhiều xương** (`beast.serpent_clip`): xương `body` ở giữa thân; chuỗi `body` (nửa trước, `fw1..3`) từ giữa lên cổ, chuỗi
  `back` (nửa sau, `bk1..3`) từ giữa về hông, đuôi 4 đốt, bờm là chuỗi riêng `hair1..2` (tên `hair`, đừng đặt `mane*`: bị cả vòng tai
  lẫn vòng đuôi lắc chồng). Chuỗi đo khoảng cách từ xương đầu chuỗi trong vùng của nó, nên gốc chuỗi phải ở **một đầu** vùng (đặt ở
  giữa vùng thì phía bên kia bị tính như ngọn chuỗi). `"parent"`: đầu theo `fw3`, chân trước theo `fw2/fw3`, chân sau theo `bk2/bk3`.
  - `"spine": {"bones": [đầu ... chóp đuôi], "amp": [...], "coil_neck/back/tail", "paddle"}`: sóng chạy từ đầu xuống đuôi (pha tăng
    0,8 mỗi đốt, biên độ tăng ra đuôi); "nâng" dương = đầu xa thân nhấc lên (tự đổi dấu theo hướng xương); đầu xoay bù 80% góc cổ (mắt
    vẫn nhìn đối thủ); chân bơi lệch pha. Clip không lặp chạy số vòng sóng nguyên, biên độ riêng hoà vào/ra hai đầu clip nên khớp
    khung 0 idle. Dáng cuộn - bung theo nhịp đòn: attack/cast cuộn lấy đà rồi bung lúc nhả đạn; skill chồm cổ cao, bung khi sét giáng;
    hit cuộn chữ C ngược; idle 4 s = 2 vòng sóng. Xương thuộc spine bị loại khỏi `tail_bones` (khỏi lắc chồng).
- **Con dài dẹt:** game co tướng theo `game.height` nên rồng dài ~2 lần cao lòi khỏi mép sân. `"max_w": 1.42` (tỉ lệ rộng/cao tối đa)
  → khai chiều cao lớn hơn cho con vẽ nhỏ lại; tiến hóa dùng chiều cao hiệu dụng nên không giật cỡ.
- Soi: `dung_thu.py` (scratchpad, vá `thuy_long.RES`) dựng không đụng Assets; tour `PokiClash/Thử/Đảo Mộc: Thanh Long ra trận ở 3 dạng`
  (đang Play, ảnh `Temp/PokiShots/thanh_long_combat`) thấy mây bay thật.
- **Dạng cuối phải khác hẳn dạng trước** (người dùng: "dạng 2 và 3 chưa khác nhau lắm"): đổi cả màu (xanh lam đậm thay ngọc lam), thêm
  giáp, đồ (ngọc sấm), đổi chi tiết (râu, chóp đuôi hình tia sét) và **đổi dáng** (chồm dựng chữ S thay vì nằm ngang): nhìn bóng dáng
  đã biết là con khác. Gói `build_thanh_long_chien.py b3` → `tai_ve/L1_chien_b.png`. Dáng dựng hẹp (rộng/cao ~1,3) nên khỏi co.
- **Bờm, râu nhiều xương có lò xo** (người dùng: "thêm xương vào tóc cho mềm mại hơn"): bờm 3–4 đốt, râu 2–3 đốt; khoá `"soft"`
  (`beast.springs_of` → `longrig.Springs`: đuổi theo dáng động học, trễ, vượt nhẹ; `k` từng đốt 380 → 180, `damp` 0,6, `maxang` 10°;
  mềm hơn nữa thì lúc đánh lộ phần vẽ bù). Bờm chung lưới với sừng thì lò xo kéo nhoè sừng: tách `"sep": {"hair": "back", "rau":
  "front"}` (bờm lớp sau đầu, sừng đè lên; râu lớp trước), `"sep_grow": 24` (bờm vẽ bù dưới đầu), `"main_grow": 14–16` (lưới chính vẽ
  bù dưới râu, râu lắc không lộ lỗ). Hạt giống bờm đừng chạm lông gáy (nhãn gần nhất kéo cả mảng lông sau đầu vào bờm).
- **Hạt lá không viền sticker** (người dùng: "bỏ shader viền trắng ở các particle lá"): `beast.plain_slots` khai `game.plain` = slot
  hiệu ứng vẽ trước thân có ảnh lá (`leaf`/`leaves`). Runtime: `AolaActor.SplitFx` (AolaSticker bật) dựng các slot đó thành lưới riêng
  đặt cao `FxLift` 1000 trên actor; `AolaSticker.MakeFxLayer` thêm camera, RT, ảnh con cùng khung, shader `StickerOutline` với
  `_Plain = 1` (không viền). Slot sau thân giữ chung ảnh có viền (tách ra thì bị vẽ đè lên thân). Đã dựng lại Tiên Lá, Thỏ Hoàng,
  Mộc Tinh để có danh sách này. Chụp thử trong Editor (`AtomikForms.Shot`) không bật SplitFx nên vẫn một lưới như cũ.
- **Chiêu mỗi dạng một khác, dạng sau dữ hơn** (người dùng: "chiêu của dạng 1, 2, 3 đang giống nhau... càng dạng sau chiêu sét
  càng dữ dội, càng to"): `beast.form_cfg` cho khoá `"<tên>_form": {dạng: ...}` trong `juice` đè khoá chung (dict trộn, còn lại
  thay): `lightning_form`, `impact_form`, `phys_form`, `phys_pre_form`; `"motion"` theo dạng (`{1: "claws", 2: "roar", 3: "rear"}`).
  Tham số sét mới: `w_main`/`w_pre` (dày nét), `br_main`/`br_pre` (số nhánh), `wide_main` (bề ngang ảnh nhát chính), `main_scale`,
  `main_hold` (khung giữ thêm của cột sét), `clouds` [(dx, cỡ)], `cloud_stay`, `caster_r`/`caster_size`, `ring_pre`/`ring_main`,
  `dur`, `t_up`, `hit`, `seed`, `up` (tia bắn ngược lên trời từ ngọc: `bone`, `at` điểm trên ảnh concept, `height`, `win`; clip có
  `post` bù góc thế giới để tia luôn dựng đứng). Thanh Long: dạng 1 một tia mảnh, một mây nhỏ (1,7 s); dạng 2 ba nhát, hai mây (2 s);
  dạng 3 ngọc bắn tia lên trời, ba mây giông, năm nhát dồn dập rồi cột sét dày gần gấp đôi, 7 nhánh, giữ thêm 12 khung, khựng 0,2 s,
  rung 1,0, chớp màn mạnh, 24 hạt lá đất (2,5 s). Tướng nhiều nhát sét làm .atomik nặng hơn (mỗi nhát 5–8 ảnh tia).

## 18. Chiêu đa dạng theo dạng, đứng một chỗ bắn, há miệng (cả 3 đảo, 2026-11-09 tối)

Người dùng chê chiêu "một màu, toàn lao lên húc rồi lộn", dặn sáng tạo hơn (lore, Pokémon), đòn bắn xa đứng một chỗ, bắn từ mồm
thì há mồm. Đã áp cho 29 dòng Thủy, Mộc, Hỏa (Kim do phiên khác làm):
- **Kiểu chiêu đứng tại chỗ mới** (`beast.py`, cùng `FAR_SKILL`): `beam` (đạn nối đuôi thành dòng từ miệng, chỗ trúng chớp liên
  hồi), `vortex` (vòng xoáy dưới chân đối thủ quay nhanh dần, cột xoáy, hạt bay vòng, nổ cuối), `rain` (từng viên rơi chéo quanh
  đối thủ; dạng cuối thêm khối lớn rơi), `nova` (vòng bùng quanh thân theo nhịp + sóng đất tới đối thủ), `orbit` (đạn hiện ra bay
  vòng quanh thân rồi phóng lần lượt), `line_erupt` (cột trồi nối nhau dọc đất tới đối thủ, slot `fll*` trên xương `flyl*`: game
  dời theo quãng như đạn `fly*`). Độ mạnh `power_of`: dạng 1 = 1, dạng cuối = 3 (số viên, cỡ, độ dài, nổ cuối tăng theo).
- **Bảng đòn/chiêu từng dạng**: khối `_REDESIGN` trong `beasts_cfg.py` (giữa phần Hỏa và phần Kim), ghi ý lore/Pokémon từng dòng.
  Còn 9/72 dạng chiêu lao (dê, bò, cuộn giáp, cánh cụt trượt bụng, liên hoàn vuốt ở dạng 1). Đòn "lộn" (spin, tailwhip) đã bỏ.
- **Cảm giác trúng mặc định theo dạng** (`game_info`, tướng không khai `impact`): khựng, rung, bật lùi tăng theo dạng, dạng cuối chớp
  màn.
- **Đứng một chỗ bắn**: `attack_range` chỉ giật lùi; trận (`StageView`) không tự nhún tới đối thủ với clip `far`/`stay` của rig
  .atomik (`AolaActor.Stays`, `AolaSticker.Stays`). Trước đó đòn đánh không khai lao vẫn bị đẩy tới 35% quãng.
- **Há miệng**: vùng `jaw` + xương `jaw` ở góc miệng phía sau, `"jaw": {"open": độ}`; `beast.jaw_clip` há theo nhịp (đòn phun/hót/
  gầm, chiêu mana, chiêu gầm, trúng đòn), tiến hóa thì dạng sau há khi gầm. Gắn nhanh bằng `_add_jaw(id, dạng, đa giác, khớp, độ)`
  trong `beasts_cfg.py`. Bẫy: cằm không có nét mực ngăn với má thì hạt giống nhỏ không loang được (há thành khối vuông): đa giác
  phải **phủ trọn hàm dưới, cằm**; răng trắng giáp hàm và đầu bị coi là khe giấy (lỗ khi há): `drop_gaps` giữ khe giáp vùng `jaw`.
  Mỏ quặp khép kín (Phong Linh 2) bỏ qua. Điểm `mouth` cũ lệch (trên má, vây) thì sửa cho đạn ra đúng miệng.
- **Bẫy đã sửa 2026-11-10 (phiên Kim phát hiện):** `P.rot/scale/move` gọi theo **tên slot** mà slot nằm trên xương tên khác (đạn `fl*` trên
  `fly*`, vệt `jt*` trên `flyt*`, `fl_wave` trên `flyw`, `fll*` trên `flyl*`, và `ff_*` trước đây chung xương `far`) bị `Q.clean` bỏ
  khi xuất: đạn không xoay, không co giãn, hiệu ứng ở chỗ đối thủ đứng yên một cỡ, vật "rơi từ trời" không rơi. Nay
  `longrig.Pose.alias` (đặt trong `build_rig`) quy tên slot về xương riêng của nó, và mỗi `ff_*` có xương riêng con của `far` (vòng loang,
  hình đứng đặt ở đất). Viết clip mới: gọi theo tên xương hay tên slot đều được, trừ slot chung xương (`fx_ring_b/f` → `fx_ring`).

## 19. Đảo Kim: chibi chỉ dạng 1, thú mặc giáp (2026-11-09 tối, máy ổ D)

Cách mục 16 áp cho 10 dòng, 22 dạng (QUY_TRINH mục 20); gói `build_kim.py`, cấu hình `beasts_cfg_kim.py` (nạp cuối `beasts_cfg.py`).
- **Tỉ lệ theo dạng** (`STAGE` trong gói): dạng 1 chibi đầu khoảng 45%, dạng giữa 30%, dạng cuối 25%; ảnh mẫu dạng trước dặn "to,
  khỏe, ngầu hơn, đừng chép tỉ lệ thân". Ảnh ra vẫn chibi thì `gen.py --note "Not chibi at all ... head about one quarter"`.
- **Aola dạng robot, người lính** thì đổi thành thú mặc giáp giữ màu, chi tiết (nhím, tatu, cú, heo rừng, linh miêu).
- **Mặt nạ đồ trắng:** lông, chùm lông trắng gần màu giấy hở viền thì `close_fill` (x0, y0, x1, y1, r); viền giáp trắng khép kín bị
  thành lỗ thì `keep`; lòng bàn chân giữa các móng thì mỗi bàn một hộp r=14, đáy ngay trên mép bàn chân.
- **Chọn chi đánh:** chân không đặt tên `leg_f*` thì `limb(paw → arm_f → claw_f)` dùng càng (Bọ Cạp); `hover` đọc theo dạng
  (`style_of`), Chiến Thần chỉ dạng 2 bay.
- **Tờ hiệu ứng bị công cụ vẽ ảnh của Codex chặn** khi tả lưỡi thép, gai, giáo: tả bằng tấm kim loại, dải bạc, vệt cong, mảnh pha
  lê. Ảnh hiệu ứng chưa gen thì `_tam_thoi()` cuối `beasts_cfg_kim.py` tạm dùng ảnh tờ chung cùng vai trò (vào game được ngay).
- **Codex hết hạn mức** (`chay_hoa.log`: "usage limit", chờ 10 phút, thử lại mãi): báo người dùng giờ mở lại; runner tách
  (Start-Process) vẫn sống và tự gen khi có hạn mức.
- **Soát theo mục 0a, 18:** khối `_REDESIGN_KIM` trong `beasts_cfg_kim.py` (mỗi dạng một chiêu; 17/20 đứng tại chỗ). Kiểm bằng
  `<id>_game.json` của từng dạng (`far` / `lunge`). Trước 2026-11-10 lệnh xoay, co, dời theo tên slot (`fl*`, `ff_*`, `fll*`) bị bỏ
  (đạn không xoay, vật rơi không rơi); phiên khác đã sửa gốc (`Pose.alias`, mỗi `ff_*` một xương con của `far`), dựng lại là
  hưởng. Ảnh đạn dài phải chĩa sang phải (code xoay theo hướng bay). Tờ khung dạng chưa cuối có 6 hàng (thêm
  `evolve`), mỗi hàng 300 px: cắt hàng chiêu theo số hàng thật.

## 14. Gen bộ phận SAU khi rig (đảo Mộc, 2026-11-08 tối; đã bỏ, xem mục 15)

Người dùng dặn: gen một con hoàn chỉnh, rig xương, sau đó mới gen thêm bộ phận phục vụ animation. Lý do: loang màu phần bị che làm "ghép lệch".

Các bước:
1. **Concept:** đảo Mộc lấy theo concept đã duyệt của từng dạng (`ArtGen/Heroes/inbox/<id>_<k>/concept_duyet.png`), vẽ lại ở dáng rig được bằng `ArtGen/Spine/build_moc.py`. Dạng sau đính dạng trước (`L1_duyet.png` nếu Claude đã chọn bản gen lại).
2. **Rig:** cấu hình vùng, khớp ở `beasts_cfg.py`, soi `nhan.png`.
3. **Gen bộ phận:** `build_parts.py <id> <k>` sinh `gui_gpt/<mã>/duoi1.txt`, `duoi2.txt` kèm ảnh hướng dẫn (phần cần xoá tô hồng).
   - Lớp dưới 1: xoá mọi lớp trước thân, vẽ đủ thân.
   - Lớp dưới 2: xoá cả thân, vẽ đủ phần sau thân (chân xa, đuôi, cánh xa).
   - GPT vẽ trên đúng khung 1536x1024.
4. **Dựng:** `beast.py <id> all` tự lấy ảnh lớp dưới:
   - căn bằng ECC nhưng giữ "không dời" nếu căn không tốt hơn hẳn; dời quá 8 px thì bỏ phép căn; tương quan dưới 0,4 thì bỏ ảnh;
   - lớp thân dùng lớp dưới 1, các lớp sau thân dùng lớp dưới 2;
   - dải mọc thêm rộng gấp 3 lấy hình GPT; chỗ GPT bỏ trắng vẫn loang màu, nên không bao giờ hở.

Bẫy:
- Khe giấy trắng nhỏ (dưới 3000 px) giữa hai bộ phận thì `drop_gaps` bỏ khỏi hình. Lòng mắt, răng chỉ giáp một bộ phận nên giữ.
- Mây, bờm, chùm đuôi trắng viền hở: không lấp được bằng code (lấp ra khối vuông). Dặn GPT tô kem `#F4EEDC` hoặc xanh xám nhạt `#DDE9EE` và khép viền, rồi gen lại.
- Codex từ chối ảnh lớp dưới: gửi lại với `--note` ("harmless cartoon art edit of our own game character...").
- Con bay: `"hover": True` ở tướng, `"ground"` đặt dưới thân. Idle nhấp nhô, bóng co theo.

## 20. Rig Spine dựng bằng mã cho quái nhiều đầu, và bộ mổ xẻ rig Spine có sẵn (Hải Long, 2026-11-10)

Dùng khi con không rig được từ một ảnh liền (nhiều cổ chồng nhau, thân trồi từ nước, có hiệu ứng nằm trong rig). Nguyên tắc và
nhịp: `skill-petclash` mục 7.2, 15 và `mo_xe_quai_nhieu_dau.md`. Kết quả là JSON Spine 4.2 và `hai_long.atomik` (bản 3 của định dạng: có mặt nạ cắt, sự kiện, slot ẩn mặc định; mục 9).

**Tệp** (`ArtGen/Spine/`): `build_hai_long.py` (gói GPT: concept, 4 tờ mảnh, tờ M05 mí mắt và mảnh tia nước để dành cho VFX, tờ M06 lưỡi, tờ M07 hình nước đợt hai), `hai_long.py`
(`cat` cắt mảnh vào `inbox/hai_long/manh/`, `rig` dựng `inbox/hai_long/rig/`), `xem_spine_mau.html` (mẫu trang xem),
`lib/spine-player.js` (runtime 4.2.120 chỉ để xem), `mo_xe/` (bộ mổ xẻ).

**Bộ mổ xẻ `mo_xe/`** (rig bất kỳ: `.skel` hoặc `.json` + `.atlas` + ảnh; tự mở server tạm, cần Chrome hoặc Edge):
- `chay.py info <thư mục> <tên> <ra.json>`: xương, slot, lưới (đỉnh, xương bám), ràng buộc, clip, atlas.
- `chay.py keys <thư mục> <tên> <ra.json> <clip,...>`: mọi khoá (giờ, giá trị, kiểu đường cong).
- `chay.py mesh <thư mục> <tên> <ra.json> [slot,...]`: từng đỉnh của lưới với uv và (xương, trọng số): đọc cách chia trọng số.
- `chay.py sample ...`: toạ độ thế giới từng khung. `chay.py sheet <thư mục> <tên> <thư mục ra> "n=10&view=cx,cy,rộng,cao&t0=&t1=&loop=1&bones=1"`: tờ khung.
- `nhip.py <info.json> <keys.json> <clip> --root <xương> --chain a,b,c --bone x`: nhịp (khung nào nhiều khoá), bảng khoá xoay
  từng đốt của một chuỗi, tỉ lệ đường cong thẳng / bậc / bezier.
- Mẹo Chrome ngầm: `--headless=new --enable-unsafe-swiftshader --ignore-gpu-blocklist --virtual-time-budget=120000 --dump-dom`;
  kết quả in vào trang giữa hai mốc `JSON_BEGIN` / `JSON_END` (tìm mốc cuối SAU mốc đầu vì chuỗi này có cả trong mã trang);
  canvas ngoài DOM thì không gọi `renderer.resize`, tự đặt `gl.viewport` và `camera.setViewport`.

**Cắt mảnh từ tờ GPT:** loang nền trắng từ mép, tách cụm liền (`components`), gán tên theo ô lưới đã dặn trong prompt (`assign`);
mẩu nhỏ cách mảnh lớn dưới 40 px nhập vào mảnh đó; lòng vòng sóng khép kín thì loang từ tâm ra đục trong suốt; mảnh vào atlas
được loang màu ra vùng trong suốt (`bleed`) để lọc tuyến tính không kéo viền trắng. Thiếu ảnh thì `placeholder` vẽ hình giữ chỗ
(dựng rig song song lúc chờ gen).

**JSON Spine 4.2 viết tay** (lớp `Sk`):
- lưới có trọng số: `vertices` = với mỗi đỉnh `[số xương, (chỉ số xương, x, y trong hệ xương đó, trọng số) ...]`, `uvs`, `triangles`, `hull`;
- mặt nạ: attachment `{"type": "clipping", "end": <tên slot cuối>, "vertexCount", "vertices"}` đặt ở slot đứng trước mọi thứ cần cắt;
- ẩn mặc định: màu slot `ffffff00`; bật tắt bằng timeline `alpha` của slot (bước = hai khoá cách nhau 4 ms);
- khoá: `rotate {time, value}`, `translate / scale {time, x, y}`, đều là lệch so với dáng gốc (scale là nhân); bỏ `time` khi bằng 0;
  chỉ dùng nội suy thẳng (đã nướng).

**Dải lưới** (`strip_mesh` + `chain_weights`): mỗi đốt hai cột 3 đỉnh (mép trên, giữa, mép dưới bám mép hình); trọng số theo
hàm cơ sở B-spline bậc hai của vị trí dọc dải (giữa đốt 0,75 / 0,125 / 0,125; khớp 0,5 / 0,5; dồn về đốt đầu, đốt cuối ở hai mút).
Dùng cho cổ, râu, đuôi, lưỡi. **Không cho cột nào bám 100% một đốt**: đó là nguyên nhân thân gập ở khớp.

**Miệng:** thịt trong miệng đi theo hàm dưới. Lòng miệng là lưới 5×3: hàng dưới bám xương hàm 100%; hàng trên bám đầu ở sát bản lề
rồi chuyển dần sang hàm ra phía mõm (hệ số hàm 0 / 0,35 / 0,8 / 1 / 1) và hạ thấp dần cho mảng mỏng lại; lấy cả viền mực ba mép của
ảnh. Khép miệng thì nấp sau đầu và hàm. Lưỡi là dải riêng, con của xương hàm, vẽ trước hàm và sau đầu. Xương hàm có tỉ lệ 0,86: toạ
độ gắn chia cho tỉ lệ (phần tử thứ tư của bộ gắn xương trong `Sk.mesh`). Không để mảng thịt nào bám đầu mà thò ra khỏi hàm trên.

**VFX không nằm trong rig:** mỗi đầu có xương `mieng_<đầu>` (chỗ và hướng nhả); clip ghi sự kiện (`Clip.events` →
`animations[clip].events`, khai tên ở `events` gốc): `phun`, `het_phun`, `can`, `gam`, `het_gam`, `troi`, `roi_nuoc`. Trang xem hiện
sự kiện vừa bắn ở góc dưới.

**Giải cổ** (`neck_joints`): đường Bezier bậc ba từ chỗ trồi `E` (hướng `dirE`) tới gáy `H` (hướng tới = góc đầu + `arr`); nối
thêm một đoạn thẳng dưới `E`; lần ngược từ gáy, mỗi bước tìm điểm cách đúng một đốt (chia đôi 18 lần) nên đốt không co giãn, phần
thừa tự trượt xuống nước. Góc từng đốt `unwrap` theo thời gian rồi dịch bội 360° cho khớp dáng gốc. Sóng chạy dọc cổ cộng vào
đường cong trước khi lần.

**Dây mềm** (`rope`): Verlet "đốt sau đi theo đốt trước", 4 bước con mỗi khung; mỗi đốt có lò xo về dáng nghỉ so với đốt trước
(tần số riêng ≈ √k × 120 rad/s), hệ số giữ vận tốc `1 − 2ζ√k`, chặn góc khớp bằng tanh; lực ngoài qua `wind` (gió hình sin cho râu, trọng lực cho lưỡi: độ võng mỗi đốt ≈ g·dt² / k); clip lặp chạy đà hai vòng, clip không
lặp đứng yên 12 khung ở dáng đầu. Trả góc lệch từng đốt để khoá.

**Sóng** (`SPINES`, `WAVES`, `wave_inst`, `animate_water`): mỗi hình sóng có một đường sống lưng ghi tay theo ảnh (chân → lưng →
mào → đầu móc; soi ảnh có kẻ lưới 0..1 để đọc toạ độ); chuỗi `NC = 4` đốt chia đều trên đường đó; lưới 5×5, mỗi đỉnh chiếu lên
sống lưng để lấy vị trí dọc chuỗi rồi chia trọng số B-spline, nhân với độ gần (`exp(−(d / 0,3 cỡ)²)`), phần còn lại bám xương gốc.
Chiều cuộn tự tính từ tổng góc rẽ của sống lưng; lật hình bằng tỉ lệ x âm của xương gốc. Đời sóng theo pha `u`: dời, alpha 6
khoá; xoay chuỗi và co giãn 4 khoá (`u` = 0; 0,5; 0,8; 0,999); khoá cuối ở 0,999 để không trùng giờ khoá đầu vòng sau; `_close`
thêm khoá đúng `t = 0` và `t = D`. Thêm hình sóng mới: thêm vào `PIECES`, `assign`, `SPINES`, rồi đặt vào `WAVES`.

**Dải nước** (`ribbon`): lưới 3 hàng × 17 cột bám `NRB = 8` xương xếp dọc dải; hàng mào bám hẳn chuỗi, hàng giữa 55%, hàng đáy bám
gốc; khoá các xương nhấp nhô lệch pha.

**Mí mắt** (`fit_lid`): vùng cần phủ = cả vùng màu ấm liền với con ngươi (cam đậm + vàng nhạt), bao lồi, nới 5 px; dò góc, tỉ lệ, độ lệch cho mí phủ kín, không lòi ngoài đầu, ít đè gờ mày; kết quả in ra phải "còn hở 0 px", rồi soi ảnh cận.

**Xuất:** nướng 30 khung/giây, lọc RDP theo sai số từng loại; atlas xếp kệ, cạnh làm tròn bội 8, lưu bảng 256 màu
(`quantize(256, FASTOCTREE, FLOYDSTEINBERG)`). `viewer()` nhúng JSON, atlas, ảnh (data URI qua `AssetManager.setRawDataURI`) vào
một `xem.html` mở được bằng `file://`; khung nhìn riêng theo clip (`__VIEWS__`) nếu clip có hình vươn xa.

**Lưu ý môi trường:** heredoc Bash dài hay bị cắt, vá mã bằng file script (Write) rồi chạy; in tiếng Việt cần
`sys.stdout.reconfigure(encoding="utf-8")`; gen ảnh: `gen.py gui_gpt/hai_long/<file>.txt --steps M05` (khoảng 2 phút một tờ).

## 21. Lô 10 quái đảo Thủy: cách lai, lưới theo chiều cao, so concept bằng IoU (2026-11-11)

Người dùng giao 10 dòng tướng mới đảo Thủy dựa trên quái game tham khảo (`D:\RefAnimation`), thiết kế lại khác hẳn, rig "như Hải
Long", lưới dày mịn đều, đủ 8 clip (`appear, idle, attack, cast, skill, hit, die, evolve` + `aura` tuỳ), VFX ngoài rig. Đặc tả lô:
`ArtGen/Spine/quai/DAC_TA_LO_THUY.md` (mục 5 "Bài học"); thư viện chung `ArtGen/Spine/quai/` (README, có mục 7 ghi chú các dòng);
mỗi dòng `ArtGen/Spine/tmNN*.py`, ghi chú `inbox/tmNN_ghichu.md`; vào game bằng `quai/da_nhan.json` + `quai/vao_game.py`
(`--kiem`), dữ liệu tướng `quai/tuong_moi_thuy.py`, golden `quai/golden_thuy.py`, các bước Unity ở `quai/VAO_GAME.md`.

- **Cách lai là cách chuẩn cho thân hình cong tròn.** Dựng toàn bằng tờ mảnh GPT thì GPT vẽ thân thành ống thẳng, ghép lại lộ khúc
  ống, khe trắng, đầu cụt, vòng viền khớp búp bê; IoU với concept kẹt 0,6–0,8 dù dò khớp tự động (dòng 1, 7, 8, 9, 10 đều bị trước
  khi đổi). Cách lai: **lớp thân chính cắt thẳng từ concept** (vùng loang từ hạt giống, nét mực làm tường, ràng buộc màu theo vùng,
  nhãn gần nhất; như `thuy_long_lien.py`), lớp tách riêng (hàm dưới, chân xa, phụ kiện chồng, vây lưng) cũng cắt từ concept khi
  thấy rõ; **mảnh GPT chỉ cho phần bị che** (lòng miệng, mí, chân xa, đoạn cổ dưới nước) và làm nguồn vẽ bù. IoU lên 0,86–0,99.
- **Lớp dưới mọc thêm ≥ 30–40 px dưới lớp trên và vẽ bù** (dán mảnh GPT đã khớp, hoặc màu trung vị của lớp + vân + nét mực mép;
  `cv2.inpaint` lấy màu mực ở biên → dải nâu đen). Ranh hai lớp không có nét mực (đầu–cổ) kẻ theo **cung bo má**, không đường thẳng
  (lỗi đã gặp: khe nêm má–cổ, mảng chữ nhật dưới họng khi đầu ngẩng).
- **Mật độ lưới theo chiều cao con**: viền 1,5% H, trong 2% H (`luoi_vung/luoi_dai(..., buoc_theo_cao=H)`, `mu=True` cho chỏm ống).
  Bước pixel cố định cho con nhỏ (H 380) chỉ ra ~1000 đỉnh, tam giác to — người dùng chê "chưa dày mịn".
- **`so_concept.png` + IoU mặt nạ khung 0 idle với concept** là phép kiểm chính (đích ≥ 0,9 với cách lai; nước, phần cố ý đổi loại
  ra và ghi rõ). Tờ khung đẹp chưa đủ: chỉ chồng concept mới thấy sừng bẹp, thân gầy, đuôi thành que.
- **Đo nối clip trên đỉnh lưới đã da hoá của mọi slot** (gồm lò xo, dây mềm), cả khung 0 lẫn khung cuối mỗi clip; đo xương thì báo
  0 px trong khi khung đầu lệch 12 px. Dao động nền trừ giá trị tại t = 0.
- **Nhịp nện đúng chiều**: phần nện nhấc lên lúc lấy đà, chạm đúng `trung`, rồi về (lỗi đã gặp: chùy đuôi dựng lên sau cú cắn rồi giữ).
- **Concept**: không đính ảnh game tham khảo vào prompt (tả bằng lời); prompt tờ mảnh đính concept + "same silhouette and
  proportions". Duyệt chéo cả lô: dòng 6 từng trùng dòng 1 (kỳ giông chàm thế võ) → đổi sang bò bốn chân màu khác; dòng 3 tránh
  hoa văn xoắn ốc khắp thân (gợi một dòng ếch nổi tiếng). Nhiều dòng dạng cuối cùng ngả chàm: giữ được nhờ màu nhấn, dáng khác.
- **Tiến hoá gộp làm file dạng 1 nặng** (mang cả dạng 2): thu dạng sau 0,4–0,7 lần, lưới thưa 1,6–2,2 lần trong rig gộp; dòng boss
  nhiều cổ chấp nhận ~1,1–1,3 MB.
- **Soi runtime Spine thật**: lưới > ~4k tam giác + mặt nạ cắt làm tràn `PolygonBatcher` của spine-player (trang không trả JSON) →
  soi bằng bộ vẽ Python, kiểm thật bằng menu `PokiClash/Tướng/Chụp thử dạng .atomik` (ảnh `Library/PokiHeroShots/<id>_atomik_<k>.png`).
- **Agent song song**: một Codex mỗi lúc (khoá `gen.py`) nên 10 dòng gen concept + tờ mảnh mất vài giờ; Chrome ngầm và việc nặng
  qua `quai/khoa.py chrome|nang` (máy từng sập khi Chrome vẽ). Claude điều phối tự soi mọi báo cáo (so_concept, tờ khung, ảnh
  cận) — các agent hay báo "đạt" khi bóng dáng còn lệch.

## 22. Tướng tô phẳng rig thẳng từ concept, không tờ mảnh; há miệng bằng ĐỔI ẢNH (cá đèn lồng, 2026-11-11)

Tướng thứ 3 đảo Thủy (mã `ca_den`, 2 dạng), người dùng lên ý và duyệt concept; rig học con quái cá hai chân của game tham khảo.
Tệp: `ArtGen/Spine/build_ca_den.py` (gói GPT), `ca_den.py` (`cat <k>` cắt lớp, `rig <k>`, `all`), ghi chú `inbox/ca_den_ghichu.md`.
Kết quả: dạng 1 gộp tiến hóa 389 KB, dạng 2 337 KB; mọi clip nối về idle lệch 0 px.

**Không cần GPT vẽ mảnh nào cho phần thân.** Nét của game tô phẳng nên phần bị che tự tô được bằng mã:
- Phân lớp pixel theo màu chuẩn gần nhất (ảnh làm mờ 1,6 px + lọc đa số 5×5). Bẫy: mép mực / kem pha ra nâu xám, gần "chàm" hơn mọi
  màu chuẩn → chỉ cho nhận màu lam khi `B − R ≥ 45`. Dạng sau đổi tông thì khai bảng màu riêng (`MAU_K`), không thì thân dạng 2 bị
  chia đôi giữa "chàm" và "đốm".
- Tô lại chỗ khuất bằng **vân sáp lát**: lấy ô vuông sạch lớn nhất của màu đó (biến đổi khoảng cách), hoà chéo hai mép cho lát liền,
  lát kín khung rồi dán vào vùng cần tô (`o_van`, `lat`, `to_lai`). Nét mực thiếu thì kẻ lại bằng `net_muc` (Catmull-Rom, hơi rung).
- Nét mực chung của hai lớp kề nhau cho CẢ hai lớp (rộng 13–15 px): hai lớp lệch nhau vài px vẫn không hở.
- **Thân, vây, chân gần, đuôi là MỘT lưới** (người dùng dặn "một mảng màu"); lớp riêng chỉ cho thứ phải tách: hàm dưới + bụng + răng,
  cần đèn, chân xa, con ngươi. Kiểm: ghép các lớp lại so concept, in số pixel concept có mà ghép bị trống (phải 0).
- **Con ngươi trượt được mà không cần mặt nạ cắt**: xoá con ngươi khỏi tròng (tô kem), dựng con ngươi tròn đủ (dò elip trên mép con
  ngươi giáp tròng), rồi đặt **vành mắt** (viền + mí, cắt từ bản chưa xoá, rộng đủ che con ngươi) đè lên trên. Thứ tự: thân → con
  ngươi → vành.
- **Chân ngắn không cần xương đùi, ống**: bàn chân là xương con của `move`; ống chân là phần lưới hoà từ thân xuống bàn chân, tự giãn.
  Muốn nhấc chân, nhảy thì cho bàn chân đi theo thân (`theo_than`: lấy phép biến đổi của `than` so với dáng gốc áp cho bàn chân).
- Trọng số viết bằng **hàm của vị trí** (bán kính, góc quanh bản lề; độ sâu dưới đường miệng) dùng chung cho mọi lớp quanh miệng, nên
  các lớp không tách nhau ở khoé. Đường miệng lấy từ **mép trên vùng kem theo từng cột** (dò theo nét mực thì lẫn nét đáy bụng).
- Vào clip từ idle: khung 0 idle có độ trễ lò xo (cần đèn lệch 14 px so với dáng gốc) → `khop_dau` hoà 0,15 s đầu clip từ dáng đó.
- Bản nhẹ của dạng sau để gộp tiến hóa: `dung(2, ti=0.6, thua=1.8)` (ảnh 0,6 lần, lưới thưa 1,8 lần).

**Há miệng: uốn lưới không đủ, phải đổi ảnh như rig thương mại.** Ba lần người dùng chê bản uốn lưới:
1. Môi nhấc + hàm hạ quanh bản lề: miệng là khe hình nêm mở ra mép, "chỉ thấy mỗi thịt đỏ".
2. Thêm vòm môi, võng hàm, răng trên, lưỡi, họng: vẫn chê "phần bên kia phải thấy má bên kia chứ không phải thịt đỏ".
3. Thêm dải má giãn theo: "chắp vá quá, gen lại đi; của họ hai hàm trên dưới khít luôn ở mép bên kia".

Cách đạt (đúng cách con gốc làm: đổi cả ảnh thân trong 1 khung):
- **Nhờ GPT vẽ lại ĐÚNG concept, chỉ đổi miệng** (`build_ca_den.build_ha` → `luot_2_ha_mieng.txt` → `tai_ve/M01.png`). Prompt phải có:
  khối "KEEP IDENTICAL" liệt kê mọi thứ giữ nguyên chỗ, nguyên cỡ ("nếu đặt đè lên image 1 thì mọi thứ ngoài miệng phải trùng");
  miệng là **một hốc tròn khép kín**, hai môi gặp nhau ở cả hai mép, **mép bên kia nằm trong viền thân**, bên ngoài mép là dải má
  (màu thân ở trên, màu hàm ở dưới), "thịt trong miệng không chạm viền ngoài"; vòm môi nằm dưới mắt; răng dưới giữ như cũ, thêm răng
  trên; không nước dãi, không hiệu ứng. Kết quả đo lệch pha với concept: dưới 0,4 px (dạng 1), dưới 0,7 px (dạng 2): không phải khớp lại.
- **Mảnh `ha`** cắt từ ảnh đó: hốc miệng + răng + hàm và bụng (đặc) + vành môi quanh hốc trong 50 px (alpha mờ dần vào da cùng màu của
  lớp thân: không thấy đường nối) + má bên kia và mọi chỗ lớp thân bản khép bị khuyết (đặc). Slot ngay trên lớp thân, dưới mắt (mắt và
  con ngươi của bản khép vẫn dùng). Một lưới: trên vòm môi theo `dau`, dưới vành hàm theo `ham` / `bung`, trong hốc hoà; răng dưới và
  lưỡi theo hàm, răng trên theo môi.
- `mo(P, m)`: `m < 0,55` uốn lưới bản khép (táp miệng, hé miệng lúc ra đòn: chỉ dùng cho hé nhẹ); `m ≥ 0,55` bật `ha`, tắt lớp hàm và
  các lớp lòng miệng của bản khép, xoay `dau` / `ham` theo `(m − 1)` để rung lúc gầm. Đổi ảnh rơi vào khung chồm tới nên không lộ.

Luật rút ra: **dáng nào đổi hẳn hình khối (há to, quay mặt, nhắm mắt kiểu khác) thì xin GPT một ảnh "giống hệt, chỉ đổi chỗ đó" rồi đổi
ảnh; đừng cố uốn lưới.** Uốn lưới chỉ cho biến dạng nhỏ. Soi tờ khung không đủ để biết đạt: người dùng chấm bằng trang xem chuyển động.

Việc khác học được ở con này:
- Chiều cao game (`game.height`) không tính phần chìa cao như cần đèn (`soi.chieu_cao(..., bo=("den",))`), không thì thân bị thu nhỏ
  so với tướng khác. Khung sticker rộng 3,4 lần chiều cao đó: clip `appear` nhảy từ ngoài vào chỉ dời tối đa ~0,8 chiều cao.
- Lưới tự đè (đốm mực lốm đốm) khi cuộn đuôi sát thân hoặc ép chân bẹp: giảm góc, dời khớp xoay của thân về hông chân trụ.
- Clip bắn tia từ miệng phải **giữ há tới `phun` + 0,94 s thật**: dòng `n_tia` của game chảy 0,88 s kể từ sự kiện `phun` (người dùng
  chê Tí Tách ngậm miệng khi nước còn phun). Dạng sau chạy chậm hơn thì tính theo giây thật, không theo số khung.
- Cần mềm dài (cần đèn 9 đốt) đổ xuống: chia góc không đều (gập ở gốc, ngọn duỗi bớt), không thì nó cuộn thành vòng trước mặt.

## 23. RESKIN rig Spine gốc: giữ nguyên xương, lưới, animation, chỉ vẽ lại da (rắn sừng, 2026-11-11)

Dùng khi tướng làm theo một con có file Spine gốc và người dùng muốn nó "y hệt con gốc". Đã thử dựng rig riêng bốn lần (một
lưới, tách khúc, cắt mảnh từ concept, GPT vẽ lại vài mảnh) và đều bị trả: tự dựng không bao giờ ra đúng dáng và độ mềm của con
gốc. Reskin thì ra ngay lần đầu. Mẫu: `ArtGen/Spine/ran_sung.py`, ghi chú `ArtGen/Spine/inbox/ran_sung_ghichu.md` mục 10.

Hình và chuyển động gốc là của hãng làm game đó (như aola): chỉ để trong máy, không đăng công khai, kể cả artifact.

1. **Lấy dữ liệu gốc bằng runtime Spine thật** (`mo_xe/chay.py`): `info`, `att` (mọi hình: đỉnh thế giới, uv, tam giác, trọng
   số), `sample <clip,...> 30` (mỗi khung: vị trí và ma trận thế giới từng xương, tên hình và alpha từng slot).
2. **Tờ mảnh gốc cho GPT**: mỗi vùng ảnh cắt theo đa giác lưới của nó, phóng 3 lần, xếp lên tờ 1536 × 1024 nền trắng, ghi ô từng
   mảnh ra json. Chia hai tờ (thân, đầu) để mảnh đủ to.
3. **Prompt reskin**: ảnh 1 concept đã duyệt, ảnh 2 tờ mảnh gốc. Dặn giữ đúng hình bóng, chỗ, cỡ từng mảnh; tả từng mảnh theo
   thứ tự trên tờ (là gì, màu cũ đổi thành gì); mép mềm giữ mềm; lỗ để trắng; mảnh nào đổi dáng (chùm lông → sừng) thì nói gốc
   và mũi nằm ở đâu so với mảnh cũ. GPT giữ hình bóng sát (IoU 0,93–0,98).
4. **Nhận da**: cắt theo ô, dò lệch vài px theo hình bóng, thu về cỡ ảnh gốc × 4/3. Khoét lỗ (mảng trắng kín nằm ở chỗ mảnh gốc
   trong suốt); nhân alpha với alpha gốc nới vài px; mảnh không viền thì tô lại dải mép bằng màu giữa của nó. Mảnh đổi dáng:
   không dò lệch, nới khung ảnh theo hình mới.
5. **Nướng rig**: mọi xương gốc thành con trực tiếp của một xương (`nhun`), mỗi khung khoá vị trí, góc, tỉ lệ thế giới từ mẫu
   khung. IK, path constraint, transform constraint của rig gốc biến hết thành khoá FK nên `.atomik` chạy được. Lưới, uv,
   trọng số giữ nguyên. Trước khi nướng kiểm ma trận: trục xương lệch vuông góc dưới vài độ, không có ma trận lật.
6. **Mảnh cứng** (sừng, vũ khí thay cho chùm lông mềm): bám trọn một xương, lưới là ô chữ nhật cả khung ảnh. Chọn xương theo
   trọng số của mảnh kề nó (đốt cuối mà mảnh kề còn bám), không chọn xương của chính chùm lông cũ (nó vẫy).
7. **Clip con gốc không có**: viết khoá trên chính bộ xương gốc trong `extra.json` (giá trị = khoá idle giây 0 + lệch, mỗi khung
   một khoá), `chay.py sample ... extra.json` nạp vào runtime Spine thật rồi lấy mẫu như clip gốc. Ràng buộc của rig gốc vẫn
   chạy, không phải tự tính động học.
8. **Thứ tự vẽ** đổi được tự do lúc dựng slot (mẫu khung không mang thứ tự vẽ vào clip).
9. **Liền khối (người dùng dặn 2026-11-11): chỗ nối giữa các khúc thân không để nét mực.** Rig gốc viền đen quanh từng mảnh; với
   nét vẽ tay của mình, nét cắt ngang thân ở chỗ khúc trước đè khúc sau trông như ghép hình. Bỏ mực tự động (`ran_sung.py lien`):
   điểm mép nào suốt idle nằm trên một khúc thân khác cùng màu (hoặc sát nét mực của khúc dưới) thì tô lại bằng màu bên trong;
   giữ nét ở viền ngoài và chỗ đổi màu. Khung nào mép đó lộ ra thành viền ngoài (lao tới, bò, trúng đòn) thì clip đổi slot sang
   bản còn nét (`<hình>_vien`). Nhận "mực" bằng cả ba kênh đều tối, không bằng một kênh (lưng chàm đậm có kênh lam thấp).
10. **Dạng sau trên cùng rig:** phóng cả rig và ảnh da; đổi da (màu, sừng, lưỡi đuôi); mảnh con gốc không có (nanh, gai, vòng thân
    thêm) thì script vẽ hình giữ chỗ xám vào tờ mảnh cho GPT vẽ lại, rig đặt thành ô cứng lấy trọng số của da ngay chỗ nó bám
    (`tren_luoi`), chèn vào thứ tự vẽ; clip tự viết thêm nhát, tăng biên độ. Tiến hóa: `tienhoa.gop` với bản nhẹ của dạng sau,
    động tác hai dạng lấy từ khung đã lấy mẫu (`dat_khung(..., tt="n_")`).

Lỗi đã gặp:
- Vùng atlas `rotate: 90` gỡ sai chiều thì mảnh lộn 180°; mảnh tròn, hạt đậu nhìn vẫn "đúng", chỉ lộ ở mặt. Gỡ bằng
  `im.rotate(-deg, expand=True)` (PIL), kiểm bằng cách dựng rig với da GỐC và so với con gốc trước khi gen da mới.
- Dáng đứng của con gốc để đuôi ngay trước miệng: clip nhả tia phải hạ đuôi né đường tia.
- GPT vẽ hai sừng cong cùng chiều: lật ngang sừng bên kia.
- Cùng một tên hình có thể nằm ở hai slot (dáng đứng và dáng bò dùng chung vùng ảnh): mọi bảng chỉnh (xương bám, số dời) khoá theo
  TÊN SLOT. Khoá theo tên hình thì mảnh dáng bò bám nhầm xương dáng đứng mà tờ khung vẫn "trông đúng" nếu xương đó đứng yên.
- Mảnh đổi dáng to hơn mảnh cũ (sừng dạng sau): đừng đặt theo khung mảnh cũ; tính trục hình mới và đầu mút của mảnh nó nối vào
  (`truc_hinh`), đặt gốc vào đầu mút, trục theo hướng mảnh đó.
- Tô lại mép đã bỏ mực: lấy màu của lõi gần nhất (pixel sạch nằm sâu hơn bề rộng nét). Chọn màu theo "ngữ cảnh" tạo mảng lởm chởm
  ở chỗ hai màu giáp nhau. GPT hay tự tô sẫm đầu khúc: làm phẳng ngay lúc nhận da, trước mọi bước khác.
- Mảnh thêm kiểu "vòng thân thứ hai" chỉ đúng ở dáng cuộn: dáng duỗi (lao tới) phải ẩn tức thì, mờ dần thành bóng ma.

## 23. Con "hai hàm bản lề giữa thân", nanh rời, chân nấp sau thân (cá voi biến dị, 2026-11-11)

Tướng thứ 7 đảo Thủy (mã `ca_voi`, con gốc `monster_3281`). Tệp: `build_ca_voi.py`, `ca_voi_bo_cuc.py` (sơ đồ bố cục đính cho GPT),
`ca_voi.py` (`cat`, `rig`, `all`, `xem`), ghi chú `inbox/ca_voi_ghichu.md`.
- **Concept**: sơ đồ bố cục đính cho GPT phải dựng từ toạ độ đọc trên ảnh cận con gốc và mang đủ chi tiết; sơ đồ trơn thì ảnh ra
  "sơ sài". Sửa một phần thì đính bản nháp trước kèm khối "KEEP ... / CHANGE only ...".
- **Chỗ khuất sau nanh / sau chân tô bằng HÌNH HỌC khai trong CFG** (mép miệng trên, mép miệng dưới, mép ngoài dải môi, ranh hai tông,
  phần hàm khuất sau chân), không dùng "nhãn gần nhất" (ra răng cưa, sọc).
- **Vách họng** (`hong`): một lưới tô bằng mã, lúc nghỉ nấp sau hai hàm; trọng số chia theo vị trí giữa mép miệng trên và dưới (trên
  theo hàm trên, dưới theo hàm dưới) nên há to là nó căng ra lấp khoảng giữa hai hàm, không cần đổi ảnh.
- **Hai hàm là lưới bản lề mềm** (trọng số 0 ở bản lề → 1 trong một phần tư hàm); nanh là mảnh cứng, mỗi nanh một xương con của hàm.
- **Chân nấp sau thân**: phải là mảnh ĐỦ ở lớp dưới (dùng lại hình chân gần lật ngang nếu concept chỉ lộ một phần); gốc chân bám phần
  thân mà nó nấp sau (ở đây là hàm dưới), đầu chân bám đất nhưng trượt ngang theo thân; chặn không cho ép bẹp quá 35 %.
- **Xoay người (quay lưng lại)**: lật ngang cả con bằng tỉ lệ x của xương `move` đi qua 0 trong ~5 khung (kẹp |sx| ≥ 0,14).
- **Soi**: báo "đã sửa" chỉ sau khi dựng bằng runtime Spine thật và phóng to đúng chỗ người dùng chụp; bộ vẽ Python ở cỡ nhỏ đã để
  lọt lỗi vây bẹp hai lần.
