## Why

GDD gốc, mục "Máy pachinko drop ball": máy bi kiểm soát nhịp tiến bộ và làm vòng lõi dày hơn. Các ý chính:
- **Thưởng:** thả bi ra hạt kinh nghiệm (lên cấp người chơi, cũng là cấp tướng), ra thẻ (tiến hóa tướng), có ô rương (thẻ tướng hoặc thêm bi).
- **Giới hạn:** mỗi lần thả tối đa 20 hoặc 30 bi.
- **Nút X nhân thưởng:** EXP 5/10/15 thành 10/20/30 ở ×2. Thẻ trong rương ở ×N thành N thẻ cùng độ hiếm nhưng có thể khác nhau.
- **Huyền thoại:** đa số rương ra bi hoặc EXP, hiếm khi ra thẻ (thường Thường, Khá, Hiếm), Sử thi và Huyền thoại cực thấp. Thẻ Huyền thoại có thể trúng lần đầu khi tiêu bi tới một mốc, về sau gần như không ra.

Bản web đã làm máy có vật lý và đo tỉ lệ bằng mô phỏng 6.000 bi. Chủ dự án chốt nút X là **mức cược** (×N tốn N bi mỗi lần thả, thưởng ×N).

## What Changes

- Chép vật lý máy bi `Web/src/core/pachinko.ts` sang C#:
  - 10 hàng đinh, 3 nấm bật, u lồi trên tường, vai nghiêng;
  - 3 cốc hứng (vàng giữa, bạc hai bên), 9 ô đáy có độ rộng khác nhau;
  - bi va nhau; bước thời gian cố định 1/120 giây chia 4 bước con.
- Mặt máy theo bản web: hai ô mép ra rương gỗ, rồi EXP 15, EXP 5, +1 bi, EXP 10 ở giữa (đối xứng).
- Đo được khi máng thả quét đều:
  - rương vàng ~3%, bạc ~6%, gỗ ~8,5%;
  - mỗi bi ở ×1 ra ~9,6 EXP và hoàn ~0,33 bi.
- **Máng thả** đung đưa. Chạm thả 1 bi, giữ thả liên tục (mỗi 0,16 giây), nút "Thả liền 20". Mỗi đợt tối đa 20 bi; **từ cấp 15 tăng lên 30** (theo GDD "20 hoặc 30 bóng").
- **Nút cược** ×1, ×2 (cấp 3), ×3 (cấp 5), ×5 (cấp 8), ×10 (cấp 12): tốn N bi mỗi lần thả, mọi thưởng ×N.
- **Rương** gỗ, bạc, vàng xếp hàng chờ, mở sau khi đợt thả xong:
  - ra bi, EXP, bản sao thẻ (theo độ hiếm), đôi khi mảnh tướng;
  - ×N cho N lần số lượng, mỗi thẻ rút riêng.
- **Mốc Huyền thoại:** thả đủ 300 bi (tính theo bi đã tiêu) thì chắc chắn nhận tướng Huyền thoại đầu tiên (Đại Sư Cà Sa). Sau đó thẻ Huyền thoại trong rương vàng chỉ còn 0,01% mỗi thẻ.
- **Bảng tỉ lệ in trên máy** (nút "Tỉ lệ").
- **Phản hồi:** đinh loé khi chạm, ô sáng khi bi rơi vào, chữ nổi "+10 XP", rương bay vào khay "Rương chờ", tiếng tích và tiếng keng. Lên cấp báo sau khi mở hết rương.

## Capabilities

### New Capabilities

- `pachinko-machine`: mặt máy và vật lý, máng thả và giới hạn mỗi đợt, nút cược ×N, thưởng ô, rương và bảng rương, mốc Huyền thoại, bảng tỉ lệ, phản hồi hình và tiếng, tái lập theo hạt giống.

### Modified Capabilities

<!-- Chưa có spec nào trong openspec/specs. -->

## Impact

- **Code:** `Core/Pachinko` (vật lý, thưởng; C# thuần); `Game/Machine` (scene, vẽ, nhập liệu).
- **Scene:** `Machine.unity`.
- **Dữ liệu:**
  - `BalanceConfig` thêm mặt máy, độ rộng ô, bảng rương, mốc cược, mốc Huyền thoại, số bi tối đa theo cấp;
  - thêm `maxPerDrop` theo cấp ở bản web cho khớp.
- **Ảnh:** gói `ArtGen/Pachinko` (thân máy, đinh, nấm, cốc, ô, máng mây, bi, rương 3 loại đóng/mở). Thiếu thì vẽ bằng code như bản web.
- **Phụ thuộc:** `setup-unity-foundation`, `add-hero-roster` (EXP, cấp, bản sao thẻ, mảnh).
