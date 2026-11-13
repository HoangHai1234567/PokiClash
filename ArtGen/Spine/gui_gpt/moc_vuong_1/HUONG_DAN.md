# Boss cuối đảo Mộc (`moc_vuong`): gói GPT

Con gốc của rig: `monster_3709` (game tham khảo). Chỉ lấy cách dựng; hình là thiết kế của mình: **rồng trúc bốn cánh**.

## Lượt 1: concept (mỗi kiểu một file, gửi GPT đường dẫn file)

- **nga** (rồng trúc ngà: lông kem, mặt vảy ngọc, cánh lá trúc lục + cánh lá ngà vàng): `D:\PokiClash\ArtGen\Spine\gui_gpt\moc_vuong_1\luot_1_concept_nga.txt`
  - lưu: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\tai_ve\L1_nga.png`
- **mac** (rồng trúc mực: lông than mực, giáp vàng ngà, cánh lục bảo + cánh vàng): `D:\PokiClash\ArtGen\Spine\gui_gpt\moc_vuong_1\luot_1_concept_mac.txt`
  - lưu: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\tai_ve\L1_mac.png`

## Ảnh mẫu trong file prompt

1. `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\mau\bo_cuc_<kiểu>.png`: sơ đồ bố cục 1536x1024 nền trắng, máy dựng: hai quạt lá lục to giơ chữ V (cánh trên), hai quạt lá vàng rủ xuống (cánh dưới), hai ống vàng cao (sừng), khối kem giữa (bờm, cổ, ngực, giáp, ngọc), dải lục dài vắt ngang phía dưới (đuôi), bốn chân. Chỉ để lấy chỗ đặt, cỡ, thứ tự chồng.
2. `D:\PokiClash\ArtGen\Spine\inbox\chim_la_1\tai_ve\L1_duyet.png`: concept chim lá đã duyệt, 1536x1024 nền trắng: mốc nét mực, vân sáp, tô phẳng, cách vẽ từng chiếc lá.
3. `D:\PokiClash\ArtGen\Spine\inbox\kiem_si_1\tai_ve\L1_duyet.png`: concept Voọc Tướng đã duyệt, 1536x1024 nền trắng: mốc nét và cách vẽ giáp tre.
4. `D:\PokiClash\ArtGen\Islands\refs\world_style.png`: bản đồ thế giới 1024x1536: mốc nét bút mực + chì sáp.

## Cách kiểm

- Đủ bốn cánh (hai quạt lục giơ lên, hai quạt vàng rủ xuống), từng chiếc lá có viền riêng, không dính thành mảng.
- Đầu rồng mõm dài có nanh, một mắt, nhìn sang PHẢI; không phải mỏ chim. Hai sừng ống trúc vát nhọn, có mắt trúc.
- Đuôi dải lá dài vắt ngang TRƯỚC chân. Bốn chân có ống giáp trúc. Ngọc bích giữa ngực.
- Tô phẳng: không bóng, không điểm sáng trắng, không bóng loáng, không quầng sáng; chỉ một chấm sáng trong mắt.
- Nền trắng tinh, không viền sticker, không đất, không chữ.

## Câu sửa nhanh (`--note`)

- Còn bóng / điểm sáng: `Remove every highlight, shine spot and shadow: each area one flat colour.`
- Lá dính mảng: `Every wing leaf must be its own closed outlined shape, overlapping like tiles.`
- Ra mỏ chim: `The head is a dragon/kirin head with a long muzzle and fangs, NOT a bird beak.`
- Vẫn chibi: `Not chibi at all: adult heroic proportions, small head, long neck, huge wings.`

## Lượt 1b: sửa sừng trên bản nháp kiểu tối (2026-11-13)

Người dùng: "bản màu đen đẹp hơn nhưng 2 cái sừng hình 2 ống tre không đẹp và sừng bên phải đang cắm ở sai chỗ". Mỗi file vẽ lại `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\tai_ve\L1_mac.png` (bản nháp 1536x1024 nền trắng: rồng trúc thân mực than), giữ nguyên mọi thứ, chỉ thay hai sừng; cả hai sừng mọc từ đỉnh sọ sau mày.

- **mang** (sừng măng tre: hai sừng cong to như búp măng xếp bẹ, mực than viền vàng): `D:\PokiClash\ArtGen\Spine\gui_gpt\moc_vuong_1\luot_1b_sung_mang.txt`
  - lưu: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\tai_ve\L1_mac_mang.png`
- **nhanh** (sừng rồng chia nhánh: gạc rồng vàng ngà ba nhánh nhọn, có mắt trúc): `D:\PokiClash\ArtGen\Spine\gui_gpt\moc_vuong_1\luot_1b_sung_nhanh.txt`
  - lưu: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\tai_ve\L1_mac_nhanh.png`
- **liem** (sừng trúc đen lưỡi liềm: hai sừng dài cong ngược ra sau, mực đen đốt vàng, mũi nhọn): `D:\PokiClash\ArtGen\Spine\gui_gpt\moc_vuong_1\luot_1b_sung_liem.txt`
  - lưu: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\tai_ve\L1_mac_liem.png`

Kiểm: hai gốc sừng nằm cạnh nhau trên đỉnh đầu, sau mắt; không còn bóng ống tre cũ; cánh, thân, đuôi trùng bản nháp.

## Lượt 2: mảnh theo khung part của rig (2026-11-13, sau khi chốt concept bản tối + sừng măng)

Concept đã duyệt: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\tai_ve\L1_duyet.png` (1536x1024 nền trắng: rồng trúc thân mực than, bốn cánh lá, sừng măng).

Mỗi tờ: ảnh 1 là tờ hướng dẫn (các khối phẳng máy dựng, mỗi khối một mảnh rời nằm đúng chỗ, đúng cỡ); ảnh 2 là concept đã duyệt (chỉ để lấy nét và chất liệu). GPT vẽ lại sạch từng mảnh, giữ nguyên hình bóng. Claude cắt bằng `moc_vuong.py cat_part Q<k>`.

- **Q1** (canh_tren_gan, 2 mảnh): `D:\PokiClash\ArtGen\Spine\gui_gpt\moc_vuong_1\luot_2_part_Q1.txt`
  - ảnh 1: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\mau\part_Q1.png`; lưu: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\tai_ve\N_Q1.png`
- **Q2** (canh_tren_gan, 7 mảnh): `D:\PokiClash\ArtGen\Spine\gui_gpt\moc_vuong_1\luot_2_part_Q2.txt`
  - ảnh 1: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\mau\part_Q2.png`; lưu: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\tai_ve\N_Q2.png`
- **Q3** (canh_tren_gan, 10 mảnh): `D:\PokiClash\ArtGen\Spine\gui_gpt\moc_vuong_1\luot_2_part_Q3.txt`
  - ảnh 1: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\mau\part_Q3.png`; lưu: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\tai_ve\N_Q3.png`
- **Q4** (canh_tren_gan, 12 mảnh): `D:\PokiClash\ArtGen\Spine\gui_gpt\moc_vuong_1\luot_2_part_Q4.txt`
  - ảnh 1: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\mau\part_Q4.png`; lưu: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\tai_ve\N_Q4.png`
- **Q5** (canh_tren_xa, 9 mảnh): `D:\PokiClash\ArtGen\Spine\gui_gpt\moc_vuong_1\luot_2_part_Q5.txt`
  - ảnh 1: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\mau\part_Q5.png`; lưu: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\tai_ve\N_Q5.png`
- **Q6** (canh_tren_xa, 14 mảnh): `D:\PokiClash\ArtGen\Spine\gui_gpt\moc_vuong_1\luot_2_part_Q6.txt`
  - ảnh 1: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\mau\part_Q6.png`; lưu: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\tai_ve\N_Q6.png`
- **Q7** (canh_tren_xa, 8 mảnh): `D:\PokiClash\ArtGen\Spine\gui_gpt\moc_vuong_1\luot_2_part_Q7.txt`
  - ảnh 1: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\mau\part_Q7.png`; lưu: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\tai_ve\N_Q7.png`
- **Q8** (canh_duoi_gan, 8 mảnh): `D:\PokiClash\ArtGen\Spine\gui_gpt\moc_vuong_1\luot_2_part_Q8.txt`
  - ảnh 1: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\mau\part_Q8.png`; lưu: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\tai_ve\N_Q8.png`
- **Q9** (canh_duoi_gan, 14 mảnh): `D:\PokiClash\ArtGen\Spine\gui_gpt\moc_vuong_1\luot_2_part_Q9.txt`
  - ảnh 1: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\mau\part_Q9.png`; lưu: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\tai_ve\N_Q9.png`
- **Q10** (canh_duoi_gan, 3 mảnh): `D:\PokiClash\ArtGen\Spine\gui_gpt\moc_vuong_1\luot_2_part_Q10.txt`
  - ảnh 1: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\mau\part_Q10.png`; lưu: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\tai_ve\N_Q10.png`
- **Q11** (canh_duoi_xa, 9 mảnh): `D:\PokiClash\ArtGen\Spine\gui_gpt\moc_vuong_1\luot_2_part_Q11.txt`
  - ảnh 1: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\mau\part_Q11.png`; lưu: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\tai_ve\N_Q11.png`
- **Q12** (canh_duoi_xa, 11 mảnh): `D:\PokiClash\ArtGen\Spine\gui_gpt\moc_vuong_1\luot_2_part_Q12.txt`
  - ảnh 1: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\mau\part_Q12.png`; lưu: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\tai_ve\N_Q12.png`
- **Q13** (duoi, 6 mảnh): `D:\PokiClash\ArtGen\Spine\gui_gpt\moc_vuong_1\luot_2_part_Q13.txt`
  - ảnh 1: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\mau\part_Q13.png`; lưu: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\tai_ve\N_Q13.png`
- **Q14** (duoi, 3 mảnh): `D:\PokiClash\ArtGen\Spine\gui_gpt\moc_vuong_1\luot_2_part_Q14.txt`
  - ảnh 1: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\mau\part_Q14.png`; lưu: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\tai_ve\N_Q14.png`
- **Q15** (than_chan, 3 mảnh): `D:\PokiClash\ArtGen\Spine\gui_gpt\moc_vuong_1\luot_2_part_Q15.txt`
  - ảnh 1: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\mau\part_Q15.png`; lưu: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\tai_ve\N_Q15.png`
- **Q16** (than_chan, 9 mảnh): `D:\PokiClash\ArtGen\Spine\gui_gpt\moc_vuong_1\luot_2_part_Q16.txt`
  - ảnh 1: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\mau\part_Q16.png`; lưu: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\tai_ve\N_Q16.png`
- **Q17** (than_chan, 15 mảnh): `D:\PokiClash\ArtGen\Spine\gui_gpt\moc_vuong_1\luot_2_part_Q17.txt`
  - ảnh 1: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\mau\part_Q17.png`; lưu: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\tai_ve\N_Q17.png`
- **Q18** (than_chan, 19 mảnh): `D:\PokiClash\ArtGen\Spine\gui_gpt\moc_vuong_1\luot_2_part_Q18.txt`
  - ảnh 1: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\mau\part_Q18.png`; lưu: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\tai_ve\N_Q18.png`
- **Q19** (than_chan, 5 mảnh): `D:\PokiClash\ArtGen\Spine\gui_gpt\moc_vuong_1\luot_2_part_Q19.txt`
  - ảnh 1: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\mau\part_Q19.png`; lưu: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\tai_ve\N_Q19.png`
- **Q20** (dau, 12 mảnh): `D:\PokiClash\ArtGen\Spine\gui_gpt\moc_vuong_1\luot_2_part_Q20.txt`
  - ảnh 1: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\mau\part_Q20.png`; lưu: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\tai_ve\N_Q20.png`
- **Q21** (dau, 2 mảnh): `D:\PokiClash\ArtGen\Spine\gui_gpt\moc_vuong_1\luot_2_part_Q21.txt`
  - ảnh 1: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\mau\part_Q21.png`; lưu: `D:\PokiClash\ArtGen\Spine\inbox\moc_vuong_1\tai_ve\N_Q21.png`

Kiểm: đủ số mảnh, mảnh không dính nhau, hình bóng trùng tờ hướng dẫn (Claude đo IoU, dưới 0,9 thì gen lại tờ đó); tô phẳng, không bóng, không điểm sáng.
