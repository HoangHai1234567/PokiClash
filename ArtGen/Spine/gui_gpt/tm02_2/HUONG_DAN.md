# Gói gửi GPT: dòng tm02, Thạch Thành Giải (dạng 2, dạng cuối)

Lô 10 tướng mới đảo Thủy (đặc tả `ArtGen/Spine/quai/DAC_TA_LO_THUY.md`), dòng tm02 thay suất ải 5 (Tiểu Y). Cua ẩn sĩ cõng tảng đá làm nhà. Pha 1 chỉ có concept trọn con; tờ mảnh dựng sau khi người dùng duyệt.

**Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\tm02_2\luot_1_concept.txt`. GPT tự mở ảnh mẫu theo đường dẫn ghi trong file và lưu ảnh vào `D:\PokiClash\ArtGen\Spine\inbox\tm02_2\tai_ve\L1_concept.png` (trùng tên thì `L1_concept_2.png`, `_3`…).

Claude tự gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/tm02_2/luot_1_concept.txt` (chạy nền, khoá Codex chung, khoảng 2 phút một ảnh).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ (1024 × 1536, bản đồ thế giới vẽ tay, nền xanh biển): viền mực nâu hơi rung, tô chì màu và sáp màu. Chỉ lấy nét |
| 2 | `D:\PokiClash\ArtGen\Spine\inbox\vay_lam_3\tai_ve\L1_lien.png` | Vây Lam dạng 3 đã duyệt (1536 × 1024, nền trắng): cá mập xanh lam đậm dạng cuối, mắt xếch, nhe nanh, thế chồm, nhìn sang phải. Lấy nét và thần thái; không chép loài, màu, dáng |
| 3 | `D:\PokiClash\ArtGen\Spine\inbox\tm02_1\tai_ve\L1_concept_2.png` | Concept dạng 1 đã chọn của dòng (1536 × 1024, nền trắng): cua ẩn sĩ vỏ xanh slate cõng tảng đá bazan có hà, san hô, rong |

Ảnh ra: 1536 × 1024, nền trắng tinh, con vật khoảng 1100 × 880 px ở giữa, viền mực khoảng 7 px.

## Kiểm

- Nhận ra cùng dòng với dạng 1 (cua ẩn sĩ cõng nhà đá, mắt hổ phách trên cuống, râu hồng, một càng búa + một càng nhỏ, hà kem) nhưng **khác hẳn**: tháp đá bazan đen cao lởm chởm (cao hơn rộng), vương miện san hô đỏ, rong nâu xanh rủ.
- Tỉ lệ trưởng thành (đầu nhỏ, mắt hẹp xếch đồng tử dọc), giáp chàm đậm viền gai trắng ngà, khớp lam lục.
- Càng búa **bọc găng đá bazan** to bằng cả thân trước, giơ cao bên phải mặt (không che mặt); càng lưỡi cưa phía xa thấy rõ.
- Nhìn sang phải, bốn chân giáp tách nhau, không chéo; đáy tháp không chạm đất; miệng há có hai nanh kem.
- Tô phẳng, không bóng, không điểm sáng (trừ chấm mắt), nền trắng tinh.

## GPT vẽ sai thì gửi thêm (cùng chat, hoặc `gen.py ... --note "..."`)

| Sai | Gửi thêm |
|---|---|
| Vẫn chibi | `Not chibi at all: adult proportions, head plate about one fifth of the height, narrow fierce eyes, heavy armour.` |
| Giống dạng 1 quá | `The final form must look clearly different from image 3: tall jagged black basalt tower with a coral crown, deep indigo armour with bone-white spikes, a stone-gauntlet hammer claw raised high.` |
| Có bóng, mảng sáng tối | `Flat colour only: remove every shadow, highlight and gradient; keep the crayon hatching as texture.` |
| Càng búa che mặt | `Raise the hammer claw to the right of the face; both eyes and the open mouth must stay fully visible.` |

## Lượt 2 (pha 2, cách lai): tờ mảnh M01

**Chỉ gửi GPT đường dẫn:** `D:\PokiClash\ArtGen\Spine\gui_gpt\tm02_2\luot_2_manh.txt`. GPT lưu vào `D:\PokiClash\ArtGen\Spine\inbox\tm02_2\tai_ve\M01.png` (trùng tên thì `M01_2.png`…).

Thân, nhà đá, chân, càng, râu, rong cắt thẳng từ concept đã duyệt (`ArtGen/Spine/tm02_lai.py`); tờ này chỉ thêm phần concept không có. Đang dùng: lòng miệng (ô trên phải). Mắt nhắm làm từ chính mắt concept (phủ kín đúng tròng) nên hai mắt nhắm GPT vẽ chỉ để dự phòng; hai ngón càng cũng dự phòng (ngón cắt từ concept, gốc vẽ bù).

| Ảnh mẫu | Đường dẫn | Trông như thế nào |
|---|---|---|
| 1 | `D:\PokiClash\ArtGen\Islands\refs\world_style.png` | Ảnh mốc nét vẽ (1024 × 1536, bản đồ thế giới vẽ tay, nền xanh biển): viền mực nâu hơi rung, tô chì màu và sáp màu. Chỉ lấy nét |
| 2 | `D:\PokiClash\ArtGen\Spine\inbox\tm02_2\tai_ve\L1_duyet.png` | Concept đã duyệt của dạng này (1536 × 1024, nền trắng) |

Ảnh ra: 1536 × 1024 nền trắng, lưới 3 × 2 ô 512: mắt trái nhắm, mắt phải nhắm, lòng miệng (hồng sẫm có lưỡi), ngón trên càng búa, ngón càng còn lại, ô cuối trống.

Kiểm: mảnh rời nhau, không bóng, đúng màu concept; lòng miệng là một mảng tròn không răng.
