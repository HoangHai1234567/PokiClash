# 31. Lão Mực: dealer và người dẫn đường của Bến Lữ Khách (kế hoạch 2026-11-25)

Viết 2026-11-25 đêm. Mới là kế hoạch và concept, chưa dựng rig hay viết code. Tên "Lão Mực" là tên làm việc, chờ người dùng đặt.
Concept: `ArtGen/Casino/dealer/` (trang xem `xem.html`). Kế hoạch đảo: `29_DaoCasino.md`.

## Người dùng dặn (2026-11-25)

> "lên plan chi tiết tôi muốn làm kĩ hơn từng phần, bạn nên học hỏi animation dealer của 1 vài game như cup head, vào sòng bài sẽ có dealer đứng
> và bàn ở phía mình (quan trọng phần biểu cảm, bạn có thể để dealer là 1 thằng người màu đen vẽ tay mắt vàng hơi xảo trá quỷ quyệt). Ông này
> sẽ đóng vai trò giới thiệu bạn với đảo, chỉ bạn chơi từng môn (trong ftue và tutorial, chỉ qua qua thôi, sẽ có hướng dẫn cho người chơi đọc).
> Nhân vật này trong mỗi scene sẽ có các animation khác nhau như chia bài, xoay roullete, biểu cảm mặt khi thắng, biểu cảm mặt khi thua, khi bạn
> đặt cược sẽ đặt chip lên bàn, thắng nó sẽ dùng 2 tay vơ lại. Kiểu animation kéo dài tay như hoạt hình disney những năm 1940-1980 (nghiên cứu
> kĩ cuphead)... bạn lên concept qua web tôi xem đúng ý tôi không"

## Đã chốt (2026-11-25, người dùng: "Làm theo bạn đề xuất")

1. Hướng **A** (dealer cổ điển). 2. Tên **Lão Mực**. 3. **Một gương mặt cho cả đảo**: bỏ 6 chủ quán riêng (`29` mục 2), Lão Mực dẫn mọi trò.
4. Giữ **duyên**, không thêm sừng / lửa. 5. **Diễn gian, luật công bằng**: chỉ liếc bài, nháy mắt; tỉ lệ không đổi. 6. Máy quả: **Lão Mực kéo
cần hộ**. 7. Tiếng nói: **chữ + tiếng lầm bầm vô nghĩa**.

## Tóm tắt

- Một nhân vật xuyên suốt đảo: **người mực đen vẽ tay, mắt vàng, gian xảo nhưng duyên**, thiết kế theo lối **tay chân ống cao su**
  (rubber hose) của hoạt hình đầu thập niên 1930 mà Cuphead dựng lại; vẽ bằng nét bút mực + chì màu của game, tô phẳng, không bóng.
- **Học cách diễn, không chép nhân vật**: lấy nguyên tắc chuyển động (tay không khớp uốn cong, nén giãn, lấy đà to, khung nhòe, đứng không
  bao giờ im, biểu cảm đổi bằng hình vẽ tay); không lấy thiết kế, tên, hình của nhân vật nào trong Cuphead.
- **Vai trò**: dealer ở ba lều (chia bài, quay bánh xe, kéo cần máy quả) và người dẫn đường của đảo (đón ở bến lần đầu, giới thiệu sơ qua mỗi
  trò trong FTUE; luật đầy đủ để người chơi tự đọc ở "Cách chơi").
- **Bố cục bàn**: người chơi ngồi trước bàn; Lão Mực đứng sau bàn ở nửa trên màn (từ thắt lưng trở lên), mặt bàn nửa dưới gần người xem,
  hàng nút ở dải dưới cùng. Tay dealer vươn tới đúng chỗ lá bài / chồng chip của người chơi.
- **Kỹ thuật**: rig AtomSpine (.atomik) cho thân và tay chuỗi nhiều xương co giãn + **bộ hình thay** cho mặt (mắt, mày, miệng) và bàn tay, vài
  **khung nhòe** vẽ riêng cho động tác nhanh; Unity có `DealerView` nghe sự kiện của từng trò để phát clip, đặt đích tay, hiện bong bóng thoại.
- **Mốc** D0 concept → D1 tờ thiết kế chốt → D2 rig + clip chung → D3 Blackjack → D4 Roulette → D5 Máy quả → D6 FTUE → D7 hướng dẫn các trò khác
  → D8 âm thanh, tối ưu, máy thật. Mỗi mốc có ảnh động để duyệt trước khi sang mốc sau.

## 1. Nhân vật

### 1.1. Ba hướng concept (Magnific GPT 2.6, ảnh mẫu nét: tờ nhân vật chính đã duyệt + `world_style.png`)

| Hướng | Tờ | Dáng | Hợp vai |
|---|---|---|---|
| **A. Dealer cổ điển** (đề xuất) | `huong_A_dealer_co_dien.png` | thân quả lê, chỏm mực xoăn, mắt vàng mí nặng, răng vàng, lưỡi trai xanh của dealer, nơ đỏ, gi lê đỏ rượu, nịt tay áo đỏ, găng trắng 4 ngón | chia bài, đứng sau bàn rõ vai "dealer" nhất; mặt to dễ đọc biểu cảm |
| B. Ảo thuật gia cao gầy | `huong_B_bong_cao.png` | cao lêu nghêu, mũ chóp tím cài lá bài, ngón tay đen dài như nhện, áo đuôi tôm tím, đồng hồ quả quýt | sân khấu, dẫn chuyện; khó đứng sau bàn (quá cao), tay đen khó đọc trên nền tối |
| C. Chủ sòng tròn | `huong_C_muc_tron.png` | tròn như giọt mực, hai chỏm như sừng nhỏ, kính một mắt, răng vàng, mũ fez, gi lê sọc | tham lam, vơ chip rất hợp; thân tròn ít tạo dáng tay |

Hướng A đã có thêm: tờ biểu cảm 9 mặt (`A_bieu_cam.png`), tờ 6 dáng hoạt ảnh (`A_dang_hoat_anh.png`), cảnh bàn bài nhìn từ ghế người chơi
(`A_canh_ban_bai.png`). Chọn B hoặc C thì gen lại ba tờ đó cho hướng ấy (3 × 95 credit).

### 1.2. Tính cách và lời nói

- Gian xảo, khéo mồm, mê thắng; thua thì cay ra mặt nhưng vẫn giữ phép chủ sòng ("Hừ... hên thôi!"). Vui tính, không đáng sợ.
- **Chỉ diễn gian, luật vẫn công bằng**: liếc trộm bài úp, nháy mắt, xoa tay, nhưng kết quả vẫn theo lõi (tỉ lệ công khai, không suýt trúng giả,
  `29` mục 6). Không bao giờ gạ chơi thêm, gạ nạp bi (chơi có trách nhiệm, `29` mục 8): hết lượt có thưởng thì "Hôm nay thế đủ rồi, mai ghé nhé".
- Lời thoại ngắn, bong bóng chữ (Loc), có thể kèm tiếng "lầm bầm" vô nghĩa ngắn (không lồng tiếng thật).

### 1.3. Luật hình

- Tô phẳng, nét chì sáp chỉ là vân; không mảng sáng tối, không bóng đổ, **không quầng sáng quanh mắt vàng**, không bóng loáng (luật hình tướng
  2026-11-04, luật VFX). Thân đen phẳng có vân chì mờ để không thành mảng đen chết.
- Nét viền nâu sẫm hơi rung như ảnh mẫu; viền trắng giấy xé quanh nhân vật (shader `StickerOutline`) dùng như tướng nếu đặt trên nền đông.
- Găng trắng, lưỡi trai xanh, nơ đỏ là điểm nhận diện; mắt vàng đọc rõ ở cỡ nhỏ (bong bóng góc màn).

## 2. Ngôn ngữ hoạt hình (nghiên cứu)

Nguồn: Cuphead (Studio MDHR) vẽ tay từng khung, 24 hình/giây "on the ones", mọi nén giãn là một hình vẽ lại chứ không phải co kéo hình có sẵn;
phác bút chì rồi mới đi nét. Hoạt hình ống cao su (Fleischer, Disney đầu 1930): tay chân không khớp uốn theo đường cong, thân nén giãn như không
xương, găng trắng, giày to. Nguyên tắc rút ra cho Lão Mực:

| Nguyên tắc | Làm thế nào ở PokiClash |
|---|---|
| Tay không khớp, uốn cong chữ C / S, vươn rất dài | tay là dải lưới dài trên chuỗi 8–10 xương; vươn = giãn xương (tới 2,5 lần) + IK tới đích; co về nảy quá đà (overshoot) rồi lắc |
| Nén giãn toàn thân | thân một lưới, xương hông / ngực nén giãn; đập bàn: bẹp ngang; cười: vươn cao |
| Lấy đà to trước động tác | trước khi chia: tay rút về sau đầu 0,12–0,2 s; trước khi quay bánh xe: xoắn người như lò xo |
| Theo đà, phần trễ | lưỡi trai, chỏm mực, nơ, vạt gi lê lắc trễ (lò xo); tay về sau thân |
| Khung nhòe (smear) | 1–2 hình vẽ riêng cho tay lúc búng bài, vơ chip, kéo cần (đổi attachment trong 1–2 khung) |
| Đứng không bao giờ im | idle nhún 2 phách theo nhạc lều, mắt liếc, ngón gõ bàn; chờ lâu: tung đồng xu, ngáp, huýt sáo |
| Biểu cảm bằng hình vẽ tay | mắt, mày, miệng là bộ hình thay (9–12 bộ theo tờ biểu cảm); đầu méo theo cảm xúc (lồi mắt, rớt hàm, lưỡi trai bay) |
| Nhịp vẽ tay | clip phát 12–24 hình/giây kiểu "giữ khung" (step) cho phần mặt / tay thay hình; xương chạy mượt; giữ dáng mạnh 0,1–0,25 s |
| Rõ ý (staging) | mỗi lúc một hành động chính; mắt dealer luôn nhìn về thứ người chơi cần nhìn (lá bài mới, viên bi, chồng chip) |

## 3. Bố cục scene có dealer

```
┌──────────────────────────┐
│ thanh trên (bậc cược...) │
│   nền lều (vẽ)           │
│        ┌─────┐           │  Lão Mực từ thắt lưng trở lên, cao ~45% màn,
│        │ mặt │           │  đứng giữa, sau mép bàn
│      ──┤ thân├──  tay    │
│ ═══════╧═════╧══════════ │  mép bàn sau (khay chip của dealer, bài dealer)
│     mặt bàn nỉ xanh      │  bàn chiếm nửa dưới, cong về phía người xem
│   [bài người chơi] (chip)│  ô cược của người chơi gần mép dưới
│ ──────────────────────── │
│   hàng nút (Rút, Dằn...) │  dải dưới cùng: nút, không vẽ gì quan trọng
└──────────────────────────┘
```

- Lớp vẽ (sau ra trước): nền lều → Lão Mực (.atomik) → mép bàn sau (che hông) → đồ trên bàn (bài, chip, bánh xe, máy quả: hình riêng, do game
  điều khiển) → tay dealer khi vươn ra trước bàn (lớp tay tách được lên trên đồ bàn) → giao diện.
- Tay chạm đúng đồ: game báo toạ độ màn của lá bài / chồng chip / tay quay → đổi sang toạ độ rig → đích IK của bàn tay.
- Các cảnh cũ (C7) đổi bố cục: tờ tin, Hũ bàn, bậc cược thu gọn lên thanh trên / bảng gỗ bên cạnh để chừa chỗ cho dealer.

## 4. Từng scene: clip và nhịp

### 4.1. Clip chung (mọi cảnh có Lão Mực)

| Clip | Khi nào | Nhịp, biểu cảm |
|---|---|---|
| `idle` | đứng chờ | vòng 2 s: nhún 2 phách, mắt liếc trái phải, ngón gõ bàn; mặt "nhếch mép" |
| `idle_wait` | 8 s không thao tác | ngẫu nhiên: tung đồng xu bắt lại, ngáp dài tay giãn, huýt sáo nhìn trời |
| `greet` | vào cảnh | chạm lưỡi trai, cúi chào; mặt "chào khách" |
| `talk` | có bong bóng thoại | miệng thay 3–4 hình theo chữ, tay khua theo câu |
| `bet_watch` | người chơi đặt cược (chip trượt vào ô) | mắt dõi chồng chip, xoa tay; cược to: nhướn mày "chơi lớn hả?" |
| `take` | nhà cái thắng | lấy đà, **hai tay vòng như thòng lọng vơ chip về khay**, mặt tham, khung nhòe; xong phủi tay |
| `pay` | người chơi thắng | đẩy chip về phía người chơi bằng một ngón, mặt tiếc, môi run |
| `react_win_small` | người chơi thắng nhỏ | "hừ", chép miệng, mắt lườm |
| `react_win_big` | người chơi thắng lớn (blackjack, Sao Vàng, huy hiệu) | sốc: rớt hàm, mắt lồi, lưỡi trai bay lên rồi rơi lại đầu |
| `react_lose` | người chơi thua | cười đắc thắng ngửa người, tay ôm bụng |
| `react_push` | hoà | nhún vai, chu môi |
| `grumpy` | người chơi thắng 3 ván liền | cáu, xì khói hai bên đầu, đập bàn (thân bẹp) |
| `sulk` | hết ván có thưởng của người chơi (đóng phiên) | xị mặt, lưỡi trai lệch, vẫy tay "mai ghé" |

### 4.2. Đêm Bài (Blackjack)

| Clip | Sự kiện lõi | Nhịp |
|---|---|---|
| `shuffle` | đầu phiên (hộp vô hạn nên chỉ diễn) | 1,2 s: bài vòng cung giữa hai tay dang rộng như phong cầm, gõ cạnh bộ bài xuống bàn |
| `deal` × 4 | `Blackjack.StartAs` | mỗi lá 0,28 s: rút tay về (0,08) → vươn dài búng lá (0,1, khung nhòe) → lá bay xoay đáp đúng ô → tay co nảy (0,1); thứ tự người – dealer – người – dealer (lá thứ hai của dealer úp) |
| `peek` | lá ngửa của dealer là A hoặc 10 | nhấc góc lá úp, một mắt to một mắt nheo; có blackjack: cười "ha!" rồi lật; không: huýt sáo đặt lại |
| `hit` | Rút | 1 lá như `deal` |
| `double` | Gấp đôi | nhướn mày khi chip thêm trượt vào, búng 1 lá úp ngang |
| `split` | Tách | hai tay kéo hai lá dạt ra hai bên |
| `reveal` | sang lượt dealer | lật lá úp kiểu ảo thuật (tay xoay cổ tay) |
| `draw_self` | dealer rút | mỗi lá: hồi hộp, mồ hôi khi tổng 12–16 |
| `bust_self` | dealer quá 21 | ôm đầu, mắt xoáy, rồi `pay` |
| kết ván | `Blackjack.Finish` | thắng / thua / hoà → `pay` + `react_*` hoặc `take` + `react_lose` |

### 4.3. Vòng Xoay Ngũ Hành (Roulette)

| Clip | Sự kiện | Nhịp |
|---|---|---|
| `invite` | vào bàn, chưa đặt chip | tay quạt về bàn "đặt cửa đi", nháy mắt |
| `bet_watch` | mỗi chip | mắt dõi chip; chip Sao Vàng: cười khẩy |
| `no_more_bets` | bấm Quay | vẫy tay trên bàn "hết đặt!" |
| `spin` | `Roulette.PlayAs` | xoắn người lấy đà (0,3) → tay quất quay bánh xe (khung nhòe) → búng viên bi bằng ngón cái |
| `watch` | bi chạy (2,4 s) | đầu và mắt xoay theo bi, người nghiêng theo, càng chậm càng ghé sát |
| `point` | bi dừng | chỉ vào ô ra |
| kết | thắng / thua | `take` (vơ chip thua bằng cây gạt hoặc hai tay) / `pay` + `react_*` |

### 4.4. Hội Máy Quả (Slot)

- Lão Mực đứng cạnh máy (máy quả vẽ to bên phải bàn), người chơi bấm Quay thì **ông kéo cần bằng tay vươn dài** (`pull`: lấy đà, kéo, cần bật
  lại, khung nhòe), mắt dõi từng cuộn dừng (`watch_reels`).
- Trúng đường: `react_win_small`; ba Rương: ôm đầu khi lượt miễn phí chạy liên tục; ba huy hiệu: `react_win_big` (ngã ngửa ra sau); trượt: phủi tay
  cười.

### 4.5. Các trò khác (FTUE, hướng dẫn)

Bến câu, Trường đua, Chợ đen, Hầm đấu, Quán trọ: Lão Mực **không đứng thường trực**, chỉ trồi lên góc màn (từ ngực trở lên) lúc hướng dẫn:
`pop_in`, `talk`, `point` (chỉ vào nút / vùng đang học), `thumbs_up`, `shrug`, `pop_out`. Đề xuất bỏ 6 chủ quán riêng của `29` mục 2 (bớt hình),
để Lão Mực là gương mặt duy nhất của đảo (câu 3).

## 5. FTUE và hướng dẫn

- **Lần đầu ra đảo**: thay hộp chữ "Bến Lữ Khách" hiện nay bằng cảnh Lão Mực đón ở bến (3–4 bong bóng): giới thiệu bến nghỉ chân, chỉ Tháp Máy
  Bi, chỉ Bến câu (trò mở đầu tiên), nhắc lều lữ khách ghé theo lịch.
- **Lần đầu vào mỗi trò**: 2–3 bong bóng ngắn + nút "Đọc luật" (mở Cách chơi đầy đủ); có "Bỏ qua"; không bắt buộc; ghi cờ trong `Tutorial`
  (`25_FTUE.md`, như các bước gợi ý theo lúc). Ván đầu miễn phí của bàn may rủi đi kèm lời dẫn.
- **Lời thoại mẫu** (bản Việt, có bản Anh khi làm):
  - đón: "Ồ, khách lạ! Chào mừng tới Bến Lữ Khách, chỗ nghỉ chân của mọi thám hiểm gia. Ta là Lão Mực, ở đây ai cũng biết ta."
  - Blackjack: "Rút bài cho gần 21 mà đừng quá. Quá là ta ăn hết đấy, khè khè." / "Ván đầu ta khao, thua không mất gì."
  - Roulette: "Đặt chip vào hệ, vào số, hay liều một ô. Bi dừng đâu, ta trả đó."
  - Máy quả: "Ba hình giống nhau trên một đường là trúng. Đừng hỏi ta máy có bịp không, nó thật thà hơn ta."
  - thắng / thua: kho câu ngắn ngẫu nhiên (5–8 câu mỗi loại).
  - hết lượt có thưởng: "Hôm nay thế đủ rồi. Mai ghé, ta còn khối chiêu."

## 6. Kỹ thuật

### 6.1. Hình

Luật rig của dự án (skill `pokiclash-spine-rig` mục 000, 12, 15, 22): ảnh đem rig **không nét viền**, nền một màu nhân vật không dùng
(xanh lơ #3AD0FF); viền vẽ sau cùng bằng Paint của AtomSpine khi người dùng đã chốt animation; thân một lưới liền; dáng đổi hẳn hình khối
(biểu cảm lớn) làm bằng **đổi ảnh**, không uốn lưới.

1. Chốt hướng → **tờ thiết kế chuẩn** (đứng sau bàn, chính diện hơi 3/4, tay buông hai bên) làm gốc rig.
2. **Gen liền một ảnh** dáng rig được (cách đã dùng cho tướng .atomik: một lưới liền, chỉ tách mảnh cần thiết): thân + đầu một lưới; tách riêng
   **hai tay** (dải dài để uốn), **bàn tay** (bộ 8 hình: xoè, nắm, chỉ, cầm bài, búng, vơ, kéo, giơ ngón cái), **mặt** (mắt 10 kiểu, mày 6, miệng
   10 theo tờ biểu cảm), lưỡi trai, nơ, chỏm mực (lò xo trễ).
3. **Khung nhòe** vẽ riêng: tay búng bài, tay vơ chip, tay kéo cần (2–3 hình).
4. Đồ bàn: lá bài (khung + hạng + chất hệ) đã dựng bằng code; thêm mặt lưng lá bài, chip 5 màu theo bậc, bánh xe 26 ô vẽ (xoay bằng code), máy
   quả, nền ba lều nhìn từ ghế người chơi.
5. Viền vẽ sau cùng (luật 2026-11-21): rig và clip duyệt xong mới vẽ viền ở mép thấy được.

### 6.2. Rig AtomSpine (.atomik)

- Thân: xương hông, ngực, cổ, đầu; lưới có trọng số cho nén giãn.
- Tay: chuỗi 8–10 xương mỗi tay, lưới dải; IK hai đầu (vai → bàn tay) với đích đặt lúc chạy; cho phép giãn (scale xương) tới 2,5 lần.
- Mặt, bàn tay: đổi attachment theo khoá thời gian (clip biểu cảm riêng chạy chồng lên clip thân, như lớp track 2).
- Lò xo cho lưỡi trai, chỏm mực, nơ.
- Thiếu tính năng thì thêm vào AtomSpine trước (luật "AtomSpine trước, chỉ .atomik"), không viết công cụ Unity song song.

### 6.3. Unity

- `DealerView` (một prefab dùng ở ba lều và bong bóng góc màn): hàng chờ clip, track thân + track mặt, đặt đích IK từ toạ độ màn, bong bóng thoại
  (Loc), chọn câu ngẫu nhiên theo sự kiện, khóa thao tác người chơi tới khi clip quan trọng xong (chia bài).
- Ba scene lều nghe sự kiện (đã có ở C7: chia, rút, quay, kết ván) và gọi `DealerView` thay cho dòng chữ kết quả hiện nay; diễn và lõi tách
  rời (lõi tính trước, dealer chỉ diễn theo).
- Đồ bàn thành vật thật trên bàn (lá bài bay theo đường cong tới ô, chip trượt), không chỉ hiện chữ.
- Hiệu năng: một .atomik cỡ tướng, atlas ASTC; bong bóng góc màn dùng lại cùng tài nguyên.

### 6.4. Âm thanh

Tiếng bài, chip, xúc xắc Kenney CC0 đã có (`ArtGen/Sfx/kenney/casino-audio`); thêm tiếng "lầm bầm" ngắn của Lão Mực (Magnific sfx hoặc tự ghép),
tiếng búng ngón, tiếng rớt hàm "boing" cho phản ứng.

## 7. Các mốc

| Mốc | Việc | Ra gì để duyệt | Ước lượng |
|---|---|---|---|
| **D0** | Concept: 3 hướng, biểu cảm, dáng, cảnh bàn (xong 2026-11-25) | trang `xem.html` | |
| **D1** | Chốt hướng + tên; tờ thiết kế chuẩn sau bàn; tờ biểu cảm 12, tờ bàn tay 8 | tờ soi | 0,5 ngày + chờ duyệt |
| **D2** | Tách mảnh, rig AtomSpine (thân, tay chuỗi co giãn, mặt / tay thay hình), clip chung `idle`, `greet`, `talk`, `react_*`, `take`, `pay` | ảnh động từng clip | 2 ngày |
| **D3** | Đêm Bài: nền lều nhìn từ ghế, bàn, lá bài bay, `shuffle`, `deal`, `peek`, `reveal`, `bust_self`; `DealerView` nối sự kiện | chạy thử + quay màn | 2 ngày |
| **D4** | Vòng Xoay: bánh xe vẽ xoay thật, `spin`, `watch`, `point`, vơ / trả chip | chạy thử | 1,5 ngày |
| **D5** | Máy Quả: máy vẽ, cuộn trượt dọc, `pull`, `watch_reels`, phản ứng | chạy thử | 1,5 ngày |
| **D6** | FTUE: đón ở bến, lời dẫn từng trò, kho câu thắng / thua, hết lượt | chạy thử từ bản lưu mới | 1 ngày |
| **D7** | Bong bóng góc màn ở Bến câu, Trường đua, Chợ đen, Hầm đấu, Quán trọ | chạy thử | 1 ngày |
| **D8** | Âm thanh, tối ưu, máy Android | bảng đo, quay màn máy thật | 1 ngày |

## 8. Câu cần chốt

1. **Hướng**: A dealer cổ điển (đề xuất), B ảo thuật gia cao gầy, C chủ sòng tròn, hay trộn (ví dụ thân A + kính một mắt của C)?
2. **Tên**: "Lão Mực" (đề xuất), "Ông Bóng", hay tên khác?
3. **Một gương mặt cho cả đảo**: bỏ 6 chủ quán riêng (`29` mục 2), Lão Mực dẫn mọi trò (đề xuất)?
4. **Mức "quỷ"**: giữ duyên dáng như concept (không sừng, không lửa) hay thêm nét quỷ nhẹ (chỏm như sừng nhỏ của hướng C)?
5. **Diễn gian mà luật công bằng** (đề xuất): dealer chỉ diễn liếc bài, nháy mắt, không ảnh hưởng tỉ lệ?
6. **Máy quả**: Lão Mực kéo cần hộ (đề xuất) hay người chơi tự kéo cần?
7. **Tiếng nói**: chỉ chữ + tiếng lầm bầm vô nghĩa (đề xuất), hay lồng tiếng thật?

## Tiến độ

### D1 xong (2026-11-26): bộ hình để rig

Ba lượt Magnific GPT 2.6 (285 credit), ảnh mẫu là tờ hướng A + tờ biểu cảm / tờ dáng; theo luật rig: không viền, nền một màu.
- `ArtGen/Casino/dealer/rig/L1_goc_rig.png`: toàn thân chính diện, tay buông tách thân, bàn tay mở, **mặt để trống**, nền xanh lơ.
- `L2_mat_mieng.png`: 10 cặp mắt + 10 miệng (theo tờ biểu cảm). `L3_ban_tay.png`: 10 dáng bàn tay phải (nền trong suốt sẵn).
- `cat_manh.py` cắt ra `rig/manh/` (`than.png`, `mat_01..10`, `mieng_01..10`, `tay_01..10`) và ghép thử 6 biểu cảm lên mặt trống
  (`rig/soi/D1_ghep_thu.png`): đổi bộ mắt + miệng là đủ biểu cảm, không phải vẽ lại đầu.
- Để ý: ở ảnh gốc rig đầu nhỏ hơn tờ hướng A một chút (đầu ~30 % chiều cao). Muốn đầu to kiểu tờ concept thì phóng xương đầu trong rig (không
  phải gen lại) hoặc gen lại ảnh gốc.

### D2 bản thô xong (2026-11-26): rig AtomSpine + 12 clip chung

- **Mảnh** (`rig/chuan_bi.py`): từ ảnh gốc rig tách `than` (thân + đầu + chỏm + chân, chỗ lưỡi trai che đầu tô đen lại), `luoi_trai`,
  `tay_trai` / `tay_phai` (dải tay từ khớp vai tới cổ găng; khớp vai vẫn giữ ở thân, đen chồng đen không lộ); mắt, miệng co theo đầu;
  bàn tay cùng một tỉ lệ, đo gốc cổ tay và hướng tay từ cụm đen. Ra `atom/images/` + `atom/geo.json`.
- **Rig** (`rig/dung_rig.py`, project `ArtGen/Casino/dealer/atom/`, ops trong `atom/ops/`): 35 xương `root > move > hip > chest > neck > head`
  (+ `chom1..2`, `luoi`, `mat`, `mieng`), hai chuỗi tay 8 đốt `tay_t1..8`, `tay_p1..8` + bàn tay `tay_tb`, `tay_pb`, hai chân. Thân một lưới
  (868 đỉnh, trọng số geodesic 12 xương), tay dải lưới 288 đỉnh trọng số dọc chuỗi; mặt 10 + 10 hình, bàn tay 10 + 10 hình (bên phải ảnh lật).
  Dáng gốc trùng ảnh gốc (`rig/soi/D2_setup_so.png`).
- **Clip** (`rig/hoat_anh.py`, hàm thời gian nướng 30 khung/giây, lược khoá RDP): tay mỗi khung là đường cong bậc hai vai → đích chia đều
  8 đốt theo cung, đốt dài ra khi với xa (dời xương con dọc trục cha, không dùng tỉ lệ), độ võng dương = khuỷu chìa ra ngoài; đích tay cho
  bằng toạ độ thế giới, đổi sang hệ ngực bằng động học thuận của thân. 12 clip: `idle, greet, talk, bet_watch, take, pay, react_win_small,
  react_win_big, react_lose, react_push, grumpy, sulk`; sự kiện `cham_chip, vo_xong, dap_ban, soc, tra_chip, cham_mu`.
- **Xem** (`rig/xem_d2.py`): bản sao tạm thêm mặt bàn + chip giữa thân và tay (đúng lớp vẽ trong game), ảnh động `dealer/d2/<clip>.gif`.
- `atom lint` sạch; `atom export atomik --atlas-cap 800` → `atom/export/lao_muc.atomik` (35 xương, 1.589 đỉnh). D3 nên nâng atlas-cap
  (dealer hiện ~45 % chiều cao màn).
- Chưa làm ở D2: lò xo chỏm tóc / nơ, khung nhòe, nhịp từng clip chờ người dùng duyệt; tay vẽ trước bàn trong game cần tách lớp ở D3.
- Lỡ tạo khung project rỗng ở `rig/` (`atomspine.json`, `.atomspine/`, `images/`, `export/` rỗng) do `atom init` chạy sai thư mục; chưa xoá.

### D2 bản 2 (2026-11-26): làm lại kiểu ống cao su

Người dùng chê bản thô: "bị cứng quá, không có độ mềm mại, vui nhộn của animation thời đó" và "phần trả chip khớp tay khi vươn ra còn
bị lỗi lòi 1 phần thừa ở vai". Làm lại rig và cả 12 clip; tên clip và tên sự kiện giữ nguyên. Bản 1 lưu ở `rig/ban1/`.

**Tư liệu người dùng ghi** (`ArtGen/Casino/dealer/ref/`, chỉ học nhịp và cách diễn, không chép thiết kế, không đưa khung trích vào game
hay trang công khai). Số đo (video 30 khung/giây, phim gốc 24):

- `mickeydance.mp4` (Steamboat Willie, 10,4 s, 209 hình khác nhau trên 311 khung = 19–23 hình / giây: phần lớn "on ones", các đoạn giữ dáng
  thì 2–3 khung một hình).
  - **Nhún theo phách không phải sóng sin.** Chu kỳ 10 khung (0,333 s, 180 phách / phút): dáng cao giữ ~6 hình có trôi nhẹ, rồi dập xuống
    trong 1 hình, giữ thấp ~2 hình, bật lên lại trong 1 hình (gần như hai dáng đổi nhau, không có khung trung gian).
  - Tay đang bám vật (bánh lái) thì **đầu và áo gần như đứng yên** (lệch ≤ 0,3 % chiều cao), **hông / quần sa xuống 18–25 px trên 924**
    (~2,5–3 % chiều cao, ~10 % chiều dài thân): thân giãn dài xuống, gối bạnh ra, bàn chân kia nhịp mũi (nhấc ở nửa sau phách, đập đúng phách).
  - Động tác lớn (đổi tay, 0,67 s): lấy đà 2 hình (thân nén, tay rụt) → giãn 1–2 hình (đầu kéo dài ~1,2 lần, tay vung thành chữ S, bàn
    tay rê phía sau) → giữ dáng cao 3–4 hình có trôi → vung về 2 hình có khung nhòe (bàn tay nhiều ngón) → chạm: nén quá đà 2 hình (mắt
    trợn) → ổn định 3 hình. Thân giãn / nén tới ±25 %, nghiêng ±20 độ.
- `cupheadfinalboss.mp4` (boss kéo dài hai tay ra ngoài camera rồi đập lại, 7,3 s). Số khung từng pha (30 khung/giây):
  - cuộn lấy đà 14 khung (0,47 s): tay chữ W ngửa bàn tay 8 khung, rồi cuộn cao hơn 6 khung (vai nhún, đầu thụt, thân nén);
  - bắn ra 3 khung (0,1 s): khung 1 ống còn chùng lượn sóng, khung 2 căng thẳng và **thon nhất (~60 % bề dày)**, khung 3 nhả về ~75 %;
    không có hình nhòe riêng: chính "chùng rồi căng" là khung nhòe; thân dập xuống khi tay bắn ra;
  - giữ ngoài khung 21 khung (0,7 s, báo trước cho người chơi né), thân run;
  - đập vào 4–5 khung (0,13–0,17 s) ngang màn hình, bàn tay nghiêng ngón đi trước, to;
  - chạm: bàn tay **bẹp còn ~55 % bề ngang** đúng khung chạm, nhả về ~70 % trong 2 khung, giữ 10 khung (0,33 s), vòng sóng xung kích là VFX;
  - rút tay 3 khung (ngón rê), tay còn duỗi ngang thêm 10 khung, rồi thu về 3 khung thành hai bụng sóng chùng; ổn định có vượt quá
    (đầu vươn ~8 % trong 3 khung) 0,15–0,2 s.
  - Dùng cho `take`, `grumpy`, `pay`; D3 dùng tiếp cho chia bài (búng lá = cuộn 2–3 khung + bắn 3 khung) và quay bánh xe (xoắn người
    lấy đà ~0,3–0,45 s rồi quất 3 khung, giữ dáng vươn 0,2 s).

**Mảnh** (`rig/chuan_bi.py`): thân **không còn mẩu tay nào** (bản 1 giữ "khớp vai" ở thân: tay vươn hướng khác thì mẩu đó đứng lại, đó là
phần thừa ở vai); ống tay **dựng lại bằng mã** (dải thẳng đều rộng 49 px, hai đầu chỏm tròn, vân chì lấy từ vùng đen sạch của mặt), gốc
ống là chỏm tròn nằm trong thân dưới cánh nơ; **nịt tay áo** tách thành mảnh cứng (tay giãn nịt không dãn theo); **nơ** tách riêng, vẽ
trước tay (che gốc tay như ảnh gốc), chỗ nơ che tô đen lại; đỉnh đầu dưới lưỡi trai tô tròn (lưỡi trai bay lên không lộ chỗ vát); khử
viền xanh quanh mắt / miệng (vòng xám quanh mí).

**Rig** (`rig/dung_rig.py`, 65 xương, 11 slot, 1.811 đỉnh, .atomik bản 3 nên runtime hiện tại của game đọc được):
- `root > move > hip > bung > nguc > vai > neck > head`: sống lưng 4 đốt (cong chữ C, chữ S); nén giãn bằng **dời đốt** dọc trục;
- `hip_d, bung_d, nguc_d, vai_d`: "xương da" (con của từng đốt, cùng chỗ) mang lưới thân; phình / bẹp bằng tỉ lệ ngang của chúng nên
  **không lây sang tay và đầu** (bản 1 nén thân bằng tỉ lệ `hip` làm méo cả chuỗi tay);
- `head > chom1 > chom2 > chom3`, `mai`, `luoi > luoi2`, `mat`, `mieng`; `vai > no > no_t, no_p`;
- `vai > tay_t1..8 > tay_tb` (và `_p`): ống tay 8 đốt, giãn bằng dời đốt con; `tay_t1d..9d` là xương da của ống (thon lại bằng tỉ lệ ngang);
- `hip > dui > ong > ban`: chân, bàn chân ghim đất bằng IK tính lúc nướng.
- Trọng số do script tính, **B-spline bậc hai dọc mỗi chuỗi** (giữa đốt 0,75 + 0,125 hai bên, ở khớp 0,5 / 0,5; với kiểu này ống giãn
  đều tuyệt đối), đặt bằng chuỗi `att.weight ... mode=set`. Lớp vẽ: thân, miệng, mắt, lưỡi trai < (bàn) < tay, nịt, nơ, bàn tay.

**Động cơ** (`rig/dong_co.py`, nướng 30 khung/giây, mô phỏng 60 Hz):
- nhịp nền `pulse` theo số đo Steamboat (dập 14 % phách, giữ, bật vượt 26 %, trôi), một phách 0,5 s (120 phách / phút);
- tay = đường cong bậc ba vai → bàn tay; chùng thì phình cung cho đủ dài, căng thì giãn và thon theo `giãn^-0,42` (kẹp 0,56–1,06);
  đổi dáng bằng **trộn điểm đường cong** của các dáng (không trộn thông số); mỗi nút dọc ống thấy vai / bàn tay trễ dần (sóng chạy dọc
  ống 0,11 / 0,09 s) + hai dạng sóng lò xo (nửa sóng, trọn sóng); nếp gập quá 62 độ được làm trơn thành vòng; bàn tay rê theo đà; bàn
  tay với xuống bàn thì to dần theo độ sâu (ở ô cược tạm hiện nay ~1,2–1,5 lần);
- phần trễ (chỏm tóc, tóc mai, lưỡi trai, vành, cánh nơ): lò xo góc do gia tốc của gốc xương kéo;
- clip một lần: chạy đà 2 s bằng idle, hai đầu hoà vào idle giây 0 (góc hoà theo đường ngắn nhất). `rig/kiem.py` in lệch cuối so
  với idle giây 0: 0,00 ở mọi clip.
- Hằng số tạm chờ D3: `TABLE_Y = 500` (mép bàn sau, thế giới rig), `CHIP = (0, 120)` (ô cược), `TRAY_Y = 460` (khay nhà cái) ở đầu
  `hoat_anh.py`; đích tay nướng sẵn theo các mốc này, D3 chốt bố cục bàn thì sửa rồi chạy lại `hoat_anh.py`.

**Clip** (`rig/hoat_anh.py`; mọi clip dài bội số 0,5 s, idle là dáng hai tay tì mép bàn):

| Clip | Dài | Diễn | Sự kiện |
|---|---|---|---|
| `idle` | 4,0 lặp | nhún theo phách, đổi bên mỗi phách, khuỷu bạnh ra lúc dập, bụng rung trễ, đầu lắc ngược pha; liếc trái (1,0) liếc phải (1,5), chớp mắt (0,55; 2,62), tay phải gõ bàn ở 2,5 / 3,0 / 3,5 | |
| `greet` | 2,0 | nhún 0,14 → bật, tay vòng lên kẹp vành lưỡi trai (0,38) → nhấc lưỡi trai, nháy mắt, cúi → vẫy → về | `cham_mu` 0,42 |
| `talk` | 2,0 lặp | khẩu hình 12 hình / giây, đầu gật, tay phải khua số 8 | |
| `bet_watch` | 2,0 | giật mình vươn lên → chồm xuống ngó chip → xoa tay 5 lần / giây, liếm mép → về | |
| `take` | 3,0 | cuộn chữ W 0,40 → bắn ra ngoài khung 0,42–0,52 → giữ, run → đập vào 0,80–0,92, bàn tay bẹp → giữ 0,25 → vơ về khay 1,2–1,7 (hai vòng thòng lọng) → thu tay thành sóng → phủi tay → về | `cham_chip` 0,92, `vo_xong` 1,7 |
| `pay` | 2,5 | né người, mặt xị → tay vòng cung lớn ra ngoài, ngón trỏ đặt lên chip ở khay 0,6 → đẩy khựng hai lần tới ô cược 1,3 → búng → thu tay → thở dài | `tra_chip` 1,3 |
| `react_win_small` | 1,5 | giật → chống nạnh, quay mặt, mắt cáu rồi lườm, chép miệng hai cái | |
| `react_win_big` | 2,5 | nén 0,07 → bật 0,1: đầu giãn 24 %, mắt lồi, rớt hàm, tay tung lên, lưỡi trai bay 190 px rồi rơi lại 0,86 → run → xìu, choáng → gượng lại | `soc` 0,1 |
| `react_lose` | 2,0 | khom → ngửa người cười, tay ôm bụng, bụng / vai rung 4,5 nhịp / giây → dứt | |
| `react_push` | 1,5 | nhún → vai dựng, đầu thụt, ngửa hai bàn tay, chu miệng → thả | |
| `grumpy` | 2,5 | giơ nắm tay 0,34, run → nện 0,46–0,56: thân bẹp 24 %, lưỡi trai nảy, nắm tay nảy lại → gồng run, dằn thêm 1,2 → xả | `dap_ban` 0,56 |
| `sulk` | 2,5 | rũ, đầu nghiêng, lưỡi trai lệch → thở dài → vẫy uể oải → về | |

**Xem** (`rig/xem_d2.py` + `rig/khung.mts`): 30 khung/giây, khung nhìn cố định (`khung.mts` gọi thẳng `renderFrame` của lõi AtomSpine
với hộp thế giới; `atom sheet` tự co theo hình nên clip có tay ra ngoài khung bị thu nhỏ). Bàn, khay, chồng chip chỉ có ở bản sao tạm.
Ra `dealer/d2/<clip>.gif`, `<clip>_to.png`, khung lớn `d2/lon/`. Trang `xem.html` mục "D2 bản 2".

**Xuất**: `atom lint` sạch (`ok lint: no issues`); `atom export atomik --atlas-cap 1200` → `atom/export/lao_muc.atomik` 2.075 KB
(2.124.570 byte; bản 3; 65 xương, 11 slot, 47 hình, 1.811 đỉnh, 2.358 tam giác, 12 clip, 38.538 khoá, atlas 704 x 2040, ~627 KB ASTC
6x6). JSON khoá nén chỉ ~190 KB; phần nặng là ảnh atlas (vân chì khó nén PNG; bản 1 xuất `--atlas-cap 800` nên nhẹ hơn).

**Đã tự soi**: tờ khung liên tiếp (30 khung/giây) của cả 12 clip; khung lớn vùng vai ở dáng duỗi xa nhất của `pay` (0,7; 1,3), `take`
(0,3; 0,5; 1,0), `react_win_big` (0,3), `greet` (0,6), `grumpy` (0,4; 0,6): không còn mẩu thừa, tay chui ra từ dưới cánh nơ; khung xen
60 khung/giây (giữa hai khoá) ở các chỗ tay vung nhanh nhất của `take`, `greet`, `react_win_big`, `grumpy`: nội suy liền, bàn tay
không quay ngược vòng (lần soi này bắt được hàm vượt đích làm tay "dịch chuyển tức thời" ở khung đầu, đã sửa). Chưa xem được chuyển
động ở tốc độ thật (chỉ soi dải khung), chưa chạy trong Unity.

**Còn lại / đề xuất**:
- chờ người dùng duyệt nhịp từng clip; chưa vẽ viền (luật: viền sau khi chốt animation);
- miệng `mieng_08` (nét nhếch mép nâu sẫm) chìm trên mặt đen nên không dùng; muốn có "nhếch mép" thì gen lại một miệng nét sáng;
- khung nhòe vẽ riêng chưa cần (ống chùng → căng + bàn tay rê đã thay); nếu muốn kiểu "bàn tay nhiều ngón" của Steamboat thì gen 1–2 hình;
- đầu vẫn nhỏ hơn tờ concept (chưa đổi); `idle_wait` và các clip riêng từng trò để D3 trở đi;
- trong game: tay phải vẽ ở lượt sau mặt bàn (slot `tay_trai`, `tay_phai`, `nit_*`, `no`, `ban_tay_*`), thân ở lượt trước; khung điện
  thoại hẹp hơn ảnh duyệt (tay chữ W của `take` rộng ±430) nên D3 cần canh cỡ.

### D2 bản 3 (2026-11-26): tay là ống chắc, sửa 4 clip

Người dùng xem bản 2 (ảnh chụp từ `xem.html`):

> take: "nhìn hơi lố, vòng tay vừa thôi là được không cần tràn ngoài cam như vid đâu"
> grumpy: "đập bàn cổ tay xoay 90 độ chứ không ai đấm thẳng đầu ngón tay xuống bàn cả"
> sulk: "phần mũ bị lỗi, cánh tay cảm giác như sợi chỉ, lỏng lẻo quá"
> talk: "phần này tay cũng lỏng lẻo"
> chung: "điểm lỗi chung phần cánh tay gần vai nhìn bị lỏng lẻo quá, hơi giống 1 sợi chỉ hơn là mềm mại"

Bài học: **mềm không phải là lỏng.** Tay ống cao su là một ỐNG có bề dày, cong thành một cung gọn; võng xuống, thon mảnh, lượn sóng từ
gốc vai thì thành sợi dây.

**Động cơ** (`rig/dong_co.py`, mọi clip cùng hưởng):
- bề dày ống `ARM_THICK = 1,16` lần ảnh gốc (~57 px); kéo căng chỉ thon theo `giãn^-0,25`, kẹp 0,82–1,10 (tức không dưới 95 % ảnh gốc;
  bản 2 thon tới 56 %);
- độ chùng `minlen` 0,92 → 0,80: tay gần thì ống dồn ngắn và phình ra thay vì thòng xuống;
- hàm `firm(u)`: ba đốt gần vai bằng 0 (bắp tay bám theo vai, không trễ, không lượn), tăng dần tới cẳng tay; sóng trễ và hai dạng sóng
  lò xo đều nhân với nó; độ nảy giảm (0,5 → 0,34, biên độ 60 / 34 → 40 / 22 px);
- lò xo cả lưỡi trai giới hạn 9 → 4 độ (mũ phải bám đầu); thêm `hrate` (tần số lò xo xoay bàn tay, mặc định 6,5 Hz) để cú nện xoay kịp.

**Clip**:
- `take` (3,0 → **2,5 s**; `cham_chip` 0,92 → **0,54**, `vo_xong` 1,7 → **1,3**): bỏ đoạn bắn tay ra ngoài khung và vòng thòng lọng. Mạch
  mới: cuộn chữ W 0,02–0,28 (cuộn cao thêm tới 0,42) → vươn thành một cung chụp xuống hai bên chồng chip 0,42–0,54 (đỉnh cung ~ x ±360,
  khung nhìn ±480), bàn tay bẹp lúc chạm, giữ tới 0,8 → quơ về khay 0,84–1,3 → phủi tay 1,5–2,0 → về bàn.
- `grumpy`: nện bằng **cạnh nắm tay**: cổ tay xoay 90 độ ở 0,44–0,52, cẳng tay và nắm tay nằm ngang chĩa vào trong, mép dưới nắm tay chạm
  bàn (`out=-18, inn=186, hrot=182`). Hình `tay_03` xoay ngang đọc được là nắm tay nhìn nghiêng (bốn nếp ngón xếp dọc, ngón cái phía
  trước) nên **không gen thêm**; nếu sau này cần hình khác thì đổi hằng `HAND_FIST_SIDE` ở đầu `hoat_anh.py`.
- `sulk`: lưỡi trai xoay 17 → 7 độ, dời (−10, −12) → (−4, −5), vành cụp 12 → 20 độ: lệch mà vẫn bám đầu (xương `luoi` có chốt ở bên phải
  đầu nên xoay nhiều thì đầu đai bên trái nhấc khỏi đầu ~57 px, đó là "mũ bị lỗi"). Tay vẫy bằng cổ tay (±34 độ), cổ tay chỉ lắc ±16 px.
- `talk`, `sulk`, cuộn chữ W của `take`: tay giơ có "khuỷu" (`out=-64, inn=82..86`): bắp tay rời vai chếch xuống ngoài, cẳng tay dựng
  lên; đích tay gắn theo vai (`space="v"`) nên không trượt khi thân nhún.
- 8 clip còn lại không đổi dáng, chỉ hưởng ống tay mới; đã soi lại tờ 10 khung của cả 12 clip.

**Xuất**: `atom lint` sạch; `lao_muc.atomik` 2.060 KB (2.109.024 byte), 65 xương, 1.811 đỉnh, 12 clip, 34.799 khoá; `kiem.py`: lệch cuối
so với idle giây 0 là 0,00 ở mọi clip. Không dùng credit Magnific.

**Đã soi** (khung lớn `dealer/d2/lon/`): `take_f009` (chữ W), `take_f017` (chạm chip), `take_f021` (giữ), `take_f033` (đang quơ);
`grumpy_f017` (khung nện), `grumpy_f018` (thân bẹp); `sulk_f036` (nghiêng đầu nhiều nhất); `talk_f034` (tay cao nhất); `idle_f003`,
`idle_f010` (đoạn tay gần vai). Vẫn chưa xem chuyển động ở tốc độ thật, chưa chạy trong Unity.

### D2 bản 4 (2026-11-26): sửa hướng bàn tay

Người dùng xem bản 3 (ống tay không bị chê nữa; sai hướng bàn tay ở 4 chỗ):

> grumpy: "lòng bàn tay phải hướng vào trong"
> tay đặt trên bàn: "mọi động tác tay đặt trên bàn như này, ngón cái tức ngón ngắn nhất phải ở gần người, ngón út ở phía người chơi"
> pay: "phần dùng tay đẩy chip cũng vậy, lòng bàn tay phải hướng vào trong"
> take: "phần vơ chip này bàn tay tôi chưa hiểu là làm gì, bạn có thể làm thành 2 bàn tay dựng dọc nối với nhau, ngón cái ở trên, lòng
> bàn tay hướng vào trong kiểu đang tạo thành hình mái nhà khép kín để vơ chip"

Luật hướng bàn tay đã ghi thành skill `animation-humanoid` mục 1. Bài học: thiếu dáng bàn tay nhìn nghiêng thì đừng xoay hình nhìn
trước 90 độ thay vào (bản 3 làm thế cho cú nện: đọc ra lòng tay quay về camera).

**Hình mới** (1 lượt Magnific GPT 2.6, 1k, **80 credit**, ảnh mẫu là tờ bàn tay L3; không viền, nền xanh lơ): `rig/L4_tay_nghieng.png`,
hai bàn tay nhìn nghiêng từ phía mu, cổ tay bên trái, chĩa sang phải, ngón cái ở mép trên, mép ngón út phẳng như tì bàn:
- `tay_11`: bàn tay MỞ dựng đứng (ngón khép, ba nếp gân trên mu) → hằng `HAND_BLADE`;
- `tay_12`: NẮM tay dựng nghiêng (ngón cái gập trên ngón trỏ, không thấy đầu ngón cuộn) → hằng `HAND_FIST_SIDE`.
`chuan_bi.py` cắt tờ L4 (`cut_side_hands`), co cho bàn tay mở dài bằng `tay_09`, ghi `manh/tay_11.png`, `tay_12.png`; bộ tay giờ 12
hình mỗi bên (`geo.json` có `n_hand`), `dung_rig.py` đọc theo đó. Bản đầu gen ra đúng hướng ngay, không phải gen lại.

**Sửa rig**: `tay_09` (tay úp) trên tờ L3 vẽ ngón cái ở mép dưới nên đặt lên bàn thì ngón cái rơi về phía người chơi; `chuan_bi.py` lật
dọc ảnh này ngay khi cắt, mọi clip dùng tay úp đều có ngón cái ở mép trên (phía bụng Lão Mực), cả hai tay.

**Clip** (nhịp và giờ sự kiện giữ như bản 3):
- tay úp trên bàn (`on_table`, dùng ở idle và đầu / cuối mọi clip, tay trái của greet, talk, pay, sulk): hưởng `tay_09` đã lật;
- `react_win_big`: dáng tay rũ đổi từ `tay_02` thõng ở mép bàn sang tay úp chĩa vào giữa, dạng rộng hơn dáng nghỉ (cùng luật);
- `grumpy`: dùng `tay_12` suốt clip; nắm tay nằm ngang chĩa vào giữa, ngón cái ở trên, cạnh ngón út chạm bàn, camera thấy mu nắm tay;
- `pay`: bỏ ngón trỏ chỉ xuống; `tay_11` nằm ngang chĩa vào giữa, mép ngón út tì bàn ngay sau chồng chip ở khay, gạt cả chồng tới ô
  cược (khựng hai lần, hất cái cuối như cũ);
- `take`: hai `tay_11` chĩa chéo xuống giữa (±38 độ), đầu ngón chụm nhau ở phía người chơi, cổ tay ở phía Lão Mực, chồng chip nằm
  trong lòng; kéo cả "mái" về khay (lúc tới khay hai tay ngả ngang hơn, ±20 độ). **Chú ý hướng mái**: nhìn từ phía Lão Mực là chữ Λ,
  còn trên màn hình (camera ở ghế người chơi) là chữ V ôm chồng chip. Làm thế vì tay nối từ vai xuống và mái phải khép ở phía người
  chơi thì kéo về mới mang được chip theo; nếu người dùng muốn đỉnh mái quay lên trên màn hình thì phải đổi lại (chờ xác nhận).

**Xuất**: `atom lint` sạch; `lao_muc.atomik` 2.160 KB (2.211.336 byte), 65 xương, 11 slot, 51 hình, 1.827 đỉnh, 12 clip, 34.728 khoá,
atlas 1224 x 1216; `kiem.py`: lệch cuối so với idle giây 0 là 0,00 ở mọi clip.

**Đã soi** (khung lớn `dealer/d2/lon/`): `idle_f010` (hai tay úp); `pay_f021` (tay chạm chồng chip ở khay), `pay_f036` (đang gạt);
`take_f018` (mái úp quanh chip), `take_f033` (đang kéo về); `grumpy_f017` (khung nện), `grumpy_f019` (thân bẹp); `react_win_big_f042`
(tay rũ); và tờ 10 khung của cả 12 clip. Chỗ tay chạm bàn khác đã rà: chỉ còn dáng tay rũ của `react_win_big` (đã sửa). Vẫn chưa xem
chuyển động ở tốc độ thật, chưa chạy trong Unity.

### D3 bản đầu (2026-11-26): lều Đêm Bài có Lão Mực chạy trong game

Người dùng: "quét update mới, làm tiếp phần đảo casino". D2 bản 4 chưa có lời duyệt; câu "mái nhà V hay Λ trên màn" vẫn để như bản 4
(chữ V ôm chồng chip) chờ xác nhận.

**Hình** (`ArtGen/Casino/dealer/d3/`, README trong đó; Magnific GPT 2.6 1k high, ảnh mẫu là cảnh bàn `A_canh_ban_bai.png` + `world_style.png`;
95 + 95 + phóng classic 2k 72 = **262 credit**):
- nền lều nhìn từ ghế người chơi, dọc 9:16, không dealer, nỉ trống, khay chip 4 chồng ở mép bàn sau; tách thành **nền** (cả ảnh) và **lớp bàn**
  (vành bàn + khay + nỉ) theo mép trên nét mực đo tay (`tach_lop.py`), Lão Mực đứng giữa hai lớp;
- tờ đồ bàn: lưng bài, mặt bài trắng, cỗ bài, 4 chip, 2 chồng chip (`cat_do_ban.py`).

**Bố cục** (sân khấu 1080 x 1920 dưới `Canvas/Nen`, phủ màn bằng tỉ lệ `max(rộng / 1080, cao / 1920)`): ảnh nền rộng 1080, mép trên ở y −150 nên
mép bàn sau ở y −1000; Lão Mực tỉ lệ 0,79, gốc rig ở y −1395. Chọn đúng tỉ lệ này thì ô cược `CHIP` (0, 120) và khay `TRAY_Y` của clip D2 rơi đúng ô
cược (y −1300) và khay chip trên ảnh: **không phải nướng lại `take` / `pay`**. Hàng bài dealer y −1140 (0,9 lần), bài người chơi y −1475 (1,3 lần),
cỗ bài (330, −1092) bên phải khay. Bậc cược ở trên; tờ tin thu thành bảng nhỏ bên trái, Hũ bàn + Cách chơi + Gợi ý bảng bên phải; dòng chế độ
trên hàng nút.

**Rig** (`rig/`): slot **`la_cam`** (lưng bài trên xương `tay_pb`, vẽ sau bàn tay) thêm bằng `them_la_bai.py` (và trong `dung_rig.py` cho lần dựng
lại); khoá `p["card"]` trong `dong_co.py`. 5 clip mới ở **`clip_d3.py`** (hoat_anh.py nạp), mọi clip hoà về idle giây 0 (`kiem.py`: lệch 0,00):

| Clip | Dài | Diễn | Sự kiện |
|---|---|---|---|
| `deal` | 1,0 | tay phải nhón lá ở cỗ bài (kẹp, lá hiện trên tay) → rút về cạnh vai lấy đà → búng về phía người chơi, lá rời tay → bàn tay xoè quá đà → về | `bung` 0,36 |
| `deal_self` | 1,0 | nhón lá → vòng tay đặt lá xuống hàng bài trước bụng → vỗ nhẹ → về | `bung` 0,38 |
| `peek` | 1,5 | chồm tới, kẹp góc lá úp, nháy một mắt, miệng méo hồi hộp | |
| `reveal` | 1,0 | tay tới lá úp, kẹp → xoay cổ tay hất (lá lật) → bàn tay xoè "ta-da", mắt cười | `lat` 0,38 |
| `bust_self` | 2,0 | giật mình mắt lồi, há hốc → khuỷu chìa ngang, hai tay giơ hai bên đầu, lắc đầu → buông tay | |

`bust_self` bản đầu nén thân 9 % làm mặt tụt sát nơ, ống tay đi từ vai lên che mặt; đã giảm nén, cho tay có khuỷu chìa ra ngoài, hạ bàn tay
xuống ngang thái dương (lượt chụp đầu thấy tay giơ cao chạm bảng nút bên phải). `reveal` có
cú xoay cổ tay 160 độ / khung lúc hất lá (cố ý, cùng cỡ cú quất ở `take`, `grumpy` của D2). Xuất `lao_muc.atomik` 65 xương, 12 slot, 17 clip, 2.234 KB,
atlas 992 x 1512 (`--atlas-cap 1200`).

**Unity**:
- `Game/Casino/DealerRig.cs` (nạp `.bytes` bằng `AtomikFile.Load` như rương máy bi, một `AtomikState`, hàng chờ clip một lần → idle, sự kiện,
  `BoneWorld`) + `DealerLayer.cs` (Graphic uGUI dựng lưới một phần slot): **hai lớp vẽ dùng chung một tư thế**, lớp sau (thân, mặt, lưỡi trai)
  dưới mặt bàn, lớp trước (ống tay, nịt, nơ, lá trên tay, bàn tay) trên đồ bàn. `AtomikGraphic` của gói chưa tách slot được nên viết riêng.
- `BlackjackScene` viết lại phần diễn: lõi vẫn tính trước cả ván, màn **diễn lại theo thứ tự lõi** (`Sync`): chồng chip cược trượt lên ô cược → chia
  p-d-p-d (lá dealer thứ hai úp; mỗi lá chờ sự kiện `bung` rồi bay từ bàn tay Lão Mực theo cung, xoay, đáp nảy, lật) → `peek` khi lá ngửa là A / 10
  (lá úp nhấc theo tay) → lá rút → tách (lá thứ hai bay sang tay 2) → `reveal` → dealer rút (`deal_self`; quá 21 thì `bust_self`) → tiền: thắng thì
  `pay` (chồng chip thắng bám bàn tay từ khay ra tới sự kiện `tra_chip`), thua thì `take` (chồng chip bám giữa hai bàn tay từ `cham_chip` tới
  `vo_xong` rồi vào khay), hoà thì chip trượt về; rồi `react_*`, thắng 3 ván liền `grumpy`, hết ván có thưởng `sulk`. Rig thiếu clip nào thì
  màn tự lùi về cách cũ (lá bay từ cỗ bài), không kẹt.
- Bong bóng thoại cạnh đầu: câu chào / ván miễn phí / ván tập lúc vào lều, "Quá 21 rồi, khè khè!", kho câu thắng / thua / hoà, "Chơi lớn hả?"
  (bậc cược 3 trở lên kèm `bet_watch`); 19 câu có bản tiếng Anh (`d3/loc_d3.py`).
- Lượt chụp `Editor/CasinoDealerTour.cs` (cờ `Temp/casino_bj_dealer_tour.flag`): khoá nhịp 20 khung / giây (`Time.captureDeltaTime`), chụp mọi
  khung một ván miễn phí và các ván có cược tới khi có cả thắng lẫn thua; `d3/lam_gif.py` ghép `d3/van_bai.webp` (WebP động; GIF cùng độ dài
  nặng ~60 MB nên chỉ xuất khi thêm `--gif`, không vào git).
- **Đã soi** (lượt hai, 915 khung, 46 giây game, khung 617 x 1235): ván miễn phí (dealer rút 5-7-10 quá 21 → `bust_self` → `pay` chồng chip xanh
  bám bàn tay từ khay ra), ván thắng có cược (`pay`, `react_win_small`), ván thua (người chơi quá 21 → `take`: hai bàn tay dựng thành chữ V quây
  chồng chip đỏ kéo về khay → `react_lose`); lá trên tay ở cú búng; lá dealer thứ hai úp rồi lật ở `reveal`; `peek` khi lá ngửa là A.
  Sửa sau lượt đầu: bài người chơi to 1,3 lần và lên gần ô cược (bản đầu nhỏ, nằm quá xa dưới đáy), bài dealer 0,9; lá Lão Mực tự đặt chỉ lượn
  nhẹ, không xoay vòng; nhãn số bi cược sang trái chồng chip (chồng chip thắng đè lên nhãn). Lượt ba (1.226 khung) soi lại: tay của
  `bust_self` ngang thái dương, không chạm bảng nút; nhãn số bi bên trái chồng chip. `d3/van_bai.webp` ghép từ lượt này (rộng 360).

**Mở hết lều khi chưa phát hành** (người dùng 2026-11-26: "sao các lều roulette, blackjack... tôi không vào được, đều ghi là không mở", rồi "cứ để
mở các event đi, đã phát hành đâu"): lều đóng là đúng lịch (mốc `anchor` 2026-11-23, hôm nay 26/11 là ngày nghỉ giữa Đêm Bài 23–25/11 và Vòng
Xoay 27–29/11; lều còn cần cấp 20). Thêm `Casino.TestAllBooths` (lõi, mặc định tắt, không lưu): coi cả ba lều đang dựng hôm nay (dùng sự kiện
vòng lặp của từng lều, khách mời như lần mở kế) và mục lều đã mở (bỏ mốc cấp). **`App.cs` bật lúc mở game**, nên trong Editor lẫn trên điện
thoại cả ba lều luôn mở. `Editor/CasinoTestBooths.cs` tắt lại khi về Edit mode (Play tắt Reload Domain) để `CasinoTests` chạy theo lịch thật.
**Trước khi phát hành phải xoá dòng đó trong `App.cs`** để lều theo lịch.

### D3 phần hai (2026-11-26): xoè bài, tách, gấp đôi, rút hồi hộp, chip theo bậc

Người dùng: "giữ chữ V, làm tiếp phần còn lại của D3" (vơ chip: hai bàn tay thành chữ V ôm chồng chip trên màn, giữ như bản 4).

**Rig** (`rig/them_d3b.py` thêm vào project đang có; `dung_rig.py` cho lần dựng lại): 7 lá `xao_1..7` (xương con của root, hình lưng bài,
slot vẽ trên ống tay, dưới bàn tay) và 2 giọt mồ hôi `mo_hoi_1..2` (xương con của head ở hai thái dương, giọt nước tô phẳng xanh nhạt viền nâu
vẽ bằng mã, không điểm sáng). Động cơ (`dong_co.py`) nhận `p["xao"]` là hàm của vị trí / góc hai xương bàn tay vừa giải (lá bám đúng lòng bàn
tay mỗi khung) và `p["sweat"]`. 74 xương, 21 slot, 21 clip, 2.271 KB.

| Clip | Dài | Diễn | Sự kiện |
|---|---|---|---|
| `shuffle` | 2,5 | tay phải nhấc cỗ bài trên nỉ → hai tay nâng trước ngực → bài bắn thành vòng cung từ tay phải sang tay trái từng lá (lò xo) → khép, gõ cỗ bài xuống mép bàn → tay phải đặt cỗ bài về chỗ cũ | `nhac_bai` 0,26, `go_bai` 1,66, `dat_bai` 2,05 |
| `split` | 1,0 | hai bàn tay dựng đứng chụm giữa bàn rồi gạt dạt ra hai bên, mắt tròn | `tach` 0,42 |
| `double` | 1,0 | nhướn mắt tròn, chồm tới, xoa tay nhanh, lè lưỡi ("chơi lớn hả?") | |
| `deal_self_tense` | 1,0 | như `deal_self` nhưng run, mắt lồi, miệng méo, hai giọt mồ hôi rịn ở thái dương rồi chảy (tắt trước đoạn hoà về idle) | `bung` 0,38 |

Mọi clip về đúng idle giây 0 (`kiem.py` lệch 0,00). Lần đầu `shuffle` vòng cung hẹp, thấp; đã dang tay rộng hơn, vòng cung cao 195.

**Unity**:
- `DealerRig`: lớp trước chọn theo **tiền tố tên slot** (`tay_`, `nit_`, `no`, `ban_tay_`, `la_`, `xao_`) thay cho danh sách cứng, slot mới tự vào đúng
  lớp (mồ hôi ở lớp sau cùng mặt).
- `BlackjackScene`: ván đầu mỗi lần vào lều Lão Mực xoè bài ("Xào bài nào!"; hình cỗ bài trên nỉ ẩn từ `nhac_bai` tới `dat_bai`); Tách thì hai tay
  gạt rồi lá mới dạt sang tay 2 ở `tach` ("Tách thì tách!"); Gấp đôi thì `double` rồi lá thêm **úp nằm ngang**, tổng tay hiện "N điểm + ?", tới
  lượt dealer mới lật (trước lá úp của dealer); dealer rút khi đang 12–16 dùng `deal_self_tense`; chồng chip cược / thắng theo màu bậc cược
  (đỏ, xanh dương, xanh lá, vàng; xanh lá và vàng xoay sắc độ từ chồng đỏ, `d3/doi_mau_chip.py`).
- Lượt chụp dò trước hạt giống bằng lõi (`CasinoTableScene.SeedForTest`, `Blackjack.Deal` với `Rng` mới): ván miễn phí có đôi để Tách (kèm xoè bài),
  ván bậc 3 Gấp đôi, ván bậc 4 dealer phải rút khi đang 12–16.

**Đã soi trong game** (lượt chụp 1.101 khung, `d3/van_bai.webp`): xoè bài (cỗ bài trên nỉ ẩn / hiện đúng lúc), A-A gặp 6 → "Nên: Tách" → hai tay
gạt, hai tay A mỗi tay một lá; 9 + 2 gặp 3 → Gấp đôi, chip xanh lá, lá Q úp nằm ngang rồi lật trước lá úp dealer; dealer 13 rút lá ba bằng
`deal_self_tense` (mắt lồi, miệng méo, hai giọt mồ hôi). Lỗi bắt được: bong bóng thoại đặt ở x 300 rộng 420 che nửa phải mặt (mắt phải, giọt mồ
hôi bên đó) → dời sang phải đầu, hẹp lại, đủ chỗ trên màn 1:2.
Sau D4 (assets-52 góp ý): dòng chế độ (ván miễn phí / ván tập) chữ xanh nằm trên nỉ xanh rất chìm → đưa vào bảng tin giấy bên trái như
Vòng Xoay (`CasinoTablesMenu.Common`, chung cho cả hai lều có dealer).

**Còn lại** (mốc sau): âm thanh lầm bầm / búng ngón / "boing" (D8); viền nét vẽ sau khi người dùng chốt animation; D4 Vòng Xoay, D5 Máy Quả.

### D4 bản đầu (2026-11-26): lều Vòng Xoay có Lão Mực, viên bi lăn bằng vật lý, ô ra do lõi chọn

Người dùng: "làm phần roullete di, làm kĩ, lấy nhân vật đen kia vào, làm việc thả bóng nhìn thật và có vật lý hơn nhưng mình phải kiểm
soát được tỉ lệ ra". Chi tiết file ở `ArtGen/Casino/dealer/d4/README.md`.

**Tỉ lệ ra (lõi)**: `Roulette.Spin` chọn ô bằng `Roulette.Pick`: 26 ô đều nhau, hoặc theo `casino.roulette.weights` (26 số, thêm vào khối
roulette của `ArtGen/Casino/so_lieu/gen_casino.py` rồi `--apply`, menu Nhập dữ liệu). `Roulette.Chance`, `RtpOf`, `RtpRange` tính xác suất
và hoàn trả từng cửa theo trọng số; Cách chơi ghi "Mọi cửa hoàn trả X%" hoặc "Hoàn trả từ A% tới B% tuỳ cửa" theo số thật (luật mục 1.2:
tỉ lệ công khai). Hiện chưa đặt trọng số: mọi cửa 25/26.

**Viên bi (`Core/Casino/RouletteBall.cs`, C# thuần)**: bánh xe có hình học cố định (`RouletteWheel`: đường bi chạy, sườn dốc 8 mấu chắn, mâm
xoay 26 ô có vách ngăn; ô xếp xen kẽ hệ quanh mâm, `PocketAt` / `SlotOf`). `Simulate` mô phỏng 480 bước/giây: bi tì vách (ma sát lăn + cản
khí), rời vách khi lực ly tâm không thắng dốc, xoáy xuống, va mấu chắn (nảy lên, lệch hướng), lên mâm đang quay ngược chiều, nảy qua vách
ngăn khi còn nhanh, bị mặt mâm bắt khi chậm, lắc trong ô rồi nằm yên. `Plan(vị trí, góc mâm)` thử các cú thả với lực thả ngẫu nhiên trong
khoảng tự nhiên tới khi bi nằm đúng ô lõi đã chọn (cho lệch tối đa 3 ô rồi lùi pha mâm đúng số ô đó: bánh xe đối xứng theo từng ô nên
đường đi không đổi), ưu tiên cú có 2–9 lần nảy qua vách; trả về đường đi ghi 120 mẫu/giây + danh sách va chạm (cho tiếng). Màn chỉ phát
lại. Đo ngoài Unity (`d4/sim/chay.py stats`): 4.000 cú thả tự do đều nằm yên, 4,6–7,5 giây mỗi cú, ~4,7 vòng, phân bố 26 vị trí đều; 1.040
cú theo ô chọn: sai 0, trung bình 9 cú thử (nhiều nhất 68), ~4 ms mỗi lần tìm trên máy bàn.

**Hình** (`d4/`): nền lều tím nhìn từ ghế người chơi (Magnific GPT 2.6 1k high 95 + phóng classic 2k 72 = **167 credit**; ảnh mẫu là phác
khối bố cục + nền lều Đêm Bài), tách lớp bàn theo cung mép bàn đo tay. Bánh xe **vẽ bằng mã** (`ve_banh_xe.py`: viền mực rung, tô phẳng
có vân chì lấy từ nỉ của ảnh nền) để khớp từng số với mô phỏng: lòng chảo chiếu nghiêng, mâm nhìn từ trên (game xoay rồi ép dẹt 0,6),
trục, bi, nửa vành gần vẽ đè lên bi. Chip dùng lại của lều bài.

**Rig** (`rig/clip_d4.py`, `them_d4.py`; 74 xương, 22 slot, 26 clip, 2.362 KB; 21 clip cũ so khoá y nguyên): slot `la_bi` (viên bi trên tay
phải, mặc định ẩn) và 5 clip:

| Clip | Dài | Diễn | Sự kiện |
|---|---|---|---|
| `rl_invite` | 2,0 | tay phải quạt một cung trên bảng cược, nháy mắt | |
| `rl_no_more` | 1,0 | bàn tay úp xua ngang "hết đặt" (game cắt ở 0,62 s để quất mâm luôn) | |
| `rl_spin` | 2,0 | khoe bi → xoắn người → tay trái bắn dài xuống mép xa của mâm, quất sang trái → thu tay → tay phải ném bi chúi xuống | `quay` 0,767, `tha_bi` 1,50 |
| `rl_watch` | 2,0 lặp | chồm tới, đầu và mắt dõi theo bi; game KÉO thời gian theo góc bi (t = 0 bi ở 40°, bi đi theo chiều kim đồng hồ khi t tăng) | |
| `rl_point` | 1,5 | giơ ngón rồi vươn tay chỉ xuống bánh xe | `chi` 0,50 |

**Unity**:
- `DealerRig.Scrub(clip, thời điểm, dt)` / `EndScrub()`: kéo thời gian clip lặp bằng tham số ngoài, hoà 0,2 giây thật lúc bắt đầu (chụp
  lại dáng mỗi khung nên không phụ thuộc tốc độ kéo). Chữ ký cũ giữ nguyên (Đêm Bài, Hầm đấu, Trường đua dùng chung).
- `RouletteScene` viết lại theo mẫu sân khấu của Đêm Bài (sân khấu 1080 x 1920, rig 0,70, mép bàn y −650): bảng cược nỉ 6 x 6 (góc Sao
  Vàng, hàng đầu 5 cửa Số, cột đầu 5 cửa Hệ, 25 ô đơn), chip theo màu bậc cược nằm ở góc ô, bánh xe to sát người chơi luôn quay chậm.
  Bấm Quay: lõi chọn ô và tính tiền ngay → `rl_no_more` → `rl_spin`; ở `quay` mâm tăng tốc và `Plan` tìm cú thả (pha mâm được nắn dần
  trong lúc tăng tốc cho khớp), ở `tha_bi` bi bay từ bàn tay tới điểm vào đường chạy đúng mốc → phát lại đường đi (tiếng lăn, va mấu, va
  vách theo danh sách va chạm) → Lão Mực dõi theo → bi vào ô 0,45 s thì báo ô ra (ô trúng sáng, ô khác lùi tối, sao đánh dấu, `rl_point`)
  → chip thua: `take` (cú đập làm chip nảy vào lòng chữ V rồi theo tay về khay), chip thắng: `pay` (chồng chip "+N bi" theo tay ra ô
  gom) rồi về tay người chơi dọc hai bên bánh xe → `react_*` / `grumpy` (3 vòng thắng liền) / `sulk` (hết vòng có thưởng).
  Vòng miễn phí / vòng tập: chip thua về lại người chơi. Rig thiếu clip thì bỏ qua bước diễn, không kẹt.
- `Editor/CasinoTablesMenu.BuildRoulette` dựng prefab; `Common` cho lều có dealer nhận cả `RouletteScene` (dòng chế độ nằm trong bảng tin
  bên trái). Lượt chụp `Editor/CasinoRouletteTour.cs` (cờ `Temp/casino_rl_dealer_tour.flag`), dò hạt giống cho lõi ra ô muốn chụp và in log
  so ô lõi chọn với ô bi nằm.
- Test (`CasinoTests`): `Roulette_TiLeRa_TheoTrongSo` (bốc đúng trọng số, hoàn trả theo trọng số), `Roulette_Bi_NamDungOLoiChon` (156 cú:
  mọi ô, mọi góc mâm, bi nằm đúng ô, lực thả trong khoảng tự nhiên, không phải ép nhãn mâm). 28 test Casino đạt ngoài Unity.

**Đã soi trong game** (lượt chụp hai, 1.155 khung, `d4/vong_xoay.webp`, khung 617 x 1235): log ba vòng đều "ĐÚNG" (lõi ra Hỏa 3 / Hỏa 2 /
Sao Vàng, bi nằm đúng ô đó; 5,7–6,8 giây, 4–5,5 vòng, 1 lần va mấu, 2–6 lần nảy qua vách, 1–7 cú thử). Vòng miễn phí trúng 3 cửa (chip Sao
Vàng thua về lại người chơi, `pay` +310 bi, `react_win_big`), vòng bậc 2 trượt hết (`take` gom 5 chip xanh về khay, `react_lose`), vòng bậc
3 trúng Sao Vàng (`take` 1 chip rồi `pay` +1,9k bi, toast mảnh khách mời). Sửa sau lượt đầu: chip che số trên ô → dời lên góc ô; bảng
cược còn tối sau khi hết vòng → chỉ tối trong lúc báo kết quả; dòng "ván đầu miễn phí" đè bánh xe, chữ xanh chìm trên nỉ → vào bảng tin
trái; bi vẽ to hơn 20 %; `rl_point` bị `pay` / `take` cắt ngay ở `chi` → giữ thêm 0,5 s.

**Đổi sang đỏ đen** (người dùng xem bản đầu, 2026-11-26: "để đỏ đen thôi, nhiều màu quá"): ô trên mâm xen kẽ đỏ / đen như roulette thật
(vị trí chẵn đỏ, lẻ đen; 13 đỏ, 12 đen), Sao Vàng giữ màu vàng; hệ của ô ghi bằng biểu tượng hệ nhỏ màu kem trong lòng ô. Trên bảng cược,
ô đơn tô đúng màu đỏ / đen của ô đó trên mâm (`RouletteWheel.SlotOf(p) % 2`), cửa Hệ và cửa Số nền giấy (biểu tượng hệ tô mực), không còn
tô theo màu hệ. Luật và tỉ lệ không đổi (vẫn 5 hệ × số 1–5 + Sao Vàng; chưa có cửa cược Đỏ / Đen). Chip vẫn theo màu bậc cược. Lượt chụp
ba (1.152 khung): ba vòng vẫn "ĐÚNG"; `d4/vong_xoay.webp` là bản đỏ đen.

**Phần chung gom vào một bảng gập** (người dùng gửi ảnh hàng mức cược + bảng tin + Hũ bàn + Cách chơi dàn quanh đầu Lão Mực, 2026-11-26:
"mấy cái này để trong 1 cái toggle bên trái dưới thôi, không dàn ra như này"): `CasinoTableScene` thêm `infoToggle` / `infoPanel`
(`SetupInfo`, `SetInfo`, `InfoOpen`; prefab không gán thì như cũ). `CasinoTablesMenu.CommonCompact` dựng nút "Cược N bi" ở góc trái dưới
(trên nút Bỏ chip, bên trái bánh xe) và một bảng giấy chứa 4 mức cược, sự kiện + khách mời, hôm nay đã cược / thắng, dòng chế độ, Hũ
bàn, Cách chơi; chọn mức cược hoặc bấm Quay thì bảng tự gập. Vòng Xoay và Máy Quả (`Common` rẽ theo loại scene) dùng bản gọn; Đêm Bài
vẫn bản dàn quanh đầu (chưa được dặn đổi). Lều Vòng Xoay dựng riêng bằng menu "Lều Vòng Xoay: dựng riêng" / cờ
`Temp/casino_rl_build.flag` (không dựng lại Đêm Bài, Máy Quả). Theo lời nhờ của phiên Máy Quả (D5): `Make<T>`, `CommonCompact` thành
`internal`, `Build()` gọi `CasinoSlotMenu.Build` theo tên, bỏ `BuildSlot` cũ. Lượt chụp bốn (1.216 khung, có mở / gập bảng): ba vòng "ĐÚNG".

**Chưa làm / còn nghi**: chưa chạy trên điện thoại (thời gian `Plan` trên máy yếu, cỡ bi và ô cược khi chạm bằng ngón tay); chưa có tiếng
riêng (đang dùng `peg`, `deal`, `bet`, `whoosh`); người dùng chưa duyệt nhịp 5 clip mới; mỗi vòng dài ~13 giây (chưa có chạm để lướt nhanh);
bánh xe là hình vẽ bằng mã, nếu muốn nét tay hơn thì gen lại theo đúng khung rồi kiểm 26 ô; mốc D5 Máy Quả chưa làm.

### D5 bản đầu (2026-11-26): lều Hội Máy Quả, máy quả sống "Háu Ăn" + Lão Mực kéo cần

Người dùng đổi hướng so với mục 4.4: máy quả là một NHÂN VẬT rig xương ("nhún nhún, lắc lắc hai bên, nhảy lên lắc khi jackpot", học hoạt
hình ống cao su), duyệt concept hướng B "Háu Ăn" (có mặt, khay bi là miệng, hai chân ống cao su), Lão Mực kéo cần, rồi "làm nốt đi".
Chi tiết, script và thứ tự dựng lại: `ArtGen/Casino/may_qua/README.md`; trang xem `ArtGen/Casino/may_qua/xem_rig.html`.

- **Rig máy** (AtomSpine, `ArtGen/Casino/may_qua/atom`, xuất `may_qua.atomik` bản 3, 31 xương, 16 slot, 1.543 đỉnh, 12 clip, 2.469 KB,
  `--atlas-cap 1100`): thân ba khối chồng (hông, tấm khung cuộn cứng, vòm đầu) nén giãn và nghiêng trễ dần; chân ống cao su phình cong,
  giày ghim đất; cần 3 đốt + núm, lò xo ăng ten, 8 mắt, 6 miệng, hai nửa mày, đèn sáng hai nhóm. Viền mực vẽ sau cùng bằng
  `paint.stroke` vào lớp `vien` (50 nét, `rig/ve_vien.py`). Clip: `idle`, `pull`, `spin`, `stop_1..3`, `tease`, `lose`, `win`, `jackpot`,
  `free`, `appear`; sự kiện `keo`, `cach`, `nha_bi`, `no`, `het_no`, `dap`, `mien_phi`, `chao`.
- **Lão Mực**: thêm đúng một clip `sl_pull` (1,1 s; `dealer/rig/clip_d5.py`, 26 clip cũ không đổi khoá nào). Bàn tay trái (hình 10, nắm
  cần) đi theo ĐƯỜNG NÚM lấy từ chính clip `pull` của máy (`may_qua/atom/duong_num.json`) đổi sang toạ độ rig Lão Mực theo bố cục
  `may_qua/bo_cuc.json`; game phát hai clip cùng một khung nên tay nằm trên núm suốt cú giật (0,30 – 0,57 s). Bàn tay xoay tới
  276 độ / khung ở cú giật (cố ý, cú quất); bản 60 khung/giây soi không thấy lật ngược.
- **Game**: nền `Leu/sl_nen.jpg` (bục thảm đỏ, quầy bên phải, mép quầy y 1137 trên sân khấu), 9 biểu tượng `Leu/sl_bt_0..8.png`, rig
  `MayQua/may_qua.bytes`. Máy và Lão Mực đều vẽ bằng `DealerRig` + `DealerLayer` (lớp thân Lão Mực nằm trong `RectMask2D` cắt ở mép quầy).
  `Game/Casino/SlotReels.cs`: hình ba cuộn là Image trong Mask, mỗi khung đặt theo xương `tam_d` / `cuon` (méo theo thân máy).
  `SlotScene` viết lại: kéo cần → cuộn giật lùi rồi chạy → dừng lần lượt (máy "cạch" từng cái) → hai cuộn đầu khớp đường lớn THẬT thì
  cuộn cuối chạy thêm 0,7 s và máy nín thở (`tease`) → `lose` / `win` / `free` / `jackpot` (huy hiệu hoặc thắng từ 20 lần cược);
  bi phun (pool 44 Image) và rung màn theo sự kiện của rig; Quay nhanh bỏ đoạn kéo cần. Phần chung dùng bảng gập `CommonCompact`.
  Dựng: menu "Lều Máy Quả: dựng scene" (`Editor/CasinoSlotMenu.cs`, cờ `Temp/casino_sl_build.flag`).
- **Kiểm**: biên dịch thử ngoài Unity rồi trong Unity sạch; tour `Temp/casino_sl_tour.flag` (trượt, trúng, jackpot, ba Rương bằng hạt
  giống dò trước, 36 ảnh `Temp/PokiShots/casino_sl`) chạy hết không lỗi trên màn 1:2; `LocTests`, `PrefabOnlyTests`, `FontAndBuildTests`
  11 / 13 đạt, hai cái hỏng nằm ở file của phần khác (chữ prefab Trường đua; `new GameObject` ở thẻ bài, Bến câu, màn Nhà).
- **Chưa làm**: máy Android thật; âm thanh riêng; clip "dõi cuộn" của Lão Mực (đang về idle rồi phản ứng `react_*`); màn 1:2 cắt vài px
  mép trái thân máy lúc bẹp.

## Nguồn

- Cuphead vẽ tay 24 hình/giây, nén giãn là hình vẽ lại: [Game Developer, Animating Cuphead](https://gamedeveloper.com/art/animating-i-cuphead-i-the-verve-of-the-1930s-with-the-tech-of-now),
  [Inverse, kỹ thuật hoạt hình gần như tuyệt chủng](https://www.inverse.com/article/36647-xbox-one-cuphead-animation),
  [GamesRadar, The making of Cuphead](https://gamesradar.com/the-making-of-cuphead).
- Hoạt hình ống cao su: [Wikipedia, Rubber hose animation](https://en.wikipedia.org/wiki/Rubber_hose_animation),
  [Cartoon Brew, các phim ống cao su kinh điển](https://www.cartoonbrew.com/cartoon-study/the-rubber-hose-classics-that-inspired-the-cuphead-show-213700.html).
- Trong dự án: `29_DaoCasino.md`, `25_FTUE.md`, skill `animation-petclash`, `atomspine`, `pokiclash-spine-rig`.
