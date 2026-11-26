---
name: animation-petclash
description: >
  Bộ skill ANIMATION của PokiClash (game pet clash 2D vẽ tay: bắt, nuôi, tiến hóa thú, hai con đối đầu trên một góc máy cố định).
  Gồm nhịp clip của tướng (idle, attack, cast, skill, hit, evolve), chống cứng kiểu con rối, luật chuỗi xương dài (cổ, đuôi, thân
  rắn), mỗi dáng một cách động, nguyên tắc diễn (lấy đà, dáng snap, nén giãn, phụ kiện trễ, đòn có lực, idle có trò), khớp animation
  với hiệu ứng, quái lớn nhiều đầu trồi từ nước, lỗi hay gặp và bảng kiểm. Dùng TRƯỚC khi dựng, sửa hay chấm bất kỳ animation nào
  của tướng hoặc quái, rồi mở `pokiclash-spine-rig` để làm chi tiết. Hiệu ứng (tia, đạn, nổ, hạt) thuộc bộ `vfx-petclash`.
---

# animation-petclash: animation tướng cho game kiểu pet clash

Đây là **skill gốc của bộ Animation**. Nó nói **làm gì và vì sao**; skill con nói **làm thế nào trong dự án này**.

| Bộ | Skill | Dùng khi |
|---|---|---|
| Animation | `animation-petclash` (skill này) | nguyên tắc, nhịp clip, diễn, khớp với hiệu ứng, bảng kiểm |
| Animation | `pokiclash-spine-rig` | rig xương từ ảnh, lưới có trọng số, viết clip, soi khung, xuất `.atomik` vào Unity |
| Animation | `animation-humanoid` | nhân vật dạng người (dealer, NPC, tướng dạng người): hướng bàn tay trên bàn, tay ống cao su, biên độ |
| VFX (bộ khác) | `vfx-petclash` → `pokiclash-vfx`, `pokiclash-hero-fx`, `pokiclash-fx-congthuc` | tia, đạn, nổ, hạt, cảm giác đánh |

**Ranh giới giữa hai bộ** (người dùng dặn 2026-11-10):
- **Animation:** thân tướng, phụ kiện dính thân (tai, đuôi, bờm, lửa trên lưng), môi trường dính thân (nước dưới chân quái).
- **VFX:** thứ gì bay ra khỏi thân (tia, đạn, vụ nổ, hạt).
- **Chỗ bám để lại cho VFX:** rig chỉ chừa xương miệng / `muzzle` (trục x chĩa hướng nhả) và sự kiện trong clip (`phun`, `het_phun`, `gam`…).
- **Vật thuộc rig nhưng bay tới đối thủ** (giáo, búa, móc xích): rig khai xương `fly_*` / `far`, đường bay do code lái.

Tài liệu đi kèm trong thư mục này:
- `nghien_cuu_animation.md`: số đo nhịp clip, chống cứng, physics, đồng bộ với hiệu ứng, tiến hóa, phân biệt theo dáng (có nguồn).
- `mo_xe_quai_nhieu_dau.md`: mổ xẻ một con quái nhiều đầu đứng trong nước của game tham khảo (xương để làm gì, nước có theo đầu
  không, mặt nạ cắt, nhịp từng clip, cần gen gì, tách ảnh thế nào) và con đã dựng theo cách đó (Hải Long Ngũ Đầu,
  `ArtGen/Spine/hai_long.py`). Đọc khi làm quái / boss nhiều đầu, nhiều cổ, thân dài trồi lên từ nước.

Khi các quy tắc xung đột: **luật của dự án (mục 1) > đọc được trong trận > hiệu năng > đẹp > chi tiết.**

## 1. Luật của dự án cho animation

- **Tướng bám con gốc.** Giữ hướng nhìn, đầu, miệng, tỉ lệ của con gốc; chỉ đổi thứ người dùng dặn. Lời dặn nhắc "con gốc" mà có
  nhiều ứng viên thì hỏi kèm tờ ảnh, đừng tự chọn.
- **Có file Spine gốc làm mẫu thì dịch ngược xem họ tách bộ phận thế nào** rồi chia mảnh theo đúng cách đó (`pokiclash-spine-rig`
  mục 00). Có rig gốc thì vẽ mảnh đúng khung từng part, dùng nguyên lưới + clip của rig; đừng tự dựng xương, tự viết clip.
- **Tướng aola** (`fightassets/pet<id>.swf`) vẽ đè lên rig vector, giữ animation aola (CLAUDE.md mục Hình tướng,
  `ArtGen/Heroes/QUY_TRINH.md`).
- **Không vẽ VFX vào rig** (ranh giới ở trên).
- **Viền vẽ SAU CÙNG** (người dùng dặn 2026-11-21): nhân vật có viền thì gen ảnh không viền, rig và làm xong mọi clip, người dùng
  chốt animation, rồi mới vẽ viền bằng Paint của AtomSpine, chỉ ở mép nhìn thấy được (viền ngoài, mảnh trước đè mảnh sau), không vẽ
  ở chỗ nối. Cách làm: `pokiclash-spine-rig` mục 000.
- **Tướng làm từng con.** Người dùng lên ý tưởng, duyệt từng bước; không làm theo lô.
- **Không tự đổi số chỉnh của người dùng** (`reskin/<tên>/adjust.json`).
- **Hình và chuyển động aola là của Baitian:** không đăng công khai, kể cả artifact.
- **Kiểm bằng runtime thật**, không bằng bộ vẽ tự viết. Lỗi rách, hở thì phóng to đúng chỗ rồi mới báo đã sửa. Đo góc nhảy 360°
  giữa khung và bước dời ở 60 khung/giây trước khi mở cho người dùng.
- Người dùng chấm trên điện thoại Android.

## 2. Bộ clip và nhịp

| Clip | Dài | Khung trúng / nhả | Ghi chú |
|---|---|---|---|
| idle | 2,0 s, lặp liền | | thở 3%, phụ kiện lệch pha, một điểm phá nhịp ở 62–72% |
| attack | 0,8–1,0 s | 0,40–0,52 s | lấy đà 0,3 s **ngược chiều** cú đánh, ra đòn 2–3 khung, khựng 0,1 s, vượt quá rồi về |
| cast | 1,0 s | 0,5–0,6 s | ngửa tụ sức, nén, chồm tới nhả, giật ngược, về |
| skill | 1,6–1,9 s | 0,9–1,3 s | tụ lực 0,4–0,6 s, phát, 1–3 nhịp, về |
| hit | 0,6 s | | bật ở 0,07 s, giữ, về |
| evolve | 2,8 s | | gồng, lốc tụ, đổi dạng lúc lốc đậm nhất, nổ, gầm, hoà về idle dạng sau |

- 80% độ "đọc" của cú đánh nằm trước lúc chạm. Một khung lấy đà cũng giúp dễ đọc.
- Lấy đà theo khối lượng: nhẹ 1–2 khung, vừa 3–4, nặng 5–8. **Dạng tiến hóa sau:** lấy đà dài hơn, ổn định dài hơn, vòng lặp dài hơn.
- Giữ nguyên dáng, đổi số khung giữa các dáng là đổi được cảm giác nặng nhẹ.

## 3. Chống cứng kiểu con rối

- Không chỉ cho xương gốc chuyển động. Mỗi mảnh lệch pha; mảnh phụ đánh ngược chiều đầu; tay, đuôi trễ hơn thân.
- Lõi thân dẫn, chi theo sau. Đuôi trễ 0,05 s mỗi đốt, tai 0,06 s, chuông 0,1 s; biên độ lớn dần ra ngọn.
- Dáng giữ vẫn có vi chuyển động (thở, ổn định dần). Phản ứng ngay khung kế tiếp trông như búp bê trên dây: giữ 4–8 khung.
- Nén giãn giữ thể tích: đòn thường (0,9; 1,09), nện tới (0,85; 1,15); hồi về trong 0,18–0,3 s.
- Smear không cần vẽ thêm: kéo giãn xương ở khung nhanh nhất rồi trả.
- Dựng idle quanh một chuyển động vòng (không chỉ lên xuống) để gợi khối.
- Tướng vẽ lại phải có chuyển động phụ: mây, vòng, đồ bay, tai, đuôi, lửa không được đứng im.
- Physics cho đuôi, tai, tóc (nếu runtime có): bắt đầu từ inertia 0,5, damping 0,85, strength 100; nặng thì mass 2–4.

Luật cho **chuỗi xương dài** (cổ, thân rắn, đuôi, râu), đọc từ khoá thật của một rig Spine thương mại
(`mo_xe_quai_nhieu_dau.md` mục 6b):

- **Đầu mút dẫn, thân theo.** Đốt gần đầu đạt cực trị trước, mỗi đốt về phía gốc trễ thêm khoảng 5 khung (0,17 s). Khoá cùng
  khung cho mọi đốt là cả chuỗi lắc như cái que.
- **Hai đốt kề xoay ngược dấu nhau**, biên độ lớn nhất ở giữa chuỗi (tới 39°), nhỏ ở gốc và ở đầu: thân uốn mạnh mà đầu gần như
  đứng yên, mắt vẫn nhìn đối thủ. Đầu trôi theo thân thì con vật vô hồn.
- **Idle chỉ cần 2 khoá một vòng cho mỗi đốt** (hai cực trị, đường cong êm). Cái làm idle không đều là **điểm phá nhịp** ngắn
  0,4–0,5 s (thè lưỡi, táp miệng, chớp mắt, giật mặt), mỗi phần làm ở giờ riêng.
- **Ra đòn: dáng → dáng, nội suy thẳng, nhanh chậm do khoảng cách khoá.** Trình tự: nhún 0,2 s → cuộn lấy đà, giữ 4 khung →
  **khung gãy** (đốt giữa bật trước, ngọn còn ở sau) → chạm trong 1 khung (giãn 1,13 đúng khung đó) → quá đà → **giữ có trôi**
  0,5 s (mỗi đốt đổi 3–7°) → về.
- **Giữ chiêu, gồng:** hai dáng lệch nhau 2–3° đổi nhau mỗi 1–2 khung. Rẻ và rõ hơn mọi kiểu nhiễu.
- **Trúng đòn: không lấy đà, sóng chạy ngược từ ngọn về gốc.** Ngọn đạt đỉnh ở 0,07 s, giữa chuỗi ở 0,2 s, gốc gần như đứng yên.
- **Dải lưới bám chuỗi xương: không đỉnh nào bám cứng một đốt.** Chia trọng số kiểu B-spline bậc hai (giữa đốt 0,75 đốt đó +
  0,125 mỗi đốt kề; ở khớp 0,5 / 0,5; rig mẫu dùng 0,70 / 0,15 / 0,15). Giữa đốt bám 100% thì mỗi khớp là một chỗ gập, tăng số
  đốt không chữa được.
- **Thịt trong miệng thuộc về hàm dưới và há theo hàm** (người dùng dặn 2026-11-10; rig mẫu cũng bám lòng miệng 100% vào xương
  hàm). Chỉ một màng nhỏ ở khoé miệng nối lên đầu; hàm trên không giữ lại mảng thịt nào; phía trước giữa hai hàm là khoảng trống.
  Ba kiểu sai đã gặp: mảng tròn bám đầu lơ lửng; khối thịt lấp kín cả khe miệng; dải thịt ở lại với hàm trên, chìa ra như cái
  lưỡi thứ hai. Soi miệng ở dáng há to nhất và dáng ngửa đầu.
- **To, quan trọng thì chậm và sau cùng:** đầu phụ trồi lên trong 0,33 s, đầu chính 1 s. Tới nơi còn lắc tắt dần vài nhịp.

## 4. Mỗi dáng một cách động

| Dáng | Điểm riêng |
|---|---|
| Bốn chân | hông và ngực là hai khối nảy lệch pha, đầu là khối thứ ba; đuôi làm sau cùng |
| Hai chân | vai dẫn tay; đổi trọng tâm qua hông trước khi ra đòn |
| Chim | vỗ cánh là nhịp chính, thân trễ cánh; lông đuôi xoè lúc nhả |
| Rắn, rồng dài | thân nhiều xương uốn sóng lan từ đầu xuống đuôi |
| Nặng (rùa, đá) | lấy đà dài, ít nảy, đất rung khi dậm |
| Tròn, mềm | nén giãn lớn, lăn |
| Cá, thân bơi | quẫy đuôi dẫn, vây trễ |
| Nhiều đầu, cổ dài trồi từ nước | mỗi đầu một pha, không hai đầu nào cùng làm một việc cùng lúc; thủ lĩnh làm sau cùng và to nhất; xem mục 7 |

Đòn và chiêu của các dòng phải **khác kiểu nhau** (bảng `_STYLE`, `_REDESIGN` trong `beasts_cfg.py`), không toàn "nhảy lên rồi ra chiêu".

## 5. Diễn: nguyên tắc và những gì người dùng đã chê

- **Lấy đà ngược chiều cú đánh**, đổi dáng lớn ở khung ra đòn (bóng dáng khác hẳn), **khựng lúc chạm**, theo đà vượt quá rồi về.
- **Dáng "snap":** dáng ra đòn nhảy tới ngay (không nội suy) ở khung ra đòn; pixelfx giữ dáng tay chân theo **bước 12 khung/giây**
  (vị trí chân vẫn mượt) cho cảm giác vẽ tay. Thử cho đòn đánh, chiêu: lượng tử hoá góc xoay xương thân, tay theo 1/12 s, giữ dời
  `move` mượt; soi rồi mới áp cả loạt.
- **Nén giãn giữ thể tích:** đòn thường (0,9; 1,09); nện, đáp nặng tới (0,85; 1,15); Celeste nhảy (0,6; 1,4), đáp (1,6; 0,4) là mức
  cực, game mình dùng nhẹ hơn. Hồi về 1 trong 0,18–0,3 s.
- **Phụ kiện trễ và ngược chiều** thân (đuôi trễ 0,05 s mỗi đốt, tai 0,06 s, chuông 0,1 s), biên độ lớn dần ra ngọn.
- **Con đánh vẫn hơi động lúc khựng** (Sakurai) để không chết hình; con bị đánh rung ngang.
- **Đòn khác kiểu nhau** giữa các dòng (không toàn "nhảy lên rồi ra chiêu"): xem bảng kiểu đòn, chiêu ở `beasts_cfg_hoa.py`,
  `beasts_cfg.py` (`_STYLE`).

Người dùng đã chê và dặn (ghi lại để không lặp):
- **Animation không đơn điệu:**
  - idle phải có trò riêng (điểm phá nhịp), không chỉ thở và lắc nhẹ;
  - lớp phụ (lá, lông, áo) tách lớp, có xương đung đưa;
  - clip xuất hiện có ý tưởng;
  - lửa trên thân phải uốn lượn (lưới + chuỗi xương), không đứng im.
- **Đòn tấn công có lực.**
  - Đừng chỉ xoay FK tay trên dáng có sẵn.
  - Dáng khoá phải có nhún, bật, nện, quá đà; cổ chân IK bám đất để hông nhún và chồm tự do.
  - Chiêu lao thì thêm trò lấy đà (cào chân) và đổi hẳn dáng lúc lao so với lúc thủ.
  - Mẫu: `ArtGen/Spine/soi_giap_don.py`.
- **Động tác có điểm tựa:** thân được đẩy, kéo thì chi phải chạm và bám điểm tựa trước, giữ yên chỗ bám.
- **Dáng khó thì gen ảnh riêng:** tay đổi hẳn dáng (ôm vũ khí hai tay, há to, quay mặt) thì xin GPT một ảnh dáng đó rồi đổi ảnh
  trong một khung. Đừng ghép mảnh dáng đứng bằng IK, đừng há to bằng uốn lưới.
- **Tách hàm để há mồm:** tướng có gầm, đớp thì mặc định tách hàm dưới có xương; soi khớp đầu–cổ ở dáng ngửa lớn nhất. Trong
  miệng không có thịt thừa.
- **Hạt idle theo hệ** (than, bọt, lá, sỏi, lấp lánh) là việc của VFX: `pokiclash-hero-fx` mục 7.

## 6. Khớp animation với hiệu ứng

Đây là phần dễ sai nhất và người dùng đã nhắc nhiều lần.

1. **Dựng dáng tướng trước, canh hiệu ứng theo dáng.** Clip có một khung nhả (`hitTimes` trong `.atomik`).
2. **Pha lấy đà của hiệu ứng chạy cùng lúc tướng lấy đà.** Bộ Thủy: `StageView.PreFx` phát hiệu ứng ngay khi clip bắt đầu, truyền
   `lead` = giờ tới khung nhả; nước nhả đúng khung đó. (Bộ Hỏa phát ở khung nhả; chiêu có pha tụ dài nên chuyển sang cách này.)
3. **Tướng giữ dáng nhả tới khi dòng hiệu ứng gần xong** rồi mới về đứng: tia và luồng phun giữ hết dòng; thương, kim giữ tới mũi
   cuối phóng đi; cầu giữ tới lúc rời miệng; mưa, vòi rồng giữ gần hết (`HoldOf`, `HoldNuoc`).
4. **Cảm giác trúng đi theo lúc hiệu ứng chạm đối thủ**, không theo khung nhả: khựng, rung, bật lùi, số sát thương đều chờ đạn tới
   (`impactAt`, `fxHitAt`, `BattlePlayer` chờ `travel`).
5. **Chọn hiệu ứng khớp động tác có sẵn của từng dạng.** Dạng lao tới thì hiệu ứng nổ đúng lúc chạm; dạng gọi trời thì vật rơi từ
   trên; dạng dậm chân thì thứ gì đó trồi lên hoặc lan trên đất. Không ép một hiệu ứng cho mọi dạng.
6. **Clip do lớp hạt lo thì bỏ ảnh hiệu ứng trong clip** và bỏ luôn khai báo `far`, không thì khung camera sticker dời theo, dạng
   nhỏ bị cắt chân.
7. **Miệng, tay, vũ khí:** điểm phát lấy từ `muzzle` của rig; tia phải ra đúng chỗ đó ở cả hai chiều lật.
8. Khựng dừng cả hai con và hiệu ứng của cú đó; đạn đang bay của đòn khác không dừng theo.

Phía hiệu ứng của cùng chuyện này (pha tụ, thời điểm chạm, lớp vẽ): `vfx-petclash` mục 7.

## 7. Quái lớn nhiều phần: nhiều đầu, thân dài, trồi lên từ nước

Đã làm thật một con (Hải Long Ngũ Đầu, 482 xương, 7 clip, 2,98 MB). Chi tiết mổ xẻ con tham khảo và bảng "luật của con gốc → làm
bằng mã" ở `mo_xe_quai_nhieu_dau.md`; cách dựng ở `pokiclash-spine-rig` mục 20.

**Trước khi làm, mổ rig tham khảo theo năm câu hỏi** (công cụ `ArtGen/Spine/mo_xe/`):
1. Xương này gắn để làm gì? (cây xương, số đốt mỗi chuỗi, mảnh nào bám xương nào)
2. Phần nào độc lập với phần nào? (lần tổ tiên của từng slot: nước có là con của đầu không)
3. Khoá nằm ở đâu? (đếm khoá theo nhóm xương và theo clip: dung lượng do đâu)
4. Người ta đặt dáng ở khung nào, đốt nào lệch đốt nào, đường cong gì? (`nhip.py`) Lưới chia trọng số ra sao? (`chay.py mesh`)
5. Mẹo che là gì? (mặt nạ cắt, thứ tự vẽ xen kẽ, bản sao lệch nửa chu kỳ)

Chỉ lấy cấu trúc và nhịp. Hình, thiết kế, diễn xuất phải là của mình.

**Nguyên tắc dựng:**
- **Tách hai nhóm xương gốc:** thân và môi trường (nước). Môi trường chạy vòng lặp riêng, không là con của phần nào trên thân.
- **Chỉ đạo diễn đầu mút** (vị trí, góc, độ há của từng đầu); phần nối (cổ) để mã giải, phần mềm (râu, bờm) để mô phỏng rồi nướng.
- **Thứ tự vẽ xen kẽ** đầu sau → nước giữa → đầu trước → sóng trước: có chiều sâu mà không cần 3D.
- **Mặt nạ cắt ở mặt nước:** trồi, chìm, vươn dài đều là trượt phần thừa xuống dưới mép cắt; sóng trước không bị cắt phủ lên đường cắt.
- **Nền lặp + lớp phản ứng:** băng chuyền sóng (mỗi cuộn hai bản sao lệch nửa chu kỳ) làm nền; đầu trồi lên hay bổ xuống thì toé
  vương miện nước, giọt, vòng sóng đúng chỗ.
- **Sóng mềm là sóng tự biến dạng, không phải sóng trượt:** mỗi cuộn là một ảnh trên chuỗi 4–6 xương đặt dọc sống lưng sóng;
  cả đời sóng nó dâng lên tại chỗ, các đốt xoay cùng chiều cho **mào tự cuộn lại** (đốt gần mào đi 40–60°), trôi ngang rất ít
  (một phần năm bề dài sóng), mờ vào rồi mờ ra. Cho ảnh sóng trượt ngang 200–300 đơn vị là "tấm bìa trượt".
- **Nước đẹp nhờ dày và nhiều cỡ:** vài chục cuộn từ vòi nước cao tới cuộn xoắn tí hon, xếp nhiều lớp quanh chỗ từng cổ trồi
  lên, một dải sóng dài quét phía trước, hàng gợn lăn tăn dưới cùng (dải lưới nhiều xương nhấp nhô lệch pha).
- **Không hai đầu nào cùng pha:** idle lệch pha và biên độ; ra đòn so le 0,06–0,25 s; trúng đòn hồi về lệch 0,02–0,04 s; chết lần lượt.
- **Tia, đạn, vụ nổ của chiêu thuộc lớp VFX của game, không vẽ trong rig** (người dùng dặn 2026-11-10). Rig chỉ diễn thân và
  phần môi trường dính với thân (nước dưới chân), rồi để lại chỗ bám cho VFX: một xương ở miệng mỗi đầu (`mieng_<đầu>`, trục x
  chĩa hướng nhả) và sự kiện trong clip (`phun`, `het_phun`, `can`, `gam`, `troi`, `roi_nuoc`). Thứ gì bay ra khỏi thân thì hỏi
  trước nó thuộc rig hay VFX.
- **Mọi clip dài bội số nửa chu kỳ nền** và dao động tuần hoàn của clip không lặp tính theo giờ lùi `t − D`: hết clip nối vào idle
  không giật. Khung đầu clip xuất hiện và khung cuối clip chết phải trống hoàn toàn.
- **Dùng lại hình:** hai thiết kế đầu, hai cổ cho năm đầu; một ảnh râu cho mười sợi; sóng dùng lại nhiều lần.

**Nhịp bảy clip đã dùng** (giây): xuất hiện 4,8 (nước nở 0,95; bốn đầu vọt lên 1,05 / 1,25 / 1,50 / 1,72; thủ lĩnh 2,35; gầm
3,55–4,25); đứng 3,2 lặp; tấn công 1,6 (cắn ở 0,45 và 0,68); chiêu gầm 3,2 (ngửa 1,15, bung 1,32, giữ rung tới 2,35); chiêu phun
nước 3,2 (nén 0,8, phun 1,0 so le 0,06, giữ tới 2,3, thở ra); trúng đòn 0,8 (đỉnh 0,07); chết 4,0 (giật 0,07 và nhắm mắt; từng
đầu ngửa ra lè lưỡi 0,30 → 0,85, lắc lư 0,6–0,8; đổ ngửa xuống nước; nổi lộn ngược 0,5; chìm; nước tan 3,5 → 4,0).

**Chết cho có hồn:** không đổ thẳng xuống. Giật → nhắm mắt → **lả đi và giữ một nhịp cho người xem đọc được** (ngửa đầu, hàm trễ,
lưỡi rũ, lắc lư) → mới đổ → nổi một nhịp → chìm. Lưỡi, râu là dây mềm có trọng lực nên tự rũ đúng theo mọi tư thế đầu.

**Kiểm:** dựng tờ khung bằng runtime Spine thật (không phải bộ vẽ tự viết), soi cận râu và chỗ nối cổ ở clip giật mạnh nhất
(trúng đòn), đo lệch khung cuối mỗi clip so với khung đầu idle, đo lệch đầu cuối của idle, mở trang xem một file. Tờ khung không
thay được việc xem chuyển động: nói rõ nếu chưa xem ở tốc độ thật.

## 8. Lỗi hay lặp lại

- Có file Spine gốc của con mẫu mà không dịch ngược xem họ tách bộ phận thế nào, tự chia mảnh theo ý mình (gộp các khúc thân thành
  một lưới, cả đầu một ảnh): người dùng trả lại. Luật và công cụ: `pokiclash-spine-rig` mục 00 (`mo_xe/chay.py att`, `to_manh.py`).
- Mổ xẻ rig tham khảo mà chỉ lấy mẫu khung: chỉ biết "nhanh cỡ nào", không biết người ta đặt dáng ở khung nào và vì sao. Phải đọc
  cả khoá (`ArtGen/Spine/mo_xe/nhip.py`).
- Phần mềm (râu, tóc) mô phỏng quá mềm, không chặn góc: cú giật mạnh vò nó thành cục, lưới gãy khúc.
- Cả chuỗi xương khoá cùng khung, cùng dấu: lắc như que.
- Dải lưới bám 100% một xương ở giữa đốt: thân gập ở từng khớp (`animation-petclash` mục 3).
- Lòng miệng không đi theo hàm dưới: mảng lơ lửng, khối lấp kín khe miệng, hoặc dải thịt ở lại với hàm trên như cái lưỡi thứ hai (`animation-petclash` mục 3).
- Vẽ tia, đạn của chiêu vào rig: việc của lớp VFX.
- Cố há miệng to bằng uốn lưới: ra khe hình nêm, lòng miệng đỏ chạy ra tới viền, chắp vá. Dáng đổi hẳn hình khối (há to, quay
  mặt) thì xin GPT một ảnh "giống hệt concept, chỉ đổi chỗ đó" rồi **đổi ảnh trong một khung**, như rig thương mại (`pokiclash-spine-rig` mục 22).
- Mảnh phủ (mí mắt, miếng che) đặt theo công thức mà không đo: hở một khe. Dò vị trí và in số điểm còn hở.
- Chỉ soi tờ khung thu nhỏ rồi báo "mượt": chỗ gập ở khớp, chỗ hở trong miệng chỉ thấy khi soi cận hoặc xem chuyển động.
- Gen ảnh có viền mực rồi cắt mảnh, vá viền chỗ nối bằng mã: nét đôi, vạch cắt ngang thân, viền đứt, răng cưa, chỗ khuyết lộ ra
  khi chi vung (nhím Kim 2026-11-21, người dùng chê "nhem nhuốc"). Gen không viền, vẽ viền sau khi chốt (`pokiclash-spine-rig` mục 000).
- Dựng thân hình cong tròn toàn bằng tờ mảnh GPT: thân thành khúc ống thẳng, lộ khe, vòng viền khớp búp bê, lệch concept. Dùng
  **cách lai** (thân cắt thẳng từ concept, mảnh GPT chỉ cho phần bị che) và kiểm bằng ảnh chồng concept + IoU (`pokiclash-spine-rig` mục 21).

## 9. Bảng kiểm trước khi báo xong

- [ ] Clip đúng nhịp mục 2: khung trúng / nhả đúng giờ, idle lặp liền, clip không lặp nối vào idle không giật?
- [ ] Lấy đà ngược chiều cú đánh; khung ra đòn đổi hẳn dáng; khựng lúc chạm; quá đà rồi về?
- [ ] Chuỗi xương dài: đầu mút dẫn, đốt kề ngược dấu, không khoá cùng khung cùng dấu? Dải lưới không bám cứng giữa đốt?
- [ ] Idle có điểm phá nhịp và phụ kiện lệch pha, không chỉ thở?
- [ ] Không hở khớp, không mảnh rời thân, thứ tự lớp như con gốc, lỗ hai lớp, hàm và miệng đúng (bảng 8 mục tự soi của
  `pokiclash-spine-rig`)?
- [ ] Đã đo góc nhảy 360° và bước dời ở 60 khung/giây; khung cuối mỗi clip khớp khung đầu idle?
- [ ] Rig để lại xương miệng và sự kiện cho VFX, không vẽ tia, đạn, vụ nổ vào rig?
- [ ] Nhân vật có viền: ảnh rig không viền, viền chỉ vẽ sau khi người dùng chốt animation, chỉ ở mép thấy được, đã soát mép lộ ở
  dáng duỗi xa nhất của mọi clip?
- [ ] Đã xem chuyển động ở tốc độ thật bằng runtime thật (tờ khung không thay được), soi cận chỗ nối ở clip giật mạnh nhất?
