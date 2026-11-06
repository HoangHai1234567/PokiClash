# Màn boot (màn mở game): 3 ý tưởng, bản web thử

Viết 2026-11-06. Người dùng muốn màn mở game **đẹp, độc đáo, lạ mắt, hợp dòng chiến thuật**, làm bản web trước.

## Tiêu chí và cách giải

- **Hợp chiến thuật:** cả 3 ý đều vẽ **vòng khắc Ngũ Hành** (Thủy → Hỏa → Kim → Mộc → Thổ → Thủy).
  - Đây là luật chiến thuật lõi của game (đánh hệ mình khắc ×1,5).
  - Đó cũng là thứ tự đảo, nên mũi tên vẽ theo đúng đường người chơi sẽ đi.
  - Vẽ nối 5 đỉnh theo thứ tự đó thì ra ngôi sao năm cánh, dùng làm mô-típ chung.
- **Độc đáo:** giữ chất "sổ tay phiêu lưu" của cả game (giấy kẻ ô, nét mực rung, sáp màu, băng keo, sticker viền trắng). Mỗi ý có một chiêu riêng: sách pop-up, vòng ấn tự vẽ, bìa sổ lật mở.
- **Có sức sống:** 5 tướng khởi đầu cử động thật bằng clip aola: đứng, bị khắc thì trúng đòn, chạm vào game thì cùng ra đòn.
  - Bu Lông, Nụ Hoa, Giọt Sương, Sư Tử Lửa, Thạch Nhân (`15_TuongKhoiDau.md`).
- **Theo luật UI:**
  - không bóng đổ, không bóng lệch cứng, không bóng dưới chân (bóng aola dưới chân tướng bị bỏ khi vẽ);
  - lớp tách nhau bằng viền mực.
- **Thông tin có ích lúc chờ:** thanh tải tô 5 màu hệ, bút chì chạy theo, kèm mẹo luật thật (vòng khắc, ×1,5, chọn 1 trong 3 thẻ…).

## 3 ý tưởng

| | A · Sa bàn giấy (đề xuất) | B · Ấn Ngũ Hành | C · Bìa sổ chiến thuật |
|---|---|---|---|
| Hình | Bản đồ đảo (`Islands/world.png`) đặt nghiêng trên bàn gỗ như sa bàn; thẻ úp và bút chì cạnh bên | Trang sổ lề đỏ; vòng ấn tròn, chữ "THỦY KHẮC HỎA ✦ …" chạy quanh; 5 tướng đứng trên bệ đá ở 5 đỉnh | Bìa kraft, gáy vải, dây chun; nhãn tên có logo, "SỔ TAY CHIẾN THUẬT", "Chủ sổ: Bạn"; 5 sticker tướng; dấu đỏ "TUYỆT MẬT" |
| Cảnh mở (~4,3 giây) | Tấm bản đồ trượt vào, đảo được tô dần; tướng và cờ hệ **bật dựng lên như sách pop-up** ở đảo cùng hệ; mũi tên kế hoạch đứt nét vẽ theo vòng khắc; khoanh "Xuất phát!" quanh đảo Thủy; logo gấp bật lên | Bút mực vẽ vòng tròn; bệ rơi xuống, tướng dán "bộp"; mũi tên khắc vẽ thành ngôi sao, tướng bị khắc giật mình; dấu kiếm chéo ở tâm, logo đóng dấu | Sổ đặt xuống bàn; nhãn, sticker dán lần lượt; bút bi vẽ vòng khắc, ghi chú "khắc!", "×1,5"; viết tên chủ sổ; đóng dấu TUYỆT MẬT |
| Lúc chờ chạm | Mũi tên chạy nét, cờ bay, tướng thở | Vòng chữ xoay chậm, vệt dạ quang chạy theo vòng khắc | Tướng trên sticker cử động, dây chun rung |
| Chạm để vào | Tướng ra đòn, camera lao vào đảo Thủy, mây khép mở ra sảnh | Tướng ra đòn, vòng ấn xoay một nhịp, mây ra sảnh | Dây chun bật ra, bìa lật mở: **trang đầu chính là sảnh** |
| Mạnh | Đọc ra "chiến thuật" ngay (sa bàn, mũi tên tác chiến); khoe thế giới thật của game; nối liền sang sảnh (sảnh cũng là bản đồ đảo) | Gọn, dễ nhớ, làm được biểu tượng game và icon; dạy luật khắc ngay từ màn đầu; làm Unity dễ nhất (toàn 2D) | Duyên nhất, hợp tên "Sổ Tay Phiêu Lưu"; lật bìa vào sảnh rất "đã" |
| Yếu | 3D giả bằng nghiêng mặt phẳng, máy yếu phải thử; tướng ở xa hơi nhỏ | Ít "thế giới", nặng về sơ đồ | Nhiều chi tiết, hơi rối; ý chiến thuật nằm ở chữ và ghi chú nhiều hơn |

**Đề xuất:** A làm màn chính. Có thể lấy vòng chữ của B làm viền logo, hoặc làm icon game.

## Bản web

- Code: `Web/src/view/boot/`.
  - `boot.ts`: điều khiển, nạp trước, chọn ý tưởng.
  - `common.ts`: tướng cử động, logo, thanh tải, vân gỗ.
  - `sceneTable.ts` (A), `sceneSeal.ts` (B), `sceneCover.ts` (C), `boot.css`.
- Mở `http://localhost:5180/` là chạy màn boot rồi vào sảnh. Hộp giới thiệu lần đầu chờ boot xong mới hiện.
  - Thanh "Ý tưởng" trên cùng đổi qua lại A / B / C và diễn lại. Trình duyệt nhớ lựa chọn.
  - `?boot=a|b|c`: chọn ý tưởng (xem được cả khi mở thẳng scene khác).
  - `?skipboot` hoặc `?skipintro`: bỏ màn boot.
- Ảnh dùng chung với Unity, không chép sang web: máy chủ dev phục vụ `/unity/*` từ `Assets/03 Art` (đảo `Islands/world.png`, bệ `Islands/be_<hệ>.png`).
- Logo "PokiClash" vẽ bằng chữ SVG (Baloo 2), viền trắng mép xé như sticker tướng. Chữ CLASH tô 5 màu hệ theo vòng khắc. Đây là logo tạm, chờ người dùng chốt hình logo.

## Khi chuyển sang Unity (sau khi người dùng chọn)

- Đặt cảnh vào `Boot.unity`. Hiện scene này chỉ nạp dữ liệu rồi mở Hub.
  - Cảnh chạy trong lúc `App` nạp, chạm thì `SceneRouter` mở Hub.
  - Với C thì Hub nạp sẵn dưới bìa.
- Logo nên gen thành ảnh (cùng nét vẽ tay của game) thay chữ SVG.
- A cần nghiêng mặt phẳng bằng camera phối cảnh, hoặc bake sẵn tấm bản đồ nghiêng. Tướng dùng prefab aola đã có, quay mặt về camera.
- B và C làm bằng UI 2D thường. Vòng ấn và nét bút vẽ dần bằng shader cắt theo độ dài nét, hoặc Image fill.
