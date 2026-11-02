# ArtGen: gói prompt gen ảnh cho PokiClash

Ảnh mới cho game thật: đảo, nền trận, bộ UI vẽ tay, icon, máy bi, công trình sảnh, side meta, tướng.

Cách làm như các dự án trước:
1. Mở `PROMPTS.md` của từng gói, gửi "Tin nhắn mở đầu" cho GPT kèm ảnh đính kèm, rồi gen từng ảnh theo mã.
2. Lưu đúng tên file vào `inbox/` của gói đó.
3. Báo Claude để xử lý (cắt nền, cắt lưới, 9-slice) và đưa vào `Assets/03 Art/`.

Spec liên quan: `openspec/changes/setup-unity-foundation/specs/art-assets/spec.md`.

## Thứ tự gen

| Thứ tự | Gói | Số ảnh | Vì sao trước |
|---|---|---|---|
| 1 | [UIKit](UIKit/PROMPTS.md) | 8 | **Chốt style nét vẽ tay**; mọi gói sau đính kèm ảnh U1 đã duyệt |
| 2 | [Islands](Islands/PROMPTS.md) | 6 đảo rời + biển + sheet phần động (đã có); 5 bản đồ đảo hệ gen riêng (tuỳ chọn) | `Islands/compose_islands.py` ghép đảo gen rời thành đảo lớn liền khối cho sảnh (kéo được, vành mây ở rìa) và bản đồ 5 đảo hệ (đảo gen + đường 8 ải); thêm vùng mới dễ |
| 3 | [Icons](Icons/PROMPTS.md) | 5 sheet × 16 | Icon thẻ, tài nguyên, hệ, chỉ số |
| 4 | [BattleBG](BattleBG/PROMPTS.md) | 5 | Nền trận theo hệ |
| 5 | [Pachinko](Pachinko/PROMPTS.md) | 4 | Máy bi (thân máy, bộ phận, rương lớn, hiệu ứng) |
| 6 | [Hub](Hub/PROMPTS.md) | 2 sheet (6 công trình, 6 mây) | Công trình trên sảnh (Tướng, Sổ thẻ, Trang trại, Đền, Hang, Máy bi) |
| 7 | [SideMeta](SideMeta/PROMPTS.md) | 5 | Trang trại, Đền Huy Hiệu, Hang Tiềm Năng, huy hiệu, đá |
| 8 | [Heroes](Heroes/QUY_TRINH.md) | mỗi dạng 1 concept + các nhóm mảnh (+ mảnh vũ khí) | 40 tướng (8 mỗi hệ), mỗi tướng là một dòng tiến hóa aola. **Vẽ đè lên rig aola**, giữ animation; nét vẽ tay như ảnh mốc bản đồ, thiết kế học từ tướng aola, vẻ "chiến"; viền giấy xé do shader. Gói gửi GPT sinh bằng `Heroes/build.py` |

## Khối STYLE (dán vào mọi prompt)

```
STYLE: hand-drawn storybook cartoon for a vertical mobile game. Bold dark-brown ink outlines (#2B2118), slightly
wobbly like a real pen, colored-pencil and crayon hatching for shading, flat warm colours with light watercolour
washes, subtle cream paper grain, soft light from the top-left. Cheerful, cozy, a little naive, like a kid's
adventure notebook drawn by a professional illustrator. No photorealism, no glossy 3D render, no heavy gradients.
PALETTE: ink #2B2118, paper #FBF4E2, red #E8553F, orange #F39A2D, yellow #F7C948, green #6CBF4F, teal #3FB8A9,
blue #4A90D9, purple #9A6AD6, pink #F07FA6.
```

Màu theo hệ và độ hiếm, game dùng thống nhất:

| | Màu |
|---|---|
| Kim | bạc #B8C4CF |
| Mộc | #6CBF4F |
| Thủy | #4A90D9 |
| Hỏa | #E8553F |
| Thổ | #E2A93B |
| Thường | #B9B1A3 |
| Khá | #6CBF4F |
| Hiếm | #4A90D9 |
| Sử thi | #9A6AD6 |
| Huyền thoại | #F39A2D |

## Ảnh tham chiếu và lưới

| Ảnh | Dùng cho |
|---|---|
| `StyleRefs/R1_UI_Cards.png` | Thẻ, khung, chữ vẽ tay của bản web (style đã duyệt) |
| `StyleRefs/R2_UI_Machine.png` | Máy bi của bản web (bố cục cũ, xem nét) |
| `StyleRefs/R2b_MayBi_KetVang.png` | Máy bi hiện tại có két vàng (ảnh tĩnh Unity vẽ từ code) |
| `StyleRefs/R3_UI_Modal.png` | Hộp thoại, con dấu, nút |
| `StyleRefs/R4_Hub_Sketch.png` | Bố cục sảnh 5 vùng (bản vẽ bằng code) |
| `guides/G_Sheet3x2.png` | Lưới 3 × 2 đánh số (1536 × 1024) cho sheet 6 món |
| `guides/G_Sheet4x4.png` | Lưới 4 × 4 đánh số (1024 × 1024) cho sheet 16 icon |
| `guides/G_Sheet4x3.png` | Lưới 4 × 3 đánh số (1536 × 1024) cho sheet 12 món |
| `guides/G_Island_2x3_SafeBand.png` | Khung đảo 2:3; dải hồng là phần còn lại trên màn 9:16; dải xám là vùng an toàn trên dưới |
| `guides/G_BattleStage.png` | Chỗ đứng hai tướng trên nền trận |

## Quy tắc

- **Ảnh đính kèm ghi đủ trong file prompt** (người dùng dặn 2026-11-02, cũng có trong `CLAUDE.md`): đường dẫn tuyệt đối, ảnh trông như thế nào (nội dung, cỡ, nền), gửi ở bước nào, là ảnh thứ mấy; ảnh chưa có thì ghi bước sinh ra nó. Người dùng chỉ kéo thả: mỗi lượt một thư mục (ảnh đánh số + `00_instructions.txt`) kèm `HUONG_DAN.md`. Mẫu: `Heroes/gui_gpt/<mã>/`.
- **Không gửi ảnh chụp game khác cho GPT** (Clash of Critters, Aola, Pokiwar), không nhắc tên game trong prompt. Ảnh vào game thật.
- **Ngoại lệ, gói Heroes** (người dùng: "cứ đính hình vào", 2026-11-02): đính bóng xám, bản đồ vùng, hình gốc từng nhóm mảnh của rig aola và tờ mẫu thiết kế từ hình aola (`Heroes/refs/`); dặn chỉ lấy thiết kế và khung, không chép con nào, nét theo bản đồ vẽ tay.
- Ảnh nhiều món (sheet): nền **trong suốt**, mỗi món nằm gọn trong một ô của lưới, không món nào chạm ô bên cạnh.
- **Không vẽ chữ lên ảnh**: game tự viết chữ tiếng Việt. Chỉ logo được có chữ.
- Khổ GPT hỗ trợ: 1024 × 1024, 1536 × 1024, 1024 × 1536. Màn game là 9:16, nên ảnh dọc 1024 × 1536 bị cắt hai bên khoảng 8% mỗi bên. Nội dung chính phải nằm trong dải giữa (`G_Island_2x3_SafeBand.png`).
- Muốn đảo 3D: gen bằng Tripo từ ảnh đã duyệt, đặt camera nhìn chéo khoảng 55° từ trên xuống, chụp ra PNG đúng khổ.
