# PokiClash · bản web thử ("Sổ Tay Phiêu Lưu")

Bản web để thử vòng lõi trước khi làm trong Unity:

**đánh ải bằng thẻ → nhận bi → thả bi vào máy → lên cấp, nâng thẻ, tiến hóa → ải khó hơn.**

Thiết kế và số liệu: [`GD_Claude/11_BanWeb_TheBai.md`](../GD_Claude/11_BanWeb_TheBai.md).

## Chạy

Nhấp đúp `chay_web.bat`. Lần đầu nó tự `npm install`, rồi mở `http://localhost:5180/`.

Hoặc chạy tay:

```
cd D:\PokiClash\Web
npm install
npm run dev
```

**Thử trên điện thoại:** máy tính và điện thoại cùng wifi. Mở địa chỉ `Network: http://192.168.x.x:5180/` mà cửa sổ dòng lệnh in ra. Màn hình dọc, khung 540 × 960 tự co theo máy.

**Hình tướng** đọc thẳng từ `D:\Aola-20261029T161238Z-1-001\Aola\AolaRipper\AolaRipper\reskin`, không chép vào đây.
- Thư mục aola ở chỗ khác thì đặt biến môi trường `AOLA_RESKIN` trước khi chạy.
- Hình là của Baitian, chỉ dùng trong bản thử: không đăng bản web này lên mạng.

## Có gì

Mỗi chức năng là một **scene** riêng (học theo Clash of Critters). Vào scene bằng nút trên đảo hoặc hàng nút dưới sảnh, ra bằng nút quay lại; chuyển scene có màn mây khép vào rồi tách ra. Không còn thanh tab.

| Scene | Nội dung |
|---|---|
| Sảnh: đảo lớn | Đảo lớn chia 5 vùng hệ, làng máy bi ở giữa. **Không khoá vùng nào**: bảng tên ghi cấp đề nghị và độ khó so với cấp của bạn ("Vừa sức", "Khó", "Quá mạnh!"), mũi tên chỉ vùng nên đánh. Hàng nút dưới: Tướng, Sổ thẻ, Máy Bi, Đánh tiếp, Sổ tay. |
| Đảo hệ | Ảnh đảo to, cuộn dọc; 8 ải dọc đường mòn từ bãi biển lên hang boss (ải 4 mini boss, ải 8 boss), mở lần lượt. Thanh tiến độ có 2 rương mốc (qua 4 và 8 ải). Khung dưới: ải tiếp theo, địch, thưởng, nút Đánh. |
| Trận | Lượt luân phiên, bên Tốc cao đi trước mỗi hiệp. Mỗi lượt chọn 5 lần, mỗi lần 1 trong 3 thẻ. Chiêu và Tuyệt kỹ xen vào hàng thẻ, không tốn lần chọn. Đổi tướng đầu lượt. Có tự chơi và tốc độ ×1/×2/×3. |
| Máy Bi | Pachinko có vật lý. Giữ nút để thả liên tục, tối đa 20 bi một đợt. Nút ×N là mức cược: tốn N bi mỗi lần thả, thưởng ×N. Bảng tỉ lệ ở nút "Tỉ lệ". |
| Tướng | 11 tướng aola: 4 clip, chỉ số theo cấp, 3 thẻ riêng (nâng bằng bản sao), tiến hóa sao. |
| Sổ thẻ | Bộ thẻ chung, mở dần theo cấp. |
| Sổ tay | Cài đặt, bảng thử (+bi, +XP, tua AFK, mở hết), chỉnh số cân bằng, máy tự chơi 100 trận. |
| Đồng hồ trên sảnh | AFK: ải đã qua tự đánh ra bi, giữ tối đa 12 giờ, nút ×2 giả lập xem quảng cáo. |

**Bắt đầu:** chỉ có Tiểu Y (Thủy). Đảo Thủy tặng Võ Sư (qua ải 3) và Gia Bỉ (qua ải 6). Thứ tự gợi ý Thủy → Hỏa → Kim → Mộc → Thổ; mỗi đảo rơi tướng hệ của nó, đúng là hệ khắc đảo kế tiếp.

**Ảnh đảo:** đặt vào `public/art/` (`world.png`, `zone_<hệ>.png`). Chưa có thì game tự vẽ bản đồ nét tay. Link tải 4 ảnh đã gen bằng Canva và prompt gen thêm: [`ArtGen/PROMPTS.md`](ArtGen/PROMPTS.md).

Dữ liệu lưu ở `localStorage` của trình duyệt. Xoá ở Sổ tay → "Xoá dữ liệu".

Đường dẫn tắt khi thử:
- `?fresh`: bắt đầu lại từ đầu;
- `?skipintro`: bỏ màn giới thiệu;
- `?screen=machine`: mở thẳng một scene (`world`, `heroes`, `cards`, `machine`, `notebook`);
- `?screen=zone&zone=hoa`: mở thẳng một đảo hệ;
- `?screen=battle&stage=5`: vào thẳng trận.

## Công cụ đo

```
npm run sim -- pachinko       # tỉ lệ từng ô máy bi, EXP và bi hoàn lại mỗi bi
npm run sim -- battle 100     # tỉ lệ thắng 40 ải (5 đảo) theo cấp, mỗi đảo một đội khắc hệ
npx tsx scripts/gen_doc.ts    # in bảng tướng, thẻ, ải từ dữ liệu thật
node scripts/shot.mjs --go "skipintro" --wait 1500 --shot ten   # chụp màn hình bằng Chrome không giao diện (cần npm run dev)
```

## Xuất sang Unity

Web là nguồn số liệu: sửa ở đây rồi xuất lại, Unity không sửa tay.

```
npx tsx scripts/export_data.ts      # tướng, thẻ, đảo, ải, cấu hình -> ../Assets/02 Data/Json
npx tsx scripts/export_golden.ts    # bộ đối chiếu cho test Unity (số ngẫu nhiên, mô tả thẻ) -> ../Assets/02 Data/Golden
node scripts/export_fallback.mjs    # ảnh thay thế: bản đồ nét tay và icon SVG -> ../Assets/03 Art/Fallback (cần npm run dev)
```

Sau khi xuất dữ liệu, trong Unity chạy menu `PokiClash/Nhập dữ liệu`.

## Cấu trúc code

Phần logic tách khỏi phần hiển thị, để chép sang C# cho Unity.

```
src/core/            logic thuần, không đụng trình duyệt, chạy được trong Node
  types.ts           kiểu dữ liệu: tướng, thẻ, hiệu ứng
  data/heroes.ts     11 tướng (hệ, độ hiếm, chỉ số gốc aola, 3 thẻ)
  data/cards.ts      23 thẻ chung + 33 thẻ riêng; hiệu ứng viết dạng dữ liệu
  data/stages.ts     5 đảo hệ × 8 ải, toạ độ vùng trên đảo lớn và ải trên ảnh đảo, rơi mảnh, tướng tặng
  data/config.ts     mọi hệ số cân bằng ở một chỗ
  battle.ts          luật trận: lượt, chọn thẻ, chiêu, đổi tướng, sát thương, bị động; trả về sự kiện kèm ảnh chụp số
  ai.ts              máy chọn thẻ, dùng chiêu, đổi tướng
  cardtext.ts        sinh mô tả thẻ theo cấp thẻ
  progression.ts     cấp, thẻ, sao, mảnh, ải, AFK, lưu
  pachinko.ts        vật lý máy bi và bảng thưởng
  sim.ts             máy tự chơi cả trận
src/view/            giao diện (DOM + canvas)
  app.ts             khung 540 × 960, thanh trên, thanh quay lại, màn mây chuyển scene
  aola.ts            phát anim.json của aola (blend, tint, filter), viền sticker
  battle/            sân đấu canvas + màn trận
  scenery.ts         nạp ảnh đảo từ public/art, chưa có thì vẽ bản đồ nét tay
  screens/           world (sảnh), zone (đảo hệ + chuẩn bị trận), tướng, thẻ, máy bi, sổ tay
  icons.ts, art.ts   icon vẽ tay, vân giấy, nét rung
```
