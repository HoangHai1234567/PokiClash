# Gói gửi GPT: dòng tm02, Thạch Giải (dạng 1)

Lô 10 tướng mới đảo Thủy (đặc tả `ArtGen/Spine/quai/DAC_TA_LO_THUY.md`), dòng tm02 thay suất ải 5 (Tiểu Y). Cua ẩn sĩ cõng tảng đá làm nhà. Pha 1 chỉ có concept trọn con; tờ mảnh dựng sau khi người dùng duyệt.

**Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\tm02_1\luot_1_concept.txt`. GPT tự mở ảnh mẫu theo đường dẫn ghi trong file và lưu ảnh vào `D:\PokiClash\ArtGen\Spine\inbox\tm02_1\tai_ve\L1_concept.png` (trùng tên thì `L1_concept_2.png`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/tm02_1/luot_1_concept.txt` (chạy nền, khoá Codex chung, khoảng 2 phút một ảnh).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ (1024 × 1536, bản đồ thế giới vẽ tay, nền xanh biển): viền mực nâu hơi rung, tô chì màu và sáp màu. Chỉ lấy nét |
| 2 | `D:\PokiClash\ArtGen\Spine\inbox\vay_lam_1\tai_ve\L1_lien.png` | Cá voi sát thủ Vây Lam dạng 1 đã duyệt (1536 × 1024, nền trắng): con cá xanh lam bụng trắng, mắt vàng cau có, nhìn sang phải. Lấy nét bút, độ dày viền, vân sáp, vẻ quả quyết; không chép loài, màu, dáng |
| 3 | `D:\PokiClash\ArtGen\Spine\inbox\ma_ket_1\tai_ve\L1_lien.png` | Dê cá Ma Kết dạng 1 đã duyệt (1536 × 1024, nền trắng): dê con xanh lục đuôi cá, sừng xám, lông kem. Lấy tỉ lệ chibi dạng 1, vân sáp, mức chi tiết; không chép loài, màu, dáng |

Ảnh ra: 1536 × 1024, nền trắng tinh, con vật khoảng 1000 × 760 px ở giữa, viền mực khoảng 7 px.

## Kiểm

- Cua ẩn sĩ **nhìn sang phải**, góc 3/4; tảng đá bazan xám than (không phải đá be) bên trái, có hà kem, mảng san hô hồng, một túm rong xanh; thân cua ló ra từ cửa đá.
- Vỏ cua xanh lam ngả xám (slate), mặt dưới lam bọt nhạt; mắt vàng hổ phách trên **hai cuống ngắn** có nắp mí giáp; hai râu hồng san hô dài vắt ra sau.
- Một **càng búa to** phía gần (thấp, trước ngực, không che mặt, không che chân), một **càng nhỏ** giơ lên cạnh cuống mắt; bốn chân bò tách nhau, không chéo; đáy tảng đá không chạm đất.
- Miệng hé thấy lòng miệng hồng sẫm; mặt quả quyết, không cười tươi.
- Tô phẳng, không bóng, không điểm sáng (trừ chấm mắt), không nước, không đất, nền trắng tinh.
- Khác hẳn Kuba (cua đỏ cam, pha lê xanh trên lưng, hai mắt tròn trắng, hai càng tròn bằng nhau) và khác con tham khảo (đá be, một mắt đỏ trong hốc tối, hai càng lưỡi hái băng nhìn thẳng).

## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `gen.py ... --note "..."`)

| Sai | Gửi thêm |
|---|---|
| Có bóng, mảng sáng tối | `Flat colour only: remove every shadow, highlight and gradient; keep the crayon hatching as texture.` |
| Quay sang trái / nhìn thẳng | `The creature must face the viewer's RIGHT in a 3/4 side view: boulder on the left, face and claws on the right.` |
| Chân chéo, càng che mặt | `Spread the legs so none crosses another; the big claw stays low in front of the chest, not over the face or legs.` |
| Đá màu be, giống đá cát | `The boulder is dark charcoal blue-grey basalt (#4B5160), not beige or sand coloured.` |
| Dễ thương quá, cười | `Make the face stern and determined (frowning eyelid caps, small open mouth), not smiling, not a mascot.` |

## Lượt 2 (pha 2, cách lai): tờ mảnh M01

**Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\tm02_1\luot_2_manh.txt`. GPT lưu vào `D:\PokiClash\ArtGen\Spine\inbox\tm02_1\tai_ve\M01.png` (trùng tên thì `M01_2.png`…).

Thân, nhà đá, chân, càng, râu, rong cắt thẳng từ concept đã duyệt (`ArtGen/Spine/tm02_lai.py`); tờ này chỉ thêm phần concept không có. Đang dùng: lòng miệng (ô trên phải). Mắt nhắm làm từ chính mắt concept (phủ kín đúng tròng) nên hai mắt nhắm GPT vẽ chỉ để dự phòng; hai ngón càng cũng dự phòng (ngón cắt từ concept, gốc vẽ bù).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ (1024 × 1536, bản đồ thế giới vẽ tay, nền xanh biển): viền mực nâu hơi rung, tô chì màu và sáp màu. Chỉ lấy nét |
| 2 | `D:\PokiClash\ArtGen\Spine\inbox\tm02_1\tai_ve\L1_duyet.png` | Concept đã duyệt của dạng này (1536 × 1024, nền trắng) |

Ảnh ra: 1536 × 1024 nền trắng, lưới 3 × 2 ô 512: mắt trái nhắm, mắt phải nhắm, lòng miệng (hồng sẫm có lưỡi), ngón trên càng búa, ngón càng còn lại, ô cuối trống.

Kiểm: mảnh rời nhau, không bóng, đúng màu concept; lòng miệng là một mảng tròn không răng.
