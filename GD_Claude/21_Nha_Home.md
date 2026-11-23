# Nhà (Home): đảo giáp biển, xây công trình, mở ô rừng

Viết 2026-11-18. Mới là kế hoạch, chưa làm dòng code nào. Nhà thay cho Trang trại (`Core/Farm.cs`, scene `Farm`, xem `12_KeHoach_OpenSpec.md` mốc 9).

## Người dùng dặn (2026-11-18)

| Mục | Lời dặn |
|---|---|
| Nút | Trang trại đổi thành **nút Nhà** ("về nhà") |
| Mẫu | Học phần nhà (homestead) của Clash of Critters |
| Công trình | Người chơi xây: vườn rau, tưới tiêu, đào mỏ, lò rèn… |
| Tiến độ | Có progression và điều kiện mở khoá |
| Tướng | Có thẻ để chỉ định tướng đã có vào làm |
| Trang trí | Có đồ trang trí |
| Concept | **Đảo giáp biển** như Critters |
| Mở đất | Mở thêm **ô rừng** theo cấp người chơi và theo tiến độ riêng của nhà |

## Critters làm nhà ra sao (bản đục 0.51.1, `D:\Ripper\ClashOfCritters`)

Chỉ đọc được tên asset và prefab. Bảng số và chữ của họ đã mã hoá, không phá (xem memory `coc-config-extraction`). Học cách dựng, không chép hình, không gửi hình của họ cho GPT.

| Phần | Họ có | Asset |
|---|---|---|
| Công trình làm ra đồ | Ruộng (đất trồng được và đất chưa khai hoang), vườn cây ăn quả, mỏ vàng (máy đào, máy dò, "đào vàng"), bếp và nhà ăn (cho thú ăn, có tăng tốc), suối nước nóng, nhà tập (đấu huy hiệu), **cây bi nằm trong nhà** | `functional_arable`, `functional_unarable`, `plant_orchard`, `building_goldmine`, `decoration_miningmachine`, `detector`, `goldrush`, `canteen_pop`, `kitchen_bubble`, `decoration_autofeeder`, `hotspring_*`, `gym`, `pinballtree_bubble` |
| Câu cá | Bến câu ven sông, câu vịt, cúp câu cá đồng, bạc, vàng | `building_riversidefishing`, `building_duckfishing`, `fishspot_bubble`, `decoration_fishingachievement*trophy` |
| Công nghệ nhà | Cây nâng cấp bổ trợ phần khác của game: kẹo, kẹo bất ngờ, nhân đôi, cây bi, máy bi bất ngờ, mở huy hiệu thú | `homestead_tech_candy`, `_candysurprise`, `_double`, `_marbletree`, `_pinballsurprise`, `_unlockpetbadge`, `build_tech_*` |
| Bong bóng trên công trình | Thu hoạch, thẻ, bắt thú lạc vào nhà, quà, tiệc, mở rộng đất | `farm_bubble`, `cardcollection_bubble`, `catch_bubble`, `giftbox_bubble`, `party_bubble`, `expand_bubble` |
| Trang trí | Hơn 150 món chia bộ chủ đề (cắm trại, công viên, tiệm bánh, quán ăn, Giáng sinh…), cây hoa, hàng rào; **trang trí thưởng trận boss chương** (phế tích) | `decoration_*`, `plant_*`, `fence_*`, `decoration_bossbattle*` |
| Đường, nền | Lát đường đất, gạch, cỏ; tô nước theo ô (bờ trong, bờ ngoài, góc) | `road_*`, `road_water_*`, `brickfloor_*` |
| Mở đất | Vùng mở được 1, 2, 3; vùng chưa mở được; hiệu ứng mở 3x3, xây 1x1 | `decoration_unlockableregion*`, `decoration_cannotunlockarea`, `pbfx_camp_expand_3x3`, `pbfx_camp_build_1x1` |
| Chế độ xây | Sửa, xoá, sửa đường | `pbui_homestead_building_edit`, `_building_delete`, `_road_edit` |
| Nền tảng | Lưới thoi, tìm đường cho thú, camera trực giao có khung, ngày đêm | `IsoGridMap`, `IsoGridPahFinder`, `HomesteadGridController`, `daynight` |

Rút ra bốn điều:

1. Nhà là chỗ thú làm việc và nghỉ, ra đồ phục vụ trận và máy bi.
2. Tiến độ của nhà gồm mở đất, công trình mới, nâng cấp, công nghệ.
3. Trang trí rất nhiều nhưng rẻ để vẽ (mỗi món một ảnh); có món chỉ lấy được bằng thắng boss.
4. Mọi thứ nằm trên lưới thoi, người chơi tự đặt và dời.

## Đề xuất

### Góc nhìn và tỉ lệ (soi bản đục Critters, 2026-11-18)

Người dùng xem concept lần 1: rừng và môi trường được, nhưng **góc nhìn chưa đúng ý** (nhìn như bản đồ thế giới, công trình mỗi cái một góc) và **đảo chưa đủ rộng**.

| Mục | Critters (đo trong bản đục) | Mình |
|---|---|---|
| Phép chiếu | Isometric 2:1: lưới thoi `cellSize 1`, `heightRatio 0.5` (`pbsc_grid_renderer`). Camera trực giao, không xoay (`pbsc_homestead_camera`, cỡ trực giao 4,5); góc nhìn vẽ sẵn trong ảnh | Giống hệt: ô thoi rộng gấp đôi cao, cạnh lưới nghiêng 26,6°. Mọi công trình có góc nhọn của chân thoi chĩa xuống phía người xem, thấy mái và hai mặt tường trái, phải, cùng một góc |
| Cỡ ô | 1 đơn vị = 100 px ảnh | 1 ô = 96 × 48 px ở khung 1080 lúc thu phóng thường (khoảng 11 ô ngang màn) |
| Công trình | Quán cà phê, vườn cây 4×4 ô; mỏ vàng 6×6; ruộng 8×8; ghế đá 2×2 | Công trình thường 4×4; Nhà chính, Mỏ 6×6; Giếng, Cây bi 2×2; trang trí 1×1 đến 2×2 |
| Đất khoá | Một ảnh rời 8×8 ô: chân thoi cỏ phủ kín thông, cây tán tròn, gốc cây, đá rêu (`decoration_unlockableregion*`) | Ô rừng 8×8, mỗi kiểu một ảnh rời |
| Nền | Đồng cỏ phẳng. Rìa ghép mảnh rời: bãi cát, cao nguyên vách nâu, núi xa, dải phong cảnh xa ở trên cùng (`bgdecoration_*`) | Như họ: hai cạnh dưới là bãi cát rồi biển, hai cạnh trên là cao nguyên, trên cùng là phong cảnh xa |
| Cỡ làng | Clash of Clans: lưới 44 × 44 ô | Đảo **72 × 72 ô** = 6 × 6 ô rừng 12 × 12 (2026-11-19; bản đầu 48 × 48, ô rừng 8 × 8) |
| Lưới | Chỉ hiện lúc xây (nét trắng mờ, hoặc gạch ngắn đầu tròn màu xanh) | Chỉ hiện lúc xây |

- Đảo là một hình thoi lớn: 48 ô × 96 px là khoảng 4.600 px ngang, tức 4,3 màn ngang và 1,2 màn dọc. Thêm vành cát, biển, cao nguyên thì khoảng 5 × 2 màn.
- Thu nhỏ hai ngón tới mức thấy cả đảo (khoảng 0,25 lần), phóng to tới 1,2 lần.

### Hình dung đảo nhà

```
                 dải phong cảnh xa, núi, biển xa
                            ▲ (góc trên)
                 cao nguyên ╱  ▲▲ ▲▲  ╲ cao nguyên
                         ╱ ░░ ░░ ~hồ~ ░░ ╲
                      ╱ ░░ ░░ ░░ ░░ ░░ ░░ ░░ ╲          ░ ô rừng 8×8 chưa mở
                   ╱ ░░ ░░ ░░  S  ░░  S  ░░ ░░ ╲        S dọn được, C đang dọn
        (góc trái) ◄ ░░ ~hồ~ ░░  C  ▲ mỏ  ░░ ░░ ░░ ► (góc phải)
                   ╲ ░░ ░░ [ruộng][Nhà chính][xưởng] ░░ ╱
                      ╲ ░░ [ao][giếng][cây bi][lò rèn]╱
                         ╲ bãi cát  [bếp] bãi cát ╱
                            ╲      ⚓ bến       ╱
                                    ▼ (mũi nam)          biển
```

- **Concept 2026-11-18, lần 2** (isometric 2:1, GPT 2.6 qua Magnific, chỉ để hình dung), ở `ArtGen/Home/concept/`. Xem cả bộ ở `xem_concept.html`; prompt nằm cạnh ảnh; bản phác bố cục do `make_refs_iso.py` dựng.
  - `concept_F_iso_toan_dao_2.png`: toàn đảo thu nhỏ hết cỡ;
  - `concept_D_iso_mot_man.png`: một màn chơi kèm UI;
  - `concept_E_iso_che_do_xay.png`: chế độ xây (lưới hiện, công trình nhấc lên, chân xanh, ô đỏ, khay thẻ công trình).
- Lần 1 (góc nhìn bản đồ, đã bỏ): `concept_A_toan_dao_nha.png`, `concept_B_mot_man_nha.png`; `concept_C_iso_toan_dao.png` là lần thử isometric hỏng (GPT vẽ lại bố cục cũ).
- Bờ nam là bãi cát và bến thuyền. Nước dùng shader `InkWater` của kế hoạch đảo (`18_DaoVungDat_Habitat.md`).
- **Khoảnh đầu** 16 × 16 ô (2 × 2 ô rừng) đã dọn sẵn quanh Nhà chính, ở giữa nửa dưới đảo, kề bãi cát.
- Phần còn lại là **6 × 6 = 36 ô rừng**, mỗi ô 8 × 8 ô lưới. Trừ khoảnh đầu và ô bến, còn khoảng 30 ô để mở dần theo vòng V1, V2, V3 tính từ khoảnh đầu.
- Vài ô rừng giấu **điểm đặc biệt** cố định, nên mở rừng có mục đích:
  - mạch quặng (V2, V3): chỗ duy nhất đặt Mỏ;
  - suối: Cối nước đặt cạnh suối;
  - đất màu: ruộng, vườn đặt lên được thêm 10% năng suất;
  - ghềnh đá ven biển: Ao cá đặt ở đây câu được thêm đồ hiếm.

### Mở ô rừng

- **Hai khoá**: cấp người chơi và cấp Nhà chính (ví dụ "Nhà cấp 3 và cấp 25").
- Chỉ mở được ô rừng **kề đất đã mở**, nên đất lan dần từ khoảnh đầu ra.
- Chi phí: gỗ, sau này thêm quặng. Dọn rừng tốn thời gian như xây (đội thợ dùng chung).
- Dọn xong rơi gỗ một lần; vài ô rơi rương cũ hoặc một món trang trí.
- Hình theo trạng thái:
  - chưa đủ điều kiện: cây dày phủ kín, bảng gỗ ghi điều kiện;
  - mở được: biển "Dọn được" nhún nhẹ;
  - đang dọn: tướng chặt cây, lá bay, đồng hồ;
  - xong: cây đổ tan thành lá, đất cỏ lộ ra (hiệu ứng mở 8x8 như `pbfx_camp_expand_3x3` của họ).

### Công trình

**Làm ra đồ** (cần tướng). Luật sức làm, nghỉ, năng suất giữ như Trang trại: ca 8 giờ (+1 giờ mỗi sao), nghỉ 15–60 phút, kho 10 giờ sản lượng, hợp hệ ×1,25, năng suất theo độ hiếm và sao.

| Công trình | Cỡ | Hệ hợp | Chỗ tướng | Làm ra | Mở ở Nhà cấp |
|---|---|---|---|---|---|
| Ruộng rau | 4x4 | Thổ | 1, cấp 4 lên 2 | bi | 1 |
| Vườn cây ăn quả | 4x4 | Mộc | 1, cấp 4 lên 2 | bi | 1 |
| Xưởng gỗ | 4x4 | Mộc | 1, cấp 4 lên 2 | gỗ | 1 |
| Ao cá | 4x4 | Thủy | 1, cấp 4 lên 2 | câu ra bi, thẻ chiêu thường, hiếm khi ra cúp (trang trí) | 2 |
| Mỏ | 6x6, chỉ trên mạch quặng | Thổ | 1, cấp 3 lên 2, cấp 6 lên 3 | quặng; ít đá tiến hóa | 3 |
| Lò rèn | 4x4 | Kim | 1, cấp 4 lên 2 | rèn quặng thành đá tiềm năng; cấp cao ra đá tinh | 4 |
| Bếp | 4x4 | Hỏa | 1, cấp 4 lên 2 | bánh: cho tướng đang nghỉ ăn thì hết nghỉ ngay | 4 |

Năm hệ đều có việc. Năm khu của Trang trại cũ khớp sẵn: ao vịt (Thủy) thành Ao cá, ruộng rau (Thổ) thành Ruộng rau, vườn cây (Mộc) thành Vườn cây, lò bánh (Hỏa) thành Bếp, xưởng nông cụ (Kim) thành Lò rèn.

**Hỗ trợ** (không cần tướng):

| Công trình | Cỡ | Tác dụng | Mở ở Nhà cấp |
|---|---|---|---|
| Nhà chính | 6x6, cố định | Cấp nhà: mở công trình, ô rừng, chỗ tướng, số công trình mỗi loại | có sẵn |
| Kho | 4x4 | Sức chứa gỗ, quặng | 1 |
| Giếng (tưới tiêu) | 2x2 | Ruộng, vườn trong bán kính 4 ô +10% năng suất | 2 |
| Cối nước (tưới tiêu) | 4x4, cạnh suối | Bán kính 8 ô +20% | 5 |
| Suối nước nóng | 4x4 | Tướng nghỉ nhanh hơn 25%, cấp 2 là 50% | 4 |
| Cây bi | 2x2 | Dời từ sảnh vào nhà như Critters, luật giữ nguyên (5 bi mỗi giờ, chứa 50, cây mới mở ở cấp 30, 50, 80, 110). Từ 2026-11-23 thẻ ở sảnh bỏ hẳn; người chơi tự đặt cây từ khay Xây (miễn phí), lần đầu có hướng dẫn (25_FTUE.md, G3a–G3d) | cùng lúc mở Nhà (trước 2026-11-23: khi qua ải 1) |
| Bến thuyền | cố định | Nút "Ra đảo" về sảnh | có sẵn |

Tưới tiêu là chỗ xếp đặt có tính toán: đặt ruộng, vườn quanh giếng và cối nước thì ra nhiều hơn. Bán kính hiện bằng vòng ô xanh khi nhấc công trình lên.

### Cấp Nhà chính

Số tạm, đã đo một vòng (mục "Tiến độ"). Số thật nằm ở khối `home` của `balance.json`.

| Nhà cấp | Cấp người chơi | Chi phí | Mở thêm | Tổng chỗ tướng | Ô rừng mở tối đa | Đội thợ |
|---|---|---|---|---|---|---|
| 1 | mở Nhà (có 3 tướng, như Trang trại) | | Ruộng rau, Vườn cây, Xưởng gỗ, Kho (có sẵn) | 4 | 6 | 1 |
| 2 | 10 | 60 gỗ | Ao cá, Giếng | 5 | 10 | 1 |
| 3 | 25 | 200 gỗ | Mỏ; dọn được vòng 2 | 6 | 13 | 1 |
| 4 | 40 | 400 gỗ, 80 quặng | Lò rèn, Bếp, Suối nước nóng | 8 | 16 | 2 |
| 5 | 60 | 700 gỗ, 200 quặng | Cối nước; dọn được vòng 3 | 9 | 20 | 2 |
| 6 | 80 | 1000 gỗ, 320 quặng | | 10 | 23 | 2 |
| 7 | 100 | 1400 gỗ, 480 quặng | | 11 | 26 | 2 |
| 8 | 125 | 1900 gỗ, 650 quặng | | 12 | 28 | 2 |
| 9 | 150 | 2500 gỗ, 850 quặng | | 13 | 30 | 2 |
| 10 | 175 | 3200 gỗ, 1100 quặng | | 14 | 32 | 2 |

- **Bi không phình**: tổng chỗ làm ra bi (ruộng, vườn, ao) giữ theo đường của Trang trại cũ, 3 chỗ lúc đầu, thêm ở cấp 40, 70, 96, 120, 144 (`farm.spotLevels`, `Home.BallSlots`).
- **Tổng chỗ tướng luôn dư 2–3 chỗ so với chỗ ra bi** (đo 2026-11-18): bản đầu (3, 4, 5…) làm Mỏ không có ai làm, không có quặng, Nhà kẹt ở cấp 3.
- Số công trình mỗi loại tăng theo cấp nhà (ví dụ ruộng 1, 2, 3).
- Mỗi công trình nâng cấp riêng (cấp 1–7, không vượt cấp nhà): thêm năng suất, kho, chỗ tướng. Hình đổi ở cấp 1, 4, 7.

### Thẻ chỉ định tướng

- Mỗi công trình làm ra đồ có 1–3 ô thẻ trên bảng của nó. Chạm ô thì mở hộp chọn tướng (dùng lại `FarmPickerDialog`): thẻ tướng ghi năng suất ở công trình này, giờ làm, hợp hệ, đang nghỉ bao lâu.
- Kéo tướng đang lang thang thả vào công trình cũng là giao việc, như Trang trại bây giờ.
- Một tướng làm một chỗ một lúc. Sức làm tách khỏi trận (GDD).
- Giữ nút **Tự xếp** (chọn cặp năng suất cao nhất).
- Tướng làm việc cử động theo công trình: cuốc (ruộng), hái (vườn), câu (ao), chặt (xưởng gỗ), đập đá (mỏ), rèn (lò rèn), nhào bột (bếp). `FarmPet` đã có cuốc, hái, nhào bột, rèn.
- Tướng rảnh đi lang thang theo tìm đường trên lưới, ngồi lên ghế, xích đu (món trang trí có "chỗ chơi"). Hết sức thì ngồi nghiêng, đang nghỉ thì ngủ ở ổ rơm hoặc ngâm suối nước nóng.

### Trang trí

- Mua bằng gỗ, quặng hoặc bi. Có món chỉ có từ thưởng:
  - **tượng boss**: thắng boss ải 70 một đảo thì được tượng nhỏ của boss đó (học "phế tích trận boss" của Critters);
  - cúp câu cá từ Ao cá;
  - quà mốc cấp nhà.
- Đặt tự do trên ô đã mở, dời được, cất vào túi. Không bán lại.
- **Điểm đẹp**: mỗi món có điểm. Qua mốc thì nhận quà một lần (gỗ, bi, đá) và tướng nghỉ nhanh hơn 5% mỗi bậc (tối đa 25%). Điểm đẹp không đụng tới sức mạnh trong trận.
- Bộ theo hệ: Thủy (vỏ sò, đèn biển), Mộc (chậu cây, hàng rào tre), Hỏa (đèn lồng, lò than), Kim (chuông, cột đồng), Thổ (tượng đá, chum). Đủ bộ thì thêm điểm.
- Đường lát: đường đất, đường đá, cầu gỗ qua suối. Code tự nối mép như `road_*` của họ.

### Chế độ xây

- Nút búa vào chế độ xây. Lưới thoi chỉ hiện lúc này: ô xanh đặt được, ô đỏ không.
- Giữ một công trình thì nhấc lên, kéo, thả. Bảng nhỏ: Nâng cấp, Cất, Lật ngang (chỉ trang trí), Thông tin.
- Khay dưới: Công trình, Trang trí, Đường. Món khoá ghi điều kiện.
- Xây, nâng cấp, dọn rừng có thời gian, một đội thợ (Nhà cấp 4 thêm đội thứ hai). Rút 30 phút bằng quảng cáo, giới hạn mỗi ngày; không bán.

### Kinh tế (số tạm, đo bằng `ProgressSim`)

- Bi từ nhà (ruộng, vườn, ao, cây bi) bằng Trang trại cộng cây bi hiện tại ở cùng cấp người chơi.
- Gỗ, quặng chỉ dùng trong nhà (xây, nâng cấp, dọn rừng, trang trí), không đổi ra bi.
- Đá tiến hóa từ mỏ: nguồn đều nhưng nhỏ, khoảng 1 đá mỗi 2 ngày ở mỏ cấp 1, 1 đá mỗi ngày ở cấp cao (một lần tiến hóa tốn 20, 55, 120 đá). Đo lại nhịp tiến hóa (`20_TangDayNoiDung.md`) sau khi thêm.
- Đá tiềm năng từ lò rèn: cỡ một lượt Hang mỗi ngày ở cấp cao.
- Đo ngày 1, 7, 30 cho ba kiểu người chơi (chăm, vừa, ít) như `12_KeHoach_OpenSpec.md`.

### Nút Nhà, chuyển cảnh

- Sảnh: công trình "Trang trại" đổi thành **Nhà**, chạm là về nhà. Điều kiện mở giữ: có 3 tướng.
- Trong Nhà: nút thuyền "Ra đảo" ở góc dưới để về sảnh. Chuyển cảnh bằng mây.
- Thanh trên: bi như cũ, thêm gỗ và quặng khi đang ở Nhà.
- Chấm đỏ trên nút Nhà: kho đầy, tướng hết sức, xây xong, có ô rừng mở được.

## Bản lưu

- **Không đổi số phiên bản** (vẫn v12): thêm khoá tuỳ chọn `home` (công trình: loại, ô, cấp, việc đang làm, tướng từng ô và đồ đang tích; ô rừng đã mở và đang dọn; gỗ, quặng, bánh; nghỉ; túi trang trí; mốc điểm đẹp). Bản lưu không có khoá này vẫn đọc bình thường.
- Gộp bản cũ lúc mở Nhà lần đầu (`Home.Of`): bi đang tích của Trang trại về túi, tướng đang làm sang công trình cùng việc (ao vịt → Ao cá, ruộng → Ruộng rau, vườn → Vườn cây, lò bánh → Bếp, xưởng nông cụ → Lò rèn; thiếu công trình thì đặt thêm, không tính giá), tướng đang nghỉ vẫn nghỉ, rồi `farm` thành null. Cây bi đã mở được đặt vào nhà; `Trees` vẫn tính bi của cây.
- Nhà chạy được thì bỏ hẳn scene `Farm`, prefab, ảnh `farm_bg.png`. Luật sức làm, nghỉ, năng suất của `Core/Farm` gom vào `Core/Home`, không viết lại.

## Code

| Việc | Chỗ |
|---|---|
| Luật: công trình, lưới, cấp, chi phí, sản xuất, ô rừng, thợ, trang trí, điểm đẹp | `Core/Home.cs` (xong H1); phần sức làm lấy từ `Core/Farm.cs` |
| Dữ liệu | Khối `home` trong `Assets/02 Data/Json/balance.json`, đọc bằng `Core/HomeConfig.cs` qua `BalanceConfig.home` (không đụng `GameData`); menu `PokiClash/Nhập dữ liệu` kiểm `HomeConfig.Validate` |
| Lưới thoi, đặt, dời, tìm đường cho thú | `App/Home/HomeGrid.cs`, `HomeBuildMode.cs` |
| Nền, nước, đồ lặt vặt, camera | Dùng chung với đảo vùng đất (`18_DaoVungDat_Habitat.md`: `LandGround`, `InkWater`, `LandScatter`, `HubPan`) |
| Cảnh | `HomeScene` thay `FarmScene`; dùng lại `FarmPet`, `FarmFx`, `FarmPickerDialog` |
| Sảnh | `HubScene.Buildings`: Trang trại thành Nhà; Cây bi rời sảnh (nếu chốt câu 3) |
| Test | `Tests/HomeTests.cs`, 11 test (xong H1); chạy ngoài Unity bằng csc + mono |
| Thử | Menu `PokiClash/Thử/Nhà: tua giờ, mở hết rừng, đủ vật liệu (đang Play)` |

Nền tảng vùng đất (lưới thoi, nền ghép mảnh, nước, rải đồ, camera) làm ở Nhà trước: một bản đồ, ít mảnh hơn đảo 10 vùng. Đảo Thủy mới dùng lại.

## Hình (gen sau khi chốt)

- Bộ nền đảo nhà: cỏ, cát, ghềnh ven biển, mép bờ. Nước do shader.
- Ô rừng: 3–4 kiểu khối rừng 8x8 (cây dày, có cây to, có đá), mỗi kiểu một ảnh rời như `decoration_unlockableregion*` của Critters; bảng gỗ ghi điều kiện.
- Mọi ảnh vẽ đúng isometric 2:1: chân thoi rộng gấp đôi cao, góc nhọn chĩa xuống, thấy mái và hai mặt tường (mục "Góc nhìn và tỉ lệ").
- Công trình: 10 loại, mỗi loại 3 dáng theo cấp, khoảng 30 ảnh.
- Trang trí đợt đầu: 20 món, 4 món mỗi hệ.
- Nét vẽ tay bút mực, chì màu như `ArtGen/Islands/refs/world_style.png`; tô phẳng, không bóng đổ (luật UI); nhìn chéo theo lưới thoi 2:1.
- Gen qua Magnific (dưới 100 credit mỗi ảnh) hoặc gói file prompt GPT `ArtGen/Home/build_home.py`, theo luật ArtGen trong `CLAUDE.md`.

## Các mốc

| Mốc | Việc | Ra gì để duyệt |
|---|---|---|
| H0 | Kế hoạch này, chốt câu hỏi | file này |
| H1 | Luật, dữ liệu, bản lưu, test (chưa có hình) | test đạt, bảng đo kinh tế |
| H2 | Cảnh Nhà bằng hình tạm: lưới thoi, đặt và dời, ô rừng, thợ, nút Nhà trên sảnh | chạy thử trong Unity, ảnh chụp |
| H3 | Giao tướng, thú đi lại làm việc, bong bóng thu | chạy thử |
| H4 | Gen hình: nền, ô rừng, công trình đợt 1 | tờ soi hình |
| H5 | Trang trí, điểm đẹp, tượng boss, đường lát | chạy thử |
| H6 | Ngày đêm theo giờ thật cho mọi đảo và Nhà (mục "Ngày đêm") | chạy thử ở 4 giờ trong ngày |
| H7 (để sau) | Công nghệ nhà (như `homestead_tech_*`: bổ trợ cây bi, máy bi, AFK), thú hoang lạc vào nhà để bắt | |

## Đã chốt (2026-11-18)

Người dùng xem concept lần 2 rồi bảo "bắt đầu làm đi", chưa trả lời 5 câu, nên Claude làm theo đề xuất. Người dùng đổi được bất cứ câu nào.

1. Vật liệu xây: **gỗ và quặng**, vật liệu riêng của nhà (bi để dành cho máy bi).
2. **Có hẹn giờ xây** và đội thợ; rút 30 phút bằng quảng cáo `home_speed`, 3 lần mỗi ngày.
3. **Cây bi dời vào nhà**; Đền Huy Hiệu, Hang Tiềm Năng giữ ở sảnh.
4. Đầu ra như bảng Công trình (Ao cá 1,6 lần câu mỗi giờ sau khi đo).
5. **Đặt tự do**, trừ điểm cố định (hồ, suối, mạch quặng, cao nguyên, bến).
6. Concept: người dùng duyệt lần 2 (isometric 2:1, đảo 48 × 48).
7. **Hình gen theo lớp** (người dùng dặn): gen đảo nền trống trước, rừng, địa hình, công trình gen sau thành ảnh rời đặt lên.

## Tiến độ

**H1 xong (2026-11-18), chưa mở Unity.**
- Code: `Core/HomeConfig.cs`, `Core/Home.cs`; `BalanceConfig.home`; `SaveData.home` (đọc, ghi); `AdGate` dùng giới hạn `home_speed` trong `balance.json`; `Editor/DataImporter.cs` kiểm dữ liệu Nhà.
- Test ngoài Unity (csc + mono): `HomeTests` 11/11. Các test thuần Core còn lại 93/97 đạt; 4 test hỏng ở `TestContext.WriteLine`, chỉ chạy được trong bộ chạy NUnit của Unity, không do Nhà. Chưa chạy EditMode trong Unity.
- Đo 30 ngày: lấy cấp và tướng mỗi ngày từ `ProgressSim`, mô phỏng Nhà (thu, tự xếp, rút tướng hết sức, cho ăn bánh; tiêu: Nhà chính, xây công trình thiếu, dọn rừng, nâng cấp; để dành gỗ cho Nhà chính khi đã đủ quặng). Bộ mô phỏng nằm ở scratchpad, chưa đưa vào dự án:

  | Kiểu (lần vào mỗi ngày) | Bi 30 ngày (Trang trại cũ) | Gỗ | Quặng | Đá tiến hóa | Ngày lên Nhà cấp 2 / 3 / 4 / 5 |
  |---|---|---|---|---|---|
  | Chăm (6) | 7.702 (8.065) | 6.469 | 820 | 6 | 2 / 6 / 15 / 20 |
  | Vừa (3) | 5.129 (6.163) | 2.618 | 417 | 3 | 4 / 11 / 24 / 30 |
  | Ít (1) | 1.428 (1.523) | 713 | 0 | 0 | 13 / 21 / – / – |

- Còn thấp: đá tiềm năng từ Lò rèn bằng 0 (tự xếp lấp chỗ gỗ, quặng trước), bánh gần như không có. Xem lại khi có cảnh thật.

**Hình: đảo nền (2026-11-18)**: `ArtGen/Home/base/base_dao_nen_1.png` (có concept F làm mẫu nét địa hình) và `base_dao_nen_2.png` (không). Prompt `base_dao_nen.txt`, bản phác `make_base_refs.py` (toạ độ lấy từ `balance.json`). Cả hai theo đúng bố cục nhưng hình thoi lệch vài chục px so với bản phác, nên khi dựng cảnh phải đo lại bốn góc hoặc khớp lại toạ độ điểm cố định. Ảnh rộng 1.344 px, trong game đảo rộng khoảng 4.600 px: cần phóng to (Magnific, 90–270 credit) hoặc gen lại theo mảnh.

**Hình: lớp rừng (2026-11-18)**, người dùng duyệt nền bản 1 và dặn:
- ngoài rìa phía trên làm thành rừng hết, chỉ nửa dưới là biển, quanh rìa có mây che;
- tự đắp các cục địa hình cho đẹp.

Đã làm:
- `base_dao_nen_3.png`: bản sửa của bản 1, rìa trên thành rừng kín, nửa dưới là biển, chưa vẽ mây (mây là lớp riêng).
- Ba khối rừng 8x8 `forest_lot_A/B/C.png`: thông; cây tán tròn có đá rêu; lẫn lộn có gốc cây, khúc gỗ đổ. Mỗi khối 10–14 cây to cho khớp cỡ cây rìa. Bản đầu nhồi khoảng 40 cây nhỏ nên lạc cỡ, cất ở `lan1/`.
- `compose_preview.py` tách nền trắng (ra `*_cut.png`) rồi đặt khối rừng lên 28 ô chưa mở, chồng 13% cho kín viền: `preview_rung.png`.
- Thoi đồng cỏ trên ảnh đo được: mũi trái (2,336), mũi phải (1338,334), góc dưới (678,700). Tỉ lệ khoảng 1,85:1; trong Unity kéo ngang nền cho đúng 2:1.
- Hồ dưới thác và mạch quặng nằm dưới rừng cho tới khi dọn.

**Mây và ánh sáng** (người dùng dặn): lấy hình Kingdom Rush (phiên khác đang đục) làm mẫu tham khảo, tự gen hoặc tự làm, không chép nguyên.

Học từ bản đục KR5 (`D:\Ripper\KingdomRush5`, tài liệu `docs\PHAN_TICH_MAP_VA_ANH_SANG.md` của phiên kia):
- Mây che vùng chưa mở là một deco hoạt ảnh `clouds_map`: một mảnh mây mềm 436 x 280, trong khoảng 0,6, dùng lại 23 lần (lật, phóng khoảng 2,2 lần), trôi khoảng 30 đơn vị trong 64 khung, nhấp nháy độ trong; tan mây là hoạt ảnh `out` riêng, có tiếng.
- Ánh sáng không dùng shader: vẽ sẵn vào nền, cộng mảnh sáng mép mềm chồng lên (blend thường), nhấp nháy độ trong. Đom đóm là cặp lõi và quầng.
- Viền tối cố định theo màn hình.

Mình làm:
- Ba mảng mây vẽ tay theo nét game (`home_cloud_1..3`), rải khoảng 30 bản quanh rìa bản đồ, trôi lệch pha, nhấp nháy độ trong (`HomeScene.BuildClouds`, `DriftClouds`).
- Sáng tối dùng chung hệ của các đảo (`DayCycle`, `DayNight` do phiên đảo dựng: nhuộm theo giờ máy, tia nắng); thêm đèn công trình bật khi tối (quầng `anim_glow` ở cửa sổ, lò).
- Sửa tia nắng cho mọi màn (người dùng báo 2026-11-18: kéo bản đồ thì nắng đứng yên như UI):
  - nguyên nhân: shader `PokiClash/UISunRays` tính dải theo toạ độ canvas (`IN.worldPosition`);
  - nay tính theo toạ độ của chính ảnh: `uv` nhân tỉ lệ khung ảnh (suy từ `ddx`, `ddy`), mật độ `_Bands` (mặc định 5,5 dải theo chiều cao ảnh); `_Scale` giữ lại nhưng không dùng;
  - kéo thì đi theo bản đồ, phóng to thì dải to theo;
  - đo: kéo 400 px, hai ảnh dời ngược khớp, chênh 7,6 so với 54 khi không dời;
  - phiên đảo co ảnh nắng của màn Đảo về đúng khung ảnh đảo, vì ảnh tràn rộng làm dải quá thưa.

**Hình công trình (2026-11-18)**, gen theo khung cùng cỡ ô (khoảng 90 px mỗi ô ở ảnh ra; `ArtGen/Home/buildings/make_building_refs.py`):
- tờ A: ruộng, vườn, xưởng gỗ;
- tờ B: kho, ao cá, lò rèn;
- tờ C: bếp, suối nước nóng, cối nước;
- tờ D: giếng, cây bi, ghế, xích đu;
- Nhà chính, Mỏ;
- mây.

`ArtGen/Home/import_home.py` tách nền, đo điểm neo (góc dưới chân thoi) và bề ngang chân thoi, kéo nền cho đúng 2:1, rồi ghi `Assets/03 Art/Home/*.png` và `home_art.json`. `ArtGen/Home/preview_scene.py` ghép thử màn ngoài Unity bằng đúng phép tính của `HomeScene`.

**Khoảnh đầu sửa (2026-11-18)**: ghép thử cho thấy 2 x 2 ô rừng quá chật, bến bị rừng tách khỏi làng. Khoảnh đầu nay là 7 ô rừng (thêm 3 ô ven biển tới bến), có đường đất lát sẵn từ bến lên Nhà chính (`startTiles`); `maxLots` cộng thêm 3.

**H2: cảnh Nhà trong Unity (2026-11-18)**:
- Code chạy trong game: `App/Scenes/Home/HomeScene.cs`, `HomeObject.cs`, `HomeTap.cs`. Editor: `Editor/HomeSceneMenu.cs`, menu `PokiClash/Prefab/Nhà và side meta/Nhà: dựng màn`; menu này nhập dữ liệu rồi dựng `Screens/Home.prefab` (chép từ Farm), `Items/NhaVat`, `NhaOLat`, `NhaMay`, scene `Home.unity`, Build Settings. Chạy được bằng cờ `Temp/home_build.flag`; tour chụp ảnh bằng `Temp/home_tour.flag`.
- `SceneIds.Home`. Sảnh: công trình Trang trại đổi thành Nhà (vào scene Home, chấm báo `Home.Alert`). `HubPan.SetOffset`, `AdGate.HomeSpeed`.
- Có: kéo bản đồ; ô lát; khối rừng trên ô chưa mở; công trình theo ảnh; bảng chọn (thu, giao hoặc rút tướng, nâng cấp, rút giờ bằng quảng cáo, cất trang trí); chế độ xây (khay, bóng ma xanh hoặc đỏ, chạm để dời, Đặt); chế độ lát ô; Tự xếp; Thu hết; Ra đảo; mây rìa; sáng tối; đèn đêm.
- Chưa có: thú đi lại, làm việc (H3); tan mây khi mở đất; hiệu ứng dọn rừng; hình công trình đổi theo cấp.

**Đợt sóng, cây, zoom, ô nối (người dùng dặn 2026-11-18)**:
- **Sóng vỗ bờ như đảo Thủy**: ảnh nền đảo vẽ bằng shader `PokiClash/UIInkWater` (vật liệu `Assets/03 Art/Home/home_water.mat`) kèm ảnh khoảng cách tới bờ `Assets/03 Art/Baked/Home/home_dist.png` (R = khoảng cách x 4, G = vùng vẽ sóng), sinh bằng `ArtGen/Home/make_home_dist.py`. Ảnh khoảng cách nhập dạng tuyến tính (không sRGB), không nén.
- **Cây rời đặt ngẫu nhiên** thay ba khối rừng lặp lại: 15 món ở ba tờ `ArtGen/Home/trees/tree_sheet_1..3.png` (prompt `trees.txt`, bản phác `make_tree_refs.py`), gộp atlas bằng `pack_trees.py`:
  - nhóm cây cao: thông, sồi, bách, cây đôi, thông non, bạch dương, cây tán tròn;
  - cây đặc biệt (thỉnh thoảng): cây hoa, cây cổ thụ; dừa ở ô ven biển;
  - đồ nhỏ: bụi, dương xỉ, đá, gốc cây, khúc gỗ.
  - Mỗi ô rừng 8x8 rải lưới 4x4 cây có xê dịch, lật ngẫu nhiên, cỡ lệch nhẹ, cộng 3 đồ nhỏ; hạt ngẫu nhiên theo số ô nên lần nào vào cũng giống nhau. Cây thu còn 0,85 cho cân với nhà.
  - Atlas để trong `Assets/03 Art/Baked/Home/` vì `ArtImporter` ép mọi ảnh khác trong `03 Art` về một sprite.
- **Zoom nhẹ**: thay `HubPan` bằng `LandView` của màn Đảo (kéo, hai ngón, cuộn chuột). Thu nhỏ tới mức vừa phủ màn, phóng to tối đa 1,25. Vào màn thì đặt máy giữa Nhà chính.
  - Trường trong `HomeScene` tên `landView`: đặt `view` thì trùng trường `view` của `SceneRoot`, Unity mất tham chiếu, máy kẹt góc trên trái.
- `ArtImporter` thêm luật ảnh lớn (2048) cho `Home/home_base`.

**Rừng chưa mở, thưởng dọn rừng (người dùng dặn 2026-11-18)**:
- Cây ở ô chưa mở tô tối nhẹ (nhân màu 0,8 / 0,82 / 0,78), đang dọn thì mờ thêm (`HomeScene.LockedTint`).
- Dọn xong ô rừng được **bi để thả** (bi máy bi) ngoài gỗ: vòng 1 được 15 bi, vòng 2 được 40, vòng 3 được 80 (`home.rings[].balls`). Dọn xong lúc vắng thì vào màn mới báo. Màn Nhà báo bằng toast "Đã dọn rừng: +N bi để thả" kèm tiếng, thanh trên cập nhật số bi (`HomeState.cleared`, không lưu). Test `DonRung_KeDat_KhoaCap_ThuongGo`.
- **Bong bóng bi, cây bay, gió, chim bướm (người dùng dặn 2026-11-23)**, học `pbsc_homestead_expand_bubble` và `pbfx_camp_expand_3x3` của Critters (`App/Scenes/Home/HomeScene.Forest.cs`, `HomeScene.Life.cs`):
  - ô rừng dọn được hoặc chỉ thiếu gỗ, quặng, thợ có bong bóng "icon bi +N" trên tán cây giữa ô (Critters: icon 3 viên bi + số bi thưởng); chạm bong bóng như chạm ô. Đang dọn chỉ hiện nhãn giờ còn;
  - dọn xong (hết giờ, hoặc xem quảng cáo rút giờ): cây trong khung nhìn bay lên trời lần lượt từ giữa ô ra. Mỗi cây nén xuống 0,13 giây, bật giãn dài 0,09 giây, vọt lên nhanh dần, nghiêng nhẹ, mờ hết sau ~0,85 giây. Gốc bung cụm khói kem + bụi đất (ảnh `farm_smoke`, `farm_dust`), cây to văng lá. Bi bay từ trên đầu ô lên chip bi như Cây bi. `ReportCleared` phải chạy trước lần lưu đầu sau khi dọn xong, nên nút quảng cáo và Dọn gọi thẳng vào nó;
  - gió: cây trong khung nhìn nghiêng quanh gốc 0–2,4 độ, ngả theo chiều lá bay; cơn gió là sóng chạy ngang bản đồ. Cứ 1,6–4,2 giây một cây to lắc mạnh rồi êm (0,9 giây), rụng 1–3 lá, 30% có chim vụt ra. Làm bằng xoay transform (mã chạy không được tạo vật liệu nên không dùng shader cần thêm kênh UV);
  - 5 bướm lượn quanh đất đã mở, đôi khi đậu; 4 ong bay số 8 quanh ruộng, vườn, bồn hoa, Cây bi; đàn 2–5 chim bay ngang khung mỗi 10–22 giây. Chỉ quanh khung nhìn, đêm thì tan. Ảnh vẽ bằng `ArtGen/Home/life/make_life.py` (tô phẳng, viền mực như lá gió) ở `Assets/Resources/HomeLife/`;
  - giá mở giữ nguyên (gỗ, quặng, thời gian, thợ); quảng cáo `home_speed` rút 30 phút, 3 lần mỗi ngày dùng chung với xây, nâng cấp (người dùng: dùng quảng cáo như vậy là ổn);
  - tour chụp: menu "PokiClash/Thử/Nhà và side meta/Nhà: rừng bay, gió, chim bướm (chụp)" (`Editor/HomeForestTour.cs`), ảnh ở `Temp/PokiShots/forest/`.
- **Bỏ thoi cỏ có viền dưới chân cây và công trình** cho hình hoà vào đất (`ArtGen/Home/foot_strip.py`, dùng ở `trees/pack_trees.py` và `import_home.py`; người dùng nhắc lại vì công trình vẫn còn viền):
  - đo thoi bằng cách dò từ mũi dưới lên: bề ngang tăng đều cho tới mũi trái, phải. Thoi vẽ tay cao khoảng 0,54 tới 0,59 bề ngang, không đúng 2:1;
  - loang từ nền thoi qua màu nền (nền sáng, nét chì xanh của nền) để xoá nền. Không lọc thẳng theo màu được, vì nét chì nền trùng màu rêu, lá;
  - gọt nét viền ở dải mép: điểm không thuộc thân vật (vùng màu dày) và cách thân vật quá 3 px thì xoá;
  - giữ nguyên khung ảnh để điểm neo không đổi.
  - công trình: đo neo trên thoi trước rồi mới gọt, nên `home_art.json` không đổi. Không gọt ruộng, vườn cây, xưởng gỗ, Mỏ, vì chúng tự có nền riêng trên cả chân thoi;
  - chỉ gieo loang ở nửa trước thoi. Gieo ở vành sau thì trúng lá hộp hoa cửa sổ; xoá quầng sáng thì ăn tường kem.
- Năm đồ nhỏ (bụi, dương xỉ, đá, gốc cây, khúc gỗ) gen lại không có thoi nền (`trees/small_props_nobase.txt`, Magnific GPT 2.6, 95 credit, ra `tree_sheet_3_nobase.png`). Lý do: thân nằm gọn trong thoi, lá, rêu, đá nhạt trùng màu nền, gọt là thủng.
- Cắt cây theo khối liền thay vì chia đều 5 cột (trước đây cây đôi, cổ thụ bị xén thẳng mép tán).

**Dời công trình (người dùng dặn 2026-11-18, như Critters / Clash of Clans)**:
- Ở chế độ xây (nút Xây), chạm một công trình hoặc trang trí trên đảo để nhấc lên. Công trình ẩn đi, bóng ma thay chỗ nó (xanh: đặt được, đỏ: không).
- Chạm đất để đổi chỗ, Đặt để dời, Thôi để về chỗ cũ.
- Dời không tốn gì; tướng đang giao, đồ tích, giờ xây, giờ lên cấp giữ nguyên (`Home.Move`, kiểm `CanPlace` bỏ qua chính nó).
- Khay công trình ẩn khi đang có bóng ma; bóng ma bị bảng chọn che thì máy tự kéo cho nó ra giữa (`HomeScene.StartMove`, `KeepVisible`).
- Tour chụp `9_doi`, `9_doi_xong`.
- **Chạm, nhấn giữ, kéo** (người dùng dặn 2026-11-18, học Critters và Clash of Clans; Critters dùng EasyTouch, nhấn giữ 1 giây, bộ giao diện `buildmode` có nút xác nhận, đóng):
  - chạm công trình: bảng chọn có thêm nút **Dời** (nút thứ tư);
  - nhấn giữ 0,45 giây lên công trình (cả ở chế độ thường) thì nhấc lên, có rung nhẹ, cùng ngón kéo đi theo ô lưới; bóng nhấc cao 18 px khi đang cầm, qua mỗi ô rung nhẹ;
  - thả tay thì còn Đặt / Thôi, chỗ đỏ ghi lý do; đang dời thì nhấn lên bóng là kéo tiếp;
  - `HomeTap` bắt nhấn, giữ, kéo trên mặt đất; không cầm công trình thì chuyển nguyên sự kiện kéo cho `LandView` (kéo, chụm bản đồ như cũ); đang cầm thì ngón khác không kéo bản đồ.
  - Tour dùng sự kiện chạm giả (`10_bang_doi`, `10_keo`, `10_tha`): giữ là nhấc được, kéo 4 ô kho dời đúng, kéo đất trống bản đồ trôi.

**Đảo to hơn, quái đi khắp đảo (người dùng dặn 2026-11-19)**: "chế độ home cho phép người chơi thả quái vật đi khắp map nên làm cho to ra nữa đi, cam không cần nhìn full cũng được, quái vật chỉ làm việc khi người chơi kéo nó vào chỗ làm hoặc chọn trong chỗ làm việc thôi".
- **Lưới 72 x 72** (trước là 48 x 48), vẫn 6 x 6 ô rừng nhưng mỗi ô rừng **12 x 12** ô lưới. Số ô rừng, vòng, giá dọn, `maxLots` giữ nguyên, nên tiến độ không đổi mà mỗi ô mở ra rộng gấp 2,25. Ô lát 2 x 2 (36 x 36 ô lát).
- Bản đồ 6.975 x 3.866 px. Thu nhỏ hết cỡ (0,56) chỉ thấy khoảng một phần tư bề ngang đảo, đúng ý người dùng.
- **Ảnh nền ghép** từ mảnh của nền cũ, cùng mật độ px mỗi ô nên không mờ thêm (`ArtGen/Home/base/compose_base72.py`, nguồn `home_base_48.png`, ảnh soi lưới `preview_72_luoi.png`):
  - cỏ, rừng nền, biển ghép vá (quilting), mép mềm;
  - bờ cát hai cạnh dưới lặp từ dải bờ cũ, nắn thẳng độ trôi, nối bằng đường cắt ít lệch nhất;
  - cụm vách, thác, hồ và vách phải phóng 1,5 cho vừa ô rừng 12 x 12; suối lặp dọc trục gy (nở dần ở chỗ ra khỏi hồ), cửa suối, hồ ven biển, bến giữ cỡ; mạch quặng phóng 1,25 cho vừa Mỏ 6 x 6;
  - ảnh 2.210 x 1.225, nhập 4096 (`ArtImporter`). Ảnh khoảng cách tới bờ cho sóng sinh lại bằng `make_home_dist.py`;
  - toạ độ hồ, suối đo trên mặt nạ đã ghép rồi ghi vào `balance.json`.
- **Khoảnh đầu giữa đảo** (người dùng dặn cùng ngày: "ban đầu unlock cho người chơi 1 khoảng rộng 1 chút ở giữa map"):
  - 3 x 3 ô rừng (2..4, 2..4), tức 36 x 36 ô lưới, thay cho 7 ô dải chéo xuống bến;
  - làng ở giữa khoảnh: Nhà chính (39,39), ruộng, vườn bên trái, xưởng gỗ, kho bên phải, đường đất từ Nhà chính xuống phía bến tới mép khoảnh. Bến nằm ở ô rừng (5,5), mở sau;
  - `maxLots` thêm 2 cho khớp: 11, 14, 17, 20, 24, 27, 30, 32 (tối đa 32 ô mở được);
  - vòng 1 là 16 ô quanh khoảnh, vòng 2 là 7 ô sát mép trên; không còn vòng 3;
  - mạch quặng trái dời sang ô rừng (2,5) (vòng 1, sát bờ trái) cho khỏi nằm trong khoảnh đầu;
  - bản lưu cũ cũng được mở thêm các ô khoảnh mới (`Home.Of`).
- Rìa rừng: dải cây rời sâu 6 ô ngoài hai cạnh trên (`HomeScene.SpawnRim`) nối ô rừng với rừng vẽ trên nền. Mỗi ô rừng rải lưới 6 x 6 cây và 7 đồ nhỏ. Mây rải theo px quanh mép.
- **Bản lưu cũ**: `HomeState.grid` (bản lưu thiếu khoá này là 48). `Home.Of` gặp lưới khác thì `Home.Regrid`:
  - ô rừng giữ chỉ số;
  - công trình dời theo tâm nhân 1,5; chỗ không hợp lệ thì tìm chỗ trống gần Nhà chính;
  - ô lát phủ lại đúng phần đất tương ứng.
  - Test `BanLuu48_DoiTheoTiLe`.
- **Quái đi lại** (H3), dùng lại `FarmPet` của Trang trại; cảnh chủ là giao diện `IFarmPetHost`, cả `FarmScene` và `HomeScene` đều theo:
  - tướng rảnh (tối đa 14 con: trong đội trước, rồi sao, độ hiếm) rải khắp đất đã mở, nhảy lò cò tới điểm gần trong 6 ô; không xuyên công trình, hồ, suối, ô nước (`Home.Walkable`);
  - tướng đang làm đứng trước công trình (ô 1 ngoài mặt trái, ô 2 ngoài mặt phải, ô 3 ở mũi), cử động theo việc: ruộng cuốc, vườn hái, ao rắc, bếp nhào, xưởng gỗ, mỏ, lò rèn đập búa. Hết sức thì ngồi nghiêng;
  - tướng vừa rút ra ngủ dọc mặt trái Nhà chính. Chạm thì hiện còn nghỉ bao lâu, có bánh thì có nút "Cho ăn bánh".
- **Chỉ giao việc khi người chơi làm**, bỏ nút Tự xếp:
  - kéo quái đang dạo thả vào công trình làm ra đồ (sáng xanh: nhận được, đỏ: không). Cầm tướng thì máy đứng yên, không tự trôi ở mép (người dùng 2026-11-23 báo lỗi "tap và hold tướng thì cam tự di chuyển"); công trình ngoài khung thì ngón thứ hai kéo bản đồ. Kéo trên tướng đang làm, nghỉ cũng không dời máy (`FarmPet.PassPan` tắt ở màn Nhà), thả tay là chạm;
  - hoặc chạm công trình, bấm "Giao tướng" (ô trống) hoặc "Đổi ca" (đủ người: ô mệt nhất) để mở hộp chọn tướng. Hộp này dùng lại `FarmPickerDialog.ShowHome`, có nút rút ra.
- Thứ tự vẽ: chỉ dời con nào lệch chỗ (lớp vật có hơn nghìn cây). Quái đứng trước mặt tường công trình thì vẽ sau công trình.
- Tour chụp thêm `11_quai_dao`, `12_tha_quai`, `13_chon_tuong`.
- **Bến tàu ở mũi dưới** (người dùng dặn qua phiên sảnh, 2026-11-19): chuyến tàu qua mây sảnh ↔ Nhà cập bến, rời bến ở đây.
  - Ảnh nền nới biển ở mép dưới (2.210 x 1.330, bản đồ 6.975 x 4.197 px) cho tàu đủ chỗ.
  - Bến vẽ bằng GPT 2.6 qua Magnific (95 credit), theo mẫu bến sảnh `ArtGen/Islands/sanh_moi/ben_tau/ben_tau_vung_1.png`. Vùng cắt mũi đảo, prompt `ArtGen/Home/base/ben_nha.txt`, ảnh ra `ben_nha_1.png`. `compose_base72.py` dán phần đổi theo chỗ khác ảnh gốc.
  - Cầu gỗ từ mũi đảo chạy thẳng xuống biển, cọc buộc dây bên phải, đèn lồng cuối cầu, thùng gỗ ở đầu cầu.
  - Tàu (`PierShip`, dựng bằng `ShipBuild.Pier` của phiên sảnh, con của lớp kéo) đậu bên phải cầu, mũi hướng lên; rời bến đi thẳng xuống dưới mép ảnh.
  - `HomeScene.Enter` gán `Frame` (đặt máy ngay theo tàu, `LandView.ShiftWorld`), `Glide` (máy lướt tới tàu trước khi rời), `OnTap` (về đảo).
  - Chỉ lần đầu tới Nhà bằng tàu: cập bến xong 0,4 giây thì máy lướt lên Nhà chính (cờ `HomeState.dockIntro` trong bản lưu). Từ lần thứ hai máy đứng ở bến, người chơi tự kéo (người dùng dặn 2026-11-19). Bến nằm ở ô rừng (5,5) chưa mở, nên quanh bến không cho cây mọc (4 ô).
  - Mây che rìa là từng đám rời (người dùng chê mây "lấp ló", muốn mây toả nhanh, thấy rõ thuyền): dựng sẵn trong prefab (lớp `may`, `HomeSceneMenu.BuildClouds`). `CloudRing` của phiên sảnh lo trôi nhẹ, toả quanh tàu (bán kính 290); chuyến tàu mang mây sang dải mây lúc chụp màn. `HomeScene` không dời mây nữa.
  - Mây Nhà cùng loại mây đảo (người dùng dặn): hình `Islands/land_thuy_may_1/2` xen kẽ như sảnh và dải mây chuyến tàu, cao theo tỉ lệ hình, alpha 1. Cỡ cho đều mây sảnh trên màn (rộng 380–540 px bản đồ), 150 đám xếp hai hàng so le quanh mép; hàng trong ở mép dưới chừa chỗ cuối bến.
  - Ngày đêm như sảnh:
    - thứ tự lớp trong lớp kéo: nền, ô lát, vật, hạt, mây, tàu, sáng tối, đèn;
    - mây nằm dưới lớp nhuộm và gán vào `DayNight.clouds` (nhân `DayCycle.CloudTint`);
    - biển ngoài ảnh (nền khung, hai bên) gán `seaOutside`;
    - biển trong ảnh tối về đêm qua shader sóng.
  - Chuyển cảnh nối liền như một thế giới (người dùng chê mờ dần): chuyến tàu ẩn giao diện cố định trước khi chụp màn làm nền trôi, hiện lại khi tàu cập bến. `HomeScene.Chrome` dùng CanvasGroup trên gốc giao diện `nha_ui`, mờ 0,25 giây; thế giới, quái, công trình, tàu không ẩn.

**Lưới phát sáng khi xây (người dùng dặn 2026-11-19)**: "khi xây / đặt vị trí các building phải nhìn thấy grid kiểu ánh sáng glowing".
- Shader `PokiClash/UIHomeGrid` (`Assets/03 Art/Shaders/UIHomeGrid.shader`, vật liệu `Assets/03 Art/Home/home_grid.mat`) trên ảnh `luoi` phủ cả bản đồ: nằm trên ô lát, dưới công trình.
- Nét lưới theo ô: lõi mảnh tính theo px màn, zoom nào cũng mảnh như nhau, cộng quầng mềm cộng sáng. Chỉ vẽ trên ô rừng đã mở.
- Mờ dần ra xa chỗ đang đặt: quanh chân thoi sáng nhất, xa còn khoảng 14%. Chưa cầm công trình thì cả lưới mờ 45%.
- Chân thoi công trình đang đặt / dời: phủ xanh (đặt được) hoặc đỏ (không), viền sáng phập phồng.
- Vào chế độ xây thì hiện dần trong 0,2 giây, ra thì tắt dần (`HomeScene.InitGrid`, `GridLots`, `GridGhost`, `FadeGrid`). Đã thử dáng bằng mô phỏng ngoài Unity.

## Ô lát: đất, cát, đường đá, nước (học Clash of Critters, 2026-11-18)

Người dùng dặn soi kỹ việc Critters cho đổi từng ô sang cát, đất, nước.

| Critters (bản đục) | Mình |
|---|---|
| Ô đường đất là chân thoi 2x2 ô lưới (`txui_homestead_road_muddyroad_c_13`, 200 x 102 px), mép giáp cỏ chồng thêm "môi cỏ": 13 miếng (mép đơn hai hướng, mép đôi, mép ba, tuýp cỏ góc trong `c_1..c_13`); prefab `pbsc_homestead_road_muddy_2..15` ghép các miếng theo ô hàng xóm | Ô lát 2x2 ô lưới (`home.tile`), lưới ô lát 24 x 24. Mép do code dựng theo `Home.TileMask` (8 hướng: 4 cạnh, 4 góc) nên luôn khít, chỉ cần vẽ một mẫu môi cỏ mỗi hướng |
| Ô nước kiểu ao trũng: viền cỏ, bờ đất nâu, nước xanh; 7 miếng `road_water_corner_inside/outside/line`, `up`, `down`, `middlle` (bờ trên thấy vách đất, bờ dưới không); thêm bộ `waterroad_01..23` | Nước: bờ phía xa (cạnh -tx, -ty) vẽ vách đất, bờ gần chỉ viền cỏ; mặt nước dùng shader `InkWater` |
| Nhiều bộ đường (đất, gạch xanh xám, sô-cô-la, cỏ, gạch hoa) | Đợt đầu 4 loại: đất (1 gỗ), cát (1 gỗ), đường đá (2 gỗ, 1 quặng), nước (3 gỗ, chặn xây) |

Luật (`Home.CanPaint`, `Home.Paint`, test `LatO_DatCatNuoc_MepTheoHangXom`):
- chỉ lát trên ô rừng đã mở;
- không lát lên hồ, suối, mạch quặng, không lát dưới công trình, trang trí;
- nước chặn xây;
- **đổi ô không mất tài nguyên** (người dùng dặn, giống Critters): lát đè thì hoàn đủ giá ô cũ rồi trừ giá ô mới (đủ tiền tính cả phần hoàn); xoá về cỏ hoàn đủ;
- bản lưu thêm `home.tiles`.

**Mép nối giữa các ô** (người dùng dặn: các ô khác loại phải liền nhau như Critters). Mỗi ô 2x2 ô lưới chọn miếng theo 8 ô hàng xóm (`HomeScene.RenderTiles`), 38 ảnh ở `Assets/03 Art/Home/tiles/`, sinh bằng `ArtGen/Home/tiles/make_tiles.py`:
- Thứ tự cao thấp: nước < đất < cát < đá < cỏ. Ở cạnh giáp ô cao hơn, ô thấp vẽ "môi" của ô cao chờm vào (`lip_<loại>_<cạnh>`): cỏ chờm lên đất, cát chờm lên nước…
- Góc trong: hai cạnh kề cùng loại mà ô chéo cao hơn thì vẽ túm góc (`cor_<loại>_<góc>`).
- Nước có vách bờ đất ở hai cạnh phía xa (`bank_2`, `bank_3`), bờ gần chỉ có môi.
- Ghép: nền ô trước, rồi vách bờ, môi, góc. Lưu miếng theo chữ ký hàng xóm nên chỉ dựng lại ô đổi.

Bỏ hai món "đường" kiểu trang trí cũ.

## Ngày đêm (người dùng dặn 2026-11-18)

Người dùng xác nhận thêm: **trời sáng tối đồng bộ cho mọi đảo và Nhà, đổi theo giờ thật**.

Người dùng muốn **mọi đảo, kể cả Nhà, theo giờ thật kiểu sáng tối**, có **tia nắng ánh sáng dịu nhẹ**, có **chế độ tối**. Critters cũng có ngày đêm trong nhà (`homestead_daynight`). Đề xuất, chờ duyệt:

- **Pha theo giờ máy**: bình minh 5–7 giờ, ngày 7–17 giờ, hoàng hôn 17–19 giờ, đêm 19–5 giờ; chuyển pha mượt trong khoảng 30 phút. Logic ở Core (`DayCycle`), có test.
- **Lớp màu**: một lớp phủ nhân màu trên lớp thế giới (đảo, công trình, tướng trên bản đồ), không phủ UI. Bình minh hồng cam nhạt, ngày trung tính, hoàng hôn cam ấm, đêm xanh tím sẫm nhưng vẫn đọc rõ hình.
- **Tia nắng dịu** (ban ngày, bình minh, hoàng hôn): vài dải sáng rộng xiên, mép mềm, trôi chậm, độ đậm thấp, có vân chì. Đây là lớp hiệu ứng môi trường, không vẽ vào ảnh tướng hay công trình.
- **Đêm**: cửa sổ nhà, đèn lồng, lò rèn đổi sang ảnh "đèn bật" (tô phẳng màu vàng, không quầng sáng); đom đóm, sao trên trời xa; biển tối hơn.
- **Cài đặt**: Tự động theo giờ (mặc định) / Luôn ngày / Luôn đêm, trong Sổ tay.
- Áp cho sảnh đảo lớn, màn từng đảo (vùng đất), Nhà; không áp cho màn trận.
- Cần chốt:
  - lớp màu có phủ lên tướng trên bản đồ không (luật hiện tại tướng tô phẳng, không ánh sáng);
  - đêm có đổi luật gì không (đề xuất: chỉ đổi hình, không đổi luật).
