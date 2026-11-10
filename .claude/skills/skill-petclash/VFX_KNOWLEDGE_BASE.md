---
title: Knowledge base VFX game 2D (Spine + engine) — dành cho AI agent
version: 1.0
updated: 2026-11-10
scope: VFX cho game mobile 2D, đặc biệt game bắt/nuôi/tiến hóa pet làm bằng Spine; kèm particle/shader phía engine (Cocos, Unity, Godot)
language: Tiếng Việt, thuật ngữ kèm English / 中文
---

# HƯỚNG DẪN CHO AGENT

File này là kiến thức đã chắt lọc từ tài liệu VFX tiếng Trung và quốc tế. Dùng nó để:
1. **Thiết kế** một hiệu ứng: đi theo mục 1 → 6 (nguyên tắc), rồi mục 11 (công thức mẫu).
2. **Dựng** hiệu ứng trong Spine: mục 7. Phía engine (shader, particle): mục 8.
3. **Review / chấm điểm** hiệu ứng: mục 10 (checklist + rubric định lượng).
4. **Tối ưu**: mục 9.

Quy ước độ tin cậy:
- `[NGUỒN]` = rút trực tiếp từ tài liệu (danh sách nguồn ở mục 14).
- `[HEURISTIC]` = con số kinh nghiệm, dùng làm điểm khởi đầu rồi chỉnh theo game.
- `[TỔNG HỢP]` = công thức agent tự suy ra từ các nguyên tắc có nguồn, chưa có tài liệu nào mô tả nguyên văn.

Thứ tự ưu tiên khi các quy tắc xung đột: **Gameplay/đọc được > Hiệu năng > Thẩm mỹ > Chi tiết**.

---

# 1. NGUYÊN TẮC CỐT LÕI

1. **Gameplay là trên hết.** VFX là phản hồi cho người chơi, không phải trang trí. Khi cần rõ ràng thì giảm hiệu ứng. `[NGUỒN: 80.lv, Creative Assembly]`
2. **Ba yếu tố của mọi hiệu ứng: Hình (Shape) – Màu (Color) – Chuyển động/Nhịp (Motion/Timing).** Mỗi hiệu ứng thiên về một yếu tố, nhưng phải kiểm cả ba. `[NGUỒN: 80.lv]`
3. **Tách mỗi hiệu ứng thành phần tử và hỏi từng cái:** nó quan trọng cỡ nào, có phải trọng tâm không? Nên hút bao nhiêu chú ý? Xuất hiện/biến mất khi nào, thế nào? Hòa với phần tử khác ra sao? Có tạo nhiễu không? `[NGUỒN: 80.lv]`
4. **Thiết kế cho đúng góc camera của game** (game 2D thường có 1 góc cố định). `[NGUỒN: 80.lv]`
5. **Làm cho "đã" trước, đẹp sau.** Chốt timing bằng hình khối đơn giản trước khi thêm chi tiết/shader. `[NGUỒN: VFX Apprentice]`
6. **Hiệu ứng ngắn.** Hiệu ứng kéo dài làm rối trận đấu, che silhouette địch, che chiêu khác; thời lượng cũng là tín hiệu độ quan trọng. `[NGUỒN: LoL VFX style guide]`
7. Hoạ sĩ VFX thường **không có concept art**, nên phải tự nắm nguyên lý mỹ thuật (màu, sáng tối, bố cục). `[NGUỒN: 特效美术圣经]`

---

# 2. NHỊP ĐỘ (TIMING / 节奏)

## 2.1 Ba pha của mọi hiệu ứng `[NGUỒN: 80.lv, LoL guide, VFX Apprentice]`

| Pha | EN / 中文 | Đặc điểm |
|---|---|---|
| 1. Lấy đà | Anticipation / Wind-up / Fade-in · 蓄力/起手 | Ngắn, báo trước cho người chơi (và đối thủ). Thời lượng thường do Game Design quy định. |
| 2. Đỉnh | Climax / Impact / Pop · 爆发/打击 | Nhiều phần tử nhất, **tương phản cao nhất, bão hòa cao nhất**. Theo LoL: đỉnh giá trị + bão hòa đạt được **trong 1/4 đầu** vòng đời hiệu ứng. |
| 3. Tan | Dissipation / Fall-off / Erosion · 消散 | Ngắn, **tương phản thấp, opacity thấp**, tan mượt, không cắt đột ngột. |

Câu chốt (LoL): dẫn não bằng anticipation → "quá tải" não đúng khoảnh khắc nó chờ → cho não thời gian xử lý.

Biến thể cho game hành động (绝区零): **打击 → 反馈 → 消散** (impact → feedback → dissipation), kể cả trong ảnh tĩnh/thiết kế. `[NGUỒN: B站 cv48141767]`

## 2.2 Hai kiểu mẫu nhịp `[NGUỒN: VFX Apprentice]`
- **Impulse (xung)** — có một đỉnh cường độ rõ:
  - *Instant*: bỏ anticipation, mở bằng cường độ cao → rất "punchy" (đòn đánh thường, hit spark).
  - *Crescendo*: có thời gian tích tụ, nhiều phần tử phối hợp (cái phình ra, cái co vào). Càng nhiều phần càng giàu nhịp nhưng dễ "lệch tông".
- **Rhythm (nhịp)** — cường độ dao động, không có một đỉnh:
  - *Flowing/Regular*: lặp, êm (sương, thác, lửa trại, chỉ báo nhặt đồ).
  - *Disruptive*: cường độ thay đổi dần theo vòng đời.
- Có thể ghép: quả cầu lửa = rhythm (tụ) → impulse (phóng) → rhythm (bay) → impulse (nổ).

## 2.3 Quy tắc nhịp cụ thể
- **Tempo ↔ cảm xúc:** nhịp nhanh hơn nhịp tim (~>60 BPM) đọc là hung hăng; chậm hơn đọc là tích cực/thân thiện. **Hiệu ứng hồi máu < 60 BPM, hiệu ứng tấn công nhanh hơn.** `[NGUỒN: VFX Apprentice]`
- **Không dùng đường cong tuyến tính.** Dùng nhịp nén, phi tuyến, "snappy". `[NGUỒN: LoL guide, Gnomon]`
- Kể cả hiệu ứng instant cũng phải có **outro**: giảm cường độ phần tử trước khi biến mất hẳn. `[NGUỒN: VFX Apprentice]`
- **So le (stagger):** lệch thời điểm bắt đầu/kết thúc giữa các phần tử để không đồng loạt bật/tắt. `[NGUỒN: realtimevfx]`
- Thay đổi **tốc độ phát của sprite sheet** để mô phỏng tích năng lượng và giải phóng. `[NGUỒN: B站 cv48094907]`
- Mật độ nét: **nét mảnh, sáng = đòn nhanh, xuyên**; **mảnh vỡ hình học vỡ vụn = sóng xung kích lan ra**; **khiên = khối màu dày, viền ổn định**. `[NGUỒN: B站 cv48141767]`
- Quy trình: có âm thanh/voice tham chiếu trước → ước timing → block-in → chi tiết. `[NGUỒN: VFX Apprentice]`
- Phần thưởng UI (mở rương, lật thẻ, gacha): **dựng anticipation trước khi lộ thưởng; thưởng càng lớn, buildup càng dài.** `[NGUỒN: 80.lv]`

## 2.4 Ngân sách khung hình tham khảo `[HEURISTIC]`
Hit/impact nhanh ở 60fps: anticipation 0–3 frame, action 3–6 frame, follow-through 6–12 frame, tổng ~12 frame ≈ 200 ms; dùng ease-out cho cảm giác giảm tốc. (Nguồn: một skill VFX công khai — coi là điểm khởi đầu, không phải chuẩn.)

---

# 3. MÀU SẮC & GIÁ TRỊ SÁNG TỐI (COLOR & VALUE / 色彩与黑白灰)

## 3.1 Màu `[NGUỒN: 特效美术圣经]`
- **Tối đa ~3 hue mỗi khung hình** (không tính đen/trắng — màu trung tính hợp với mọi hue).
- **Một màu chủ đạo** chiếm diện tích lớn; màu phụ chỉ diện tích nhỏ để cân bằng, giảm mỏi mắt, dẫn mắt.
- **Phối bão hòa + xám:** toàn màu bão hòa → chói, hỗn loạn; toàn xám → đục. Trộn hai loại để chủ thể nổi.
- Mặt hướng sáng bão hòa hơn, vùng tối xám hơn, tối nhất gần đen; **càng gần nguồn sáng càng bão hòa**.
- Tương phản hue (khác họ màu) tạo điểm nhấn; dùng cho phần tử phụ nhỏ.

## 3.2 Bão hòa theo tầng (LoL) `[NGUỒN]`
- Môi trường: bão hòa thấp, dịu → nền dễ đọc.
- UI: bão hòa có kiểm soát.
- **VFX: dải bão hòa rộng nhất, cao nhất** → nổi lên khỏi nền.
- Phối bổ túc (vd. xanh–cam): **một màu phải áp đảo**, màu đối được giảm bão hòa, chỉ dùng cho highlight nhỏ / particle phụ.

## 3.3 Giá trị sáng tối (Value)
- **Tránh đen tuyệt đối (0%) và trắng tuyệt đối (100%)** cho thân hiệu ứng để không lẫn vào nhân vật/map/UI; thân hiệu ứng dùng giá trị trung bình. **Chỉ dùng đỉnh sáng nhất cho flash tức thời tại điểm va chạm/lõi nổ.** `[NGUỒN: LoL guide]`
- Chọn **tông chủ đạo** đen / xám / trắng: trắng chủ đạo → nhẹ, thoáng nhưng dễ cháy sáng; xám chủ đạo → đục; cân bằng → sáng và có nhịp. `[NGUỒN: 特效美术圣经]`
- **Điểm sáng nhất phải nằm ở trung tâm thị giác / chủ thể.** `[NGUỒN: 特效美术圣经]`
- Ánh xạ cảm xúc: đen chủ đạo → tĩnh, buồn, bí ẩn (hiệu ứng hắc ám/tà thuật); sáng chủ đạo → vui, nhẹ, thiêng (hiệu ứng thánh/chuẩn). `[NGUỒN: 特效美术圣经]`
- Vài **chấm trắng nhỏ trong mảng tối lớn** tạo điểm nhấn, làm sống động. `[NGUỒN: 特效美术圣经]`
- Dùng **glow/emission cục bộ** để mở rộng dải sáng tối mà không phải sửa texture; gradient glow có thể báo quỹ đạo, cấp sức mạnh, thời gian còn lại (glow mờ dần khi sắp hết). `[NGUỒN: LoL guide]`
- Hệ 5 tông sáng tối của vật thể: highlight, mid-tone, core shadow, reflected light, cast shadow. `[NGUỒN: 特效美术圣经]`

## 3.4 Mã màu theo hệ (element color coding)
- Quy ước phổ biến: **hồi máu = xanh lá, băng = xanh dương, thuốc súng/lửa = cam-đỏ**. `[NGUỒN: LoL guide]`
- 绝区零: vật lý = va chạm trắng, Ether = ăn mòn tím; dùng màu hệ **nhất quán** suốt game. `[NGUỒN: B站 cv48141767]`
- Tương phản nóng–lạnh (băng lạnh trên nền neon ấm) để tách lớp. `[NGUỒN: B站 cv48141767]`
- Gợi ý bảng hệ cho game pet `[TỔNG HỢP]`: Lửa = cam/đỏ + lõi vàng-trắng; Nước = xanh lam + trắng; Băng = cyan nhạt + trắng; Điện = vàng/tím, nhấp nháy tần số cao; Độc = xanh lá/tím đục; Cỏ = xanh lá tươi; Đất = nâu/vàng đất; Ánh sáng = vàng nhạt/trắng ấm; Bóng tối = tím đậm/đen với chấm sáng.

---

# 4. BỐ CỤC, PHÂN TẦNG, CHIỀU SÂU (COMPOSITION / 构图)

## 4.1 Chính – phụ (Primary / Secondary) `[NGUỒN: LoL guide, B站 cv48094907]`
- **Phần tử chính** mang tín hiệu gameplay (hitbox, mục tiêu): giá trị sáng cao, silhouette rõ, opacity cao, **một điểm nhấn sắc**.
- **Phần tử phụ** (tàn lửa, sương): giá trị thấp hơn, opacity thấp, hình mờ đơn giản, chuyển động nhẹ, **giảm bão hòa hoặc dùng màu phụ** → không tranh chú ý.
- Bất kỳ "nhiễu thị giác" nào gây khó hiểu = thiết kế thất bại.

## 4.2 Hệ chiều sâu bằng độ trong + độ sáng `[NGUỒN: 特效美术圣经]`
- Chủ thể: **đặc nhất (ít trong suốt nhất) và sáng nhất**.
- Đi ra xa chủ thể: **trong suốt tăng, sáng giảm**.
- Phần tử phụ **lớn**: trong hơn, tối hơn.
- Phần tử phụ **nhỏ** (particle): có thể đặc hơn, sáng hơn, thậm chí đặc hoàn toàn.
- Mọi phần tử cùng độ sáng + độ trong → lộn xộn.

## 4.3 Bố cục `[NGUỒN: 特效美术圣经]`
- **Đa dạng trong thống nhất:** khác kích thước, góc xoay, vị trí, độ sâu; nhưng quá đa dạng → rời rạc, quá thống nhất → đơn điệu.
- **Thưa – dày (疏密):** lên kế hoạch chỗ tụ, chỗ thưa trước khi đặt; tránh chen chúc, chồng lặp, đặt ngẫu nhiên.
- **Cân bằng theo trọng lượng thị giác**, không phải đối xứng; chủ thể lệch tâm quá → yếu; dồn một góc → mất cân bằng.
- **Khoảng trống (留白):** xen vùng đơn giản và phức tạp; không lấp kín chi tiết.
- Phân lớp **tiền cảnh – trung cảnh – hậu cảnh**. `[NGUỒN: T/UNP 311—2024]`

## 4.4 Thang độ quan trọng (Scale of importance) `[NGUỒN: LoL guide, B站 cv48094907]`
- Độ lớn/cường độ hiệu ứng **tương ứng sức mạnh chiêu**.
- **Tuyệt chiêu:** dải sáng tối rộng nhất, chuyển động phức tạp nhất, chi tiết nhiều nhất.
- **Đòn thường/chiêu cơ bản:** tiết chế. Chiêu cấp thấp không bao giờ to bằng tuyệt chiêu (mất cảm giác phần thưởng).
- Kiểm soát "thể tích" và "độ sáng" = kiểm soát nhịp game.
- Hiệu ứng skin/nâng cấp: so lượng thông tin thị giác với bản gốc, không được làm mất công bằng (quá kín hoặc quá lộ).

---

# 5. HÌNH KHỐI & CHUYỂN ĐỘNG (SHAPE & MOVEMENT)

- **Vẽ tay hình và texture**, trộn cạnh mềm + cạnh cứng; tránh texture ảnh chụp và noise thủ tục nhiễu. `[NGUỒN: LoL guide]` Ưu tiên sprite có nét cọ vẽ tay hơn hình khối cứng sinh bằng code. `[NGUỒN: B站 cv48094907]`
- **Hạn chế chồng nhiều lớp alpha** → silhouette đục trong trận đông. `[NGUỒN: LoL guide]`
- Tránh hình mâu thuẫn làm ý nghĩa hiệu ứng mơ hồ. `[NGUỒN: LoL guide]`
- **Thể hiện tốc độ:** motion blur theo hướng đi (báo hướng, tốc độ, điểm đến); hoặc **mép trước của đạn sáng nhất, sắc nhất**, đặt trên nền tối, tần số thấp → kéo mắt về phía trước. `[NGUỒN: LoL guide]`
- Lõi rất sáng và sắc; mép (khói, dư ảnh) mờ dần với texture thô vẽ tay. `[NGUỒN: B站 cv48141767]`
- Squash & stretch làm hiệu ứng **cảm giác nhanh hơn**; không có squash → cảm giác frame rate chậm. `[NGUỒN: digital garden notes]`
- Smear frame: kéo giãn/biến dạng phóng đại ở khung nhanh; kết hợp anticipation để đòn "nổ". `[NGUỒN: VFX Apprentice, Gamedeveloper]`
- Phong cách NPR/anime (绝区零): cel-shading tương phản cao; hạt Ether kiểu glitch rung; khói nổ vật lý giữ bóng cel cạnh cứng; lửa thêm chấm halftone kiểu manga; tránh volumetric light quá chân thực. `[NGUỒN: B站 cv48141767]`

---

# 6. CẤU TRÚC HIỆU ỨNG CHO GAMEPLAY (EFFECT ARCHITECTURE)

- Một chiêu thường có **~3 animation** (vào – lặp/duy trì – ra), chuyển bằng **trigger** do lập trình định nghĩa theo logic chiêu. `[NGUỒN: 80.lv]`
- Phần tử xảy ra **thời điểm không đoán trước** (hit reaction, dissipation khi hết giờ) đặt trên **layer/track riêng** → đổi thời lượng chiêu không vỡ hiệu ứng. `[NGUỒN: 80.lv]`
  - Ví dụ Meteor: anticipation tô vùng chỉ báo (chỉnh 0.5 s → 2 s); chỉ rơi khi có trigger HIT; climax + dissipation chung một animation.
  - Ví dụ Dome: vào / năng lượng lặp / sét ngẫu nhiên lặp / hit reaction (layer riêng, khi địch dùng chiêu) / tan (layer riêng, trigger END).
- **Áp dụng cho Spine** `[TỔNG HỢP]`: tách animation `fx_in`, `fx_loop`, `fx_hit`, `fx_out`; phát `fx_loop` trên track 0, `fx_hit` trên track cao hơn (AnimationState cho phép xếp lớp/trộn nhiều animation), dùng **Spine events** để báo frame va chạm cho code (trừ máu, rung màn hình, âm thanh).
- Bản thiết kế (design sheet) nên có các lớp: silhouette chính → ký hiệu hệ (màu/biểu tượng) → mũi tên hướng năng lượng → ghi chú camera/diện tích màn hình → hướng dẫn frame rate → dải tham số shader (vd. noise). `[NGUỒN: B站 cv48141767]`
- Cung cấp **tham số chỉnh được** cho màu, kích thước, tốc độ; thiết kế module để tái tổ hợp; có template cho hiệu ứng ghép. `[NGUỒN: T/UNP 311—2024]`

---

# 7. TRIỂN KHAI VFX TRONG SPINE 2D

## 7.1 Ba cách làm VFX với Spine `[NGUỒN: Esoteric forum]`
1. **Frame-by-frame** vẽ ở phần mềm khác (Photoshop/AE/Procreate) rồi nhập vào Spine để khớp animation nhân vật. Dễ nhưng tốn dung lượng.
2. **Bone làm điểm spawn**: tại runtime load skeleton hiệu ứng / frame-by-frame / particle của engine ở vị trí bone đó.
3. **Rig hiệu ứng bằng công cụ Spine** (mesh, blend mode, constraint, sequence) — nhẹ và mượt nhất.
- Project mẫu **Spineboy** (trong thư mục cài Spine) có hiệu ứng bắn súng dùng blend mode — điểm khởi đầu chuẩn.

## 7.2 Blend mode của slot `[NGUỒN: Spine User Guide – Slots]`
| Mode | Tương đương Photoshop | Dùng cho |
|---|---|---|
| Normal | Normal | Khói đặc, mảnh vỡ, khối chính |
| Additive | Linear Dodge (Add) | Glow, tia, lửa, điện, lóe sáng |
| Multiply | Multiply | Bóng, vùng tối, ăn mòn |
| Screen | Screen | Sáng dịu hơn Additive |
- Chỉ có 4 mode này (Photoshop layer Add/Multiply/Screen tự map khi export PSD; mode khác → Normal).
- Blend mode khác Normal **có thể tăng draw call** ở một số engine. Với **premultiplied alpha (PMA)**, nhiều runtime làm Additive "miễn phí" không flush batch (đặt alpha = 0 trong vertex color). **Multiply/Screen không có mẹo này** → cần material/shader riêng.
- Lỗi thường gặp: PMA bật khi export nhưng runtime không bật (hoặc ngược lại) → vùng đen, viền bẩn. Phải khớp cài đặt PMA hai đầu.
- **Unity Linear color space làm Additive bị "mờ sương", kém sáng.** Cách khắc phục: (a) vẽ ảnh additive sáng hơn; (b) nhân đôi attachment; (c) shader custom nhân màu ×2 hoặc tham số; (d) render UI Spine sang RenderTexture blend trong Gamma. Slot color không thể > 1.0, nên làm ảnh sáng gấp 2–3 rồi dùng slot color hạ xuống. `[NGUỒN: Esoteric forum 29166]`
- spine-unity: blend Additive/Multiply/Screen có hỗ trợ native ở SkeletonDataAsset; Linear space nên dùng straight alpha (bật Bleed, tắt PMA). `[NGUỒN: Esoteric forum 15294]`

## 7.3 Tint Black `[NGUỒN: Spine User Guide – Slots]`
- Tô màu riêng vùng tối và vùng sáng của ảnh. Với ảnh grayscale → ra nhiều biến thể màu từ 1 ảnh (tái sử dụng texture cho nhiều hệ).
- Làm được: silhouette một màu đặc, đảo màu, **nhấp nháy kiểu "ngôi sao bất tử" Mario** (hữu ích cho hit flash, buff, bất tử).
- Kết hợp Additive/Screen/Multiply cho thêm hiệu ứng.
- **Separate color and alpha:** key màu RGB và alpha riêng → fade độc lập với đổi màu.

## 7.4 Sequence attachment (Spine 4.1+) `[NGUỒN: Spine User Guide – Keys]`
- Tick **Sequence** trên region/mesh attachment để chạy frame-by-frame dễ hơn (trước 4.1 phải đặt mọi ảnh vào một slot rồi key ẩn/hiện từng cái).
- Sequence key modes: **Hold** (giữ frame), **Once**, **Loop**, **Pingpong**, **Once reverse**, **Loop reverse**, **Pingpong reverse**. Có **Frame** (chọn frame hiển thị) và **FPS** (tốc độ chuyển frame).
- Sequence trên **mesh** → vừa chạy frame vừa uốn theo xương (vd. lửa bám vào kiếm đang vung).
- Sequence không tự chạy khi gắn vào skin; phải key trong animation (hoặc code runtime đặt `slot.sequenceIndex`). `[NGUỒN: Esoteric forum 17814]`

## 7.5 Mesh, deform, weights `[NGUỒN: Spine User Guide, Armanimation]`
- **Ưu tiên weights (bind mesh vào bone); deform key dùng ít.** Deform key lưu vị trí mọi vertex cho mỗi bone ảnh hưởng → dữ liệu phình.
- Một mesh chỉ key deform được trên **một timeline** → không animate riêng từng phần mesh bằng deform.
- Deform nội suy vertex theo **đường thẳng** → **không xoay mesh bằng deform key** (sẽ co lại ở giữa rồi phình lại).
- Mọi vertex của attachment được key cùng lúc; thêm vertex sau sẽ không deform đến khi cập nhật lại mọi key.

## 7.6 Clipping (mặt nạ) `[NGUỒN: Spine User Guide – Clipping, Esoteric forum]`
- Clipping chạy trên **CPU, rất tốn**, nhất là với mesh nhiều vertex.
- Chi phí ≈ **số vertex của clipping × số vertex bị clip**.
- Tốt nhất: polygon clipping **3 vertex (tam giác)**; kích thước polygon **không ảnh hưởng** hiệu năng. Giữ **lồi (convex)** — polygon lõm bị tách thành nhiều polygon lồi.
- Clip **ít attachment nhất có thể**; tránh mesh hóa attachment bị clip hoặc dùng ít vertex.
- Polygon không được tự cắt nhau. Bật/tắt clipping bằng key attachment của slot; đổi phạm vi bằng key draw order.
- Chỉ đáng lo khi chạy runtime (xuất video/ảnh không ảnh hưởng). Trên mobile: dùng tiết kiệm.
- Ứng dụng VFX: vệt sáng lướt qua kiếm/đá quý (shine sweep), che sequence trong khung.

## 7.7 Physics constraint (Spine 4.2, Pro) `[NGUỒN: Spine User Guide – Physics]`
- Mô phỏng chuyển động phụ (secondary motion) cho bone: tóc, đuôi, xúc tu, dải lụa, ngọn lửa đung đưa.
- Thuộc tính (đều key được): **Inertia** (bao nhiêu chuyển động bone truyền sang offset vật lý — kiểu biên độ trễ), **Strength** (lực lò xo kéo về tư thế gốc), **Damping** (giảm dao động), **Mass** (kháng gia tốc; mass + strength quyết định tần số), **Wind** (lực hằng theo trục X thế giới), **Gravity** (lực hằng theo trục Y), **Mix**.
- FPS mô phỏng 30–60 thường ổn; FPS thấp dễ hỏng mô phỏng.
- Mẹo:
  - Muốn vật **rơi tự do**: bật translate Y, đặt gravity, **strength = 0**; damping ~0 để rơi nhanh dần.
  - Ít vượt quá (overshoot): tăng damping hoặc giảm strength.
  - **Gió hỗn loạn tự nhiên**: key wind/gravity trên track cao hơn; dùng **2 animation có độ dài khác nhau** để tổng không lặp; hoặc code runtime đặt wind ngẫu nhiên.
  - Thứ tự constraint (order) ảnh hưởng kết quả physics chuỗi.
  - Ví dụ cấu hình chuỗi tóc: rotate=1, inertia=0.5, damping=0.85, gravity=100 cho từng đốt. `[NGUỒN: Esoteric forum 25363]`

## 7.8 Path constraint
- Cho bone chạy dọc đường Bezier: vệt sáng neon chạy theo đường, đạn bay cong, vòng xoáy, quỹ đạo hạt bay quanh, **xúc tu** (Path constraint giúp animate xúc tu dễ hơn nhiều). `[NGUỒN: Esoteric forum, Eldritch Zookeeper devlog]`
- Nhảy vị trí tức thời trên path: dùng **frame lẻ** (vd. frame 15 và 15.01). `[NGUỒN: Spine User Guide – Keys]`

## 7.9 Các kỹ thuật VFX trong Spine khác `[NGUỒN: Armanimation, Esoteric forum, Gamedeveloper]`
- **Linked mesh** cho shine / glare / tinh thể (một mesh gốc, nhiều bản dùng chung hình dạng).
- **Ánh sáng giả trên nhân vật:** đặt ảnh nguồn sáng Additive đè lên bộ phận cơ thể rồi di chuyển, bóp méo nguồn sáng đó (phong cách Dragon's Crown).
- **Smear frame bằng bone:** biến dạng bone đầu/vũ khí, lật, thêm follow-through.
- **Glitch trong Spine:** tách kênh RGB bằng mesh chồng lớp + blend; xé ngang bằng deform nhanh + dịch bone; **stepped key** (bỏ nội suy) để có giật cục.
- **Offset key** trong animation lặp để tạo overlapping/follow-through.
- Kéo key giữ phím `alt/option` để dời mà không đẩy các key sau.
- **Clean Up** sau khi key nhiều để giảm dữ liệu và chi phí runtime.
- Danh mục hiệu ứng làm được bằng Spine (theo series Armanimation): kiếm lửa, dash, glow; điện, sét, nứt, mảnh vỡ; phép, dịch chuyển, pha lê; tia năng lượng, tia lửa; khiên lực, hào quang, lóe, nứt đất; hạt, tia sáng, mây, aura; lốc xoáy, gió, lá bay quanh; lõi lửa, tích lửa; đất, lốc bụi, đá xoay quanh; nứt đất – va chạm – nổ – đá vụn; bề mặt mặt trời; tia hướng tâm (radial rays).

## 7.10 Hiệu năng Spine `[NGUỒN: Spine docs, Medium G5, Armanimation]`
- Mỗi attachment kể cả không mesh cũng có 4 vertex → nhiều vertex = tải CPU.
- Thủ phạm phổ biến: **lạm dụng clipping, nhiều deform key, số vertex transform rất cao**. Số bone tác động tuyến tính, hiếm khi là nút thắt.
- Ảnh gốc to không thành vấn đề hiệu năng vì scale khi export; Spine export được nhiều atlas theo tỉ lệ khác nhau cho nhiều độ phân giải màn hình.
- Dùng **Metrics view** trong Spine để đếm vertex, clipping polygon, v.v.
- Dùng **prune** cho weights.
- Cocos Creator: Animation Cache Mode `SHARED_CACHE` (nướng sẵn, nhanh, tiết kiệm bộ nhớ khi nhiều bản giống nhau; không hỗ trợ mix/xếp lớp animation; chỉ event start/end) **hợp cho hiệu ứng, quái, NPC**; `PRIVATE_CACHE` khi cần đổi texture; `REALTIME` khi cần đủ tính năng. `[NGUỒN: Cocos docs]`

---

# 8. PHÍA ENGINE: SHADER & PARTICLE

## 8.1 Hit flash / 受击闪白 `[NGUỒN: Cocos forum 101777]`
Ý tưởng: trộn màu flash với màu gốc theo tham số `rate`, giữ alpha gốc để vùng trong suốt vẫn trong.
```glsl
// fragment
vec4 base = texture(mainTex, uv) * vColor;
vec3 rgb  = mix(uFlashColor.rgb, base.rgb, uRate); // uRate: 0 = toàn màu flash, 1 = bình thường
fragColor = vec4(rgb, base.a);
```
Điều khiển (script): `rate = abs(t - duration/2) * 2 / duration` với `t` đếm ngược → rate 1 → 0 → 1, flash đạt đỉnh ở giữa. Lưu ý Cocos native: đổi tham số material của Spine có thể cần gọi cập nhật material mới có hiệu lực. Cách khác không cần shader: Spine **Tint Black** / slot color.

## 8.2 Hiệu ứng trạng thái qua kênh vertex color `[NGUỒN: Cocos forum 149405]`
Dùng 4 kênh RGBA của vertex color làm 4 công tắc hiệu ứng, chung 1 shader (giảm material/draw call):
```glsl
vec3 gray = vec3(dot(base.rgb, vec3(0.3, 0.6, 0.1)));     // khử màu
base.rgb = mix(vec3(1.0),            base.rgb, v.r);       // R: flash trắng
base.rgb = mix(POISON * gray * 1.5,  base.rgb, v.g);       // G: độc (xanh lá, phơi sáng 1.5x)
base.rgb = mix(FROST  * gray * 3.0,  base.rgb, v.b);       // B: băng (xanh dương, 3.0x)
base.rgb = mix(THUNDER* (1.0-gray)*3.5, base.rgb, v.a);    // A: điện (đảo sáng tối, 3.5x)
// kênh = 1 → bình thường; kênh → 0 → bật hiệu ứng
```
(Lưu ý: trong bài gốc, kênh A còn dùng cho dissolve chết → xung đột với sét; agent nên tách bằng uniform riêng.)

## 8.3 Dissolve / 溶解 / 消融 `[NGUỒN: GameDev.net shaderlab, godotshaders (CC0), CSDN]`
Nguyên lý: so ngưỡng với trường noise; vệt cháy viền = hiệu của hai ngưỡng gần nhau.
```glsl
float n = texture(noiseTex, uv).r;          // Perlin/Simplex noise
// progress 0..1, cho phạm vi vượt nhẹ 0 và 1 để đạt được hai cực
float keep = smoothstep(progress, progress + 0.02, n);              // smoothstep để viền khử răng cưa
float edge = keep - smoothstep(progress + uEdge, progress + uEdge*2.4, n);
vec3 rgb = mix(base.rgb, uEdgeColor.rgb, clamp(edge,0.,1.)) + uEdgeColor.rgb*edge*1.4;
fragColor = vec4(rgb, base.a * keep);       // NHÂN alpha gốc, không thay thế → lỗ trong ảnh vẫn là lỗ
```
- Edge width ~0.04–0.1 thường đẹp; noise tần số cao = vụn nhỏ, tần số thấp = mảng lớn.
- Tránh chấm màu viền sót lại khi progress = 0 hoặc 1 (nhân edge width với `step(0.001,p)*step(p,0.999)`).
- Dùng chung cho: chết, dịch chuyển, xuất hiện, tàng hình, trạng thái hư hại; **xuất hiện pet mới sau tiến hóa** (chạy ngược).
- Cocos ví dụ tween: chờ 1.8 s rồi đưa giá trị từ 255 → 20 trong 1.4 s ghi vào alpha màu Spine, xong trả material mặc định. `[NGUỒN: Cocos forum 149405]`

## 8.4 Master shader đóng gói kênh `[NGUỒN: 80.lv]`
- Texture grayscale để tái sử dụng; RGBA chỉ cho asset độc nhất.
- **R** = màu (qua gradient 1–4 màu chuyển thành LUT), **G** = emission (2 màu trên 1 texture animate riêng), **B** = alpha.
- Fade in/out như Levels của Photoshop; vertex alpha làm mờ mép mesh; texture thứ 2 blend với texture chính; mọi blend mode; flipbook có motion vector; flow map.
- **Thay particle bằng mesh + texture cuộn (scrolling UV)** khi được; scale particle system dễ lỗi → ưu tiên mesh.

## 8.5 Unity Particle System — tham số chính (主模块) `[NGUỒN: Unity docs CN]`
Duration · Looping · Prewarm (chỉ khi Looping) · Start Delay · Start Lifetime · Start Speed · Start Size (3D Start Size tách trục) · Start Rotation · Start Color · Gravity Modifier · **Simulation Space** (Local: hạt đi theo cha — tia lửa giữa hai điện cực; World: để lại vệt — khói, lửa phun) · Scaling Mode · Play on Awake · **Max Particles** · Auto Random Seed · **Stop Action** (Disable/Destroy khi hết hạt).
Module hay dùng: Emission (rate/burst), Shape (Sphere bắn tỏa, Cone chùm loe, Mesh theo pháp tuyến), Color over Lifetime (từ có → không), Size over Lifetime, Texture Sheet Animation (vd. sprite lửa 8×4), Trails, Noise.

## 8.6 Quy trình sprite sheet từ After Effects `[NGUỒN: zcool]`
Ảnh hiệu ứng trên nền đen → blend Screen/Add → Turbulent Displace (key Evolution cho lửa/năng lượng "sống") → Glow 2 lớp (lớn-nhạt + nhỏ-sáng) → CC Particle World cho tia lửa/bụi phép → xuất PNG sequence có alpha → nhập vào engine/Spine sequence.

---

# 9. TỐI ƯU HIỆU NĂNG (MOBILE)

- **Overdraw = số lớp × số pixel bị phủ** (GPU). Ngoài ra: tick time (game thread), draw calls (render thread), tính bounds. `[NGUỒN: Unreal docs]`
- Mobile bị giới hạn fill-rate → thủ phạm chính là **hạt trong suốt to, chồng nhau**. Dùng hạt ít hơn, nhỏ hơn, ít chồng; shader hạt rẻ (additive / alpha đơn giản); **giới hạn diện tích màn hình hiệu ứng phủ**. Thường **giảm nửa số hạt trông vẫn y vậy**. `[NGUỒN: Bugnet]`
- **Cắt texture sát hình**: vùng trong suốt thừa trên quad vẫn bị render. `[NGUỒN: PocketGamer.biz]`
- Tạo thân chính hiệu ứng bằng **một lớp mesh** (vd. cầu/khối phình to với shader đẹp), rồi trang trí bằng ít mảnh nhỏ thay vì chồng nhiều hạt lớn. `[NGUỒN: Polycount]`
- Flipbook: **ít frame nhất đủ cho thời lượng**; motion vector blending cho phép ít frame hơn. Tái dùng texture, nén grayscale, thử độ phân giải thấp hơn. `[NGUỒN: 80.lv]`
- Nén texture **ASTC**: 5×5 hoặc 6×6 là điểm khởi đầu; asset nhỏ thử 8×8, 10×10. `[NGUỒN: Arm/Unity]`
- Dissipation kéo dài vài frame thừa cũng tốn overdraw → cắt sớm. `[NGUỒN: LoL guide]`
- **Ngân sách draw call theo loại chiêu** `[NGUỒN: 80.lv]`: chiêu hiếm → ngân sách lớn; chiêu tồn tại lâu → ngân sách chặt (người chơi thả nhiều cái cùng lúc); chiêu nhiều đơn vị → tính theo số đơn vị tối đa trên màn hình; chiêu tốn tài nguyên (ít dùng) → được phép phức tạp hơn.
- Spine: xem mục 7.10. Stress-test trên máy mục tiêu trong điều kiện xấu nhất. `[NGUỒN: T/UNP 311]`

---

# 10. REVIEW & CHẤM ĐIỂM

## 10.1 Checklist review nhanh (agent chạy trên mọi hiệu ứng) `[TỔNG HỢP từ các nguồn trên]`
- [ ] Đọc được trong 1 cái nhìn? Silhouette chính rõ? Hitbox/vùng ảnh hưởng đúng ranh giới?
- [ ] Có đủ 3 pha; đỉnh rơi vào ~1/4 đầu; tan ngắn, không cắt cụt?
- [ ] Không dùng đường cong tuyến tính; có stagger giữa các phần tử?
- [ ] ≤ 3 hue; có 1 màu chủ đạo; màu hệ đúng quy ước của game?
- [ ] Không có đen/trắng tuyệt đối trên thân; điểm sáng nhất ở chủ thể/điểm va chạm?
- [ ] Phần tử phụ trong hơn/tối hơn/ít bão hòa hơn chủ thể?
- [ ] Quy mô tương ứng độ mạnh chiêu (đòn thường < chiêu < tuyệt chiêu)?
- [ ] Không che silhouette nhân vật/địch, không che UI quan trọng?
- [ ] Heal < 60 BPM; tấn công nhanh hơn?
- [ ] Hiệu năng: overdraw, số hạt, clipping (≤3 vertex, lồi), deform key, draw call trong ngân sách?
- [ ] ≥ 30 fps trên máy mục tiêu; ổn ở ≥ 720p; không răng cưa/nháy?
- [ ] Spine: PMA khớp export–runtime; blend mode render đúng trong engine (kiểm Linear/Gamma)?

## 10.2 Rubric định lượng theo tiêu chuẩn T/UNP 311—2024 《数字动漫游戏特效设计技术规范》 `[NGUỒN]`
- **7 nhóm, 20 chỉ tiêu**, mỗi chỉ tiêu 1–5 điểm, tổng = cộng điểm:
  1. Thông số cơ bản: độ sáng, tương phản, bão hòa, cân bằng màu
  2. Hiệu quả thị giác: thể hiện màu, chi tiết, độ rõ
  3. Nhịp: động thái, biến thiên tốc độ
  4. Sáng tạo: tính độc đáo, đổi mới
  5. Kỹ thuật: tương thích, hỗ trợ engine, hiệu năng
  6. Trải nghiệm: thích mắt, logic nhất quán, phản hồi
  7. Nhất quán: phong cách, yêu cầu, phối hợp phần tử
- Ngưỡng định lượng:
  | Chỉ tiêu | 1 | 2 | 3 | 4 | 5 |
  |---|---|---|---|---|---|
  | Tỉ lệ tương phản | 100:1 | 200:1 | 300:1 | 500:1 | 600:1 |
  | Bão hòa | 20–80% | 30–80% | 40–80% | 50–80% | 60–70% |
  | Frame rate | 20 fps | 25 | 30 | 35 | 40 |
  | Thời gian phản hồi | 0.8 s | 0.7 s | 0.6 s | 0.5 s | 0.4 s |
- **Tổng < 85 → phải sửa** đến khi mọi chỉ tiêu ≥ 4 hoặc tổng ≥ 85.
- Yêu cầu hiệu quả khác: ánh sáng khớp hướng sáng cảnh; màu chuyển hợp lý qua các trạng thái (kích hoạt → duy trì → kết thúc); tương phản/bão hòa vừa phải; ≥ 30 fps; ổn ở ≥ 720p; chuyển động theo logic vật lý/game, không giật/gãy/khựng; xuất hiện – duy trì – biến mất theo nhịp game, phản hồi chiêu kịp thời, tan không cắt đột ngột.

---

# 11. CÔNG THỨC MẪU CHO GAME PET (2D, SPINE)

Tất cả mục này là `[TỔNG HỢP]` từ nguyên tắc ở trên; chỉnh theo phong cách game.

## 11.1 Đòn đánh thường / hit spark (Impulse – Instant)
- 0–2 frame: lóe lõi sáng (Additive, gần trắng, nhỏ) tại điểm va chạm.
- 2–6 frame: 3–6 tia nhọn tỏa (mesh dài, scale X nhanh rồi mảnh dần) + vòng sóng mỏng.
- 6–12 frame: tia mờ + vài hạt nhỏ đặc bay ra; fade alpha.
- Đồng thời: hit flash trên mục tiêu (mục 8.1) 2–4 frame; Spine event "hit".
- Quy mô nhỏ, ≤ 2 hue (màu hệ + trắng).

## 11.2 Chém / slash
- Mesh vệt chém cong theo quỹ đạo vũ khí; mép trước sáng/sắc nhất, đuôi mờ thô (vẽ tay); sequence 3–5 frame hoặc mesh + alpha gradient.
- Smear vũ khí bằng biến dạng bone ở frame nhanh nhất; thêm anticipation (lùi vũ khí) trước khi chém.

## 11.3 Chiêu hệ / chiêu lớn (Impulse – Crescendo)
- Anticipation: hạt hút vào tâm + vòng tròn tụ năng lượng sáng dần (thời lượng theo design).
- Climax (~1/4 đầu): flash lõi, sóng xung kích, mảnh vỡ (đất), tia (điện, stepped key nhấp nháy tần số cao), lưỡi lửa (sequence lửa trên mesh).
- Dissipation: khói/tàn mờ, alpha thấp, ngắn.
- Tuyệt chiêu: dải sáng tối rộng nhất, nhiều lớp hơn, có thể rung màn hình — nhưng vẫn giới hạn diện tích.

## 11.4 Hồi máu / buff
- Rhythm – Flowing, **< 60 BPM**; xanh lá (heal) hoặc vàng ấm (buff); hạt nhẹ bay lên, vòng sáng mềm dưới chân; Screen thay vì Additive nếu muốn dịu.

## 11.5 Khiên
- Khối màu dày, viền ổn định, lóe nhẹ khi bị đánh (hit reaction trên track riêng); tan bằng dissolve hoặc vỡ mảnh.

## 11.6 Trạng thái (độc / băng / điện / bỏng)
- Dùng shader kênh vertex color (8.2) hoặc Tint Black để đổi màu thân pet; thêm hạt lặp nhỏ (bong bóng độc, tinh thể băng, tia điện) trên bone; vòng lặp rhythm.

## 11.7 Tiến hóa pet (Evolution) — kết hợp UI reward buildup
1. **Buildup (dài, vì là phần thưởng lớn):** pet cũ phát sáng dần (Tint Black/slot color → trắng), hạt hút vào, vòng ký hiệu xoay chậm rồi nhanh dần (tăng tốc = tăng căng thẳng).
2. **Đỉnh:** flash trắng che hoàn toàn silhouette (điểm sáng nhất toàn màn), sóng tỏa, tia hướng tâm (radial rays, Additive).
3. **Lộ diện:** pet mới xuất hiện bằng dissolve ngược hoặc scale từ 0.9 → 1.05 → 1.0 (overshoot nhẹ), aura màu hệ của dạng mới.
4. **Tan:** hạt lấp lánh rơi chậm, alpha giảm; quay về idle của pet mới.
- Giữ ≤ 3 hue: màu hệ dạng mới + trắng + 1 màu phụ.

## 11.8 Chết / biến mất
- Hit flash cuối → dissolve với viền màu hệ (8.3) → vài hạt bay lên.

---

# 12. THUẬT NGỮ (中文 – English – Tiếng Việt)

| 中文 | English | Tiếng Việt |
|---|---|---|
| 特效 / 游戏特效 | VFX / game VFX | hiệu ứng / hiệu ứng game |
| 特效师 | VFX artist | hoạ sĩ hiệu ứng |
| 蓄力 / 起手 | anticipation / wind-up | lấy đà, tụ lực |
| 爆发 / 打击 | climax / impact | đỉnh, va chạm |
| 消散 | dissipation | tan biến |
| 打击感 | hit feel / impact | cảm giác đánh trúng |
| 节奏 | timing / rhythm | nhịp |
| 剪影 | silhouette | hình bóng |
| 层次 / 分层 | layering | phân tầng |
| 主次 | primary/secondary | chính – phụ |
| 疏密 | sparse & dense | thưa – dày |
| 留白 | negative space | khoảng trống |
| 黑白灰 | value (black/white/gray) | sáng tối |
| 饱和度 / 纯度 | saturation | độ bão hòa |
| 冷暖对比 | warm-cool contrast | tương phản nóng lạnh |
| 序列帧 | sprite sequence / flipbook | chuỗi khung hình |
| 粒子 / 粒子系统 | particle / particle system | hạt / hệ thống hạt |
| 拖尾 | trail | vệt đuôi |
| 刀光 | slash trail | vệt chém |
| 受击闪白 | hit flash (white) | nháy trắng khi trúng đòn |
| 溶解 / 消融 | dissolve | tan rã |
| 描边 | outline | viền |
| 扭曲 | distortion | méo |
| 叠加 / 加法混合 (add) | additive blending | cộng sáng |
| 正片叠底 | multiply | nhân |
| 滤色 | screen | screen |
| 预乘 Alpha | premultiplied alpha | alpha nhân trước |
| 遮罩 / 裁剪 | mask / clipping | mặt nạ |
| 骨骼 | bone | xương |
| 网格 | mesh | lưới |
| 蒙皮 / 权重 | skinning / weights | gán trọng số |
| 约束 | constraint | ràng buộc |
| 路径约束 | path constraint | ràng buộc đường dẫn |
| 物理约束 | physics constraint | ràng buộc vật lý |
| 过度绘制 | overdraw | vẽ đè |
| 合批 / DrawCall | batching / draw call | gộp lệnh vẽ |
| 噪声图 | noise texture | ảnh nhiễu |
| 设计稿 | design sheet | bản thiết kế |

---

# 13. NGUỒN HỌC CHO NGƯỜI (agent có thể giới thiệu)

- 《特效美术圣经》 (京沅) PDF miễn phí — nền mỹ thuật VFX. 
- T/UNP 311—2024 《数字动漫游戏特效设计技术规范》 PDF — tiêu chuẩn + rubric.
- Diễn đàn/khóa học TQ: CGWell (bbs.cgwell.com), CGJoy (cgjoy.com), Magesbox 魔法盒 (magesbox.com), Element3ds, biubiu游戏美术论坛, Huaban board 特效; nhiều trang yêu cầu QQ/WeChat/số TQ (theo thảo luận cũ trên realtimevfx, CGJoy từng nhận VISA, CGWell thì không — cần kiểm tra lại).
- Reel tham khảo timing: Cheng Gang (程刚) VFX reel (YouTube).
- Spine: User Guide (esotericsoftware.com), forum Tutorials, project mẫu Spineboy; kênh YouTube Armanimation (Armanimation_spine) với series VFX.
- Sách: Elemental Magic I & II (Joseph Gilland); Real Time Visual Effects for the Technical Artist (Chris Roda, CRC Press 2022).
- Unity: "The definitive guide to creating advanced visual effects in Unity" (miễn phí, có bản dịch trên learn.u3d.cn).
- SurfCG (surfcg.com): ~20.000 tham khảo hiệu ứng game.

---

# 14. NGUỒN ĐÃ DÙNG

- 特效美术圣经 – 京沅 (PDF): https://realtimevfx.com/uploads/short-url/zgKTB2RQJTPjJeGksSU6IxLzXKr.pdf
- T/UNP 311—2024 数字动漫游戏特效设计技术规范: https://www.ttbz.org.cn/Home/PdfFileStreamGet/c3QsMTIzMjg3
- 《英雄联盟》风格特效制作核心解析 (B站): https://www.bilibili.com/read/cv48094907
- 《绝区零》特效设计稿 (B站): https://www.bilibili.com/read/cv48141767
- 10 Design Tips from the League of Legends VFX Style Guide: https://www.vfxapprentice.com/blog/10-league-of-legends-vfx-design-tips
- The Soul of Effects: What is Timing in VFX?: https://www.vfxapprentice.com/blog/the-soul-of-effects-what-is-timing-in-vfx
- VFX Staples: Shape, Color and Motion (80.lv): https://80.lv/articles/vfx-staples-shape-color-and-motion/
- Chinese VFX Awesomeness (realtimevfx thread): https://realtimevfx.com/t/chinese-vfx-awesomeness/690
- Spine User Guide – Slots: https://esotericsoftware.com/spine-slots
- Spine User Guide – Keys: https://esotericsoftware.com/spine-keys
- Spine User Guide – Clipping: https://esotericsoftware.com/spine-clipping
- Spine User Guide – Physics constraints: https://esotericsoftware.com/spine-physics-constraints
- Spine forum – Linear color space Additive (中文): https://esotericsoftware.com/forum/d/29166
- Spine forum – Physics general questions: https://esotericsoftware.com/forum/d/25363
- Spine forum – VFX tutorial for beginners: https://esotericsoftware.com/forum/d/29573
- Armanimation – Spine optimization (transcript): https://tubescript.cc/transcript/H2LktmTdxGI
- 13 VFX techniques for Spine Animators (Spine forum): https://esotericsoftware.com/forum/d/26463
- Cocos forum – 受击闪白: https://forum.cocos.org/t/topic/101777
- Cocos forum – Shader 割草游戏特效: https://forum.cocos.org/t/topic/149405
- Cocos Creator Spine component: https://docs.cocos.com/creator/3.0/manual/en/components/spine.html
- GameDev.net – Sprite Dissolve Effect: https://gamedev.net/shaderlab/14-sprite-dissolve-effect/
- Godot Shaders – 2D dissolve with burn edge (CC0): https://godotshaders.com/shader/2d-dissolve-with-burn-edge/
- Unity Particle System Main module (CN): https://docs.unity3d.com/cn/560/Manual/PartSysMainModule.html
- Unreal VFX Optimization (CN): https://docs.unrealengine.com/udk/Three/VFXOptimizationCH.html
- Bugnet – particle overdraw on mobile: https://bugnet.io/blog/how-to-fix-particle-overdraw-killing-mobile-performance
- PocketGamer.biz – VFX optimisation in midcore games: https://www.pocketgamer.biz/vfx-optimisation-in-midcore-games-commonly-overlooked-techniques-and-advanced-methods/
- Polycount – overdraw discussion: https://polycount.com/discussion/comment/1940608
- zcool – Firefly + AE 特效流程: https://www.zcool.com.cn/article/ZMTY3MzQwNA==.html
- Heuristic frame budget (vfx-realtime skill): https://openskillindex.com/skills/vibeforge1111-vibeship-spawner-skills-vfx-realtime
