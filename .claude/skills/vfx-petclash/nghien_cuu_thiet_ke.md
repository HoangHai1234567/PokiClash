# Ghi chú nghiên cứu: nguyên tắc thiết kế hiệu ứng (2026-11-10)

Đối chiếu các ý chính của `VFX_KNOWLEDGE_BASE.md` với nguồn gốc, rồi bổ sung số đo và quy tắc còn thiếu. Mỗi dòng có nguồn.
**[chưa kiểm chứng]**: chỉ thấy gián tiếp hoặc trang không mở được.

## 1. Đính chính so với bộ tài liệu gốc

| Ý trong bộ tài liệu | Kết quả đối chiếu |
|---|---|
| "Theo LoL: đỉnh sáng và bão hòa đạt trong 1/4 đầu vòng đời" | **Không có trong bản hướng dẫn của Riot.** Câu này của blog VFX Apprentice (mẹo 9). Bản Riot chỉ ghi: mọi hiệu ứng có lấy đà và tan; phần ra là phụ (sáng, bão hòa, độ đặc thấp hơn); nhịp "dynamic", không tuyến tính. Dùng như gợi ý, không coi là luật của Riot |
| Tránh 0% và 100% | Đúng, và áp cho **cả độ sáng lẫn độ bão hòa**; lý do là dễ lẫn với môi trường hoặc UI |
| Thang độ quan trọng: đòn thường < chiêu < tuyệt chiêu | Đúng nhưng bản gốc có **6 bậc**: hạt idle, phép phòng thủ, đòn thường (chỉ ghi "cỡ nhỏ"), phép sát thương, chiêu đổi cục diện, tuyệt chiêu (bão hòa, độ đặc, dải sáng cao nhất, cỡ lớn) |
| "Nhanh hơn 60 nhịp/phút là hung hăng" | Bài chỉ có số cho **hồi máu: dưới 60 nhịp/phút**; cho đòn đánh chỉ ghi "ngược lại", không có số. Gốc của luật nhịp tim là Julian Love (GDC 2013, Diablo) |
| "Một chiêu có khoảng 3 animation: vào, lặp, ra" | Bài ghi "khoảng ba animation mỗi phép" điều khiển bằng tín hiệu; chữ "vào, lặp, ra" **không có**. Ví dụ Unstable Dome gồm lấy đà, 2 đoạn lặp, trúng, tan |
| Phần thưởng càng lớn, dẫn dắt càng dài | Phần "dựng dẫn dắt trước khi lộ thưởng" đúng; phần "tỉ lệ theo cỡ thưởng" **[chưa kiểm chứng]** nguyên văn. Nguồn khác đỡ cho ý này: Hearthstone gắn cường độ hiệu ứng với độ hiếm của thẻ |

Các ý còn lại đã xác nhận: chính và phụ; giữ hiệu ứng ngắn; hai kiểu nhịp xung và nhịp; hiệu ứng tức thì vẫn cần đoạn ra; ba
pha; phần tử trúng và tan ở lớp riêng gọi bằng tín hiệu HIT / END; tối đa khoảng ba màu với một màu chủ; chiều sâu bằng độ trong
và độ sáng.

Nguồn: bản hướng dẫn của Riot (bản lưu) https://drive.google.com/file/d/1eyNV-GxtpGLD2UuBU3BbkeNrQfSdok5C/view ·
https://www.vfxapprentice.com/blog/10-league-of-legends-vfx-design-tips ·
https://www.vfxapprentice.com/blog/the-soul-of-effects-what-is-timing-in-vfx ·
https://80.lv/articles/vfx-staples-shape-color-and-motion/ ·
https://media.gdcvault.com/GDC+2022/Speaker+Slides/VFXasagamedesignlanguage_Nguyen_An-Tim.pdf ·
特效美术圣经 https://realtimevfx.com/uploads/short-url/zgKTB2RQJTPjJeGksSU6IxLzXKr.pdf

## 2. Thời lượng (khung quy về 60 khung/giây)

- Bảng của một blog công cụ, không dẫn nguồn ngoài: lấy đà 0,1–0,25 s (6–15 khung); chớp 0,03–0,1 s (2–6); giữ 0,05–0,15 s (3–9);
  bung 0,1–0,3 s (6–18); tan 0,3–1 s (18–60). Lấy đà cộng va chạm không quá 1/3 tổng. https://particlefx.studio/guides/2d-vfx-timing
- Tổng thời lượng, cùng nguồn: trúng nhỏ 0,2–0,5 s; trúng nặng hoặc chiêu 0,5–1 s; nổ có khói 0,8–2 s; vòng lặp 1–4 s.
- Khung trúng kiểu LoL khoảng 0,1 s (6 khung); thứ tự tàn: thân sáng chính, loé, tia lửa, chấm mờ.
  https://80.lv/articles/constructing-vfx-worthy-of-league-of-legends/
- Lấy đà của chiêu vùng (Meteor Strike) chỉnh trong 0,5–2 s. https://80.lv/articles/vfx-staples-shape-color-and-motion/
- Nếu người chơi phải phản ứng: lấy đà = 0,25 s + thời gian thao tác + đệm; pha đánh chỉ vài khung.
  https://gdkeys.com/keys-to-combat-design-1-anatomy-of-an-attack/
- Chớp sáng 0,075–0,15 s (5–9 khung), kèm một chớp tối sát trước hoặc sau; co vào trước khi bung; lệch giờ bắt đầu và kết thúc
  giữa các lớp.
  https://realtimevfx.com/t/help-ideas-on-how-to-make-it-more-snappy-crunchy-poppy-feedback-is-immensely-welcome/21693
- Khung va chạm (impact frame) 1–3 khung; dài hơn đọc thành đổi cảnh. https://particlefx.studio/guides/anime-impact-frame
- Không tìm được số riêng cho tia, đạn và tuyệt chiêu trong các nguồn đã đọc.

## 3. Không che mục tiêu, đọc được

- Không nguồn nào cho giới hạn phần trăm màn hình; chỉ có luật định tính. Riot: tan nhanh, không đặc 100% ngay cả lúc đỉnh.
- Không chồng quá nhiều lớp alpha; phần tan dư vài khung là che hình bóng đối thủ.
  https://www.vfxapprentice.com/blog/10-league-of-legends-vfx-design-tips
- **Phép thử hình bóng:** tô đen cả hiệu ứng vẫn phải nhận ra. Một phần tử chính (ít nhất 1/4 bề ngang), 2–3 phần tử phụ. Soi ở cỡ
  thật trong game (tia trúng khoảng 48 px trên điện thoại); kiểm bằng ảnh xám và giảm còn 2–3 mức sáng.
  https://particlefx.studio/guides/vfx-shape-language
- Thứ quan trọng nhất tại mỗi thời điểm phải hút mắt nhất; đạn phải cho thấy hướng ngay cả khi đứng hình (đuôi mờ dần).
  https://www.leagueoflegends.com/en-us/news/dev/clarity-in-league/
- Màu không được là kênh duy nhất báo trạng thái (người mù màu); đánh với máy cho phép nổ to, đặc hơn đánh với người.
  https://media.gdcvault.com/GDC+2022/Speaker+Slides/VFXasagamedesignlanguage_Nguyen_An-Tim.pdf

## 4. Hình theo hệ

- Tròn, cong: an toàn (hồi máu, bong bóng, khói, khiên). Tam giác, gai: nguy hiểm, tốc độ, hướng. Vuông: vững, máy móc. Băng trong
  ví dụ là tam giác chĩa lên. https://particlefx.studio/guides/vfx-shape-language
- Chiêu mạnh hơn thì to hơn, hình sắc hơn; hồi máu hình không đe doạ; hất tung có phần tử dọc mạnh; trói chân là vòng đất cộng trụ
  dâng. https://realtimevfx.com/t/anatomy-of-a-league-of-legends-missile-part-2-what-are-we-communicating-with-our-vfx/13062
- **Lửa:** dựng bằng nét chữ S, khoét bằng nét chữ C, đỉnh nhọn bằng móc; gốc dày thon dần và luôn đi lên; tránh khối đều kiểu "kem
  đánh răng". https://www.vfxapprentice.com/blog/how-to-draw-stylized-fire-flames
- **Nước:** chỉ dùng cạnh tròn; gợn, bong bóng, bọt đi cùng hướng dòng nhưng khác cỡ; càng xa tâm càng vỡ thành bong bóng nhỏ dần.
  https://www.vfxapprentice.com/blog/how-to-draw-stylized-water
- **Sét:** gai sắc, dùng khung chớp, không cho sét "bò" ngang màn hình. **Khói:** sợi mảnh chuyển động như lửa, cụm cuộn như mây.
  **Đất:** mảnh vỡ xoay. Mọi hệ: to – vừa – nhỏ, tránh đối xứng. https://www.vfxapprentice.com/courses/elemental-foundation
- Mộc, kim, độc, quang, ám: không tìm được luật hình có nguồn; bản của Riot chỉ có bảng màu theo chủ đề.

## 5. Nước vẽ tay

- Một cú nước toé dài hơn 1 s một chút; pha vọt lên vẽ mỗi khung một hình (hình 2 cao khoảng 1/4, hình 3 gần đỉnh), sau đó hai
  khung một hình; có vượt quá ở đỉnh. https://www.schoolofmotion.com/blog/photoshop-animation-splash
- "Váy" nước cao nhất ở hình 2–4, **rách từ đáy**, đến hình 7 thì vỡ hẳn; mỗi mảnh bay theo cung riêng, nhỏ dần, mọc đuôi, tách vụn
  rồi biến mất. (cùng nguồn)
- Giọt nhanh chóng thành cầu do sức căng bề mặt; giọt bắn nhỏ dần khi bay xa, không tắt phụt; cần gợn hoặc vết tại điểm chạm (ý
  kiến diễn đàn). https://pixeljoint.com/forum/printer_friendly_posts.asp?TID=24418
- Gilland, *Elemental Magic*: cỡ và thời lượng cú toé tuỳ lượng nước bị chiếm chỗ; đừng thêm quá nhiều cú toé phụ
  **[chưa kiểm chứng]**.
- Sóng, tia nước: không tìm được nguồn có số.

## 6. Khựng, rung, chớp

- Smash Ultimate: số khung khựng = ⌊sát thương × 0,65 + 6⌋, trần 30 khung, hệ điện × 1,5. Melee: ⌊sát thương / 3 + 3⌋, trần 20.
  https://www.ssbwiki.com/Hitlag
- Sakurai: hai bên khựng bằng nhau; sát thương càng lớn càng dài; đạn khựng ít hơn; rung giảm dần trong lúc khựng, đứng đất rung
  ngang, trên không rung dọc; máy quay càng xa rung càng mạnh.
  https://sourcegaming.info/2015/11/11/thoughts-on-hitstop-sakurais-famitsu-column-vol-490-1/
- Mức đặt sẵn: yếu 0–0,03 s; mạnh 0,05–0,08 s; chí mạng hoặc tuyệt chiêu 0,1–0,15 s; chớp 0,08 s. Đòn nhiều nhịp chỉ khựng ở nhịp
  đầu và nhịp cuối; chỉ một chớp ngắn trên mục tiêu. https://uhiyama-lab.com/en/notes/unity/unity-game-feel-hit-feedback/
- Khựng 60–120 ms, dài hơn thì giống giật máy. Rung = trauma², lệch tối đa 12 px, giảm 4 mỗi giây, một cú cộng khoảng 0,3–0,4.
  https://dev.to/saltmire/godot-4-screen-shake-and-hit-stop-in-one-script-11eh
- **An toàn:** chớp không quá 3 lần mỗi giây; vùng chớp cùng lúc không quá 1/4 ô 341 × 256 px (ở 1024 × 768); tránh chớp đỏ bão
  hòa. https://developer.mozilla.org/en-US/docs/Web/Accessibility/Guides/Seizure_disorders
- Capcom (8 / 12 / 16 khung cho nhẹ / vừa / nặng) **[chưa kiểm chứng]**.
