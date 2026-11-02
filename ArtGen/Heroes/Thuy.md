# Heroes: đảo Thủy (8 tướng)

**Cách làm đổi ngày 2026-11-01:** ảnh `tieu_y_1` gen theo cách cũ (một ảnh cả người, nét sổ tay) bị chê "không đúng theme game". Nay mọi tướng làm theo [QUY_TRINH.md](QUY_TRINH.md):
- **tướng là sinh vật kiểu thú nuôi**, nét như hình trận aola;
- **thay tạo hình trên rig vector của aola**, giữ animation: sinh vật mới khác hẳn con gốc, nhưng tay chân trùng rig;
- mỗi dạng có: concept (bóng xám và bản đồ vùng), rồi gen từng nhóm mảnh vẽ đè lên hình gốc.

Luật chọn vẫn như cũ:
- mỗi tướng là một dòng tiến hóa, lên sao thì đổi hình;
- quái thường lấy dòng 2–4 dạng, boss lấy dòng từ 3 dạng.

## Danh sách

Cả 21 dạng dưới đây đều có bản vector (`fightassets/pet<id>.swf`), nên thay được.

| Tướng | File | Vai | Dòng aola | Trạng thái |
|---|---|---|---|---|
| **Giọt Sương** | [thuy/giot_suong.md](thuy/giot_suong.md) | **Tướng đầu tiên** (dòng khởi đầu hệ Nước của aola) | 7 → 8 → 9 | **cả 3 dạng có prompt**, mỗi dạng một file (`giot_suong_1/2/3.md`); gen thử dạng 1 trước |
| Tiểu Y | `thuy/tieu_y.md` | Quái thường | 1319 → 1320 | bản cũ, chờ viết lại |
| Cánh Cụt | `thuy/canh_cut.md` | Quái thường | 1691 → 1692 | bản cũ, chờ viết lại |
| Tám Tay | `thuy/tam_tay.md` | Quái thường | 1053 → 1054 | bản cũ, chờ viết lại |
| Cá Ngựa | `thuy/ca_ngua.md` | Quái thường | 181 → 182 → 183 | bản cũ, chờ viết lại |
| Mập Răng Cưa | `thuy/map_rang.md` | Quái thường | 31 → 32 → 33 | bản cũ, chờ viết lại |
| Lam Quân | `thuy/lam_quan.md` | Boss ải 4 | 1831 → 1832 → 2955 | bản cũ, chờ viết lại |
| Huyền Vũ | `thuy/huyen_vu.md` | Boss ải 8 | 713 → 714 → 715 | bản cũ, chờ viết lại |

- Giọt Sương thay Tiểu Y làm tướng khởi đầu. Concept dạng 1 của nó được duyệt thì dùng làm ảnh mẫu style cho concept các tướng khác.
- Dáng ngoài đổi được và nên khác bản gốc (người dùng 2026-11-01). Tiểu Y, Lam Quân giữ dòng; dáng người của chúng đổi thành dáng sinh vật theo cách này, tay chân vẫn theo rig.
- Gen thử Giọt Sương dạng 1 trước; 7 tướng còn lại viết lại sau khi kết quả thử ổn.
- Các file "bản cũ" theo cách một ảnh cả người kèm ảnh `refs/thuy/REF_*.png`. **Không dùng nữa**; sẽ viết lại từng tướng như Giọt Sương.

## Thư mục

| Đường dẫn | Chứa gì |
|---|---|
| `refs/thuy/<mã dạng>/` | Ảnh đính kèm: `Silhouette.png`, `RegionMap.png`, `Rig_Numbered.png`, `orig/<nhóm>.png` |
| `inbox/<mã dạng>/` | Ảnh GPT trả về: `Concept.png`, `orig_parts/<nhóm>.png` |
| `<aola>/reskin/pet<id>_parts/` | Rig đã tách (Claude dùng) |
| `<aola>/reskin/thuy_<id>/` | Bộ ghép: `regions.json`, `groups.json`, trang so sánh, `export/anim.json` |

Mã dạng là `<tướng>_<dạng>`, ví dụ `giot_suong_1`. `<aola>` = `D:\Aola-20261029T161238Z-1-001\Aola\AolaRipper\AolaRipper`.

## Thứ tự

1. Gen concept `giot_suong_1`, Claude soi và duyệt.
2. Gen 8 nhóm mảnh `giot_suong_1`, Claude ghép, soi, người dùng chỉnh trong trình chỉnh sửa.
3. Concept dạng 2, rồi dạng 3 của Giọt Sương (prompt đã có), rồi lần lượt các tướng khác.
