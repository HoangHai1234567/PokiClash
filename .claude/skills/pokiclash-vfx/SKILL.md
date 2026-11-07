---
name: pokiclash-vfx
description: >
  Luật và cách làm hiệu ứng (VFX) của PokiClash trong Unity: tia chiêu mana, tuyệt kỹ, đòn đánh, chữ nổi, rung, phần động
  sàn đấu, hạt máy bi; gói GPT vẽ ảnh hiệu ứng (build_fx.py), nhập ảnh vào Assets/03 Art/Fx, tối ưu dung lượng, chụp thử.
  Dùng khi thêm, sửa hay soi bất kỳ hiệu ứng nào trong game (trận, sàn đấu, máy bi, đảo), hoặc khi vẽ ảnh hiệu ứng mới.
---

# Hiệu ứng (VFX) PokiClash

Đọc hết trước khi đụng hiệu ứng. Game là Unity 6 URP, mọi thứ nằm trên **uGUI canvas**. Hiệu ứng là **ảnh vẽ tay rời**, được code
cho nở, bay, mờ, xoay, nhuộm màu. Project **không dùng** ParticleSystem, VFX Graph hay post-processing (bloom). Đừng đưa chúng vào
khi người dùng chưa đồng ý: chúng không chạy theo nhịp sân (`StageView.Clock`), không khớp nét vẽ tay, và làm nặng build.

## 1. Luật hình (người dùng chốt, bắt buộc)

- **Nét vẽ tay như ảnh mốc** `ArtGen/Islands/refs/world_style.png`: viền mực nâu sẫm `#2B2118` hơi rung, tô chì màu và sáp màu.
- **Tô phẳng, không bóng, không ánh sáng** (2026-11-04, áp cho cả hiệu ứng của tướng): mỗi vùng một màu đều, không mảng sáng
  tối, không điểm sáng trắng, không bóng loáng, **không quầng sáng (glow, halo), không gradient**. Màu trắng chỉ là màu phẳng
  (bọt, ngôi sao lấp lánh), không phải ánh phản chiếu. Câu dán vào prompt có sẵn: `FLAT_FIX`, `LINE` trong `ArtGen/Heroes/build_fx.py`.
- Trong engine chỉ được chồng lớp, đổi alpha, nhuộm màu `Image.color`. **Không** dùng additive blend, bloom hay shader phát sáng
  để bù "cho rực". Muốn hoành tráng hơn thì thêm hình vẽ tay, cho to hơn, thêm nhịp (nổ, văng, rung).
- Hiệu ứng không được che con bị trúng: vụ nổ trúng đòn luôn nhỏ hơn thân nó (`BeamHit` lấy cỡ theo `tH`).
- Hình và chuyển động aola là của Baitian: không đăng công khai, kể cả artifact.

## 2. Luật trận (người dùng chốt 2026-11-03)

- **Chiêu mana = bắn tia** cho mọi tướng, quái thường, phần lớn mini boss. Tia to dần theo dạng tiến hóa: cỡ 0,7 tới 1,4,
  quái một dạng là 1, boss ×1,2. Chỉ vài boss làm riêng, khai `"mana": "clip"` trong `anim_moi.json` (ra `anim.json`,
  `AolaActor.ManaUsesClip`), lúc đó phát clip CHIÊU.
- Dạng có clip bắn `1_5` + khoá `"cast"` (mảnh, điểm bắn, khung, cỡ tia) thì tia ra đúng chỗ đó. Không có thì nhún tại chỗ, tia ra từ trước ngực.
- **Clip CHIÊU (1_6) chỉ dùng cho tuyệt kỹ**, khoá `"lunge": true` thì lao tới đối thủ trước khi đánh.
- Chiêu mana nổ ngay lúc bấm, không xếp hàng (`Battle.UseInnate`). Quy tắc Unity đã khác bản web, đừng xuất golden web đè lên.
- Con đang ra đòn vẽ đè lên con kia. Lúc ra đòn cả sân chậm lại (`AttackPace` 1,3, `SkillPace` 1, `skillHold` giữ nhịp tới khi tia tan).
- Hiện chỉ có ảnh tia **nước**. Hệ khác đang nhuộm màu hệ (`Theme.Of(elem)`) làm tạm, tới khi có ảnh riêng từng hệ.

- **Đòn xa của tướng aola** (đạn bay, cầu nước trên đầu đối thủ, sóng thần, chuông rơi): vẽ trong clip, hình ở xa được trận kéo về
  thân đối thủ. anim.json khai `"hit"` (khung trúng), `"stay"` (không kéo lao), `"far_ramp"` (kéo trọn từ điểm này), xem
  `ArtGen/Heroes/QUY_TRINH.md` mục 11. Toạ độ quanh đối thủ tính theo chiều cao đối thủ chuẩn (150 đơn vị sân), không theo con ra
  đòn. Phía trên giữa thân đối thủ (phe địch ở trên trái màn) chỉ còn khoảng 1 chiều cao tới mép sân, sau lưng cũng vậy: cầu nước,
  chuông đặt khoảng 0,8 trên giữa thân, cỡ 0,5; sóng thần sát lưng đối thủ, cỡ khoảng 1,15. Đòn đánh, chiêu cuối các tướng phải
  khác kiểu nhau (người dùng chê "lộn xong đánh hoặc lao vào đánh" một kiểu, 2026-11-07).

## 2b. Animation phụ của tướng (người dùng dặn 2026-11-07, bắt buộc)

- Tướng vẽ lại phải **đủ animation như con gốc aola**, nhất là **nước bao quanh** và animation phụ (bọt sủi, giọt bay, sóng cuộn,
  lửa nước, cánh phất, đuôi quẫy, xúc tu, chuông lắc). Không để mảng nước thành một ảnh tĩnh chỉ trôi lên xuống.
- Bản ghép thay mảnh tự chạy của aola (khung con `c<n>_<k>` trong clip đứng gốc) bằng một ảnh GPT tĩnh, nên sau mỗi lần ghép phải
  kiểm: `py -3 ArtGen/Heroes/tools/kiem_anim_phu.py <ảnh> <dạng ...>` (mảnh có khung con ở bản gốc),
  `py -3 ArtGen/Heroes/tools/anim_thuy_dung.py <ảnh> <dạng ...>` (clip đứng gốc cạnh bản mới, 6 khung).
- Nước, bọt, giọt: dùng khung con gốc tô lại bằng `<aola>/tools/to_nuoc.py` (giữ đúng nhịp chảy của bản gốc; viền mực bằng viền mảnh
  GPT, cụm nhỏ tô xanh đậm; nước màu khác thì đổi bảng màu, giữ viền mực). Hình gốc là vệt trắng mảnh (vòng sóng loang) thì tô ra
  vòng mực sẫm: không dùng, làm bằng hiệu ứng vẽ tay khác.
- Thân (cánh, đuôi, xúc tu, râu, chuông, áo choàng): xoay thêm quanh khớp, lệch pha, lan xuống mảnh con, ở mọi clip.
- Đảo Thủy làm bằng `ArtGen/Heroes/tools/anim_thuy.py` (bảng `SUB`, `PHU` trong `anim_thuy_choreo.py`).

## 3. Code: hiệu ứng nằm ở đâu

| Chỗ | Làm gì |
|---|---|
| `Assets/01 Script/Game/Battle/StageView.cs` | Sân đấu. Hàng chờ hiệu ứng `Take(prefab)` / `AddFx(item, prefab, life, update)` / `Release`; `update(f, k)` nhận `k` 0..1. Có sẵn: `Beam`, `BeamHit`, `Pop` (nở rồi mờ), `Drift` (bay, rơi, xoay), `Ripple` (vòng dẹt dưới chân), `Spark`, `Burst` (chữ tượng thanh), `Ring`, `Flash`, `shake` |
| `Assets/01 Script/Game/Battle/StageFx.cs` | Thành phần của mọi prefab hiệu ứng trên sân: `CanvasGroup` + `Image` và/hoặc `TextMeshProUGUI` |
| `Assets/01 Script/Game/Battle/ArenaAnim.cs` | Phần động của nền sân (lớp `PhanDong`, dưới tướng), đọc `Resources/arena_fx.json`, sprite `san_*`, `anim_*`. `Flare()` bừng lên khi dùng chiêu |
| `Assets/01 Script/Game/Machine/MachineFx.cs` | Hạt của máy bi: từng loạt `Burst` (số hạt, đời, tốc, trọng lực), sprite `fx_*` tìm qua ArtLibrary |
| `Assets/01 Script/Editor/BeamFxMenu.cs` | Menu `PokiClash/Prefab/Sàn đấu: tia nước của chiêu bắn`: dựng `Items/TiaNuoc`, `Items/AnhHieuUng`, gán ảnh `Assets/03 Art/Fx/*` vào StageView của `Screens/Battle.prefab` |
| `Assets/01 Script/Editor/ArenaFxMenu.cs` | Menu dựng lớp `PhanDong` trong `Screens/Battle` |
| Hiệu ứng trong clip tuyệt kỹ | Vẽ thẳng vào clip aola bằng `tools/anim_moi.py` của AolaRipper (khoá `"fx"`, `"fx_dir"`, `"far"`, `"fx_off"`), xem `ArtGen/Heroes/QUY_TRINH.md` mục 6 |
| Đòn đánh, chiêu cuối, animation phụ đảo Thủy | `ArtGen/Heroes/tools/anim_thuy.py` dựng thẳng trên dạng đã nhập (atlas, asset, anim.bytes), bộ đòn và bảng `SUB`/`PHU` ở `anim_thuy_choreo.py`, ảnh gói `thuy_chieu_fx`; xem `QUY_TRINH.md` mục 11 |

Quy ước khi viết hiệu ứng mới trên sân:
- Toạ độ theo khung web 540 × 464, nhân `StageView.K = 2` ra UI. Đặt vị trí qua `P(...)`, cỡ `sizeDelta` nhân `K`.
- Thời gian là **giây sân** (đã nhân nhịp, chậm khi ra đòn, nhanh khi tua). Chờ bằng `Wait(...)` trong coroutine, không dùng
  `WaitForSeconds` hay `Time.deltaTime`.
- Luôn lấy bản sao qua `Take`, không `Instantiate` trực tiếp, không `Destroy`. Ảnh rời đổi sprite bằng `Theme.SetSprite(item.Image, s)`.
- Cỡ hiệu ứng phụ to chậm hơn cỡ tia (`g = (scale/0.7)^0.4`) để không che tướng bắn. Theo cách này khi thêm hiệu ứng theo dạng.
- Prefab hiệu ứng mới: chép từ `Items/TranVong` như `BeamFxMenu.MakeFx`, dựng bằng menu Editor, không sửa tay trong scene.

## 4. Ảnh hiệu ứng: gen, nhập, tối ưu

1. **Gói GPT**: thêm bước vào `LINES` trong `ArtGen/Heroes/build_fx.py` (mã bước `FXnn`, tên file, mô tả tiếng Anh, độ dày viền px,
   ghi chú tiếng Việt), rồi `py -3 -I ArtGen/Heroes/build_fx.py <mã gói>`. Gói ra `ArtGen/Heroes/gui_gpt/<mã>_fx/`, gồm file prompt
   và `HUONG_DAN.md`. Theo luật file prompt trong `CLAUDE.md`: mở đầu bằng danh sách ảnh mẫu đường dẫn tuyệt đối, mục SAVE, tự đủ.
   Trong chat chỉ đưa người dùng đường dẫn file prompt.
2. Ảnh hiệu ứng: nền trắng tinh, chừa lề, chiếm khoảng 75% khung 1024, không sinh vật, không chữ, không viền sticker.
   Tia vẽ **hướng sang phải** (game xoay và lật).
3. **Nhập vào sân**: `py -3 -I ArtGen/Heroes/build_fx.py --xuat` lấy ảnh GPT mới nhất theo mtime của từng bước trong `STAGE_FX`, cắt nền
   trắng nối mép (`hollow` cho hình vòng), cắt sát, thu về cạnh dài tối đa (tia, nổ, vòng 512; giọt, lấp lánh 192), lưu
   `optimize=True` vào `Assets/03 Art/Fx/`. Sau đó chạy menu `PokiClash/Prefab/Sàn đấu: tia nước của chiêu bắn`.
4. **Dung lượng** (build Android phải ở khoảng 60–70 MB): tối ưu ngay lúc nhập, không để dồn. Sprite không mipmap, Android ASTC (ảnh Fx
   hiện là 6x6), cỡ ảnh bằng cỡ lớn nhất hiện trên màn. Kiểm bằng menu `PokiClash/Dung lượng: ảnh nặng trong build`.
5. **Tên ảnh không trùng ảnh thay thế** trong `Assets/03 Art/Fallback/` (`fx_glow`, `fx_puff`, `fx_ring`, `fx_sparkle`, `fx_star`,
   `fx_streak`, `battle_<hệ>`…). Trùng tên thì `PokiClash/Dựng lại danh mục ảnh` thay ảnh đó vào mọi prefab. Ảnh sân dùng tên tiếng
   Việt (`tia_nuoc`, `no_nuoc`) hoặc tiền tố `san_`. Sau khi dựng lại danh mục, dòng log "Đổi ảnh thay thế sang ảnh gen" phải là 0.
6. Ảnh tia hệ mới: đặt tên `tia_<hệ>` và nối vào `StageView.Beam` theo hệ, thay chỗ nhuộm màu tạm.

## 5. Kiểm trước khi báo xong

- Tự chạy, không đưa người dùng danh sách việc. Editor Unity điều khiển qua mcp-for-unity HTTP `127.0.0.1:8090/mcp`.
  Editor dùng chung với session khác: nhắn trước khi Play, refresh hay chạy test.
- Tour có sẵn (đang Play, mở từ Boot): `PokiClash/Thử/Giọt Sương ra trận: đánh, bắn tia, chiêu cuối ở 3 dạng`,
  `PokiClash/Thử/Tiểu Y ra trận: …`, `PokiClash/Thử/Máy bi: soi hiệu ứng`, các tour `Sàn đấu đảo …`. Ảnh chụp vào `Temp/PokiShots/<thư mục>/`.
  Hiệu ứng mới mà không tour nào chụp tới thì thêm tour mới theo mẫu `GiotSuongCombatTour.cs`.
- **Tự xem từng khung chụp**: tia có ra đúng chỗ bắn không, có lật đúng chiều không, vụ nổ có nhỏ hơn con bị trúng không, có mảng
  sáng hay glow lọt vào không, đủ ba pha phóng, bay, trúng/tan chưa. Đếm "đã có prefab, đã gán ảnh" không thay cho việc xem.
- Tướng mới hay vừa sửa animation: chạy `kiem_anim_phu.py` và `anim_thuy_dung.py`, xem nước bao quanh có chảy, cánh, đuôi có động
  như bản gốc không. Tour đảo Thủy: `PokiClash/Thử/Đảo Thủy: … ra trận`, `PokiClash/Thử/<boss> ra trận`.
- Người dùng chấm trên điện thoại Android (build thường, không phải Development). Hiệu ứng chỉ chạy trong Editor thì coi như chưa xong.
- Đổi hiệu ứng không đổi luật trận nên không cần tính lại golden. Đổi thời điểm trúng (`HitTime`) hay thứ tự sự kiện thì chạy EditMode.
