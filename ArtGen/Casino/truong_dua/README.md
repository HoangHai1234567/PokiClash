# Hình Trường đua kiểu sân vận động (người dùng dặn 2026-11-26)

"Sáng tạo hơn ở màn đua, thiết kế track đua như kiểu sân vận động 2 bên có khán giả." Màn: `RaceScene` + `RaceStadium`, dựng bằng menu
`PokiClash/Prefab/Đảo Casino/Trường đua: dựng scene` (`Editor/CasinoRaceMenu.cs`). Ghi chép thiết kế ở `GD_Claude/29_DaoCasino.md`.

## Tờ gen (`goc/`)

Magnific GPT 2.6, 3:2, 1k, chất lượng high: 95 credit / tờ; 4 tờ đầu + tờ bục + tờ quầy cược = 570 credit, tờ nào cũng đạt ngay lượt đầu. Ảnh mẫu kèm cả 4 tờ:
`ArtGen/Islands/refs/world_style.png` (nét vẽ) và `Assets/03 Art/Casino/casino_ct_dua.png` (khán đài nhỏ trên đảo: mái sọc đỏ kem, cờ
vàng, gỗ mật ong, rào dây). Mọi tờ nền trong suốt, không chữ, không bóng đổ.

| Tờ | Nội dung dặn trong prompt |
|---|---|
| `khan_dai_1k.png` | Ba dải ngang chạy hết bề rộng, nhìn thẳng mặt trước (không phối cảnh), để lát cuộn: (A) lưng khán đài: cờ đuôi nheo vàng trên mái, mái bạt sọc viền vỏ sò, vách ván sẫm, ba bậc ghế gỗ TRỐNG (khán giả game tự thêm); (B) tường ván phía trước có dây cờ tam giác và hai băng vải trống; (C) hàng rào dây: cọc tròn mũ vàng, hai dây chùng |
| `khan_gia_1k.png` | Hàng trên 8 con thú nhỏ tự nghĩ (mèo, ếch, thỏ, gà con, gấu, rồng con, chuột, cáo; mỗi con một màu) nhìn TỪ TRƯỚC, bán thân cắt ngang ngực, giơ tay reo, có cờ / mũ / loa giấy / khăn. Hàng dưới 6 con nhìn TỪ SAU LƯNG, to hơn 30%, có biển trống, mũ rơm, cờ. Tô phẳng |
| `do_dung_1k.png` | Bảng treo khung gỗ lòng bảng đen trống (hai dây, hàng bóng đèn vàng); cán cờ trơn mũ vàng; dải vạch đích ca rô dọc; cờ ca rô rời; cờ đuôi nheo TRẮNG rời (game nhuộm màu hệ); biển tròn trống trên cọc |
| `trang_tri_he_1k.png` | Lưới 5 cột × 3 hàng vật nhỏ ven đường theo hệ: Kim (bánh răng, đe, bu lông), Mộc (cỏ, nấm, bụi), Thủy (vũng, giọt, sóng), Hỏa (lửa, than hồng, dung nham), Thổ (đá, gốc cây, ụ cát) |
| `buc_1k.png` | Lượt hai (kèm thêm tờ đồ dùng làm mẫu nét): bục nhận thưởng 3 bậc (giữa cao nhất, trái vừa, phải thấp; mỗi bậc một biển tròn trống, dây cờ, thảm đỏ), cúp vàng, ba nơ hạng vàng / bạc / đồng |
| `quay_cuoc_1k.png` | Lượt cược: tấm quầy cược gỗ có mái bạt sọc (lòng trống để đặt nút), 4 đồng chip xanh lá / xanh dương / đỏ / tím lòng trống, dải băng đỏ trống, vé vàng và vé xám |

## Đóng gói

`py -3 -I ArtGen/Casino/truong_dua/dong_goi.py` → `Assets/03 Art/Baked/Casino/`:

- `race_san.png` (2048 x 1024): `khan_dai` (đã bỏ hàng cờ mái, vá chân cán cờ; cắt ở tâm hai cột biên), `tuong`, `rao` (cắt ở tâm cọc
  đầu / cọc cuối), `dat` (vân chì sáp chéo sinh bằng mã, lặp liền; game nhân màu chặng lên). Ba dải đầu lát lật gương nên mép nối luôn
  khớp; mỗi hình nới mép 2 px chống rỉ màu.
- `race_hinh.png` (2048 x 1024): `fan_f0..7`, `fan_b0..5`, `bang`, `cot`, `vach_dich`, `co_caro`, `co_trang`, `bien_tron`, `co_mai`
  (cờ mái cắt từ tờ khán đài), `decal_<hệ>_<0..2>`.
- `race_buc.png` (1024 x 672): `buc`, `cup`, `no_vang`, `no_bac`, `no_dong`.
- `race_quay.png` (2048 x 736): `quay` (cắt 9 mảnh: viền trái 62, dưới 56, phải 62, trên 168 px), `chip_0..3`, `bang_ron` (cắt 9 mảnh hai đầu 96 px), `ve`, `ve_het`. Viền ghi ở `border` của từng hình trong `race_art.json`.
- `race_art.json`: khung từng hình + `bang_trong` (ô bảng đen để đặt chữ) + `buc_cho`, `buc_bien` (chỗ đứng và tâm biển tròn hạng 1, 2, 3 trên bục). Menu dựng scene đọc file này và đặt cách nhập (nhiều sprite,
  ASTC 6x6). Thư mục `Baked` nên `ArtImporter` không ép về một sprite.
- `xem/race_san.jpg`, `xem/race_hinh.jpg`: tờ soi.

Số đo khung trong `dong_goi.py` là của đúng 4 tờ này. Gen lại tờ nào thì đo lại tờ đó (soi hàng / cột alpha).
