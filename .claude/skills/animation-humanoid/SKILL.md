---
name: animation-humanoid
description: >
  Luật animation cho nhân vật DẠNG NGƯỜI của PokiClash (dealer Lão Mực đảo Casino, NPC, người dẫn truyện, tướng dạng người như
  dòng Tiểu Y, Mi Nhi): hướng bàn tay đúng giải phẫu khi đặt, đẩy, vơ, nện trên mặt bàn; tay ống cao su kiểu hoạt hình 1930–40
  (ống chắc, không thành sợi chỉ); biên độ vừa phải; phụ kiện đầu bám theo đầu. Dùng TRƯỚC khi dựng, sửa hay chấm animation có
  bàn tay, cánh tay người (rig AtomSpine/.atomik), cùng với `animation-petclash` và `atomspine`.
---

# animation-humanoid: tay và thân nhân vật dạng người

Rút từ góp ý của người dùng khi làm Lão Mực (GD_Claude/31, 2026-11-26). Mỗi luật là một lần bản trước bị trả.
Góc máy mặc định: camera ở ghế người chơi, nhân vật quay mặt về camera, mặt bàn nằm giữa hai bên.

## 1. Hướng bàn tay (bắt buộc)

Quy ước: "trong" = phía giữa thân nhân vật / phía tay kia; "gần người" = phía bụng nhân vật (xa camera); "phía người chơi" = phía
camera. Ngón cái là ngón ngắn nhất.

| Động tác | Đúng | Sai đã gặp |
|---|---|---|
| Tay úp đặt trên bàn (idle, chờ, nghe) | lòng úp xuống, ngón chĩa vào giữa; **ngón cái ở phía gần người, ngón út ở phía người chơi** | dùng nhầm bản lật gương nên ngón cái rơi xuống phía người chơi |
| Đẩy chip / gạt vật trên bàn | bàn tay **dựng đứng**, ngón cái ở trên, **lòng tay hướng vào trong**, gạt bằng cạnh hoặc lòng bàn tay | một ngón chỉ thẳng xuống bàn để đẩy |
| Vơ chip / quây vật về (hai tay) | hai bàn tay dựng đứng, ngón cái ở trên, lòng tay quay vào nhau, đầu ngón chạm nhau thành **mái nhà khép kín** (chữ Λ) úp quanh vật rồi kéo về | hai bàn tay úp lộn xộn trên chồng chip, nhìn không hiểu đang làm gì |
| Nện bàn khi cáu | **cổ tay xoay 90°**: nắm tay dựng nghiêng, ngón cái ở trên, lòng (mặt ngón cuộn) quay vào trong, **cạnh ngón út nện xuống**; từ camera thấy mu và cạnh nắm tay | đấm thẳng mặt đốt ngón / đầu ngón xuống bàn |

Cách soi: mỗi khung tay chạm bàn, hỏi "ngón cái ở đâu, lòng tay quay về đâu", với CẢ hai tay. Tay trái và tay phải là hai bản gương
của nhau; đổi nhầm bản là sai hướng ngay.

Cách Lão Mực làm đúng (bản 4, 2026-11-26):
- **Tay úp:** hình gen gốc vẽ ngón cái ở mép dưới. Lật dọc ngay lúc cắt mảnh (không gen lại) là ngón cái về phía gần người.
  Soi hình gốc của mọi bàn tay úp trước khi rig.
- **Đẩy chip:** bàn tay dựng đứng nhìn từ phía mu, mép ngón út tì ngay sau chồng chip (phía nhân vật) rồi gạt cả chồng tới ô cược.
  Camera thấy mu và cạnh bàn tay.
- **Vơ chip:** hai bàn tay dựng đứng chĩa chéo xuống giữa, đầu ngón chụm nhau. Trên màn hình thành chữ **V**: cổ tay ở trên (phía
  nhân vật), đầu ngón ở dưới (phía người chơi), chip nằm trong lòng. Nhìn từ phía nhân vật mới là mái nhà Λ. Mái phải khép ở phía
  người chơi thì kéo về mới mang chip theo. (Người dùng chưa xác nhận V hay Λ trên màn; hỏi lại trước khi dùng cho nhân vật khác.)
- **Nện bàn:** nắm tay nghiêng nằm ngang chĩa vào giữa, ngón cái trên, camera thấy mu nắm tay, cạnh ngón út chạm bàn đúng khung nện.

Bộ hình bàn tay cần có từ đầu (gen không viền, cùng nét): úp xoè, xoè giơ, chỉ, nắm nhìn trước, **mở dựng đứng nhìn nghiêng từ
phía mu (ngón cái ở mép trên, mép ngón út phẳng)**, **nắm dựng nghiêng nhìn từ phía mu (ngón cái trên)**, cầm vật. Thiếu dáng
nghiêng thì đừng xoay hình nhìn trước 90° thay vào: đọc ra sai hướng lòng tay (bản 3 làm vậy, bị trả). Hai dáng nghiêng gen chung
một tờ, lấy bàn tay sẵn có làm ảnh mẫu, một lượt GPT 2.6 1k (~80 credit) ra đúng ngay; tay kia lật gương.
Mẫu: `refs/humanoid/lao_muc` trong AtomSpine (rig 65 xương, 12 clip, bộ tay 12 hình mỗi bên).

## 2. Tay ống cao su: ống chắc, không phải sợi chỉ

- Tay là một **ống** dày đều, cong thành một cung mượt (chữ C; S rất nhẹ chỉ khi đang vung). Không võng, không lượn như dây.
- **Đoạn gần vai bám chắc theo vai**: 2–3 đốt đầu không trễ, không lò xo. Trễ và lò xo chỉ ở cẳng tay, cổ tay, biên độ nhỏ.
- Kéo dài thì ống chỉ thon nhẹ (không dưới ~95% bề dày gốc). Thon nhiều = "sợi chỉ" (bản 2 thon tới 56% bị trả).
- Tay gần (đích ở sát vai) thì ống dồn ngắn và phình ra, không thòng xuống.
- Giơ tay lên (nói, vẫy, chỉ) phải có **khuỷu ngầm**: bắp tay chếch xuống ngoài, cẳng tay dựng lên; khua bằng cẳng tay và cổ tay,
  bắp tay đứng yên.
- Gốc tay giấu trong thân (dưới nơ, cổ áo), không để mẩu tay thừa ở vai lòi ra khi vươn.

## 3. Biên độ

- Học nhịp của hoạt hình cũ (dậm, nén, bật, lơi) nhưng **động tác vừa phải**: không tự ý cho tay vươn ra ngoài camera hay quăng vòng
  thòng lọng như mẫu Cuphead, trừ khi người dùng xin. Tay luôn trong khung nhìn (chừa cả khung điện thoại hẹp).
- Vòng tay lớn thành hai vòng tròn thòng xuống mặt bàn nhìn lố: rút ngắn cho tay cong vừa đủ tới đích.

## 4. Phụ kiện trên đầu

- Mũ, lưỡi trai, băng đầu xoay quanh chốt bám đầu; dáng "xị" thì dồn vào vành cụp xuống, góc xoay nhỏ (≤ ~7°), lò xo giới hạn
  vài độ. Không để đầu đai nhấc khỏi đầu khi nghiêng.

## 5. Bảng kiểm trước khi báo

- [ ] Mọi khung tay chạm bàn: đúng bảng mục 1, cả hai tay.
- [ ] Đoạn tay gần vai ở idle và dáng giơ cao: ống chắc, không lượn.
- [ ] Dáng vươn xa nhất của từng clip: còn trong khung, ống không thon thành sợi, vai không lòi mẩu thừa.
- [ ] Dáng nghiêng đầu nhiều nhất: mũ bám đầu.
- [ ] Soi khung lớn (không chỉ tờ khung nhỏ) ở các dáng trên.
