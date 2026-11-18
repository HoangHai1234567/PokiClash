# Ghi chú nghiên cứu: animation tướng (2026-11-10)

Số liệu và quy tắc tra từ nguồn ngoài, dùng để viết `SKILL.md`. Mỗi dòng có nguồn. Dòng ghi **[chưa kiểm chứng]** là chỉ thấy trong
kết quả tìm kiếm hoặc trang không mở được: coi là gợi ý, không coi là chuẩn. Bộ tài liệu gốc người dùng tải về nằm cạnh file này:
`VFX_KNOWLEDGE_BASE.md`.

## A. Animation tướng

### A1. Nhịp clip

- Dự án mẫu chính thức của Spine (30 khung/giây, đọc thẳng JSON): idle 1,0–2,1 s (hero 1,0; spineboy 1,67; snowglobe 2,1), idle
  con cú 6,67 s; hit 0,33 s; attack 0,4 s; shoot 0,63 s; death 2,2–4,9 s; roar 2,13 s.
  https://github.com/EsotericSoftware/spine-runtimes/tree/4.2/examples
- Attack 0,4 s của hero (12 khung, 30 khung/giây): key mỗi 2 khung; thân hạ thấp nhất ở khung 2 (lấy đà), vung ở khung 4–6, giữ tới
  khung 8, về thế đứng ở khung 12. (cùng nguồn)
- Pokémon GO, đòn nhanh (Tackle, Water Gun): dài 0,5 s, gây sát thương từ 0,3 s (60% clip). https://db.pokemongohub.net/move/221
- Pokémon GO, chiêu tụ lực: Charm 1,5 s, trúng ở 0,9–1,2 s; Hyper Beam 4,0 s, trúng ở 3,5–3,8 s (tụ lực chiếm 87%).
  https://db.pokemongohub.net/move/14
- Lấy đà theo khối lượng: nhẹ, nhanh 1–2 khung; vừa 3–4; nặng 5–8. Cú đấm: 2–3 khung lấy đà, 1 khung vượt quá, 4–6 khung ổn định.
  Đòn 4 khung đọc là "nhanh, khô", 12 khung là "chậm, nặng" (bài không ghi số khung/giây).
  https://www.udit.es/en/timing-y-spacing-en-animacion-que-es-y-como-mejora-la-sensacion-de-peso/
- Skullgirls: một cú đấm có thể chỉ có 6 khung; 1 khung lấy đà đã giúp dễ đọc hơn; vượt quá 1 khung rồi kéo về.
  https://80.lv/articles/tips-on-making-fluid-and-powerful-animations
- Khựng (hit-stop) ở game đối kháng (60 khung/giây): nhẹ khoảng 9 khung, vừa 11, nặng 13; Street Fighter 2 khoảng 14 cho mọi đòn
  thường. https://sonichurricane.com/?p=1043

### A2. Chống cứng kiểu "con rối"

- Lỗi gốc: chỉ cho xương gốc chuyển động nên mọi thứ đi cùng nhau. Sửa: từng mảnh đi lệch pha, mảnh phụ (mũ, mũi) đánh ngược chiều
  đầu, tay trễ hơn thân.
  https://gamedeveloper.com/design/tips-to-create-funny-and-juicy-character-animations-with-spine-basics
- Idle chỉ thở chung chung thì phẳng; dựng idle quanh chuyển động vòng tròn để gợi khối. (cùng nguồn)
- Smear không cần vẽ thêm: bóp méo xương đầu ở khung chuyển, thêm đà theo sau; che chỗ đổi ảnh bằng một nhịp co giãn nảy. (cùng nguồn)
- Khoảng cách đều và nhịp tuyến tính cho ra máy móc; dáng giữ phải có vi chuyển động (thở, ổn định dần); phản ứng ngay khung kế
  tiếp trông như "búp bê trên dây", nên giữ 4–8 khung.
  https://www.udit.es/en/timing-y-spacing-en-animacion-que-es-y-como-mejora-la-sensacion-de-peso/
- Lõi thân dẫn, chi theo sau; chỉnh đầu và cột sống trước rồi mới ra ngoài. https://blog.animschool.edu/?p=852
- Dám "bẻ gãy" chi để đẩy lực; người chơi không nhận ra khung sai.
  https://80.lv/articles/tips-on-making-fluid-and-powerful-animations
- Công cụ Offset của Spine: dịch key của mảnh phụ trong clip lặp mà không vỡ vòng (key đầu và cuối phải giống nhau).
  https://esotericsoftware.com/spine-keys
- Chớp mắt làm clip riêng 0,33–0,63 s rồi chồng lên idle (mẫu celestial-circus, snowglobe).
  https://github.com/EsotericSoftware/spine-runtimes/tree/4.2/examples
- Chớp mắt 2 khung nhắm, 1 khung giữ, 3 khung mở (24 khung/giây) **[chưa kiểm chứng]**.
  https://www.animationmentor.com/blog/tutorial-animate-blinks-eye-movement/

### A3. Kỹ thuật Spine dùng được cho mọi runtime xương + lưới

- Mặc định physics của runtime: inertia 1, strength 100, damping 1, mass 1, wind 0, gravity 0, limit 5000, 60 khung/giây.
  https://github.com/EsotericSoftware/spine-runtimes/blob/4.2/spine-libgdx/spine-libgdx/src/com/esotericsoftware/spine/SkeletonJson.java
- Số khởi điểm trong mẫu chính thức cho tóc, tai, áo choàng, dây: rotate 1, inertia 0,5, damping 0,85, strength 100, mass 1. Rất
  mềm: damping 0,15. Nặng (váy, lá): strength 113–165, mass 2,3–4, damping 0,84–0,94. Lông vũ: strength 48,8. Tóc co giãn: scaleX
  0,36–0,6. Thân rung: x/y 0,3–0,5, inertia 0,12–0,36. Limit 300–1500.
  https://github.com/EsotericSoftware/spine-runtimes/tree/4.2/examples
- Physics chạy 30–60 khung/giây; tắt Deterministic cho clip lặp; dùng Warm Up khi xuất; Scale X cho nén giãn; key được Reset và Mix.
  https://esotericsoftware.com/spine-physics-constraints
- Path constraint: Chain Scale cho thân mềm kiểu dây (các xương chung một cha); Chain cho đốt cứng; mix giữa 0 và 100 có thể lật
  hướng xoay. https://esotericsoftware.com/spine-path-constraints
- Ưu tiên trọng số; deform key dùng dè vì phình dữ liệu, nội suy thẳng và phải sửa lại khi thêm đỉnh.
  https://esotericsoftware.com/spine-keys
- Smooth xong mới Prune để giảm số xương mỗi đỉnh. https://esotericsoftware.com/spine-weights
- Sequence (hiệu ứng từng khung): các ảnh cùng kích thước; chế độ Hold, Once, Loop, Pingpong và bản đảo; số khung/giây riêng.
  https://esotericsoftware.com/spine-keys
- Event có int, float, string; mẫu đặt `footstep` ở 0,267 s và 0,533 s của clip chạy. https://esotericsoftware.com/spine-events
- Track cao chỉ đè các thuộc tính nó key; trộn mặc định 0,1–0,2 s; trả về thế gốc bằng animation rỗng; Clean Up có thể xoá key cần
  để đè track dưới. https://esotericsoftware.com/spine-applying-animations

### A4. Đồng bộ animation với hiệu ứng

- Khựng: kẻ đánh và kẻ trúng đứng cùng thời lượng; dài theo sát thương, có trần; đạn ngắn hơn, điện dài hơn.
  https://sourcegaming.info/2015/11/11/thoughts-on-hitstop-sakurais-famitsu-column-vol-490-1/
- Trong lúc khựng: nạn nhân rung ngang, biên độ giảm dần; kẻ đánh rung nhẹ và vẫn nhích một chút; 4 khung chuyển từ giật sang
  dáng đau. (cùng nguồn)
- Đạn: chỉ nạn nhân khựng (8–12 khung ở 60 khung/giây), người bắn không khựng; đạn đang bay không dừng theo khựng của đòn khác.
  https://sonichurricane.com/?p=1043
- Hiệu ứng ba pha: lấy đà, đỉnh (nhiều phần tử nhất, tương phản cao nhất), tan (ngắn, mờ). Logic bắn tín hiệu HIT và END nên đổi
  thời lượng không phải dựng lại. Vòng báo trước 0,5–2 s. https://80.lv/articles/vfx-staples-shape-color-and-motion/
- Dựng dáng nhân vật trước, rồi canh hiệu ứng theo dáng. (cùng nguồn)
- Chiêu dạng tia giữ dáng nhả suốt cửa sổ sát thương: Solar Beam dài 5,0 s, cửa sổ 2,8–4,8 s (40% clip).
  https://db.pokemongohub.net/move/116
- Đạn rời tay ở "attack point" (lính bắn xa trong Dota: 0,5 s, thu chiêu 0,3 s); cú giật của nạn nhân tính theo lúc đạn chạm
  **[chưa kiểm chứng]**. https://liquipedia.net/dota2/Attack_backswing

### A5. Tiến hóa

- Pokémon Emerald (đọc mã nguồn, khoảng 60 khung/giây): tướng tô trắng thành hình bóng, hạt xoắn lên 160 khung, rơi vòng cung 96
  khung, hai dạng thay nhau phóng to thu nhỏ với tốc độ tăng từ 8 lên 128 (khoảng 350 khung, tự tính từ mã), hạt hút vào 48 khung,
  loé trắng toàn màn (mờ lại từ khung 32) cùng hạt toé 128 khung. Tổng khoảng 13 s.
  https://github.com/pret/pokeemerald/blob/master/src/evolution_graphics.c
- Thứ tự cảnh: chữ, tiếng kêu dạng cũ, nhạc dạo, chuỗi trên, tiếng kêu dạng mới, nhạc mừng; huỷ giữa chừng thì loé trắng rồi trả
  về dạng cũ. https://github.com/pret/pokeemerald/blob/master/src/evolution_scene.c
- Pokémon GO: cảnh tiến hóa giảm từ khoảng 30 s xuống 18–20 s **[chưa kiểm chứng]**.

### A6. Phân biệt theo dáng

- Nặng thì cần nhiều thời gian tăng và giảm tốc; giữ nguyên dáng, đổi số khung giữa các dáng.
  https://education.siggraph.org/static/HyperGraph/animation/character_animation/principles/timing.htm
- Dạng tiến hóa sau: tăng lấy đà từ 1–2 lên 5–8 khung, ổn định dài hơn.
  https://www.udit.es/en/timing-y-spacing-en-animacion-que-es-y-como-mejora-la-sensacion-de-peso/
- Bốn chân: hông và ngực là hai "bóng nảy" lệch pha, đầu là bóng thứ ba; đuôi làm sau cùng, từng trục một; đi chậm 40 khung một
  vòng; chạy nhanh cần sống lưng dẻo và nén giãn. https://gamedeveloper.com/art/animating-four-legged-beasts
- Mỗi con một kiểu chuyển động: lơ lửng nhẹ, dậm đất sắc gọn, bò trườn, bay uyển chuyển (Monster Legends).
  https://kevurugames.com/monster-legends
- Rắn, rồng dài: path constraint Chain Scale. https://esotericsoftware.com/spine-path-constraints
- Con to thì vòng lặp dài hơn: raptor đi 1,27 s so với spineboy 1,0 s.
  https://github.com/EsotericSoftware/spine-runtimes/tree/4.2/examples
- Chim: vòng vỗ 9 khung, đập xuống 5 khung giữa, nâng lên 3; thân trễ cánh 2 khung **[chưa kiểm chứng]**.

**Không tìm được nguồn có số:** Clash of Critters, Summoners War, AFK Arena, Brawl Stars, Hollow Knight, Cult of the Lamb, Dead Cells;
"The Art of Screenshake" và talk Skullgirls (không có bản chép lời); "13 VFX techniques" (khoá sau trả phí); tiến hóa của Digimon,
Temtem, Monster Hunter Stories; dáng rùa, blob, cá. Số đo Clash of Critters của chính dự án nằm ở skill `pokiclash-hero-fx` mục 1b.
